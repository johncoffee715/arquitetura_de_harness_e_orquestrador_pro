# Vega 20 Overclock — Sessão 2026-07-24

## Status
✅ Concluída

## Objetivo
Desenvolver metodologia COMPLEX para gerenciamento de power/clocks do Vega 20 (MI50)

## Resultados

### Clocks Alcançados
| Domínio | Máximo Alcançado | Máximo Estável | Limitação |
|---------|------------------|----------------|-----------|
| SCLK | 2140 MHz | 2010 MHz | DPM level 8 |
| MCLK | 1340 MHz | 1300 MHz | DPM level 2 |
| FCLK | 1180 MHz | 1180 MHz | DPM level 7 |
| SOCCLK | 971 MHz | 971 MHz | Firmware SMU |
| TDP | 310W | 310W | VBIOS pptable |

### DPM Levels Confirmados
- SCLK: 859, 860, 1153, 1316, 1425, 1514, 1583, 1654, 2010 MHz
- MCLK: 350, 800, 1300 MHz
- FCLK: 550, 610, 690, 760, 870, 960, 1080, 1180 MHz
- SOCCLK: 309, 523, 566, 618, 680, 755, 850, 971 MHz

### Proporções Ideais
```
SCLK ≈ 1.5× a 1.6× o MCLK
FCLK ≈ 1.0× o MCLK
SOCCLK ≈ 1.0× a 1.1× o MCLK (limitado a 971 MHz)
```

### Scripts Criados
- `~/vega20-force-oc.sh` — Force overclock máximo
- `~/vega20-scaler.sh` — Escalonamento dinâmico
- `~/vega20-tdp.sh` — Gerenciador de TDP
- `~/vega20-boot-diag.sh` — Diagnóstico de bootloader

### Knowledge Base
- `~/.claude/skills/vega20-overclock.md` — Documentação completa
- `~/.claude/memory/vega20-overclock.md` — Memória persistente
- `~/vega20-methodology.md` — Metodologia COMPLEX
- `~/vega20-abordagens-testadas.md` — Histórico de tentativas
- `~/vega20-arquitetura-final.md` — Arquitetura final

## Aprendizados
1. SOCCLK é limitado a 971 MHz (82.2% de FCLK) pelo firmware SMU
2. TDP é limitado a 310W pelo VBIOS
3. MCLK 1180 MHz não é um DPM level (só 800 ou 1300)
4. Hotspot sensor tem falsos positivos — priorizar edge temp
5. ppfeaturemask não persiste sem configurar bootloader

## Próximos Passos
1. Configurar ppfeaturemask no bootloader correto
2. Testar TDP 350W após ppfeaturemask habilitado
3. Otimizar clocks dentro dos limites VBIOS
4. Implementar escalonamento dinâmico com perfis corretos

## Tags
#vega20 #overclock #power-management #gran-mestre #cognicao
