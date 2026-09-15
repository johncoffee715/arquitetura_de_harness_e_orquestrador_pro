---
name: awesome-policy-as-code
description: Policy-as-code taxonomy — OPA/Rego, Sentinel, Kyverno/Gatekeeper, IaC scanners (Checkov/Terrascan/KICS), Cloud Custodian.
category: skill
model: local-forge/proposer
---

# awesome-policy-as-code

Taxonomia policy-as-code: onde cada família atua (admission, IaC-scan, runtime,
cloud-governance) e com que ferramenta. Helenizado de `hysnsec/awesome-policy-as-code`
(origem: https://github.com/hysnsec/awesome-policy-as-code, CC0-1.0).

## Quando usar

- Escolher ferramenta de policy (OPA vs Sentinel vs Kyverno vs scanner)
- Cobrir IaC (Terraform/CloudFormation/K8s manifests) pré-deploy
- Governança cloud contínua (custo, segurança, compliance)

## Taxonomia

| Camada | Ferramentas |
|---|---|
| Engine genérico | OPA/Rego, Styra DAS, OPAL, Topaz |
| K8s admission | Gatekeeper, Kyverno, MagTape, Konstraint |
| IaC scan | Checkov, Terrascan, KICS, Regula, Fregot |
| Cloud governance | Cloud Custodian |
| Linguagem embed | Sentinel (HashiCorp) |

## Princípio

Policy no pipeline (CI/admission), não no improviso: bloquear pré-deploy, auditar pós.
