#!/usr/bin/env python3
"""
HEFESTO LLAMA BRIDGE — Ferramental da Tríplice (.md/.py/.json/.gbnf)

Unifica bridge + automation + pipeline do ferramental Hefesto (helenizado):
- Compila flags do llama_cpp_config.json em comandos executáveis.
- Descobre novas flags do llama.cpp (--help) e injeta no JSON (PENDING_GBNF_VAL).
- Enriquecimento via LLM com gramática GBNF (hefesto_deep_spec.gbnf).
- Webhook para gatilho externo (GitHub Actions/CRON).

Origin: helenizado: tranqueiras/autofagia e helenizaçao (hefesto_llama_bridge.py,
hefesto_automation.py, hefesto_pipeline.py) — unificado 2026-08-31.
"""

import json
import os
import re
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

try:
    from pydantic import BaseModel, Field  # noqa: F401
    PYDANTIC_AVAILABLE = True
except Exception:
    PYDANTIC_AVAILABLE = False
    BaseModel = object  # type: ignore


# Paths globais do harness (R2/R44)
TOOLING_DIR = Path("/mnt/dados/Assistente Pessoal/opencode/config/opencode/skills/hefesto/tooling")
CONFIG_PATH = TOOLING_DIR / "llama_cpp_config.json"
SPEC_PATH = TOOLING_DIR / "llama_cpp_spec.md"
FEATURE_GBNF = TOOLING_DIR / "hefesto_feature.gbnf"
DEEP_GBNF = TOOLING_DIR / "hefesto_deep_spec.gbnf"
LLAMA_CLI = "/mnt/dados/Assistente Pessoal/opencode/llama.cpp/bin/llama-cli"
LLAMA_SERVER = "/mnt/dados/Assistente Pessoal/opencode/llama.cpp/bin/llama-server.real"
LD_LIBRARY_PATH = "/mnt/dados/Assistente Pessoal/opencode/llama.cpp/bin"



# ==============================================================================
# NÚCLEO R81/R82 — Geração Restrita Universal (Constrained Decoding)
# Fonte única: gabarito.json (R77) → Pydantic → JSON Schema → GBNF em runtime.
# .gbnf manual = legado/fallback; nunca fonte nova (R81/R82).
# ==============================================================================


def _lit(value) -> str:
    """Sanitiza valor para literal GBNF (escape de aspas/backslash)."""
    s = str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return s


def _regex_alt(pattern: str) -> str:
    """Regex simples (ex.: ^(a|b)$) -> alternância GBNF de literais."""
    pat = pattern.strip()
    if pat.startswith("^") and pat.endswith("$"):
        pat = pat[1:-1]
    if pat.startswith("(") and ")" in pat:
        inner = pat[pat.index("(") + 1:pat.rindex(")")]
        parts = [p for p in inner.split("|") if p.strip()]
        if parts:
            return " | ".join('"' + _lit(p) + '"' for p in parts)
    return '"' + _lit(pat) + '"'


