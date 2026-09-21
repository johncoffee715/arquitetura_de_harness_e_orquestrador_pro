---
name: visao-guardrail
description: Gate visual pré-entrega — inspeciona UI/imagem/frame via VLM edge :9188 e emite veredito PASS/FAIL em JSON estrito GBNF.
provenance: spec do usuário 2026-09-17 (fonte canônica) + regra R105 promulgada 2026-09-17
slot_fisico: Qwen2-VL-7B Q4_K_M + mmproj f16 em http://127.0.0.1:9188 (llama.cpp, OpenAI-compat multimodal)
slot_alvo: Qwen2.5-VL-3B (rápido, evolutivo)
grammar: schema.gbnf (contrato JSON estrito, ordem de chaves fixa)
version: 1.0.0
date: 2026-09-17
---

# visao-guardrail — Guardrail de Visão-Edge (R105)

## 1. Propósito / gatilho

**Toda entrega de produto visual PASSA por esta skill antes de ir ao usuário (R105).**
Produto visual = UI, screenshot, imagem gerada, frame de vídeo, thumbnail, deck/slide,
asset de marca, diagrama, foto de bancada/DoP.

Sem o carimbo `visao-guardrail` (JSON válido + 4-self gate + registro), a entrega é **INVÁLIDA**.

### 4-self de visão (executado sempre, nesta ordem)

1. **Evidência é do produto certo?** — o arquivo inspecionado é o entregável final
   (hash/path + dimensão conferem; não é mock, placeholder ou versão antiga).
2. **Cobre os critérios do pedido?** — cada critério visual do pedido original tem
   evidência correspondente na imagem (layout, texto legível, cores/marca, sem artefato).
3. **Julgamento verificável?** — cada defeito aponta `component` + `bounding_box`
   `[x1,y1,x2,y2]` + `description` reproduzível por um terceiro olhando o mesmo ROI.
4. **Veredito categórico R28?** — saída é só `PASS` ou `FAIL`, sem "parcial",
   "quase" ou texto livre fora do JSON. `pass_delivery_criteria` espelha o veredito.

## 2. Arquitetura 3 fases (pipeline híbrido — spec do usuário)

### FASE 1 — Pre-filter & ROI (rápido / leve)

- **Função:** detecção rápida de regiões de interesse (ROI) e anomalias
  geométricas brutas (bordas cortadas, texto borrado, desalinhamento, artefato,
  área vazia, contraste quebrado).
- **Modelos previstos:** Florence-2 (detecção/grounding) ou YOLOv10/v11 custom
  treinado nos defeitos do produto.
- **Fallback no harness atual (nada instalado):** heurística determinística +
  **crop central** (centro 80% como ROI primário + thumbnail integral como ROI 0).
  Nunca pular a fase — o fallback gera ao menos 1 ROI documentado.
- **Saída da fase:** lista de ROIs + flags geométricas → anexadas ao prompt da Fase 2.

### FASE 2 — VLM semântico (raciocínio)

- **Modelos previstos:** Qwen2.5-VL-3B / Moondream2.
- **Slot físico hoje no harness:** **Qwen2-VL-7B Q4_K_M + mmproj f16 em `:9188`**
  (llama.cpp, OpenAI-compat multimodal). É o que executa de fato até o alvo
  evolutivo (Qwen2.5-VL-3B rápido) pousar.
- **System prompt de Quality Assurance Inspector (FIXO, anti-alucinação):**

> Você é um inspetor de Quality Assurance visual. Responda ESTRITAMENTE em JSON
> conforme o schema (schema.gbnf). Nunca texto livre, nunca markdown, nunca
> explicação fora do JSON. Se não houver defeito visível, retorne defects=[]
> com status PASS. Descreva apenas o que é VISÍVEL na imagem (componente +
> bounding_box normalizada 0..1 + description curta). Não invente elementos fora
> da imagem. Não avalie código, apenas pixels. Responda em PT-BR nas descriptions.

- **Prompt em PT-BR por padrão** (descriptions em PT-BR; chaves e enums em inglês
  conforme schema).

