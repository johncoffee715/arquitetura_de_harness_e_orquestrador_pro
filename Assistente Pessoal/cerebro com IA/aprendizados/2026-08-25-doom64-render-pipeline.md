# Aprendizado � Pipeline de render DOOM64 (2026-08-25)

## Sintoma
Tela preta com HUD funcional (crosshair + barras): engine nem inicializava.

## Causa raiz (cadeia de 5 bugs, cada um mascarando o próximo)
1. `index.html` � `./src/main.ts` era 404 (arquivo real era `main-loop.ts`) � sem bootstrap nada rodava.
2. Módulos usam global `BABYLON` (padrão do harness de teste) � no browser ninguém injetava. Fix: `import * as BABYLON` + `globalThis.BABYLON` no entry.
3. `World.buildMeshes()` só criava piso+teto � 108 paredes do grid NUNCA viravam mesh.
4. `Materials.ts` atribuía `BABYLON.Vector3` em `diffuseColor` (que é Color3, lê .r/.g/.b) � tudo preto.
5. `resolveCapsuleWall`: `if (dx < hw)` dentro de branch onde `dx < hw && dz < hd` é garantido � push em Z morto � player atravessava paredes (chegou a z=144 num mapa 96�96).

## Método que funcionou
Playwright via CDP (chromium headless `--remote-debugging-port=9222` + skill_mcp cdp_url) + `gl.readPixels()` para PROVAR render com números RGB, não screenshot. `window.__HELLRAISER` exposto p/ E2E.

## Provas de ferro coletadas
- Render: parede RGB[81,18,7], piso [119,51,17], teto preto (normal p/ baixo, ok DOOM)
- Movimento: 20 u/s exatos (W e D)
- Colisão: clamp z=92.00 exato na face da borda
- Tiro: munição 30�29
- Console: 0 erros

## Lições
- Teste unitário não pegou o bug de colisão: player.test nunca chama update() (gap de cobertura em movimento).
- Assinatura de função mudou (3 args), chamada ficou com 4 � TypeScript deveria pegar; revisar tsconfig strict noEmit.
- readPixels > screenshot para QA de engine: verificável por máquina, sem olho humano.
