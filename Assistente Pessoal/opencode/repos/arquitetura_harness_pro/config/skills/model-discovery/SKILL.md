---
name: model-discovery
description: "Varre o MODEL_LIBRARY (*.gguf), extrai metadados sem carregar tensores e gera o registry normalizado com capacidades estimadas, VRAM por âncoras medidas GMB-1 e exclusões evidenciadas. Use ao adicionar/remover modelos locais ou antes de rotear tasks."
---

<objective>
Manter o registry canônico dos LLMs locais sincronizado com o diretório de modelos.
</objective>

<usage>
python3 ~/.config/opencode/skills/model-discovery/run.py [--dir DIR] [--out PATH] [--quiet]
</usage>

<notes>
- Exclusões NUNCA removem arquivos: metadata_unreadable · vram_insufficient (>16GiB físico no ctx de referência 32768) · user_blacklist.
- Modelos entre 90% e 100% do orçamento ficam YELLOW (carregam; router prefere fallback).
- Âncoras empíricas GMB-1 prevalecem sobre heurística (ornith 14.2@32K → 13.69@131K, KV sublinear).
- Código-fonte: /mnt/dados/opencode/harness/models/discovery.py · testes: harness/tests/test_discovery.py (14 ✅).
</notes>

<referencia-completa>
Parâmetros run.py: `--dir` (default: MODEL_LIBRARY) · `--out` (default: benchmark/runs/registry.json) · `--quiet`
Exit codes: 0 = scan ok · 1 = exceção (diretório ausente/escrita negada)
Dependências: apenas stdlib Python; NÃO requer servidor ativo.
Integrações: `vram-router` consome o --out · `watch_registry.sh` invoca este CLI em mudança de *.gguf · `session.start` garante o watcher via hooks/watch-registry-start.sh.
Schema por entrada: path · file.size_bytes · architecture{family,quantization,context_length,parameters_b} · backend · capabilities{estimated,measured,confidence} · roles_suitability · resources{estimated_vram_gib,vram_warning?} · performance_history · health{status,last_check} · status{available,excluded,exclusion_reason}.
Regras de exclusão (nunca remove arquivo): metadata_unreadable · vram_insufficient (>16GiB físico @REF_CTX 32768) · user_blacklist (fragmento do id).
</referencia-completa>
</notes>
