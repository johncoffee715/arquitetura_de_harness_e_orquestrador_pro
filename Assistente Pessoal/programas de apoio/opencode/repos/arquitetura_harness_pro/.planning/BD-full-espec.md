# B/D-FULL — ESPECIFICAÇÃO DE EXECUÇÃO (sessão dedicada futura)

Pré-requisitos: aprovação do usuário · ~90min de GPU exclusiva · stack 7/7 · harness corrigido (dual-field).
Ordem fixa de swaps: qwen9b@131072 → qwen27b@32768 → bonsai1bit@32768 → ornith@131072 (restore final).
Invariantes: dreno VRAM entre swaps · dual-field parsing · evidência JSON+raw por probe (proibido nota sem artefato).

## CATEGORIA B-full — decomposição ×2 domínios (rubrica 10pts cada)

### Domínio 1: e-commerce (baseline já medido no mini-B — reusar)
Componentes: catálogo · carrinho · pagamento/pix · email.

### Domínio 2: migração de BD legado → PostgreSQL (NOVO)
Componentes obrigatórios: inventário/inventário de schema · mapeamento de tipos · estratégia de dados históricos · rollback plan.
Ground truth (referência para overlap):
1. Inventariar schema+volume da fonte
2. Mapear tipos (incl. edge cases: NULL, encoding, datas pré-1970)
3. Criar schema destino + constraints
4. Migração em lotes idempotentes (batch testável)
5. Validação de integridade pós-carga (counts+checksums)
6. Plano de cutover com rollback

Rubrica por domínio: componentes cobertos 4×1.5 · ordenação topológica válida 2.0 · dependências explícitas entre etapas 2.0.
Score B = média dos 2 domínios.

## CATEGORIA D-full — execução determinística (12 tarefas em 3 tiers)

| Tier | Tarefas | Peso/task |
|---|---|---|
| Trivial (reusar mini-D) | soma · eh_primo · inverte | 1 |
| Médio | valida_cpf · top_dict · fib_lista · regex_email (extração de emails em texto) | 2 |
| Difícil (NOVAS) | parser_json_malformado (recuperar dados de JSON quebrado com heurísticas) · sql_safe_builder (query parametrizada contra injection — validar AST) · state_machine_semaforo (transições válidas/inválidas) · diff_patch (aplicar unidiff em texto e validar resultado) | 3 |

Verificador: extração de bloco → subprocesso isolado (timeout 8s) → asserts → exit code.
Score D = Σ(passos × peso)/Σ(pesos máximos).

## CÁLCULO GM-OFICIAL
Substituir minis por fulls na fórmula integral (Adenda 10) · publicar Adenda 13 comparativa
(GM-mini vs GM-full por candidato — mede se os minis superestimam).

## Evidências por candidato
`gmb1-{bfull,dfull}-{tag}.json` + raws · wall-clock por task · falhas com stderr citado.
