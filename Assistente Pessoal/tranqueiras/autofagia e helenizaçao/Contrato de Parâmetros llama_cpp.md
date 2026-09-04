# Contrato de Parâmetros llama.cpp • Skill Hefesto
> **Contexto:** Especificação técnica para automação, geração de código e orquestração de infraestrutura de LLMs locais.
> **Formatos de Integração:** `Hefesto-Engine (Python)` ➔ `Config (JSON)` ➔ `Documentação (MD)`.

---

## 1. Ciclo de Vida e Provisionamento de Modelos
Flags utilizadas pela Hefesto para gerenciar o download, cache e carregamento dos arquivos GGUF.

```json
{
  "category": "model_lifecycle",
  "parameters": ["model", "hf-repo", "model-url", "lazy-mode"]
}
```

* **`-m, --model`**  
  * **Tipo:** `string` (Path)  
  * **Uso no Python:** `subprocess.run(["llama-cli", "-m", config["model_path"]])`  
  * **Descrição:** Caminho absoluto do arquivo `.gguf`. Chave primária de carregamento.
  
* **`-hf, --hf-repo`**  
  * **Tipo:** `string` (`user/repo-GGUF`)  
  * **Descrição:** Repositório do Hugging Face. Permite que a Hefesto baixe novos modelos *on-the-fly*.

* **`-mu, --model-url`**  
  * **Tipo:** `string` (URL)  
  * **Descrição:** Link direto para download. Útil para espelhos (mirrors) internos do ecossistema.

* **`-lzm, --lazy-mode`**  
  * **Tipo:** `boolean` (Flag)  
  * **Descrição:** Ativa carregamento tardio de tensores. Reduz o *Cold Start* da skill em microserviços.

---

## 2. Orquestração de Hardware (CPU & VRAM)
Configurações dinâmicas que a Hefesto deve calcular via Python (usando `os.cpu_count()` ou ferramentas de monitoramento de GPU) antes de subir a instância.

```json
{
  "category": "hardware_allocation",
  "auto_calculable": true
}
```

* **`-t, --threads`**  
  * **Tipo:** `integer`  
  * **Regra Hefesto:** `threads = os.cpu_count() or 4` (Recomendado fixar em cores físicos).  
  * **Descrição:** Quantidade de threads para a etapa de geração de tokens.

* **`-ngl, --n-gpu-layers`**  
  * **Tipo:** `integer`  
  * **Descrição:** Quantidade de camadas do modelo movidas para a GPU. `0` roda 100% na CPU; `99` força carregamento total na VRAM.

* **`-fa, --flash-attn`**  
  * **Tipo:** `boolean` (Flag)  
  * **Descrição:** Habilita Flash Attention. Reduz drasticamente o consumo de VRAM e RAM durante o processamento do contexto.

* **`--mlock`**  
  * **Tipo:** `boolean` (Flag)  
  * **Descrição:** Bloqueia a memória RAM/VRAM para o processo, impedindo paginação (swap) em disco e garantindo latência linear.

---

## 3. Gestão de Contexto e Janela de Memória
Controladores do buffer de tokens para o pipeline de dados de entrada e saída.

```json
{
  "category": "context_management",
  "metrics": ["tokens", "batch"]
}
```

* **`-c, --ctx-size`**  
  * **Tipo:** `integer`  
  * **Descrição:** Tamanho total da janela de contexto (ex: `4096`, `8192`). `0` adota o padrão nativo do arquivo GGUF.

* **`-b, --batch-size`**  
  * **Tipo:** `integer`  
  * **Descrição:** Tamanho do lote lógico de tokens processados de uma vez (Processamento do prompt / *Prompt Ingestion*).

* **`-n, --n-predict`**  
  * **Tipo:** `integer`  
  * **Descrição:** Limite de tokens gerados na resposta. Use `-1` para permitir geração contínua até o token de parada (`EOS`).

---

## 4. Engenharia de Amostragem (Deterministic vs Creative)
Configurações comportamentais do modelo. Essencial para alternar o modo de operação da Hefesto entre "Escrever Código Estrito" e "Explorar Soluções Criativas".

```json
{
  "category": "sampling_profiles",
  "profiles": {
    "deterministic_json_code": { "temp": 0.0, "min-p": 0.05 },
    "creative_brainstorm": { "temp": 0.7, "min-p": 0.1 }
  }
}
```

* **`--temp`**  
  * **Tipo:** `float` (Faixa: `0.0` a `2.0`)  
  * **Descrição:** Temperatura de amostragem. `0.0` torna a resposta estritamente determinística (ideal para geração de código Python e schemas JSON).

* **`--min-p`**  
  * **Tipo:** `float` (Faixa: `0.0` a `1.0`)  
  * **Descrição:** Filtro dinâmico baseado na probabilidade do token líder. Remove alucinações mantendo a fluidez.

* **`--repeat-penalty`**  
  * **Tipo:** `float`  
  * **Descrição:** Penalidade para evitar loops de repetição de texto ou blocos de código redundantes.

---

## 5. Casamento de Estruturas e Validação Estrita (Grammar)
O recurso mais crítico para a Skill Hefesto garantir que as saídas geradas correspondam exatamente ao esperado pelo ecossistema.

```json
{
  "category": "structural_guarantee",
  "engine": "GBNF"
}
```

* **`--grammar`**  
  * **Tipo:** `string` (Conteúdo GBNF ou caminho para arquivo `.gbnf`)  
  * **Uso na Hefesto:** Força o LLM a responder **estritamente** no formato gramatical definido.
  * **Exemplo de aplicação:** Se a Hefesto precisa que o modelo retorne um JSON com chaves específicas (`{"feature_name": "...", "status": "..."}`), a flag `--grammar` impede o modelo de gerar qualquer texto explicativo fora do JSON.
