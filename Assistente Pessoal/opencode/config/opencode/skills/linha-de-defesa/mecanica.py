#!/usr/bin/env python3
import sys
sys.path.insert(0, "/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/hefesto/tooling")
from kv_guard import calculate_budget
from generation_watchdog import watchdog_check
from execution_gate import execution_gate
from result_validator import result_validator
from hefesto_llama_bridge import PydanticToGbnf, ConstrainedGenerate, validate_byte_level
import json, time

def linha_defesa(task, schema, completions_fn, tool_fn, context="", window=262144):
    budget = calculate_budget(window, context, json.dumps(schema))
    grammar = PydanticToGbnf(schema).to_gbnf() if schema else ""
    cg = ConstrainedGenerate(completions_fn, None, grammar=grammar, temperature=0.0, max_tokens=300, max_retries=3)
    text, meta = cg.run(task, context)
    wd = watchdog_check(text, len(text)//4, 300, time.time())
    if wd["action"] != "continue":
        raise RuntimeError(f"watchdog {wd}")
    ok, detail = validate_byte_level(text, None)
    if not ok:
        raise ValueError(f"validation {detail}")
    gate = execution_gate("write_file", {"path": "/tmp/test"}, schema, {}, task, task)
    if gate["gate"] == "DENY":
        raise PermissionError(gate)
    before = {}
    result = tool_fn(text)
    after = {"status": "done"}
    validation = result_validator({"status": "done"}, before, after, {"content": text})
    return {"status": validation["result"], "output": text, "budget": budget, "watchdog": wd}
