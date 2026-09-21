---
name: context-mode
description: >-
  Gestão de contexto longo para agentes via sandboxing de saída de ferramentas,
  retenção FTS5 e recuperação pós-compactação (helenizada de
  kujohnson/context-mode). Use quando tool outputs volumosos estourarem a
  janela, quando a sessão se aproximar de PreCompact, ou para recuperar
  contexto perdido após compactação/limpeza.
---
# Context Mode (helenizada)

## Origem (antropofagia)
- **kujohnson/context-mode** (MIT) — skill para contexto longo: sandbox de tool
  output, SQLite FTS5 como buffer de recuperação, snapshot PreCompact.
- Integrada com a regra global **R-context-compaction** (ARMARENAR → COMPACTAR → LIMPAR).

## Pilares

### 1. Sandboxing de saída de ferramentas
Tool outputs volumosos (grep/read de arquivos grandes, logs, diffs) **não** vão
inteiros para o contexto — vão para um buffer SQLite e o contexto recebe só um
resumo + ponteiro de recuperação.

**Quando aplicar:**
- Output > ~2.000 tokens estimados.
- Comando que vai retornar > 200 linhas.
- Leitura de arquivo > 300 linhas (usar codegraph/Read com offset/limit).

**Fluxo:**
1. Rodar o comando normalmente.
2. Gravar output bruto em `harness/cache/ctxmode/` (arquivo por turno).
3. Inserir no índice FTS5 com payload completo.
4. Injetar no contexto apenas: resumo (3-5 bullets) + `CTXREF:<id>` para re-leitura sob demanda.

### 2. Retenção FTS5
Índice SQLite FTS5 em `harness/cache/ctxmode/index.sqlite`:

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS ctx_out USING fts5(id, kind, summary, payload);
-- id: CTXREF-<timestamp>; kind: grep|read|log|diff|probe
```

**Recuperação:** ao ver `CTXREF:<id>` no contexto, consultar:
```sql
SELECT payload FROM ctx_out WHERE id = 'CTXREF-<id>';
```
e devolver APENAS o trecho pedido (offset/limit), nunca o payload inteiro.

### 3. Snapshot PreCompact (recuperação pós-compactação)
Disparado por `system-reminder CONTEXT COMPACTION TRIGGER` (~96% da janela) **ou**
~50% da janela (regra R-context-compaction do harness):

1. **ARMARENAR**: gravar estado do workflow em `harness/cache/ctxmode/snapshot-<ts>.json`
   (objetivo, fase, tasks pendentes, decisões, arquivos tocados, CTXREFs ativos).
2. **COMPACTAR**: resumir o histórico; manter só o essencial (vetor de estado).
3. **LIMPAR**: encerrar subagentes antigos, limpar buffers intermediários.
4. **RECUPERAR**: ao retomar, ler o snapshot mais recente e reconstruir o vetor
   de estado antes de continuar — NUNCA recomeçar do zero.

## Contrato do vetor de estado (obrigatório no snapshot)
```json
{
  "workflow": "gran-mestre",
  "fase": "F4",
  "objetivo": "<pedido original>",
  "pending": ["<task>", "..."],
  "decisions": ["<decisões tomadas>"],
  "files_touched": ["<caminhos>"],
  "ctxrefs": ["CTXREF-..."]
}
```

## Anti-padrões (proibido)
- **NUNCA** injetar output bruto de ferramenta no contexto sem sandbox.
- **NUNCA** compactar sem ARMARENAR primeiro (perde estado → alucinação).
- **NUNCA** recomeçar workflow do zero após compactação — sempre recuperar do snapshot.

## Integração com o harness
- Complementa `context-compaction` (skill global) e `pxpipe` (compressão de entrada).
- Buffer: `harness/cache/ctxmode/` (criar dir no primeiro uso; ignorar falha de escrita).
