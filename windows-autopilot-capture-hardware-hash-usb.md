# Windows Autopilot – Capture Hardware Hash

1. On another PC (admin PowerShell):
   ```powershell
   Install-Script Get-WindowsAutoPilotInfo
   ```
2. Copy `Get-WindowsAutoPilotInfo.ps1` to USB, plus a `GetAutoPilot.cmd`:

```
@ECHO OFF
PowerShell -NoProfile -ExecutionPolicy Unrestricted -Command Enable-PSRemoting -SkipNetworkProfileCheck -Force
PowerShell -NoProfile -ExecutionPolicy Unrestricted -Command %~dp0Get-WindowsAutoPilotInfo.ps1 -ComputerName $env:computername -OutputFile %~dp0compHash.csv -append
pause
```
3. Run the cmd on target device to generate `compHash.csv`.
