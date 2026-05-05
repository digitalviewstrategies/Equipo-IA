---
name: check-fase-gate
description: "Corre el set completo de validators para el gate de una fase operativa de Digital View (3 preproducción, 4 producción, 5 pauta, 6 lanzamiento) sobre los outputs de un cliente y una fecha. Devuelve veredicto consolidado GATE OPEN / GATE CLOSED. Usar antes de cerrar una fase y avanzar a la siguiente. Argumentos: <fase> <cliente> [<fecha YYYY-MM-DD>]. Si no se pasa fecha, usa hoy."
---

# /check-fase-gate

Skill para correr el gate completo de una fase. Reemplaza la pasada manual de validator-por-validator. Es el chequeo que se corre **antes de avanzar de fase** según la regla de oro DV: ninguna fase avanza si los controles de la anterior no están completos.

## Uso

```
/check-fase-gate <fase> <cliente> [<fecha>]
```

Ejemplos:
- `/check-fase-gate 3 ini_propiedades 2026-05-04`
- `/check-fase-gate 5 digital_view`  (fecha = hoy)
- `/check-fase-gate 6 lopez_props 2026-05-10`

## Mapeo fase → validators

| Fase | Nombre | Validators que corre | Sobre qué |
|---|---|---|---|
| 3 | Preproducción | `guion-validator` + `tono-brand-validator` | `agentes/02_creativo/outputs/<cliente>/<fecha>/guion_*.md` y `agentes/02_creativo/outputs/<cliente>/<fecha>/guiones/**/*.md` |
| 4 | Producción/Postpo | `naming-validator --drive` | Todos los archivos en `agentes/*/outputs/<cliente>/<fecha>/` |
| 5 | Pauta | `brief-pauta-validator` + `naming-validator --meta` + `tono-brand-validator` | `plan_campana*.md` + `campaigns_*.csv` + creativos en `agentes/04_pauta/outputs/<cliente>/<fecha>/` |
| 6 | Lanzamiento | `naming-validator --meta` + `brief-pauta-validator` | Re-check de `plan_campana*.md` + `campaigns_*.csv` finales |

## Procedimiento

1. Parseá args: `fase`, `cliente` (brand_id), `fecha` (default = hoy en `YYYY-MM-DD`).
2. Resolvé los paths reales con Glob según la fila de la tabla.
3. Si **no hay archivos** que matcheen: imprimí "Nada para validar en fase X / cliente Y / fecha Z" y veredicto **GATE CLOSED — sin artifacts**.
4. Para cada validator de la fase, invocalo en paralelo (Task tool) con el path de los archivos correspondientes. Pasale el `cliente` como brand activa explícita.
5. Recolectá los outputs.
6. Generá tabla consolidada y veredicto final.

## Output

```
# Gate de fase — Fase <N>: <Nombre>
**Cliente:** <brand_id> | **Fecha:** <YYYY-MM-DD>
**Artifacts auditados:** <count> archivos

## Resultados por validator

| Validator | Archivo | Veredicto | Bloqueantes |
|---|---|---|---|
| guion-validator | guion_reel_captacion.md | APTO | — |
| tono-brand-validator | guion_reel_captacion.md | OK | — |
| naming-validator --meta | campaigns_2026-05-04.csv | GATE CLOSED | 2 nombres mal formados |

## Resumen
- Validators corridos: N
- PASS/APTO/OK: N
- FLAG/REVISAR: N
- BLOCK/NO APTO/GATE CLOSED: N

## Veredicto del gate
**<GATE OPEN | GATE CLOSED>**

<si CLOSED, lista compacta de bloqueantes — qué hay que arreglar antes de re-correr>
```

## Reglas duras

- **GATE OPEN** solo si: 0 BLOCK + 0 NO APTO + 0 GATE CLOSED en cualquier validator. FLAG/REVISAR no bloquea pero se reporta.
- Si un validator falla por falta de artifacts (ej. fase 5 sin `plan_campana*.md`): GATE CLOSED.
- No avanzás de fase sin GATE OPEN. Esto no es sugerencia, es regla DV.

## Lo que NO hace

1. No corrige nada. Solo audita.
2. No invoca validators que no aplican a la fase pedida (ej. no corre `brief-pauta-validator` en fase 3).
3. No infiere fase. Si el usuario no pasa `<fase>`, pedila y cortá.
4. No hardcodea cliente. Usa el brand_id pasado como argumento (es la única excepción al `.claude/active_client` — acá la skill recibe el cliente explícito por argumento para que sirva en gates multi-cliente del mismo día).

## Auto-verificación antes de entregar

- ¿Args parseados correctamente (fase, cliente, fecha)?
- ¿Paths resueltos con Glob, no asumidos?
- ¿Cada validator de la fase fue invocado?
- ¿Tabla consolidada lista cada validator + archivo + veredicto?
- ¿Veredicto final coincide con la regla (1+ BLOCK = CLOSED)?
