---
tags:
  - texto
source: "textos, pdf e esquemas"
---

# modo escuro via cmd

# Forçar modo escuro para apps (HKCU)
Reg.exe add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v "AppsUseLightTheme" /t REG_DWORD /d 0 /f | Out-Null

# Edge tema (HKCU)
Reg.exe add "HKCU\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppContainer\Storage\microsoft.microsoftedge_8wekyb3d8bbwe\MicrosoftEdge\Main" /v "Theme" /t REG_DWORD /d 1 /f | Out-Null

# Forçar modo escuro global (HKLM) -> precisa de PowerShell como admin
Reg.exe add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\DefaultColors\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f | Out-Null
