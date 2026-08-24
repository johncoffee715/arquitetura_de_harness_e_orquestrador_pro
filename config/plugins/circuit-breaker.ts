// Circuit-Breaker Global — implementação executável das regras R6/R18/R48
// Bloqueia a 3ª tentativa CONSECUTIVA IDÊNTICA de um comando bash que falhou 2x.
// Força o modelo a variar a abordagem ou replanejar (anti-tool-loop).
// Formato nativo opencode: export const <Name> = async ({...}) => ({ hooks })

interface BreakerState {
  byCall: Map<string, string> // callID -> hash do comando
  fails: Map<string, number> // hash -> falhas consecutivas na sessão
}

const MAX_CONSECUTIVE_FAILS = 2 // na 3ª tentativa idêntica: bloqueia
const MAX_CALLS_TRACKED = 2000 // teto de memória por processo

const state = new Map<string, BreakerState>() // sessionID -> estado

function getSession(sessionID: string): BreakerState {
  let s = state.get(sessionID)
  if (!s) {
    s = { byCall: new Map(), fails: new Map() }
    state.set(sessionID, s)
    if (state.size > 50) {
      const oldest = state.keys().next().value
      if (oldest) state.delete(oldest)
    }
  }
  return s
}

function normalize(cmd: string): string {
  return cmd.replace(/\s+/g, " ").trim()
}

function looksLikeFailure(text: string): boolean {
  return /command not found|No such file or directory|cannot access|Permission denied|syntax error near|is not recognized/.test(
    text,
  )
}

export const CircuitBreaker = async () => {
  return {
    "tool.execute.before": async (
      input: { tool: string; sessionID: string; callID: string },
      output: { args: any },
    ) => {
      if (input.tool !== "bash") return
      const raw = String(output?.args?.command ?? "")
      if (!raw) return
      const s = getSession(input.sessionID)
      const hash = normalize(raw)
      s.byCall.set(input.callID, hash)
      if (s.byCall.size > MAX_CALLS_TRACKED) {
        const first = s.byCall.keys().next().value
        if (first) s.byCall.delete(first)
      }
      const n = s.fails.get(hash) ?? 0
      if (n >= MAX_CONSECUTIVE_FAILS) {
        throw new Error(
          `[CIRCUIT-BREAKER R18] Este comando idêntico já falhou ${n}x consecutivas nesta sessão e foi BLOQUEADO antes de executar:\n` +
            `  ${hash.slice(0, 160)}\n` +
            `PROIBIDO repetir o mesmo comando esperando resultado diferente.\n` +
            `Obrigatório agora: (1) diagnosticar a causa real do erro com um comando DIFERENTE ` +
            `(ex.: listar o diretório pai, verificar o caminho correto), ou (2) replanejar a task.\n` +
            `Regra: R18 circuit-breaker · R48 monitoramento · anti-loop.`,
        )
      }
    },
    "tool.execute.after": async (
      input: { tool: string; sessionID: string; callID: string },
      output: { title?: string; output?: string; metadata?: any },
    ) => {
      if (input.tool !== "bash") return
      const s = getSession(input.sessionID)
      const hash = s.byCall.get(input.callID)
      if (!hash) return
      s.byCall.delete(input.callID)

      const meta = output?.metadata ?? {}
      const exit = typeof meta.exit === "number" ? meta.exit : undefined
      const text = String(output?.output ?? "")
      const failed =
        (exit !== undefined && exit !== 0) || (exit === undefined && looksLikeFailure(text))

      if (failed) {
        s.fails.set(hash, (s.fails.get(hash) ?? 0) + 1)
      } else {
        s.fails.delete(hash) // sucesso quebra a sequência
      }
    },
  }
}
