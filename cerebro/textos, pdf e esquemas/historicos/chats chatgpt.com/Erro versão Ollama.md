---
title: "Erro versão Ollama"
source: "https://chatgpt.com/c/6a4de26c-e60c-83e9-a29d-b6cbff6b1236"
author:
published:
created: 2026-07-17
description: "O ChatGPT é seu assistente de IA para uso diário. Converse com a IA mais avançada para explorar ideias, resolver problemas e aprender mais rápido."
tags:
  - "clippings"
---
Agora o problema mudou completamente. Você corrigiu o caminho, e isso revelou a causa real.

Antes:

```nix
ExecStart=/usr/local/bin/ollama
↓
203/EXEC (arquivo inexistente)
```

Agora:

```
ExecStart=/usr/bin/ollama
↓
203/EXEC
```

Ou seja, **o binário existe**, mas o `systemd` não consegue executá-lo.

## O que significa 203/EXEC

Esse erro pode ocorrer por alguns motivos:

- permissões incorretas;
- arquitetura/binário inválido (não parece ser o caso);
- caminho errado (já descartado);
- usuário do serviço sem permissão;
- dependência ausente;
- política de segurança (SELinux/AppArmor, improvável no seu caso).

Precisamos olhar o motivo exato.

Execute estes comandos:

```bash
ls -l /usr/bin/ollama

file /usr/bin/ollama

ldd /usr/bin/ollama | grep "not found"

journalctl -u ollama -n 50 --no-pager
```

O último é o mais importante.

---

## Outro teste importante

Tente iniciar exatamente como o serviço faria:

```bash
sudo -u johncoffee /usr/bin/ollama serve
```

Se funcionar, interrompa com `Ctrl+C`.

Depois teste:

```bash
/usr/bin/ollama serve
```

Se um deles falhar, a mensagem de erro vai indicar a causa.

---

## Um detalhe importante

Seu comando:

```bash
readlink -f /proc/$(pidof ollama)/exe
```

falhou porque:

```
pidof ollama
```

não retornou nenhum PID.

Isso confirma que **nenhum servidor Ollama está rodando**, por isso o cliente mostra:

```
Warning: could not connect to a running Ollama instance
```

---

## Suspeita forte

Você mostrou anteriormente que o serviço roda como:

```
User=johncoffee
```

Mas o serviço original tinha:

```
User=ollama
```

Verifique se o usuário `johncoffee` tem permissão para acessar os diretórios configurados, especialmente:

```
/opt/rocm
/mnt/win2/Assistente Pessoal2/data/ollama_models
```

e se o `gpu.conf` e o `override.conf` não estão introduzindo alguma variável incompatível.

---

### Minha principal hipótese

Como o erro continua sendo `203/EXEC` mesmo apontando para um binário existente, a saída do `journalctl -u ollama -n 50 --no-pager` deve revelar exatamente qual etapa do `execve()` está falhando. Essa será a informação decisiva para identificar a causa.

---

**Você disse**

