# GMB-lite — bateria 12 tarefas p/ duelo de orquestrador (não-oficial)

> Uso 2026-09-07: Ornith-1.5-9B-Q3 vs Qwen3.6-35B+draft (TESTE, não troca — R39).
> O GMB oficial (spec B/D-FULL, placar GM-local) não está arquivado no vault;
> esta bateria é documentada e reutilizável, mas NÃO gera GM-oficial.
> Mesmos prompts, temp 0.6/topp 0.95/topk 20 (R61 agentic), n_predict 120.
> Rubrica por tarefa: 1.0 certa · 0.5 parcial · 0.0 errada. Placar em /12.

1. LÓGICA: "Se todos os Zorks são Blips e alguns Blips voam, o que se pode concluir com certeza? Responda em 2 frases."
2. LÓGICA: "Point out the flaw in one sentence: All cats are mammals, Whiskers is a mammal, therefore Whiskers is a cat."
3. LÓGICA: "Três caixas: ouro/prata/bronze. Etiquetas todas erradas. Abrindo uma moeda de uma caixa, como rotular certo? Explique em 3 passos."
4. MATEMÁTICA: "Um trem a 120km/h parte às 14h; outro a 80km/h parte às 15h mesmo trajeto 400km. Quem chega primeiro e com que diferença? Mostre contas."
5. MATEMÁTICA: "Responda em portugues: 17*23 = ? Mostre a decomposição."
6. TOOL-CALL: "Extract JSON with keys capital and country from: Paris is the capital of France. Reply ONLY with the JSON."
7. JSON-EXATO: "Reply with exactly this JSON and nothing else: {\"status\": \"ok\", \"n\": 3}"
8. PLANEJAMENTO: "Write a 4-step test plan (headers only) for: login com OAuth2 quebrou após deploy. Seja específico."
9. INSTRUÇÃO: "Responda em portugues, uma frase: por que o ceu e azul?"
10. REFUTAÇÃO: "Refute em 2 frases: 'Modelo maior sempre vence porque tem mais parâmetros.'"
11. CÓDIGO: "Write a Python function is_prime(n). Reply with only the code."
12. ROTEAMENTO: "Classifique com UMA palavra (codigo/revisao/pesquisa): Corrigir NullPointerException no AuthService quando token expira."
