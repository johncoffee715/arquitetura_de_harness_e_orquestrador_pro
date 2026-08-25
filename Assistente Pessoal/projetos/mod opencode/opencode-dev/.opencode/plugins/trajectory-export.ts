/// <reference path="../env.d.ts" />
import type { Plugin } from "@opencode-ai/plugin"
import { appendFile, mkdir } from "node:fs/promises"
import path from "node:path"

// Autofagia + helenização (2026-08-25): essência absorvida de
//   - dsh community `trajectory-logger` (JSONL append-only + replay)
//   - hermes-agent `trajectory_compressor.py` (trajetória como dado)
//   - MiMo-Code trajectory SQLite (fonte da verdade p/ dream/distill)
// Helenizada para o OpenCode como plugin consumidor do bus nativo de hooks
// (tool.execute.*, chat.message, permission.ask) — zero mudança no core.
// Ativação explícita: TRAJECTORY_EXPORT=1 (inerte por padrão, PoLP).

const enabled = () => process.env.TRAJECTORY_EXPORT === "1"

export const TrajectoryExportPlugin: Plugin = async ({ directory, worktree }) => {
  if (!enabled()) return {}

  const root = worktree ?? directory ?? process.cwd()
  const dir = path.join(root, ".opencode", "trajectory")
  await mkdir(dir, { recursive: true })
  const file = path.join(dir, `trajectory_${new Date().toISOString().replace(/[:.]/g, "-")}.jsonl`)
  let seq = 0

  // Sanitização mínima: nunca exportar segredos ambientais em texto plano
  const redact = (value: unknown): unknown => {
    if (typeof value === "string") return value.replace(/(sk-[A-Za-z0-9]{8})[A-Za-z0-9]+/g, "$1***")
    return value
  }
  const write = async (type: string, data: Record<string, unknown>) => {
    const row = JSON.stringify({ ts: new Date().toISOString(), seq: seq++, type, ...data })
    try {
      await appendFile(file, `${redact(row)}\n`, { encoding: "utf-8" })
    } catch {
      // CONTEXT.md: falha de retenção não pode transformar sucesso em erro (lossy success)
    }
  }

  await write("session.start", { directory, worktree })

  return {
    "tool.execute.before": async (input, output) => {
      await write("tool.execute.before", { callID: input.callID, tool: input.tool, args: output.args })
    },
    "tool.execute.after": async (input, output) => {
      await write("tool.execute.after", { callID: input.callID, tool: input.tool })
    },
    "chat.message": async (input) => {
      await write("chat.message", { ...input })
    },
    "permission.ask": async (input, output) => {
      await write("permission.ask", { permission: input.permission, patterns: input.patterns, status: output.status })
    },
  }
}
