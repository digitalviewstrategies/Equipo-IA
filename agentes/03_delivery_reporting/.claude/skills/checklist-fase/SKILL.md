---
name: checklist-fase
description: Use this skill to validate that all deliverables of a given DV operational phase are complete before moving to the next one. Triggers "checklist de fase [N] para [cliente]", "podemos avanzar a fase [N] con [cliente]", "que falta para pasar a produccion con [cliente]", "validar fase [N] de [cliente]", "estamos listos para [pauta/produccion/lanzamiento]", "checklist de onboarding de [cliente]".
---

# Skill: Checklist de Fase

Valida que todos los entregables de una fase del proceso DV están completos antes de avanzar. La regla de oro es que ninguna fase avanza si la anterior no está cerrada.

## Antes de ejecutar

Necesitás:
1. **Cliente** (nombre exacto en `shared/brands/`).
2. **Fase** (número del 1 al 6, o nombre: "comercial", "onboarding", "preproduccion", "produccion", "pauta", "seguimiento").

## Mapeo de fases

| Input | Fase |
|---|---|
| 1, "comercial" | Fase 1 — Comercial |
| 2, "onboarding" | Fase 2 — Onboarding |
| 3, "preproduccion", "preproducción", "contenido" | Fase 3 — Preproducción |
| 4, "produccion", "producción", "postproduccion" | Fase 4 — Producción |
| 5, "pauta", "campana", "campaña" | Fase 5 — Pauta |
| 6, "seguimiento", "lanzamiento", "reportes" | Fase 6 — Seguimiento |

## Pasos

### 1. Leer el contexto de la fase

```python
# Lee context/fases_operativas.md para el detalle de entregables de la fase pedida
```

### 2. Evaluar entregables con el helper compartido

```python
from scripts.output_manager import get_phase_gaps
info = get_phase_gaps(cliente, fase=numero)
```

`info` trae:
- `items`: lista completa de entregables con `status` ('ok' | 'falta' | 'manual'), `responsable`, `criticidad`.
- `gaps`: solo los faltantes o no verificables.
- `gaps_criticos`: los críticos que bloquean el avance.
- `puede_avanzar`: bool.

Esta es la misma fuente de verdad que consume `/reporte-semanal` para la sección "Atención para la próxima semana", así no hay divergencia entre ambas skills.

### 3. Generar el checklist

Mapeo de `status` a marca:
- `ok` → **[x]** (verificado en repo).
- `falta` → **[ ]** (no hay evidencia, indicá responsable y acción).
- `manual` → **[?]** (no verificable automáticamente, indicá quién confirma).

Formato del checklist:

```markdown
# Checklist Fase [N] — [nombre de la fase] — [Cliente]
**Fecha:** [hoy]

## Estado: [COMPLETA / INCOMPLETA / PENDIENTE CONFIRMACIÓN]

### Entregables
- [x] [Entregable verificado automáticamente]
- [ ] [Entregable faltante — qué falta y quién lo resuelve]
- [?] [Entregable no verificable — quién confirma: Elias / Bauti / Valentin / Felipe]

### Bloqueantes para avanzar
[Lista de lo que falta, con responsable y acción concreta]

### Próximo paso
[Qué hacer ahora mismo para desbloquear]
```

### 4. Guardar

```python
from scripts.output_manager import save_output
save_output(cliente, f"checklist_fase{numero}", f"{cliente}", checklist)
```

## Entrega

Mostrá el checklist con estado claro. Decí explícitamente si se puede o no avanzar a la siguiente fase.

```
[PUEDE AVANZAR / NO PUEDE AVANZAR]. Faltan [N] items bloqueantes.
Va para [Elias / Bauti / quien corresponda] para resolver: [items pendientes].
```

No suavices el estado. Si no está lista la fase, decilo directamente.
