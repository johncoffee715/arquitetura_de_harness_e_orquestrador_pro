# DOOM64 clone (HELLRAISER) � sessão completa 2026-08-25

## Entregue
Jogo FPS completo em Babylon.js: 6 armas, 7 inimigos + boss 3 fases, 3 mapas,
FSM de IA, colisão AABB, projéteis anti-tunneling (segmento � cápsula vertical),
partículas, minimapa, HUD, save/load F5/F9, vitória/derrota.
139 testes unitários (23 arquivos) + 7 E2E Playwright. ~20 commits atômicos.

## Bugs de ferro da sessão (padrões recorrentes)
1. Módulo-level `new BABYLON.X` quebra com global injetado no entry (fase de imports
   ES roda ANTES do corpo do main.ts). Regra: constantes de módulo NUNCA instanciam
   classes do engine � usar specs (tuples) + factory lazy.
2. "Testes E2E falhando" eram o gate isPlaying() funcionando: player morto por
   zombies em ~6s � GAMEOVER � loop para. Sempre setState('PLAYING') antes de
   testar mecânica; e o fracasso do teste PROVOU o loop spawn�chase�attack�death.
3. Arg-order em construtor de subclasse (super(template, scene) vs (scene, template))
   � eliminado removendo construtores boilerplate (herança direta).
4. Hit-test de projétil: ponto-esfera dá tunneling; segmento-esfera resolve dt grande;
   cápsula vertical resolve tiro horizontal na altura do peito.

## Método de verificação (reutilizável)
Playwright via CDP (chromium --remote-debugging-port=9222) + gl.readPixels para
provar render por números RGB + window.__HELLRAISER exposto p/ inspeção.
readPixels > screenshot: verificável por máquina.

## Pendências conhecidas (não-bloqueantes)
- Pitch do mouse look: mecanismo unit-testado; verificação ao vivo requer gesto real
  de pointer lock (headless não concede).
- Spawn do MAP1 brutal: zombie a 5.7 unidades do player (morte em ~6s parado).
- Armas 2-6 implementadas mas não ciclam no gameplay (sem troca de arma ainda).
