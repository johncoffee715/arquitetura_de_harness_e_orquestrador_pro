"""Admission + cost + sampling patterns absorbed from NInfer (Apache-2.0).

Pure-stdlib reference implementation. No GPU, no torch, no network.
Covers: FIFO head with protected backfill (epoch/donor proofs),
context transfer/prefill cost model, layered sampling resolution,
startup-fixed capacity contract.
"""
from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------- capacity
@dataclass
class CapacityContract:
    max_context: int = 32768
    kv_capacity: int = 32768          # shared pool, tokens
    max_concurrency: int = 2          # 1..8, startup-fixed
    max_pending: int = 16
    headroom_tokens: int = 1024       # sizing headroom, never loaned

    def usable(self) -> int:
        return max(0, self.kv_capacity - self.headroom_tokens)


# ---------------------------------------------------------------- requests
@dataclass
class Request:
    rid: int
    tokens_needed: int
    persistent: bool = False          # wants checkpoint retention
    epoch: int = 0


@dataclass
class ActiveSnapshot:
    rid: int
    epoch: int
    reserved: int                     # tokens reserved in shared pool
    persistent: bool = False


# ------------------------------------------------------- admission shield
@dataclass
class AdmissionProtection:
    epoch_id: int
    head_request_id: int
    resource_revision: int
    donor_ids: list[int] = field(default_factory=list)


def make_admission_protection(epoch_id: int, head_request_id: int,
                              resource_revision: int,
                              active: list[ActiveSnapshot]) -> AdmissionProtection:
    """Freeze incumbent donor identities whose release may unblock the head."""
    donors = [a.rid for a in active if a.rid != head_request_id]
    return AdmissionProtection(epoch_id, head_request_id, resource_revision, donors)


def rebind_admission_protection(prot: AdmissionProtection,
                                active: list[ActiveSnapshot],
                                resource_revision: int,
                                current_epoch_persistent: set[int]) -> AdmissionProtection:
    """Drop dead donors; NEVER promote current-epoch persistent borrowers."""
    live = {a.rid for a in active}
    prot.donor_ids = [d for d in prot.donor_ids
                      if d in live and d not in current_epoch_persistent]
    prot.resource_revision = resource_revision
    return prot


def protection_has_live_donor(prot: AdmissionProtection,
                              active: list[ActiveSnapshot]) -> bool:
    live = {a.rid for a in active}
    return any(d in live for d in prot.donor_ids)


def free_tokens(cap: CapacityContract, active: list[ActiveSnapshot]) -> int:
    return cap.usable() - sum(a.reserved for a in active)


def persistent_backfill_is_authorized(prot: AdmissionProtection,
                                      candidate: Request,
                                      active: list[ActiveSnapshot],
                                      cap: CapacityContract,
                                      program_proof_revision: int,
                                      head_need: int) -> bool:
    """A backfill is safe iff it fits in free space AND the head stays runnable
    once frozen donors release (stale proof revision => deny)."""
    if program_proof_revision != prot.resource_revision:
        return False
    live = {a.rid for a in active}
    releasable = sum(a.reserved for a in active if a.rid in prot.donor_ids)
    head_runnable = (free_tokens(cap, active) + releasable) >= head_need
    fits_now = free_tokens(cap, active) >= candidate.tokens_needed
    still_runnable_after = (free_tokens(cap, active) - candidate.tokens_needed
                            + releasable) >= head_need
    _ = live
    return head_runnable and fits_now and still_runnable_after


# ------------------------------------------------------------- cost model
@dataclass
class TransferCost:
    batch_ns: int = 0
    operation_ns: int = 0
    ns_per_byte_q32: int = 1 << 32  # 1.0 ns/byte in Q32


@dataclass
class PrefillCost:
    chunk_ns: int = 0
    token_ns_q32: int = 1 << 32
    attention_pair_ns_q32: int = 0


@dataclass
class MachineCostModel:
    transfer: TransferCost = field(default_factory=TransferCost)
    prefill: PrefillCost = field(default_factory=PrefillCost)

    def transfer_ns(self, payload_bytes: int, copy_ops: int) -> int:
        t = self.transfer
        per_op = t.batch_ns + copy_ops * t.operation_ns
        per_byte = (payload_bytes * t.ns_per_byte_q32) >> 32
        return max(per_op, per_byte)

    def prefill_ns(self, tokens: int, attention_pairs: int = 0) -> int:
        p = self.prefill
        return p.chunk_ns + ((tokens * p.token_ns_q32) >> 32) \
            + ((attention_pairs * p.attention_pair_ns_q32) >> 32)


def resolve_cost_model(presets: dict | None) -> MachineCostModel:
    """Generic numerical defaults always exist; hardware presets override."""
    m = MachineCostModel()
    if not presets:
        return m
    if "transfer" in presets:
        for k, v in presets["transfer"].items():
            setattr(m.transfer, k, v)
    if "prefill" in presets:
        for k, v in presets["prefill"].items():
            setattr(m.prefill, k, v)
    return m


# ------------------------------------------------------- layered sampling
def resolve_sampling(defaults: dict, mode: str,
                     overrides: dict | None,
                     greedy: bool = False,
                     fresh_seed: int = 0) -> dict:
    """Model preset supplies every omitted field; process overrides sit in the
    middle; request fields win. Omitted seed -> fresh random (here: caller
    supplied fresh_seed). --greedy forces temperature 0 (exact argmax)."""
    out = dict(defaults.get(mode, defaults.get("default", {})))
    out.update(overrides or {})
    if greedy:
        out["temperature"] = 0.0
    out.setdefault("seed", fresh_seed)
    return out


# -------------------------------------------------------------- scheduler
def schedule_fifo_with_backfill(cap: CapacityContract,
                                active: list[ActiveSnapshot],
                                pending: list[Request],
                                revision: int,
                                epoch: int) -> list[int]:
    """Return admitted rids in order. Head first if it fits; else protected
    backfill scan over the rest (persistent borrowers of the current epoch
    are never donors)."""
    admitted: list[int] = []
    if not pending:
        return admitted
    head = pending[0]
    used = sum(a.reserved for a in active)
    if used + head.tokens_needed <= cap.usable() and \
            len(active) + len(admitted) < cap.max_concurrency:
        return [head.rid]
    prot = make_admission_protection(epoch, head.rid, revision, active)
    cur_persistent = {a.rid for a in active if a.persistent and a.epoch == epoch}
    prot = rebind_admission_protection(prot, active, revision, cur_persistent)
    sim_active = list(active)
    for cand in pending[1:]:
        if len(sim_active) >= cap.max_concurrency:
            break
        if persistent_backfill_is_authorized(prot, cand, sim_active, cap,
                                             revision, head.tokens_needed):
            admitted.append(cand.rid)
            sim_active.append(ActiveSnapshot(cand.rid, epoch,
                                             cand.tokens_needed, cand.persistent))
    return admitted
