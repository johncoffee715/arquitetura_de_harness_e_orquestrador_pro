// Gran-Mestre State — garantia de estado durável (doc §11 · R47/R48)
// harness_state.json: fase atual, SHA de segurança, gates, status.
// Regra: status="failed" BLOQUEIA bash/edit até `gm-validate` assinar o retorno.
// Atômico (tmp+rename), defensivo, nunca derruba a sessão por erro interno.

import { existsSync, readFileSync, statSync, mkdirSync, renameSync, writeFileSync } from "node:fs"
import { dirname } from "node:path"

const STATE_PATH =
  process.env.GM_STATE_FILE ?? "/mnt/dados/harness/state/harness_state.json"

// R70 window-guard: bytes lidos acumulados por sessão (leitura extensa = janela perdida)
const READ_LIMIT_BYTES = 262144
const readBytes = new Map<string, number>()

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
      if (input.tool === "read" || input.tool === "grep") {
        const path = String(_output?.args?.path ?? _output?.args?.pattern ?? "")
        let size = 32768 // grep: estimativa default
        try { size = statSync(path.startsWith("/") ? path : path).size } catch {}
        const acc = (readBytes.get(input.sessionID) ?? 0) + size
        if (acc > READ_LIMIT_BYTES && size > 32768) {
          throw new Error(
            `[R70 WINDOW-GUARD] Leitura acumulada ${(acc/1048576).toFixed(1)}MB > 256KB nesta sessão — janela do primário em risco.\n` +
            `ARQUIVO: ${path} (${(size/1024).toFixed(0)}KB) — LEITURA NEGADA.\n` +
            `OBRIGATÓRIO: delegue via task ao subagente explore/general: "Leia ${path} e responda APENAS: <sua pergunta>" — consuma o resumo (<2KB). R70: o primário não lê matéria-prima.`)
        }
        readBytes.set(input.sessionID, acc)
        return
      }
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
      // R70-v2 (vetor 2): output pesado NUNCA entra na janela do primário — vira head+tail
      if (input.tool === "read" || input.tool === "bash" || input.tool === "grep") {
        const out = String(output?.output ?? "")
        const nLines = out ? out.split("\n").length : 0
        if (out.length > 131072 || nLines > 2000) {
          const head = out.slice(0, 4096)
          const tail = out.slice(-2048)
          if (output) output.output =
            head + `\n[R70-v2: OUTPUT ${Math.round(out.length/1024)}KB/${nLines} linhas TRUNCADO — integral disponível ao subagente; delegue a análise se necessário]\n` + tail
        }
      }
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
