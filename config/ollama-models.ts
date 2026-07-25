export default async () => {
  return {
    config: (cfg: any) => {
      const raw =
        cfg?.provider?.ollama?.options?.baseURL ||
        "http://localhost:11434/v1"
      const root = String(raw).replace(/\/v1\/?$/, "") || "http://localhost:11434"

      const label = (id: string) => {
        const clean = id.replace(/:latest$/, "")
        const [base, tag] = clean.split(":")
        const head = base.charAt(0).toUpperCase() + base.slice(1)
        return head + (tag ? ` ${tag}` : "")
      }

      return fetch(`${root}/api/tags`)
        .then((r) => r.json() as Promise<{ models: any[] }>)
        .then((data) => {
          const models: Record<string, { name: string }> = {}
          for (const m of data.models ?? []) {
            const caps: string[] = m.capabilities ?? []
            if (!caps.includes("completion")) continue
            const tags: string[] = []
            if (caps.includes("tools")) tags.push("tools")
            if (caps.includes("thinking")) tags.push("think")
            if (caps.includes("vision")) tags.push("vision")
            const size = m.details?.parameter_size ? ` · ${m.details.parameter_size}` : ""
            const suffix = tags.length ? ` [${tags.join("+")}]` : ""
            models[m.name] = { name: `${label(m.name)}${size}${suffix}` }
          }
          cfg.provider = cfg.provider ?? {}
          cfg.provider.ollama = cfg.provider.ollama ?? {}
          cfg.provider.ollama.models = models
        })
        .catch((err) => {
          console.error("[ollama-models] could not list models:", err)
          cfg.provider = cfg.provider ?? {}
          cfg.provider.ollama = cfg.provider.ollama ?? {}
          cfg.provider.ollama.models = {}
        })
    },
  }
}
