// Camada de compatibilidade `./promise` — Ciclo E2/E3 (2026-08-25)
// Ponte p/ consumidores que usavam o vocabulário do cliente publicado antigo
// (tarball 1.17.13-v2). Aliases estruturais espelham os tipos canônicos atuais;
// cada entrada documenta o equivalente canônico p/ alinhamento futuro.
export * from "./generated"

// Canônico: @opencode-ai/schema `FileDiff.Info` (SnapshotFileDiff) tornou os
// campos opcionais no servidor; consumidores legados compilam contra a forma
// obrigatória do tarball e já filtram variantes em união. Espelho exato aqui.
export type FileDiffInfo = {
  file: string
  patch: string
  additions: number
  deletions: number
  status: "added" | "deleted" | "modified"
}