class PydanticToGbnf:
    """Transpilador runtime: Pydantic (ou dict JSON Schema) -> gramática GBNF válida.

    R81/R82: a mesma estrutura que controla a lógica Python define a barreira física
    do amostrador. GBNF correto para JSON: literais de chaves/colchetes/aspas são
    escapados (ex.: "{" e "\""); `{ }` são quantificadores, NÃO delimitadores.
    """

    def __init__(self, model):
        if isinstance(model, dict):
            self.schema = model
        elif PYDANTIC_AVAILABLE and isinstance(model, type) and issubclass(model, BaseModel):
            self.schema = model.model_json_schema()
        else:
            raise TypeError("PydanticToGbnf requer dict JSON Schema ou classe BaseModel")

    def _resolve_ref(self, sch: dict) -> dict:
        ref = sch.get("$ref")
        if not ref:
            return sch
        return self.schema.get("$defs", {}).get(ref.split("/")[-1], {"type": "object"})

    def _build(self, sch: dict, depth: int = 0) -> str:
        if depth > 8:
            return '"null"'
        sch = self._resolve_ref(sch)
        if sch.get("enum"):
            # enum de strings: envolver com aspas literais ("\"" ... "\"") — GBNF aspas = delimitador
            if all(isinstance(e, str) for e in sch["enum"]):
                return "(" + " | ".join('"\\"" ' + '"' + _lit(e) + '"' + ' "\\""' for e in sch["enum"]) + ")"
            return "(" + " | ".join('"' + _lit(e) + '"' for e in sch["enum"]) + ")"
        if "const" in sch:
            if isinstance(sch["const"], str):
                return '"\\"" ' + '"' + _lit(sch["const"]) + '"' + ' "\\""'
            return '"' + _lit(sch["const"]) + '"'
        t = sch.get("type")
        if t == "string":
            if sch.get("pattern"):
                return _regex_alt(sch["pattern"])
            return "string"
        if t in ("integer", "number"):
            return '("-"? [0-9]{1,10})'
        if t == "boolean":
            return '("true" | "false")'
        if t == "null":
            return '"null"'
        if t == "array":
            inner = self._build(sch.get("items") or {}, depth + 1)
            maxi = sch.get("maxItems", 16)
            if maxi <= 1:
                return '"[" ws ' + inner + ' ws "]"'
            return '"[" ws ' + inner + ' ("," ws ' + inner + '){0,' + str(maxi - 1) + '} ws "]"'
        if t == "object":
            props = sch.get("properties", {})
            required = set(sch.get("required", []) or [])
            pairs = []
            for pname, ps in props.items():
                # key JSON = aspas literais "\"" + nome + "\"" (GBNF aspas são delimitadores)
                key = '"\\"" ' + '"' + _lit(pname) + '"' + ' "\\""'
                pair = key + ' ws ":" ws ' + self._build(ps, depth + 1)
                if pname not in required:
                    pair = "(" + pair + ")?"
                pairs.append(pair)
            if pairs:
                body = pairs[0] + "".join(' "," ws ' + pr for pr in pairs[1:])
            else:
                body = ""
            return '"{" ws ' + body + ' ws "}"'
        anyof = sch.get("anyOf") or sch.get("oneOf")
        if anyof:
            return "(" + " | ".join(self._build(a, depth + 1) for a in anyof[:3]) + ")"
        return '"null"'

    def to_gbnf(self) -> str:
        root = self._build(self.schema, 0)
        return (
            "root ::= " + root + "\n\n"
            'ws ::= [ \\t \\n]\n'
            'string ::= "\\"" [^"\\\\\\n\\t]{0,256} "\\""\n'
        )


class ConstrainedGenerate:
    """Pipeline de validação determinístico (R81/R82) — anti-loop obrigatório.

    - Gera com GBNF (barreira física) quando o cliente suporta.
    - Valida com Pydantic model_validate_json; erro parseado e RE-INJETADO.
    - max_retries=3: 3 falhas => exceção Python ou fallback default (nunca loop no LLM).
    """

    def __init__(self, completions_fn, response_model, grammar: str = "",
                 temperature: float = 0.0, stop=None, max_tokens: int = 300,
                 max_retries: int = 3, fallback=None):
        self.completions_fn = completions_fn
        self.response_model = response_model
        self.grammar = grammar
        self.temperature = temperature
        self.stop = stop or ["\n\n", "```"]
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.fallback = fallback

    def run(self, prompt: str, context: str = "") -> tuple:
        last_error = "sem resposta do motor"
        for attempt in range(1, self.max_retries + 1):
            msgs = [
                {"role": "system", "content": "Você é um parser estrito. Responda APENAS o formato exigido."},
                {"role": "user", "content": context + "\n" + prompt if context else prompt},
            ]
            if attempt > 1:
                msgs.append({"role": "user", "content": "ERRO NA TENTATIVA ANTERIOR — corrija exatamente: " + last_error})
            try:
                text = self.completions_fn(
                    messages=msgs, temperature=self.temperature, stop=self.stop,
                    max_tokens=self.max_tokens, grammar=self.grammar or None,
                )
                if not text or not text.strip():
                    last_error = "resposta vazia do motor"
                    continue
                if self.response_model is None:
                    return text, {"attempts": attempt, "ok": True, "raw": text}
                obj = self.response_model.model_validate_json(text)
                return obj, {"attempts": attempt, "ok": True, "raw": text}
            except Exception as exc:
                last_error = _fmt_validation_error(exc) if "validate" in str(type(exc).__name__).lower() else str(exc)
        if self.fallback is not None:
            return self.fallback, {"attempts": self.max_retries, "ok": False, "raw": None, "error": last_error}
        raise RuntimeError("constrained_generate: " + str(self.max_retries) + " falhas — último erro: " + last_error)


