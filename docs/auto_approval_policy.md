# Política de Auto-Aprobación Interna — DV

> Quién aprueba qué, cuándo, y cómo se revierte.
> Sprint 1 del autonomy map. Versión 1 — 2026-05-08.

## Qué es

Cuando un agente DV (copywriter, creative_director, design, etc.) produce un output bajo `agentes/**/outputs/<cliente>/<fecha>/`, un proceso automático corre los validators y escribe un sidecar `<archivo>.status.json` con el veredicto. Si todo PASA, el output queda **listo para handoff interno** sin esperar a que un humano lo apruebe.

**Esto NO reemplaza la aprobación del cliente.** Reemplaza el "ok" interno entre agentes DV.

## Qué se auto-aprueba

| Tipo de output | Auto-aprueba si... | Sino, queda en... |
|---|---|---|
| `*.md` bajo outputs/ | tono PASS (sin `forbidden_words`) | `needs_human` |
| Binarios (`.mp4`, `.png`, `.jpg`, `.pdf`) | naming PASS (`<CLIENTE>_<Tipo>_V<n>.<ext>`) | `needs_human` |
| Output sin brand resoluble | nunca | sin sidecar |

## Qué NUNCA se auto-aprueba (gate humano obligatorio)

1. **Push de campañas a Meta Ads** — Felipe siempre revisa el plan antes de correr el script de creación.
2. **Envío de mensajes/reportes al cliente** — Elias OK explícito antes de mandar (excepción: reporte semanal con todo PASS y métricas en rango — se delegará en Sprint 1.3).
3. **Decisiones comerciales** (fee, scope, contrato) — Valentin.
4. **Decisiones creativas de concepto** (línea editorial nueva, cambio de estética) — Nico.
5. **Cualquier output flageado como `needs_human`** — humano dueño de la fase resuelve.

## Schema del sidecar (v1)

```json
{
  "schema_version": 1,
  "output_path": "agentes/.../outputs/<cliente>/<fecha>/<file>.md",
  "brand": "<cliente>",
  "validators": {
    "tono":   {"status": "PASS|FAIL", "violations": [...]},
    "naming": {"status": "PASS|FAIL|N/A", "detail": "..."}
  },
  "status": "ready_for_handoff | needs_human",
  "approved_at": "<iso8601>",
  "approved_by": "auto-validators-v1",
  "notes": ""
}
```

Convención de path: `<archivo>.status.json` al lado del output.

## Cómo se dispara

- **CLI manual** (re-validar al toque):
  ```
  python .claude/scripts/auto_approve.py                    # hoy + ayer
  python .claude/scripts/auto_approve.py <cliente>          # un cliente, todas las fechas
  python .claude/scripts/auto_approve.py <cliente> <YYYY-MM-DD>
  python .claude/scripts/auto_approve.py --rerun            # ignora sidecars previos
  ```
- **Cron** (cada 6h, vía `cron_runner.py auto-approve`).

## Cómo revertir / cómo apelar

1. **Override manual**: editá el sidecar y poné `"status": "needs_human"` con `"notes": "<por qué>"`. Próxima corrida no lo pisa salvo `--rerun`.
2. **Re-ejecución**: borrá el sidecar (`rm <file>.status.json`) y re-corré el script.
3. **Bloqueo permanente**: agregá la frase ofensora al `forbidden_words` del brand JSON. La próxima validación va a flaguearla siempre.

## Qué hace cada actor

| Actor | Responsabilidad |
|---|---|
| Sistema (cron) | Validar y escribir sidecar cada 6h |
| Agente productor (copywriter, etc.) | Producir outputs en path correcto, con brand resoluble |
| Coordinador (`/status`) | Reportar cuántos outputs están en `ready_for_handoff` vs `needs_human` |
| Humano dueño (Nico/Elias/Felipe) | Resolver `needs_human` |

## Limitaciones conocidas (v1)

- Tono valida solo `forbidden_words` (regex). Capa semántica de `principles` la sigue haciendo el subagent `tono-brand-validator` invocado a mano.
- Hooks no se scorean automáticamente todavía — eso queda para `hook-scorer` invocado por skill.
- Brief-pauta no se valida automáticamente todavía (subagent dedicado).
- Los sidecars no tienen TTL — si cambia el brand JSON, hay que correr `--rerun` para revalidar.

## Integraciones activas

- **`process_creative_briefs.py`** — antes de notificar a Nico, gate del sidecar. Si `needs_human`, alerta a Felipe en lugar de spamear a Nico con brief roto.
- **`auto_deliver.py`** — antes de spawnear el subproceso `claude /reporte-semanal`, gate del sidecar. Si `needs_human`, no dispara y alerta a Felipe.

## Próximos pasos (siguientes sprints)

- v2: integrar capa semántica del `tono-brand-validator` (LLM).
- v3: validar hook-score automático.
- v4: gate de métricas en rango (CPL/leads) además del gate de tono, antes de auto-deliver.
- v5: send-to-client directo (sin pasar por Elias) cuando todo PASS + métricas en rango + cliente opt-in.
