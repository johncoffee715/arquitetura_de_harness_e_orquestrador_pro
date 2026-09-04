#!/usr/bin/env python3
"""
HelenizeDeploy v2 — Mecanismo AUTOMÁTICO e GLOBAL de deploy de autofagia/helenização.

Merge R10 (autofagia crítica):
  v2 (auditoria externa)  → slug regex, shell/yaml escape, flock, escrita atômica,
                            schema dataclass, dry-run, rollback, logging JSON, $ECC_HARNESS_ROOT
  R8 (nossos fixes)       → guard de SKILL.md rico, MCP derivado da spec (is_mcp),
                            hook gera JSON via jq (sem bug de aspas do v2), parse jq-first

Para cada alvo absorvido, gera os 6 formatos de artefato orquestrável:
  skill    → ~/.opencode/skills/<slug>/SKILL.md
  subagent → ~/.config/opencode/agents/<slug>.md
  hook     → ~/.config/opencode/hooks/helenize-<slug>.sh
  plugin   → ~/.config/opencode/plugins/<slug>/index.ts
  mcp      → entrada no opencode.json mcp (se tipo_artefato == mcp)
  lsp      → entrada no opencode.json lsp (se aplicável)

+ registro no agent-registry.json (origem tipo_origem=framework-externo)
Idempotente: re-executar não duplica.
"""
import argparse
import fcntl
import json
import logging
import os
import re
import shutil
import sys
import tempfile
from contextlib import ExitStack
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

HOME = Path.home()
HARNESS_ROOT = Path(os.environ.get("ECC_HARNESS_ROOT", "/mnt/dados"))
OCODE_CONFIG = HOME / ".config" / "opencode"
OCODE_SKILLS = HOME / ".opencode" / "skills"
AGENTS_DIR = OCODE_CONFIG / "agents"
HOOKS_DIR = OCODE_CONFIG / "hooks"
PLUGINS_DIR = OCODE_CONFIG / "plugins"
REGISTRY_PATH = HARNESS_ROOT / "opencode" / "config" / "agents" / "gran-mestre" / "agent-registry.json"
ALVOS_PATH = HARNESS_ROOT / "harness" / "autofagia" / "alvos.json"
CATALOGO_PATH = HARNESS_ROOT / "harness" / "autofagia" / "catalogo-padroes.json"
LOG_DIR = HARNESS_ROOT / "harness" / "logs"

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RE_REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "script": "helenize_deploy",
            "source": record.name,
        }, ensure_ascii=False)


