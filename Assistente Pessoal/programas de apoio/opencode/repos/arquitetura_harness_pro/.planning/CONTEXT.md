# CONTEXT — estado para a próxima sessão (2026-08-24)

## ECOSISTEMA ATIVO (verificado)
9 slots LLM + Needle L0 dispatcher · sampling/KV/janela por responsabilidade · doutrina cold/warm ativa.
GPU :8083 Ornith-1.5-9B @262144 NATIVO no-think (lei #7 · repeat-penalty 1.1) — GM-oficial 76.3 rank#1.
CPU HOT :9084 qwen0.8b 123 · :9085 judge 139 t0.15 · :9086 lfm230m 228 · :9087 qwen2b 155 t0.3 · :9088 qwen1.7B 183 · :9089 ternary17 207.
WARM sob demanda :9083 bonsai27B F1-prosa densa 15.72 · bonsai8B F1-volume 125 warm · IQ1_S reserva-BD · XXS planner-e-commerce.

## DECISÃO VIGENTE D-2026-08-23-b
ENSEMBLE complementar PROVADO (nenhum ≥80 sozinho · rank invariado mini↔full).
Ornith orquestra · Qwen27B planeja≥96K · Qwen9B executa c/ verificador §9 · Bonsai/IQ1_S curtos · Needle F4-mecânico.

## LEIS CODIFICADAS
R57 lei#7 endless-think⇒no-think · R58 cold/warm · R59 t/s-per-KV-GB (ternary17 544.8 🏆 · ornith 5.8 por design) ·
R60 ornith nativo 262144 · R61 sampling unsloth por responsabilidade · R62 geometria≠custo · R63 watchdog-decode >5×⇒restart.
Vacina: MALLOC_ARENA_MAX=4+TRIM no start script.

## MECANISMOS ATIVOS
watcher registry (.wregd.sh pid vivo) · KRON 15 dias (timer systemd-user + gate hook session.start) ·
modo compacto ATIVO (agents-mode.sh monolito reverte) · needle-dispatch v4 c/ vector_cache_surrogate semântico ·
pipeline pytest→hook logreport→JSONL→cartão→dispatch FECHADO.

## ARTEFATOS-CANÔNICOS
.planning/: GRAFO-fases-canonical · MAPA-funcoes-melhor-modelo · SERVING-PROFILES · BD-full-espec · AUDITORIA-janela-ram · GAPS-regras(R57-R63 ✓formalizadas · README ✓reescrito)
benchmark/reports/final/GMB1-relatorio-completo.md (35.981c · adendas 1-19 + apêndices A/B/C + FECHAMENTO)

## PENDENTES (nenhum executável bloqueante)
BD-full-espec execução integral (~90min GPU exclusiva) sob aprovação · reteste Qwen38-4B em RAM livre ·
bitnet.cpp kernels nativos (clang≥18) · smaps-bancada por slot CPU · formalizar módulos 07+ se crescer
