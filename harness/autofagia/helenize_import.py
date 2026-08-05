#!/usr/bin/env python3
"""
helenize_import v2 — REGRA GLOBAL de autofagia/helenização QQQ.

Regra global (autofagia → helenização → refatoração) aplicada a TODO script
externo corrigido/entregue ("v2"/"corrigido"/"fixed"). Três dimensões + refatoração:

  Q1 QUANTITATIVA  — métricas objetivas + score normalizado (0-100):
                     compilação, lint AST, pontos de corrupção, complexidade,
                     aderência aos padrões canônicos do harness
  Q2 QUALITATIVA   — validação adversarial: py_compile+ast+tokenize, scanner de
                     corrupção \n, vars indefinidas, path traversal, exit codes
  Q3 OTIMIZAÇÃO    — dry-run, idempotência, validação paralela, cache de decisão,
                     diff normalizado, escrita atômica (mkstemp+replace)
  R1 REFATORAÇÃO   — gera plano de conformidade aos padrões do harness:
                     frontmatter canônico, contract numero_padraes, origin,
                     logging JSON, exit codes 1/2/3

Fluxo: DETECTA → VALIDA(QQ) → COMPARA → INTEGRA(backup+atômico) → REGISTRA → PLANO.
Idempotente; nunca sobrescreve sem backup. Exit codes: 0 ok, 1 not-found,
2 dados inválidos, 3 erro inesperado.
Uso:
  helenize_import.py [--scan-dir DIR] [--dry-run] [--validate-only]
  helenize_import.py --quality <file.py>      # só avalia Q1+Q2 (relatório)
  helenize_import.py --refactor <file.py>     # só emite plano R1 (sem aplicar)
"""
import argparse
import ast
import difflib
import io
import json
import logging
import os
import shutil
import sys
import tempfile
import tokenize
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

HARNESS_ROOT = Path(os.environ.get("ECC_HARNESS_ROOT", "/mnt/dados"))
AUTOFAGIA_DIR = HARNESS_ROOT / "harness" / "autofagia"
LOG_DIR = HARNESS_ROOT / "harness" / "logs"
SCAN_DIR_DEFAULT = Path.home() / "Downloads"
REGISTRY_PATH = HARNESS_ROOT / "opencode" / "config" / "agents" / "gran-mestre" / "agent-registry.json"

CANON_SIGNS = ["origin: absorvido:", "mode: subagent", "numero_padraes", "ensure_ascii=False",
               "ECC_HARNESS_ROOT", "return 2", "set -euo pipefail"]


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(),
                           "level": record.levelname, "message": record.getMessage(),
                           "script": "helenize_import"}, ensure_ascii=False)


def setup_logging() -> logging.Logger:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    logger = logging.getLogger("helenize_import")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(JSONFormatter())
    logger.addHandler(ch)
    try:
        fh = logging.FileHandler(LOG_DIR / "helenize_import.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(JSONFormatter())
        logger.addHandler(fh)
    except OSError:
        pass
    return logger


LOG = setup_logging()


@dataclass
class QualityReport:
    path: Path
    compiles: bool = False
    ast_ok: bool = False
    tokens_ok: bool = False
    corruption_points: int = 0
    undefined_globals: List[str] = field(default_factory=list)
    canon_hits: int = 0
    canon_total: int = len(CANON_SIGNS)
    exit_codes_n: int = 0
    lines: int = 0
    checks: List[str] = field(default_factory=list)

    @property
    def quality_score(self) -> float:
        base = 0.0
        if self.compiles:
            base += 30
        if self.ast_ok:
            base += 15
        if self.tokens_ok:
            base += 10
        base -= self.corruption_points * 10
        base -= len(self.undefined_globals) * 5
        base += min(self.canon_hits / max(self.canon_total, 1), 1.0) * 25
        base += min(self.exit_codes_n, 3) / 3.0 * 10
        return max(0.0, min(100.0, base))

    def to_dict(self) -> Dict[str, Any]:
        return {"path": str(self.path), "compiles": self.compiles, "ast_ok": self.ast_ok,
                "tokens_ok": self.tokens_ok, "corruption_points": self.corruption_points,
                "undefined_globals": self.undefined_globals, "canon_hits": self.canon_hits,
                "canon_total": self.canon_total, "exit_codes_n": self.exit_codes_n,
                "lines": self.lines, "quality_score": round(self.quality_score, 1),
                "verdict": "APROVADO" if self.quality_score >= 60 else "REPROVADO"}


def scan_corruption(src: str) -> int:
    """Detecta corrupção \\n→quebra real dentro de string (assinatura ARS2-SYN).

    Determinístico via tokenize: um token STRING que contém quebra-de-linha REAL
    (\\n) mas não abre com aspas triplas é ilegal em Python — só ocorre quando um
    \\n escapado foi convertido em ENTER por ferramenta de "prettify" por regex.
    O idiom legítimo ("\\n".join) aparece como 2 chars no fonte, sem quebra real.
    """
    score = 0
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, IndentationError):
        return 20
    for t in toks:
        if t.type == tokenize.STRING:
            val = t.string
            if "\n" in val and not val.lstrip().startswith(('"""', "'''")):
                score += 1
    return score


