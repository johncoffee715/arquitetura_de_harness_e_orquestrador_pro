#!/usr/bin/env python3
"""
arsenal v2 — Consulta rica do arsenal de autofagia/helenização (modo MIX).

REFATORAÇÕES CRÍTICAS (v1 → v2):
  • Paths via env var ECC_HARNESS_ROOT (portabilidade)
  • Tratamento de exceção em todas as operações I/O
  • Validação do output de integration.py antes de parsear JSON
  • Saída JSON com ensure_ascii=False (Unicode legível)
  • Lazy evaluation: só processa categorias necessárias
  • Códigos de retorno apropriados (0=sucesso, 1=erro, 2=dados inválidos)
  • Logging estruturado
  • Type hints completos
  • Filtro --pads funciona corretamente (pré-filtra, não pós-filtra)

PROTEGE A JANELA DE CONTEXTO DO ORQUESTRADOR:
  Em vez de ler READMEs/artefatos (100KB+), o orquestrador consulta este
  resumo de metadados — auto-descoberto, sem entrada do usuário.

Combina:
  - harness/registry.json   (auto-descoberta das 6 categorias: plugins, mcp,
    lsp, hooks, skills, subagents)
  - agent-registry.json       (metadados ricos dos alvos helenizados: padrões
    absorvidos, formato orquestrável, origem, tags)

Uso:
  gran-mestre arsenal                     → resumo global
  gran-mestre arsenal --cat skills|hooks  → 1 categoria
  gran-mestre arsenal --fresh             → reconstrói registry antes
  gran-mestre arsenal --json              → saída JSON (para automação)
  gran-mestre arsenal --pads              → só alvos com padrões absorvidos
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ── Configuração ──────────────────────────────────────────────────────────

HOME = Path.home()
HARNESS_ROOT = Path(os.environ.get("ECC_HARNESS_ROOT", "/mnt/dados"))
REGISTRY_PATH = HARNESS_ROOT / "harness" / "registry.json"
AGENT_REGISTRY_PATH = (
    HARNESS_ROOT / "opencode" / "config" / "agents" / "gran-mestre" / "agent-registry.json"
)
INTEGRATION_PY = HARNESS_ROOT / "harness" / "core" / "integration.py"
LOG_DIR = HARNESS_ROOT / "harness" / "logs"

CATS: List[str] = ["plugins", "mcp", "lsp", "hooks", "skills", "subagents"]

# ── Logging estruturado ───────────────────────────────────────────────────

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "script": "arsenal",
        }, ensure_ascii=False)


def setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("arsenal")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    file_handler = logging.FileHandler(LOG_DIR / "arsenal.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)

    return logger


LOG = setup_logging()

# ── Data classes ──────────────────────────────────────────────────────────

@dataclass
class HelenizedEntry:
    id: str
    framework: Optional[str]
    padroes: int
    formato: Dict[str, bool]
    tags: List[str]
    status: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "framework": self.framework,
            "padroes": self.padroes,
            "formato": self.formato,
            "tags": self.tags,
            "status": self.status,
        }


@dataclass
class ArsenalSummary:
    categories: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    helenizados: List[HelenizedEntry] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            **self.categories,
            "helenizados": [h.to_dict() for h in self.helenizados],
            "_meta": self.meta,
        }


# ── Registry Loader ───────────────────────────────────────────────────────

class RegistryLoader:
    def __init__(self, registry_path: Path, agent_registry_path: Path) -> None:
        self.registry_path = registry_path
        self.agent_registry_path = agent_registry_path

    def build_fresh(self) -> Dict[str, Any]:
        """Reconstrói registry via integration.py com validação rigorosa."""
        if not INTEGRATION_PY.exists():
            raise FileNotFoundError(f"integration.py não encontrado: {INTEGRATION_PY}")

        LOG.info(f"Reconstruindo registry via {INTEGRATION_PY}")
        result = subprocess.run(
            [sys.executable, str(INTEGRATION_PY), "registry"],
            capture_output=True,
            text=True,
            cwd=str(HARNESS_ROOT),
            check=False,
        )

        if result.returncode != 0:
            LOG.error(f"integration.py falhou: rc={result.returncode} stderr={result.stderr[:500]}")
            raise RuntimeError(f"integration.py falhou com rc={result.returncode}")

        if not result.stdout.strip():
            LOG.error("integration.py retornou stdout vazio")
            raise RuntimeError("integration.py retornou stdout vazio")

        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            LOG.error(f"integration.py retornou JSON inválido: {e}")
            raise RuntimeError(f"JSON inválido do integration.py: {e}")

        # Persiste com escrita atômica + lock (mesmo padrão do helenize_deploy — R10-predição c)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.registry_path.with_suffix(".lock")
        import fcntl
        fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            tmp_fd, tmp = tempfile.mkstemp(dir=self.registry_path.parent, suffix=".tmp")
            try:
                with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                os.replace(tmp, self.registry_path)
            except Exception:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
                raise
        finally:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
            except OSError:
                pass
            os.close(fd)
        LOG.info(f"Registry reconstruído e salvo atômicamente: {self.registry_path}")
        return data

    def load(self) -> Dict[str, Any]:
        if not self.registry_path.exists():
            LOG.info("Registry não existe, reconstruindo...")
            return self.build_fresh()

        try:
            text = self.registry_path.read_text(encoding="utf-8")
            return json.loads(text)
        except json.JSONDecodeError as e:
            LOG.error(f"Registry corrompido: {e}")
            raise RuntimeError(f"Registry corrompido em {self.registry_path}: {e}")
        except Exception as e:
            LOG.error(f"Erro lendo registry: {e}")
            raise

    def load_agent_meta(self) -> Dict[str, Any]:
        if not self.agent_registry_path.exists():
            LOG.warning(f"Agent registry não encontrado: {self.agent_registry_path}")
            return {}
        try:
            text = self.agent_registry_path.read_text(encoding="utf-8")
            return json.loads(text)
        except json.JSONDecodeError as e:
            LOG.error(f"Agent registry corrompido: {e}")
            return {}
        except Exception as e:
            LOG.error(f"Erro lendo agent registry: {e}")
            return {}


# ── Summarizer ────────────────────────────────────────────────────────────

class Summarizer:
    def __init__(self, registry: Dict[str, Any], agent_meta: Dict[str, Any]) -> None:
        self.registry = registry
        self.agent_meta = agent_meta

    def summarize(
        self,
        cat_filter: Optional[str] = None,
        only_with_pads: bool = False,
    ) -> ArsenalSummary:
        summary = ArsenalSummary()

        # Categorias (lazy: só processa a filtrada se especificado)
        # Registry pode vir int (contagem pós --fresh/integration.py) ou list (itens).
        cats_to_process = [cat_filter] if cat_filter else CATS
        for cat in cats_to_process:
            if cat is None:
                continue
            raw = self.registry.get(cat, [])
            if isinstance(raw, (int, float)):
                items: List[Any] = []
                total = int(raw)
            else:
                items = raw if isinstance(raw, list) else list(raw)
                total = len(items)
            summary.categories[cat] = {
                "total": total,
                "itens": items,
            }

        # Helenizados
        helenized: List[HelenizedEntry] = []
        for e in self.agent_meta.get("entries", []):
            origem = e.get("origem") or {}
            if origem.get("tipo_origem") != "framework-externo":
                continue

            num_padroes = e.get("numero_padraes", 0)
            if only_with_pads and num_padroes == 0:
                continue

            helenized.append(HelenizedEntry(
                id=e.get("id", "?"),
                framework=origem.get("framework"),
                padroes=num_padroes,
                formato=e.get("formato_orquestravel") or {},
                tags=(e.get("tags") or [])[:3],
                status=e.get("status"),
            ))

        summary.helenizados = helenized
        summary.meta = {
            "fonte_registry": str(REGISTRY_PATH),
            "fonte_agents": str(AGENT_REGISTRY_PATH),
            "total_helenizados": len(helenized),
            "total_artefatos_globais": sum(
                (int(v) if isinstance(v, (int, float)) else (len(v) if v else 0))
                for v in (self.registry.get(c) for c in CATS)
            ),
            "gerado_em": datetime.now(timezone.utc).isoformat(),
        }
        return summary


# ── Formatter ─────────────────────────────────────────────────────────────

class Formatter:
    @staticmethod
    def format_json(summary: ArsenalSummary) -> str:
        return json.dumps(summary.to_dict(), ensure_ascii=False, indent=1)

    @staticmethod
    def format_pretty(summary: ArsenalSummary, cat_filter: Optional[str] = None) -> str:
        lines: List[str] = []
        m = summary.meta
        lines.append("═══ ARSENAL v2 — Metadados de Orquestração (protege janela de contexto) ═══")
        lines.append(f"Registry: {m['fonte_registry']}")
        lines.append(f"Agent Registry: {m['fonte_agents']}")
        lines.append(f"Gerado: {m['gerado_em']}")
        lines.append(f"TOTAL artefatos (6 cat): {m['total_artefatos_globais']} | Helenizados: {m['total_helenizados']}\n")

        if cat_filter:
            items = summary.categories.get(cat_filter, {}).get("itens", [])
            lines.append(f"┌─ {cat_filter.upper()} ({len(items)})")
            for it in items:
                nome = it.get("name") or it.get("id") or it.get("path") or str(it)[:60]
                nome = nome.replace(str(HOME), "~") if nome else "?"
                lines.append(f"│   • {nome}")
            lines.append("└")
            return "\n".join(lines)

        for cat in CATS:
            cat_data = summary.categories.get(cat, {})
            total = cat_data.get("total", 0)
            lines.append(f"▸ {cat:<12} {total}")
            if total and cat in ("skills", "subagents", "hooks", "plugins"):
                names = []
                for it in cat_data.get("itens", [])[:8]:
                    n = it.get("name") or it.get("id") or ""
                    n = n.replace(str(HOME), "~") if n else "?"
                    names.append(n)
                lines.append(f"    exemplos: {', '.join(names)}{'…' if total > 8 else ''}")

        lines.append("\n▸ HELENIZADOS (framework-externo, orquestráveis):")
        for h in summary.helenizados:
            f = h.formato
            fm = (
                f"{'S' if f.get('skill') else '.'}"
                f"{'A' if f.get('subagent') else '.'}"
                f"{'H' if f.get('hook') else '.'}"
                f"{'P' if f.get('plugin') else '.'}"
                f"{'M' if f.get('mcp') else '.'}"
                f"{'L' if f.get('lsp') else '.'}"
            )
            lines.append(
                f"    '{h.id}' ← {h.framework or '?'}  "
                f"padrões:{h.padroes}  [{fm}]  {h.status or '?'}")

        return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(
        prog="gran-mestre arsenal",
        description="Consulta rica do arsenal de autofagia/helenização (modo MIX).",
    )
    ap.add_argument("--cat", choices=CATS, help="filtrar por categoria")
    ap.add_argument("--fresh", action="store_true", help="reconstruir registry antes")
    ap.add_argument("--json", action="store_true", help="saída JSON completa")
    ap.add_argument("--pads", action="store_true", help="mostrar só alvos com padrões")
    args = ap.parse_args()

    try:
        loader = RegistryLoader(REGISTRY_PATH, AGENT_REGISTRY_PATH)
        registry = loader.build_fresh() if args.fresh else loader.load()
        agent_meta = loader.load_agent_meta()

        summarizer = Summarizer(registry, agent_meta)
        summary = summarizer.summarize(
            cat_filter=args.cat,
            only_with_pads=args.pads,
        )

        if args.json:
            print(Formatter.format_json(summary))
        else:
            print(Formatter.format_pretty(summary, cat_filter=args.cat))

        return 0

    except FileNotFoundError as e:
        LOG.error(str(e))
        print(f"✗ Arquivo não encontrado: {e}", file=sys.stderr)
        return 1
    except (RuntimeError, json.JSONDecodeError) as e:
        LOG.error(f"Dados inválidos: {e}")
        print(f"✗ Dados inválidos: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        LOG.exception("Erro inesperado")
        print(f"✗ Erro inesperado: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
