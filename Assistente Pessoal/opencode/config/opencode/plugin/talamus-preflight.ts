import type { Plugin } from "@opencode-ai/plugin"

// talamus-preflight.ts — Córtex Sensorial talâmico PRÉ-LLM (R71)
// Captura o contexto BRUTO de todas as mensagens ANTES do dispatch às LLMs
// alvo (gancho canônico pre-LLM: experimental.chat.messages.transform).
//
// COMPORTAMENTO CONSERVADOR (fail-open total):
//   - POR PADRÃO: apenas OBSERVA e loga JSONL em
//     <XDG_STATE_HOME|state>/watcher/talamus-preflight.jsonl — nunca modifica.
//   - TALAMUS_CONDENSE=1: se tokens totais > TALAMUS_BUDGET (default 20000),
//     remove mensagens antigas não-system que NÃO contenham termos da última
//     mensagem de usuário, preservando SEMPRE system + cauda quente (últimas 8).
//   - TALAMUS_DEBUG=1: loga snippet truncado (200 chars) por mensagem.
//   - Nunca lança exceção que quebre a conversa (try/catch + fail-open).
//
// Heurística de intent portada do hooks/kronjob-talamus-filter.py (R71).

type Msg = { info?: { role?: string }; parts?: Array<{ type?: string; text?: string }> }
type Text = { role?: string; parts?: Array<{ type: string; text?: string }> }

const LOG_DEFAULT_DIR =
  (process.env.XDG_STATE_HOME || "/mnt/dados/Assistente Pessoal/opencode/state") + "/watcher"

const logFile = (): string =>
  process.env.TALAMUS_PREFLIGHT_LOG || `${LOG_DEFAULT_DIR}/talamus-preflight.jsonl`

const condenseEnabled = (): boolean => process.env.TALAMUS_CONDENSE === "1"
const budgetTokens = (): number => {
  const n = Number(process.env.TALAMUS_BUDGET ?? 20000)
  return Number.isFinite(n) && n > 0 ? n : 20000
}
const hotTail = (): number => 8
const debugMode = (): boolean => process.env.TALAMUS_DEBUG === "1"

const norm = (s: string): string =>
  s.toLowerCase().normalize("NFD").replace(/\p{M}/gu, "")

const tokenize = (s: string): string[] => norm(s).match(/[a-z0-9][a-z0-9]*/g) ?? []

// ---- intent (porta fiel do kronjob-talamus-filter.py, R71) ----
const KEYWORDS: Record<string, string[]> = {
  PRIMITIVE_HELLO_OR_THANKYOU: [
    "ola", "oi", "bom dia", "boa tarde", "boa noite", "eae", "hey", "hi",
    "hello", "thanks", "obrigado", "thank you", "tchau", "bye", "ok",
  ],
  RAG_DOCUMENTS: [
    "documento", "rag", "contexto", "paragrafo", "relevant", "rerank", "busca em docs",
  ],
  LONG_CHAT_HISTORY: [
    "historico", "history", "conversa anterior", "chat anterior", "thread",
  ],
  RAW_LOGS: [
    "log", "erro", "error", "critical", "stack trace", "exception", "crash",
  ],
  WEB_SCRAPING: [
    "web", "scrap", "html", "scrape", "site", "pagina", "markdown",
  ],
  NEEDLE_EXACT_SEARCH_TRIGGER: [
    "buscar exato", "exact search", "needle", "busca exata", "hash",
  ],
}
const INTENT_ORDER = [
  "PRIMITIVE_HELLO_OR_THANKYOU",
  "NEEDLE_EXACT_SEARCH_TRIGGER",
  "RAG_DOCUMENTS",
  "LONG_CHAT_HISTORY",
  "RAW_LOGS",
  "WEB_SCRAPING",
]

const hasKeyword = (text: string, keywords: string[]): boolean => {
  const n = norm(text)
  const toks = new Set(tokenize(text))
  for (const kw of keywords) {
    if (kw.includes(" ")) {
      if (n.includes(kw)) return true
      continue
    }
    const klen = kw.length
    if (klen < 3) {
      if (toks.has(kw)) return true
    } else if (klen === 3) {
      if (toks.has(kw) || (kw === "log" && toks.has("logs"))) return true
    } else {
      for (const t of toks) if (t.startsWith(kw)) return true
    }
  }
  return false
}

export const classifyIntent = (prompt: string): string => {
  if (!prompt || !prompt.trim()) return "GENERAL"
  for (const intent of INTENT_ORDER) {
    if (hasKeyword(prompt, KEYWORDS[intent])) return intent
  }
  return "GENERAL"
}

export const estimateTokens = (text: string): number => Math.max(1, Math.ceil(text.length / 4))

const textOf = (m: Text): string =>
  (m.parts ?? []).map((p) => (p.type === "text" ? p.text ?? "" : "")).join(" ")

// A API real de messages.transform é { info: { role }, parts }: role aninhada.
const roleOf = (m: Msg | Text | undefined | null): string =>
  m?.info?.role ?? (m as Text | undefined)?.role ?? "?"

