// ecc-compact-gate.ts — REGRA GLOBAL: agenda ecc-compact-gate.sh no PreCompact.
//
// PreCompact real do OpenCode = evento "experimental.session.compacting"
// (ver packages/opencode/src/session/compaction.ts -> plugin.trigger(...)).
// settings.json é editor-level e não carrega hooks; hooks de compactação só
// existem via plugin. Este plugin roda o gate ANTES da compactação, garantindo
// ARMAZENA + COMPACTA + LIMPA sem bloquear o fluxo (fire-and-forget idempotente).

const COMPACT_GATE = "/mnt/dados/opencode/claude/hooks/ecc-compact-gate.sh"

export const EccCompactGate = async (_ctx: unknown) => {
  return {
    "experimental.session.compacting": async (_input: unknown, _output: unknown) => {
      try {
        const { exec } = await import("node:child_process")
        exec(`bash "${COMPACT_GATE}"`, { env: { ...process.env } }, () => {
          // nunca bloqueia nem derruba a compactação
        })
      } catch {
        // silent: o gate nunca deve quebrar o ciclo de compactação
      }
    },
  }
}
