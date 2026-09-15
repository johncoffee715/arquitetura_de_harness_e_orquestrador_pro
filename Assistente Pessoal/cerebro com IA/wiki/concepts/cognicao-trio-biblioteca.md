---
tags: [concept, cognicao, snn, biblioteca, trio]
related: [[snn/snn-motor-indice]] [[snn/snn-conectoma-malecns-indice]] [[snn/snn-mb-corpos-cogumelo]] [[snn/snn-cx-complexo-central]] [[snn/snn-ppl101-dopamina]]
last_updated: 2026-09-14
decisao-em: decision-log 2026-09-14T22:30:00Z (papeis travados pelo usuário)
---

# Cognição do Trio da Biblioteca — RWKV7 + Needle 2 + Qwen3-Embedding

A ideia cognitiva: o ecossistema não "usa" a biblioteca — a biblioteca **é um órgão do
cérebro vivo**. Três LLMs locais com papéis travados pelo usuário (2026-09-14) compõem
o loop cognitivo que liga a topologia real do MaleCNS (SNN) ao vault Obsidian.

## Papéis (travados por decisão do usuário)

| Papel | Modelo | Slot | Função cognitiva |
|---|---|---|---|
| **Bibliotecário** | RWKV7-G1d-0.4B | :9084 | **Decide** (`ignorar/ler/agir`) — tem **autonomia total** dentro da biblioteca. É o córtex de decisão do trio: lê o resumo da atividade neural e julga o que fazer com a nota. |
| **Assistente** | Needle 2 | :9091 | **Executa** — extração cirúrgica de conteúdo (a "mão" do bibliotecário). Recebe a intenção e entrega o texto exato. |
| **Secretário** | Qwen3-Embedding-0.6B-Q8_0 | :9094 | **Registra** — vetoriza cada episódio (1024-dim). É a memória de curto prazo pesquisável: tudo que o cérebro vive vira vetor re-encontrável. |

### Implementação real do Secretário (Hefesto, 2026-09-15)

Deixou de ser só papel — existe como **skill `secretario`** (`~/.config/opencode/skills/secretario/`,
quarteto R85 completo + tooling): triagem semântica (cosseno puro via :9094/:9097), registro
vetorial real na coleção Qdrant **`bibliotecario_1024`** (payload `origem: secretario`), agenda
determinística, correspondência com frontmatter estrito, diário JSONL auditável com quarentena.
Quando o motor SNN precisar de memória semântica (hoje: embedding cru em live_loop), a rota
evolutiva é chamar `secretario/tooling/registro.py` — memória do cérebro passa a ser
recuperável por busca híbrida real (lexical + vetorial), não só por data.

## O loop cognitivo (como roda de verdade — provado E2E)

```
nota nova/editada no vault (estímulo sensorial)
  → daemon_vault (debounce 3s, taxa 1/10s, fila 5)         [tálamo do sistema de arquivos]
  → motor SNN avança na topologia MaleCNS real (CSR)       [córtex sensório-motor]
  → resumo da atividade → RWKV7 :9084 classifica           [BIBLIOTECÁRIO decide]
       ↳ 'ler'|'agir' → Needle 2 acionado                  [ASSISTENTE executa]
       ↳ episódio inteiro → Qwen3-Embedding :9094          [SECRETÁRIO registra (vetor)]
  → write-back na nota (## Cérebro episódio) com
    marcador <!-- snn-episode (anti-loop, prova 2º run = 0)
  → live_state.json + daemon_episodes.jsonl                [memória sináptica durável]
  → reinforce(±) via PPL101 → eficácias ajustadas          [cerebelo calibrando rotas]
```

## Por que isso é "cérebro" e não ilustração

1. **Reatividade bidirecional real**: LLM→vault (write-back com marcador) e vault→LLM
   (daemon) — não topologia estática.
2. **Memória sináptica persistente**: eficácias em `live_state.json` sobrevivem a restart
   (diferencial vs DOOMFLY, que perdiam ao parar a run).
3. **Aprendizado provado**: reforço +1 elevou a rota r2 de 17→51 spikes (probe 3 episódios,
   reproduzido pelo juiz 17→34→51).
4. **Anatomia real**: regiões por `anatomy.py` (body→região MaleCNS), não `i%4`.
5. **Autonomia de papel**: o Bibliotecário (RWKV7) manda no vault; o modelo com W7 ganhou
   postura curiosa (na dúvida → 'ler') — o cérebro agora lê por conta própria
   (prova: decisão 'ler' em nota real, spikes=158, episódio 1789437471).

## Fronteiras honestas (não é mágica)

- Embedding ≠ entendimento semântico profundo; o Secretário indexa p/ recuperação vetorial,
  não p/ síntese.
- Needle 2 executa extração, não raciocínio aberto (GBNF estrito forja é o forte).
- O SNN roda fatia (slice CSR), não os 166k simultâneos — biologicamente fiel (1–2% ativo),
  computacionalmente honesto.
- B3: PPL101 no código é rótulo funcional (a formula biológica fina segue UNKNOWN).

## Histórico

- 2026-09-14: pipeline motor-funcional W0→W7 completo (50→51 passed; juiz R34 92.5/100);
  papéis travados; classify W7 = bibliotecário curioso; W6 = write-back + anatomia real.
