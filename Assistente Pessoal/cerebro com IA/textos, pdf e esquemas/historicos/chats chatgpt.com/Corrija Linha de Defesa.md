---
title: "Corrija Linha de Defesa"
source: "https://chatgpt.com/c/6a9a16ce-5e88-83e9-a01a-258e6e0f1bfa"
author:
published:
created: 2026-09-03
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**Você disse**

corrija a "Linha de Defesa" Multi-Formato contra alucinaçoes, falha looping sistemico, quantização agreessiva, combinar Markdown + Python + JSON + GBNF, mas arquiteturalmente sólida. Cada formato atua em uma camada de defesa diferente e como eles se complementam: ┌─────────────────────────────────────────────────────────────┐ │ CAMADA 4: VALIDAÇÃO FUNCIONAL (Python.py) │ │ → Executa testes, verifica se a saída faz sentido lógico │ │ → Simula chamadas de API, checa consistência de dados │ ├─────────────────────────────────────────────────────────────┤ │ CAMADA 3: VALIDAÇÃO SEMÂNTICA (JSON Schema + Python) │ │ → Verifica se campos obrigatórios existem │ │ → Valida tipos, ranges, enums │ ├─────────────────────────────────────────────────────────────┤ │ CAMADA 2: VALIDAÇÃO SINTÁTICA (GBNF.gbnf) │ │ → Força o modelo a gerar apenas tokens válidos │ │ → Garante JSON bem-formado, Markdown válido, etc. │ ├─────────────────────────────────────────────────────────────┤ │ CAMADA 1: ESTRUTURAÇÃO DO PROMPT (Markdown.md) │ │ → Separa contexto, instruções, exemplos, constraints │ │ → Reduz ambiguidade no input │ ├─────────────────────────────────────────────────────────────┤ │ CAMADA 0: MODELO (quantização agressiva) │ │ → Gera a saída (potencialmente ruidosa devido à quantização)│ └─────────────────────────────────────────────────────────────┘ | Formato | Função na defesa | Quando é aplicado | | ------------------ | ------------------------------------------------ | ------------------------------------------------------------------------ | | \*\*Markdown (.md)\*\* | Estruturação do prompt e do output intermediário | No prompt system/instruction e na saída de raciocínio (chain-of-thought) | | \*\*GBNF (.gbnf)\*\* | Gramática constrangedora — força sintaxe válida | Durante a geração (sampler do llama.cpp), token a token | | \*\*JSON (.json)\*\* | Contrato de dados — schema rigoroso | Na saída final para consumo por APIs ou próximo agente | | \*\*Python (.py)\*\* | Validador e executor — checa semântica e lógica | Pós-processamento da saída, antes de executar qualquer ação | | Risco | Mitigação com sua arquitetura | | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------- | | Modelo gera JSON sintaticamente válido mas semanticamente absurdo | JSON Schema (campos obrigatórios + enums) + validação Python | | Modelo escolhe ferramenta errada devido a reasoning degradado | Few-shot examples no prompt Markdown + validação de existência da ferramenta em Python | | Modelo "esquece" constraints em contexto longo | Resumo periódico em Markdown + re-injeção de constraints a cada turno | | Modelo gera parâmetros com tipos errados (string vs int) | GBNF com tipagem forte + JSON Schema `type` rigoroso | | Alucinação de ferramentas inexistentes | Python valida contra whitelist de tools disponíveis | Teste A/B: Compare a mesma tarefa entre a quantização base mais coerente e quantizaçoes mais agressivas. Meça taxa de erro (ferramenta errada, JSON inválido, parâmetros incorretos). Se a taxa de erro das quantizaçoes mais agressivas >5% a mais, considere puro ou a quantização base. Use GBNF sempre para orquestração, independente da quantização. A penalidade de performance é menor que o custo de parsear JSON malformado. Não pule a camada Python. GBNF garante sintaxe, JSON Schema garante estrutura, mas apenas Python garante que a orquestração faz sentido (ex: "esta ferramenta realmente pode receber estes parâmetros?"). Considere fallback: Se as quantizaçoes mais agressivas falhar em uma tarefa crítica, tenha um caminho para repetir com quantização base mais coerente ou delegar para um modelo menor mas denso (ex: Qwen3-8B em Q4\_K\_M a ~12 t/s) como validador. estratégia é viável e inteligente. A quantização agressiva compensa pela velocidade e economia de RAM, desde que você trate o modelo como um "gerador potencialmente ruidoso" e invista pesado nas camadas de validação. A combinação Markdown → GBNF → JSON → Python é exatamente a ordem correta de defesa.

