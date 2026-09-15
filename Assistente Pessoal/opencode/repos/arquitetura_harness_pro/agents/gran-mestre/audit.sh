#!/usr/bin/env bash
# GRAN-MAESTRO AUDITOR — Verificação completa de componentes
# Data: 2026-07-24

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
PASS=0
FAIL=0
WARN=0

# Funções
log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    PASS=$((PASS + 1))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    FAIL=$((FAIL + 1))
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    WARN=$((WARN + 1))
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

separator() {
    echo ""
    echo "============================================"
    echo ""
}

# =============================================================================
# 1. VERIFICAR ESTRUTURA DE DIRETÓRIOS
# =============================================================================

check_directories() {
    log_info "Verificando estrutura de diretórios..."
    
    # Diretórios obrigatórios
    dirs=(
        "$HOME/.opencode"
        "$HOME/.opencode/skills"
        "$HOME/.opencode/architecture"
        "$HOME/.opencode/logs"
        "$HOME/.opencode/state"
        "$HOME/.config/opencode/agents"
        "$HOME/.config/opencode/agents/gran-mestre"
    )
    
    for dir in "${dirs[@]}"; do
        if [ -d "$dir" ]; then
            log_pass "Diretório existe: $dir"
        else
            log_fail "Diretório NÃO existe: $dir"
        fi
    done
}

# =============================================================================
# 2. VERIFICAR AGENTS GRAN-MAESTRE
# =============================================================================

check_gran_mestre_agents() {
    log_info "Verificando agents Gran-Mestre..."
    
    agents=(
        "$HOME/.config/opencode/agents/gran-mestre/HESTIA.md"
        "$HOME/.config/opencode/agents/gran-mestre/ATHENA.md"
        "$HOME/.config/opencode/agents/gran-mestre/TEMPLATE.md"
        "$HOME/.config/opencode/agents/gran-mestre/MODEL_ROTATION.md"
        "$HOME/.config/opencode/agents/gran-mestre/MONITOR.md"
        "$HOME/.config/opencode/agents/gran-mestre/gran-mestre-monitor.py"
        "$HOME/.config/opencode/agents/gran-mestre/monitor-config.json"
    )
    
    for agent in "${agents[@]}"; do
        if [ -f "$agent" ]; then
            log_pass "Agent existe: $(basename $agent)"
        else
            log_fail "Agent NÃO existe: $(basename $agent)"
        fi
    done
}

# =============================================================================
# 3. VERIFICAR SKILLS
# =============================================================================

check_skills() {
    log_info "Verificando skills..."
    
    skills=(
        "$HOME/.opencode/skills/hestia/SKILL.md"
        "$HOME/.opencode/skills/athena/SKILL.md"
        "$HOME/.opencode/skills/gran-mestre/SKILL.md"
    )
    
    for skill in "${skills[@]}"; do
        if [ -f "$skill" ]; then
            log_pass "Skill existe: $(basename $(dirname $skill))"
        else
            log_warn "Skill NÃO existe: $(basename $(dirname $skill))"
        fi
    done
}

# =============================================================================
# 4. VERIFICAR ARQUITETURA
# =============================================================================

check_architecture() {
    log_info "Verificando arquitetura..."
    
    arch_files=(
        "$HOME/.opencode/architecture/CORPO_DO_OPENCODE.md"
        "$HOME/.opencode/architecture/README.md"
    )
    
    for file in "${arch_files[@]}"; do
        if [ -f "$file" ]; then
            log_pass "Arquivo existe: $(basename $file)"
        else
            log_fail "Arquivo NÃO existe: $(basename $file)"
        fi
    done
}

# =============================================================================
# 5. VERIFICAR CLAUDE.md
# =============================================================================

check_claude_md() {
    log_info "Verificando CLAUDE.md..."
    
    claude_md="$HOME/.opencode/CLAUDE.md"
    
    if [ -f "$claude_md" ]; then
        log_pass "CLAUDE.md existe"
        
        # Verificar seções obrigatórias
        sections=(
            "Gran-Mestre Pipeline"
            "Héstia"
            "Atena"
            "Model Rotation"
        )
        
        for section in "${sections[@]}"; do
            if grep -q "$section" "$claude_md"; then
                log_pass "Seção encontrada: $section"
            else
                log_warn "Seção NÃO encontrada: $section"
            fi
        done
    else
        log_fail "CLAUDE.md NÃO existe"
    fi
}

# =============================================================================
# 6. VERIFICAR METADATA DOS AGENTS
# =============================================================================

