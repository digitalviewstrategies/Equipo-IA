# Cron — Setup en Windows Task Scheduler

`cron_runner.py` orquesta tres tareas recurrentes:

| Tarea | Frecuencia recomendada | Que hace |
|---|---|---|
| `recompute-state` | Cada 6 hs | Recalcula `shared/state/<cliente>.json` por filesystem |
| `daily-monitor`   | Diario 08:30 | Trae insights del dia anterior y escribe alerta si hay KILL/fatiga |
| `weekly-report`   | Lunes 09:00 | Reporte semanal markdown por cliente con campanas |
| `pull-leads`      | Cada 4 hs   | Trae leads de Meta Lead Ads y los inserta en pipeline comercial |

Output:
- Reportes/alertas: `agentes/04_pauta/outputs/<cliente>/<fecha>/`
- Log: `shared/state/cron_log.jsonl`

## Registrar tareas (PowerShell, una sola vez)

```powershell
$proj = "C:\Users\proba\Documents\Felipe\Claude\Equipo-IA"
$py   = "python"

# 1. Recompute state cada 6 hs
schtasks /Create /SC HOURLY /MO 6 /TN "DV-Recompute-State" `
    /TR "$py `"$proj\agentes\00_coordinador\scripts\cron_runner.py`" recompute-state" /F

# 2. Daily monitor 08:30
schtasks /Create /SC DAILY /ST 08:30 /TN "DV-Daily-Monitor" `
    /TR "$py `"$proj\agentes\00_coordinador\scripts\cron_runner.py`" daily-monitor" /F

# 3. Weekly report lunes 09:00
schtasks /Create /SC WEEKLY /D MON /ST 09:00 /TN "DV-Weekly-Report" `
    /TR "$py `"$proj\agentes\00_coordinador\scripts\cron_runner.py`" weekly-report" /F
```

## Verificar / desregistrar

```powershell
schtasks /Query /TN "DV-Daily-Monitor"
schtasks /Run   /TN "DV-Daily-Monitor"   # corre ahora
schtasks /Delete /TN "DV-Daily-Monitor" /F
```

## Inspeccionar log

```powershell
Get-Content "$proj\shared\state\cron_log.jsonl" -Tail 20
```

## Probar manualmente antes de schedulear

```powershell
cd $proj
python agentes\00_coordinador\scripts\cron_runner.py recompute-state
python agentes\00_coordinador\scripts\cron_runner.py daily-monitor
python agentes\00_coordinador\scripts\cron_runner.py weekly-report
```

## Notas

- Requiere `agentes/04_pauta/.env` con `META_ACCESS_TOKEN` y `agentes/04_pauta/credentials/google_service_account.json`.
- Las alertas diarias solo se generan si hay ads en `KILL` / `ITERATE` o `frequency >= 3.0`. Si todo va bien, no genera ruido.
- Si un cliente no tiene `meta_ads.ad_account_id` en su brand JSON, se saltea silenciosamente.
