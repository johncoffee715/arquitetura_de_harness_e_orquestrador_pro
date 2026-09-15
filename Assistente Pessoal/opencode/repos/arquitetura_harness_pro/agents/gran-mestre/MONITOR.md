# Gran-Mestre Monitor — Documentação

## Origem

**Autofagia de:** `/mnt/dados/Assistente Pessoal/agents/cairo_agent.py`

O Cairo Agent original era um daemon de vigilância + dreaming para o assistente pessoal. Esta versão é uma **evolução** adaptada para o Gran-Mestre Pipeline.

## O que foi absorvido (Autofagia)

### ✅ Útil — Mantido e melhorado

| Componente | Cairo Original | Gran-Mestre Monitor |
|------------|---------------|---------------------|
| GPU Monitoring | `vram_free_gb()`, `gpu_temp()`, `gpu_usage()` | `GPUMonitor` class |
| Service Check | `svc_alive(port)` | `ServiceMonitor` class |
| Auto-Heal | `auto_fix(fix)` | `AutoHealer` class |
| Dreaming | `dream(history)` | `DreamEngine` class |
| Análise | `analyze(m)` | `Analyzer` class |
| Coleta | `collect()` | `GranMestreMonitor.collect()` |

### ❌ Não útil — Removido ou substituído

| Item | Motivo | Substituição |
|------|--------|--------------|
| `BASE=Path("/mnt/win2/...")` | Hardcoded | `Config.base_dir` (configurável) |
| `VRAM_TOTAL=17163091968` | Hardcoded | `_detect_vram_total()` (auto-detect) |
| `notify-send` | Desktop only | Logging estruturado |
| `import urllib.request` | HTTP manual | Subprocesso Ollama/Qdrant |
| Paths absolutos | Inflexível | Configuração JSON |

## Arquitetura

```
GranMestreMonitor
├── Config              ← Configuração centralizada
├── Logger              ← Logging estruturado
├── GPUMonitor          ← Monitoramento de GPU
├── ServiceMonitor      ← Monitoramento de serviços
├── AutoHealer          ← Auto-healing
├── DreamEngine         ← Consolidação de memória
└── Analyzer            ← Análise de métricas
```

## Uso

### Como daemon
```bash
python3 ~/.config/opencode/agents/gran-mestre/gran-mestre-monitor.py --daemon
```

### Ver status
```bash
python3 ~/.config/opencode/agents/gran-mestre/gran-mestre-monitor.py --status
```

### Executar dream agora
```bash
python3 ~/.config/opencode/agents/gran-mestre/gran-mestre-monitor.py --dream-now
```

### Com configuração customizada
```bash
python3 ~/.config/opencode/agents/gran-mestre/gran-mestre-monitor.py --config monitor-config.json
```

## Configuração

O arquivo `monitor-config.json` permite configurar:

- **interval** — Intervalo de coleta em segundos (default: 300)
- **dream_after** — Segundos idle antes de dream (default: 1800)
- **auto_heal** — Habilitar auto-healing (default: true)
- **gpu.device** — Path do device GPU
- **gpu.temp_critical** — Temperatura crítica (default: 80°C)
- **gpu.vram_critical_gb** — VRAM crítica (default: 2GB)
- **services** — Portas dos serviços

## Auto-Healing

| Issue | Fix | Descrição |
|-------|-----|-----------|
| TEMP CRÍTICA | `gpu_reset` | Reset performance level |
| VRAM CRÍTICA | `clear_vram` | Reiniciar Ollama |
| Ollama offline | `restart_ollama` | `systemctl restart ollama` |
| Qdrant offline | `restart_qdrant` | `systemctl restart qdrant` |
| CPU FALLBACK | `heal_gpu` | Matar e reiniciar Ollama |

## Dreaming

O Dream Engine consolida memória quando o sistema está idle:

1. Verifica arquivos modificados (SHA256)
2. Calcula VRAM média
3. Salva relatório de estado
4. (Futuro) Ingestão no Qdrant

## Diferenças para o Cairo Original

| Aspecto | Cairo | Gran-Mestre Monitor |
|---------|-------|---------------------|
| Arquitetura | Monolítico | Modular (classes) |
| Configuração | Hardcoded | JSON configurável |
| Logging | Print + arquivo | Estruturado |
| Error handling | Try/except silencioso | Logging de erros |
| Extensibilidade | Baixa | Alta |
| Testabilidade | Baixa | Alta |

---

**Versão:** 1.0.0
**Origem:** Autofagia de cairo_agent.py
**Autor:** Gran-Mestre