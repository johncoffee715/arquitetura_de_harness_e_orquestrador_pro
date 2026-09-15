"""Plugin helenizado v3 (espec do usuário): filtra NA FONTE.
Emite APENAS falhas da fase 'call' com excinfo bruta — zero ruído setup/teardown."""
import json, os, pytest

OUT = os.environ.get("NEEDLE_JSONL", "needle_evidencias.jsonl")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if call.when != "call" or not call.excinfo:
        return
    rec = {"nodeid": item.nodeid,
           "arquivo": item.location[0], "linha": item.location[1],
           "excecao_tipo": call.excinfo.typename,
           "excecao_valor": str(call.excinfo.value)[:300],
           "repr_cauda": str(rep.longrepr)[-600:]}
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
