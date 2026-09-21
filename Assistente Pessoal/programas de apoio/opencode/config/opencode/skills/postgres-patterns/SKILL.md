---
name: postgres-patterns
description: Relational durability concepts — MVCC, WAL, constraints as contracts (concepts only, never the DB).
category: skill
model: local-forge/proposer
---

# postgres-patterns

Conceitos de durabilidade relacional: MVCC (leitores nunca bloqueiam escritores),
WAL (durabilidade antes de confirmação), constraints como contratos.
Helenizado de `postgres/postgres` (origem: https://github.com/postgres/postgres).

> PROIBIDO como dependência (doutrina R2): vault é o estado. Só conceitos.
