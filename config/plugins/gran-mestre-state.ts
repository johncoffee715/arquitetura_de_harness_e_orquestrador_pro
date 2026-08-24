// Gran-Mestre State — garantia de estado durável (doc §11 · R47/R48)
// harness_state.json: fase atual, SHA de segurança, gates, status.
// Regra: status="failed" BLOQUEIA bash/edit até `gm-validate` assinar o retorno.
// Atômico (tmp+rename), defensivo, nunca derruba a sessão por erro interno.

import { existsSync, readFileSync, mkdirSync, renameSync, writeFileSync } from "node:fs"
import { dirname } from "node:path"

const STATE_PATH =
  process.env.GM_STATE_FILE ?? "/mnt/dados/harness/state/harness_state.json"

interface HarnessState {
  version: number
  status: "idle" | "running" | "failed" | "done"
  phase?: string
  task?: string
  sha?: string
  gate?: string | null
  updatedAt: string
  validateToken?: string | null
}

function now(): string {
  return new Date().toISOString()
}

function readState(): HarnessState | null {
  try {
    if (!existsSync(STATE_PATH)) return null
    return JSON.parse(readFileSync(STATE_PATH, "utf-8")) as HarnessState
  } catch {
    return null
  }
}

function writeState(patch: Partial<HarnessState>): void {
  try {
    const next = { ...(readState() ?? {}), ...patch, updatedAt: now() }
    next.version = 1
    mkdirSync(dirname(STATE_PATH), { recursive: true })
    const tmp = `${STATE_PATH}.tmp-${process.pid}`
    writeFileSync(tmp, JSON.stringify(next, null, 2))
    renameSync(tmp, STATE_PATH)
  } catch {
    // estado é best-effort: nunca quebrar a sessão por falha de escrita
  }
}

function isBlocked(s: HarnessState | null): boolean {
  return s?.status === "failed" && !s?.validateToken
}

export const GranMestreState = async () => {
  return {
    "tool.execute.before": async (
      input: { tool: string; sessionID: string; callID: string },
      _output: { args: any },
    ) => {
      if (input.tool !== "bash" && input.tool !== "edit") return
      const s = readState()
      if (!isBlocked(s)) return
      throw new Error(
        `[GM-STATE] Pipeline marcado FAILED em ${s!.updatedAt} (fase ${s!.phase ?? "?"}, task ${s!.task ?? "?"}).\n` +
          `Execução de ${input.tool} BLOQUEADA até validação.\n` +
          `Rode: gm-validate  (assina retorno após conferir git status/diff)\n` +
          `Regra: doc §11 garantia de estado · rollback máx 1 · R47`,
      )
    },

    "tool.execute.after": async (
      input: { tool: string; sessionID: string; callID: string },
      output: { title?: string; output?: string; metadata?: any },
    ) => {
      if (input.tool !== "bash") return
      const title = String(output?.title ?? "")
      // captura de SHA de segurança (F3): qualquer rev-parse HEAD bem-sucedido
      if (/git\s+rev-parse\s+HEAD/.test(title)) {
        const out = String(output?.output ?? "").trim()
        if (/^[0-9a-f]{7,40}$/.test(out)) writeState({ sha: out })
      }
      // heartbeat barato em comandos git (prova de atividade)
      if (/^git(\s|$)/.test(title.trim())) writeState({ status: "running" })
    },

    event: async (input: { type?: string; properties?: any }) => {
      const t = String(input?.type ?? "")
      if (t === "session.idle") {
        const s = readState()
        if (s && s.status === "running") writeState({ status: "idle" })
      }
      // gate pendente ≈ permission.ask (G1-G4 humanos passam por aqui)
      if (t === "permission.ask") {
        const s = readState()
        if (s && (s.status === "running" || s.status === "idle"))
          writeState({ gate: "pending" })
      }
    },
  }
}
