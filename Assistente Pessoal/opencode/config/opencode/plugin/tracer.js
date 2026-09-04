// tracer.js — Trajectory Tracing (helenização dsh · R44)
// Log JSONL estruturado de cada chamada de ferramenta: tool, duração, tamanho,
// sucesso/falha, agente/modelo. NUNCA registra payload completo (privacidade+janela).
const starts = new Map();

export const Tracer = async ({ project }) => {
  const stateDir =
    (process.env.XDG_STATE_HOME || "/tmp") + "/watcher";
  try {
    const fs = await import("fs");
    fs.mkdirSync(stateDir, { recursive: true });
  } catch {}

  const file = () => `${stateDir}/trajectory.jsonl`;

  return {
    "tool.execute.before": async (input) => {
      starts.set(input.callID, {
        ts: Date.now(),
        tool: input.tool,
        session: input.sessionID,
      });
    },

    "tool.execute.after": async (input, output) => {
      const st = starts.get(input.callID) || { ts: Date.now(), tool: input.tool, session: input.sessionID };
      starts.delete(input.callID);
      let outLen = 0;
      try {
        outLen = typeof output.output === "string" ? output.output.length : JSON.stringify(output.output ?? "").length;
      } catch {}
      const entry = {
        ts: new Date().toISOString(),
        tool: input.tool,
        session: input.sessionID,
        callID: input.callID.slice(0, 8),
        dur_ms: Date.now() - st.ts,
        out_bytes: outLen,
        title: String(output.title ?? "").slice(0, 120),
        // erro aparece como metadata.error quando presente
        error: output.metadata?.error ? String(output.metadata.error).slice(0, 200) : null,
      };
      try {
        const fs = await import("fs");
        fs.appendFileSync(file(), JSON.stringify(entry) + "\n");
      } catch {}
    },
  };
};
