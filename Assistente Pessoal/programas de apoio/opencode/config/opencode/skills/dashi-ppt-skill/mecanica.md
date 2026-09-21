# dashi-ppt-skill — Mecânica de Ignição (R77 camada 3)

## 1. Seleção de motor (catálogo R75 — sempre refutando)

- **Categoria alvo**: `contrato-plano` (montagem multi-arquivo HTML, janela longa)
- **Slot esperado**: `:9088` (131K ctx p/ brief + N páginas)
- **Refutação do catálogo**: janela cobre brief+10 páginas? tps sustenta ~100k tok? vocação é montagem (sim) — aceito
- **Fallback**: cloud-direct (modo autônomo §9) se local offline

## 2. Parâmetros de ignição (samplers & setup)

```json
{
  "temp": 0.2,
  "top_k": 20,
  "top_p": 0.95,
  "repeat_penalty": 1.1,
  "max_tokens": 4096
}
```

- **Ganchos de backend**: Node.js 20+ p/ build; Chrome/Chromium/Edge local p/ export PPTX/PDF (`CHROME_PATH`); preview servido só em loopback

## 3. Sequência de ignição

1. Validar gabarito (deny) antes de qualquer ação — sem `theme`+`pages` o spec é inválido
2. Resolver motor via inventário (R75) — contrato-plano primeiro
3. `brief` → `theme_choice` → `page_spec[]` (layout + copy fields + console) → `export_artifact`
4. Gate categórico (R28): toda página tem layout + copy + console; export no formato pedido; nota R34 com bugs concretos

## 4. Funções focadas (Python, blocos curtos)

```python
def ignicao(brief: str, theme: str, pages: list) -> dict:
    """Monta spec do deck: valida → páginas (layout+copy+console) → export."""
    spec = montar_spec(brief, theme, pages)
    return validar_export(spec)
```

## 5. Enforcement

- O motor/validador **recusa ignição** se a mecânica violar o próprio gabarito (deny) — camada 2 é lei.
- Alteração de sampling sem novo crivo empírico = proibida (R62/R66).
- Conteúdo do deck nunca sai da máquina — zero upload.
