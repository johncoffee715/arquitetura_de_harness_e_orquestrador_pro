# Contexto Atual — snapshot cognitivo (2026-08-24T20:39:11.497453+00:00)

## Decisões desta sessão
- Deploy R11 real concluído: alvos.json 16→31; 158 artefatos (15 skills+15 subagents+hooks+plugins); registry 28→43
- MTP verificado no build local llama.cpp (--spec-type draft-mtp, libmtmd.so) — feature llama-mtp p/ 4 modelos Vulkan
- MCP openwork ativado em opencode/config/opencode.json (remote, oauth, mcp_openwork: allow) — aprovado pelo usuário
- Histórico HISTORICO_AUTOFAGIA.md §16 atualizado com deploy real + MCP

## Tarefas ativas / pendências
- (sem pendências)

## Próximos passos
- Aplicar BM25 em route_to_model (herdada R10)
- pytest 8 cenários do arsenal (herdada R10)
- Opcional: testar MCP openwork (requer auth OAuth no browser)

## Riscos / estado
- WORKSPACE COM MUDANÇAS NÃO-COMMITADAS (deploy R11 + MCP openwork) — commit pendente antes de reset
- Delegação de subagents falha (anti-padrão R8/R9) — usar gh api contido
- Skills ricas preservadas (hallmark, book-to-skill — guard)

## Snapshot técnico
- git:  M "cerebro com IA/aprendizados/R64_R65_manifesto_llm_auditoria_kv_2026-08-24.md",  M harness/logs/llm-usage-8083.jsonl,  M harness/logs/llm-usage-8090.jsonl,  m opencode, ?? "Assistente Pessoal/gpu-fw/", ?? "Assistente Pessoal/logs/", ?? "Assistente Pessoal/modelos LLM/Bonsai-27B-1bit.Q4_K_M.gguf", ?? "Assistente Pessoal/modelos LLM/LFM2.5-230M-Q4_0.gguf", ?? "Assistente Pessoal/modelos LLM/LLMJudge-Qwen2.5-3B.Q4_K_M.gguf", ?? "Assistente Pessoal/modelos LLM/Ornith-1.5-9B-Q4_K_M.gguf", ?? "Assistente Pessoal/modelos LLM/Phi-4-mini-instruct-Q4_K_M.gguf", ?? "Assistente Pessoal/modelos LLM/Qwen3-1.7B-Q4_K_M.gguf", ?? "Assistente Pessoal/modelos LLM/Qwen3.5-0.8B.gguf", ?? "Assistente Pessoal/modelos LLM/Qwen3.5-4B-UD-IQ2_XXS.gguf", ?? "Assistente Pessoal/modelos LLM/Qwen3.8-27B-UD-IQ1_S.gguf", ?? "Assistente Pessoal/modelos LLM/Qwen3.8-27B-UD-IQ2_XXS.gguf", ?? "Assistente Pessoal/modelos LLM/Qwen3.8-2B-Q4_K_M.gguf", ?? "Assistente Pessoal/modelos LLM/Qwen3.8-4B-Q4_K_M.gguf", ?? "Assistente Pessoal/modelos LLM/Qwen3.8-9B-Q4_K_M.gguf", ?? "Assistente Pessoal/modelos LLM/Ternary-Bonsai-1.7B-Q2_0_g64.gguf"
- ECC_HOME: $HOME/.ecc/autofagia
- registry entries: 336
