# Doutrina de Geração Restrita (Constrained Decoding) — Motor de Features do Ecossistema Local

**Artefato**: constrained-decoding-doutrina · **Data**: 2026-08-31 · **Autor**: Gran-Mestre (diretriz do usuário)
**Registrado no decision-log**: HEFESTO-CONSTRAINED-DECODING-2026-08-31 · **Regra global**: R81 (AGENTS.md)

---

## Princípio central

Para extrair **previsibilidade** de LLMs — **QUALQUER LLM do ecossistema, independentemente das
capacidades cognitivas** (pequeno OU grande: Granite-4.2-3B, Qwen, Phi-3, Ternary-8B, LFM, RWKV7,
Ornith-35B) — rodando localmente, NÃO se confia na capacidade do modelo de "acertar" sintaxe. O modelo
deixa de ser um **gerador livre** e passa a ser um **motor de preenchimento de estados**: a arquitetura
envelopa o LLM em Geração Restrita (Constrained Decoding) + Pipeline de Validação Determinístico.
**Este é o PADRÃO EXIGIDO para todo output estruturado consumido por máquina (R81) — não uma opção
para modelos fracos.**

> Previsibilidade não vem do prompt ("seja cuidadoso") — vem da barreira física no amostrador (GBNF)
> + validação determinística (Pydantic) + anti-loop de máquina (max_retries no Python com fallback).

## Stack de Correção (arquitetura de controle)

| Camada | Ferramenta/Linguagem | Função técnica |
|---|---|---|
| Definição de Tipos | **Python (Pydantic)** | Esquemas de dados rígidos — o modelo só pode responder o que está tipado |
| Geração Restrita | **Outlines ou Instructor** | Injeta o schema JSON/Regex diretamente na máquina de estado do LLM (nível de token) |
| Controle de Estado | **.md e .json** | System Prompts estruturados em Markdown (tags XML) + Few-Shot examples (3–5 interações perfeitas no array de mensagens) |
| Motor de Inferência | **vLLM ou llama.cpp** | GGUF/AWQ com parâmetros estritos (temp=0, stop_tokens, max_tokens calculado) |
| Validação/Correção | **Pydantic `model_validate_json` + retry** | Parse do erro → injeção de volta no modelo (auto-correção) com `max_retries=3` |

## Mecanismos anti-erro (por camada)

1. **Extirpação de erros de sintaxe — Constrained Decoding**: LLMs pequenos alucinam chaves JSON ou
   esquecem de fechar strings. A correção NÃO é pedir "seja cuidadoso" — é limitar a probabilidade dos
   tokens seguintes via **gramática GBNF** (llama.cpp) ou **FSM** (Outlines). Tokens inválidos saem do
   amostrador antes do softmax (logit bias infinito negativo). Ex.: `risk_level ::= [0-5]` impede
   fisicamente "baixo", "6" ou "0.5".
2. **Instructor acoplado ao modelo**: força output formatado; se houver erro, faz parse e injeta de
   volta com auto-correção. `max_retries=3` — anti-loop: falhou 3× = exceção no Python (NÃO no LLM).
3. **Engenharia de contexto via .md/.json**: tags XML no Markdown separam instrução de dados (o modelo
   pequeno se perde quando mistura); Few-Shot perfeito (Input→Output) calibra pesos de atenção temporários.
4. **Barreiras físicas no motor**: `temperature=0.0` (determinismo), `stop_tokens` (ex. `["\n\n", "```",
   "<|eot_id|>"]` — corta geração instantânea se o modelo tentar justificar código), `max_tokens`
   calculado do schema (se a resposta deve ter 50 tokens, trave em 70 — o modelo bate no muro rápido,
   economiza VRAM/tempo).
5. **Fallback handling**: se o LLM falhar as tentativas (max_retries no Python), o código assume default
   (JSON vazio ou log de erro) — NUNCA re-alimentar a falha em loop infinito.

## GBNF no motor C++ (llama.cpp)

- Gramática opera no nível do motor: logit bias infinito negativo para qualquer token que não obedeça à
  regra estrutural — o modelo é **fisicamente impedido** de alucinar sintaxe.
- `LlamaGrammar.from_string(gguf)` para gramática manual; **`LlamaGrammar.from_json_schema(...)`** para
  compilação dinâmica: Pydantic → JSON Schema → GBNF em runtime (na memória).

## Transpilação Pydantic → JSON Schema → GBNF (runtime)

```python
class AjusteKernel(BaseModel):
    governador_cpu: str = Field(pattern="^(performance|schedutil|powersave)$")
    frequencia_max_mhz: int = Field(gt=800, le=5000)
    flag_systemd_boot: bool
    parametros_adicionais: list[str] = Field(max_items=3)

schema_dicionario = AjusteKernel.model_json_schema()
gramatica_dinamica = LlamaGrammar.from_json_schema(json.dumps(schema_dicionario))
resposta = llm("Gere o perfil...", grammar=gramatica_dinamica, max_tokens=150, temperature=0.0)
payload_validado = AjusteKernel.model_validate_json(resposta["choices"][0]["text"])
```

## Vantagens arquiteturais

- **Controle centralizado**: nova métrica/campo = editar a classe Pydantic; a gramática C++ se adapta na
  próxima execução (sem regenerar .gbnf manual — manual quebra o dinamismo).
- **Regex mapeado**: `pattern` do Pydantic vira regra GBNF que zera probabilidade de tokens fora do padrão.
- **Tipos complexos garantidos**: o LLM não precisa "entender" booleano/array — a gramática força
  `true/false` e `[ ]` corretos (nunca "Sim"/"Verdadeiro").
- **Determinismo em modelos burros**: 8B/3B sob GBNF + temp=0.0 = função determinística f(x)=y — ideal
  como core de features de automação/scripts do ecossistema local.

## Estado do terreno (o que JÁ existe no tooling do Hefesto)

- `skills/hefesto/tooling/hefesto_llama_bridge.py` (helenizado, unificado 2026-08-31): compila flags do
  `llama_cpp_config.json`, enriquecimento via LLM com GBNF (`hefesto_deep_spec.gbnf`), webhook.
- `skills/hefesto/tooling/hefesto_deep_spec.gbnf` + `hefesto_feature.gbnf`: gramáticas manuais existentes.
- `skills/hefesto/tooling/llama_cpp_config.json`: flags do motor (temperatura, threads auto R72).
- Skills atômicas hefesto-* com gabarito.json (firewall R77) — candidato a virar fonte Pydantic.

## GAPs para implementar (roadmap)

1. **[bridge]** Centralizar transpilação Pydantic→JSON Schema→GBNF runtime no `hefesto_llama_bridge.py`
   (fonte única: classes Pydantic das features; .gbnf manual só como legado/fallback).
2. **[retry]** Implementar loop instructor-like (`max_retries=3`, erro parseado e re-injetado, exceção no
   Python após 3×, fallback default) no bridge ou na forja.
3. **[forja]** Aplicar o stack como motor padrão da fase FORJA (tool calling estruturado com schema
   byte-level — validação 100% conformidade).
4. **[skills]** Tornar o gabarito.json (R77 camada 2) a definição-fonte: gabarito → Pydantic → GBNF.
5. **[engine]** Parâmetros estritos por feature no `llama_cpp_config.json`: temp=0.0, stop_tokens,
   max_tokens calculado; validar com o modelo atual do slot (granite-4.2-3b :9088).
6. **[testes]** TDD do bridge: gramática gerada válida (llama.cpp carrega), output 100% conforme schema
   em N tentativas, anti-loop (3× = exceção + fallback).