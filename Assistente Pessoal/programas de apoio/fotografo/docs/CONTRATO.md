# CONTRATO — MCP Fotógrafo (anti-lixo)

## Retorno obrigatório por tool

Toda tool retorna dado **verificável**: `path`/`outputs` sempre absolutos e
existentes no filesystem; `render_final`/`draft_generate` incluem `prompt_id`
do ComfyUI. `status_job` normaliza para
`{state: queued|running|done|error, message, outputs}`.

**NUNCA afirmar render sem arquivo**: se o PNG/WEBP/MP4 não existe no disco,
o retorno é erro com mensagem bruta — nunca `ok` resumido.

## Variáveis de ambiente

| Var | Default | Papel |
|---|---|---|
| `COMFY_URL` | `http://127.0.0.1:8188` | API do ComfyUI (POST /prompt, GET /history, GET /view) |
| `FOTOGRAFO_LLM` | `http://127.0.0.1:9188/v1` | LLM-Fotógrafo OpenAI-compatível (DoP JSON) |
| `DISPLAY_CMD` | `xdg-open` | Visualizador local (não-bloqueante via Popen) |

## LOG MELT

Append-only em `logs/mcp.jsonl`, um JSON por linha:
`ts` (ISO-8601), `tool`, `args_hash` (sha256-12 dos args), `dur_ms`,
`exit_status` (ok|error), `ref` (path/prompt_id/erro resumido).

## Troubleshooting

- **ComfyUI offline** (normalmente PARADO — nunca iniciar sozinho):
  `draft_generate`/`render_final`/`status_job` levantam
  `ComfyUI offline ou ...` com a URL tentada. Ação: subir
  `programas de apoio/ConfyUI` sob demanda (`python main.py`) e repetir.
- **VLM/LLM offline** (`:9188` pode estar down): `analyze_reference` levanta
  `LLM-Fotógrafo offline ou falhou ...` com corpo bruto. Ação: subir o
  llama.cpp do LLM-Fotógrafo e repetir. Parse DoP: retry 1x com
  "APENAS JSON válido"; 2ª falha propaga o bruto para o usuário corrigir.
- **playwright ausente**: `search_references` levanta instrução ACTIONABLE:
  `fotografo/.venv/bin/python -m playwright install firefox`.
  Sem Firefox/continência, a busca não roda — nunca retorna path fake.
- **Pesos em download**: `sd_xl_base_1.0.safetensors` OK;
  `diffusion_pytorch_model_promax.safetensors` (ControlNet union) e
  `svd_xt_1_1.safetensors` podem estar baixando (ver `logs/downloads-pesos.log`).
  Workflow referencia o nome exato; ComfyUI erra com bruto se o peso faltar.
- **Stack A viva** (:8083/:9084-9098): proibido tocar; ComfyUI/SVD (GPU)
  só com a Stack A livre — sem GPU simultânea.

## Prova audiovisual (gate)

Todo gate exibe o arquivo real via `display_locally` e registra o path
absoluto no relatório. Sem exibição, o gate não fecha.