/mnt/win2/Assistente Pessoal2 ❯ ls -l /usr/bin/ollama file /usr/bin/ollama ldd /usr/bin/ollama | grep "not found" journalctl -u ollama -n 50 --no-pager.rwxr-xr-x 35M root 1 jul 10:42 󰡯 /usr/bin/ollama /usr/bin/ollama: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID\[sha1\]=4f57f682d9ca1b47c9bce524ef0d11ae3c6cdfa8, for GNU/Linux 4.4.0, stripped jul 08 02:56:01 JohnCoffeeDesk systemd\[1\]: ollama.service: Main process exited, code=exited, status=203/EXEC jul 08 02:56:01 JohnCoffeeDesk systemd\[1\]: ollama.service: Failed with result 'exit-code'. jul 08 02:56:04 JohnCoffeeDesk systemd\[1\]: ollama.service: Scheduled restart job, restart counter is at 18. jul 08 02:56:04 JohnCoffeeDesk systemd\[1\]: Started Ollama Service. jul 08 02:56:04 JohnCoffeeDesk (ollama serve)\[262095\]: ollama.service: Unable to locate executable '/usr/bin/ollama serve': No such file or directory jul 08 02:56:04 JohnCoffeeDesk (ollama serve)\[262095\]: ollama.service: Failed at step EXEC spawning /usr/bin/ollama serve: No such file or directory jul 08 02:56:04 JohnCoffeeDesk systemd\[1\]: ollama.service: Main process exited, code=exited, status=203/EXEC jul 08 02:56:04 JohnCoffeeDesk systemd\[1\]: ollama.service: Failed with result 'exit-code'. jul 08 02:56:07 JohnCoffeeDesk systemd\[1\]: ollama.service: Scheduled restart job, restart counter is at 19. jul 08 02:56:07 JohnCoffeeDesk systemd\[1\]: Started Ollama Service. jul 08 02:56:07 JohnCoffeeDesk (ollama serve)\[262105\]: ollama.service: Unable to locate executable '/usr/bin/ollama serve': No such file or directory jul 08 02:56:07 JohnCoffeeDesk (ollama serve)\[262105\]: ollama.service: Failed at step EXEC spawning /usr/bin/ollama serve: No such file or directory jul 08 02:56:07 JohnCoffeeDesk systemd\[1\]: ollama.service: Main process exited, code=exited, status=203/EXEC jul 08 02:56:07 JohnCoffeeDesk systemd\[1\]: ollama.service: Failed with result 'exit-code'. jul 08 02:56:10 JohnCoffeeDesk systemd\[1\]: ollama.service: Scheduled restart job, restart counter is at 20. jul 08 02:56:10 JohnCoffeeDesk systemd\[1\]: Started Ollama Service. jul 08 02:56:10 JohnCoffeeDesk (ollama serve)\[262113\]: ollama.service: Unable to locate executable '/usr/bin/ollama serve': No such file or directory jul 08 02:56:10 JohnCoffeeDesk (ollama serve)\[262113\]: ollama.service: Failed at step EXEC spawning /usr/bin/ollama serve: No such file or directory jul 08 02:56:10 JohnCoffeeDesk systemd\[1\]: ollama.service: Main process exited, code=exited, status=203/EXEC jul 08 02:56:10 JohnCoffeeDesk systemd\[1\]: ollama.service: Failed with result 'exit-code'. jul 08 02:56:13 JohnCoffeeDesk systemd\[1\]: ollama.service: Scheduled restart job, restart counter is at 21. jul 08 02:56:13 JohnCoffeeDesk systemd\[1\]: Started Ollama Service. jul 08 02:56:14 JohnCoffeeDesk (ollama serve)\[262120\]: ollama.service: Unable to locate executable '/usr/bin/ollama serve': No such file or directory jul 08 02:56:14 JohnCoffeeDesk (ollama serve)\[262120\]: ollama.service: Failed at step EXEC spawning /usr/bin/ollama serve: No such file or directory jul 08 02:56:14 JohnCoffeeDesk systemd\[1\]: ollama.service: Main process exited, code=exited, status=203/EXEC jul 08 02:56:14 JohnCoffeeDesk systemd\[1\]: ollama.service: Failed with result 'exit-code'. jul 08 02:56:17 JohnCoffeeDesk systemd\[1\]: ollama.service: Scheduled restart job, restart counter is at 22. jul 08 02:56:17 JohnCoffeeDesk systemd\[1\]: Started Ollama Service. jul 08 02:56:17 JohnCoffeeDesk (ollama serve)\[262124\]: ollama.service: Unable to locate executable '/usr/bin/ollama serve': No such file or directory jul 08 02:56:17 JohnCoffeeDesk (ollama serve)\[262124\]: ollama.service: Failed at step EXEC spawning /usr/bin/ollama serve: No such file or directory jul 08 02:56:17 JohnCoffeeDesk systemd\[1\]: ollama.service: Main process exited, code=exited, status=203/EXEC jul 08 02:56:17 JohnCoffeeDesk systemd\[1\]: ollama.service: Failed with result 'exit-code'. jul 08 02:56:20 JohnCoffeeDesk systemd\[1\]: ollama.service: Scheduled restart job, restart counter is at 23. jul 08 02:56:20 JohnCoffeeDesk systemd\[1\]: Started Ollama Service. jul 08 02:56:20 JohnCoffeeDesk (ollama serve)\[262128\]: ollama.service: Unable to locate executable '/usr/bin/ollama serve': No such file or directory jul 08 02:56:20 JohnCoffeeDesk (ollama serve)\[262128\]: ollama.service: Failed at step EXEC spawning /usr/bin/ollama serve: No such file or directory jul 08 02:56:20 JohnCoffeeDesk systemd\[1\]: ollama.service: Main process exited, code=exited, status=203/EXEC jul 08 02:56:20 JohnCoffeeDesk systemd\[1\]: ollama.service: Failed with result 'exit-code'. jul 08 02:56:23 JohnCoffeeDesk systemd\[1\]: ollama.service: Scheduled restart job, restart counter is at 24. jul 08 02:56:23 JohnCoffeeDesk systemd\[1\]: Started Ollama Service. jul 08 02:56:23 JohnCoffeeDesk (ollama serve)\[262151\]: ollama.service: Unable to locate executable '/usr/bin/ollama serve': No such file or directory jul 08 02:56:23 JohnCoffeeDesk (ollama serve)\[262151\]: ollama.service: Failed at step EXEC spawning /usr/bin/ollama serve: No such file or directory jul 08 02:56:23 JohnCoffeeDesk systemd\[1\]: ollama.service: Main process exited, code=exited, status=203/EXEC jul 08 02:56:23 JohnCoffeeDesk systemd\[1\]: ollama.service: Failed with result 'exit-code'. jul 08 02:56:26 JohnCoffeeDesk systemd\[1\]: ollama.service: Scheduled restart job, restart counter is at 25. jul 08 02:56:26 JohnCoffeeDesk systemd\[1\]: Started Ollama Service. jul 08 02:56:27 JohnCoffeeDesk (ollama serve)\[262190\]: ollama.service: Unable to locate executable '/usr/bin/ollama serve': No such file or directory jul 08 02:56:27 JohnCoffeeDesk (ollama serve)\[262190\]: ollama.service: Failed at step EXEC spawning /usr/bin/ollama serve: No such file or directory jul 08 02:56:27 JohnCoffeeDesk systemd\[1\]: ollama.service: Main process exited, code=exited, status=203/EXEC jul 08 02:56:27 JohnCoffeeDesk systemd\[1\]: ollama.service: Failed with result 'exit-code'. /mnt/win2/Assistente Pessoal2 ❯ sudo -u johncoffee /usr/bin/ollama serve time=2026-07-08T02:56:43.752-03:00 level=INFO source=routes.go:1961 msg="server config" env="map\[CUDA\_VISIBLE\_DEVICES: GGML\_VK\_VISIBLE\_DEVICES: GPU\_DEVICE\_ORDINAL: HIP\_VISIBLE\_DEVICES: HSA\_OVERRIDE\_GFX\_VERSION: HTTPS\_PROXY: HTTP\_PROXY: LLAMA\_ARG\_FIT: LLAMA\_ARG\_FIT\_TARGET: NO\_PROXY: OLLAMA\_CONTEXT\_LENGTH:0 OLLAMA\_DEBUG:INFO OLLAMA\_DEBUG\_LOG\_REQUESTS:false OLLAMA\_EDITOR: OLLAMA\_FLASH\_ATTENTION:false OLLAMA\_GO\_TEMPLATE:true OLLAMA\_GPU\_OVERHEAD:0 OLLAMA\_HOST:[http://127.0.0.1:11434](http://127.0.0.1:11434/) OLLAMA\_IGPU\_ENABLE: OLLAMA\_KEEP\_ALIVE:5m0s OLLAMA\_KV\_CACHE\_TYPE: OLLAMA\_LLM\_LIBRARY: OLLAMA\_LOAD\_TIMEOUT:5m0s OLLAMA\_MAX\_LOADED\_MODELS:0 OLLAMA\_MAX\_QUEUE:512 OLLAMA\_MAX\_TRANSFER\_STREAMS:4 OLLAMA\_MODELS:/home/johncoffee/.ollama/models OLLAMA\_NOHISTORY:false OLLAMA\_NOPRUNE:false OLLAMA\_NO\_CLOUD:false OLLAMA\_NUM\_PARALLEL:1 OLLAMA\_ORIGINS:\[[http://localhost](http://localhost/) [https://localhost](https://localhost/) [http://localhost:\*](http://localhost:*) [https://localhost:\*](https://localhost:*) [http://127.0.0.1](http://127.0.0.1/) [https://127.0.0.1](https://127.0.0.1/) [http://127.0.0.1:\*](http://127.0.0.1:*) [https://127.0.0.1:\*](https://127.0.0.1:*) [http://0.0.0.0](http://0.0.0.0/) [https://0.0.0.0](https://0.0.0.0/) [http://0.0.0.0:\*](http://0.0.0.0:*) [https://0.0.0.0:\*](https://0.0.0.0:*) app://\* file://\* tauri://\* vscode-webview://\* vscode-file://\*\] OLLAMA\_REMOTES:\[ollama.com\] OLLAMA\_SCHED\_SPREAD:false OLLAMA\_VULKAN:true ROCR\_VISIBLE\_DEVICES: http\_proxy: https\_proxy: no\_proxy:\]" time=2026-07-08T02:56:43.752-03:00 level=INFO source=routes.go:1963 msg="Ollama cloud disabled: false" time=2026-07-08T02:56:43.753-03:00 level=INFO source=images.go:883 msg="total blobs: 0" time=2026-07-08T02:56:43.753-03:00 level=INFO source=images.go:890 msg="total unused blobs removed: 0" time=2026-07-08T02:56:43.753-03:00 level=INFO source=routes.go:2023 msg="Listening on 127.0.0.1:11434 (version 0.31.1)" time=2026-07-08T02:56:43.753-03:00 level=INFO source=model\_list\_cache.go:111 msg="model list cache hydration complete" models=0 failures=0 elapsed=118.74µs time=2026-07-08T02:56:43.755-03:00 level=INFO source=runner.go:60 msg="discovering available GPUs..." time=2026-07-08T02:56:43.925-03:00 level=INFO source=model\_recommendations.go:177 msg="model recommendations cache sleep scheduled" wait=3h58m45.063556868s consecutive\_failures=0 time=2026-07-08T02:56:47.136-03:00 level=INFO source=types.go:32 msg="inference compute" id=0 filter\_id=0 library=ROCm compute=gfx906 name=ROCm0 description="AMD Radeon Pro VII" libdirs=ollama,rocm\_v7\_2 driver=0.0 pci\_id=0000:05:00.0 type=discrete total="16.0 GiB" available="15.9 GiB" time=2026-07-08T02:56:47.136-03:00 level=INFO source=routes.go:2073 msg="vram-based default context" total\_vram="16.0 GiB" default\_num\_ctx=4096