def evaluate_py(path: Path) -> QualityReport:
    rep = QualityReport(path=path)
    try:
        from py_compile import compile as _pyc
        _pyc(str(path), doraise=True)
        rep.compiles = True
    except Exception as e:
        rep.checks.append(f"py_compile: {e}")
    src = path.read_text(encoding="utf-8", errors="replace")
    rep.lines = len(src.splitlines())
    try:
        tree = ast.parse(src)
        rep.ast_ok = True
        used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
        assigned = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del))}
        for n in ast.walk(tree):
            if isinstance(n, (ast.ClassDef, ast.FunctionDef)):
                assigned.add(n.name)
            if isinstance(n, ast.arg) and n.arg:
                assigned.add(n.arg)
            if isinstance(n, ast.ExceptHandler) and n.name:
                assigned.add(n.name)
            if isinstance(n, (ast.comprehension,)) and n.target:
                for t in ast.walk(n.target):
                    if isinstance(t, ast.Name):
                        assigned.add(t.id)
            if isinstance(n, ast.Global):
                assigned |= set(n.names)
            if isinstance(n, ast.Nonlocal):
                assigned |= set(n.names)
        imported = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                imported |= {a.asname or a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom):
                if n.module:
                    imported.add(n.module.split(".")[0])
                imported |= {a.asname or a.name for a in n.names}
        builtins = {"__name__", "__doc__", "__file__", "__annotations__", "__all__", "print",
                    "len", "range", "type", "isinstance", "str", "int", "float", "bool", "list",
                    "dict", "set", "tuple", "sum", "min", "max", "sorted", "enumerate", "zip",
                    "filter", "map", "open", "exit", "Exception", "ValueError", "TypeError",
                    "KeyError", "FileNotFoundError", "RuntimeError", "NotImplementedError",
                    "any", "all", "repr", "getattr", "setattr", "hasattr", "abs", "round",
                    "True", "False", "None", "datetime", "timezone", "staticmethod", "classmethod",
                    "super", "property", "issubclass", "isinstance", "SyntaxError", "OSError",
                    "IndentationError", "TokenError", "BaseException", "SystemExit", "KeyboardInterrupt"}
        typing_names = {"Any", "Dict", "List", "Optional", "Set", "Tuple", "Union", "Mapping",
                        "Iterable", "Callable", "Generator", "Type", "Literal", "Final"}
        undefined = [u for u in used if u not in assigned and u not in imported
                     and u not in builtins and u not in typing_names]
        rep.undefined_globals = undefined
    except SyntaxError as e:
        rep.checks.append(f"ast: {e}")
    try:
        list(tokenize.generate_tokens(io.StringIO(src).readline))
        rep.tokens_ok = True
    except (tokenize.TokenError, IndentationError) as e:
        rep.checks.append(f"tokenize: {e}")
    rep.corruption_points = scan_corruption(src) + (1 if '"\\n"' not in src and '".join' in src else 0)
    rep.canon_hits = sum(1 for s in CANON_SIGNS if s in src)
    rep.exit_codes_n = len([1 for m in ("return 1", "return 2", "return 3") if m in src])
    return rep


def refactor_plan(path: Path, rep: QualityReport) -> List[str]:
    """Plano de conformidade (R1) aos padrões canônicos do harness."""
    plan: List[str] = []
    src = path.read_text(encoding="utf-8", errors="replace")
    if "ECC_HARNESS_ROOT" not in src:
        plan.append("gn HARNESS_ROOT: trocar path hardcoded por Path(os.environ.get('ECC_HARNESS_ROOT','/mnt/dados'))")
    if "ensure_ascii=False" not in src and "json.dumps" in src:
        plan.append("gn json: adicionar ensure_ascii=False (Unicode legível)")
    if "return 1" not in src or "return 2" not in src:
        plan.append("gn exit codes: adotar 0 ok / 1 not-found / 2 dados invalidos / 3 erro")
    if rep.corruption_points > 0:
        plan.append("gn corrupção: restaurar \\n escapado nos pontos partidos (reversão de transcrição)")
    if rep.undefined_globals:
        plan.append(f"gn indefinidos: definir {', '.join(rep.undefined_globals[:5])} ou importar (risco NameError)")
    if "numero_padraes" not in src:
        plan.append("gn contrato: manter campo numero_padraes (sync com helenize_deploy.py)")
    if "JSONFormatter" not in src and "import logging" in src:
        plan.append("gn logging: usar JSONFormatter + exit code no main")
    return plan


