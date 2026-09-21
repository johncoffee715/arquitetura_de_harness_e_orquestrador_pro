// Gran-Mestre Boot — plugin global de boot (nativo opencode, manual)
// Formato nativo opencode: export const <Name> = async (ctx) => ({ hooks })
// Fire-and-forget: nunca bloqueia o startup do opencode.
export const GranMestreBoot = async ({ $ }) => {
  // fire-and-forget: nunca bloquear o boot
  void (async () => {
    try {
      // 1) Se servidores locais (portas 8081-8084) down → `gran-mestre models-up`
      //    verificar com `ss -ltn` ou `pgrep llama-server`; disparar `gran-mestre models-up`
      const listeners = await $.quiet`ss -ltn`.text().catch(() => "");
      const hasLocal = [8081, 8082, 8083, 8084].some((p) => listeners.includes(`:${p}`));
      if (!hasLocal) {
        await $.quiet`gran-mestre models-up`.nothrow();
      }
      // 2) Rebuild silencioso do registry: `gran-mestre registry`
      await $.quiet`gran-mestre registry`.nothrow();
    } catch {}
  })();
  return {};
};
