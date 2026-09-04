---
tags: [aprendizado, mi50, overclock, upp, sysfs, gpu, vega20, tty]
date: 2026-07-28
area: hardware/performance/gpu
---

# Aprendizado: Overclock MI50 via PP Table com UPP

## Contexto

Fazer overclock de uma AMD Radeon Instinct MI50 (Vega20, gfx906) sem modificar
VBIOS, usando apenas patching runtime da PowerPlay table via sysfs.

## O que Funcionou

### UPP (Uplift PowerPlay)
- Ferramenta correta para o trabalho
- `upp -p pp_table.bin set --write --from-conf conf.file` é o método mais seguro
- Única escrita atômica vs múltiplas chamadas UPP individuais
- Dump com nomes simbólicos validados contra a PP table real (não offsets hex)

### Auto-detect de Card
- `/sys/class/drm/card*/device` itera sobre todos os cards
- `vendor=0x1002` identifica AMD
- `pp_table` no mesmo diretório confirma GPU com PowerPlay
- Evita hardcode de card0/card1

### Persistência via Systemd
- `Before=lightdm.service` garante aplicação antes do display manager
- `ExecStartPre` com `while [ ! -f pp_table ]` espera driver carregar
- Oneshot + RemainAfterExit para verificação posterior

## O que Não Funcionou

### pkexec para escrever em sysfs
- Sem política polkit para `tee`, pkexec retorna exit 127
- sysfs é root-only, sem exceção para video group

### card0 hardcoded
- Script original quebra se a GPU estiver em card1
- Systemd service também quebrava

### Hex Edit Manual
- Offsets mudam entre VBIOS
- Sem validação semântica dos valores

## Padrões Identificados

1. **sysfs root-only constraint** — Qualquer automação de overclock via pp_table
   precisa de sudo ou systemd rodando como root
2. **TTY safety** — Toda modificação de GPU que controla display deve ser feita
   em TTY para evitar crash de vídeo irrecuperável
3. **Atomic writes > incremental** — Modificar 29 parâmetros de uma vez via
   `--from-conf` é mais seguro que múltiplas escritas
4. **Vega20 hotspot false positive** — Sensor junction (7nm) pode marcar 50°C
   acima do real em watercooling. Não confiar cegamente no hotspot.
5. **Config file as source of truth** — Manter o `.conf` junto com a `.bin`
   permite recriar a PP table modificada a qualquer momento

## Próximas Investigações

- Teste de carga real: clpeak, vkpeak, llama.cpp com 350W sustentado
- Verificar ECC uncorrected após 2h+ de carga
- PMBus IR35217 — descobrir acesso ao VRM de memória

## 2026-07-29 — Perfil MIX + SOCCLK 1000MHz

**Problema:** SOCCLK 1080MHz crashava durante loading do kernel.
**Solução** Reduzir SOCCLK para 1000MHz (estável).
**Perfil:** "MIX" — 350W / SCLK 2000 / MCLK 1200 / FCLK 1200 / SOCCLK 1000
**Config salvo:** `pp_table_patches/upp_targets_350w_mix_socclk1000.conf`
**Commit:** `aea8f17 Add MIX profile: SOCCLK 1000MHz`

## 2026-07-29 — Gran-Mestre Pipeline MIX + DevLoop SOCCLK 1000MHz

### Pipeline Executado (6 Fases)
1. FASE 1: DESCOBERTA — Prometheus investigou crash do SOCCLK 1080MHz
2. FASE 2: CONTRATO — Spec Writer definiu aceitação SOCCLK=1000
3. FASE 3: PLANO — Plan Writer mapeou tasks e dev loop
4. FASE 4: EXECUÇÃO — Atlas aplicou config, Implementer commitou, Code Reviewer validou
5. FASE 5: REVISÃO MACRO — Atena verificou coerência cross-task
6. FASE 6: ENTREGA — Verification + Héstia + Fable Judge: ALL PASS

### Dev Loop Tracking
| Iteração | SOCCLK | Resultado |
|----------|--------|-----------|
| 1 | 1165 (stock) | OK |
| 2 | 1080MHz | CRASH kernel loading |
| 3 | 1000MHz | ESTÁVEL ✅ |

### Arquivos Pipeline
- SPEC: pp_table_patches/SPEC-socclk-1000mhz.md
- PLAN: pp_table_patches/PLAN-socclk-1000mhz.md
- Config: upp_targets_350w.conf (SOCCLK=1000, 8/8 slots)
- Config MIX: upp_targets_350w_mix_socclk1000.conf

### Erro de Contexto Anterior
- "modo MIX" foi corretamente interpretado como modo de execução do Gran-Mestre (COMPLEX)
- Não como "nome de perfil" da PP table
- O Pipeline MIX orquestra todos agents em paralelo na execução
- Dev Loop permite iteração rápida entre valores de SOCCLK até encontrar estável
