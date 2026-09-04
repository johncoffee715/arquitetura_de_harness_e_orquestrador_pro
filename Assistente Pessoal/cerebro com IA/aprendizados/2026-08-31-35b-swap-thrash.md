# Lição — 35B CPU + stack simultânea > RAM → swap thrash (2026-08-31)

## Contexto
O orquestrador (Ornith-1.5-35B-A3B-IQ4_XS, :8083, CPU) ficou "travado/lento" ao rodar
no path `/mnt/dados/Assistente Pessoal`. Diagnóstico completo realizado em sessão.

## Causa raiz (evidências)
- 35B @ ctx 262144 exige ~26GB RAM: 18GB pesos (IQ4_XS) + ~8.6GB KV (q4_0/q4_0, ~32KB/tok).
- RAM física total: 31GB. Com 8 slots LLM up → 21GB em swap (zram, swappiness 150).
- RSS do processo 35B: 213MB — pesos NÃO residentes; cada token = page-fault → decode
  cai de ~2.2 t/s para ~0.1-0.5 t/s → timeouts → retries → mais carga (thrash).
- vmstat: si 4MB/s / so 69MB/s pico; sdb w_await 812ms.
- **Efeito colateral crítico**: subagentes com backends em swap (Qwen-4B :9088 5.7GB,
  Ternary :9090 3.9GB em swap) retornaram diffs ALUCINADOS (diziam ter editado, arquivos
  intactos) — transporte de subagentes degradado por pressão de memória, não por bug de código.

## Correções identificadas
1. ctx 262144 → 32768 (libera ~7.5GB; KV 8.6GB → ~1.1GB). GM opera com estado compacto (R70);
   delegação que exigir mais janela → omniroute (R23).
2. Modo WARM (R21/R58): só ESSENTIAL (8083+9084) up por padrão; WARM sob demanda
   (`start-stack.sh <porta|nome>`). Delay: ~10-20s slots pequenos, ~1-1.5min 35B (restart).
3. swappiness 150 → 10 (preserva page cache; zram continua p/ OS).
4. RAM 64GB (Pacote B) = única forma de manter 262K sem thrash.

## Lições
1. **Janela de contexto em CPU = custo de RAM real**: 262K num 35B CPU exige ~26GB —
   calcular RAM (não só VRAM) antes de fixar ctx (extensão de R60/R62 p/ CPU).
2. **Swap thrash é a causa nº1 de "LLM lento" em máquina com pouca RAM** — checar
   `free -g` + `VmSwap` dos PIDs antes de culpar o modelo.
3. **Subagente com backend em swap alucina edições** — verificar diff real após retorno
   (zero-trust R28/R53); sintoma de infra, não de código.
4. **WARM sob demanda** é o padrão correto p/ stack híbrida com RAM limitada (R21/R58).

## Referências
- Instruções completas: `decisoes/2026-08-31-stack-warm-instrucoes.md`
- Backup scripts: `/tmp/opencode/stack-warm-backup-1788204293/`
- Disco modelos: /mnt/dados = sdb SSD SATA (~345MB/s medido)