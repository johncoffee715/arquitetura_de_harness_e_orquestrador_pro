# Modelos — Estratégia de Download

**Data:** 2026-07-21  
**GPU:** AMD Vega 20 (Radeon Pro VII / MI50) — 16 GB HBM2  
**Runtime:** Ollama em `/mnt/dados/Assistente Pessoal/modelos LLM/`  
**Fine-tune:** Pesos fp16 via HuggingFace para LoRA

---

## 1. Gran-Mestre / Prometheus / Héstia — Planejamento & Validação (cat. 1)

| Atributo | Valor |
|---|---|
| **Modelo** | Qwen3.5 27B IQ3_XXS |
| **Comando** | `ollama pull hf.co/unsloth/Qwen3.5-27B-GGUF:IQ3_XXS` |
| **Quant** | IQ3_XXS (Unsloth) |
| **Nota** | Priorizar quant Unsloth — a origem do GGUF muda drasticamente a confiabilidade |

## 2. Atlas / Atena — Execução & Revisão (cat. 2)

| Atributo | Valor |
|---|---|
| **Modelo** | Qwen3-Coder-30B-A3B MoE |
| **Comando** | `ollama pull qwen3-coder:30b-a3b-q3_K_M` |
| **Quant** | Q3_K_M ou IQ4_XS |
| **Nota** | ⚠️ Q4_K_M estoura 16 GB. Q3_K_M/IQ4_XS cabe (~15 GB). Confirmar tag exata em ollama.com/library/qwen3-coder |

## 3. Pesquisa & Documentação (cat. 3)

| Atributo | Valor |
|---|---|
| **Modelo** | Gemma 4 26B-A4B MoE |
| **Comando** | `ollama pull gemma4:26b-a4b-q4_K_M` |
| **Quant** | Q4_K_M |
| **Nota** | Confirmar disponibilidade no library; se não existir, buscar GGUF no HuggingFace |

## 4. Leve / Rápido — Uso diário (cat. 4)

| Opção | Modelo | Comando | Tamanho |
|---|---|---|---|
| **A** (recomendado) | Qwen2.5-Coder-14B | `ollama pull qwen2.5-coder:14b` | ~9 GB |
| **B** (alternativa) | Phi-4 14B | `ollama pull phi4:14b` | ~9 GB |

Ambos cabem folgados em 16 GB e são bons para tarefas rápidas.

## 5. Fine-tune — Pesos fp16 (não GGUF)

### Modelo alvo do fine-tune
| Atributo | Valor |
|---|---|
| **Modelo** | Qwen2.5-Coder-7B-Instruct |
| **Fonte** | HuggingFace: `Qwen/Qwen2.5-Coder-7B-Instruct` |
| **Formato** | fp16 (pesos originais, não GGUF) |
| **Uso** | LoRA / fine-tune |

### Roteador Gran-Mestre (se fine-tune separado)
| Atributo | Valor |
|---|---|
| **Modelo** | Qwen3 8B |
| **Fonte** | HuggingFace: `Qwen/Qwen3-8B` |
| **Formato** | fp16 |

## 6. A Testar — Promover com cautela

| Atributo | Valor |
|---|---|
| **Modelo** | Bonsai 27B |
| **Fonte** | HuggingFace: `prism-ml/Bonsai-27B-gguf` |
| **Tag Ollama** | Nenhuma ainda (lançamento de ~1 semana) |
| **Validação** | Testar antes de promover para categoria CRITICAL |
| **Risco** | Não confiar ainda — validar confiabilidade antes de usar em autofagia e caminhos críticos |

## Ordem de Download

```
1. ollama pull qwen2.5-coder:14b              # Leve/rápido — já testado, cabe folgado
2. ollama pull phi4:14b                        # Alternativa — uso imediato
3. ollama pull hf.co/unsloth/Qwen3.5-27B-GGUF:IQ3_XXS  # Cat. 1 — prioridade máxima
4. ollama pull qwen3-coder:30b-a3b-q3_K_M     # Cat. 2 — confirmar tag
5. ollama pull gemma4:26b-a4b-q4_K_M          # Cat. 3 — verificar disponibilidade
6. git clone ... Qwen2.5-Coder-7B-Instruct     # Fine-tune (fp16)
```

## Setup Docker

```bash
# Iniciar daemon
sudo dockerd

# Subir stack de observabilidade
cd ~/observability && docker-compose up -d

# Verificar
curl http://localhost:16686   # Jaeger UI — traces
curl http://localhost:3000    # Grafana (admin/admin) — métricas
```
