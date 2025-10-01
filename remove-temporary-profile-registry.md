# Remove Temporary Profile (Registry)

> ⚠️ Be careful editing the registry.

1. `Win + R` → `regedit` → go to:  
   `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList`
2. Find twin SIDs: one with **.bak** (original), one without (temp).
3. Rename temp (no .bak) → `.temp`. Remove `.bak` suffix from original.
4. Set **State** and **RefCount** to `0`. Reboot and test.
