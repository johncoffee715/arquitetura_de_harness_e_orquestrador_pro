---
name: professional-decompilation
description: "Descompilação e engenharia reversa profissional de binários, firmware, bibliotecas, executáveis e componentes embarcados — metodologia baseada em evidências (nunca hipótese vira fato sem prova). Pipeline INTAKE→IDENTIFICATION→FINGERPRINT→TRIAGE→STATIC/DYNAMIC→CORRELATION→RECONSTRUCTION→VALIDATION→REPORT, com classificação de confiança (CONFIRMED/HIGH_CONFIDENCE/PROBABLE/POSSIBLE/UNKNOWN/CONTRADICTED), base de evidências E-XXX, hypothesis engine e output contract. Use para analisar binário, firmware, BIOS/UEFI, ROM dump, malware, executável desconhecido, descompilar função, entender protocolo embarcado, reconstruir estrutura de dados ou produzir relatório técnico reproduzível de RE. Integra com o agente reverser (GhidraMCP) e com fable-judge para validação adversarial das conclusões."
user-invocable: true
allowed-tools: "Read Bash Glob Grep Task WebSearch WebFetch"
metadata:
  version: "1.0.0"
  author: "OpenCode Gran-Mestre (helenizada do documento 'Professional Binary Decompilation & Reverse Engineering' fornecido pelo usuário)"
  source: "Documento do usuário — Professional Binary Decompilation & Reverse Engineering"
  license: "MIT"
  helenizado_em: "2026-08-15"
---

# professional-decompilation — Descompilação & Engenharia Reversa Profissional

A descompilação transforma um programa compilado (código de máquina/binário) de volta em uma representação legível por humanos (código-fonte/pseudocódigo/modelo comportamental).

## Princípio central

> **Nunca transformar uma hipótese em fato sem evidência suficiente.**

O objetivo não é produzir um código-fonte bonito. É produzir um **modelo comportamental verificável** do artefato original.

---

## 1. Quando usar (triggers)

- Análise de binário, firmware, BIOS/UEFI, ROM dump, malware, executável desconhecido;
- Descompilar/entender uma função, restaurar pseudocódigo, mapear fluxo de execução;
- Identificar formato, arquitetura, toolchain, packing, crypto indicators;
- Reconstruir estruturas de dados, protocolos, interfaces, hardware interaction;
- Produzir relatório técnico reproduzível de RE;
- Correlacionar análise estática com comportamento dinâmico (sandbox/VM).

**Roteamento no harness:** análise pesada → delegar ao agente `reverser` (GhidraMCP + web + bash). Esta skill define a **metodologia**; o `reverser` executa as ferramentas. Antes de declarar conclusões, validação adversarial via `fable-judge`.

## 2. Classificação de confiança (obrigatória em toda conclusão)

```text
CONFIRMED       — comprovado (múltiplas fontes independentes convergem)
HIGH_CONFIDENCE — evidência forte
PROBABLE        — hipótese altamente plausível
POSSIBLE        — hipótese plausível
UNKNOWN         — insuficiência de evidência
CONTRADICTED    — hipótese contradita
```

Toda conclusão deve rastrear:

```text
CONCLUSÃO → EVIDÊNCIA → MÉTODO DE OBTENÇÃO → VALIDAÇÃO
```

## 3. Separação fato × hipótese

NUNCA escrever: `A função inicializa o controlador PWM.`
quando a evidência apenas demonstra:
`A função escreve repetidamente em endereços compatíveis com registradores de controle e posteriormente aguarda alteração de estado.`

O primeiro é conclusão. O segundo é evidência. Formular como hipótese com nível de confiança, nunca como fato.

---

## 4. Pipeline

```text
INPUT → [INTAKE] → [IDENTIFICATION] → [FINGERPRINT] → [TRIAGE]
        → STATIC ANALYSIS / DYNAMIC ANALYSIS → [CORRELATION]
        → [RECONSTRUCTION] → [VALIDATION] → [REPORT]
```

---

