# Cron — Setup en Windows Task Scheduler

`cron_runner.py` orquesta tareas recurrentes:

| Tarea | Frecuencia recomendada | Que hace |
|---|---|---|
| `recompute-state`         | Cada 6 hs     | Recalcula `shared/state/<cliente>.json` + reindex assets |
| `daily-monitor`           | Diario 08:30  | Insights del dia anterior. Alerta si hay KILL/fatiga + brief auto a Creative Director |
| `weekly-report`           | Lunes 09:00   | Reporte semanal markdown por cliente con campanas |
| `pull-leads`              | Cada 4 hs     | Trae leads de Meta Lead Ads a `02_comercial`. Si hay nuevos, alerta WA a Elias (`lead_alerts.notify`) |
| `process-creative-briefs` | Diario 09:00  | Notifica a Nico por WA los briefs auto pendientes |
| `prescore-leads`          | Cada 4 hs     | Auto-prescore de leads en pre_filtro: priority + knockouts + red_flags |
| `lead-followups`          | Cada 4 hs     | Drafts WA primer contacto para leads priority 1/2 sin knockouts |
| `auto-approve`            | Cada 6 hs     | Corre validators sobre outputs recientes, escribe sidecar `.status.json` |
| `health`                  | Cada 6 hs     | Chequea SLA de tareas. Alerta a Felipe por WA si algo no corre |

Output:
- Reportes/alertas: `agentes/04_pauta/outputs/<cliente>/<fecha>/`
- Log: `shared/state/cron_log.jsonl`

## Registrar tareas (PowerShell, una sola vez)

**IMPORTANTE**: usar `/RU SYSTEM` para que corran sin login. La version anterior usaba "Solo interactivo" y se caia si la PC quedaba sin login.

```powershell
$proj = "C:\Users\proba\Documents\Felipe\Claude\Equipo-IA"
$py   = "python"
$cr   = "$proj\agentes\00_coordinador\scripts\cron_runner.py"

# 1. Recompute state cada 6 hs
schtasks /Create /SC HOURLY /MO 6 /TN "DV-Recompute-State" /RU SYSTEM `
    /TR "$py `"$cr`" recompute-state" /F

# 2. Daily monitor 08:30
schtasks /Create /SC DAILY /ST 08:30 /TN "DV-Daily-Monitor" /RU SYSTEM `
    /TR "$py `"$cr`" daily-monitor" /F

# 3. Weekly report lunes 09:00
schtasks /Create /SC WEEKLY /D MON /ST 09:00 /TN "DV-Weekly-Report" /RU SYSTEM `
    /TR "$py `"$cr`" weekly-report" /F

# 4. Pull leads cada 4 hs
schtasks /Create /SC HOURLY /MO 4 /TN "DV-Pull-Leads" /RU SYSTEM `
    /TR "$py `"$cr`" pull-leads" /F

# 5. Process creative briefs diario 09:00 (despues de daily-monitor)
schtasks /Create /SC DAILY /ST 09:00 /TN "DV-Process-Creative-Briefs" /RU SYSTEM `
    /TR "$py `"$cr`" process-creative-briefs" /F

# 6. Health check cada 6 hs
schtasks /Create /SC HOURLY /MO 6 /TN "DV-Health" /RU SYSTEM `
    /TR "$py `"$cr`" health" /F

# 7. Auto-approve outputs cada 6 hs
schtasks /Create /SC HOURLY /MO 6 /TN "DV-Auto-Approve" /RU SYSTEM `
    /TR "$py `"$cr`" auto-approve" /F

# 8. Prescore leads cada 4 hs
schtasks /Create /SC HOURLY /MO 4 /TN "DV-Prescore-Leads" /RU SYSTEM `
    /TR "$py `"$cr`" prescore-leads" /F

# 9. Lead followups drafts cada 4 hs (despues de prescore)
schtasks /Create /SC HOURLY /MO 4 /TN "DV-Lead-Followups" /RU SYSTEM `
    /TR "$py `"$cr`" lead-followups" /F
```

## Migrar tareas existentes a /RU SYSTEM

Si las tareas ya estan creadas en modo "Solo interactivo", reemplazarlas:

```powershell
schtasks /Delete /TN "DV-Recompute-State" /F
schtasks /Delete /TN "DV-Daily-Monitor" /F
schtasks /Delete /TN "DV-Weekly-Report" /F
schtasks /Delete /TN "DV-Pull-Leads" /F
# Luego correr el bloque de Registrar tareas
```

## Verificar / desregistrar

```powershell
schtasks /Query /FO LIST | Select-String "DV-" -Context 0,4
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
python agentes\00_coordinador\scripts\cron_runner.py process-creative-briefs
python agentes\00_coordinador\scripts\cron_runner.py health
```

## Variables requeridas en `agentes/03_delivery_reporting/.env`

```
REPORTES_WABA_TOKEN=...
REPORTES_PHONE_NUMBER_ID=...
ELIAS_WA_NUMBER=549...
NICO_WA_NUMBER=549...     # nuevo: para process-creative-briefs
FELIPE_WA_NUMBER=549...   # nuevo: para health alerts
```

Si `NICO_WA_NUMBER` falta, `process-creative-briefs` cae a `ELIAS_WA_NUMBER`.
Si `FELIPE_WA_NUMBER` falta, `health` solo printea (no alerta).

## Notas

- Requiere `agentes/04_pauta/.env` con `META_ACCESS_TOKEN` y `agentes/04_pauta/credentials/google_service_account.json`.
- Las alertas diarias solo se generan si hay ads en `KILL` / `ITERATE` o `frequency >= 3.0`.
- Si un cliente no tiene `meta_ads.ad_account_id` en su brand JSON, se saltea silenciosamente.
- `process-creative-briefs` deja sentinel `<brief>.notified` al lado del brief para no avisar dos veces.
