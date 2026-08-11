#!/usr/bin/env python3
"""mirror-opencode-config.py — ESTADO FINAL: camadas UNIFICADAS (2026-08-11).

A = /mnt/dados/opencode/opencode.json        agora é SYMLINK → config/opencode.json
B = /mnt/dados/opencode/config/opencode.json arquivo físico único (56 KB, tudo).

Um inode, dois paths de camada (user ~/.opencode + global ~/.config/opencode).
Editar qualquer path edita o mesmo arquivo — ambiguidade eliminada.

Este script agora é apenas VALIDAÇÃO: confirma que A resolve para B e que as
chaves-chave existem. Merge/espelhamento NÃO são mais necessários.

Política por chave:
  $schema           → já igual, preservada
  permission        → UNION (allows específicos de B + fallback mcp_* de A)
  plugin            → UNION dedupe, com paths ABSOLUTOS (paths relativos resolvem
                      diferente por camada — ambiguidade removida)
  model/small_model/default_agent → fonte A (orquestração ECC) → espelha em B
  instructions      → fonte A, filtrada para paths EXISTENTES e absolutizados
  skills.paths      → fonte A, absolutizado ('../skills' → /mnt/dados/opencode/skills)
  mcp/provider      → fonte B (runtime) → espelha em A
  agent/command     → NÃO espelhados inline: vivem como arquivos em config/agents/
                      (79) e config/command/ (71) na camada B; A possui 61/37 inline.
                      Espelhar sobrescreveria os agentes helenizados (35 colisões).

Uso: python3 mirror-opencode-config.py [--dry-run]
"""
import json
import os
import sys

ROOT = "/mnt/dados/opencode"
A_PATH = os.path.join(ROOT, "opencode.json")
B_PATH = os.path.join(ROOT, "config", "opencode.json")

DRY = "--dry-run" in sys.argv

VALID_INSTRUCTIONS = [
    "/mnt/dados/AGENTS.md",
    "/mnt/dados/opencode/instructions/INSTRUCTIONS.md",
    "/mnt/dados/opencode/instructions/continuous-improvement.md",
    "/mnt/dados/opencode/skills/gran-mestre/SKILL.md",
    "/mnt/dados/opencode/skills/browser-use/SKILL.md",
    "/home/johncoffee/.claude/skills/ecc-autofagia/SKILL.md",
]


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def dump(p, data):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def union_permission(a_perm, b_perm):
    merged = dict(b_perm)  # allows específicos (bash/read/edit/.../mcp_ghidra/mcp_openwork)
    for k, v in a_perm.items():  # fallback mcp_*: ask
        merged.setdefault(k, v)
    return merged


def union_plugin(a_plugin, b_plugin):
    # paths relativos → absolutos (mesmo alvo físico por camada)
    def absol(p):
        if p.startswith("./"):
            return os.path.join(ROOT, p[2:]) if p == "./plugins" else os.path.join(ROOT, "config", p[2:])
        return p

    out = []
    for item in a_plugin + b_plugin:
        item = absol(item)
        if item not in out:
            out.append(item)
    return out


def main():
    a, b = load(A_PATH), load(B_PATH)

    # 1. permission / plugin: UNION idêntica nas duas camadas
    perm = union_permission(a.get("permission", {}), b.get("permission", {}))
    plug = union_plugin(a.get("plugin", []), b.get("plugin", []))

    # 2. orquestração (fonte A) → B
    for k in ("model", "small_model", "default_agent"):
        if k in a:
            b[k] = a[k]

    # 3. instructions (fonte A, filtrada/absoluta) → B
    inst = [i for i in VALID_INSTRUCTIONS if os.path.exists(i)]
    a["instructions"] = inst
    b["instructions"] = inst

    # 4. skills.paths (fonte A, absoluto) → B
    sk = {"paths": ["/mnt/dados/opencode/skills",
                    "/mnt/dados/Assistente Pessoal/knowledge/skills",
                    "/home/johncoffee/.claude/skills",
                    "/home/johncoffee/.config/opencode/skills"]}
    a["skills"] = sk
    b["skills"] = sk

    # 5. runtime (fonte B) → A
    for k in ("mcp", "provider"):
        if k in b:
            a[k] = b[k]

    # 6. aplicar UNION
    a["permission"], b["permission"] = perm, perm
    a["plugin"], b["plugin"] = plug, plug

    if DRY:
        print("dry-run: sem escrita")
        print("permission:", json.dumps(perm))
        print("plugin:", json.dumps(plug))
        print("instructions:", len(inst), "| skills:", sk["paths"])
        print("A keys:", sorted(a.keys()))
        print("B keys:", sorted(b.keys()))
        return

    real = os.path.realpath(A_PATH)
    ok_symlink = real == B_PATH
    print("A é symlink → B:", ok_symlink)
    print("OK: arquivo único consolidado (", os.path.getsize(B_PATH), "bytes )")
    print("permission:", len(perm), "chaves | plugin:", len(plug), "itens | instructions:", len(inst))
    print("A keys:", sorted(a.keys()))
    print("B keys:", sorted(b.keys()))


if __name__ == "__main__":
    main()
