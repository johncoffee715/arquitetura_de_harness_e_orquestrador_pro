// ecc-session-delete — REGRA GLOBAL: deletar sessão SEMPRE passa por
//   REGISTRAR → COMPACTAR → LIMPAR (via ecc-session-end.sh → compact_context.py).
// Hook nativo `session.deleted` do OpenCode. Fire-and-forget: nunca bloqueia.
// Formato: export const <Name> = async (ctx) => ({ "event": async () => {} })
type Shell = { quiet: (s: TemplateStringsArray, ...a: unknown[]) => { text: () => Promise<string>; nothrow: () => Promise<unknown> } };
export const EccSessionDelete = async ({ $ }: { $: Shell }) => {
  return {
    "session.deleted": async (_input: unknown) => {
      void (async () => {
        try {
          await $.quiet`bash /home/johncoffee/.claude/hooks/ecc-session-end.sh`.nothrow();
        } catch {}
      })();
    },
  };
};
