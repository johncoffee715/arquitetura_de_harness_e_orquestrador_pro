---
tags:
  - texto
source: "textos, pdf e esquemas"
---

# desativar o Controle de Conta de Usuário do Windows

REG ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /V EnableLUA /T REG_DWORD /D 0 /F