check_metadata() {
    log_info "Verificando metadata dos agents..."
    
    hestia="$HOME/.config/opencode/agents/gran-mestre/HESTIA.md"
    athena="$HOME/.config/opencode/agents/gran-mestre/ATHENA.md"
    
    # Verificar Héstia
    if [ -f "$hestia" ]; then
        if grep -q "name: hestia" "$hestia"; then
            log_pass "Héstia: name definido"
        else
            log_fail "Héstia: name NÃO definido"
        fi
        
        if grep -q "model:" "$hestia"; then
            log_pass "Héstia: model definido"
        else
            log_fail "Héstia: model NÃO definido"
        fi
        
        if grep -q "mode:" "$hestia"; then
            log_pass "Héstia: mode definido"
        else
            log_fail "Héstia: mode NÃO definido"
        fi
        
        if grep -q "origin:" "$hestia"; then
            log_pass "Héstia: origin definido"
        else
            log_fail "Héstia: origin NÃO definido"
        fi
        
        if grep -q "model_rotation:" "$hestia"; then
            log_pass "Héstia: model_rotation definido"
        else
            log_warn "Héstia: model_rotation NÃO definido"
        fi
    fi
    
    # Verificar Atena
    if [ -f "$athena" ]; then
        if grep -q "name: atena" "$athena"; then
            log_pass "Atena: name definido"
        else
            log_fail "Atena: name NÃO definido"
        fi
        
        if grep -q "model:" "$athena"; then
            log_pass "Atena: model definido"
        else
            log_fail "Atena: model NÃO definido"
        fi
        
        if grep -q "mode:" "$athena"; then
            log_pass "Atena: mode definido"
        else
            log_fail "Atena: mode NÃO definido"
        fi
        
        if grep -q "origin:" "$athena"; then
            log_pass "Atena: origin definido"
        else
            log_fail "Atena: origin NÃO definido"
        fi
        
        if grep -q "model_rotation:" "$athena"; then
            log_pass "Atena: model_rotation definido"
        else
            log_warn "Atena: model_rotation NÃO definido"
        fi
    fi
}

# =============================================================================
# 7. VERIFICAR PYTHON
# =============================================================================

check_python() {
    log_info "Verificando Python..."
    
    if command -v python3 &> /dev/null; then
        log_pass "Python3 instalado: $(python3 --version)"
    else
        log_fail "Python3 NÃO instalado"
    fi
    
    # Verificar script do monitor
    monitor="$HOME/.config/opencode/agents/gran-mestre/gran-mestre-monitor.py"
    if [ -f "$monitor" ]; then
        if python3 -c "import ast; ast.parse(open('$monitor').read())" 2>/dev/null; then
            log_pass "Monitor: syntax OK"
        else
            log_fail "Monitor: syntax ERROR"
        fi
    fi
}

# =============================================================================
# 8. VERIFICAR JSON
# =============================================================================

check_json() {
    log_info "Verificando arquivos JSON..."
    
    json_files=(
        "$HOME/.config/opencode/agents/gran-mestre/monitor-config.json"
    )
    
    for json in "${json_files[@]}"; do
        if [ -f "$json" ]; then
            if python3 -c "import json; json.load(open('$json'))" 2>/dev/null; then
                log_pass "JSON válido: $(basename $json)"
            else
                log_fail "JSON inválido: $(basename $json)"
            fi
        fi
    done
}

# =============================================================================
# 9. VERIFICAR MODELOS
# =============================================================================

check_models() {
    log_info "Verificando modelos configurados..."
    
    oh_my="$HOME/.opencode/config/opencode/oh-my-openagent.json"
    
    if [ -f "$oh_my" ]; then
        log_pass "oh-my-openagent.json existe"
        
        # Verificar agents configurados
        agents=$(python3 -c "import json; data=json.load(open('$oh_my')); print(len(data.get('agents', {})))" 2>/dev/null || echo "0")
        log_pass "Agents configurados: $agents"
        
        # Verificar se hestia e atena estão configurados
        if python3 -c "import json; data=json.load(open('$oh_my')); assert 'hestia' in data.get('agents', {})" 2>/dev/null; then
            log_pass "Héstia: configurado em oh-my-openagent.json"
        else
            log_warn "Héstia: NÃO configurado em oh-my-openagent.json"
        fi
        
        if python3 -c "import json; data=json.load(open('$oh_my')); assert 'atena' in data.get('agents', {})" 2>/dev/null; then
            log_pass "Atena: configurado em oh-my-openagent.json"
        else
            log_warn "Atena: NÃO configurado em oh-my-openagent.json"
        fi
    else
        log_warn "oh-my-openagent.json NÃO existe"
    fi
}

