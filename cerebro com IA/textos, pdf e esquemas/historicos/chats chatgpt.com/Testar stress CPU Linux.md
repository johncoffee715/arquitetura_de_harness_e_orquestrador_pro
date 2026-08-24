---
title: "Testar stress CPU Linux"
source: "https://chatgpt.com/c/69faa518-3274-832b-8fae-2cb7a74bdf48"
author:
published:
created: 2026-07-17
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**Você disse**

test stress cpu

---

Direto ao ponto: formas práticas de estressar CPU no Linux (nível técnico).

### 1) Método rápido (já pronto)

Use o **stress-ng** — é o padrão profissional.

Instalar:

```bash
sudo pacman -S stress-ng   # Arch/CachyOS
sudo apt install stress-ng # Debian/Ubuntu
```

Rodar (usar todos os threads por 5 min):

```bash
stress-ng --cpu 0 --cpu-method matrixprod --verify --timeout 300s
```
- `--cpu 0` = usa 100% de todos os núcleos
- `matrixprod` = carga pesada real (melhor que loop vazio)
- `--verify` = detecta erro computacional (importante p/ estabilidade)

---

### 2) Método hardcore (carga máxima contínua)

```bash
stress-ng --cpu 0 --cpu-method all --aggressive --tz --timeout 600s
```
- `--aggressive` força uso mais pesado de instruções
- `--cpu-method all` varia padrões → pega instabilidade oculta

---

### 3) Alternativa leve (sem instalar nada)

```bash
yes > /dev/null &
```

Repita isso várias vezes.

Ex:

```bash
for i in (seq 1 (nproc))
    yes > /dev/null &
end
```

Para parar:

```bash
killall yes
```

---

### 4) Benchmark + stress real (nível engenheiro)

Use:

- sysbench
```bash
sysbench cpu --threads=$(nproc) --time=300 run
```

---

### 5) Monitoramento (ESSENCIAL)

Enquanto roda, acompanha:

```bash
htop
```

ou

```bash
watch -n 1 sensors
```

Se quiser algo mais bruto:

```bash
watch -n 0.5 "cat /proc/cpuinfo | grep MHz"
```

---

### 6) Interpretação técnica (o que observar)

- Queda de clock → thermal throttling
- Freeze / reboot → VRM / fonte / instabilidade
- Erro em `--verify` → problema real de CPU/RAM/IMC
- Oscilação de frequência → governor ou limite de energia

---

### Insight avançado (nível laboratório)

Se quiser subir nível:

- Combine CPU + RAM + IO:
```bash
stress-ng --cpu 0 --vm 2 --vm-bytes 80% --io 4 --timeout 600s
```
- Isso simula workload real (tipo render + swap + IO)

---

Se quiser, posso montar um **script automático de validação tipo burn-in profissional (com log, gráfico e fail detection)** pra você integrar no teu lab.