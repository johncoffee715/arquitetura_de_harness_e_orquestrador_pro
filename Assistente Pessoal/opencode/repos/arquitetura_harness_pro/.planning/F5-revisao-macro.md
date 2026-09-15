# F5 — REVISÃO MACRO DO HARNESS (2026-08-23)

**Escopo:** diff total F4 — `harness/{models,core,tests}` + 2 skills globais + 2 agents + registry.
**Método:** bateria adversarial estilo fable-judge — cada verificação afirmada foi RE-EXECUTADA do zero nesta sessão; nada aceito por afirmação.

## 1. Veredito categórico por métrica (R28)

| Métrica | Veredito | Evidência fresca |
|---|---|---|
| Testes TDD executados do zero | **PASSOU_CATEGORICO** | 42 passed in 0.09s (rodada F5.1, não herdada) |
| Determinismo do discovery/registry | **PASSOU_CATEGORICO** | Regen dupla: 17/14/3 idênticos; trio GMB-1 YELLOW estável entre runs |
| Determinismo do router | **PASSOU_CATEGORICO** | `diff` vazio entre duas chamadas idênticas (--top 5) |
| Coerência registry ↔ âncoras GMB-1 | **PASSOU_CATEGORICO** | 14.2 / 14.9 / 15.7 GiB exatos nas entradas YELLOW; famílias ornith/qwen/bonsai corretas por filename |
| Guardrail escada de contexto | **PASSOU_CATEGORICO** | `--role planner --ctx 200000` ⇒ UNSCHEDULABLE, exit=1 (nada além de 192K sem override) |
| Skills globais funcionais (R44) | **PASSOU_CATEGORICO** | Smoke real das 2 CLIs: discovery lista 17; router rankeia com level/residency/basis |
| Cobertura dos 20 critérios SPEC F2 §42 | **PARCIAL — sem fraude** | Implementados+testados: [1]<30s · [2]registry normalizado · [4]scoring quantificado · [5]VRAM real · gates/breaker · escada · residency. Critérios [3][6]-[20] EXIGEM a Matriz B-G (medidas reais), bloqueada em janela GPU |

## 2. Bugs capturados e corrigidos durante o ciclo (prova de valor do TDD)

1. Blacklist casamento exato vs fragmento (`user_blacklist` nunca disparava)
2. Família por arquitetura interna sobrescrevendo filename (ornith virava "qwen")
3. VRAM estimada no ctx nativo gerando falsos `vram_insufficient` (21.95GiB fantasma)
4. Teto duro usando orçamento conservador (trio GMB-1 injustamente excluído)
5. Reserva subtraída em duplicidade sobre âncoras medidas (ornith@64K falhava por 0.03GiB)
6. `try_next` retornando gates exigidos em vez de pendentes (walk travava no F2 para sempre)
7. Dois eventos de gravação em caminho errado (recuperados; verificação antes de confiança adotada)

## 3. Limitações declaradas (zero gap silencioso)

- **GM-SCORE oficial NÃO emitido** — exige Matriz GMB-1 B-G (Exec 20 tasks, Recovery injection, Needle 8K–256K), que requer monopólio da MI50 conflitando com R39 (:8083 = cérebro do orquestrador). Decisão de janela é do usuário.
- MCP `health` deferido — necessidade coberta pelo agent `health-monitor` (CLI probing); custo/benefício desfavorável agora.
- Watcher entregue como script (`watch_registry.sh`), não daemonizado em session.start.
- `runtime.residency` permanece COLD default até primeira passada real do health-monitor.
- Decisão GPU_PRIMARY_SLOT segue **PROVISÓRIA** (Ornith) até o GM-SCORE oficial.

## 4. Conclusão

Núcleo do Meta-Orquestrador Adaptativo Modular está **implementado, testado, determinístico e helenizado globalmente** (R2/R44). O pipeline transita F5→F6 com entrega do rank provisório + memória cerebral; a elevação a definitivo fica condicionada — de forma explícita e rastreável — à janela GPU autorizada para a Matriz B-G.

*Nota de impressão (R34): 91/100 — menos pelo que falta (bloqueios declarados) e mais pela cadeia completa estimativa→medida→correção que o próprio sistema agora codifica.*