---

Excelente. Agora temos o diagnóstico definitivo.

## O erro está na sintaxe do ExecStart

O `journalctl` mostrou:

```
Unable to locate executable '/usr/bin/ollama serve'
```

O `systemd` está tentando encontrar um **arquivo chamado literalmente**:

```
/usr/bin/ollama serve
```

Isso significa que o arquivo de serviço foi escrito incorretamente.

### O correto é:

```
ExecStart=/usr/bin/ollama serve
```

**sem aspas** e em uma única linha.

### O incorreto (e que produz exatamente esse erro) é algo como:

```
ExecStart="/usr/bin/ollama serve"
```

ou

```
ExecStart='/usr/bin/ollama serve'
```

Nesses casos, o `systemd` interpreta **toda a string** como o caminho do executável.

---

## Vamos confirmar

Mostre exatamente estas linhas:

```bash
sed -n '1,30p' /etc/systemd/system/ollama.service

echo "----------------"

sed -n '1,30p' /etc/systemd/system/ollama.service.d/override.conf
```

Quero ver a linha exatamente como foi salva.

---

## O teste manual prova que o Ollama está perfeito

Você executou:

```bash
sudo -u johncoffee /usr/bin/ollama serve
```

E ele iniciou normalmente:

- ✅ Versão 0.31.1
- ✅ Detectou a MI50 (`gfx906`)
- ✅ ROCm funcionando
- ✅ 16 GB de VRAM
- ✅ Servidor ouvindo em `127.0.0.1:11434`

