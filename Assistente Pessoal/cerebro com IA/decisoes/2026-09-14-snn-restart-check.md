# Restart-check SNN — 2026-09-14 (Gari R99, veredito honesto)

- Gatilho: pergunta direta do usuário "posso reiniciar ou ainda existem pendencias" (R99).
- Veredito: **PODE REINICIAR — nada se perde (restart-safe), MAS existem 3 pendências SNN** (parked-blocked, 100% persistidas). Mascarar como zero seria fraude (anti-padrão Gari).

## Pendências reais (pipeline `pipeline/2026-09-13-snn-conectoma-CONTEXT.md`)

| # | Task | RunID parked | Estado |
|---|---|---|---|
| 1 | Planner spec §§7–10 (4 selfs R90, "imitando um cérebro" = imitação funcional) | `0cb3ed3a` snn-plan-selfs-7a10-retry / resume `7e5a9032` | PARKED-BLOCKED-410 |
| 2 | Import MaleCNS (FaseA research URLs + gate 5GB + FaseB streaming) | `5b5c3d48` snn-malecns-import / resume `cd1886fa` | PARKED-BLOCKED-410 |
| 3 | Fix P2–P3 (criar `snn/__init__.py` + normalizar `from snn.*`→top-level, ≤4 arqs) | `e513414d` snn-fix-p2p3-imports / resume `c5dd659f` | PARKED-BLOCKED-410 |

Packets integrais reconstruídos a partir do ground truth em disco: ver bloco
`[Packets-2026-09-14-restart-check]` no pipeline CONTEXT.md (3 envelopes + run_ids + budgets 10k/12k/6k).

## Evidência fresca desta sessão (por que estão parked)

- Task cloud 410 ×2: `ses_f5efe27b` (explorador-tool), `ses_f5efe150` (general) —
  modelo pinado `deepseek-ai/deepseek-v4-pro-0813` EOL em 2026-09-14T08:00Z. 13/13 agents cloud pinam o morto.
- `OPENCODE_CONFIG` ATIVO (`.../session-cloud-route.json` → flash-0731) mas o **Task-tool ignora o override**
  (override só vale p/ `opencode run` CLI). Retry cego proibido (R9) — 2 probes bastam.
- Probe `sdd-executor` local (`ses_f5efc3d2`): responde mas retorna LIXO (`ok|ok|ok|…`, sem exit_status,
  sem responder ao acceptance) → `NAO_PASSOU_CATEGORICO` no anti-lixo gate. Canal local imprestável p/ planejar/codar.
- Dívida P2–P3 confirmada em disco: `snn/__init__.py` NÃO existe; 3 arquivos usam forma `snn.*`
  (`test_parser.py`, `test_pin.py`, `pin.py`) vs 7 em forma top-level — suite só passa rodada de dentro de `snn/`.
- `snn/` está UNTRACKED no git (nunca commitado) → `git reset --hard` não o toca, mas `git clean` o apagaria.
  NENHUM reset/clean executado. Risco registrado, nenhuma ação irreversível tomada.
- Slots locais 7/7 health ok (8083/9084/9086/9088/9090/9092/9093); Qdrant ok (3 collections);
  auditoria paralela: 10 OTs rankeadas AGUARDANDO ORDEM do usuário (não bloqueiam restart).

## Pérolas quantitativas

- 410 Gone ×2 (cloud), lixo-local ×1, health 7/7, Qdrant 3 collections, snn/ 15 `.py` untracked,
  imports mistos 3-vs-7, suite 22 passed (pré-existente, sem regressão — nada foi tocado).

## Pérolas qualitativas

- Task-tool ≠ `opencode run`: OPENCODE_CONFIG não re-pina a frota Task; restart NÃO destrava sozinho.
- Destravar exige UMA destas (todas precisam de ordem explícita, nada automático):
  (a) re-pinar os 13 agent files p/ modelo vivo (muse-spark provado vivo — sou a prova);
      mutação do harness em meio à auditoria → G4/soberania;
  (b) despacho via `opencode run` CLI com o session-cloud-route (canal ainda não provado — 1 probe bounded pendente);
  (c) aguardar backend Task suportar modelo vivo.
- Auditoria mantém routing provisório até seu fim — não tocar `session-cloud-route.json` sem ordem.

## Pós-restart

Re-despachar os 3 packets do bloco `[Packets-2026-09-14-restart-check]` do CONTEXT assim que houver
canal vivo (prova de vida ANTES do side-effect; R9). Nenhum gate humano pendente além da escolha (a/b/c).
