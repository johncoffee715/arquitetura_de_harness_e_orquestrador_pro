# Decisões de Arquitetura — Vega 20

## Decisão 1: Não modificar VBIOS
**Data**: 2026-07-24
**Contexto**: Usuário queria TDP 350W, mas VBIOS limita a 310W
**Alternativas**:
1. Modificar VBIOS (risco alto de brick)
2. Power play table override (médio risco)
3. Aceitar 310W (baixo risco)
**Decisão**: Aceitar 310W como limite seguro
**Rationale**: Risco de brick não justifica ganho de 40W

## Decisão 2: Priorizar edge temp sobre hotspot
**Data**: 2026-07-24
**Contexto**: Hotspot sensor tem falsos positivos intermitentes
**Alternativas**:
1. Confiar no hotspot (risco de throttling desnecessário)
2. Priorizar edge temp (mais confiável)
3. Usar ambos com fallback
**Decisão**: Priorizar edge temp
**Rationale**: Hotspot sensor é unreliable, edge temp é mais estável

## Decisão 3: Usar DPM levels reais
**Data**: 2026-07-24
**Contexto**: Usuário queria MCLK 1180 MHz, mas não é DPM level
**Alternativas**:
1. Forçar 1180 MHz via OC (instável)
2. Usar 1300 MHz (DPM level 2)
3. Usar 800 MHz (DPM level 1)
**Decisão**: Usar 1300 MHz (DPM level 2)
**Rationale**: DPM levels são estáveis, OC é instável

## Decisão 4: Criar sistema cognitivo no Obsidian
**Data**: 2026-07-24
**Contexto**: Gran-Mestre precisa de memória persistente
**Alternativas**:
1. Usar apenas arquivos .md (limitado)
2. Usar Obsidian como vault cognitivo (completo)
3. Usar banco de dados (complexo)
**Decisão**: Usar Obsidian como vault cognitivo
**Rationale**: Obsidian suporta links, tags, busca, é Markdown-based

## Tags
#decisao #arquitetura #vega20 #gran-mestre #cognicao
