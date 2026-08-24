---
name: mattpocock-skills
description: "Skills for Real Engineers. Straight from .agents directory. (absorvido de mattpocock/skills)"
---
# Mattpocock Skills

Helenizado de [`mattpocock/skills`](https://github.com/mattpocock/skills).

## Propósito
My agent skills that I use every day to do real engineering - not vibe coding.

## Padrões absorvidos (núcleo canônico do repo)
- Ask you which issue tracker you want to use (GitHub, Linear, or local files)
- Ask you what labels you apply to tickets when you triage them (`/triage` uses labels)
- Ask you where you want to save any docs we create
- [`/grill-me`](./skills/productivity/grill-me/SKILL.md) - for non-code uses
- [`/grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md) - same as [`/grill-me`](./skills/productivity/grill-me/SKILL.md), but adds more goodies (see below)
- BEFORE**: "There's a problem when a lesson inside a section of a course is made 'real' (i.e. given a spot in the file system)"
- AFTER**: "There's a problem with the materialization cascade"
- [`/to-spec`](./skills/engineering/to-spec/SKILL.md) quizzes you about which modules you're touching before creating a spec

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="mattpocock-skills")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/mattpocock/skills
