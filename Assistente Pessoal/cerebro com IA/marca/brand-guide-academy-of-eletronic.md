---
setor: marca
tipo: brand-guide
marca: The Academy of Eletronic
data: 2026-09-16
status: v1.0 — auditoria concluída (F1)
fonte_empirica: histogramas ImageMagick sobre assets reais (fotografo/docs/histogramas.txt)
---

# Brand Guide — The Academy of Eletronic

## 1. Veredito canônico (medido, não opinado)

A marca possui **duas trilhas visuais conflitantes** nos assets. A trilha **ouro-oliva + preto** é a canônica:

- Documental de impressão (`logo cortado.psd` 4899×2800, `logo 0.png` 1090×626 — frente do cartão)
- Sistema do mascote (`avatar logo 0/1/2.jpeg` — fichas AMALGAMA e ASSISTENTE BIOMECATRÔNICO)

A trilha **azul-navy/ciano** (`logo.png` 1808², `avatar logo.png` 1254², ficha HUD azul) NÃO é lixo:
classificada como **ARTE CONCEITUAL e MATERIAL DE APOIO** (decisão do usuário 2026-09-16). Uso legítimo:
moodboards, B-roll, explorar variações de "modo noturno/stealth" do mascote, contraste dramático quando o
design pedir. Regra permanece: identidade primária = ouro; azul nunca ancora sozinho uma peça oficial.

Decisão de registro: `logo cortado.psd` = fonte-mestra; a variante dark (p/ web/landing) deriva de `logo 0.png`.

## 2. Paleta canônica (valores medidos — histograma 16 cores, 300px)

| Token | Hex | Papel |
|---|---|---|
| `--ae-void` | `#030303` | fundo absoluto (cartão dark) |
| `--ae-ink` | `#0A0C0C` | fundo base das fichas/HUD |
| `--ae-olive-shadow` | `#2C2B15` | sombra oliva (respiros escuros) |
| `--ae-olive` | `#555628` | oliva estrutural |
| `--ae-olive-mid` | `#6C6D51` | oliva médio (bordas suaves) |
| `--ae-gold-aged` | `#9D9D5D` | ouro envelhecido (texto secundário HUD) |
| `--ae-gold` | `#A3A44A` | **OURO CANÔNICO — HUD, acento, CTA** |
| `--ae-bone` | `#CAC7B2` | osso (corpo mármore do mascote, cinzas úteis) |
| `--ae-gold-pale` | `#F4F4D2` | ouro pálido (print claro, highlights) |
| `--ae-white` | `#FFFFFF` | branco do PSD impresso |

### Paleta de apoio (arte conceitual — nunca primária)

| Token | Hex | Papel |
|---|---|---|
| `--ae-navy` | `#022E4E` | navy profundo (apoio) |
| `--ae-cyan` | `#0075C9` | ciano HUD (apoio, uso pontual) |

Prova visual: `programas de apoio/fotografo/docs/paleta-academy.png` (10 swatches organizados).

## 3. Tipografia (recomendação — assets não trazem fonte identificável)

- **Display/títulos**: condensada técnica (sugestão: *Rajdhani*, *Orbitron* ou *Eurostile-like*), caixa alta, tracking positivo
- **HUD/dados**: monoespaçada (*JetBrains Mono*) — espelha os blocos de especificação das fichas
- **Texto corrido**: neutra legível (Inter/System), nunca maior que 16px sobre fundo escuro sem contraste ouro

## 4. Inventário auditado (/mnt/win2/imagens/documentos/art da empresa/)

| Asset | Dimensão | Veredito |
|---|---|---|
| logo cortado.psd | 4899×2800 | **MESTRA** (ouro/branco, impressão) |
| art frente cartão.psd | 1098×626 | print oficial — manter como referência de layout |
| logo 0.png | 1090×626 | canônico dark ✔ |
| avatar logo 0/1.jpeg | 896×1200 | canônico ouro/preto ✔ |
| avatar logo 2.jpeg | 1536×1024 | canônico ouro/preto ✔ (ficha HUD completa) |
| avatar logo.png | 1254×1254 | arte conceitual (azul) — apoio |
| logo.png | 1808×1807 | arte conceitual (navy) — apoio |
| avatar mascote da empresa.mp4 | 1920×1088 @24fps, 5,2s | canônico (soldagem/bancada) |
| avatar mascote da empresa correndo.mp4 | 1152×640 @48fps, 10,1s | canônico (cena corrida) |
| apresentação da loja.mp4 | 864×480 @30fps, 16,3s | legado 2020 — só histórico |

## 5. Regras de uso (F5/F6 obedecem)

1. HUD sempre `#A3A44A` sobre `#0A0C0C`/`#030303`; azul/ciano só como apoio pontual, nunca acento primário.
2. O mascote é o rosto da marca: toda peça nova (vídeo/landing) ancora nele.
3. Equação oficial: `HUMANO + BIOMECATRÔNICA + INTELIGÊNCIA ARTIFICIAL = EVOLUÇÃO`; trindade `DISCIPLINA TECNOLOGIA SUPERIORIDADE`.
4. Grade/hexágono de fundo (padrão das fichas) é textura oficial recorrente.
5. Claims técnicos (serviços) usam jargão real: board-level, BGA, reballing, microsolda, ESD.