Ou seja:

**O Ollama não tem problema nenhum.**

O único problema restante é a configuração do `systemd`.

---

## Há mais uma coisa que eu corrigiria

Nos logs do teste manual apareceu:

```
OLLAMA_MODELS=/home/johncoffee/.ollama/models
```

Mas seu AI-Lab usa:

```
OLLAMA_MODELS=/mnt/win2/Assistente Pessoal2/data/ollama_models
```

Se você pretende que o serviço do `systemd` seja a forma oficial de iniciar o Ollama, confirme depois que essa variável está realmente sendo aplicada quando o serviço iniciar, pois no teste manual ela não foi usada (o que é esperado, já que você iniciou o binário diretamente, fora do `systemd`).

---

### Minha recomendação para o AI-Lab

Como você está consolidando essa infraestrutura, eu eliminaria a duplicação entre o `daemon.py` e o `systemd`. O mais robusto seria o `daemon.py` apenas verificar e controlar o serviço:

```
daemon.py
    ├── systemctl start ollama
    ├── systemctl stop ollama
    ├── systemctl restart ollama
    └── health-check
```

Assim toda a configuração (GPU, modelos, variáveis de ambiente, usuário, reinício automático) fica centralizada em um único lugar: o serviço do `systemd`. Isso reduz bastante a chance de divergências como as que você encontrou hoje.

