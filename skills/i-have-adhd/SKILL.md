---
name: i-have-adhd
description: "A skill to stop your coding agent from burying the answer. ADHD-friendly output. (absorvido de ayghri/i-have-adhd)"
---
# I Have Adhd

Helenizado de [`ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd).

## Propósito
Shaped response for a reader with ADHD: lead with the next action, number multi-step work, restate state every turn, suppress tangents, give specific time estimates, make wins visible. Stays on until 'stop adhd mode'.

## Padrões absorvidos (núcleo canônico do repo)
- Lead with the next action: the first line is something the reader can do (command, path, or snippet first, prose after)
- Number multi-step tasks with bounded, numbered steps; no step contains 'and then' twice; cut unneeded steps
- End with one concrete next action the reader can do in under two minutes if anything is left open
- Suppress tangents: finish the first issue, then offer the second as a separate question
- Restate state every turn: the reader cannot hold 'step 3 of 5' between messages — restate progress explicitly
- Give specific time estimates in concrete units (e.g. 'about 15 minutes'), never vague ('some work')
- Make completed work visible: show what now works in concrete terms, do not bury wins in a recap
- Matter-of-fact tone for errors: state cause and fix, never 'Uh oh' or 'There seems to be a problem'
- Cap lists at 5 items: split into 'do now' vs 'later' or 'must' vs 'nice to have' past five
- No preamble, no recap, no closing pleasantries: start with the answer, end when the answer is done

## Como usar (orquestrado pelo Gran-Mestre)
1. Detectar necessidade que casa com este padrão.
2. Carregar skill (`skill(name="i-have-adhd")`) ou subagent (`task(subagent_type="...")`).
3. Aplicar o padrão helenizado ao contexto atual.

## Fonte
https://github.com/ayghri/i-have-adhd
