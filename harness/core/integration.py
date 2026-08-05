#!/usr/bin/env python3
"""
Integration Manager v2 — Gran-Mestre Hybrid Harness

Catalogação automática das 6 categorias do registro para escolha automática
por task pelo orquestrador (Ornith):

    plugins | mcp | lsp | hooks | skills | subagents

Refatoração de autofagia/helenização (2026-07-31):
- Registro separado por categorias (spec: Orquestrador Profissional §1.4,
  engenharia de harness §1 "O Meta Orquestrador e todo o harness sao modular")
- Seleção automática de recursos por task (tags + descrição)
- Orquestrador (Ornith) consulta o registro via ModelProvider → integração
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class IntegrationManager:
    """Manages integration with OpenCode ecosystem (registry v2 — 6 categorias)."""

    # Categorias do registro (ordem = prioridade de consulta do orquestrador)
    CATEGORIES = ["plugins", "mcp", "lsp", "hooks", "skills", "subagents"]

    # BM25 lexical (padrão ratel/context-selector — R9): sem dependência externa.
    # k1=0.9, b=0.4 (descrições curtas → saturação rápida de TF, moins peso em len).
    _BM25_K1 = 0.9
    _BM25_B = 0.4

    def _bm25_score(self, query_terms, doc_tokens, doc_len, avg_dl, n_docs, df):
        """BM25 puro sobre tokens do documento (idf com suavização).
        query_terms: dict {term: freq_no_query}; df: dict {term: n_docs_contendo}.
        Retorna score float.
        """
        import math
        score = 0.0
        for term, qf in query_terms.items():
            tf = doc_tokens.get(term, 0)
            if tf == 0:
                continue
            idf = math.log(1 + (n_docs - df.get(term, 0) + 0.5) / (df.get(term, 0) + 0.5))
            denom = tf + self._BM25_K1 * (1 - self._BM25_B + self._BM25_B * doc_len / max(avg_dl, 1))
            score += idf * (tf * (self._BM25_K1 + 1)) / max(denom, 1e-9)
        return score

    def _tokenize(self, text: str):
        import re as _re
        return _re.findall(r"[a-z0-9]{2,}", text.lower())

    def _rank_bm25(self, query: str, docs):
        """Ranks docs (list of {'text': str, 'item': dict}) por BM25. Retorna itens ordenados."""
        import re as _re
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return [d["item"] for d in docs]
        query_terms = {t: q_tokens.count(t) for t in set(q_tokens)}
        doc_tokens_list = [self._tokenize(d["text"]) for d in docs]
        df = {}
        n = len(doc_tokens_list)
        for toks in doc_tokens_list:
            for t in set(toks):
                df[t] = df.get(t, 0) + 1
        avg_dl = sum(len(t) for t in doc_tokens_list) / max(n, 1)
        scored = []
        for d, toks in zip(docs, doc_tokens_list):
            freq = {}
            for t in toks:
                freq[t] = freq.get(t, 0) + 1
            s = self._bm25_score(query_terms, freq, len(toks), avg_dl, n, df)
            scored.append((s, d["item"]))
        scored.sort(key=lambda x: -x[0])
        return [item for s, item in scored if s > 0 or True][:max(len(docs), 0)]

    def __init__(self, project_root: str = "/mnt/dados"):
        self.project_root = Path(project_root)
        self.home_config = Path.home() / ".config" / "opencode"
        self.opencode_dir = self.project_root / "opencode"
        self.skills_dir = self.opencode_dir / "skills"
        self.agents_dir = self.project_root / "opencode" / "config" / "agents"
        self.commands_dir = self.opencode_dir / "commands"

        # Fontes por categoria
        self.skill_sources = [
            self.skills_dir,
            self.opencode_dir / "config" / "opencode" / "skills",
            self.home_config / "skills",
            Path("/home/johncoffee/.opencode/skills"),
            Path("/home/johncoffee/.claude/skills"),
        ]
        self.agent_sources = [
            self.agents_dir,
            self.home_config / "agents",
            Path("/home/johncoffee/.opencode/agents"),
        ]
        self.plugin_sources = [
            self.home_config / "plugins",
            self.opencode_dir / "plugins",
            self.opencode_dir / "config" / "plugins",
        ]
        self.hook_sources = [
            self.home_config / "hooks",
            self.opencode_dir / "hooks",
        ]
        self.lsp_sources = [
            self.home_config / "lsp.json",
            self.opencode_dir / "lsp.json",
            self.home_config / "opencode.json",
        ]
        self.mcp_sources = [
            self.home_config / "opencode.json",
            self.opencode_dir / "opencode.json",
            self.project_root / "opencode" / "opencode.json",
        ]

    # ────────────────────────────────────────────────────────────────
    # PLUGINS
    # ────────────────────────────────────────────────────────────────
    def discover_plugins(self) -> List[Dict[str, Any]]:
        """Descobre plugins (dirs com package.json/index.ts ou entradas no config)."""
        plugins: List[Dict[str, Any]] = []
        seen = set()

        for src in self.plugin_sources:
            if not src.exists():
                continue
            if src.is_file() and src.suffix == ".json":
                self._parse_plugin_config(src, plugins, seen)
            elif src.is_dir():
                for entry in sorted(src.iterdir()):
                    if entry.is_dir():
                        pkg = entry / "package.json"
                        if pkg.exists():
                            try:
                                meta = json.loads(pkg.read_text())
                            except Exception:
                                meta = {}
                            plugins.append({
                                "name": meta.get("name", entry.name),
                                "description": meta.get("description", ""),
                                "version": meta.get("version", "0.0.0"),
                                "path": str(entry),
                                "source": str(src),
                                "type": "package"
                            })
                            seen.add(entry.name)
                    elif entry.suffix == ".ts" or entry.suffix == ".js":
                        plugins.append({
                            "name": entry.stem,
                            "description": "plugin script",
                            "version": "0.0.0",
                            "path": str(entry),
                            "source": str(src),
                            "type": "script"
                        })
                        seen.add(entry.stem)

        # plugin do config (oh-my-openagent@latest etc)
        cfg = self._load_json(self.home_config / "opencode.json")
        if cfg:
            for p in cfg.get("plugin", []):
                if isinstance(p, str) and p not in seen:
                    plugins.append({
                        "name": p,
                        "description": "plugin (config)",
                        "version": "latest",
                        "path": "",
                        "source": "opencode.json",
                        "type": "config"
                    })
        return plugins

    def _parse_plugin_config(self, path: Path, out: List[Dict], seen: set) -> None:
        cfg = self._load_json(path)
        if not cfg:
            return
        for p in cfg.get("plugin", []):
            if isinstance(p, str) and p not in seen:
                out.append({
                    "name": p, "description": "plugin (config)",
                    "version": "latest", "path": str(path),
                    "source": str(path), "type": "config"
                })
                seen.add(p)

    # ────────────────────────────────────────────────────────────────
    # MCP SERVERS
    # ────────────────────────────────────────────────────────────────
    def discover_mcp(self) -> List[Dict[str, Any]]:
        """Descobre MCP servers (opencode.json mcp section)."""
        servers: List[Dict[str, Any]] = []
        seen = set()

        for src in self.mcp_sources:
            cfg = self._load_json(src)
            if not cfg:
                continue
            mcp = cfg.get("mcp", {})
            for name, spec in mcp.items():
                if name in seen:
                    continue
                seen.add(name)
                if isinstance(spec, dict):
                    servers.append({
                        "name": name,
                        "type": spec.get("type", "local"),
                        "url": spec.get("url", ""),
                        "command": spec.get("command", ""),
                        "enabled": spec.get("enabled", True),
                        "timeout": spec.get("timeout", 0),
                        "path": str(src),
                        "description": f"MCP server: {name}"
                    })
                else:
                    servers.append({
                        "name": name, "type": "local",
                        "command": str(spec), "enabled": True,
                        "path": str(src), "description": f"MCP server: {name}"
                    })
        return servers

    # ────────────────────────────────────────────────────────────────
    # LSP SERVERS
    # ────────────────────────────────────────────────────────────────
    def discover_lsp(self) -> List[Dict[str, Any]]:
        """Descobre LSP servers (lsp.json, opencode.json lsp, .codex/lsp-client.json)."""
        servers: List[Dict[str, Any]] = []
        seen = set()
        candidates = list(self.lsp_sources) + [
            self.project_root / ".opencode" / "lsp.json",
            self.project_root / ".codex" / "lsp-client.json",
            Path.home() / ".codex" / "lsp-client.json",
            self.home_config / "lsp-client.json",
        ]

        for src in candidates:
            if not src.exists():
                continue
            cfg = self._load_json(src)
            if not cfg:
                continue
            # opencode.json lsp section
            lsp = cfg.get("lsp", {}) if isinstance(cfg, dict) else {}
            if isinstance(lsp, dict):
                for lang, spec in lsp.items():
                    key = f"{lang}:{src}"
                    if key in seen:
                        continue
                    seen.add(key)
                    servers.append({
                        "name": lang,
                        "language": lang,
                        "command": spec.get("command", "") if isinstance(spec, dict) else str(spec),
                        "enabled": spec.get("enabled", True) if isinstance(spec, dict) else True,
                        "path": str(src),
                        "description": f"LSP server: {lang}"
                    })

            # lsp-client.json format (codex style)
            for lang_key in ("languages", "servers"):
                section = cfg.get(lang_key, {}) if isinstance(cfg, dict) else {}
                if isinstance(section, dict):
                    for lang, spec in section.items():
                        key = f"{lang}:{src}"
                        if key in seen:
                            continue
                        seen.add(key)
                        servers.append({
                            "name": lang,
                            "language": lang,
                            "command": json.dumps(spec) if not isinstance(spec, str) else spec,
                            "enabled": True,
                            "path": str(src),
                            "description": f"LSP server: {lang}"
                        })

        lsp_binaries = {
            "rust": "rust-analyzer",
            "c/c++": "clangd",
            "python": "pyright",
            "python-alt": "basedpyright",
            "typescript": "typescript-language-server",
            "go": "gopls",
            "lua": "lua-language-server",
            "python-legacy": "pylsp",
        }
        for lang, binary in lsp_binaries.items():
            key = f"bin:{lang}"
            if key in seen:
                continue
            bin_path = self._which(binary)
            if bin_path:
                seen.add(key)
                servers.append({
                    "name": lang,
                    "language": lang,
                    "command": bin_path,
                    "enabled": True,
                    "path": bin_path,
                    "detected": "binary",
                    "description": f"LSP server: {lang} ({binary})"
                })
        return servers

    @staticmethod
    def _which(binary: str) -> Optional[str]:
        import shutil
        return shutil.which(binary)

    # ────────────────────────────────────────────────────────────────
    # HOOKS
    # ────────────────────────────────────────────────────────────────
    def discover_hooks(self) -> List[Dict[str, Any]]:
        """Descobre hooks (dirs de hooks — .js/.ts/.sh)."""
        hooks: List[Dict[str, Any]] = []
        seen = set()

        for src in self.hook_sources:
            if not src.is_dir():
                continue
            for entry in sorted(src.iterdir()):
                if entry.is_file() and entry.suffix in (".js", ".ts", ".sh", ".cjs", ".mjs"):
                    if entry.name in seen:
                        continue
                    seen.add(entry.name)
                    hooks.append({
                        "name": entry.stem,
                        "filename": entry.name,
                        "type": entry.suffix.lstrip("."),
                        "path": str(entry),
                        "source": str(src),
                        "description": f"Hook: {entry.stem}"
                    })
        return hooks

    # ────────────────────────────────────────────────────────────────
    # SKILLS
    # ────────────────────────────────────────────────────────────────
    def discover_skills(self) -> List[Dict[str, Any]]:
        """Descobre todas as skills (SKILL.md) em todas as fontes."""
        skills = []
        seen = set()

        for src in self.skill_sources:
            if not src.is_dir():
                continue
            for skill_dir in sorted(src.iterdir()):
                if not skill_dir.is_dir():
                    continue
                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    # procura em subdir (gran-mestre/SKILL.md)
                    nested = list(skill_dir.glob("*/SKILL.md"))
                    if nested:
                        skill_md = nested[0]
                    else:
                        continue
                name = skill_md.parent.name
                if name in seen:
                    continue
                seen.add(name)
                info = self._parse_skill_md(skill_md)
                info["path"] = str(skill_md.parent)
                info["source"] = str(src).split("/")[-2] if len(str(src).split("/")) > 1 else "local"
                skills.append(info)
        return skills

    def _parse_skill_md(self, skill_md_path: Path) -> Dict[str, Any]:
        """Parse SKILL.md frontmatter para metadados."""
        try:
            content = skill_md_path.read_text(errors="replace")
        except Exception:
            return {"name": skill_md_path.parent.name, "description": ""}

        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        metadata = {}
        if frontmatter_match:
            for line in frontmatter_match.group(1).split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if value:
                        metadata[key] = value

        name = skill_md_path.parent.name
        desc = metadata.get("description", "")
        return {
            "name": metadata.get("name", name),
            "description": desc,
            "model": metadata.get("model", ""),
            "mode": metadata.get("mode", ""),
            "origin": metadata.get("origin", ""),
            "category": metadata.get("category", ""),
            "version": metadata.get("version", ""),
            "tags": [t.strip() for t in metadata.get("tags", "").split(",") if t.strip()],
            "path": str(skill_md_path.parent)
        }

    # ────────────────────────────────────────────────────────────────
    # SUBAGENTS
    # ────────────────────────────────────────────────────────────────
    def discover_subagents(self) -> List[Dict[str, Any]]:
        """Descobre subagents (agents .md/.json em todas as fontes)."""
        agents = []
        seen = set()

        for src in self.agent_sources:
            if not src.exists():
                continue
            files = []
            if src.is_dir():
                files = sorted(src.glob("*.md")) + sorted(src.glob("*.json"))
            elif src.is_file():
                files = [src]
            for agent_file in files:
                name = agent_file.stem
                if name in seen:
                    continue
                seen.add(name)
                info = self._parse_agent_md(agent_file)
                info["path"] = str(agent_file)
                info["source"] = "home" if "johncoffee" in str(src) else "local"
                agents.append(info)
        return agents

    def _parse_agent_md(self, agent_md_path: Path) -> Dict[str, Any]:
        """Parse agent file (frontmatter ou JSON) para metadados."""
        try:
            content = agent_md_path.read_text(errors="replace")
        except Exception:
            return {"name": agent_md_path.stem, "description": ""}

        # JSON agent
        if agent_md_path.suffix == ".json":
            try:
                data = json.loads(content)
                return {
                    "name": data.get("name", agent_md_path.stem),
                    "description": data.get("description", ""),
                    "model": data.get("model", ""),
                    "mode": data.get("mode", ""),
                    "tools": data.get("tools", []),
                    "path": str(agent_md_path)
                }
            except Exception:
                pass

        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        metadata = {}
        if frontmatter_match:
            for line in frontmatter_match.group(1).split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if value:
                        metadata[key] = value

        name = agent_md_path.stem
        return {
            "name": metadata.get("name", name),
            "description": metadata.get("description", ""),
            "model": metadata.get("model", ""),
            "mode": metadata.get("mode", ""),
            "origin": metadata.get("origin", ""),
            "max_cycles": metadata.get("max_cycles", "3"),
            "path": str(agent_md_path)
        }

    # ────────────────────────────────────────────────────────────────
    # COMMANDS (compat)
    # ────────────────────────────────────────────────────────────────
    def discover_commands(self) -> List[Dict[str, Any]]:
        """Descobre comandos (compat — usado pelo registry v1)."""
        commands = []
        if self.commands_dir.exists():
            for cmd_file in sorted(self.commands_dir.glob("*.md")):
                commands.append({
                    "name": cmd_file.stem,
                    "path": str(cmd_file),
                    "source": "local"
                })
        return commands

    # ────────────────────────────────────────────────────────────────
    # REGISTRY v2 (6 categorias)
    # ────────────────────────────────────────────────────────────────
    def build_registry(self) -> Dict[str, Any]:
        """Build the global registry — 6 categorias separadas."""
        registry = {
            "plugins": self.discover_plugins(),
            "mcp": self.discover_mcp(),
            "lsp": self.discover_lsp(),
            "hooks": self.discover_hooks(),
            "skills": self.discover_skills(),
            "subagents": self.discover_subagents(),
            "commands": self.discover_commands(),  # compat
            "timestamp": datetime.now().isoformat(),
            "schema_version": "2.0",
            "categorias": self.CATEGORIES,
        }

        registry_path = self.project_root / "harness" / "registry.json"
        with open(registry_path, "w") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)

        print(f"[Integration] Registry v2 built: {registry_path}", file=sys.stderr)
        for cat in self.CATEGORIES:
            print(f"[Integration]   {cat}: {len(registry.get(cat, []))}", file=sys.stderr)
        return registry

    # ────────────────────────────────────────────────────────────────
    # APRENDIZADO ADAPTATIVO (orquestrador estuda por task)
    # ────────────────────────────────────────────────────────────────
    DECISION_LOG = "harness/decision-log.jsonl"

    def _decision_path(self) -> Path:
        return self.project_root / self.DECISION_LOG

    def record_decision(self, task: str, phase: str, selections: Dict[str, list],
                        outcome: str = "pending", feedback: str = "") -> None:
        """Registra a decisão do orquestrador + feedback (outcome: pending|success|fail)."""
        path = self._decision_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "phase": phase,
            "selections": {
                cat: [item.get("name", "") for item in items]
                for cat, items in selections.items()
            },
            "outcome": outcome,
            "feedback": feedback,
        }
        with open(path, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        if outcome != "pending":
            self._update_scores(entry)

    def _update_scores(self, entry: Dict[str, Any]) -> None:
        return

    def _scores_from_log(self) -> Dict[str, float]:
        """Scores derivados do decision-log — fonte de verdade idempotente.

        build_registry() re-descobre recursos a cada chamada e sobrescreve
        registry.json, então o score NÃO pode viver lá — é computado do log.
        """
        path = self._decision_path()
        if not path.exists():
            return {}
        scores: Dict[str, float] = {}
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            delta = 1.0 if entry.get("outcome") == "success" else -1.0
            if entry.get("outcome") not in ("success", "fail"):
                continue
            for cat, names in entry.get("selections", {}).items():
                for name in names:
                    key = f"{cat}:{name}"
                    scores[key] = scores.get(key, 0) + delta
        return scores

    def get_decision_history(self, task: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        path = self._decision_path()
        if not path.exists():
            return []
        history = []
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue
            if not task or task.lower() in entry.get("task", "").lower():
                history.append(entry)
        return history[-limit:]

    # ────────────────────────────────────────────────────────────────
    # SELEÇÃO AUTOMÁTICA POR TASK (orquestrador)
    # ────────────────────────────────────────────────────────────────
    def select_for_task(self, task: str, phase: str = "", top_k: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """Seleciona recursos do registro por task — escolha automática do orquestrador.

        Matching: tags da skill + palavras-chave na descrição vs termos da task.
        Retorna: {categoria: [recursos rankeados]}
        """
        registry = self.build_registry()
        task_lower = task.lower()
        task_terms = set(re.findall(r'[a-z0-9]{3,}', task_lower))

        STOPWORDS = {
            "para", "com", "por", "uma", "um", "dos", "das", "que", "aplicar",
            "the", "and", "for", "with", "from", "this", "that", "using",
            "harness", "task", "fase", "phase", "usar", "sobre", "como",
        }
        task_terms -= STOPWORDS

        # Palavras-chave de fase → categorias prioritárias
        phase_boost = {
            "discovery": {"skills": 1, "subagents": 1, "mcp": 1},
            "contract": {"skills": 1, "subagents": 1},
            "plan": {"skills": 1, "subagents": 1, "lsp": 1},
            "execute": {"subagents": 2, "plugins": 1, "lsp": 1, "hooks": 1},
            "review": {"subagents": 1, "skills": 1, "mcp": 1},
            "deliver": {"hooks": 1, "mcp": 1},
        }
        boosts = phase_boost.get(phase.lower(), {})
        learned = self._scores_from_log()

        # Sinônimos pt/en — task em português casa com recursos descritos em inglês
        SYNONYMS = {
            "validar": "validate", "valida": "validate", "validacao": "validation",
            "seguranca": "security", "segurança": "security", "politicas": "policy",
            "políticas": "policy", "codigo": "code", "código": "code",
            "revisar": "review", "revisa": "review", "revisao": "review", "revisão": "review",
            "testar": "test", "teste": "test", "depurar": "debug", "debug": "debug",
            "deploy": "deploy", "publicar": "publish", "implantar": "deploy",
            "autenticacao": "auth", "autenticação": "auth", "usuario": "user", "usuário": "user",
            "permissao": "permission", "permissão": "permission", "criptografia": "encryption",
            "senha": "password", "injetar": "injection", "injection": "injection",
            "vulnerabilidade": "vulnerability", "sintaxe": "syntax", "compilar": "compile",
            "executar": "run", "executa": "run", "processar": "process", "processa": "process",
            "gerar": "generate", "gera": "generate", "imagem": "image", "documento": "document",
            "traduzir": "translate", "traduz": "translate", "resumir": "summarize",
            "resumo": "summary", "resume": "summarize", "log": "log", "relatorio": "report",
            "relatório": "report", "monitorar": "monitor", "monitora": "monitor",
            "deploy": "deployment", "integra": "integration", "integrar": "integration",
            "design": "design", "audio": "audio", "áudio": "audio", "som": "sound",
            "estetica": "aesthetic", "estética": "aesthetic", "estilo": "style",
            "layout": "layout", "ui": "interface", "visual": "visual", "design visual": "visual design",
            "feedback": "feedback", "transcricao": "transcript", "transcrição": "transcript",
            "legenda": "caption", "legendagem": "caption",
        }
        expanded_terms = set(task_terms)
        for term in task_terms:
            synonym = SYNONYMS.get(term)
            if synonym:
                expanded_terms.add(synonym)

        # Ranking BM25 (context-selector/ratel — R9) sobre descrição+tags completos
        bm25_candidates: Dict[str, List[Dict[str, Any]]] = {}
        for cat in self.CATEGORIES:
            docs = []
            for item in registry.get(cat, []):
                text = " ".join([
                    str(item.get("name", "")),
                    str(item.get("description", "")),
                    " ".join(str(t) for t in item.get("tags", []) or []),
                ])
                docs.append({"text": text, "item": item})
            if docs:
                ranked = self._rank_bm25(task, docs)
                bm25_candidates[cat] = ranked

        selected: Dict[str, List[Dict[str, Any]]] = {}
        for cat in self.CATEGORIES:
            scored = []
            for item in registry.get(cat, []):
                score = 0
                desc = f"{item.get('description', '')} {item.get('name', '')}".lower()
                matched = False
                for tag in item.get("tags", []):
                    if tag.lower() in task_lower:
                        score += 3
                        matched = True
                for term in expanded_terms:
                    if term in desc:
                        score += 1
                        matched = True
                if item.get("name", "").lower() in task_lower:
                    score += 2
                    matched = True
                if not matched:
                    continue
                score += boosts.get(cat, 0)
                score += learned.get(f"{cat}:{item.get('name', '')}", 0) * 0.5
                # BM25 como boost fino (0..3): reforça recursos semanticamente relevantes
                bm25_rank = bm25_candidates.get(cat, [])
                if bm25_rank and item in bm25_rank:
                    import math as _m
                    pos = bm25_rank.index(item)
                    bonus = 3.0 * (1.0 - pos / max(len(bm25_rank), 1))
                    score += bonus
                if score > 0:
                    scored.append((score, item))
            scored.sort(key=lambda x: -x[0])
            selected[cat] = [item for _, item in scored[:top_k]]

        return selected

    def route_to_model(self, task: str, phase: str = "", top_k: int = 3) -> Dict[str, Any]:
        """Delegação oferta-demanda: recurso → submodelo mais capaz.

        O orquestrador (Ornith) escolhe os recursos e roteia cada um para o
        submodelo cujas capacidades melhor atendem a task (desempenho,
        eficiência, precisão). Capacidades vêm do harness-config.json.
        """
        selections = self.select_for_task(task, phase, top_k)
        config_path = self.project_root / "harness" / "harness-config.json"
        config = self._load_json(config_path) or {}
        models = config.get("harness", {}).get("models", {})
        task_lower = task.lower()

        # Capacidades por submodelo (oferta) — divisão de trabalho:
        # Ornith = Controlador Lógico | Bonsai = Unidade de Síntese |
        # Nanbeige = raciocínio/validação | LFM = visão/instant
        MODEL_CAPS = {
            "gran_mestre": {"orquestra", "delega", "planeja", "agente", "tool", "loop",
                            "revisa", "decide", "scaffold", "mcp", "hook", "roteia",
                            "controla", "json", "xml", "parsing", "fallback", "rede",
                            "sintaxe", "roteamento", "workflow", "estado"},
            "heavy_execution": {"código", "code", "gera", "gera_codigo", "executa",
                                "visão", "imagem", "ocr", "grafico", "analisa",
                                "engenharia reversa", "ghidra", "decompila", "binário",
                                "firmware", "build", "compila", "teste", "refatora",
                                "resumo", "sumariza", "sintetiza", "log", "manual",
                                "texto", "leitura", "relatório", "relatorio"},
            "filter_medium": {"valida", "verifica", "revisa", "raciocina", "chain",
                              "math", "matemática", "matematica", "lógica", "logica",
                              "micro_review", "checa", "precisão", "precisao"},
            "filter_fast": {"imagem", "ocr", "documento", "multimodal", "frame",
                            "vídeo", "video", "instant", "rápido", "rapido",
                            "traduz", "idioma", "visual", "áudio", "audio", "som",
                            "transcrição", "transcricao", "legenda", "design",
                            "estética", "estetica", "estilo", "layout", "ui",
                            "feedback", "interpreta", "interpretação",
                            "interpretacao", "caption", "grounding"},
        }

        def cap_score(model_key: str, cat: str, name: str) -> int:
            caps = MODEL_CAPS.get(model_key, set())
            hay = f"{cat} {name} {task_lower}"
            return sum(1 for c in caps if c in hay)

        # Nota: o BM25 (R10-A) já ranqueia `selections` em select_for_task — a ordem
        # de iteração aqui (posição no top_k) já reflete relevância BM25∨tags.
        routing: Dict[str, List[Dict[str, Any]]] = {}
        for cat, items in selections.items():
            for item in items:
                name = item.get("name", "")
                scored = [(cap_score(k, cat, name), k) for k in MODEL_CAPS]
                scored.sort(key=lambda x: -x[0])
                best_score, best_key = scored[0]
                if best_score == 0:
                    best_key = "gran_mestre"
                routing.setdefault(best_key, []).append({
                    "categoria": cat,
                    "recurso": name,
                    "modelo": models.get(best_key, {}).get("name", best_key),
                })
        return routing

    def get_resources_by_tags(self, tags: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Compat v1: recursos por tags, ranqueados por BM25 (relevância)."""
        registry = self.build_registry()
        query = " ".join(tags)
        matching: Dict[str, List[Dict[str, Any]]] = {}
        for cat in self.CATEGORIES:
            matched = []
            for item in registry.get(cat, []):
                item_tags = [t.lower() for t in item.get("tags", [])]
                desc_lower = f"{item.get('description', '')} {item.get('name', '')}".lower()
                if any(tag.lower() in item_tags or tag.lower() in desc_lower for tag in tags):
                    matched.append(item)
            docs = [{
                "text": f"{item.get('name', '')} {item.get('description', '')} "
                        f"{' '.join(item.get('tags', []))}",
                "item": item,
            } for item in matched]
            matching[cat] = self._rank_bm25(query, docs)
        return matching

    # ────────────────────────────────────────────────────────────────
    # HELPERS
    # ────────────────────────────────────────────────────────────────
    @staticmethod
    def _load_json(path: Path) -> Optional[Dict[str, Any]]:
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(errors="replace"))
        except Exception:
            return None

    # Integrações (v1 — mantidas)
    def integrate_with_opencode(self) -> bool:
        return True

    def integrate_with_obsidian(self) -> bool:
        return True

    def integrate_with_github(self) -> bool:
        return True

    def get_integration_status(self) -> Dict[str, Any]:
        return {
            "opencode": self.opencode_dir.exists(),
            "obsidian": Path("/mnt/dados/cerebro com IA").exists(),
            "registry_v2": (self.project_root / "harness" / "registry.json").exists(),
            "categorias": self.CATEGORIES
        }


