---
regra: R107
titulo: "GUARDRAIL UNIVERSAL — todo vídeo lido pelo orquestrador na sessão TEM transcrição automática (ou falha declarada)"
fonte: user session 2026-09-18 (ordem explícita)
data: 2026-09-18
---

# ═══ REGRA GLOBAL R107 — TRANSCRIÇÃO AUTOMÁTICA DE TODO VÍDEO LIDO — promulgada 2026-09-18 ═══

**Regra**: nenhum vídeo (URL ou arquivo local) é "absorvido" pelo orquestrador sem trilha de texto.
No mesmo ciclo de leitura (antes do próximo verbo da sessão), a transcrição é executada e o artefato
cai no vault. Vídeo sem transcrição ao fim da sessão = **NAO_PASSOU_CATEGORICO** do encerramento
(o Gari R99 verifica: sessão que leu vídeo e não gerou transcrição não fecha limpo).

<Workflow (fail-closed)>
1. **URL YouTube/estréia**: caminho PRIMÁRIO é `yt-dlp` (pipeline vivo, R: `aprendizados/2026-09-09_pratica-padrao-ingestao-transcricoes.md`):
   legendas manuais primeiro; senão auto-subs; línguas PT + EN/ES + original quando útil.
   Limpar cues/timestamps → texto corrido deduplicado.
2. **Arquivo local (mp4/mkv/webm/mp3/wav)**: `scripts/attach_media.py` (ffprobe → wav 16k mono → ASR).
   **ASR local ATIVO desde 2026-09-18** (reparo `asr-20260918-001`): whisper.cpp rebuildado em path
   PERMANENTE `programas de apoio/whisper.cpp/` (CPU-only, ggml-base.bin 141MB) — defaults do
   attach_media.py apontam para lá. Se ainda assim falhar (arquivo sem fala / ASR quebrado de
   novo) ⇒ registrar `transcricao.asr_indisponivel` no decision-log e sinalizar ao usuário —
   NUNCA fingir absorção completa.
3. **Sem fala / sem legenda / ASR falhou** ⇒ saída honesta `sem_fala_detectada`/`transcricao_falhou`
   com motivo — vídeo conta como "lido com ressalva", nunca como absorvido pleno.
4. Sem internet/serviço fora ⇒ mesma disciplina: falha declarada, não absorção silenciosa.

<Destino canônico (frontmatter obrigatório — padrão vivo do acervo)>
`cerebro com IA/textos, pdf e esquemas/<VIDEOID_ou_slug>-transcricao-<LANG>.md` com YAML:
video_id · titulo · url · canal · publicado · duracao · etiquetas_4selfs [S-ca|H-e|L-e|A-m]
· origem_legenda (auto-sub/whisper/parcial) · data_ingestao · cues · nota_relevancia.
Corpo: texto limpo deduplicado, SEM timecodes. Indexar na sessão (bibliotecario/R86)
na próxima janela útil — não travar a leitura atual.

<Anti-padrões (recusa imediata)>
- "Assistir"/ler vídeo sem gerar a trilha (R28: absorção sem artefato = fraude de entrega).
- Fingir transcrição quando ASR indisponível (partial vazio apresentado como completo).
- Transcrição fora do path canônico ou sem frontmatter (não indexável = não existe).
- Timecodes na versão limpa final (poluem RAG).
- Blob de vídeo adicionado ao prompt (orquestrador lê TEXTO, nunca bruto — R70).

<Régua de cumprimento (R34)>
100% dos vídeos lidos na sessão têm arquivo `*-transcricao-*.md` válido OU exceção declarada
com motivo no decision-log. Qualquer coisa < 100% sem declaração ⇒ NAO_PASSOU_CATEGORICO.
</Régua>
