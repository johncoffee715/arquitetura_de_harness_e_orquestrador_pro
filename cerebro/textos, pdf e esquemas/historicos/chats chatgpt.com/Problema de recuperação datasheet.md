---
title: "Problema de recuperação datasheet"
source: "https://chatgpt.com/c/6a481f93-652c-83e9-bf53-17c3c0ff0601"
author:
published:
created: 2026-07-17
description: "O ChatGPT é seu assistente de IA para uso diário. Converse com a IA mais avançada para explorar ideias, resolver problemas e aprender mais rápido."
tags:
  - "clippings"
---
O patch **funcionou parcialmente**, mas o teste mostra que o problema principal **não foi resolvido**.

O esperado era:

> **300 kHz – 1 MHz** (valor da tabela Electrical Characteristics)

O modelo respondeu:

> **até 2,4 MHz**

Isso significa que ele **ignorou a tabela** e respondeu usando outro trecho do datasheet (provavelmente o limite do oscilador, modo especial ou frequência máxima permitida por sincronização externa).

## Diagnóstico

A sequência mostra:

```
Tabela de specs elétricas encontrada
18014 chars
```

Isso apenas confirma que a tabela foi extraída.

Não confirma que ela foi realmente usada durante a resposta.

Na prática aconteceu isto:

```
PDF
 ↓
Texto
 ↓
Tabela extraída ✔
 ↓
LLM recebeu capítulo inteiro
 ↓
LLM escolheu outro trecho
 ↓
alucinação parcial
```

Ou seja:

**o problema agora não é OCR.**

É **recuperação (retrieval)**.

---

## O erro está aqui

Hoje provavelmente seu fluxo faz algo parecido com:

```
pergunta
↓

busca embedding

↓

retorna capítulos

↓

manda tudo para o LLM

↓

LLM escolhe
```

O LLM continua decidindo.

Ele nunca deveria decidir quando existe tabela oficial.

---

## O pipeline correto para datasheets

Para datasheet industrial eu faria:

```
Pergunta

↓

identificar se pergunta envolve:

- voltage
- current
- timing
- frequency
- abs max
- operating conditions
- thermal

↓

SIM

↓

buscar SOMENTE
SPEC_TABLE

↓

não usar embeddings

↓

extrair linha literal

↓

responder literalmente

↓

só depois permitir explicação
```

Ou seja:

```
SPEC_TABLE
↓

regex

↓

valor

↓

LLM apenas explica
```

Não o contrário.

---

## Outro indício

O tamanho chamou atenção:

```
18014 chars
```

Nos dois PDFs.

```nginx
TPS51125

18014

RK818

18014
```

Dois datasheets completamente diferentes.

Mesmo tamanho.

Isso é extremamente suspeito.

Pode indicar que sua função

```
extract_spec_table()
```

está capturando sempre:

```
primeiros 18014 caracteres
```

ou

```
primeiro bloco
```

e não a tabela inteira.

Eu verificaria imediatamente:

```python
print(spec_table_text[:1000])
```

e

```python
print(spec_table_text[-1000:])
```

para confirmar.

---

## Faça este teste

Abra:

```nix
knowledge/
skills/
pwm-e-pfm-tps51125-v3/
ch01.md
```

e procure por

```
300kHz
```

ou

```
1MHz
```

Se não existir:

→ o extractor falhou.

Se existir:

→ o retrieval falhou.

---

## Faça também

```armasm
grep -Ri "300" pwm-e-pfm-tps51125-v3
```

e

```armasm
grep -Ri "1MHz" pwm-e-pfm-tps51125-v3
```

Se nada aparecer:

o problema é extração.

---

Se aparecer:

o problema é recuperação.

---

## Minha suspeita (80%)

Pelo comportamento:

```
resposta = "até 2.4MHz"
```

eu apostaria que o embedding recuperou um capítulo onde aparece:

```
2.4MHz
```

e ignorou completamente a tabela.

---

## Como eu resolveria definitivamente

Eu deixaria o fluxo assim:

```
Pergunta
↓

Parser semântico

↓

É pergunta de especificação?

↓

SIM

↓

SPEC_TABLE INDEX
(SQLite / JSON)

↓

Regex

↓

Retorna linha exata

↓

LLM apenas reescreve
```

Sem embeddings.

Sem RAG.

Sem similaridade.