### FASE 3 — Contrato JSON estrito (nunca texto livre)

- O VLM **só** pode emitir o JSON do §5, validado por `schema.gbnf`.
- O orquestrador **consome o JSON** (não o texto): `status`, `defects[]`,
  `pass_delivery_criteria`. Qualquer byte fora do JSON = FAIL de protocolo
  (re-tentar 1x com temperature 0.0; persistindo, FAIL + registrar).

## 3. Tabela de modelos de borda (spec do usuário — colada exata)

| Modelo | Parâmetros | Latência típica | Papel |
|---|---|---|---|
| Florence-2 | 0.23B / 0.77B | ~15–50ms | Pre-filter & ROI |
| Qwen2.5-VL-3B | 3B | 180–350ms | Raciocínio espacial |
| Moondream2 | 1.6B | 100–250ms | Ultra-leve CPU sim/não |
| SmolVLM | 2.2B | 150–300ms | Parsing alta-res |

**Regra de escolha (spec do usuário):**
- **Precisão →** Qwen2.5-VL-3B com TensorRT.
- **Restrição (CPU/borda) →** Florence-2 + Moondream2 via llama.cpp GGUF
  `Q4_K_M` / `IQ4_XS`.

## 4. Runtime / rota no harness REAL

- **Endpoint padrão:** `http://127.0.0.1:9188/v1/chat/completions`
  (OpenAI-compat, multimodal — `content: [{type:"text"},{type:"image_url"}]`).
- **Baseline de subida do servidor (llama.cpp):**
  `-ngl 99 -fa -c 8192 -t 18 --image-min-tokens 1024`
  (modelo Qwen2-VL-7B `Q4_K_M` + `mmproj f16`).
- **Contrato do cliente (obrigatório):**
  - redimensionar entrada para **lado maior ≤768px, JPEG q80** (base64 data-URL);
  - `max_tokens ≤ 700`;
  - `temperature 0.2` (0.0 no retry de protocolo);
  - `timeout 300s`.
- **VRAM budget:** ~6GB (7B Q4_K_M + mmproj f16 + ctx 8192 com flash-attention).

## 5. Schema de saída (campo a campo — exemplo do usuário)

| Campo | Tipo | Regra |
|---|---|---|
| `inspection_id` | string | id único da inspeção (ex.: `vg-20260917-001`). |
| `status` | enum | `PASS` ou `FAIL`. Só estes dois. |
| `overall_confidence` | number | `0..1` (0 = chute, 1 = certeza). |
| `defects` | array | lista de defeitos; `[]` quando limpo. |
| `defects[].type` | string | classe curta do defeito (ex.: `texto_borrado`, `logo_trocado`, `overflow_layout`). |
| `defects[].component` | string | onde no produto (ex.: `header/logo`, `card-preco/botao`, `slide-3/titulo`). |
| `defects[].severity` | enum | `low` \| `medium` \| `high` \| `critical`. |
| `defects[].bounding_box` | array 4 números | `[x1,y1,x2,y2]` normalizado 0..1 (origem canto sup-esq). |
| `defects[].description` | string | PT-BR, curta, verificável (o que se vê no ROI). |
| `pass_delivery_criteria` | bool | `true` sse `status==PASS` **e** critérios do pedido todos cobertos. |

**MODELO DE RESPOSTA: JSON puro validado por `schema.gbnf`.** Nada antes, nada
depois, sem markdown fence. Ordem de chaves fixa conforme grammar.

Exemplo mínimo válido:

```json
{"inspection_id":"vg-20260917-001","status":"PASS","overall_confidence":0.93,"defects":[],"pass_delivery_criteria":true}
```

Exemplo com defeito:

```json
{"inspection_id":"vg-20260917-002","status":"FAIL","overall_confidence":0.88,"defects":[{"type":"texto_borrado","component":"card-preco/botao","severity":"high","bounding_box":[0.42,0.71,0.58,0.78],"description":"Texto do botão ilegível por blur no ROI central."}],"pass_delivery_criteria":false}
```

