# Autonomy Map — Digital View

> Diagnóstico del nivel de autonomía actual por fase operativa, qué falta para cerrar el loop, y backlog priorizado por ROI.
> Fecha: 2026-05-08

## Niveles de autonomía (definición)

- **L0 — Manual**: humano hace 100%.
- **L1 — Asistido**: IA sugiere, humano ejecuta y valida.
- **L2 — Semi-auto**: IA ejecuta, humano valida en gate.
- **L3 — Auto con gate**: IA ejecuta end-to-end, humano solo aprueba en checkpoints críticos (push a Meta, envío al cliente).
- **L4 — Full-auto**: IA ejecuta sin gate (solo apto para tareas internas reversibles).

**Meta DV**: L3 en producción interna (ideación, validación, reportes), L2 en touchpoints con cliente, L4 sólo en housekeeping (state, logs, indexes).

---

## Snapshot por fase

| Fase | Hoy | Target | Brecha |
|---|---|---|---|
| 1 — Comercial (lead → reunión → propuesta) | **L1** | L2 | Falta: ingesta automática lead → scoring → preparación reunión → seguimiento |
| 2 — Onboarding | **L1** | L3 | Falta: kickoff que dispare creación brand JSON + Drive + ficha sin Elias tipeando |
| 3 — Preproducción y estáticos | **L2** | L3 | Maduro. Falta: auto-aprobación interna por validators + handoff sin click |
| 4 — Producción / postproducción | **L0** | L1 | Editores 100% manual. Sólo `video_ai` scaffold. |
| 5 — Pauta | **L2** | L3 | Sheet → Meta funciona. Falta: auto-trigger desde gate fase 3 + auto-validación brief |
| 6 — Lanzamiento y seguimiento | **L2** | L3 | Reportes semanales corren por cron. Falta: auto-envío al cliente + acción sobre alertas SCALE/KILL |

---

## Inventario de lo automatizado HOY

### Crons activos (`cron_runner.py`)
- `recompute-state` (6h) — recalcula state + reindexa assets
- `daily-monitor` (08:30) — insights día anterior + alerta WA si KILL/ITERATE/freq≥3
- `process-creative-briefs` (09:00) — notifica a Nico briefs pendientes
- `health` (6h) — chequea SLA + alerta a Felipe

### Scripts operativos
- `02_comercial/meta_leads_puller.py` + `csv_importer.py` + `leads_clientes.py` — ingesta de leads Meta + CSV frío
- `02_comercial/pipeline.py` — pipeline comercial
- `01_contenido/design/render_editorial.py` + `generate.py` + `upload_drive.py` — render carruseles + push a Drive
- `01_contenido/creative_director/market_research.py`
- `04_pauta/*` (Media Buyer Sheet→Meta operativo end-to-end)
- `.claude/scripts/pre_commit_validators.py` — gate de tono y naming

### Skills disponibles
- **Coordinador**: `/kickoff`, `/nueva-campana`, `/status`, `/buscar`
- **Copywriter**: `/meta-ad`, `/caption`, `/banco-hooks`, `/estrategia-copy`
- **Creative Director**: skills de guion + brief
- **Design**: `/data-visualizer`, render editorial
- **Comercial**: `/preparar-reunion`
- **Delivery**: `/checklist-fase`, `/reporte-semanal`, `/reporte-mensual`
- **Validators (subagents)**: tono, naming, hook-scorer, guion, brief-pauta, fase-gate

### Brand system
- `shared/brands/<cliente>.json` — fuente única de verdad multi-cliente, leído dinámicamente

---

## Cuellos de botella reales (ranking por costo de horas/semana)

### #1 — Aprobaciones humanas síncronas (Nico/Elias/Valentin)
**Problema**: cada pieza de copy/guion/diseño espera un humano que diga "ok" en WA. Bloquea 3 fases (3, 5, 6).
**Hoy**: validators corren pero no decretan handoff. Humano sigue siendo el gate.
**Solución**: política de **auto-aprobación interna** — si tono+naming+guion+hook PASS y nadie objeta en N horas, el output se considera aprobado para handoff interno (sigue requiriendo OK humano para enviar a cliente).
**Impacto**: ~6–10h/sem de Nico+Elias.

