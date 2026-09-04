#!/usr/bin/env python3
"""
Testes TDD para Kronjob Tálamos Filter Hook.
Cobertura: intent classification, slot resolution, hook integration.
"""

import sys
import json
from pathlib import Path

# Adiciona path do hook
HOOK_PATH = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/hooks/kronjob-talamus-filter.py")
sys.path.insert(0, str(HOOK_PATH.parent))

# Importa o módulo
import importlib.util
spec = importlib.util.spec_from_file_location("kronjob_talamus", HOOK_PATH)
kronjob = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kronjob)


def test_classify_intent_primitive():
    """Testa classificação de intents primitivos (olá, obrigado, etc)."""
    primitives = ["olá", "oi", "bom dia", "obrigado", "thanks", "tchau", "bye", "hey", "hi", "hello"]
    for p in primitives:
        intent = kronjob.classify_intent(p)
        assert intent == "PRIMITIVE_HELLO_OR_THANKYOU", f"Falhou para '{p}': {intent}"
    print(f"✅ test_classify_intent_primitive: {len(primitives)} prompts classificados corretamente")


def test_classify_intent_needle():
    """Testa classificação NEEDLE_EXACT_SEARCH_TRIGGER."""
    needles = ["buscar exato no needle", "exact search", "needle search", "procurar exat", "busca exata"]
    for n in needles:
        intent = kronjob.classify_intent(n)
        assert intent == "NEEDLE_EXACT_SEARCH_TRIGGER", f"Falhou para '{n}': {intent}"
    print(f"✅ test_classify_intent_needle: {len(needles)} prompts classificados")


def test_classify_intent_rag():
    """Testa classificação RAG_DOCUMENTS."""
    rags = ["documento relevante", "rag context", "contexto do parágrafo", "rerank documentos"]
    for r in rags:
        intent = kronjob.classify_intent(r)
        assert intent == "RAG_DOCUMENTS", f"Falhou para '{r}': {intent}"
    print(f"✅ test_classify_intent_rag: {len(rags)} prompts classificados")


def test_classify_intent_history():
    """Testa classificação LONG_CHAT_HISTORY."""
    histories = ["resumo do histórico de conversa", "conversa anterior", "chat anterior", "thread de discussão"]
    for h in histories:
        intent = kronjob.classify_intent(h)
        assert intent == "LONG_CHAT_HISTORY", f"Falhou para '{h}': {intent}"
    print(f"✅ test_classify_intent_history: {len(histories)} prompts classificados")


def test_classify_intent_logs():
    """Testa classificação RAW_LOGS."""
    logs = ["extrair erros do log", "error critical", "stack trace exception", "log de erro"]
    for l in logs:
        intent = kronjob.classify_intent(l)
        assert intent == "RAW_LOGS", f"Falhou para '{l}': {intent}"
    print(f"✅ test_classify_intent_logs: {len(logs)} prompts classificados")


def test_classify_intent_web():
    """Testa classificação WEB_SCRAPING."""
    webs = ["scraping de página web", "scrape site html", "web scrap página"]
    for w in webs:
        intent = kronjob.classify_intent(w)
        assert intent == "WEB_SCRAPING", f"Falhou para '{w}': {intent}"
    print(f"✅ test_classify_intent_web: {len(webs)} prompts classificados")


def test_classify_intent_general():
    """Testa classificação GENERAL para prompts sem padrão."""
    generals = ["implementar feature X", "refatorar código", "explicar conceito", "criar teste"]
    for g in generals:
        intent = kronjob.classify_intent(g)
        assert intent == "GENERAL", f"Falhou para '{g}': {intent}"
    print(f"✅ test_classify_intent_general: {len(generals)} prompts classificados")


def test_resolve_fast_cpu_slot():
    """Testa resolução do slot CPU mais rápido para Tálamos."""
    slot = kronjob.resolve_fast_cpu_slot()
    assert slot is not None, "Slot CPU não resolvido"
    assert "id" in slot, "Slot sem id"
    assert "port" in slot, "Slot sem port"
    assert "params" in slot, "Slot sem params"
    # Deve ser um modelo pequeno (≤2B) para velocidade
    params = slot.get("params", "99B")
    assert "0.4" in params or "1" in params or "2" in params, f"Slot não é rápido: {params}"
    print(f"✅ test_resolve_fast_cpu_slot: {slot['id']} @ {slot['port']} ({params})")


def test_resolve_orchestrator_slot():
    """Testa resolução do slot orquestrador (VRAM)."""
    slot = kronjob.resolve_orchestrator_slot()
    assert slot is not None, "Slot orquestrador não resolvido"
    assert "id" in slot, "Slot sem id"
    assert "port" in slot, "Slot sem port"
    assert "baseURL" in slot, "Slot sem baseURL"
    print(f"✅ test_resolve_orchestrator_slot: {slot['id']} @ {slot['port']}")


