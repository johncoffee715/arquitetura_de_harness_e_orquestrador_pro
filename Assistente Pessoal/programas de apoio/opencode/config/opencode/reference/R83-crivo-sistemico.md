> [ARQUIVO FRI extraido de AGENTS.md em 2026-09-10 — regra R83 integral aqui. AGENTS.md carrega apenas o stub de 3 linhas.]

# ═══ REGRA GLOBAL R83 — CRIVO SISTÊMICO OBRIGATÓRIO (FATOS · DADOS · MEMORIAL COMPARATIVO) — promulgado 2026-08-31 ═══

**Regra**: TUDO dentro do ecossistema (LLM, feature, hook, subagent, skill, motor, pipeline — qualquer
coisa que execute) DEVE passar pelo **crivo sistêmico** através de **fatos, dados, argumentos
plausíveis e irrefutáveis que comprovem as capacidades do LLM/feature em teste empírico** — registrados
em **memorial comparativo** (append-only, comparável entre rodadas/versões/modelos).

<Etapas obrigatórias do crivo (feature interna de benchmark)>:
1. **Etapa A — ANTI-ALUCINAÇÃO**: prompts com GROUND TRUTH verificável (fatos conhecidos, extração
   estruturada com schema, verificação de não-invenção de campos/valores/arquivos). Métricas:
   conformidade de schema (Pydantic model_validate_json), acurácia factual vs ground truth, taxa de
   invenção (campos/valores que não existem na fonte).
2. **Etapa B — ANTI-LOOP**: N amostras do mesmo prompt (temp 0.0 e variada). Métricas: determinismo
   (respostas idênticas em temp 0), repetição n-gram (loop de tokens), finish_reason length vs stop
   (bateu no muro = explosão/loop), content vazio com reasoning infinito (R57), latência anômala.
3. **Veredito categórico por métrica (R28)**: PASSOU_CATEGORICO / NAO_PASSOU com limiares configuráveis
   (default: alucinação <10%, loop <10%, determinismo ≥90%). Resultado que não impressiona (R40) NÃO transita.
4. **Memorial comparativo**: append em `harness/logs/llm-crivo-memorial.jsonl` (schema com ts, alvo,
   versão, métricas, veredito) + relatório legível; comparável entre modelos/versões para decisão (R45).

<Aplicação>
- Vale para: canonização de novo LLM (R79), troca de slot (R27), dúvida sobre capacidade de feature,
  antes de entrar no A2A/conselho, e REGRESSÃO ao trocar prompt/modelo/tool (R28 trajectory).
- Nada é aceito por "parece bom" ou benchmark externo sozinho — o crivo empírico local prevalece (R45).
- Feature implementada em `scripts/llm_crivo.py` (+ testes) — parte do arsenal do Gran-Mestre (R44).

<Exemplo canônico (2026-08-31)>
- granite-4.2-3b :9088 cravado: Etapa A taxa de alucinação ~0%; Etapa B determinismo 100% (temp0),
  stop vs length saudável; memorial registrado.