### #2 — Onboarding manual (Fase 2)
**Problema**: cada cliente nuevo es 4–6h tipeando ficha + creando estructura Drive + cargando brand JSON.
**Hoy**: skill `/kickoff` existe pero no dispara automatización completa.
**Solución**: `/kickoff <cliente>` que: (a) genera brand JSON desde formulario CORE, (b) crea estructura Drive vía MCP, (c) inicializa pipeline.json, (d) registra en `shared/brands/`, (e) avisa a equipo por WA.
**Impacto**: 4h por cliente nuevo × N clientes/mes.

### #3 — Producción de video (Fase 4)
**Problema**: 100% manual con editores humanos. `video_ai` está vacío.
**Hoy**: L0.
**Solución realista**: NO automatizar edición creativa. Sí automatizar: (a) ingesta de crudos a Drive con naming validado, (b) auto-thumbnails, (c) auto-subtítulos (Whisper), (d) auto-corte de versiones (9:16, 1:1, 16:9) con ffmpeg. Esto libera 30–50% del tiempo de editor.
**Impacto**: 8–15h/sem repartidas entre 3 editores.

### #4 — Loop de feedback Pauta → Creativo
**Problema**: Felipe detecta fatiga/SCALE/KILL pero el brief creativo de vuelta a Nico es manual.
**Hoy**: `process-creative-briefs` notifica pero no genera el brief.
**Solución**: cuando un ad llega a KILL/ITERATE, auto-generar `brief_creativo.md` con: ángulo que falló, datos, hipótesis nueva, hook framework sugerido. Nico recibe el brief listo, no la alerta cruda.
**Impacto**: cierra el loop performance → contenido sin reuniones.

### #5 — Reportes a cliente
**Problema**: reporte semanal se genera pero Elias lo copia/pega/edita/manda.
**Solución**: `auto-deliver` — si el reporte semanal pasa validators, se manda al cliente directo por WA con un mensaje template. Gate humano sólo si hay anomalías (CPL fuera de rango, sin leads en 3 días).
**Impacto**: 2–3h/sem de Elias.

### #6 — Comercial (Fase 1)
**Problema**: leads de pauta de DV mismo + leads fríos viven en pipeline pero el seguimiento es manual.
**Hoy**: ingesta automatizada, scoring no.
**Solución**: scoring ICP automático + secuencia de outreach con drafts WA listos para Valentin.
**Impacto**: difícil de cuantificar, alto ROI si destrabas pipeline.

---

## Plan de ataque sugerido (orden de implementación)

### Sprint 1 (semana 1-2) — Quick wins de alto ROI
1. **Auto-aprobación interna por validators** — política + script que marque outputs PASS como "ready for handoff" sin esperar a Nico. (#1)
2. **Auto-brief creativo desde KILL/ITERATE** — extender `daily-monitor` para que escriba brief estructurado a `creative_director/inbox/`. (#4)
3. **Auto-deliver reporte semanal** si PASS validators + métricas en rango. (#5)

### Sprint 2 (semana 3-4) — Cierre del loop comercial
4. **Scoring ICP automático** sobre `leads_clientes.json`. (#6)
5. **Drafts de seguimiento WA** para Valentin (1-click send).

### Sprint 3 (semana 5-6) — Onboarding y producción
6. **`/kickoff` end-to-end** con MCP Drive + brand JSON gen. (#2)
7. **Pipeline de producción audiovisual asistida**: subtítulos auto, multi-format, naming validado. (#3)

### Sprint 4 (semana 7+) — Observabilidad
8. **Dashboard único** (`/status` ampliado): semáforo por cliente × fase, alertas, pendientes humanos.
9. **MCP server propio DV** (opcional): expose pipeline, brands, outputs como recursos para Claude desde cualquier sesión.

---

## Principios de diseño

1. **Humanos en gates de riesgo, no en gates de proceso.** Aprobar copy interno = automatizable. Aprobar mensaje al cliente = humano.
2. **Validators son hard gates, no sugerencias.** Si tono falla → no pasa, sin excepción.
3. **Todo cron tiene log + alerta WA si falla.** Ya está parcial, completar.
4. **Default-deny en touchpoints con cliente.** Nada se manda sin OK humano salvo reportes 100% verdes.
5. **Cada automatización rinde cuentas en `cron_log.jsonl`** (lo que no se mide, se rompe).

---

## Métricas de éxito

- Horas/semana del equipo en tareas operativas → bajar 40% en 8 semanas.
- Time-to-launch de campaña nueva (kickoff → ads vivos) → de 7-10 días a 2-3 días.
- % de outputs que pasan validators al primer intento → >85%.
- Clientes activos que el equipo puede manejar sin sumar gente → 2x.