def test_execute_talamus_filter_primitive():
    """Testa execução completa do filtro para intent primitivo."""
    result = kronjob.execute_talamus_filter("olá")
    assert result["intent"] == "PRIMITIVE_HELLO_OR_THANKYOU"
    assert result["action_required"] == "DIRECT_RESPONSE"
    assert "fast_cpu_slot" in result
    assert "orchestrator_slot" in result
    print(f"✅ test_execute_talamus_filter_primitive: action={result['action_required']}")


def test_execute_talamus_filter_dispatch():
    """Testa execução completa do filtro para intent que requer dispatch."""
    result = kronjob.execute_talamus_filter("buscar exato no needle")
    assert result["intent"] == "NEEDLE_EXACT_SEARCH_TRIGGER"
    assert result["action_required"] == "DISPATCH_VRAM"
    assert result["distilled"].startswith("[INTENT: NEEDLE_EXACT_SEARCH_TRIGGER]")
    print(f"✅ test_execute_talamus_filter_dispatch: action={result['action_required']}")


def test_hook_session_start_primitive():
    """Testa hook session.start para intent primitivo (economiza VRAM)."""
    ctx = {"prompt": "obrigado", "session_id": "test-001"}
    result = kronjob.hook_session_start(ctx)
    assert "__KRONJOB_TALAMUS__" in result, "Tálamos não injetado"
    assert result["__KRONJOB_TALAMUS__"]["active"] is True
    assert result["__KRONJOB_TALAMUS__"]["intent"] == "PRIMITIVE_HELLO_OR_THANKYOU"
    assert result["__KRONJOB_TALAMUS__"]["action"] == "DIRECT_RESPONSE"
    assert result.get("__VRAM_SAVED__") is True, "VRAM deveria estar marcada como economizada"
    print(f"✅ test_hook_session_start_primitive: VRAM economizada ✅")


def test_hook_session_start_dispatch():
    """Testa hook session.start para intent que requer dispatch."""
    ctx = {"prompt": "implementar feature complexa", "session_id": "test-002"}
    result = kronjob.hook_session_start(ctx)
    assert "__KRONJOB_TALAMUS__" in result
    assert result["__KRONJOB_TALAMUS__"]["intent"] == "GENERAL"
    assert result["__KRONJOB_TALAMUS__"]["action"] == "DISPATCH_VRAM"
    assert "__VRAM_SAVED__" not in result, "VRAM não deveria estar economizada para dispatch"
    print(f"✅ test_hook_session_start_dispatch: dispatch VRAM ativado")


def test_hook_before_tool():
    """Testa hook before_tool."""
    args = {"file": "test.py", "action": "read"}
    result = kronjob.hook_before_tool("read", args)
    assert result == args, "Args não preservados"
    print(f"✅ test_hook_before_tool: args preservados")


def test_no_hardcoded_ports():
    """Testa que não há portas hardcoded no hook (R35/R47)."""
    source = HOOK_PATH.read_text()
    # Verifica que não há atribuição direta de porta numérica
    # exceto em comentários/documentação
    lines = [l for l in source.split("\n") if "9090" in l or "8083" in l or "9087" in l or "9088" in l]
    hardcoded = [l for l in lines if not l.strip().startswith("#") and "http" not in l]
    # Apenas referências em docstrings/comentários são aceitas
    non_doc = [l for l in hardcoded if '"""' not in l and "slot ==" not in l and "==" not in l]
    assert len(non_doc) == 0, f"Portas hardcoded encontradas: {non_doc}"
    print(f"✅ test_no_hardcoded_ports: nenhuma porta hardcoded em código ativo")


def test_inventory_resolved():
    """Testa que o inventário é carregado e usado (R35)."""
    inv = kronjob.load_inventory()
    assert "models" in inv, "Inventário sem models"
    assert len(inv["models"]) > 0, "Inventário vazio"
    assert "schema_version" in inv, "Inventário sem schema_version"
    print(f"✅ test_inventory_resolved: {len(inv['models'])} modelos no inventário")


# Execução dos testes
if __name__ == "__main__":
    print("=" * 60)
    print("KRONJOB TALAMUS HOOK — TESTES TDD")
    print("=" * 60)
    print()
    
    tests = [
        test_classify_intent_primitive,
        test_classify_intent_needle,
        test_classify_intent_rag,
        test_classify_intent_history,
        test_classify_intent_logs,
        test_classify_intent_web,
        test_classify_intent_general,
        test_resolve_fast_cpu_slot,
        test_resolve_orchestrator_slot,
        test_execute_talamus_filter_primitive,
        test_execute_talamus_filter_dispatch,
        test_hook_session_start_primitive,
        test_hook_session_start_dispatch,
        test_hook_before_tool,
        test_no_hardcoded_ports,
        test_inventory_resolved,
    ]
    
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"❌ {t.__name__}: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"RESULTADO: {passed}/{len(tests)} passed, {failed} failed")
    print("=" * 60)
    
    sys.exit(0 if failed == 0 else 1)
