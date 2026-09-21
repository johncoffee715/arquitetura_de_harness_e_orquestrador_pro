import { test } from "node:test"
import assert from "node:assert/strict"
import { verdict, segment, isGovPath, isSandboxTmp, isAllowedWritePath, unescapePath } from "../scripts/guard-engine.ts"

test("segmenta ; && | e preserva segmentos simples", () => {
  assert.deepEqual(segment("a; b && c | d"), ["a", "b", "c", "d"])
})
test("isGovPath ancore e nao casa repo alheio", () => {
  assert.ok(!isGovPath("/proj/plugins/x.ts"), "plugins/ fora do harness NÃO é governança")
  assert.ok(!isGovPath("/proj/scripts/app.py"))
  assert.ok(isGovPath("/proj/CONTEXT.md"))
  assert.ok(isGovPath("/x/CONTEXT.md"))
  assert.ok(isGovPath("/mnt/dados/Assistente Pessoal/cerebro com IA/a.md"))
  assert.ok(isGovPath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/config/opencode/skills/gran-mestre/SKILL.md"))
  assert.ok(!isGovPath("/proj/src/app.py"))
})

test("unescapePath resolve backslash-espaco e escapes simples", () => {
  assert.equal(unescapePath("/mnt/dados/Assistente\\ Pessoal/programas\\ de\\ apoio/opencode/scripts/x.sh"), "/mnt/dados/Assistente Pessoal/programas de apoio/opencode/scripts/x.sh")
  assert.equal(unescapePath("a\\ b\\ c"), "a b c")
})

test("isAllowedWritePath: harness operacional + globais + sandbox; terceiros/produtivo negado", () => {
  assert.ok(isAllowedWritePath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/scripts/start-stack.sh"), "scripts/ do harness")
  assert.ok(isAllowedWritePath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/scripts/watchers/x.sh"), "subárvore scripts/")
  assert.ok(isAllowedWritePath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/tools/needle2/forja-tools.json"), "tools/ do harness")
  assert.ok(isAllowedWritePath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/tests/test_x.py"), "tests/ do harness")
  assert.ok(isAllowedWritePath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/state/watcher/guard.jsonl"), "state/ do harness")
  assert.ok(isAllowedWritePath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/bin/app"), "bin/ do harness")
  assert.ok(isAllowedWritePath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/templates/x.json"), "templates/ do harness")
  assert.ok(isAllowedWritePath("/home/johncoffee/.opencode/tests/test_y.py"), "config global ~/.opencode")
  assert.ok(isAllowedWritePath("/home/johncoffee/.config/opencode/opencode.jsonc"), "config global ~/.config/opencode")
  assert.ok(isAllowedWritePath("/mnt/dados/Assistente Pessoal/cerebro com IA/a.md"), "vault")
  assert.ok(isAllowedWritePath("/tmp/opencode/bench.py"), "sandbox /tmp/opencode")
  assert.ok(isAllowedWritePath("/mnt/dados/Assistente\\ Pessoal/programas\\ de\\ apoio/opencode/scripts/start-stack.sh"), "path escapado")
  assert.ok(!isAllowedWritePath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/repos/vendor/src/app.py"), "repos/ = código de terceiros")
  assert.ok(!isAllowedWritePath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/cactus-build/cactus/CMakeLists.txt"), "cactus-build/ = build de terceiros")
  assert.ok(!isAllowedWritePath("/mnt/dados/Assistente Pessoal/programas de apoio/opencode/llama.cpp/src/ggml.c"), "llama.cpp/ = upstream")
  assert.ok(!isAllowedWritePath("/mnt/dados/Assistente Pessoal/projetos/app/src/main.ts"), "projetos/ = workspace do usuário")
  assert.ok(!isAllowedWritePath("/etc/hosts"), "fora do ecossistema")
  assert.ok(!isAllowedWritePath("/home/johncoffee/prj/src.ts"), "código produtivo alheio")
})

const CASES: Array<[string, string]> = [
  ["git status --porcelain", "allow"],
  ["git reset --hard 1ab3e9c984ec06e7d45e7084c8b364", "allow-r18"],
  ["git reset --hard HEAD", "allow-r18"],
  ["git reset --hard", "deny"],
  ["git reset --soft HEAD~1", "deny"],
  ["git checkout -- file.txt", "deny"],
  ["sed -i s/a/b/ src.py", "deny"],
  ["python3 -i script.py", "deny"],
  ["tee x > /tmp/out.py", "deny"],
  ["tee x >> /mnt/dados/Assistente Pessoal/programas de apoio/opencode/config/opencode/skills/gran-mestre/reference/a.md", "allow-gov"],
  ["cat >> CONTEXT.md", "allow-gov"],
  ["cat >> \"/mnt/dados/Assistente Pessoal/cerebro com IA/aprendizados/x.md\"", "allow-gov"],
  ["cat > \"/mnt/dados/Assistente Pessoal/programas de apoio/opencode/scripts/start-stack.sh\"", "allow-gov"],
  ["cat > \"/mnt/dados/Assistente Pessoal/programas de apoio/opencode/tools/needle2/forja-tools.json\"", "allow-gov"],
  ["cat > /mnt/dados/Assistente\\ Pessoal/programas\\ de\\ apoio/opencode/scripts/stack-guard.sh", "allow-gov"],
  ["sed -i 's/x/y/' \"/mnt/dados/Assistente Pessoal/programas de apoio/opencode/scripts/start-stack.sh\"", "allow-gov"],
  ["sed -i 's/x/y/' /mnt/dados/Assistente\\ Pessoal/programas\\ de\\ apoio/opencode/scripts/start-stack.sh", "allow-gov"],
  ["echo x > /home/johncoffee/.opencode/tests/test_y.py", "allow-gov"],
  ["echo x > /home/johncoffee/.config/opencode/opencode.jsonc", "allow-gov"],
  ["echo x > src/app.py", "deny"],
  ["printf x > b.ts", "deny"],
  ["tee x > /tmp/opencode/bench.py", "allow-gov"],
  ["python3 scripts/llm-inventory.py --resolve judge", "allow"],
  ["cp a.py src/lib/", "deny"],
]
for (const [cmd, expected] of CASES) {
  test(`verdict: ${cmd.slice(0, 40)} => ${expected}`, () => {
    assert.equal(verdict(cmd).verdict, expected)
  })
}

// POLÍTICA 2026-09-15 (soberania do usuário): deny NÃO-hard = allow+auditoria no plugin.
// Apenas hardDeny (perda de dados irreversível) bloqueia de fato.
test("hard flag: perda de dados = true; escrita fora do escopo = false", () => {
  assert.equal(verdict("rm -rf /tmp/x").hard, true, "rm -f é hardDeny")
  assert.equal(verdict("rm --force arquivo.tmp").hard, true)
  assert.equal(verdict("git clean -fdx").hard, true)
  assert.equal(verdict("git checkout -- a.py").hard, true)
  assert.equal(verdict("git reset --hard").hard, true)
  assert.equal(verdict("git reset --soft HEAD~1").hard, true)
  assert.equal(verdict("truncate -s 0 f.log").hard, true)
  assert.equal(verdict("dd of=/dev/sda").hard, true)
  assert.equal(verdict("bash -c 'rm -rf /'").hard, true, "shell -c destrutivo")
  // soft (viram allow-outside auditados no plugin):
  assert.equal(verdict("sed -i s/a/b/ src.py").hard, false, "edição in-place fora da governança")
  assert.equal(verdict("tee x > /tmp/out.py").hard, false, "tee fora de caminho permitido")
  assert.equal(verdict("echo x > src/app.py").hard, false, "redirect fora da governança")
  assert.equal(verdict("cat >> /mnt/dados/.gitignore").hard, false, "redirect p/ dotfile do repo")
  assert.equal(verdict("cp a.py src/lib/").hard, false, "cp sobre árvore de código")
  assert.equal(verdict("git status").hard, undefined, "allow não carrega hard")
})