---

A arquitetura é boa em princípio, mas há um erro conceitual importante: **Markdown, GBNF, JSON Schema e Python não são quatro barreiras independentes contra alucinação**. Cada um resolve uma classe diferente de falha. Além disso, **GBNF não deve ser apresentado como garantia de tipagem semântica**, e o problema de looping precisa de uma camada própria durante a geração.

No `llama.cpp`, por exemplo, GBNF pode restringir a saída e JSON Schema pode ser convertido em gramática, mas o próprio schema não é automaticamente visível ao modelo; ele serve para restringir a geração. [^1]

### Arquitetura corrigida

```
┌──────────────────────────────────────────────────────────────────────┐
│                    META-ORQUESTRADOR / SUPERVISOR                    │
│                                                                      │
│  classifica task → escolhe modelo → escolhe contrato → executa      │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ CAMADA 6 — RECUPERAÇÃO / FALLBACK                                    │
│                                                                      │
│ • retry controlado                                                   │
│ • modelo alternativo                                                 │
│ • quantização menos agressiva                                        │
│ • delegação para validador/especialista                              │
│ • abortar tarefa quando confiança < threshold                        │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ CAMADA 5 — VALIDAÇÃO FUNCIONAL / EXECUTION GATE                     │
│                         Python                                      │
│                                                                      │
│ • ferramenta existe?                                                 │
│ • parâmetros são compatíveis?                                       │
│ • dependências existem?                                             │
│ • operação é permitida?                                             │
│ • resultado é plausível?                                            │
│ • pré-condições / pós-condições                                     │
│ • dry-run antes da execução                                          │
│                                                                      │
│ >>> NADA É EXECUTADO ANTES DE PASSAR AQUI <<<                        │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ CAMADA 4 — VALIDAÇÃO SEMÂNTICA                                      │
│                   JSON Schema + Python                              │
│                                                                      │
│ • required                                                          │
│ • type                                                              │
│ • enum                                                              │
│ • range                                                             │
│ • min/max                                                            │
│ • additionalProperties                                              │
│ • cross-field validation                                             │
│ • invariantes                                                        │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ CAMADA 3 — CONTROLE SINTÁTICO                                       │
│                         GBNF                                         │
│                                                                      │
│ • estrutura permitida                                               │
│ • JSON válido                                                        │
│ • tokens permitidos                                                  │
│ • formato de tool-call                                               │
│ • enum lexical quando possível                                      │
│                                                                      │
│ ATUA TOKEN A TOKEN DURANTE A GERAÇÃO                                 │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ CAMADA 2 — WATCHDOG DE GERAÇÃO                                     │
│                  runtime / sampler                                  │
│                                                                      │
│ • max output tokens                                                  │
│ • timeout                                                            │
│ • repetição de n-gram                                                │
│ • repetição de sequência                                             │
│ • baixa diversidade                                                  │
│ • stall detector                                                      │
│ • EOS anômalo                                                         │
│ • crescimento anormal do KV                                          │
│ • abort imediato em looping                                          │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ CAMADA 1 — PROMPT / CONTEXTO                                         │
│                         Markdown                                    │
│                                                                      │
│ • system policy                                                      │
│ • task                                                             │
│ • contexto relevante                                                │
│ • exemplos                                                           │
│ • constraints                                                        │
│ • contrato                                                           │
│ • estado resumido                                                    │
│                                                                      │
│ Markdown = organização humana do protocolo, NÃO validador           │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│ CAMADA 0 — MODELO                                                    │
│                                                                      │
│ modelo + arquitetura + quantização + sampler + KV cache             │
│                                                                      │
│ potencialmente ruidoso                                               │
└──────────────────────────────────────────────────────────────────────┘
```

