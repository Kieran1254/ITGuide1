# RMM (N‑able) – Remotely Add Local Admin

Run in **Remote Background** (Admin CMD):

```
net user "Firstname.Lastname" "TempPass123!" /add
net localgroup Administrators "Firstname.Lastname" /add
```