A tabela elétrica é um banco de dados estruturado, não texto narrativo. Embeddings são excelentes para conceitos e explicações, mas são uma escolha fraca para recuperar valores exatos de parâmetros técnicos.

**Neste momento, eu diria que o projeto está aproximadamente em:**

- ✅ Extração de texto: **100%**
- ✅ Detecção da tabela: **100%**
- ⚠️ Extração correta da tabela: **precisa ser verificada**
- ❌ Recuperação de especificações: **não confiável**
- ❌ Resposta determinística para valores numéricos: **ainda não implementada**

O próximo passo é descobrir se o gargalo está na **extração** ou na **recuperação**. Verificar o conteúdo de `ch01.md` e fazer os `grep` acima responderá isso rapidamente.

---

**Você disse**

e possivel melhorar esse projeto, se sim me descreva oq pode ser feito e como posso usar [https://github.com/anomalyco/opencode](https://github.com/anomalyco/opencode)

---

Sim. Pelo histórico do seu AI-Lab Local, eu diria que ele está em torno de **65–75% da arquitetura ideal**. O restante não depende de modelos maiores, mas sim de **engenharia de software**.

O seu objetivo nunca foi criar apenas um RAG, e sim um **engenheiro eletrônico especialista**, capaz de consultar datasheets, esquemas, código-fonte, normas e projetos com alta confiabilidade. Para isso, a arquitetura precisa evoluir.

## Arquitetura que eu faria

```
PDF
                 │
         OCR + Extração
                 │
      Classificador de documento
                 │
     ┌───────────┴───────────┐
     │                       │
Datasheet               Livro/Manual
     │                       │
Parser Estruturado      Chunking Semântico
     │                       │
JSON de Specs           Embeddings
     │                       │
SQLite                  Qdrant
     │                       │
      └───────────┬──────────┘
                  │
           Query Planner
                  │
      ┌───────────┼───────────┐
      │           │           │
 Regex      BM25/Qdrant     Código
      │           │           │
      └───────────┼───────────┘
                  │
               LLM Final
```

---

## 1) Abandonar embeddings para especificações

Hoje você faz algo parecido com:

```
PDF

↓

Chunks

↓

Embedding

↓

LLM
```

Para datasheets isso é uma arquitetura fraca.

Especificações são dados estruturados.

Exemplo:

```fortran
Parameter
Min
Typ
Max
Unit
```

Isso deveria virar:

```json
{
 "Switching Frequency":{
   "min":"300kHz",
   "max":"1MHz"
 }
}
```

Depois:

```coffeescript
Pergunta

↓

Regex

↓

JSON

↓

Resposta
```

Zero alucinação.

---

## 2) Criar um parser real de tabelas

Hoje você extrai texto.

O ideal é gerar algo assim:

```json
ElectricalCharacteristics.json

AbsoluteMaximum.json

Thermals.json

PinConfiguration.json

Timing.json

Features.json

Application.json
```

Cada seção separada.

---

## 3) Query Planner

Esse é provavelmente o maior ganho do projeto.

Ao invés de mandar tudo ao LLM:

```
Pergunta

↓

Planner

↓

tipo = datasheet

↓

tipo = especificação

↓

JSON

↓

Resposta
```

Outro exemplo:

```
Como funciona o bootstrap?

↓

Planner

↓

explicação

↓

Qdrant

↓

LLM
```

Ou:

```nginx
qual o pino EN?

↓

Pin Database

↓

Resposta
```

Cada pergunta segue um pipeline diferente.

---

## 4) Banco próprio

Hoje você usa apenas Qdrant.

Eu faria:

```markdown
SQLite

+

DuckDB

+

Qdrant
```

Cada um resolve um problema.

SQLite

- specs
- pinos
- registradores
- comandos

DuckDB

- tabelas enormes

Qdrant

- texto

---

## 5) Construir Knowledge Graph

Em vez de:

```
TPS51125
```

Você passa a ter:

```
TPS51125

↓

Buck Controller

↓

PWM

↓

Notebook

↓

VCORE

↓

MOSFET

↓

Driver

↓

Bootstrap
```

Isso melhora muito respostas técnicas.

---

## 6) Parser de esquemas

Você comentou que quer analisar placas.

Eu faria:

```
PDF esquemático

↓

OCR

↓

Componentes

↓

Netlist

↓

Grafo
```

Depois:

```nginx
Qual MOSFET controla VCORE?

↓

Resposta imediata
```

---

## 7) Engenharia reversa

Criar um banco assim:

```
Componentes

↓

Datasheet

↓

Footprint

↓

Substitutos

↓

Falhas conhecidas

↓

Casos reais
```

Isso é ouro para bancada.

---

## 8) Memória por domínio

Ao invés de:

```
1 coleção
```

Ter:

```
Power

Audio

USB

Display

GPU

CPU

DDR

PMIC

EC

BIOS

Firmware
```

Cada domínio com embeddings próprios.

---

## 9) Agentes especializados

Ao invés de um agente.

Criaria vários.

```
Datasheet Agent

↓

PCB Agent

↓

Firmware Agent

↓

Reverse Engineering Agent

↓

Linux Agent

↓

Programming Agent

↓

Electronics Agent
```

Cada um com prompt diferente.

---

## 10) Sistema de confiança

Toda resposta recebe uma nota.

```
Fonte

↓

Tabela Oficial

100%
```
```
Texto

↓

90%
```
```
Inferência

↓

40%
```

Assim o usuário sabe quando confiar.

---

## Onde o OpenCode entra?

O projeto [^1] é um agente de programação open source para terminal, com agentes integrados ("build" e "plan"), suporte a ferramentas, execução de comandos e possibilidade de extensão. [^1]

**Eu não o usaria para responder perguntas técnicas.**

Eu o usaria como **engenheiro de software do AI-Lab**.

Por exemplo:

```
Você

↓

"Refatore o parser de datasheets"

↓

OpenCode

↓

Analisa o projeto

↓

Cria novos módulos

↓

Executa testes

↓

Abre Pull Request

↓

Atualiza documentação
```

---

## Aplicação prática no seu projeto

Você pode criar agentes como:

```
ParserAgent

Responsável por:

- OCR
- PDF
- tabelas
- imagens
```
```
SkillBuilderAgent

Responsável por:

- glossary
- cheatsheet
- patterns
- SKILL.md
```
```
RetrievalAgent

Responsável por:

- ranking
- reranking
- BM25
- Qdrant
```
```
RefactorAgent

Responsável por:

- detectar código duplicado
- melhorar arquitetura
- otimizar desempenho
```
```
TestAgent

Responsável por:

- criar testes unitários
- validar respostas
- detectar regressões
```

Como o OpenCode possui um agente de planejamento e outro de construção, ele pode automatizar boa parte desse ciclo de desenvolvimento. [^1]

---

## Minha proposta para o AI-Lab 2.0

Se fosse reestruturar o projeto do zero, eu dividiria em **10 módulos independentes**:

1. **Parser Engine** (OCR, PDFs, tabelas, imagens).
2. **Knowledge Builder** (gera skills estruturadas).
3. **Structured Database** (SQLite/DuckDB para especificações).
4. **Vector Engine** (Qdrant apenas para conteúdo narrativo).
5. **Knowledge Graph** (relações entre componentes e conceitos).
6. **Planner** (escolhe automaticamente a melhor estratégia para cada pergunta).
7. **Specialist Agents** (eletrônica, firmware, Linux, programação, etc.).
8. **Validation Engine** (confere respostas contra fontes oficiais e calcula confiança).
9. **Automation Layer** (OpenCode para refatoração, testes, documentação e manutenção do código).
10. **Desktop Interface** (painel para importar PDFs, acompanhar indexação, visualizar grafos e conversar com os agentes).

Na minha avaliação, essa arquitetura elevaria o AI-Lab de um bom sistema de RAG para uma plataforma de engenharia assistida por IA, mais próxima de um **copiloto técnico especializado em eletrônica e engenharia reversa** do que de um simples chatbot com busca em documentos.

---

**Você disse**

Isso fará com que o opencode analise seu projeto e crie um arquivo AGENTS.md na raiz do projeto. Dica Você deve commitar o arquivo AGENTS.md do seu projeto no Git. Isso ajuda o opencode a entender a estrutura do projeto e os padrões de codificação utilizados.

---

Sim. O `AGENTS.md` é uma das funcionalidades mais úteis do OpenCode, mas é importante entender o que ele faz e o que ele **não** faz.

## O que é o AGENTS.md?

É um arquivo de instruções para os agentes do OpenCode. Pense nele como uma mistura de:

- guia de arquitetura do projeto;
- convenções de código;
- regras de desenvolvimento;
- documentação operacional para a IA.

Ele é semelhante ao papel que arquivos como `CLAUDE.md`, `GEMINI.md` ou `copilot-instructions.md` desempenham em outras ferramentas.

O agente consulta esse arquivo antes de modificar o projeto.

---

## Por que isso é importante?

Sem um `AGENTS.md`, o agente precisa inferir tudo:

- arquitetura;
- convenções;
- organização das pastas;
- estilo de código;
- objetivos do projeto.

Isso aumenta a chance de ele gerar código inconsistente.

Com um bom `AGENTS.md`, você reduz bastante esse risco.

---

## No seu AI-Lab

Pelo que conheço do seu projeto, eu criaria um `AGENTS.md` contendo informações como:

### Estrutura do projeto

```nix
knowledge/
skills/
cache/
embeddings/
book/
cli/
llm/
retrieval/
planner/
parsers/
tests/
```

---

### Objetivo

```markdown
AI-Lab é um sistema local para engenharia eletrônica.

Prioridades:

1. precisão
2. rastreabilidade
3. evitar alucinações
4. funcionamento offline
5. modularidade
```

---

### Regras

Por exemplo:

```erlang
Nunca apagar código sem justificar.

Nunca remover compatibilidade.

Criar testes antes de grandes refatorações.

Sempre documentar novos módulos.

Toda função pública deve possuir docstring.

Nunca duplicar código.

Sempre preferir composição a herança.
```

---

### Como lidar com datasheets

```
Datasheets NÃO devem usar apenas embeddings.

Sempre extrair:

- Pin table
- Absolute Maximum Ratings
- Electrical Characteristics
- Timing
- Features

Salvar também em JSON estruturado.
```

Essa instrução orienta o agente a manter o comportamento desejado.

---

### Regras para RAG

```
Embeddings apenas para:

explicações

manuais

livros

whitepapers

Nunca para:

tabelas

registradores

especificações

valores elétricos
```

---

### Organização de agentes

Você pode definir papéis claros:

```
ParserAgent

responsável por:

OCR

PDF

imagens

tabelas
```
```
RetrievalAgent

responsável por:

BM25

Qdrant

Reranking
```
```
PlannerAgent

responsável por:

identificar tipo de pergunta

escolher pipeline
```
```
ValidationAgent

responsável por:

comparar resposta

fonte oficial

score de confiança
```

---

## Versionar no Git

A recomendação de manter o `AGENTS.md` no repositório faz sentido porque:

- qualquer colaborador (humano ou IA) recebe as mesmas instruções;
- os agentes trabalham de forma consistente;
- mudanças nas regras ficam registradas no histórico do Git e podem ser revisadas.

---

## Eu iria além

Para um projeto como o AI-Lab, eu manteria não apenas um `AGENTS.md`, mas um conjunto de documentos de arquitetura, por exemplo:

```
/
├── AGENTS.md
├── ARCHITECTURE.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── TESTING.md
├── KNOWLEDGE_MODEL.md
├── RETRIEVAL.md
├── PARSER.md
├── PLANNER.md
├── ELECTRONICS.md
└── docs/
```

Assim:

- **AGENTS.md**: instruções operacionais para os agentes.
- **ARCHITECTURE.md**: visão geral da arquitetura.
- **KNOWLEDGE\_MODEL.md**: como representar datasheets, manuais e esquemas.
- **RETRIEVAL.md**: regras para Qdrant, BM25, SQLite e seleção de fontes.
- **PLANNER.md**: como decidir entre consulta estruturada, busca vetorial ou explicação.
- **TESTING.md**: critérios e testes obrigatórios antes de aceitar mudanças.

## Minha recomendação

Para o seu projeto, eu não deixaria o OpenCode "descobrir" a arquitetura sozinho. Vale muito mais a pena escrever um `AGENTS.md` detalhado, alinhado com os objetivos do AI-Lab, e deixar o OpenCode usá-lo como referência durante todas as análises e refatorações. Isso tende a produzir alterações mais consistentes e evita que o agente tome decisões que conflitem com a direção técnica que você definiu para o projeto.

[^1]: [github.com](https://github.com/anomalyco/opencode?utm_source=chatgpt.com)