const textOfAny = (m: Msg | Text | undefined | null): string =>
  textOf(m as Text)

const hasAnyTerm = (m: Text, terms: Set<string>): boolean => {
  if (terms.size === 0) return true
  return tokenize(textOf(m)).some((t) => terms.has(t))
}

const lastUserText = (msgs: (Msg | Text)[]): string => {
  for (let i = msgs.length - 1; i >= 0; i--) {
    if (roleOf(msgs[i]) === "user") return textOfAny(msgs[i])
  }
  return ""
}

// Condensação BM25-lite por contenção de termos (adaptado do context-bm25.ts):
// SEMPRE preserva system + cauda quente; mensagens frias SEM termos da última
// consulta do usuário são removidas (mais antigas primeiro) até caber no budget;
// mensagens frias COM termos são mantidas por relevância. Ordem preservada.
function condense(msgs: (Msg | Text)[], query: string, budget: number, tailN: number): (Msg | Text)[] {
  const kept = new Set<number>()  // índices em `msgs` que permanecem

  for (let i = 0; i < msgs.length; i++) {
    const m = msgs[i]
    if (!m) continue
    if (roleOf(m) === "system") {
      kept.add(i) // system: sempre preservada
      continue
    }
  }
  // cauda quente (últimas tailN não-system): sempre preservada
  let nonSystem = 0
  for (let i = msgs.length - 1; i >= 0 && nonSystem < tailN; i--) {
    if (roleOf(msgs[i]) !== "system") {
      kept.add(i)
      nonSystem++
    }
  }

  const uses = (idx: number): number => estimateTokens(textOfAny(msgs[idx]))
  let used = 0
  for (const i of kept) used += uses(i)

  // frias sem termos (candidatas à remoção), mais novas primeiro
  const terms = new Set(tokenize(query))
  const dropOrder: number[] = []
  for (let i = msgs.length - 1; i >= 0; i--) {
    const m = msgs[i]
    if (!m || kept.has(i)) continue
    if (!hasAnyTerm(m as Text, terms)) dropOrder.push(i)
  }
  for (const i of dropOrder) {
    if (used + uses(i) <= budget) {
      kept.add(i)
      used += uses(i)
    }
  }

  return msgs.filter((_, i) => kept.has(i) || hasAnyTerm(msgs[i] as Text, terms))
}

function rolesOf(msgs: Msg[]): string[] {
  return msgs.map((m) => m?.info?.role ?? "?")
}

function textAll(m: Msg): string {
  return (m?.parts ?? [])
    .map((p) => (p?.type === "text" ? p?.text ?? "" : ""))
    .join(" ")
}

function snippet(m: Msg, len: number): string {
  return textAll(m).slice(0, len)
}

export const TalamusPreflight: Plugin = async () => {
  return {
    "experimental.chat.messages.transform": async (input, output) => {
      try {
        const msgs = (output?.messages ?? []) as Msg[]
        if (!Array.isArray(msgs)) return
        const sessionID = (input as { sessionID?: string })?.sessionID ?? "unknown"
        const ts = new Date().toISOString()
        const tokens = msgs
          .map((m) => estimateTokens(textAll(m)))
          .reduce((a, b) => a + b, 0)
        const textAllText = msgs.map(textAll).join("\n")
        const intent = classifyIntent(lastUserText(msgs) || textAllText)
        const action =
          intent === "PRIMITIVE_HELLO_OR_THANKYOU"
            ? "DIRECT_RESPONSE"
            : tokens > budgetTokens()
              ? "CONDENSE"
              : "DISPATCH_VRAM"

        const entry: Record<string, unknown> = {
          ts,
          source: "plugin/talamus-preflight.ts",
          sessionID,
          messages: msgs.length,
          tokens_estimated: tokens,
          roles: rolesOf(msgs),
          intent,
          action,
        }
        if (condenseEnabled()) entry.budget = budgetTokens()

        // Condensação ONLY com TALAMUS_CONDENSE=1 e orçamento estourado.
        if (condenseEnabled() && tokens > budgetTokens() && msgs.length > hotTail() + 1) {
          const before = msgs.length
          const out = condense(msgs, lastUserText(msgs) || textAllText, budgetTokens(), hotTail())
          if (out.length < before) {
            output.messages = out as typeof output.messages
            entry.condensed = before - out.length
          }
        }

        if (debugMode()) {
          entry.debug = msgs.map((m) => ({
            role: m?.info?.role ?? "?",
            snippet: snippet(m, 200),
          }))
        }

        const fs = await import("fs")
        fs.mkdirSync(logFile().replace(/\/[^/]+$/, ""), { recursive: true })
        fs.appendFileSync(logFile(), JSON.stringify(entry) + "\n")
      } catch (err) {
        // Fail-open absoluto: o Tálamos nunca pode derrubar a conversa (R71).
        try {
          const fs = await import("fs")
          fs.appendFileSync(
            logFile(),
            JSON.stringify({ ts: new Date().toISOString(), source: "plugin/talamus-preflight.ts", error: String(err) }) + "\n"
          )
        } catch {}
      }
    },
  }
}