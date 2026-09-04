# Auditoria de Segurança — Skills (.agents/skills + harness) · 2026-08-25

## Escopo
11 skills auditadas: `security-review`, `threejs-game-director` (+5 fases), `threejs-3d/image/audio-generator`, `context-selector` (harness). ~900 KB, 7 scripts executáveis lidos linha a linha (Python/Node/Bash), todos os SKILL.md e referências varridos por padrões de risco.

## Veredito
**SEGURO (PASSOU_CATEGORICO)** — 0 críticos. Sem eval/exec/shell=True/pickle/yaml.load/verify=False, sem segredos hardcodados, sem telemetria/exfiltração, sem prompt-injection nos .md. Chaves via env vars (`TRIPO/GEMINI/ELEVENLABS_API_KEY`), egresso HTTPS apenas para 3 APIs documentadas (Tripo, Gemini, ElevenLabs).

## Achados
| # | Severidade | Achado |
|---|---|---|
| 1 | IMPORTANTE | `--api-key` em CLI vaza em `ps`/history — preferir env var |
| 2 | IMPORTANTE | `threejs_3d_asset.py:download_url` escreve caminho com `task_id` controlado pela API sem sanitizar (defesa em profundidade) |
| 3 | OPCIONAL | Downloads sem cap de tamanho (exaustão de disco) |
| 4 | OPCIONAL | import-map CDN jsdelivr `fflate@0.8.2` sem SRI (supply-chain) — preferir npm |
| 5 | FUTURA | Helenização: path ladder do director cita `~/.claude`/`~/.codex` (runners estrangeiros) — adaptar a OpenCode; registrar no registry (R2/R8) |

## Scaffolding gerado
`opencode/config/opencode/scripts/skills-security-audit.sh` — gate de auditoria contínua: scan de scripts (*.py/sh/mjs/js/ts) por padrões de execução perigosa + segredos, .md por injection; log JSONL append-only; exit 1 = bloqueio (R18/R40). Validado: baseline limpo (exit 0) + canário malicioso detectado (2 CRITICOS, exit 1).

## Padrão reutilizável (instinto)
Skill segura = frontmatter legítimo + chaves em env + egresso documentado HTTPS + scripts stdlib sem exec dinâmica + patches propose-only. Auditoria = estática (padrões) + canário adversarial (provar o caminho de falha) + gate binário com evidência.
