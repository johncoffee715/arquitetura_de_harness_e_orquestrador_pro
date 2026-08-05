# Insights — Vega 20 Power Management

## Insight 1: Firmware é o Limitador Principal
**Descoberta**: TDP e SOCCLK são limitados pelo firmware, não pelo silício
**Implicação**: Overclock além dos limites requer modificação de firmware
**Ação**: Aceitar limites ou modificar VBIOS (risco alto)

## Insight 2: DPM Levels São Discretos
**Descoberta**: Frequências são fixas em níveis discretos
**Implicação**: Não é possível usar frequências arbitrárias
**Ação**: Usar DPM levels disponíveis

## Insight 3: Hotspot Sensor É Unreliable
**Descoberta**: Sensor de hotspot tem falsos positivos
**Implicação**: Throttling baseado em hotspot pode ser desnecessário
**Ação**: Priorizar edge temp para decisões de throttling

## Insight 4: Proporções São Críticas
**Descoberta**: Relações entre domínios afetam estabilidade
**Implicação**: Desbalanceamento causa instabilidade
**Ação**: Manter proporções ideais (SCLK ≈ 1.5-1.6× MCLK)

## Insight 5: Escalonamento Dinâmico É Necessário
**Descoberta**: Carga GPU varia significativamente
**Implicação**: Clocks fixos são ineficientes
**Ação**: Implementar scaler dinâmico baseado em carga

## Tags
#insight #vega20 #firmware #dpm #sensor #proporcao #escalabilidade