def main():
    """CLI — Integration Manager v2."""
    import argparse

    parser = argparse.ArgumentParser(description="Gran-Mestre Integration Manager v2")
    parser.add_argument("command", choices=["registry", "select", "status", "tags", "decision", "history", "route"],
                        help="Integration command")
    parser.add_argument("--task", type=str, help="Task description for auto-selection")
    parser.add_argument("--phase", type=str, default="",
                        choices=["", "discovery", "contract", "plan", "execute", "review", "deliver"],
                        help="Pipeline phase (boost de categorias)")
    parser.add_argument("--tags", type=str, nargs="+", help="Tags to search for")
    parser.add_argument("--top", type=int, default=5, help="Top-K resources per category")
    parser.add_argument("--outcome", type=str, default="pending",
                        choices=["pending", "success", "fail"],
                        help="Decision outcome for feedback (learning)")
    parser.add_argument("--feedback", type=str, default="",
                        help="Feedback text describing the result")
    parser.add_argument("--limit", type=int, default=20,
                        help="History limit (default: 20)")
    parser.add_argument("--print", dest="print_only", action="store_true",
                        help="Print selection without recording (dry-run)")

    args = parser.parse_args()
    manager = IntegrationManager()

    if args.command == "registry":
        registry = manager.build_registry()
        print(json.dumps({c: len(registry.get(c, [])) for c in manager.CATEGORIES}, indent=2))

    elif args.command == "select":
        if not args.task:
            print("Error: --task required")
            exit(1)
        result = manager.select_for_task(args.task, args.phase, args.top)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if not args.print_only:
            manager.record_decision(args.task, args.phase, result)

    elif args.command == "decision":
        if not args.task:
            print("Error: --task required")
            exit(1)
        selections = manager.select_for_task(args.task, args.phase, args.top)
        manager.record_decision(args.task, args.phase, selections,
                                outcome=args.outcome, feedback=args.feedback)
        print(f"[Decision] registered — outcome: {args.outcome}")
        print(json.dumps({c: [i.get("name", "") for i in items]
                          for c, items in selections.items()}, indent=2, ensure_ascii=False))

    elif args.command == "route":
        if not args.task:
            print("Error: --task required")
            exit(1)
        routing = manager.route_to_model(args.task, args.phase, args.top)
        for model_key, resources in routing.items():
            print(f"\n[{model_key}]")
            for r in resources:
                print(f"  {r['categoria']} → {r['recurso']}  ({r['modelo']})")

    elif args.command == "history":
        entries = manager.get_decision_history(args.task, args.limit)
        if not entries:
            print("[]")
        else:
            print(json.dumps(entries, indent=2, ensure_ascii=False))

    elif args.command == "status":
        print(json.dumps(manager.get_integration_status(), indent=2))

    elif args.command == "tags":
        if not args.tags:
            print("Error: --tags required")
            exit(1)
        print(json.dumps(manager.get_resources_by_tags(args.tags), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