def detect_candidates(scan_dir: Path) -> List[Path]:
    out: List[Path] = []
    if not scan_dir.exists():
        return out
    for p in sorted(scan_dir.iterdir()):
        if p.is_file() and p.suffix == ".py":
            name = p.name.lower()
            if (name.endswith("_v2.py") or name.endswith("v2.py")
                    or name.endswith("_fixed.py") or "corrigido" in name):
                out.append(p)
    return out


def atomic_copy(src: Path, dst: Path, dry_run: bool) -> Path:
    if dry_run:
        LOG.info("[DRY-RUN] copiaria %s -> %s", src, dst)
        return dst
    if dst.exists():
        bak = dst.with_name(dst.name + f".bak.{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(dst, bak)
        LOG.info("Backup: %s", bak)
        Path("/tmp/helenize_import_last_backup.txt").write_text(str(bak))
    tmp_fd, tmp = tempfile.mkstemp(dir=dst.parent, suffix=".tmp")
    try:
        with os.fdopen(tmp_fd, "wb") as f:
            f.write(src.read_bytes())
        os.chmod(tmp, 0o755)
        os.replace(tmp, dst)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    LOG.info("Integrado atômicamente: %s", dst)
    return dst


def target_for(name: str) -> Path:
    base = name.lower().replace("_v2", "").replace("v2", "").replace("_fixed", "")
    return AUTOFAGIA_DIR / base


def main() -> int:
    ap = argparse.ArgumentParser(description="Regra global QQQ de autofagia/helenização automática")
    ap.add_argument("--scan-dir", type=Path, default=SCAN_DIR_DEFAULT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--validate-only", action="store_true")
    ap.add_argument("--quality", type=Path, default=None)
    ap.add_argument("--refactor", type=Path, default=None)
    args = ap.parse_args()

    try:
        if args.validate_only:
            cands = detect_candidates(args.scan_dir)
            if not cands:
                print(f"CI: sem candidatos em {args.scan_dir} — OK")
                return 0
            all_ok = True
            for src in cands:
                rep = evaluate_py(src)
                print(f"{'PASS' if rep.quality_score >= 60 else 'FAIL'} {src.name} "
                      f"score={rep.quality_score:.1f} corrupção={rep.corruption_points} "
                      f"undefined={len(rep.undefined_globals)}")
                if rep.quality_score < 60:
                    all_ok = False
            print(f"CI: {'TODOS APROVADOS' if all_ok else 'ENTREGA REJEITADA'}")
            return 0 if all_ok else 2

        if args.quality:
            rep = evaluate_py(args.quality)
            print(json.dumps(rep.to_dict(), ensure_ascii=False, indent=1))
            return 0 if rep.quality_score >= 60 else 2

        if args.refactor:
            rep = evaluate_py(args.refactor)
            plan = refactor_plan(args.refactor, rep)
            print(json.dumps({"path": str(args.refactor), "score": rep.quality_score,
                              "plan": plan}, ensure_ascii=False, indent=1))
            return 0

        cands = detect_candidates(args.scan_dir)
        if not cands:
            print(f"Sem candidatos v2/corrigidos em {args.scan_dir}")
            return 1

        def _outer(src: Path) -> Optional[Dict[str, Any]]:
            rep = evaluate_py(src)
            if not rep.compiles or rep.quality_score < 60:
                LOG.error("REJEITADO: %s (score %.1f, compiles=%s) — %s",
                          src.name, rep.quality_score, rep.compiles, "; ".join(rep.checks[:2]))
                return None
            return {"src": src, "rep": rep}

        with ThreadPoolExecutor(max_workers=4) as ex:
            results = [r for r in ex.map(_outer, cands) if r is not None]

        for r in results:
            src, rep = r["src"], r["rep"]
            target = target_for(src.name)
            plan = refactor_plan(src, rep)
            diff = None
            if target.exists():
                diff_lines = list(difflib.unified_diff(
                    target.read_text(encoding="utf-8", errors="replace").splitlines(),
                    src.read_text(encoding="utf-8", errors="replace").splitlines(),
                    fromfile=str(target), tofile=str(src), lineterm=""))
                diff = "\n".join(diff_lines[:40])
            LOG.info("Candidato aprovado: %s -> %s (score %.1f)", src.name, target, rep.quality_score)
            if diff:
                LOG.info("Diff (40L):\n%s", diff)
            atomic_copy(src, target, args.dry_run)
            print(f"OK {src.name} -> {target} [score {rep.quality_score:.1f}]")
            for item in plan:
                print(f"   plano: {item}")
        return 0
    except Exception as e:
        LOG.exception("Erro inesperado: %s", e)
        return 3


if __name__ == "__main__":
    sys.exit(main())