## 5. Fase 0 — INTAKE

Registrar (YAML):

```yaml
artifact:
  name:            # nome
  path:            # caminho
  size:            # bytes
  hash_sha256:     # hash
  acquisition_method:
  acquisition_date:

environment:
  host_os:
  architecture:
  tools:           # ghidra/radare2/binwalk/objdump/strings/xxd/capa/etc.

authorization:
  authorized: true
  scope:           # limites da autorização
```

- **Nunca modificar o artefato original.** Criar cópia de trabalho (hash antes/depois).

## 6. Fase 1 — IDENTIFICATION

Determinar: formato, arquitetura, endianness, ABI, OS provável, toolchain provável, versão, packing, compression, encryption indicators, debugging info, symbols, sections, entry point.

```yaml
binary_identity:
  format:          # ELF/PE/Mach-O/UEFI/raw firmware/...
  architecture:    # x86/ARM/ARM64/MIPS/RISC-V/...
  bits:
  endian:
  abi:
  os:
  compiler:
  linker:
  packer:
  encryption:
  confidence:
```

## 7. Fase 2 — FINGERPRINT

Coletar: SHA-256, SHA-1, MD5, tamanho, entropia, strings, imports, exports, sections, relocation data, symbols, version info, embedded resources, timestamps, compiler signatures.

> ⚠️ **Nunca confiar isoladamente em timestamps ou metadata** (são falsificáveis/irrelevantes).

## 8. Fase 3 — TRIAGE

Responder primeiro:

1. O que é este artefato?
2. Qual arquitetura?
3. Onde está o entry point?
4. Quais componentes principais?
5. Quais APIs externas são utilizadas?
6. Sinais de packing? Regiões comprimidas? Criptografadas?
7. Existem símbolos? Strings úteis?
8. Quais funções parecem críticas?
9. Quais áreas merecem análise prioritária?

Produzir triage score:

```text
TRIAGE SCORE
Architecture       [HIGH/MEDIUM/LOW]
Format             [HIGH/MEDIUM/LOW]
Symbols            [HIGH/MEDIUM/LOW]
Strings            [HIGH/MEDIUM/LOW]
Imports            [HIGH/MEDIUM/LOW]
Packing            [HIGH/MEDIUM/LOW]
Crypto indicators  [HIGH/MEDIUM/LOW]
Interesting funcs  [HIGH/MEDIUM/LOW]
```

---

## 9. Fase 4 — STATIC ANALYSIS

### Control Flow

basic blocks, branches, loops, switch/case, exception paths, indirect calls, function pointers, tail calls, recursion.

### Data Flow

Rastrear `SOURCE → TRANSFORMATION → STORAGE → CONSUMER` para cada variável importante: origem, transformação, destino, tipo provável, largura, signedness, lifetime.

## 10. Funções — registro obrigatório

Cada função relevante recebe um registro:

```yaml
function:
  address:          # ex: 0x401230
  name:             # FUN_00401230 até haver evidência
  size:
  calling_convention:
  arguments:
  return_value:
  callers:
  callees:
  side_effects:
  globals_read:
  globals_written:
  strings:
  constants:
  behavior:
  confidence:
```

> **Não renomear prematuramente.** Preferir `FUN_00401230` até existir evidência suficiente para `InitializeMotorController`. Quando renomear, preservar o nome original como comentário (`// formerly FUN_00401230`).

## 11. Data structures

Identificar: structs, arrays, linked lists, trees, vtables, object layouts, buffers, ring buffers, packet structures, configuration blocks.

Registrar offsets:

```text
struct candidate:
+0x00 uint32_t
+0x04 uint16_t
+0x06 uint16_t
+0x08 pointer
+0x10 buffer[32]
```

Não atribuir semântica definitiva sem validação.

## 12. Strings

Classificar: `ERROR | DEBUG | PROTOCOL | FILE PATH | REGISTRY | COMMAND | NETWORK | UI | CONFIGURATION | UNKNOWN`.

Correlacionar cada string com: função, XREF, bloco, chamada, contexto.