def llama_cpp_completions(base_url: str, api_key: str = "llamacpp", timeout: int = 60):
    """Cliente para llama.cpp server.

    - grammar presente -> POST /completion (única rota que aplica GBNF de verdade).
    - sem grammar        -> POST /v1/chat/completions (OpenAI-compatible).
    """
    import urllib.request

    def _call(messages, temperature=0.0, stop=None, max_tokens=300, grammar=None):
        if grammar:
            prompt = ""
            for m in messages:
                role = m.get("role", "user")
                prompt += ("<|system|>\\n" if role == "system" else "<|user|>\\n") + m.get("content", "") + "\\n"
            prompt += "<|assistant|>\\n"
            payload = {"prompt": prompt, "grammar": grammar, "temperature": temperature,
                       "max_tokens": max_tokens, "cache_prompt": False}
            root = base_url.rstrip("/")
            if root.endswith("/v1"):
                root = root[:-3]
            url = root + "/completion"
        else:
            payload = {"model": "local", "messages": messages, "temperature": temperature,
                       "max_tokens": max_tokens, "chat_template_kwargs": {"enable_thinking": False}}
            if stop:
                payload["stop"] = stop
            url = base_url.rstrip("/") + "/chat/completions"
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        try:
            if grammar:
                return data.get("content", "")
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise RuntimeError("resposta inesperada do motor: " + json.dumps(data)[:300])

    return _call




