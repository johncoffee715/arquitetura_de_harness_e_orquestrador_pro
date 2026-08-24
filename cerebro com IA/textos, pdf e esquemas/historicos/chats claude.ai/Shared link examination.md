**Claude**

Confirmei que é um link legítimo de share do OpenCode (`opncd.ai/share/*`, gerado pelo comando `/share` no TUI) — mas não consigo puxar o conteúdo real. A página de share é um SPA em SolidJS (confirmado no próprio tracker do projeto): o histórico de mensagens carrega via JS/API depois do load inicial, e meu fetch estático só trouxe o shell vazio (só meta tags, sem body). Tentei um segundo método de extração e deu erro de conexão.

Não existe endpoint JSON público documentado pra esse domínio de share — o REST completo do OpenCode (`/session/:id/message`, etc.) é exposto pelo `opencode serve` local, não pelo host público de share.

Mais rápido pra eu examinar de verdade:

- Cola aqui o texto da sessão (abre o link, ctrl+A, copia o trecho que importa), ou
- Se essa sessão tá rodando na tua instância local, passa o session ID e eu sigo via API local (`opencode serve` + curl), sem depender do share público.

Manda o que for mais direto pra você.

---

**Claude**

Vi o conteúdo. O achado central é sólido e bate com o que eu já sabia da tua stack: `~/.local/share/ailab2/` é o destino correto (ext4, runtime mutável), então `config.sh`, `ai-lab.sh` e o default do `state_authority.py` ainda apontando pra `ailab` (sem o 2) não é só uma "inconsistência a documentar" — é um bug ativo. Documentar no AGENTS.md é bom pra não deixar um agente futuro escolher o path errado por acaso, mas isso sozinho não impede o daemon de gravar estado no lugar errado se algum script cair no default antigo.

Pontos que valem atenção:

1. **O `state/runtime.json` na NTFS está obsoleto** — se algum processo ainda lê dali em vez de `~/.local/share/ailab2/state`, isso é uma fonte de bugs silenciosos (estado defasado sendo consultado).
2. **Duas fontes de config de modelo** (`core/config.sh` vs `inference/model_aliases.conf`) é um padrão frágil — se você atualizar um e esquecer o outro, o CLI e o daemon divergem sobre qual modelo é qual role.
3. **`OLLAMA_MODELS`** também tem path duplo (NTFS vs `$RUNTIME/ollama_models`) — mesma classe de problema do `ailab` / `ailab2`.

O AGENTS.md em si parece bem calibrado (curto, específico, sem enchimento genérico) — fez o trabalho de achar os pontos de atrito reais em vez de listar trivialidades.

Quer que eu monte o patch pra unificar tudo em `ailab2` (grep dos 4 arquivos que ainda referenciam o path antigo e normalizar), ou prefere só manter documentado por enquanto e resolver manualmente?