> Uma string isolada **não constitui prova** da funcionalidade.

## 13. Imports / Exports

Construir mapa `MODULE → API → CALLERS/PARAMETERS/PURPOSE`. Priorizar APIs de: filesystem, networking, cryptography, memory, process/thread, device I/O, synchronization, graphics, serial, USB, PCIe, hardware registers.

---

## 14. DYNAMIC ANALYSIS

Quando permitido e seguro, correlacionar:

```text
STATIC ADDRESS ↔ RUNTIME ADDRESS ↔ INPUT ↔ STATE CHANGE ↔ OUTPUT
```

Observar: chamadas, argumentos, retornos, memória, arquivos, sockets, syscalls, threads, locks, exceptions, hardware I/O.

Executar preferencialmente em: VM, sandbox, equipamento dedicado, ambiente isolado. **Nunca em ambiente não seguro.**

## 15. HYPOTHESIS ENGINE

Para comportamento desconhecido:

```yaml
hypothesis:
  id: H-017
  statement:       # ex: "A função controla uma máquina de estados"
  evidence:        # [E-031, E-032, E-041]
  counter_evidence:
  tests:
    - test:        # "Alterar condição de entrada e observar transição"
      expected:
      result:
  confidence:      # CONFIRMED / HIGH_CONFIDENCE / ...
```

## 16. EVIDENCE DATABASE

Toda descoberta relevante recebe ID `E-001, E-002, ...`:

```yaml
evidence:
  id: E-001
  address:
  type:            # STRING | XREF | CALL | MEMORY | REGISTER | CONTROL_FLOW
                   # DATA_FLOW | RUNTIME | SYMBOL | IMPORT | EXPORT | PROTOCOL | TRACE
  observation:
  source:
  reproducible:    # true/false
  confidence:
```

## 17. CORRELATION ENGINE

Correlacionar `STRING → XREF → FUNCTION → CALLER → DATA → RUNTIME`.

> Uma conclusão ganha confiança quando **múltiplas fontes independentes convergem**.

## 18. Prioridade de investigação

`Priority = Impact × Evidence Density × Centrality × Unknownness`

Prioridade máxima: entry point, dispatcher, initialization, hardware abstraction, protocol parser, state machine, configuration, authentication, critical algorithms, error handling.

---

## 19. Validação — checklist por função

- [ ] fluxo de entrada compreendido;
- [ ] argumentos identificados;
- [ ] retorno identificado;
- [ ] principais branches explicados;
- [ ] principais variáveis explicadas;
- [ ] callers conhecidos;
- [ ] callees relevantes conhecidos;
- [ ] efeitos colaterais conhecidos;
- [ ] hipótese testada;
- [ ] evidências registradas.

Se algum item crítico estiver ausente: `STATUS = PARTIALLY UNDERSTOOD` (nunca declarar compreendida).

## 20. RECONSTRUCTION

Quando possível: `Original binary → Function map → Data model → Control-flow model → Behavior model → Pseudocode → Reconstructed implementation`.

O pseudocódigo deve preservar: condições, loops, chamadas, side effects, estados, erros, dependências. **Não "embelezar"** a ponto de perder correspondência com o binário.

## 21. Comparação com código reconstruído

Se houver implementação reconstruída, validar `SOURCE ↔ ASSEMBLY ↔ BINARY ↔ RUNTIME`: comportamento, branches, constantes, estruturas, calling convention, side effects, resultados.

---

## 22. FAILURE POLICY

```text
1. Registrar erro.
2. Preservar evidências já coletadas.
3. Identificar causa.
4. Tentar método alternativo.
5. Não apagar resultados anteriores.
6. Marcar área como inconclusiva se necessário.
```

> **Nunca preencher lacunas inventando comportamento.**

## 23. STOP CONDITIONS

Parar uma linha de investigação quando: evidência insuficiente; hipótese refutada; custo > benefício; análise depende de informação indisponível; ambiente não seguro; alteração do artefato comprometeria evidências.

