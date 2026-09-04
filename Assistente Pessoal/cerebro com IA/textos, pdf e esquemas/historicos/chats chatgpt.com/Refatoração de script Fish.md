---
title: "Refatoração de script Fish"
source: "https://chatgpt.com/c/69faa4c9-7f00-832b-99fe-f42f7bbc5d6a"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**Você disse**

#!/usr/bin/fish # Nome: super-run.sh # Função: Execução autônoma com checkpoint de aprovação humana. # Uso:./super-run.sh "comando\_ou\_script" set CMD $argv\[1\] function log\_tech -a msg echo (set\_color cyan)"\[ENGINEER-LOG\] "(set\_color normal)$msg end log\_tech "Analisando comando: $CMD" # O loop de supervisão while true echo (set\_color yellow)"\[REQ\] Executar ação proposta? (ENTER para sim, Ctrl+C para abortar)"(set\_color normal) read confirmation # Execução e captura de telemetria log\_tech "Executando..." set output (eval $CMD 2>&1) set status\_code $status if test $status\_code -eq 0 log\_tech "Sucesso operacional." echo $output break else log\_tech "Falha detectada (Exit Code: $status\_code)." echo (set\_color red)"--- STDERR/STDOUT ---"(set\_color normal) echo $output echo (set\_color red)"---------------------"(set\_color normal) log\_tech "Enviando telemetria para análise de causa raiz..." # Aqui, no fluxo real, você colaria o erro de volta para mim. # No modo autônomo pleno, o script enviaria via API. break end end

---

Vou direto: esse script ainda não cria um checkpoint real. O `read confirmation` não é validado, então ele executa do mesmo jeito; além disso, `eval` abre brecha de parsing e o loop sai na primeira falha.

Esse script tem 3 problemas centrais:

1. `read confirmation` não é usado para decidir nada, então o “checkpoint” é simbólico, não real.
2. `set CMD $argv[1]` pega só o primeiro pedaço do comando; argumentos extras se perdem.
3. `eval $CMD` é frágil e perigoso; quebra fácil com aspas, espaços e redirecionamentos.

Versão refatorada, mais limpa e operacional:

```
#!/usr/bin/env fish
# Nome: super-run.sh
# Função: Execução supervisionada com aprovação humana explícita.

function log_tech -a msg
    echo (set_color cyan)"[ENGINEER-LOG] "(set_color normal)$msg
end

if test (count $argv) -eq 0
    echo (set_color red)"Uso: ./super-run.sh comando [args...]"(set_color normal)
    exit 1
end

set -l cmd $argv
log_tech "Comando proposto: "(string join ' ' (string escape -- $cmd))

while true
    echo -n (set_color yellow)"[REQ] Executar ação proposta? [ENTER=sim / n=abortar / r=revisar] "(set_color normal)
    read -l confirmation

    switch $confirmation
        case ''
            log_tech "Executando..."
            set -l output (command $cmd 2>&1)
            set -l status_code $status

            if test $status_code -eq 0
                log_tech "Sucesso operacional."
                printf '%s\n' $output
                break
            else
                log_tech "Falha detectada (Exit Code: $status_code)."
                echo (set_color red)"--- STDERR/STDOUT ---"(set_color normal)
                printf '%s\n' $output
                echo (set_color red)"---------------------"(set_color normal)
                log_tech "Ação interrompida para análise."
                exit $status_code
            end

        case n N no NO
            log_tech "Execução abortada pelo operador."
            exit 130

        case r R
            log_tech "Revisão solicitada. Reinsira o comando antes de continuar."
            exit 0

        case '*'
            log_tech "Opção inválida."
    end
end
```

O ganho real aqui é este: comando com argumentos funciona direito, a aprovação humana passa a valer de verdade, e você não depende de `eval` para executar.

Se quiser, eu também posso te devolver uma versão **mais robusta**, com:

- log em arquivo,
- timeout,
- checksum do comando,
- modo dry-run,
- e reexecução automática com rollback de estado.