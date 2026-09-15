# 2026-09-15 — needle-sync (snn-w9r-needle-sync / w9r-1789445799)

## Estado
- REAL: `opencode/scripts/start-stack.sh` (bash -n OK, idempotente pgrep, sobe needle 8097+9091).
- DECOY movido: `opencode/config/opencode/start-stack.sh` → `start-stack.sh.STALE-2026-09-15.bak` (granite path inexistente, JSON solto linha 30-33).
- Manifesto: `opencode/config/opencode/manifest_llm.json` + chave `needle2` (demais chaves preservadas, json.tool OK).

## Servicos needle2 (`opencode/tools/needle2/needle --serve`, endpoint `POST /complete`)
- 8097: `opencode/tools/needle2/graph-tools.json` — triagem L0 / talamico de ferramentas.
- 9091: `opencode/config/opencode/tools/needle2/forja-tools.json` — forja GBNF estrita (validate_schema/write_artifact/upsert_vault/emit_manifest).
- Extra existente (nao acoplado): `opencode/tools/needle2/smoke-tools.json`, `config/.../unified-tools.json`.

## Pares
- 8097 acopla 9084 RWKV7 (classify/talamico); 9091 acopla 9088 contrato-plano.
- Auto-start: `opencode/scripts/start-stack.sh` (pgrep `needle2/needle --serve` / `needle --serve --port 9091`).

## Prova 2026-09-15
- GET /health 8097/9091: FAIL (correto — needle nao expoe /health).
- POST /complete ping: 8097 OK (decode_tps 160.1), 9091 OK (decode_tps 146.6); procs 37994/38036 UP. Sem restart.

## Estender p/ novos LLMs
1. Criar `<nome>-tools.json` (num dos dirs acima, sem inventar no manifesto).
2. Acrescentar bloco `launch` + porta em `scripts/start-stack.sh` (pgrep idempotente) — nao tocar resto.
3. Adicionar entrada em `manifest_llm.json:needle2.servicos` com `{port, tools, papel, acopla}` + `python -m json.tool` antes de fechar.