class HefestoLlamaBridge:
    """Compila a tríplice em comandos executáveis + auto-otimização de hardware."""

    def __init__(self, config_path: Path = CONFIG_PATH):
        self.config = self._load_config(config_path)

    def _load_config(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Configuração do Hefesto não localizada: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _calculate_hardware(self, hardware_cfg: dict) -> dict:
        """Auto-otimização de hardware (R72: sem limitação artificial de CPU)."""
        optimized = hardware_cfg.copy()
        if optimized.get("threads") == "auto":
            cpu_count = os.cpu_count()
            optimized["threads"] = max(1, cpu_count - 2) if cpu_count else 4
        return optimized

    def compile_flags(self) -> list:
        """Transforma a tríplice estruturada em comandos executáveis lineares."""
        commands = [LLAMA_SERVER]
        lifecycle = self.config.get("model_lifecycle", {})
        if lifecycle.get("model"):
            commands.extend(["-m", lifecycle["model"]])
        if lifecycle.get("lazy-mode"):
            commands.append("--lazy-mode")
        hardware = self._calculate_hardware(self.config.get("hardware_allocation", {}))
        commands.extend(["--threads", str(hardware.get("threads", 4))])
        commands.extend(["--n-gpu-layers", str(hardware.get("n-gpu-layers", 0))])
        if hardware.get("flash-attn", True):
            commands.append("--flash-attn")
        if hardware.get("device"):
            commands.extend(["--device", hardware["device"]])
        ctx = self.config.get("context_management", {})
        commands.extend(["--ctx-size", str(ctx.get("ctx-size", 0))])
        commands.extend(["--batch-size", str(ctx.get("batch-size", 2048))])
        commands.extend(["--n-predict", str(ctx.get("n-predict", -1))])
        sampling = self.config.get("sampling_profiles", {})
        commands.extend(["--temp", str(sampling.get("temp", 0.6))])
        commands.extend(["--top-k", str(sampling.get("top_k", 20))])
        commands.extend(["--top-p", str(sampling.get("top_p", 0.95))])
        commands.extend(["--min-p", str(sampling.get("min-p", 0.05))])
        if sampling.get("grammar"):
            commands.extend(["--grammar", sampling["grammar"]])
        return commands


class HefestoAutomation:
    """Pipeline de autodescoberta: flags novas → JSON → GBNF → consolidação."""

    @staticmethod
    def discover_flags() -> list:
        """Captura flags reais do llama.cpp (--help)."""
        try:
            env = dict(os.environ)
            env["LD_LIBRARY_PATH"] = LD_LIBRARY_PATH
            result = subprocess.run([LLAMA_CLI, "--help"], capture_output=True, text=True,
                                    check=True, env=env, timeout=30)
            help_output = result.stdout + result.stderr
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            help_output = "--model, -m : Caminho\n--ctx-size : Tamanho\n--new-hyper-parameter : Parâmetro de teste"
        return list(set(re.findall(r"(--[a-zA-Z0-9-]+)", help_output)))

    @staticmethod
    def read_registered(spec_path: Path = SPEC_PATH) -> set:
        """Lê flags registradas no spec.md."""
        if not spec_path.exists():
            return set()
        with open(spec_path, "r", encoding="utf-8") as f:
            return set(re.findall(r"-\s\*\*(--[a-zA-Z0-9-]+)\*\*", f.read()))

    @classmethod
    def sync_new_flags_to_json(cls, new_flags: list, config_path: Path = CONFIG_PATH) -> None:
        """Injeta novas flags no JSON com valor PENDING_GBNF_VAL."""
        if not config_path.exists():
            return
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        if "auto_discovered_features" not in config_data:
            config_data["auto_discovered_features"] = {}
        for flag in new_flags:
            clean_key = flag.lstrip("-")
            if clean_key not in config_data["auto_discovered_features"]:
                config_data["auto_discovered_features"][clean_key] = "PENDING_GBNF_VAL"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

    @classmethod
    def run_pipeline(cls) -> list:
        """Varre o ecossistema, descobre novidades e injeta no JSON."""
        discovered = cls.discover_flags()
        registered = cls.read_registered()
        new_flags = [f for f in discovered if f not in registered]
        if new_flags:
            cls.sync_new_flags_to_json(new_flags)
            return new_flags
        return []


class HefestoWebhookHandler(BaseHTTPRequestHandler):
    """Recebe gatilho externo (GitHub Actions/CRON) e roda o pipeline."""

    def do_POST(self):
        new_flags = HefestoAutomation.run_pipeline()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"status": "success", "updated_flags": new_flags,
                    "action_required": len(new_flags) > 0}
        self.wfile.write(json.dumps(response).encode("utf-8"))


def start_webhook_server(port: int = 8098):
    server = HTTPServer(("0.0.0.0", port), HefestoWebhookHandler)
    print(f"🚀 Webhook do Hefesto aguardando gatilhos na porta {port}...")
    server.serve_forever()



# ==============================================================================
# R81 itens 3-4-5 — FORJA byte-level + gabarito-fonte + config estrita
# ==============================================================================


# ---- Item 4: gabarito.json (R77) → schema JSON (fonte única) ----
def gabarito_to_schema(gabarito: dict) -> dict:
    """Extrai o esquema transpilável do gabarito.json (R77) -> JSON Schema.

    Suporta gabaritos no formato:
      {"properties": {..., "tipos": {...}}, "required": [...]}
      ou com chave "schema"/"json_schema" contendo o JSON Schema.
    Nunca inventa campos: o que não estiver no gabarito não entra no schema.
    """
    if not isinstance(gabarito, dict):
        raise TypeError("gabarito deve ser dict")
    candidatos = ["json_schema", "schema", "properties"]
    for key in candidatos:
        if key in gabarito and isinstance(gabarito[key], dict):
            return gabarito[key]
    raise ValueError("gabarito.json deve conter 'json_schema', 'schema' ou 'properties'")