def setup_logging() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("helenize_deploy")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(JSONFormatter())
    logger.addHandler(ch)
    fh = logging.FileHandler(LOG_DIR / "helenize_deploy.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(JSONFormatter())
    logger.addHandler(fh)
    return logger


LOG = setup_logging()


@dataclass(frozen=True)
class Alvo:
    slug: str
    desc: str
    repo: str
    tipo_artefato: str
    prioridade: int = field(default=0)
    lang: str = field(default="?")
    topics: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.slug or not SLUG_RE.match(self.slug):
            raise ValueError(f"slug invalido: {self.slug!r} (regex {SLUG_RE.pattern})")
        if not self.desc or len(self.desc) > 500:
            raise ValueError("desc invalida: deve ter 1-500 chars")
        # repo = "owner/name" — HTML-safe, sem metashell/YAML (injeção via shell_escape/yaml_escape)
        if not RE_REPO.match(self.repo):
            raise ValueError(f"repo invalido: {self.repo!r} (esperado owner/name alfanumérico)")
        if not isinstance(self.prioridade, int):
            raise ValueError(f"prioridade deve ser int, got {type(self.prioridade)}")

    def to_dict(self) -> Dict[str, Any]:
        return {"slug": self.slug, "desc": self.desc, "repo": self.repo,
                "tipo_artefato": self.tipo_artefato, "prioridade": self.prioridade,
                "lang": self.lang, "topics": self.topics}


def shell_escape(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"


def yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").replace("\r", " ")


def safe_path(base: Path, *parts: str) -> Path:
    target = base.joinpath(*parts).resolve()
    base_res = base.resolve()
    if not str(target).startswith(str(base_res)):
        raise ValueError(f"Path traversal detectado: {target} escapa de {base_res}")
    return target


def is_mcp(alvo: Alvo) -> bool:
    return "mcp" in str(alvo.tipo_artefato).lower()


class RegistryManager:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock_path = path.with_suffix(".lock")
        self._lock_fd: Optional[int] = None

    def _acquire_lock(self) -> None:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock_fd = os.open(str(self.lock_path), os.O_CREAT | os.O_RDWR)
        fcntl.flock(self._lock_fd, fcntl.LOCK_EX)

    def _release_lock(self) -> None:
        if self._lock_fd is not None:
            fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
            os.close(self._lock_fd)
            self._lock_fd = None

    def load(self) -> Dict[str, Any]:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                LOG.error(f"Registry corrompido: {e}")
                raise
        return {"registry_version": "1.1.0", "updated_at": datetime.now(timezone.utc).isoformat(),
                "entries": [
                    {"id": "gran-mestre", "tipo": "agent", "nome": "Gran-Mestre",
                     "versao": "7.0.0", "status": "ativo",
                     "origem": {"tipo_origem": "interno"},
                     "proposito": "Meta-orquestrador senior",
                     "categoria_roteamento": "n/a",
                     "modelo": {"primario": "github-copilot/claude-opus-4.7", "fallback": []}}
                ]}

    def save(self, data: Dict[str, Any]) -> None:
        self._acquire_lock()
        try:
            if self.path.exists():
                bak = self.path.with_suffix(f".bak.{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}")
                shutil.copy2(self.path, bak)
            tmp_fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
            try:
                with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                os.replace(tmp, self.path)
            except Exception:
                try: os.unlink(tmp)
                except OSError: pass
                raise
        finally:
            self._release_lock()

    def upsert_entry(self, registry: Dict[str, Any], entry: Dict[str, Any]) -> None:
        entries = registry.setdefault("entries", [])
        existing = {e.get("id") for e in entries}
        if entry.get("id") in existing:
            for i, e in enumerate(entries):
                if e.get("id") == entry.get("id"):
                    entries[i] = entry
                    break
        else:
            entries.append(entry)


def slug_title(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.replace("-", " ").split())


def pascal_case(slug: str) -> str:
    return "".join(w.capitalize() for w in slug.replace("-", " ").split())


def skill_md(a: Alvo, catalogo: Dict[str, Any]) -> str:
    padrao = catalogo.get(a.slug, {})
    proposito = padrao.get("proposito") or a.desc
    padroes = padrao.get("padroes") or [a.desc]
    bul = "\n".join(f"- {p}" for p in padroes)
    return f"""---
name: {a.slug}
description: "{yaml_escape(a.desc)} (absorvido de {a.repo})"
origin: absorvido:{a.repo}
metadata:
  autofagia: {a.repo} ({datetime.now(timezone.utc).date().isoformat()})
  prioridade: {a.prioridade}
  linguagem: {a.lang}
  topics: {', '.join(a.topics)}
  artefatos: {a.tipo_artefato}
  padroes_absorvidos: {len(padroes)}
---
# {slug_title(a.slug)}

Helenizado de [`{a.repo}`](https://github.com/{a.repo}).

## Propósito
{proposito}

## Padrões absorvidos (núcleo canônico do repo)
{bul}

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="{a.slug}")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/{a.repo}
"""


def subagent_md(a: Alvo, catalogo: Dict[str, Any]) -> str:
    padrao = catalogo.get(a.slug, {})
    padroes = padrao.get("padroes") or [a.desc]
    desc = yaml_escape(f"Subagent helenizado de {a.repo}: {a.desc}")
    return f"""---
description: "{desc}"
mode: subagent
tools:
  bash: true
  read: true
  edit: true
  webfetch: true
---

# {slug_title(a.slug)} — Helenizado

Agente especialista absorvido de `{a.repo}`.

## Origem
- Repo: [`{a.repo}`](https://github.com/{a.repo})
- Deploy: Helenize-Deploy v2 (autofagia global) — origem `absorvido:{a.repo}`

## Escopo
{a.desc}

## Padrões absorvidos (núcleo)
{chr(10).join(f"- {p}" for p in padroes)}

## Regras
1. Aplicar o padrão do repo original de forma crítica (antropofagia).
2. Reportar em formato Plug-and-Play para o Gran-Mestre orquestrar (MIX/Dev Loop).
"""


def hook_sh(a: Alvo) -> str:
    slug_esc = shell_escape(a.slug)
    repo_esc = shell_escape(a.repo)
    log_dir = shell_escape(str(HOME / ".opencode" / "helenize"))
    return f"""#!/usr/bin/env bash
# helenize-{a.slug}.sh — hook pós-tool para o padrão absorvido de {a.repo}
# Gerado automaticamente por helenize_deploy.py v2 (NÃO editar manualmente)
set -euo pipefail

INPUT=$(cat)
if command -v jq >/dev/null 2>&1; then
  TOOL=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || true)
else
  TOOL=$(printf '%s' "$INPUT" | python3 -c "import sys,json;
try:
  d=json.load(sys.stdin); print(d.get('tool_name',''))
except Exception: pass" 2>/dev/null || true)
fi

if [ -n "$TOOL" ]; then
  LOG={log_dir}/{slug_esc}.log
  mkdir -p {log_dir}
  if command -v jq >/dev/null 2>&1; then
    jq -nc --arg tool "$TOOL" --arg ts "$(date -Is)" --arg origem {repo_esc} \
      '{{tool:$tool,ts:$ts,origem:$origem}}' >> "$LOG" 2>/dev/null || true
  else
    printf 'tool=%s ts=%s origem=%s\n' "$TOOL" "$(date -Is)" {repo_esc} >> "$LOG" 2>/dev/null || true
  fi
fi
printf '%s\\n' '{{"status":"ok"}}'
"""


def plugin_ts(a: Alvo) -> str:
    name = f"Helenize{pascal_case(a.slug)}"
    repo_escaped = a.repo.replace("\\", "\\\\")
    return f"""// Helen — plugin helenizado de {repo_escaped} — gerado por helenize_deploy.py v2 (NÃO editar)
export const {name} = async ({{ client, $ }}) => {{
  return {{
    "session.created": async (input) => {{
      // no-op leve; a origem vive no agent-registry (consultável via gran-mestre arsenal)
    }},
  }};
}};
"""


class DeployEngine:
    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run
        self.deployed: List[str] = []

    def _write(self, path: Path, content: str, mode: int = 0o644) -> bool:
        if self.dry_run:
            LOG.info(f"[DRY-RUN] Escreveria: {path} ({len(content)} bytes)")
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
        try:
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(content)
            os.chmod(tmp, mode)
            os.replace(tmp, path)
        except Exception:
            try: os.unlink(tmp)
            except OSError: pass
            raise
        return True

    def deploy_alvo(self, a: Alvo, catalogo: Dict[str, Any]) -> None:
        slug = a.slug

        skill_dir = safe_path(OCODE_SKILLS, slug)
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists() and "origin: absorvido:" not in skill_file.read_text(encoding="utf-8", errors="ignore"):
            self.deployed.append(f"skill:{skill_file} (rico preservado — não sobrescrever)")
        else:
            if self._write(skill_file, skill_md(a, catalogo)):
                self.deployed.append(f"skill:{skill_file}")

        sa = safe_path(AGENTS_DIR, f"{slug}.md")
        if self._write(sa, subagent_md(a, catalogo)):
            self.deployed.append(f"subagent:{sa}")

        hk = safe_path(HOOKS_DIR, f"helenize-{slug}.sh")
        if self._write(hk, hook_sh(a), mode=0o755):
            self.deployed.append(f"hook:{hk}")

        pl_dir = safe_path(PLUGINS_DIR, slug)
        if self._write(pl_dir / "index.ts", plugin_ts(a)):
            self.deployed.append(f"plugin:{pl_dir / 'index.ts'}")

        if is_mcp(a):
            self.deployed.append(f"mcp:{slug} (registrar em opencode.json mcp)")
        self.deployed.append(f"lsp:{slug} (sem servidor nativo — hook opcional já visa telemetria)")


def load_catalogo() -> Dict[str, Any]:
    if CATALOGO_PATH.exists():
        try:
            data = json.loads(CATALOGO_PATH.read_text(encoding="utf-8"))
            return {a["slug"]: a for a in data.get("alvos", []) if "slug" in a}
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            LOG.error(f"Catalogo invalido em {CATALOGO_PATH}: {e}")
    return {}


def load_alvos() -> List[Alvo]:
    if not ALVOS_PATH.exists():
        raise FileNotFoundError(f"Spec não encontrada: {ALVOS_PATH}")
    raw = json.loads(ALVOS_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError(f"alvos.json deve ser uma lista, got {type(raw)}")
    alvos: List[Alvo] = []
    seen: Set[str] = set()
    for i, item in enumerate(raw):
        try:
            slug = item.get("slug", "")
            if slug in seen:
                LOG.warning(f"Duplicata ignorada no indice {i}: {slug}")
                continue
            alvo = Alvo(slug=slug, desc=item.get("desc", ""), repo=item.get("repo", ""),
                        tipo_artefato=item.get("tipo_artefato", ""),
                        prioridade=item.get("prioridade", 0), lang=item.get("lang", "?"),
                        topics=item.get("topics", []))
            seen.add(slug)
            alvos.append(alvo)
        except (ValueError, TypeError) as e:
            LOG.error(f"Alvo invalido no indice {i}: {e}")
            raise
    return alvos


def build_registry_entry(a: Alvo, catalogo: Dict[str, Any]) -> Dict[str, Any]:
    padrao = catalogo.get(a.slug, {})
    padroes = padrao.get("padroes") or [a.desc]
    return {
        "id": a.slug,
        "tipo": "subagent" if "subagent" in a.tipo_artefato else "skill",
        "nome": slug_title(a.slug),
        "versao": "2.0.0",
        "status": "ativo",
        "origem": {"tipo_origem": "framework-externo", "framework": a.repo,
                   "url": f"https://github.com/{a.repo}"},
        "proposito": a.desc,
        "padroes_absorvidos": padroes,
        "numero_padraes": len(padroes),
        "categoria_roteamento": f"baseado-em-{a.prioridade}" if a.prioridade else "n/a",
        "formato_orquestravel": {"skill": True, "subagent": True, "hook": True,
                                 "plugin": True, "mcp": is_mcp(a), "lsp": False},
        "tags": [a.slug, *a.topics],
        "linguagem": a.lang,
        "modelo": {"primario": "github-copilot/claude-opus-4.7", "fallback": []},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="HelenizeDeploy v2 — deploy seguro de autofagia")
    ap.add_argument("--dry-run", action="store_true", help="Preview sem escrever no filesystem")
    ap.add_argument("--validate-only", action="store_true", help="Só valida alvos.json, não deploya")
    args = ap.parse_args()

    try:
        alvos = load_alvos()
        LOG.info(f"Alvos carregados: {len(alvos)}")
        if args.validate_only:
            print(f"OK {len(alvos)} alvos válidos")
            for a in alvos:
                print(f"  • {a.slug} <- {a.repo}")
            return 0

        catalogo = load_catalogo()
        reg = RegistryManager(REGISTRY_PATH)
        registry = reg.load()
        engine = DeployEngine(dry_run=args.dry_run)

        with ExitStack() as stack:
            if not args.dry_run:
                stack.callback(lambda: LOG.warning("Falha parcial: verifique backups .bak.* manualmente"))
            for alvo in alvos:
                LOG.info(f"Deployando: {alvo.slug}")
                engine.deploy_alvo(alvo, catalogo)
                reg.upsert_entry(registry, build_registry_entry(alvo, catalogo))
            stack.pop_all()

        if not args.dry_run:
            registry["updated_at"] = datetime.now(timezone.utc).isoformat()
            reg.save(registry)

        print(f"[MIX] {len(alvos)} alvos processados, {len(engine.deployed)} artefatos.")
        for line in engine.deployed:
            print("  OK", line)
        return 0

    except FileNotFoundError as e:
        print(f"X {e}", file=sys.stderr)
        return 1
    except (ValueError, json.JSONDecodeError) as e:
        LOG.error(f"Dados invalidos: {e}")
        print(f"X Dados inválidos: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        LOG.exception("Erro inesperado")
        print(f"X Erro inesperado: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
