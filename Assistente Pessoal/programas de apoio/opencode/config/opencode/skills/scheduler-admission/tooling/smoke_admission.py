"""Smoke test for scheduler-admission (stdlib only, deterministic)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tooling.admission import (
    CapacityContract, Request, ActiveSnapshot,
    make_admission_protection, rebind_admission_protection,
    protection_has_live_donor, persistent_backfill_is_authorized,
    MachineCostModel, resolve_cost_model, resolve_sampling,
    schedule_fifo_with_backfill,
)

fails = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


cap = CapacityContract(max_context=32768, kv_capacity=10000,
                       max_concurrency=2, headroom_tokens=1000)
act = [ActiveSnapshot(rid=1, epoch=7, reserved=8000)]
prot = make_admission_protection(7, 99, 3, act)
check(prot.donor_ids == [1], "donors freeze incumbents")
check(protection_has_live_donor(prot, act), "live donor detected")
rebind_admission_protection(prot, [], 4, set())
check(prot.donor_ids == [] and prot.resource_revision == 4, "rebind drops dead donors")

# current-epoch persistent borrower never promoted to donor
act2 = [ActiveSnapshot(rid=1, epoch=7, reserved=8000),
        ActiveSnapshot(rid=2, epoch=7, reserved=500, persistent=True)]
prot2 = make_admission_protection(7, 99, 5, act2)
rebind_admission_protection(prot2, act2, 5, {2})
check(2 not in prot2.donor_ids, "current-epoch persistent never donor")

# backfill: head needs 8000, free = 9000-8500 = 500, donors hold 8500
cap2 = CapacityContract(kv_capacity=10000, max_concurrency=3, headroom_tokens=1000)
prot3 = make_admission_protection(7, 99, 5, act2)
small = Request(rid=10, tokens_needed=400)
big = Request(rid=11, tokens_needed=5000)
check(persistent_backfill_is_authorized(prot3, small, act2, cap2, 5, 8000) is True,
      "backfill authorized: fits now and head runnable after donors release")
check(persistent_backfill_is_authorized(prot3, small, act2, cap2, 6, 8000) is False,
      "stale proof revision denies")
act3 = [ActiveSnapshot(rid=1, epoch=7, reserved=1000)]
prot4 = make_admission_protection(7, 99, 5, act3)
ok = persistent_backfill_is_authorized(prot4, small, act3, cap2, 5, 8000)
check(ok is True, "backfill authorized when head stays runnable")

# cost model: max(batch + ops*op, bytes*ns/byte)
m = MachineCostModel()
check(m.transfer_ns(100, 2) == 100, "transfer byte-bound default")
m2 = resolve_cost_model({"transfer": {"batch_ns": 500, "operation_ns": 100,
                                      "ns_per_byte_q32": 1 << 32}})
check(m2.transfer_ns(100, 2) == 700, "transfer op-bound preset override")
check(m2.prefill_ns(10) == 10, "prefill token linear")

# layered sampling
defaults = {"default": {"temperature": 0.7, "top_p": 0.9},
            "thinking": {"temperature": 1.0, "top_p": 0.95}}
r = resolve_sampling(defaults, "thinking", {"top_p": 0.5}, fresh_seed=42)
check(r == {"temperature": 1.0, "top_p": 0.5, "seed": 42}, "layers: preset<override, seed fresh")
g = resolve_sampling(defaults, "default", None, greedy=True, fresh_seed=7)
check(g["temperature"] == 0.0 and g["seed"] == 7, "greedy forces temp 0")

# end-to-end: head needs 8500 (blocked: free 8000; runnable after donor frees 1000)
pend = [Request(rid=99, tokens_needed=8500), Request(rid=10, tokens_needed=400),
        Request(rid=11, tokens_needed=9000)]
adm = schedule_fifo_with_backfill(cap2, act3, pend, 5, 7)
check(adm == [10], f"fifo head blocked, backfill admits small only (got {adm})")

print("SMOKE " + ("OK" if not fails else f"FAILED {fails}"))
raise SystemExit(1 if fails else 0)
