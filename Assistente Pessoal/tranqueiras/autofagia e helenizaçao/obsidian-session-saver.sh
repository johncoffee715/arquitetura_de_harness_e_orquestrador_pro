#!/bin/bash
# Gran-Mestre Cognitive Session Saver
# Salva sessões no Obsidian como memória persistente

VAULT="/home/johncoffee/ObsidianGranMestre"
SESSIONS_DIR="$VAULT/sessions"
MEMORIA_DIR="$VAULT/memoria"
HISTORICO_DIR="$VAULT/historico"

# Criar diretórios se não existirem
mkdir -p "$SESSIONS_DIR" "$MEMORIA_DIR" "$HISTORICO_DIR"

# Função para salvar sessão
save_session() {
    local session_id=$1
    local date=$(date '+%Y-%m-%d_%H-%M-%S')
    local filename="session_${date}_${session_id:0:8}.md"
    
    # Criar arquivo de sessão
    cat > "$SESSIONS_DIR/$filename" << EOF
# Sessão: $session_id

## Data
$date

## ID
$session_id

## Status
Salva automaticamente pelo Gran-Mestre

## Tags
#session #gran-mestre #cognicao

## Conteúdo
(Espaço para anotações da sessão)

## Aprendizados
- (Aprendizado 1)
- (Aprendizado 2)

## Decisões
- (Decisão 1)
- (Decisão 2)

## Referências
- (Referência 1)
- (Referência 2)
EOF

    echo "✅ Sessão salva: $filename"
}

# Função para listar sessões salvas
list_sessions() {
    echo "=== Sessões Salvas no Obsidian ==="
    ls -la "$SESSIONS_DIR"/*.md 2>/dev/null | awk '{print $NF}'
}

# Função para buscar na memória
search_memory() {
    local query=$1
    echo "=== Buscando na memória: $query ==="
    grep -r "$query" "$VAULT"/*.md 2>/dev/null | head -20
}

# Função principal
case "$1" in
    save)
        save_session "$2"
        ;;
    list)
        list_sessions
        ;;
    search)
        search_memory "$2"
        ;;
    *)
        echo "Uso: $0 {save <session_id>|list|search <query>}"
        ;;
esac
