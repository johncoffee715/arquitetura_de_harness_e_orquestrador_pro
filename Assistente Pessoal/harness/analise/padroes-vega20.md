# Padrões Identificados — Vega 20

## Padrão 1: Limites de Firmware
**Descrição**: Limites de TDP e SOCCLK são hardcoded no firmware
**Frequência**: Sempre presente
**Impacto**: Alto — impede overclock além dos limites
**Solução**: Aceitar limites ou modificar VBIOS (risco alto)

## Padrão 2: DPM Levels Fixos
**Descrição**: Frequências são discretas, não contínuas
**Frequência**: Sempre presente
**Impacto**: Médio — limita opções de clock
**Solução**: Usar DPM levels disponíveis

## Padrão 3: Sensor de Hotspot Unreliable
**Descrição**: Hotspot sensor tem falsos positivos intermitentes
**Frequência**: Ocorre em cargas específicas
**Impacto**: Alto — pode causar throttling desnecessário
**Solução**: Priorizar edge temp

## Padrão 4: Proporções de Clock
**Descrição**: Relações entre domínios afetam estabilidade
**Frequência**: Sempre aplicável
**Impacto**: Alto — instabilidade se desbalanceado
**Solução**: Manter proporções ideais

## Padrão 5: Escalonamento Dinâmico
**Descrição**: Carga GPU varia, clocks devem acompanhar
**Frequência**: Sempre presente
**Impacto**: Médio — performance vs eficiência
**Solução**: Implementar scaler dinâmico

## Tags
#padrao #vega20 #firmware #dpm #sensor #proporcao #escalabilidade
