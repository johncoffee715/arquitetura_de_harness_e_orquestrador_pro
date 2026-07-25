# Vega 20 Overclock Session - Key Learnings

## Date: 2026-07-23

## Critical Finding
SOCCLK on Vega 20 is **firmware-limited to 971 MHz** (82.3% of FCLK), NOT the 97.1% requested. This is due to VBIOS/SMU firmware hardcoded DPM table, not silicon limitations.

## Clock Ranges (Atual)
- **MCLK**: 350-1300 MHz
- **SCLK**: 859-2010 MHz
- **FCLK**: 690-1180 MHz
- **SOCCLK**: 309-971 MHz

## TDP (Power Limit)
- **Atual**: 310W
- **Máximo VBIOS**: 310W
- **Desejado**: 350W (requer VBIOS mod ou power play table override)

### Opções para Aumentar TDP
1. **VBIOS modification** — Risco alto de brick
2. **Power play table override** — Mais seguro, via driver
3. **Aceitar 310W** — Limite seguro atual

## Processo de Testes
- Overclock em escala incremental
- Testando estabilidade a cada aumento
- Valores finais podem ser diferentes dos máximos alcançados
- Instabilidade observada durante os testes

## Temperature Management
### Hotspot Sensor Issue
- **Problem**: Hotspot sensor has **intermittent false positives** - delivers wrong values
- **Solution**: Prioritize **edge temperature** and **VRAM temperature** instead
- **Hotspot limit**: Set to 150°C (not 100°C) due to sensor unreliability

### Monitoring Priority
1. **Edge temp** — Most reliable for Vega 20
2. **VRAM temp** — Critical for HBM2 memory
3. **Hotspot** — Unreliable, use only as rough guide

## DPM Levels Confirmed
- SCLK: 8 levels (852-2000 MHz) + **2140 MHz via OC**
- MCLK: 3 levels (400/800/1000 MHz) + **1340 MHz via OC**
- FCLK: 8 levels (550-1180 MHz)
- SOCCLK: 8 levels (309-971 MHz)

## Solution Created
Dynamic clock scaler that:
- Monitors GPU load via sysfs
- Scales clocks based on demand (idle/low/medium/high/max)
- Auto-throttles at **150°C hotspot** (due to false positive sensor)
- Prioritizes edge and VRAM temperatures
- Runs as systemd service for persistence across reboot

## Files Created
- `~/vega20-scaler.sh` - Dynamic scaling daemon
- `~/vega20-scaler.service` - Systemd service
- `~/vega20-ctrl.sh` - Control script
- `~/.claude/skills/vega20-overclock.md` - Full knowledge base

## Solução Final (COMPLEX Pipeline)

### Arquivos de Documentação
| Arquivo | Conteúdo |
|---------|----------|
| `~/vega20-arquitetura-final.md` | Arquitetura final de power management |
| `~/vega20-abordagens-testadas.md` | Histórico de tentativas e resultados |
| `~/vega20-methodology.md` | Metodologia COMPLEX completa |
| `~/.claude/skills/vega20-overclock.md` | Knowledge base técnica |

### Scripts Finais
| Script | Função |
|--------|--------|
| `~/vega20-force-oc.sh` | Force overclock máximo |
| `~/vega20-scaler.sh` | Escalonamento dinâmico |
| `~/vega20-tdp.sh` | Gerenciador de TDP |
| `~/vega20-boot-diag.sh` | Diagnóstico de bootloader |

### Configuração Ótima (Forçada)
| Domínio | Valor | % do Ideal | Limitação |
|---------|-------|------------|-----------|
| SCLK | 2010 MHz | 100% | DPM level 8 |
| MCLK | 1300 MHz | 100% | DPM level 2 |
| FCLK | 1180 MHz | 100% | DPM level 7 |
| SOCCLK | 971 MHz | 82.2% de FCLK | Firmware SMU |
| TDP | 310W | 100% | VBIOS pptable |

### Decisões Finais
1. **SOCCLK 82.2% de FCLK** (não 90%) — firmware limit
2. **TDP 310W** (não 350W) — VBIOS limit, sem modding
3. **MCLK 1300 MHz** (não 1180 MHz) — DPM level mais próximo
4. **Hotspot 150°C** — sensor com falsos positivos

### Pipeline COMPLEX Executado
- ✅ Prometheus: PLAN.md criado
- ✅ Análise de histórico
- ✅ Documentação de falhas
- ✅ Arquitetura final proposta
