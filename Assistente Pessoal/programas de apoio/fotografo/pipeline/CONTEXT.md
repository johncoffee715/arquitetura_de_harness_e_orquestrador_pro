# Pipeline CONTEXT — Programa Fotógrafo / Academy of Eletronic

- Modo: COMPLEX+ (doutrina integral, modo autônomo aprovado pelo usuário 2026-09-16)
- Snapshot harness: fotografo/pipeline/harness-snapshot.sha256 (119 arquivos)
- Decisões do usuário: download autorizado · stacks A/B exclusivas · LLM-Fotógrafo CPU :9188 (único da Stack B)
  · ComfyUI sob demanda via input · fila completa 3 candidatos até terminar · forja via Hefesto ·
  landing Vite+React+TS · provas audiovisuais a cada gate · orquestrador cloud assume quando Stack A cai
  · 2026-09-16b: MOTOR DA SESSÃO = cloud LLM (até fim da auditoria) · trilhas azuis = arte conceitual/apoio
  · provas abrem no viewer padrão (xdg-open) · rotação VLM 100% CPU confirmada · interlock com sessão API-TEST
  · SESSÃO API-TEST em paralelo (crivo em :8090 CPU) — interlock em /tmp/stack-interlock/fotografo-apitest.json

## VRAM / Stack (CIRÚRGICO 18:5x)
- Slots GPU derrubados: 8083 (orq), 9084 (cortex), 9088 (proposer), 9095 (executor) → 14,8GB→3,4GB livres
- Slots CPU INTACTOS: 9086/9090/9092/9093/9094/9098 + 8090 (apitest) + 9188 (VLM fotógrafo)
- Para religar stack GPU: programas de apoio/opencode/scripts/start-stack.sh (MODE_WARM=0 all)

## Estado

- [F1] DONE — vault marca/brand-guide-academy-of-eletronic.md + paleta-academy.png (azul=arte conceitual)
- [F2] Pesos OK: sdxl_base 6,9G ✓ · controlnet-union promax 2,5G ✓ · LTX-Video 2B v0.9.5 6,3G ✓ · T5 fp8 4,9G ✓
  SVD-XT GATED (precisa token HF/licença) → substituto LTXV. stackctl pendente.
- [ComfyUI] 0.36.0 em programas de apoio/ConfyUI · torch venv(3.14) 2.9.1+rocm6.4 NÃO tem gfx906 →
  NOVO venv311 (python3.11) com torch 2.5.1+rocm6.2 montando em bg (log setup-venv311.log)
- [F3a] Hefesto forjou pacote: mcp/server_fotografo.py (6 tools) + workflows + gbnf + skill + testes 4/4 verde
- [F3b] CRIVO (skills/fotografo/tooling/crivo_vlm.py, T1 5img visão GBNF + T2 10x texto):
  · gemma3-4b-it-qat:  T1 5/5 T2 10/10, 6.6 t/s, 15,9s lat
  · qwen2vl-2b:        T1 5/5 T2 10/10, 199,7 t/s, 1,6s lat  ← SPRINTER
  · qwen2vl-7b:        T1 5/5 T2 10/10, 67,2 t/s, 2,7s lat   ← PRECISÃO/velocidade
  · qwen3-4b (texto):  rodando; T1 será N/A por falta de visão (baseline T2)
  · minicpm26: modelo falhou download (repo path) — mmproj presente
- [F4] MCP registro opencode.jsonc: pendente (fora dos meus caminhos de escrita — snippet pronto a aplicar)
- [F5] Vídeo: cenário em cerebro com IA/marca/cenario-video-macro-solda.md · S1 queued em ComfyUI (re-render após venv311)
- [F6] Landing: pendente (após vídeo)
- [QUARTETO VAULT] skills/bibliotecario/tooling/vault_lint.py VERDE: 51 checagens, 0 falhas — 2 summaries YT + conceito 4-selfs destilados e indexados

## RunIDs / Budget / Lições
- Lição: hf download NÃO misturar positional filename com --include
- Lição: torch rocm 2.9.1 descartou gfx906 (MI50); usar 2.5.1+rocm6.2 em venv py3.11
- Lição: usar setsid + </dev/null para processos bg não morrerem com timeout do shell

