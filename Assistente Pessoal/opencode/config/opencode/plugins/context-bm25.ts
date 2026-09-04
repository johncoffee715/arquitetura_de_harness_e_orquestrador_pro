/// <reference path="../env.d.ts" />
import type { Plugin } from "@opencode-ai/plugin"

// Autofagia + helenização (2026-08-25) — PERSPECTIVA B:
//   essência do skill harness `context-selector` (BM25 + disclosure progressivo,
//   validada em produção pelo MiMo-Code: skills ranqueadas por BM25)
// helenizada para o OpenCode via hook nativo `experimental.chat.messages.transform`.
//
// Comportamento conservador:
//   - INERTE por padrão (CONTEXT_BM25=1 para ativar — PoLP)
//   - só aparando quando o histórico excede CONTEXT_BM25_BUDGET mensagens
//   - SEMPRE preserva: system prompt, N últimas mensagens (cauda quente),
//     e qualquer mensagem contendo termo da consulta mais recente (BM25)
//   - sem dependências externas (BM25 implementado localmente)

const enabled = () => process.env.CONTEXT_BM25 === "1"
const budget = () => Number(process.env.CONTEXT_BM25_BUDGET ?? 40)
const hotTail = () => Number(process.env.CONTEXT_BM25_TAIL ?? 8)

type Text = { role?: string; parts?: Array<{ type: string; text?: string }> }
const textOf = (m: Text): string =>
  (m.parts ?? []).map((p) => (p.type === "text" ? p.text ?? "" : "")).join(" ")

const tokenize = (s: string): string[] =>
  s.toLowerCase().match(/[a-z0-9áéíóúâêôãõç]{2,}/g) ?? []

// BM25 k1=1.2 b=0.75 sobre o corpus de mensagens do turno
function bm25Top(query: string, docs: string[], keep: number): Set<number> {
  const q = new Set(tokenize(query))
  if (q.size === 0 || docs.length <= keep) return new Set(docs.map((_, i) => i))
  const tok = docs.map(tokenize)
  const df = new Map<string, number>()
  for (const t of tok) for (const term of new Set(t)) df.set(term, (df.get(term) ?? 0) + 1)
  const avg = tok.reduce((a, t) => a + t.length, 0) / tok.length
  const score = tok.map((t, i) => {
    const tf = new Map<string, number>()
    for (const term of t) tf.set(term, (tf.get(term) ?? 0) + 1)
    let s = 0
    for (const term of q) {
      const f = tf.get(term)
      if (!f) continue
      const idf = Math.log((docs.length - (df.get(term) ?? 0) + 0.5) / ((df.get(term) ?? 0) + 0.5) + 1)
      s += idf * ((f * 2.4) / (f + 1.2 * (0.25 + 0.75 * (t.length / avg))))
    }
    return { i, s }
  })
  return new Set(score.sort((a, b) => b.s - a.s).slice(0, keep).map((x) => x.i))
}

export const ContextBm25Plugin: Plugin = async () => {
  if (!enabled()) return {}
  return {
    "experimental.chat.messages.transform": async (input, output) => {
      const msgs = output.messages as unknown as Text[]
      const limit = budget()
      if (!Array.isArray(msgs) || msgs.length <= limit) return

      const head = msgs[0]?.role === "system" ? [msgs[0]] : []
      const body = head.length ? msgs.slice(1) : msgs
      const tailStart = Math.max(0, body.length - hotTail())
      const cold = body.slice(0, tailStart)
      const tail = body.slice(tailStart)

      // consulta = última mensagem de usuário na cauda quente
      const lastUser = [...tail].reverse().find((m) => m.role === "user")
      const keep = bm25Top(textOf(lastUser ?? {}), cold.map(textOf), Math.max(0, limit - tail.length))
      const kept = cold.filter((_, i) => keep.has(i))

      output.messages = [...head, ...kept, ...tail] as typeof output.messages
    },
  }
}
