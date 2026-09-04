/// <reference path="../env.d.ts" />
import type { Plugin } from "@opencode-ai/plugin"
import { appendFile, mkdir } from "node:fs/promises"
import path from "node:path"
import { verdict, isAllowedWritePath } from "../scripts/guard-engine"

// guard-gap-p5.ts — GAP-P5 (fechado 2026-08-26; escopo corrigido 2026-08-30): camada 2 do enforcement do orquestrador.
// Camada 1 = `permission` nativo no frontmatter de agent/gran-mestre.md (por agente, last-match-wins).
// Camada 2 = plugin GLOBAL (auto-carregado de plugins/ no BOOT da sessão): fail-closed de
// bash-destrutivo + auditoria JSONL pós-tool. Lógica pura em guard-engine.ts (testável: node --test).
// ESCOPO DE ESCRITA PERMITIDA (guard-engine.isAllowedWritePath): governança (CONTEXT.md, decision-log,
// vault cerelebro, config/opencode, state/watcher) + harness operacional (scripts/tools/tests/state/bin/
// templates/data) + configs globais (~/.opencode, ~/.config/opencode) + sandbox /tmp/opencode.
// Código de TERCEIROS (repos/, cactus-build/, llama.cpp/, cache/, projetos/, tranqueiras/) = NUNCA.
// EXCEÇÃO legitimada: `git reset --hard <ativa>` = rollback R18 (única escrita produtiva permitida).
// PoLP: bloqueia apenas os padrões destrutivos abaixo. Sandbox SO = fora do escopo (declarado).

const AUDIT_DIR = "/mnt/dados/Assistente Pessoal/opencode/state/watcher"
const AUDIT_LOG = path.join(AUDIT_DIR, "guard-gap-p5.jsonl")

async function audit(entry: Record<string, unknown>) {
  try {
    await mkdir(AUDIT_DIR, { recursive: true })
    await appendFile(AUDIT_LOG, JSON.stringify({ ts: new Date().toISOString(), ...entry }) + "\n")
  } catch {
    // fail-open apenas na telemetria; nunca bloqueia por causa da auditoria
  }
}

export const GuardGapP5Plugin: Plugin = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      const t = input.tool
      if (t === "bash") {
        const cmd: string = output.args?.command ?? ""
        const v = verdict(cmd)
        if (v.verdict === "deny") {
          await audit({ tool: t, sessionID: input.sessionID, callID: input.callID, cmd: cmd.slice(0, 200), action: "deny", why: v.why })
          throw new Error(`[guard-gap-p5] comando destrutivo bloqueado (${v.why}). Delegação R1 ou rollback com SHA salvo (R18)?`)
        }
        if (v.verdict === "allow-r18" || v.verdict === "allow-gov") {
          await audit({ tool: t, sessionID: input.sessionID, callID: input.callID, cmd: cmd.slice(0, 200), action: v.verdict, why: v.why })
        }
        return
      }
      if (t === "edit") {
        const p: string =
          output.args?.filePath ?? output.args?.path ?? output.args?.file ?? ""
        if (!isAllowedWritePath(p)) {
          await audit({ tool: t, sessionID: input.sessionID, callID: input.callID, path: p, action: "deny", why: "path fora do workdir e fora da governança" })
          throw new Error("[guard-gap-p5] escrita fora do workdir e fora da governança (vault/config) — use caminho permitido ou delegação.")
        }
        await audit({ tool: t, sessionID: input.sessionID, callID: input.callID, path: p, action: "allow" })
        return
      }
    },
    "tool.execute.after": async (input) => {
      if (["bash", "edit"].includes(input.tool)) {
        await audit({ tool: input.tool, sessionID: input.sessionID, callID: input.callID, action: "after" })
      }
    },
  }
}
