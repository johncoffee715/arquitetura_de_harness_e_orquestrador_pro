// guard-engine.ts — lógica pura e testável do guard-gap-p5 (sem dependências de runtime).
// Extraída em 2026-08-26 para permitir TDD RED→GREEN (R51). NÃO importa opencode/node: basta
// node --test para validar cada padrão de segurança em isolamento (allow/deny/allow-gov/allow-r18).

export type Verdict = "allow" | "deny" | "allow-gov" | "allow-r18"

export interface Rule { re: RegExp; label: string; govAware?: boolean; destGroup?: number }

// Paths com escape de shell (`Assistente\ Pessoal`) quebram âncoras e extração de destino.
// TODO comando/argumento é NORMALIZADO (unescape) antes de qualquer casamento de padrão.
export function unescapePath(p: string): string {
  return p.replace(/\\(.)/g, "$1")
}

export const DESTRUCTIVE_PATTERNS: Rule[] = [
  { re: /^\s*python3\s+-c\b.*\b(shutil\.rmtree|os\.remove|os\.unlink|pathlib.*unlink)\b.*/, label: "python3 -c destrutivo (bypass)" },
  { re: /^\s*rm\s+(-[a-zA-Z]*[fF]|--force)\b.*/, label: "rm -f/--force" },
  { re: /^\s*git\s+clean\s+(-[a-zA-Z]*[fd]|--force|-fdx)\b.*/, label: "git clean (delete worktree)" },
  { re: /^\s*git\s+checkout\s+--\s+.*/, label: "git checkout -- (descarta mudanças)" },
  { re: /^\s*git\s+reset\s+--hard\s*$/, label: "git reset --hard SEM SHA" },
  { re: /^\s*git\s+reset\s+(?!--hard\b).*/, label: "git reset não-hard" },
  { re: /^\s*truncate\s+.*/, label: "truncate (zerar arquivo)" },
  { re: /^\s*dd\s+of=.*/, label: "dd of= (zerar bloco)" },
  { re: /^\s*(sed|perl|python3)\s+-i\b(?:.*?\s+)?((?:"[^"]*")|(?:'[^']*')|(?:\\.|\S)+)\s*$/, label: "edição in-place", govAware: true, destGroup: 2 },
  { re: /^\s*tee\s+(?:.*\s)?((?:"[^"]*")|(?:'[^']*')|(?:\\.|\S)+)\s*$/, label: "tee p/ arquivo", govAware: true },
  { re: /^\s*(cat|echo|printf)\b.*(>>?|>)\s+((?:"[^"]*")|(?:'[^']*')|(?:\\.|\S)+)\s*.*/, label: "redirecionamento p/ arquivo", govAware: true, destGroup: 3 },
  { re: /^\s*(cp|mv)\s+.*\.(py|js|ts|rs|go|c|cpp|h|json|jsonc|md|sh)\s+.*(src|lib|app|packages|test)/, label: "cp/mv sobre árvore de código" },
  { re: /^\s*(sh|bash|zsh)\s+-c\b.*\b(rm|mv|dd|truncate|tee|sed\s+-i|git\s+clean|git\s+checkout\s+--)\b.*/, label: "shell -c destrutivo (bypass)" },
]

export const LEGIT_DESTRUCTIVE: Rule[] = [
  { re: /^\s*git\s+reset\s+--hard\s+\S+\s*$/, label: "rollback R18" },
]

export function segment(cmd: string): string[] {
  return cmd.split(/;\s*|\s*&&\s*|\s*\|\s*/).map((s) => s.trim())
}

// Roots de código de TERCEIROS dentro do ecossistema (repos upstream, builds, workspaces):
// escrita NUNCA permitida fora do fluxo de delegação/validação.
export const THIRD_PARTY_ROOTS: RegExp[] = [
  /^\/mnt\/dados\/Assistente Pessoal\/opencode\/(repos|cactus-build|llama\.cpp|cache)(\/|$)/,
  /^\/mnt\/dados\/Assistente Pessoal\/(projetos|tranqueiras)(\/|$)/,
]

// Roots OPERACIONAIS do próprio harness (código do orquestrador, estado e artefatos):
// escrita legítima da forja/helenização — governança estendida além de config/opencode.
export const HARNESS_OP_ROOTS: RegExp[] = [
  /^\/mnt\/dados\/Assistente Pessoal\/opencode\/(scripts|tools|tests|state|bin|templates|data)(\/|$)/,
]

// Config GLOBAL do runtime opencode (qualquer instância, mesmo fora do ecossistema /mnt/dados).
export const GLOBAL_CFG_ROOTS: RegExp[] = [
  /^\/home\/johncoffee\/\.opencode(\/|$)/,
  /^\/home\/johncoffee\/\.config\/opencode(\/|$)/,
]

export function isGovPath(p: string): boolean {
  const q = unescapePath(p)
  // GOVERNANÇA REAL (artefatos de estado + scaffolding DO HARNESS sob config/opencode).
  // Ancorado: exige config/opencode OU os artefatos de estado/log OU vault.
  return (
    q.startsWith("CONTEXT.md") ||
    /CONTEXT\.md$/.test(q) ||
    /decision-log/.test(q) ||
    /cerebro com IA/.test(q) ||
    /opencode\/config\/opencode($|\/)/.test(q) ||
    /state\/watcher/.test(q)
  )
}

export function isSandboxTmp(p: string): boolean {
  const q = unescapePath(p)
  return q.startsWith("/tmp/opencode/") || q.startsWith("/tmp/opencode")
}

export function isAllowedWritePath(p: string): boolean {
  const q = unescapePath(p)
  for (const re of THIRD_PARTY_ROOTS) {
    if (re.test(q)) return false
  }
  if (isGovPath(q) || isSandboxTmp(q)) return true
  for (const re of HARNESS_OP_ROOTS) {
    if (re.test(q)) return true
  }
  for (const re of GLOBAL_CFG_ROOTS) {
    if (re.test(q)) return true
  }
  return false
}

export function verdict(cmd: string): { verdict: Verdict; why: string; dest?: string } {
  const segs = segment(cmd)
  for (const seg of segs) {
    // 1) roteiro legitimado (rollback R18) — segmento inteiro deve ser o reset
    for (const r of LEGIT_DESTRUCTIVE) {
      if (r.re.test(seg)) return { verdict: "allow-r18", why: r.label }
    }
    // 2) padrões destrutivos
    for (const r of DESTRUCTIVE_PATTERNS) {
      const m = r.re.exec(seg)
      if (m) {
        const dest = unescapePath((m[r.destGroup ?? 1] ?? "").replace(/^["']|["']$/g, ""))
        if (r.govAware && dest && isAllowedWritePath(dest)) {
          return { verdict: "allow-gov", why: "escopo governado (harness/global/sandbox)", dest }
        }
        return { verdict: "deny", why: r.label, dest }
      }
    }
  }
  return { verdict: "allow", why: "não-destrutivo" }
}
