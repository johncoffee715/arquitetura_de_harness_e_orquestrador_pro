# Learnings — Sessão: Integração Cascade + LLM Local

## Arquitetura

### 1. Cascade zíper (6 fases)
Superpowers agent system integrado ao Gran-Mestre. Fases: DESCOBERTA → CONTRATO → PLANO → EXECUÇÃO → REVISÃO → ENTREGA. Portões duplos: A=interativo (aprovação do usuário por fase), C=autônomo (executa tudo). Validação dupla: Implementer TDD → Code Reviewer micro → Atena macro.

### 2. Metáfora do usuário
"OpenCode é a cabeça, Tesseract são os olhos, agents/subagents/skills/MCP são o tronco, braços e pernas."

## LLM Local

### 3. Bypass do OmniRoute
Bug "No active credentials" não resolvido mas contornado. Provider direto `local` adicionado ao opencode.json apontando para llama-server em localhost:8080/v1. Permite operação offline do cascade sem dependência do OmniRoute.

### 4. Split de modelos
- **Escritores de fase** (superpowers/spec-writer/plan-writer): `local/qwen3.5-27b` (offline)
- **Implementer + code-reviewer**: `omniroute/auto/coding` (cloud necessária)
- **Orquestrador** (superpowers primary): modelo cloud

### 5. Constraint GPU Mi50
AMD Radeon Pro VII (Vega 20, gfx906) com 16GB VRAM carrega UM modelo grande por vez. Não roda Qwen3.5-27B e Qwen3-Coder-30B simultaneamente.

### 6. Deploy llama-server
systemd user service na porta 8080, backend Vulkan via driver RADV em /dev/dri/renderD128. Modelo: Qwen3.5-27B IQ3_XXS (11.51GB), ~6 tok/s.

## Disciplina

### 7. YAGNI ladder (ponytail)
Integrada ao GRAN_MESTRE.md. 7 passos:
1. Não adicione o que não precisa
2. Não configure o que funciona
3. Não abstraia antes da 3ª uso
4. Sem padrões sem 3 exemplos
5. Sem interfaces sem 2 implementações
6. Sem módulo novo se função serve
7. Sem pacote novo se módulo serve

## Misterioso

### 8. OmniRoute provider_connections
Row existe no SQLite, SQL correto, decrypt() OK, cache limpo por restart — ainda retorna "No active credentials". Causa raiz desconhecida. Contornado via provider direto.
