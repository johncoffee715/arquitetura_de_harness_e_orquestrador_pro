# Pipeline AUDITORIA-STACK — CONTEXT.md (working, dono: Gran-Mestre)

- [Safety] SHA: pending (snapshot via subagent bash-leve)
- [Phase] ts=2026-09-15T00:00:00Z F0-ingest done | Route: explorador-tool + bibliotecario paralelo | Budget ~2subs/teto-ok | Trajectory pass
- [Phase] ts=2026-09-15T00:00:00Z P1-readonly done | Route: 2x explorador-tool | Gate: ok (12=9+3, 10=9+1duplo, 9 stale) | Trajectory pass
- [Authorize] ts=2026-09-15T00:00:00Z HUMAN_APPROVE — usuário autorizou P2 correção stale (O1+O3, reversível git checkout, sem restart) → "sim"
- [RunID] ts=2026-09-15T00:00:00Z d5e4f6a4-3333-4333-8333-333333333333 fix-manifesto-stale blocked (guard-gap-p5: path fora workdir/governança, zero writes, retry cego proibido R9)
- [Phase] ts=2026-09-15T00:00:00Z P2-blocked | Gate: NAO_PASSOU_CATEGORICO (write negado, diff preparado não aplicado) | Trajectory pass (falha honesta, sem bypass)
- [Authorize] ts=2026-09-15T00:00:00Z allow — usuário autorizou Gari Salvar→Armazenar→Limpar pré-restart → "s"
- [RunID] ts=2026-09-15T00:00:00Z e6f5a7b5-4444-4444-8444-444444444444 gari-save-store-clean done (snapshot+benchmarks, P2 segue blocked)
- [Budget] ts=2026-09-15T00:00:00Z gari-save-store-clean ~6ktok/teto-8k
- [Budget] ts=2026-09-15T00:00:00Z fix-manifesto-stale ~8ktok/teto-10k
- [RunID] ts=2026-09-15T00:00:00Z b3c2d4e2-1111-4111-8111-111111111111 crivo-chat-slots done
- [RunID] ts=2026-09-15T00:00:00Z c4d3e5f3-2222-4222-8222-222222222222 crivo-emb-needle done
- [Phase] ts=2026-09-15T00:00:00Z P1-full done | Gate: ok (8/8 chat vivos + 2/2 emb + 2/2 needle, 2 drifts) | Trajectory pass
- [Budget] ts=2026-09-15T00:00:00Z crivo-chat-slots ~8ktok/teto-10k
- [Budget] ts=2026-09-15T00:00:00Z crivo-emb-needle ~6ktok/teto-8k
- [Derivation] refs: ses_f5ca5c11 + ses_f5ca5c0f → strategy: delegation+synthesis → weights: {disco: 0.4, tabela: 0.3, stack: 0.3}

## Plano (N2 Mini Loop, P1-full)
1. Crivo chat-slots: health/props + crivo-padrao.py --port nos 8 slots chat, sem writes.
2. Crivo emb-needle: bench :9094/:9097 + Needle :8097/:9091, sem writes.
3. Síntese G2: tabela-verdade + O1-O7 refinados.
