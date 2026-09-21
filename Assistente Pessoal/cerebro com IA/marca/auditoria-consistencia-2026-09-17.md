---
tipo: auditoria
setor: marca
data: 2026-09-17
autor: Gran-Mestre (orquestrador) — leitura visual direta dos assets
fonte_empirica: /mnt/win2/imagens/documentos/art da empresa/ + programas de apoio/fotografo/docs/paleta-academy.png
status: auditado — recomendações pendentes de aprovação do dono
---

# Auditoria de Consistência da Marca — Academy of Eletronic (2026-09-17)

> Audição crítica dos assets visuais contra o brand-guide v1.0 (2026-09-16).
> 10 assets canônicos lidos visualmente + inventário 19 arquivos (explorer). Vereditos categóricos R28.

## 1. Ponto forte — o ícone é sólido

A pose **rear-flex duplo-bíceps com ferros de solda cruzados** se repete em TODOS os assets
(logo navy, logo 0 dark, fichas técnicas HUD, cartão, mp4s). É um ícone memorável, único no nicho
e já funciona como assinatura. **Manter blindado — não mexer.**

## 2. ACHADO CRÍTICO — Dualidade cromática não resolvida

Existem **dois sistemas visuais paralelos** disputando a identidade:

| Sistema | Assets | Paleta |
|---|---|---|
| **Azul/Navy HUD** | `logo.png` (1808², hexágono azul #0d8ecf+, navy), `avatar logo.png` (ficha HUD azul-ciano) | navy #022E4E + ciano #0075C9 |
| **Ouro/Oliva canônico** | `logo 0.png` (dark 1090×626, arco ouro-oliva), `avatar logo 0.jpeg` (ficha gold-on-black) | ouro #A3A44A..#9D9D5D, oliva #555628, osso #CAC7B2 |

O guide declara ouro/oliva **canônico** e azul como "apoio/conceitual" — mas na prática os
assets **mais polidos e de maior resolução são azuis** (logo.png 1808², ficha HUD 1254²), e os
ouro são versão sketch/gravura menos acabada. O dono já declarou o destino ("HUD amarelo ouro"
na landing). 

**RECOMENDAÇÃO R-1 (categórica):** canonizar **ouro/oliva** e **re-colorir** os assets azuis
para a paleta canônica (troca de cor dos hexágonos/painéis HUD; procedimento barato via
hue-shift no Photoshop/GIMP ou regeneração img2img com ControlNet). Azul #022E4E permanece
SÓ como "azul_desvio" de alerta/acento (já batizado na paleta). A landing page P3 e o vídeo
P2 herdam ouro/oliva — nunca ciano.

## 3. Três gerações estilísticas convivendo

| Geração | Assets | Veredito |
|---|---|---|
| **Legado 2020** | `art cartão de visita 0.jpg` (fonte pixel-art 8-bit, branco/preto), `apresentação da loja.mp4` (864×480) | FORA do sistema: redesignar o cartão na paleta canônica; vídeo legado = arquivo histórico |
| **Gravura/sketch** | `logo 0.png`, `avatar logo 0/1/2.jpeg` (gosto clássico, tinta) | CANÔNICO de identidade — estilo "manual técnico gravado" = alma da marca |
| **AI-polish HUD** | `avatar logo.png` (ficha técnica HUD) | MANTER como linguagem de UI/HUD (landing, vídeos) **após re-cor para ouro** |

## 4. ACHADO CRÍTICO 2 — texto corrompido por IA nas fichas

`avatar logo.png` e `avatar logo 0.jpeg` carregam **microtipografia corrompida** típica de
geração por IA: "SERUEREiÇÃO TÁTEIS", "SÍUFORTE ARTIFICIAIS", "CONEÇÃO CÉREBRO-MÁQUINA"
(logo.png azul), "HYGRAULE DEALS / MECHAN COPPINTS / MODERN TORSTOS" (avatar 0). Inaceitável
para uso profissional/impressão.

**RECOMENDAÇÃO R-2:** separar arte (boa) de texto (ruim) — recriar as camadas de texto como
**vetor real** (tipografia canônica: display condensada técnica caixa-alta + JetBrains Mono p/
dados HUD, conforme guide §3). Fluxo prático: extrair a arte sem texto via inpainting →
recompor texto em Figma/Inkscape/HTML-overlay. Isso alimenta direto a P3 (landing) e P2 (vídeo).

## 5. Matriz de prontidão por uso

| Uso | Asset base | Estado | Ação |
|---|---|---|---|
| Landing page (P3) | `avatar logo.png` HUD + `logo 0.png` | arte boa / cor errada / texto podre | re-cor ouro + texto vetorial (R-2) |
| Vídeo 20-30s (P2) | `avatar mascote da empresa.mp4` (1920×1088 ✓ já FullHD) | BOM — já 1080p24 | usar como loop-base; corrigir para ouro? (verificar cor dominante do mp4) |
| Posts redes | `avatar mascote correndo.mp4` (1152×640) | sub-HD | upscale com **4x-UltraSharp (instalado 2026-09-17)** → 1080p |
| Cartão novo | redesign do zero | — | paleta canônica + fonte técnica, matar pixel-font |
| Print/adesivo | `logo cortado.psd` (4899×2800 RGBA) | mestra alta-res ✓ | gerar derivados PNG vetoriais/1-color p/ gráfica |

## 6. Arquivo operacional ≠ identidade

`entrada da loja 1.jpeg`, `pc.jpeg`, `agua.jpeg`, `quebrado.jpeg`, `nota fiscal...jpg`, `ccmei.pdf`
são **registro operacional** (loja física/CNPJ), não identidade. 
**RECOMENDAÇÃO R-3:** mover para `art da empresa/_operacional/` (ou vault `marca/anexos/`)
para que o conjunto de marca fique limpo: 10 canônicos + 3 vídeos + mestras PSD.

## 7. Checklist de padronização (proposta de "v1.1 da marca")

1. [ ] R-1: decidir oficialmente **ouro/oliva canônico absoluto**; azul rebaixado a acento (impacto: re-cor de ~3 assets)
2. [ ] R-2: saneamento tipográfico das 4 fichas HUD (texto vetorial)
3. [ ] Redesign cartão (matar pixel-font 2020)
4. [ ] Upscale 4x do mp4 "correndo" → 1152×640→1080p
5. [ ] Reorganizar pasta: `_operacional/` separado
6. [ ] Registrar tokens oficiais: ouro #A3A44A sobre preto #030303, osso #CAC7B2 texto, azul #022E4E SÓ alerta

## Anexo — evidência visual lida (orquestrador, 2026-09-17)

- `logo.png` 1808²: ciborgue gravura, hexágono duplo AZUL vivo, placa preta "THE ACADEMY OF ELETRONIC" metálica — polido mas fora da paleta
- `logo 0.png` 1090×626: mesma pose, arco ouro-oliva "THE ACADEMY OF ELETRONIC", sketch — **este é o DNA canônico**
- `avatar logo.png` 1254²: ficha técnica HUD azul-ciano completa (interface neural, atuadores, paleta de materiais, equipamentos) — layout excelente p/ inspirar P3
- `avatar logo 0.jpeg` 896×1200: ficha "AMALGAMA REAR FLEX" ouro/preto gradeada — estética correta, texto corrompido
- `art cartão de visita 0.jpg` 539×303: pixel-font branca/preto, contatos — legado fora do sistema
- `paleta-academy.png`: tira canônica com 9 hex confirmados
