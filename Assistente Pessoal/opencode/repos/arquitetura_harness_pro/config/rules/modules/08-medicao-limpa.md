---
numero: R55
tema: Medicao limpa entre testes de LLM (zero absoluto)
categoria: harness
setor: telemetria
escopo: global
vigencia: 2026-08-19
---

# R55 — Medição Limpa Entre Execuções de Modelo (Zero Absoluto)

- ENTRE a execução de CADA modelo em baterias de benchmark/telemetria:
  1. Derrubar COMPLETAMENTE o processo do backend (Ollama ou llama.cpp) —
     `pkill -x llama-server` / `ollama stop` — e aguardar a porta liberar.
  2. Limpar caches do kernel via root:
     `sync && echo 3 > /proc/sys/vm/drop_caches`
     (requer root; sem root → documentar e medir RSS via /proc/<pid>/status,
     que já zera com o backend derrubado).
  3. Só então subir o próximo modelo e medir RAM/VRAM — leitura parte do zero
     absoluto, sem page cache/backing file mascaram consumo real.
- Resultados de telemetria SEMPRE compilados em MATRIZ preenchida por modelo:
  | modelo | quant | ctx | GPU/CPU | RAM(GB) | VRAM(GB) | t/s | temperatura | MTP | notas |
- A matriz é o artefato de saída obrigatório de qualquer bateria (SPEC §X).