---

**Você disse**

/mnt/win2/Assistente Pessoal2 ❯ sed -n '1,30p' /etc/systemd/system/ollama.service echo "----------------" sed -n '1,30p' /etc/systemd/system/ollama.service.d/override.conf \[Unit\] Description=Ollama Service After=network-online.target \[Service\] ExecStart=/usr/bin/ollama serve User=ollama Group=ollama Restart=always RestartSec=3 Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/bin" \[Install\] WantedBy=default.target ---------------- \[Service\] Environment="ROCR\_VISIBLE\_DEVICES=0" Environment="HIP\_VISIBLE\_DEVICES=0" ExecStart= ExecStart="/usr/bin/ollama serve" Environment="HSA\_OVERRIDE\_GFX\_VERSION=9.0.6" Environment="ROCM\_PATH=/opt/rocm" Environment="OLLAMA\_MODELS=/mnt/win2/Assistente Pessoal2/data/ollama\_models" Environment="OLLAMA\_HOST=0.0.0.0:11434" Environment="OLLAMA\_NUM\_GPU=99" /mnt/win2/Assistente Pessoal2 ❯

---

Achamos o bug.

O erro está exatamente aqui:

```
ExecStart="/usr/bin/ollama serve"
```

No `systemd`, **o executável e os argumentos não podem ficar dentro da mesma string entre aspas**. Assim, ele tenta executar um arquivo chamado literalmente:

```
/usr/bin/ollama serve
```

que obviamente não existe.

## Corrija para:

```
[Service]
Environment="ROCR_VISIBLE_DEVICES=0"
Environment="HIP_VISIBLE_DEVICES=0"

ExecStart=
ExecStart=/usr/bin/ollama serve

Environment="HSA_OVERRIDE_GFX_VERSION=9.0.6"
Environment="ROCM_PATH=/opt/rocm"
Environment="OLLAMA_MODELS=/mnt/win2/Assistente Pessoal2/data/ollama_models"
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_NUM_GPU=99"
```

Observe que:

- ✅ `ExecStart=` continua vazio para limpar a definição anterior.
- ✅ `ExecStart=/usr/bin/ollama serve` **não tem aspas**.

Depois execute:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
systemctl status ollama
ollama --version
```

---

## Mais duas melhorias importantes

Analisando sua configuração, eu também faria estas correções:

### 1\. Remover /usr/local/bin do PATH

Hoje você tem:

```
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/bin"
```

Como você já removeu a instalação manual do Ollama, eu deixaria:

```
Environment="PATH=/usr/local/sbin:/usr/bin"
```

ou simplesmente removeria essa linha, deixando o `systemd` usar o `PATH` padrão, a menos que haja uma necessidade específica.

### 2\. Consolidar os arquivos de configuração

Você tem:

- `ollama.service`
- `gpu.conf`
- `override.conf`

Todos alteram o mesmo serviço. Para facilitar manutenção, eu concentraria todas as customizações do AI-Lab em **um único drop-in** (por exemplo, `ailab.conf`) e deixaria o serviço principal o mais próximo possível do padrão do pacote. Isso reduz a chance de conflitos em futuras atualizações.

---

Depois de remover as aspas, o serviço deve iniciar normalmente e você poderá testar novamente:

```bash
ai-lab pull gemma4:26b-a4b-it-qat
```

Se ainda houver algum problema, a partir daí provavelmente será relacionado apenas à versão mínima exigida pelo modelo, e não mais à configuração do serviço.