Registrar:

```text
STOP_REASON
CURRENT_KNOWLEDGE
MISSING_INFORMATION
NEXT_REQUIRED_TEST
```

---

## 24. RELATÓRIO FINAL — estrutura

```text
1.  Executive Summary
2.  Artifact Identification
3.  Architecture
4.  Toolchain / Compiler
5.  Binary Layout
6.  Entry Point
7.  Function Map
8.  Data Structures
9.  Control Flow
10. Protocols / Interfaces
11. Runtime Behavior
12. Important Algorithms
13. Hardware Interaction
14. Configuration
15. Error Handling
16. Unknown Components
17. Hypotheses
18. Evidence
19. Validation
20. Confidence Assessment
21. Limitations
22. Reproduction Procedure
23. Conclusions
```

## 25. OUTPUT CONTRACT

Toda execução deve terminar produzindo:

```yaml
analysis:
  artifact:
  architecture:
  format:
  entry_point:

coverage:
  functions_identified:
  functions_analyzed:
  data_structures:
  protocols:
  runtime_paths:

confidence:
  confirmed:
  high_confidence:
  probable:
  possible:
  unknown:
  contradicted:

evidence:
  total:
  reproducible:

limitations:
next_steps:
```

---

## 25.5 REVERSÃO AO ECOSSISTEMA OPencode

A descompilação **reverte para o ecossistema do OpenCode**: o conhecimento extraído
não termina no relatório — é absorvido pelo harness (R14/R26). Após o REPORT:

### 1. Memória cerebral (Obsidian)
Arquivar em `/mnt/dados/cerebro com IA/`:
- `wiki/summaries/` — summary da análise (artifact, arquitetura, achados-chave);
- `wiki/concepts/` — conceitos descobertos (protocolo, formato, algoritmo, struct);
- `wiki/entities/` — entidades identificadas (funções renomeadas, módulos, componentes);
- `decisoes/` — decisão datada `YYYY-MM-DD-<assunto>.md` (o que foi concluído e com que confiança);
- append em `wiki/log.md` (fluxo de ingestão padrão do harness).

### 2. Skills / instintos (R36)
Padrão repetido 2+ vezes (mesmo tipo de offset, mesma API, mesmo padrão de firmware)
→ registrar como skill/instinto reutilizável (`/learn` ou skill helenizada nova).

### 3. Catálogo e registry (R-catalog)
Novos artefatos/ferramentas/descobertas → `harness/registry.json` via `build_registry`/`registry-sync`.

### 4. Relatório de retorno ao orquestrador
Entregar ao Gran-Mestre: resumo executivo, confidence assessment, evidence DB,
limitações e next steps — para o orquestrador decidir follow-ups.

> A análise só está completa quando o conhecimento **retornou ao ecossistema**
> (memória + catálogo + lições), não apenas quando o relatório foi escrito.

---

## 26. Regra mestra do agente

Pensar como um engenheiro de RE:

```text
OBSERVE → MEASURE → MODEL → HYPOTHESIZE → TEST → CORRELATE → VALIDATE → DOCUMENT
```

Nunca:

```text
GUESS → ASSUME → DECLARE
```

## 27. DEFINITION OF DONE

A análise somente está concluída quando:

- [ ] artefato identificado;
- [ ] arquitetura determinada;
- [ ] entry point localizado;
- [ ] mapa funcional mínimo construído;
- [ ] estruturas críticas modeladas;
- [ ] fluxo principal compreendido;
- [ ] hipóteses relevantes classificadas;
- [ ] evidências vinculadas às conclusões;
- [ ] limitações explicitadas;
- [ ] resultados reproduzíveis.

**Antes do done:** rodar `fable-judge` contra as conclusões (re-executar cada verificação afirmada; rotular UNVERIFICÁVEL o que não puder ser re-rodado) e conferir o output contract (seção 25).

**Princípio final:**

> O objetivo da descompilação profissional não é produzir um código-fonte bonito. É produzir um **modelo comportamental verificável** do artefato original.