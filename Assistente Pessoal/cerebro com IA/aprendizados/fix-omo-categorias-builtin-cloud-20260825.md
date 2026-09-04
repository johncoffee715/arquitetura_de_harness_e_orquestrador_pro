# FIX 2026-08-25 ‚ Categorias builtin cloud do OMO sombreadas com override local

## Sintoma
"erro ainda persiste": delega√ß√µes ca√≠am em modelos cloud inexistentes/sem credencial.
Log: `stream error providerID=openai modelID=gpt-5.6-luna-fast ... AI_APICallError: model 'gpt-5.6-luna' not found` (24/08 21:25, agent=librarian) + `429 rate_limit_exceeded openrouter stealth/ox-alpha` (25/08 03:48).

## Causa-raiz (evidenciada)
- Plugin oh-my-openagent 4.19.4 tem **categorias builtin cloud** em `BUILTIN_CATEGORIES`:
  - `deep` ‚ openai/gpt-5.6-sol ¬∑ `quick` ‚ kimi-for-coding/kimi-for-coding-highspeed
  - `artistry` ‚ anthropic/claude-fable-5 ¬∑ `ultrabrain` ‚ openai/gpt-5.6-sol
  - `unspecified-low` ‚ openai/gpt-5.6-luna ¬∑ `unspecified-high` ‚ kimi-for-coding/k3
  - `visual-engineering` ‚ anthropic/claude-opus-5 ¬∑ `writing` ‚ kimi-for-coding/k3
- User config (`~/.omo/omo.jsonc`, √∫nico path lido ‚ N√O √© ~/.config/opencode/) definia categorias com OUTROS nomes (cognitivo/executor/refutacao/exploracao/criativo) ‚ builtin cloud ficava viva.
- Agentes hom√¥nimos (deep/quick/artistry) com `model:` local eram ignorados na listagem por categoria.
- `sisyphus`/`sisyphus-junior` vazios (`{}`) = provider fallback ‚ anthropic.

## Fix
Sombrear TODOS os nomes builtin em `[opencode].categories` (+ sisyphus/sisyphus-junior em agents) com modelos locais:
deep/ultrabrain/unspecified-high/visual-engineering ‚ local-orchestrator/qwen3.8-9b ¬∑ quick/unspecified-low ‚ local-qwen38-2b/qwen3.8-2b ¬∑ artistry/writing ‚ local-bonsai/bonsai-27b.
Valida√ß√£o: `omo doctor --verbose` ‚ todas ‚ user override locais; 6 passed / 0 failed / 1 warning benigno (capabilities unknown p/ modelos fora do cat√°logo models.dev).
Backup: `~/.omo/omo.jsonc.bak-fix-cloud-categories-20260825-080807`.

## Aprendizado
1. **Config OMO ativa = `~/.omo/omo.jsonc`** (link para /mnt/dados/opencode/omo/omo.jsonc). Snapshots em ~/.config/opencode s√£o s√≥ hist√≥rico.
2. **Nome colide = builtin vence se n√£o houver override** no mesmo namespace de categorias. Criar agente hom√¥nimo N√O desativa a categoria builtin.
3. Diagn√≥stico r√°pido: `omo doctor --verbose` mostra ‚ (user override) vs ‚ (provider fallback) ‚ qualquer ‚ cloud √© bomba-rel√≥gio sem credencial.
4. Plugin atualiza sozinho (cache @latest): ap√≥s update, REVISAR novas categorias builtin contra overrides locais.
