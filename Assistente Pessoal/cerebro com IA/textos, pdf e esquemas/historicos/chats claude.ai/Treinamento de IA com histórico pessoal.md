**Claude**

**Encontrei o erro exato:**

```
error: invalid argument: --log-format
```

O flag `--log-format` **não existe** nessa versão do llama.cpp. No teste manual que funcionou, eu não usei ele — mas o daemon e o provider adicionaram `--log-format json`, que o llama-server rejeita e sai na hora. Por isso o llama.cpp nunca subia na:8080.

Repara que `--device Vulkan0` passou sem erro (o erro foi só no `--log-format`), então esse flag é válido. É só remover o `--log-format`.

Também vi que `OLLAMA_MODELS` aponta pro NTFS (que só tem blobs pequenos de metadata), enquanto o modelo real de 7GB está em `~/.local/share/ai-lab`. Vou corrigir os dois problemas — remover o flag inválido e tornar a resolução de modelo robusta (acha o maior blob onde quer que esteja):

---

**You**

ainda em cpu ~ ❯ python3 "/mnt/win2/Assistente Pessoal2/runtime/daemon.py" start \[16:36:23\]\[daemon\] === AI-Lab daemon iniciando === \[16:36:23\]\[gfx906\] VRAM baseline medida: 1.92GB \[16:36:23\]\[daemon\] Iniciando qdrant... \[16:36:25\]\[daemon\] qdrant pronto::6333 (PID 94254) \[16:36:25\]\[daemon\] Iniciando llamacpp... \[16:36:35\]\[daemon\] llamacpp aguardando... 10s \[16:36:45\]\[daemon\] llamacpp aguardando... 20s \[16:36:55\]\[daemon\] llamacpp aguardando... 30s \[16:37:05\]\[daemon\] llamacpp aguardando... 40s \[16:37:15\]\[daemon\] llamacpp aguardando... 50s \[16:37:25\]\[daemon\] llamacpp aguardando... 60s \[16:37:35\]\[daemon\] llamacpp aguardando... 70s \[16:37:45\]\[daemon\] llamacpp aguardando... 80s \[16:37:55\]\[daemon\] llamacpp aguardando... 90s \[16:37:55\]\[daemon\] llamacpp não respondeu em 90s \[16:37:55\]\[daemon\] Falha ao iniciar llamacpp — stack pode estar degradado \[16:37:55\]\[daemon\] ollama::11434 já rodando \[16:37:56\]\[daemon\] Iniciando webui... \[16:38:06\]\[daemon\] webui aguardando... 10s \[16:38:16\]\[daemon\] webui aguardando... 20s \[16:38:18\]\[daemon\] webui pronto::3000 (PID 94759) \[16:38:18\]\[daemon\] Iniciando pipelines... \[16:38:24\]\[daemon\] pipelines pronto::9099 (PID 94976) \[16:38:29\]\[gfx906\] CPU FALLBACK — delta=0.06GB < 7.20GB esperado. Fix: HSA\_OVERRIDE\_GFX\_VERSION=9.0.6 no systemd do Ollama, ou -ngl 9 no llama.cpp \[16:38:29\]\[daemon\] GPU FALLBACK — inferência será lenta (CPU) \[16:38:29\]\[daemon\] Execute: ai-lab gpu check \[16:38:29\]\[daemon\] === Stack inicializado === \[16:38:29\]\[daemon\] Watchdog iniciado \[16:48:44\]\[daemon\] Sinal 15 recebido \[16:48:45\]\[daemon\] Encerrando daemon... ~ 12m 21s ❯ # Atualiza daemon e provider cp ~/Downloads/daemon\_vulkan.py /mnt/win2/Assistente\\ Pessoal2/runtime/daemon.py cp ~/Downloads/llamacpp\_vulkan.sh /mnt/win2/Assistente\\ Pessoal2/providers/llamacpp.sh # Mata processos antigos e sobe o stack completo pkill -f "runtime/daemon.py"; pkill -f "llama-server"; sleep 2 python3 "/mnt/win2/Assistente Pessoal2/runtime/daemon.py" start \[16:59:58\]\[daemon\] === AI-Lab daemon iniciando === \[16:59:58\]\[gfx906\] VRAM baseline medida: 2.02GB \[16:59:58\]\[daemon\] Iniciando qdrant... \[17:00:00\]\[daemon\] qdrant pronto::6333 (PID 106015) \[17:00:00\]\[daemon\] Iniciando llamacpp... \[17:00:02\]\[daemon\] llamacpp pronto::8080 (PID 106162) \[17:00:02\]\[daemon\] ollama::11434 já rodando \[17:00:02\]\[daemon\] Iniciando webui... \[17:00:12\]\[daemon\] webui aguardando... 10s \[17:00:14\]\[daemon\] webui pronto::3000 (PID 106204) \[17:00:14\]\[daemon\] Iniciando pipelines... \[17:00:16\]\[daemon\] pipelines pronto::9099 (PID 106361) \[17:00:21\]\[gfx906\] CPU FALLBACK — delta=0.00GB < 7.20GB esperado. Fix: HSA\_OVERRIDE\_GFX\_VERSION=9.0.6 no systemd do Ollama, ou -ngl 9 no llama.cpp \[17:00:21\]\[daemon\] GPU FALLBACK — inferência será lenta (CPU) \[17:00:21\]\[daemon\] Execute: ai-lab gpu check \[17:00:21\]\[daemon\] === Stack inicializado === \[17:00:21\]\[daemon\] Watchdog iniciado