### O ponto mais importante: separar os tipos de falha

Sua versão anterior trata **looping sistêmico** como consequência genérica de uma quantização ruim. Eu separaria isso explicitamente:

| Falha | Detector principal | Ação |
| --- | --- | --- |
| JSON inválido | GBNF | bloquear na geração |
| Campo ausente | JSON Schema | rejeitar |
| Tipo incorreto | JSON Schema | rejeitar |
| Enum inválido | Schema + Python | rejeitar |
| Tool inexistente | Python | rejeitar |
| Parâmetro incompatível | Python | rejeitar |
| Ferramenta válida, mas decisão errada | Python + supervisor | rejeitar |
| Resultado logicamente absurdo | Python | rejeitar |
| Repetição infinita | **Watchdog runtime** | abortar geração |
| Contexto degradado | Context Monitor | compactar/reiniciar |
| KV corrompido/degradado | Runtime | resetar sessão |
| Quantização degradada | Benchmark/A-B | trocar modelo/quant |
| Falha repetida | Fallback | escalar para modelo mais confiável |

Esse `Watchdog` é a peça que estava faltando.

### Não use Markdown para “chain-of-thought”

Eu também mudaria isto:

> “Markdown (.md) → saída de raciocínio (chain-of-thought)”

Para:

> **Markdown → estado operacional estruturado**

Por exemplo:

```markdown
## TASK_STATE
goal: reparar_firmware
phase: 2
confidence: 0.82

## FACTS
- arquivo existe
- checksum confirmado
- ferramenta disponível

## CONSTRAINTS
- não modificar bootloader
- backup obrigatório

## NEXT_ACTION
tool: disassembler
```

Você não precisa depender de uma cadeia de raciocínio textual gigantesca. Para seu orquestrador, **estado explícito e verificável é muito mais robusto**.

---

Sua formulação:

```
Markdown → GBNF → JSON → Python
```

é útil como simplificação, mas arquiteturalmente eu usaria:

```
PROMPT/STATE
     ↓
WATCHDOG
     ↓
GBNF
     ↓
JSON
     ↓
JSON Schema
     ↓
PYTHON VALIDATOR
     ↓
EXECUTION GATE
     ↓
TOOL
     ↓
RESULT VALIDATOR
     ↓
SUPERVISOR
```

E há **dois fluxos de validação**, não um:

```
┌──── geração ────┐
                ↓                  │
MODEL → WATCHDOG → GBNF → JSON → SCHEMA
                                  │
                                  ▼
                              PYTHON
                                  │
                           ┌──────┴──────┐
                           │             │
                         FAIL          PASS
                           │             │
                           ▼             ▼
                        RETRY         EXECUTE
                                         │
                                         ▼
                                  RESULT VALIDATOR
                                         │
                                  ┌──────┴──────┐
                                  │             │
                                FAIL          PASS
                                  │             │
                                  ▼             ▼
                               RECOVERY       COMMIT
```

Isso transforma o LLM de **“agente que executa”** em **“gerador de intenção que precisa obter autorização para executar”**.

Esse é um desenho muito mais seguro para seu Meta-Orquestrador.

---

## GBNF não deve carregar tudo

Há outro ajuste importante.

Não tente colocar toda a semântica no GBNF.

Por exemplo:

```
tool ::= "read_file" | "write_file" | "delete_file"
```

é ótimo.

Mas tentar codificar no GBNF:

```
"se tool == write_file então path deve existir,
mas se create == true então não precisa existir..."
```

fica complexo e pode gerar uma gramática enorme/lenta.

O ideal:

```
GBNF
 ↓
estrutura lexical/sintática
 ↓
JSON Schema
 ↓
semântica declarativa
 ↓
Python
 ↓
lógica operacional
```

O `llama.cpp` inclusive suporta conversão de JSON Schema para GBNF e uso de schema na geração, então você pode manter **um contrato canônico** e derivar a gramática dele, em vez de manter dois contratos independentes. [^1]

---

## E a defesa contra quantização agressiva?

Aqui eu faria uma mudança fundamental.

Não use:

> “quantização agressiva + validação pesada = confiável”

Isso é forte demais.

O correto é:

> **quantização agressiva + validação + detecção de falhas + fallback = operacionalmente tolerável**

Porque um modelo quantizado pode produzir uma saída **perfeitamente válida segundo a gramática e schema e ainda tomar uma decisão errada**.

Exemplo:

```json
{
  "tool": "write_file",
  "path": "/etc/config",
  "action": "replace"
}
```

Sintaxe: ✅  
Schema: ✅  
Tipos: ✅  
Tool existe: ✅

Mas a decisão pode ser completamente inadequada.

Por isso o **Execution Gate** é obrigatório.

---

## Fallback adaptativo

Eu substituiria seu critério fixo de `>5%` por um sistema de risco:

```
TASK
 │
 ├── CRITICAL
 │     └── modelo base / quantização confiável
 │
 ├── HIGH
 │     └── agressiva + dupla validação
 │
 ├── NORMAL
 │     └── agressiva + watchdog + validator
 │
 └── LOW
       └── agressiva
```

E ainda:

```
quantização agressiva
       │
       ├── PASS → continua
       │
       ├── LOOP → abort + retry
       │
       ├── schema fail → retry
       │
       ├── semantic fail → retry
       │
       └── repeated fail
                 ↓
          quantização base
                 ↓
             validator
```

Assim você não desperdiça o modelo mais pesado em todas as tarefas.

---

## Seu benchmark também precisa mudar

Em vez de medir apenas:

```
JSON inválido
tool errada
parâmetro errado
```

eu mediria:

```
1. syntax_error_rate
2. schema_error_rate
3. semantic_error_rate
4. tool_selection_error_rate
5. parameter_error_rate
6. execution_error_rate
7. hallucinated_tool_rate
8. loop_rate
9. premature_eos_rate
10. retry_rate
11. fallback_rate
12. task_success_rate
13. tokens_to_success
14. latency_to_success
15. VRAM_peak
16. RAM_peak
17. KV_peak
```

E principalmente:

```
Effective Success Rate
=
tarefas concluídas corretamente
/
tarefas totais
```

Porque uma quantização que gera 30% mais rápido, mas exige 20% de retries, pode ser pior na prática.

---

## Arquitetura final que eu recomendo para seu sistema

```
┌─────────────────┐
              │ META-ORQUESTRADOR│
              └────────┬────────┘
                       │
              task classification
                       │
                       ▼
              ┌─────────────────┐
              │ MODEL ROUTER     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ PROMPT / STATE   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ GENERATION       │
              │ WATCHDOG         │
              └────────┬────────┘
                       │
                  GBNF / schema
                       │
                       ▼
              ┌─────────────────┐
              │ STRUCTURE        │
              │ VALIDATOR        │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ SEMANTIC         │
              │ VALIDATOR        │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ EXECUTION GATE   │
              └────────┬────────┘
                       │
                       ▼
                   TOOL/API
                       │
                       ▼
              ┌─────────────────┐
              │ RESULT           │
              │ VALIDATOR        │
              └────────┬────────┘
                       │
            ┌──────────┴──────────┐
            │                     │
          FAIL                   PASS
            │                     │
            ▼                     ▼
       RECOVERY                COMMIT
            │
  ┌─────────┼─────────┐
  │         │         │
retry    compact    fallback
            │         │
            └────┬────┘
                 ▼
            MODEL ROUTER
```

**Resultado:** sua ideia original é viável, mas eu renomearia a “Linha de Defesa Multi-Formato” para **Linha de Defesa Multicamadas**, porque o objetivo não é ter quatro formatos, e sim ter **quatro mecanismos independentes de controle + watchdog + recuperação**.

E a mudança crítica é esta:

```
Markdown = contexto
GBNF     = sintaxe
JSON     = transporte/estrutura
Schema   = contrato
Python   = semântica + execução
Watchdog = estabilidade da geração
Fallback = tolerância à degradação
```

Isso fica muito mais sólido para o seu cenário de **LLM quantizado agressivamente + orquestração local + KV cache grande + múltiplos subagentes**.

[^1]: [github.com](https://github.com/osllmai/llama.cpp/blob/main/grammars/README.md?utm_source=chatgpt.com)