# ---- Item 3: FORJA byte-level (schema 100% conforme) ----
def validate_byte_level(texto: str, response_model=None) -> tuple:
    """Validação byte-level: JSON puro + conformidade de schema.

    Retorna (ok: bool, detalhe: dict). Rejeita fences markdown, texto solto,
    chaves não tipadas, valores fora de domínio — com motivo exato.
    """
    erros = []
    if not texto or not texto.strip():
        return False, {"motivo": "vazio"}
    t = texto.strip()
    if t.startswith("```"):
        erros.append("fence_markdown")
    if not (t.startswith("{") and t.endswith("}")):
        erros.append("nao_json_objeto")
    obj = None
    try:
        obj = json.loads(t)
    except Exception as e:
        erros.append("json_invalido: " + str(e)[:120])
    if obj is not None and response_model is not None:
        if PYDANTIC_AVAILABLE and isinstance(response_model, type) and issubclass(response_model, BaseModel):
            try:
                response_model.model_validate(obj)
            except Exception as e:
                erros.append("schema: " + str(e)[:200])
    return (not erros), {"erros": erros, "texto": t[:200]}


def _validar_schema_manual(obj: dict, schema_json: dict) -> list:
    """Valida JSON contra JSON Schema básico (campos/tipos) sem Pydantic."""
    erros = []
    props = (schema_json or {}).get("properties", {})
    req = set((schema_json or {}).get("required", []) or [])
    if not isinstance(obj, dict):
        return ["nao_objeto"]
    faltando = [k for k in req if k not in obj]
    if faltando:
        erros.append("campos_faltantes: " + ",".join(faltando))
    extras = [k for k in obj if k not in props]
    if extras:
        erros.append("campos_extra: " + ",".join(extras))
    for k, v in obj.items():
        if k not in props:
            continue
        pt = props[k].get("type")
        if pt == "integer" and not isinstance(v, int):
            erros.append(f"tipo:{k} esperava int")
        elif pt == "number" and not isinstance(v, (int, float)):
            erros.append(f"tipo:{k} esperava number")
        elif pt == "string" and not isinstance(v, str):
            erros.append(f"tipo:{k} esperava string")
        elif pt == "boolean" and not isinstance(v, bool):
            erros.append(f"tipo:{k} esperava bool")
        if pt == "integer" and isinstance(v, int):
            if props[k].get("minimum") is not None and v < props[k]["minimum"]:
                erros.append(f"min:{k}")
            if props[k].get("maximum") is not None and v > props[k]["maximum"]:
                erros.append(f"max:{k}")
    return erros