## 6. 4-self gate (checklist pós-resposta — sem ele a entrega é inválida)

Executar nesta ordem após cada resposta do VLM, antes de carimbar:

- [ ] **G1 produto certo:** `inspection_id` ↔ path+hash do entregável; dimensão
      da imagem de entrada == dimensão do artefato final (pós-resize documentado).
- [ ] **G2 cobertura:** cada critério visual do pedido tem linha "coberto por
      ROI N / sem defeito" ou defeito correspondente; critério sem evidência = FAIL.
- [ ] **G3 veredito recalculado:** `status==PASS` exige `defects` sem
      `high`/`critical` **e** `pass_delivery_criteria==true`; qualquer
      `high`/`critical` → forçar `FAIL`/`false` (corrige alucinação de PASS).
      `overall_confidence < 0.5` → re-inspecionar (novo crop/ROI), não entregar.
- [ ] **G4 registro:** JSON + veredito + thumbnails de ROI gravados no
      decision-log e na pasta do entregável (§8). Sem registro = inválida.

## 7. Integrações

- **R105** promulgada 2026-09-17: gate visual obrigatório pré-entrega; esta skill
  é a implementação nativa.
- **Slots:** físico hoje = Qwen2-VL-7B `:9188` (executa); alvo evolutivo =
  Qwen2.5-VL-3B rápido (migra quando pousar; trocar só endpoint/modelo, o
  contrato JSON/GBNF não muda).
- **sentinel-guard:** auditoria de imagens **externas** (origem não confiável) —
  chamar antes do visao-guardrail quando o asset veio de fora (URL, upload,
  terceiros); visao-guardrail julga qualidade, sentinel julga segurança.
- **fotografo:** captura/referência (DoP, macro solda, asset Academy) — produz a
  imagem que o visao-guardrail inspeciona. Ordem: fotografo captura →
  visao-guardrail carimba → entrega.

## 8. Uso (procedimento executável)

1. **Capture/congele** o entregável final (screenshot do build servido, export
   do deck em PNG por slide, render final da imagem). Anote `path + sha256 +
   WxH`. Nunca inspecionar rascunho.
2. **Resize:** lado maior ≤768px, JPEG q80 (ex.:
   `python3 -c "from PIL import Image; im=Image.open(src); ..."`, ou `ffmpeg -vf
   scale`). Preservar original; inspecionar o redimensionado e documentar fator.
3. **Pre-filter & ROI (Fase 1):** rodar detector se houver; senão fallback —
   ROI 0 = imagem integral, ROI 1 = crop central 80%. Anotar bboxes dos ROIs.
4. **POST (Fase 2):** `POST http://127.0.0.1:9188/v1/chat/completions` com system
   prompt fixo do §2 + critérios do pedido + imagem base64; `max_tokens≤700`,
   `temperature 0.2`, `timeout 300s`.
5. **GBNF-validate (Fase 3):** validar a resposta contra `schema.gbnf`
   (grammar-file no servidor ou validador local). Falha de protocolo → 1 retry
   com `temperature 0.0`; persistindo → `FAIL` registrado como erro de protocolo.
6. **4-self gate (§6):** G1→G4. Recalcular veredito (G3) independente do que o
   VLM declarou.
7. **Registrar veredito:** gravar (a) JSON do veredito + (b) linha no
   decision-log + (c) cópia na pasta do entregável (`<entregavel>/qa-visao/
   <inspection_id>.json` + ROIs). `PASS` libera a entrega ao usuário; `FAIL`
   volta ao produtor com a lista `defects[]` como backlog.
8. **Re-inspeção:** após correção, novo `inspection_id` (nunca reutilizar);
   manter histórico de todas as tentativas na pasta do entregável.

## Contrato de retorno (ao orquestrador)

Devolver: `inspection_id · status PASS/FAIL · overall_confidence ·
n_defects + severidade máxima · paths registrados · exit_status`.
`exit_status 0` = gate executado e registrado (independe de PASS/FAIL);
`≠0` = gate não executado (protocolo/timeout/registro falhou) → entrega inválida.