# =============================================================================
# 10. VERIFICAR PIPELINE
# =============================================================================

check_pipeline() {
    log_info "Verificando pipeline Gran-Mestre..."
    
    # Verificar se as fases estão documentadas
    hestia="$HOME/.config/opencode/agents/gran-mestre/HESTIA.md"
    
    if [ -f "$hestia" ]; then
        phases=("Fase 2" "Fase 3" "Fase 6")
        for phase in "${phases[@]}"; do
            if grep -q "$phase" "$hestia"; then
                log_pass "Héstia: $phase documentada"
            else
                log_warn "Héstia: $phase NÃO documentada"
            fi
        done
    fi
    
    athena="$HOME/.config/opencode/agents/gran-mestre/ATHENA.md"
    
    if [ -f "$athena" ]; then
        if grep -q "Fase 5" "$athena"; then
            log_pass "Atena: Fase 5 documentada"
        else
            log_warn "Atena: Fase 5 NÃO documentada"
        fi
    fi
}

# =============================================================================
# 11. VERIFICAR SEGURANÇA
# =============================================================================

check_security() {
    log_info "Verificando segurança..."
    
    # Verificar se agents são read-only
    hestia="$HOME/.config/opencode/agents/gran-mestre/HESTIA.md"
    athena="$HOME/.config/opencode/agents/gran-mestre/ATHENA.md"
    
    for agent in "$hestia" "$athena"; do
        if [ -f "$agent" ]; then
            name=$(basename "$agent" .md)
            
            if grep -q "edit/deny" "$agent" || grep -q "write/deny" "$agent"; then
                log_pass "$name: permissões restritivas"
            else
                log_warn "$name: permissões NÃO verificadas"
            fi
            
            if grep -q "read-only" "$agent" || grep -q "read/allow" "$agent"; then
                log_pass "$name: modo read-only"
            else
                log_warn "$name: modo read-only NÃO verificado"
            fi
        fi
    done
}

# =============================================================================
# 12. VERIFICAR ROTAÇÃO DE MODELOS
# =============================================================================

check_model_rotation() {
    log_info "Verificando sistema de rotação..."
    
    rotation="$HOME/.config/opencode/agents/gran-mestre/MODEL_ROTATION.md"
    
    if [ -f "$rotation" ]; then
        log_pass "MODEL_ROTATION.md existe"
        
        if grep -q "max_retries_per_model: 1" "$rotation"; then
            log_pass "Rotação: falha em 1x"
        else
            log_warn "Rotação: configuração diferente"
        fi
        
        if grep -q "continue_after_escalate: true" "$rotation"; then
            log_pass "Rotação: continuar após escalar"
        else
            log_warn "Rotação: configuração diferente"
        fi
        
        if grep -q "restart_order: free_first" "$rotation"; then
            log_pass "Rotação: reiniciar por FREE + PAGOS"
        else
            log_warn "Rotação: configuração diferente"
        fi
    else
        log_fail "MODEL_ROTATION.md NÃO existe"
    fi
}

# =============================================================================
# EXECUTAR TODAS AS VERIFICAÇÕES
# =============================================================================

main() {
    echo ""
    echo "============================================"
    echo "  GRAN-MAESTRO AUDITOR — Verificação Completa"
    echo "  Data: $(date)"
    echo "============================================"
    echo ""
    
    separator
    check_directories
    
    separator
    check_gran_mestre_agents
    
    separator
    check_skills
    
    separator
    check_architecture
    
    separator
    check_claude_md
    
    separator
    check_metadata
    
    separator
    check_python
    
    separator
    check_json
    
    separator
    check_models
    
    separator
    check_pipeline
    
    separator
    check_security
    
    separator
    check_model_rotation
    
    separator
    echo ""
    echo "============================================"
    echo "  RESULTADO FINAL"
    echo "============================================"
    echo ""
    echo -e "${GREEN}PASS: $PASS${NC}"
    echo -e "${RED}FAIL: $FAIL${NC}"
    echo -e "${YELLOW}WARN: $WARN${NC}"
    echo ""
    
    if [ $FAIL -eq 0 ]; then
        echo -e "${GREEN}✅ AUDITORIA COMPLETA — SEM FALHAS CRÍTICAS${NC}"
        exit 0
    else
        echo -e "${RED}❌ AUDITORIA COMPLETA — $FAIL FALHAS ENCONTRADAS${NC}"
        exit 1
    fi
}

main