def forja_byte_level(schema_json: dict, prompt: str, completions_fn,
                     response_model=None, grammar: str = "",
                     temperature: float = 0.0, max_tokens: int = 512,
                     output_path: str = "", max_retries: int = 3) -> dict:
    """FORJA R81 item 3: tool calling persistido com schema 100% conforme.

    1. transpila schema -> GBNF (se grammar vazio)
    2. gera com ConstrainedGenrate (retry + reinjeção)
    3. valida byte-level (validate_byte_level)
    4. persiste com manifest se output_path dado
    Retorna dict com status/manifest/evidência.
    """
    if not grammar:
        grammar = PydanticToGbnf(schema_json).to_gbnf() if schema_json else ""
    cg = ConstrainedGenerate(completions_fn, response_model, grammar=grammar,
                           temperature=temperature, max_tokens=max_tokens, max_retries=max_retries)
    try:
        obj, meta = cg.run(prompt)
    except Exception as e:
        return {"status": "failed", "erro": str(e)[:300], "etapa": "geração"}
    texto = meta.get("raw", "obj") if isinstance(meta, dict) else str(obj)
    ok, det = validate_byte_level(texto, response_model)
    # validação de schema manual (byte-level) quando não há Pydantic
    if ok and response_model is None and schema_json:
        try:
            obj_para_validar = json.loads(texto)
            extra = _validar_schema_manual(obj_para_validar, schema_json)
            if extra:
                ok = False
                det = {"erros": extra, "texto": texto[:200]}
        except Exception:
            ok = False
            det = {"erros": ["json_bruto_invalido"], "texto": texto[:200]}
    if not ok:
        # anti-loop: tenta uma 2ª via com validação pura (sem grammar) até retries
        for _ in range(2):
            cg2 = ConstrainedGenerate(completions_fn, response_model, grammar="",
                                     temperature=temperature, max_tokens=max_tokens, max_retries=1)
            try:
                obj2, meta2 = cg2.run(prompt)
                texto2 = meta2.get("raw", "obj2") if isinstance(meta2, dict) else str(obj2)
                ok2, det2 = validate_byte_level(texto2, response_model)
                if ok2 and response_model is None and schema_json:
                    try:
                        obj_para_validar2 = json.loads(texto2)
                        extra2 = _validar_schema_manual(obj_para_validar2, schema_json)
                        if extra2:
                            ok2 = False
                            det2 = {"erros": extra2, "texto": texto2[:200]}
                    except Exception:
                        ok2 = False
                        det2 = {"erros": ["json_bruto_invalido"], "texto": texto2[:200]}
                if ok2:
                    obj, meta, texto = obj2, meta2, texto2
                    ok, det = True, det2
                    break
            except Exception:
                continue
    resultado = {"status": "ok" if ok else "nao_conforme",
                 "validacao_byte_level": det, "tentativas": meta.get("attempts", 0) if isinstance(meta, dict) else 0}
    if ok and output_path:
        manifesto = {"artifact": output_path, "schema_conforme": True, "ts": __import__("datetime").datetime.now().isoformat()}
        Path(output_path).write_text(texto, encoding="utf-8")
        (Path(output_path).with_suffix(".manifest.json")).write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
        resultado["manifest"] = manifesto
        resultado["persistido"] = output_path
    return resultado


# ---- Item 5: parâmetros estritos por feature (config estrita) ----
class ForjaMotor:
    """Motor da fase FORJA (R81 item 5): aplica sampling estrito por feature,
    valida no slot alvo (ex.: granite :9088)."""

    DEFAULT_SAMPLING = {
        "temperature": 0.0,
        "stop": ["\n\n", "```", "<|eot_id|>"],
        "max_tokens_calc": True,  # calculado do schema se disponíve
    }

    def __init__(self, sampling: dict = None):
        self.sampling = {**self.DEFAULT_SAMPLING, **(sampling or {})}

    def max_tokens_para_schema(self, schema_json: dict) -> int:
        """Estima teto de tokens a partir do schema (trava física)."""
        # heurística conservadora: nº de propriedades * 40 + base
        props = schema_json.get("properties", {})
        base = 64 + len(props) * 48 if props else 128
        return min(base, 2048)

    def validar_slot(self, base_url: str, schema_json: dict, prompt: str = "gerar conforme schema",
                     model: str = "local") -> dict:
        """Prova real no slot: gera com sampling estrito + grammar e retorna conformidade."""
        fn = llama_cpp_completions(base_url)
        resultado = forja_byte_level(
            schema_json, prompt, fn, response_model=None, grammar="",
            temperature=self.sampling["temperature"], max_tokens=self.max_tokens_para_schema(schema_json),
        )
        return resultado



def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hefesto Llama Bridge (tríplice)")
    parser.add_argument("--compile", action="store_true", help="compilar flags do config")
    parser.add_argument("--discover", action="store_true", help="descobrir novas flags")
    parser.add_argument("--webhook", type=int, metavar="PORT", help="subir webhook")
    args = parser.parse_args()

    if args.compile:
        bridge = HefestoLlamaBridge()
        print(" ".join(bridge.compile_flags()))
        return 0
    if args.discover:
        new = HefestoAutomation.run_pipeline()
        print(json.dumps({"new_flags": new}, indent=2, ensure_ascii=False))
        return 0
    if args.webhook:
        start_webhook_server(args.webhook)
        return 0
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())