---

**Claude**

**Progresso real:** o `--log-format` era o que matava — agora o llama.cpp **sobe em 2 segundos** (`llamacpp pronto ::8080`) em vez do timeout de 90s. Mas surgiu outra coisa: delta de VRAM **0.00GB**. E "pronto em 2s" é a pista — um modelo de 7GB não carrega em 2 segundos. Então o llama-server subiu, mas ou carregou um modelo **minúsculo/errado**, ou não fez offload pra GPU.

Suspeito de duas coisas: o daemon resolveu um modelo pequeno do NTFS (os blobs lá são de 488 bytes), OU o flag `--device Vulkan0` quebra o offload. Vou desambiguar com um teste decisivo — modelo de 7GB confirmado + os args exatos do daemon, mostrando o log completo:

```bash
pkill -f "runtime/daemon.py"; pkill -f "llama-server"; sleep 2

set MODEL (find ~/.local/share/ai-lab/ollama_models/blobs -type f -size +3G 2>/dev/null | head -1)
echo "Modelo (7GB confirmado): $MODEL"

env LD_LIBRARY_PATH=$HOME/.local/share/ailab2/bin/llamacpp $HOME/.local/share/ailab2/bin/llamacpp/llama-server --model "$MODEL" --port 8081 -ngl 99 --ctx-size 8192 --parallel 4 --cont-batching --device Vulkan0 > /tmp/vk.log 2>&1 &

sleep 25
echo "=== VRAM agora: "(cat /sys/class/drm/card1/device/mem_info_vram_used | python3 -c "import sys; print(f'{int(sys.stdin.read())/1073741824:.2f}GB')")" ==="
echo "=== LOG do llama-server ==="
grep -iE "load_tensor|offload|layer|vulkan|device|buffer size|error|warn" /tmp/vk.log | head -25

pkill -f "llama-server"
```

Esse teste usa o modelo de 7GB **explícito** (não a resolução do daemon) + os flags do daemon. O log vai mostrar quantas layers foram pra GPU e qual device foi escolhido.

Dois resultados possíveis:

**VRAM sobe pra ~9GB + log diz `offloaded 33/33 layers to GPU`** → os args do daemon estão certos, o problema é a **resolução de modelo**: o daemon está carregando um modelo pequeno/errado do NTFS em vez do 7GB. Fix: corrigir pra onde o daemon procura o modelo.

**VRAM fica em ~2GB + log diz `offloaded 0/N` ou erro no `--device`** → o flag `--device Vulkan0` é o culpado (no teste que funcionou eu não usei ele). Fix: remover `--device` do daemon e deixar auto-selecionar.

Cola o output (VRAM + log). Esse é o teste que fecha o diagnóstico — com ele eu sei exatamente qual dos dois é e aplico o fix certo.

---

**You**

~ 5m 31s ❯ pkill -f "runtime/daemon.py"; pkill -f "llama-server"; sleep 2 set MODEL (find ~/.local/share/ai-lab/ollama\_models/blobs -type f -size +3G 2>/dev/null | head -1) echo "Modelo (7GB confirmado): $MODEL" env LD\_LIBRARY\_PATH=$HOME/.local/share/ailab2/bin/llamacpp $HOME/.local/share/ailab2/bin/llamacpp/llama-server --model "$MODEL" --port 8081 -ngl 99 --ctx-size 8192 --parallel 4 --cont-batching --device Vulkan0 > /tmp/vk.log 2>&1 & sleep 25 echo "=== VRAM agora: "(cat /sys/class/drm/card1/device/mem\_info\_vram\_used | python3 -c "import sys; print(f'{int(sys.stdin.read())/1073741824:.2f}GB')")" ===" echo "=== LOG do llama-server ===" grep -iE "load\_tensor|offload|layer|vulkan|device|buffer size|error|warn" /tmp/vk.log | head -25 pkill -f "llama-server" Modelo (7GB confirmado): /home/johncoffee/.local/share/ai-lab/ollama\_models/blobs/sha256-b559938ab7a0392fc9ea9675b82280f2a15669ec3e0e0fc491c9cb0a7681cf94 === VRAM agora: 9.56GB === === LOG do llama-server === 0.00.116.479 I device\_info: 0.00.116.668 I - Vulkan0: AMD Radeon Pro VII (RADV VEGA20) (16368 MiB, 14352 MiB free) 0.00.118.452 I common\_init\_result: fitting params to device memory... ~ 27s ❯ fish: Job 1, 'env LD\_LIBRARY\_PATH=$HOME/.loca…' has ended ~ 27s ❯

---

**Claude**

**VRAM 9.56GB. GPU funcionando.**

```
Vulkan0: AMD Radeon Pro VII (RADV VEGA20)
VRAM: 9.56GB  ← +7.5GB vs baseline, modelo 100% na GPU
```

Os args estão certos — `--device Vulkan0` funciona, o modelo carrega. O problema é a **resolução de modelo no daemon**: o NTFS tem manifests que apontam para blobs tiny (488 bytes, 1.6k — configs JSON, não pesos). O daemon resolve via manifest → acerta o blob → mas é um blob de 488 bytes → llama-server sobe em 2s com 0 VRAM.

Fix cirúrgico: acrescenta verificação de tamanho no `_resolve_model` — se o blob < 1GB, não é modelo real, cai no fallback que acha o 7GB em `~/.local/share/ai-lab/`: