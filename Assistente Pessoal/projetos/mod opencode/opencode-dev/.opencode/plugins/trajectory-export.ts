/// <reference path="../env.d.ts" />
import type { Plugin } from "@opencode-ai/plugin"
import { appendFile, mkdir } from "node:fs/promises"
import path from "node:path"

// Autofagia + helenização (2026-08-25) — PERSPECTIVA A:
//   dsh community `trajectory-logger` (JSONL append-only + replay)
//   hermes-agent `trajectory_compressor.py` (trajetória como dado)
//   MiMo-Code trajectory SQLite (fonte da verdade p/ dream/distill)
// Helenizada para o OpenCode como plugin consumidor do bus nativo de hooks.
// Ativação explícita: TRAJECTORY_EXPORT=1 (inerte por padrão, PoLP).
// Refinamentos pós-refutação A2A (2026-08-26): redact por família de chave,
// escrita serializada (ordem causal), mkdir lossy.

const enabled = () => process.env.TRAJECTORY_EXPORT === "1"

// Famílias atuais de credenciais; truncar no 1º hífen interno evita
// falsos completos em formatos segmentados (sk-proj-, sk-ant-api03-…)
const REDACT =
  /\b((?:sk-(?:ant|proj|svcacct)|ghp_|gho_|github_pat_|xox[bpoas]-|glpat-|npm_|AKIA|AIza)[A-Za-z0-9_-]{6,}|sk-[A-Za-z0-9]{16,})/g

const redact = (value: unknown): unknown => {
  if (typeof value === "string") {
    return value.replace(REDACT, (m) => m.slice(0, 10) + "***")
  }
  if (Array.isArray(value)) return value.map(redact)
  if (value && typeof value === "object") {
    const out: Record<string, unknown> = {}
    for (const [k, v] of Object.entries(value)) out[k] = redact(v)
    return out
  }
  return value
}

export const TrajectoryExportPlugin: Plugin = async ({ directory, worktree }) => {
  if (!enabled()) return {}

  try {
    const root = worktree ?? directory ?? process.cwd()
    const dir = path.join(root, ".opencode", "trajectory")
    await mkdir(dir, { recursive: true })
    const file = path.join(dir, `trajectory_${new Date().toISOString().replace(/[:.]/g, "-")}.jsonl`)
    let seq = 0
    // serializa appends concorrentes preservando ordem causal no arquivo
    let chain: Promise<void> = Promise.resolve()
    const write = (type: string, data: Record<string, unknown>) => {
      const row = JSON.stringify({ ts: new Date().toISOString(), seq: seq++, type, ...redact(data) })
      chain = chain.then(() => appendFile(file, row + "\n", { encoding: "utf-8" })).catch(() => {})
    }

    write("session.start", { directory, worktree })

    return {
      "tool.execute.before": async (input, output) => {
        write("tool.execute.before", { callID: input.callID, tool: input.tool, args: output.args })
      },
      "tool.execute.after": async (input, output) => {
        write("tool.execute.after", { callID: input.callID, tool: input.tool, result: redact(output) })
      },
      "chat.message": async (input) => {
        write("chat.message", { ...input })
      },
      "permission.ask": async (input, output) => {
        write("permission.ask", { permission: input.permission, patterns: input.patterns, status: output.status })
      },
    }
  } catch {
    // lossy success: falha ao preparar retenção nunca impede a sessão
    return {}
  }
}
