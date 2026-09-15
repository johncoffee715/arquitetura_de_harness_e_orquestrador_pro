---
name: ruview
description: "π RuView turns commodity WiFi signals into real-time spatial intelligence, vital sign monitoring, presence detection — without video. (absorvido de ruvnet/RuView)"
---
# Ruview

Helenizado de [`ruvnet/RuView`](https://github.com/ruvnet/RuView).

## Propósito
π RuView turns commodity WiFi signals into real-time spatial intelligence, vital sign monitoring, and presence detection — all without a single pixel of video.

## Padrões absorvidos (núcleo canônico do repo)
- Presence and occupancy** — detect people through walls, count them, track entries and exits
- Vital signs** — breathing rate and heart rate, contactless, while sleeping or sitting
- Activity recognition** — walking, sitting, gestures, falls — from temporal CSI patterns
- Environment mapping** — RF fingerprinting identifies rooms, detects moved furniture, spots new objects
- Sleep quality** — overnight monitoring with sleep stage classification and apnea screening
- Camera-free pose** — estimate 17 body keypoints from WiFi CSI
- Built-in model workflow** — record CSI, train models, load RVF files, and switch LoRA profiles
- Local automation** — HOMECORE provides state, history, automations, signed Wasm plugins, voice hooks, and HomeKit support

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="ruview")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/ruvnet/RuView
