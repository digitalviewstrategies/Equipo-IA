# CLICKUP — DIGITAL VIEW
### Cómo está armado y cómo usarlo

**Versión**: 2.0 — Abril 2026
**Responsable del sistema**: Valentin Hechter
**Uso**: Interno. Todo el equipo.

---

## ÍNDICE

- [PARTE 1 — Estructura del workspace](#parte-1)
- [PARTE 2 — Cómo usar cada space](#parte-2)
- [PARTE 3 — Los templates](#parte-3)
- [PARTE 4 — Statuses y qué significan](#parte-4)
- [PARTE 5 — Rutina diaria y semanal](#parte-5)
- [PARTE 6 — Reglas de uso](#parte-6)

---

## PARTE 1 — ESTRUCTURA DEL WORKSPACE {#parte-1}

### 1.1 Vista general

El workspace se llama **Digital View's Workspace**. Tiene 4 spaces y 3 carpetas dentro de uno de ellos.

```
WORKSPACE: Digital View's Workspace
│
├── SPACE: COMERCIAL
│   ├── Lista: Pipeline de prospectos
│   └── Lista: Seguimiento post-reunión
│
├── SPACE: ONBOARDING
│   └── Lista: Onboarding por cliente
│
├── SPACE: PRODUCCIÓN
│   ├── Lista: Contenido por cliente
│   ├── Lista: Diseño y estáticos
│   └── Lista: Edición de video
│
└── SPACE: OPERACIONES
    ├── 📁 Carpeta: PAUTA
    │   ├── Lista: Setup de campañas
    │   └── Lista: Seguimiento semanal de campañas
    ├── 📁 Carpeta: DELIVERY
    │   ├── Lista: Reuniones y reportes
    │   └── Lista: Incidencias y reclamos
    └── 📁 Carpeta: MANAGEMENT
        ├── Lista: Tareas del equipo DV
        └── Lista: OKRs y métricas
```

**Nota**: el space COMERCIAL puede aparecer como "Space" en la UI. Renombrarlo manualmente a "COMERCIAL" en Settings del space.

### 1.2 Quién es responsable del sistema

**Dueño del sistema**: Valentin Hechter
**Ejecución operativa diaria**: Bauti R

Valentin es quien define la estructura, aprueba cambios al sistema y tiene la última palabra sobre cómo se usa ClickUp. Bauti R es quien corre la reunión semanal de revisión y onboardea a nuevos integrantes al uso del sistema. Si algo del sistema no funciona o necesita ajustarse, el reporte va directo a Valentin.

### 1.3 Principio fundamental

**Si no está en ClickUp, no existe.**

Tres excepciones únicas:
1. **Drive**: sigue siendo el repositorio de archivos. ClickUp tiene links a las carpetas, no reemplaza Drive.
2. **Sheets del CRM de leads**: el CRM del cliente sigue en Sheets. ClickUp trackea el proceso, no los datos del lead.
3. **WhatsApp**: sigue siendo el canal urgente con clientes. Pero cualquier acción que salga de ese WhatsApp se convierte en tarea en ClickUp.

---

## PARTE 2 — CÓMO USAR CADA SPACE {#parte-2}

### 2.1 SPACE: COMERCIAL

**Quién lo usa**: Valentin (principalmente) + Elias

**Lista: Pipeline de prospectos**

Cada prospecto es una tarea. Para crear una nueva:
1. Ir a COMERCIAL → Pipeline de prospectos
2. Click en "+ Nueva tarea"
3. Nombre de la tarea: nombre del prospecto o de la inmobiliaria
4. Asignar a Valentin o Elias
5. Completar el status inicial: **NUEVO**

Mover el status a medida que avanza la conversación:

| Status | Cuándo usarlo |
|---|---|
| NUEVO | Prospecto identificado, sin contacto aún |
| CONTACTADO | Se hizo el primer contacto |
| FIT CALL AGENDADA | Se agendó la llamada de filtro |
| FIT CALL REALIZADA | Se hizo la llamada, pasó el filtro |
| DISCOVERY AGENDADA | Se agendó la reunión de discovery |
| DISCOVERY REALIZADA | Se hizo el discovery, scorecard completado |
| PROPUESTA ENVIADA | Se presentó la propuesta comercial |
| EN NEGOCIACIÓN | Están evaluando o pidiendo ajustes |
| CERRADO — CLIENTE | Firmó contrato y pagó |
| CERRADO — NO AVANZÓ | Descartado o perdido |

**Lista: Seguimiento post-reunión**

Para prospectos que pasaron el discovery pero todavía no cerraron. Una tarea por prospecto con las acciones de seguimiento pendientes.

---

### 2.2 SPACE: ONBOARDING

**Quién lo usa**: Bauti R (responsable del sistema ClickUp) + Elias + Nico + Felipe según fase

**Lista: Onboarding por cliente**

Cada cliente nuevo que firma tiene su propia tarea acá. Se crea usando el **Template 1** (ver PARTE 3).

Pasos para arrancar el onboarding de un nuevo cliente:
1. Ir a ONBOARDING → Onboarding por cliente
2. Click en "+ Nueva tarea" → elegir "[TEMPLATE] Onboarding nuevo cliente"
3. Renombrar la tarea: `[NOMBRE CLIENTE] — Onboarding`
4. Asignar al PM responsable del cliente (Elias o Bauti R)
5. Poner deadline: 7 días hábiles desde la firma del contrato
6. Status inicial: **INICIADO**

El template ya trae todas las subtareas ordenadas. Ir marcándolas completadas a medida que avanzan.

| Status | Cuándo usarlo |
|---|---|
| INICIADO | Contrato firmado, onboarding comenzado |
| CUESTIONARIO CORE | Enviando/recibiendo el formulario de negocio |
| CONFIGURACIÓN META | Configurando accesos y cuenta publicitaria |
| CRM LISTO | CRM en Sheets creado y compartido con cliente |
| IDENTIDAD VISUAL | Recibiendo logos y paleta de colores |
| BRIEF LISTO | Brief de pauta y guiones aprobados |
| LISTO PARA LANZAR | Todo completo, campaña lista para salir |
| COMPLETADO | Primera campaña live |

---

### 2.3 SPACE: PRODUCCIÓN

**Quién lo usa**: Bauti R (responsable) + editores (Gian, Fran, Eze) + Nico + Fefi

**Lista: Contenido por cliente**

Acá vive cada video a producir. Reemplaza el Trello actual.

Para crear un nuevo video:
1. Ir a PRODUCCIÓN → Contenido por cliente
2. Click en "+ Nueva tarea" → elegir "[TEMPLATE] Producción de video"
3. Renombrar: `[CLIENTE] — [Tipo de video] — [Fecha]`
   - Ejemplo: `LopezProps — Reel marca personal — Abril W2`
4. Asignar a Bauti R
5. Poner deadline según calendario editorial
6. Status inicial: **PENDIENTE BRIEF**

| Status | Cuándo usarlo |
|---|---|
| PENDIENTE BRIEF | Hay que armar el brief de producción |
| BRIEF LISTO | Brief aprobado, listo para filmar/producir |
| PENDIENTE MATERIAL | Esperando que el cliente filme y suba el material |
| MATERIAL RECIBIDO | El material está en Drive, listo para editar |
| EN EDICIÓN | El editor está trabajando en la pieza |
| REVISIÓN INTERNA | Bauti R revisando antes de mandar al cliente |
| REVISIÓN CLIENTE | Esperando aprobación del cliente |
| APROBADO | El cliente aprobó |
| PUBLICADO | La pieza está publicada o lista para pauta |

**Lista: Diseño y estáticos**

Para piezas de diseño (carruseles, placas, stories). Responsable: Fefi.

Para crear una nueva pieza:
1. Ir a PRODUCCIÓN → Diseño y estáticos
2. Nueva tarea: `[CLIENTE] — [Tipo] — [Fecha]`
   - Ejemplo: `Abitat — Carrusel captación — Abril W3`
3. Asignar a Fefi

| Status | Cuándo usarlo |
|---|---|
| PENDIENTE BRIEF | Falta el brief de diseño |
| EN DISEÑO | Fefi está trabajando |
| REVISIÓN INTERNA | Revisión de Nico antes de mandar |
| REVISIÓN CLIENTE | Esperando aprobación del cliente |
| APROBADO | Aprobado y listo para usar |

**Lista: Edición de video**

Es la misma lista de Contenido por cliente pero vista filtrada por editor. Cada editor entra acá para ver solo sus tareas asignadas. No crear tareas acá directamente — crearlas siempre en Contenido por cliente.

---

### 2.4 SPACE: OPERACIONES → Carpeta PAUTA

**Quién lo usa**: Felipe (principal) + Elias

**Lista: Setup de campañas**

Para configurar una nueva campaña en Meta Ads.

Para crear una nueva campaña:
1. Ir a OPERACIONES → PAUTA → Setup de campañas
2. Click en "+ Nueva tarea" → elegir "[TEMPLATE] Setup de campaña Meta"
3. Renombrar: `[CLIENTE] — Campaña [tipo] — [Mes]`
   - Ejemplo: `Abitat — Campaña venta propiedad Palermo — Abril 2026`
4. Asignar a Felipe
5. Status inicial: **PENDIENTE MATERIAL**

| Status | Cuándo usarlo |
|---|---|
| PENDIENTE MATERIAL | Esperando el video/imagen aprobado |
| CONFIGURANDO | Felipe armando la campaña en Ads Manager |
| EN REVISIÓN DE META | Meta revisando el anuncio (24-48hs) |
| LIVE | Campaña activa |
| PAUSADA | Pausada temporalmente |
| FINALIZADA | Campaña terminada |

**Lista: Seguimiento semanal de campañas**

Una tarea por cliente por semana. Crear cada lunes con el checklist de revisión. Nombre: `[CLIENTE] — Revisión semanal — [fecha del lunes]`

---

### 2.5 SPACE: OPERACIONES → Carpeta DELIVERY

**Quién lo usa**: PM asignado al cliente (Elias o Bauti R) + Felipe

**Lista: Reuniones y reportes**

Para reportes semanales y reuniones con clientes.

Para crear un reporte semanal:
1. Ir a OPERACIONES → DELIVERY → Reuniones y reportes
2. Click en "+ Nueva tarea" → elegir "[TEMPLATE] Reporte semanal"
3. Renombrar: `[CLIENTE] — Reporte semana [fecha del lunes]`
4. Asignar al PM responsable del cliente (Elias o Bauti R)
5. Deadline: lunes antes de las 12h
6. Status inicial: **PENDIENTE**

**Lista: Incidencias y reclamos**

Cuando un cliente tiene un problema o queja. Nunca ignorar una incidencia abierta.

Para crear una incidencia:
1. Nueva tarea: `[CLIENTE] — [Descripción corta del problema]`
2. Status: **ABIERTA**
3. Asignar inmediatamente a quien va a resolverla

| Status | Cuándo usarlo |
|---|---|
| ABIERTA | Problema reportado, sin resolver |
| EN PROCESO | Alguien está trabajando en resolverlo |
| RESUELTA | Problema cerrado |

---

### 2.6 SPACE: OPERACIONES → Carpeta MANAGEMENT

**Quién lo usa**: Valentin + Elias + todo el equipo

**Lista: Tareas del equipo DV**

Mejoras internas, tareas administrativas, proyectos de la empresa que no son de cliente específico.

Para crear una tarea interna:
1. Nueva tarea con nombre descriptivo
2. Asignar a quien corresponde
3. Poner deadline
4. Status: **PENDIENTE**

**Lista: OKRs y métricas**

Los objetivos trimestrales y seguimiento de KPIs del negocio. Responsable: Valentin.

---

## PARTE 3 — LOS TEMPLATES {#parte-3}

Hay 4 templates creados en ClickUp. Son tareas con subtareas ya armadas. Para usarlos:

1. En la lista correspondiente, click en "+ Nueva tarea"
2. En el menú de creación, seleccionar el template
3. Renombrar la tarea según el formato indicado
4. Asignar responsable y deadline

### Template 1 — Onboarding nuevo cliente
**Dónde**: ONBOARDING → Onboarding por cliente
**Cuándo usarlo**: cada vez que firma un cliente nuevo
**Subtareas incluidas**: 28 subtareas en 4 bloques (Negocio, Técnica, Lanzamiento, Checklist final)

### Template 2 — Producción de video
**Dónde**: PRODUCCIÓN → Contenido por cliente
**Cuándo usarlo**: cada vez que hay un nuevo video a producir
**Subtareas incluidas**: 19 subtareas (Preproducción, Producción, Edición, Revisión, Publicación)

### Template 3 — Setup de campaña Meta
**Dónde**: OPERACIONES → PAUTA → Setup de campañas
**Cuándo usarlo**: cada vez que hay que configurar una nueva campaña
**Subtareas incluidas**: 15 subtareas (Preparación, Configuración, Seguimiento)

### Template 4 — Reporte semanal
**Dónde**: OPERACIONES → DELIVERY → Reuniones y reportes
**Cuándo usarlo**: cada lunes para cada cliente activo
**Subtareas incluidas**: 8 subtareas (Datos de pauta, Datos de contenido, Envío)

---

## PARTE 4 — STATUSES Y QUÉ SIGNIFICAN {#parte-4}

### Código de colores

| Color | Significado |
|---|---|
| Gris | Pendiente / Sin arrancar |
| Azul | En proceso |
| Amarillo | Requiere acción externa (cliente, Meta, tercero) |
| Verde | Completado |
| Rojo | Problema / urgente |

### Tabla completa de statuses por lista

**Pipeline de prospectos**
NUEVO → CONTACTADO → FIT CALL AGENDADA → FIT CALL REALIZADA → DISCOVERY AGENDADA → DISCOVERY REALIZADA → PROPUESTA ENVIADA → EN NEGOCIACIÓN → CERRADO — CLIENTE / CERRADO — NO AVANZÓ

**Onboarding por cliente**
INICIADO → CUESTIONARIO CORE → CONFIGURACIÓN META → CRM LISTO → IDENTIDAD VISUAL → BRIEF LISTO → LISTO PARA LANZAR → COMPLETADO

**Contenido por cliente / Edición de video**
PENDIENTE BRIEF → BRIEF LISTO → PENDIENTE MATERIAL → MATERIAL RECIBIDO → EN EDICIÓN → REVISIÓN INTERNA → REVISIÓN CLIENTE → APROBADO → PUBLICADO

**Diseño y estáticos**
PENDIENTE BRIEF → EN DISEÑO → REVISIÓN INTERNA → REVISIÓN CLIENTE → APROBADO

**Setup de campañas**
PENDIENTE MATERIAL → CONFIGURANDO → EN REVISIÓN DE META → LIVE → PAUSADA → FINALIZADA

**Seguimiento semanal / Reuniones y reportes / Tareas del equipo DV**
PENDIENTE → EN REVISIÓN / EN PROGRESO → COMPLETADO

**Incidencias y reclamos**
ABIERTA → EN PROCESO → RESUELTA

---

## PARTE 5 — RUTINA DIARIA Y SEMANAL {#parte-5}

### Check-in diario — antes de las 10am

Esto lo hace cada integrante del equipo todos los días hábiles. Toma 10 minutos.

1. Revisar tareas con deadline de hoy → confirmar que están en progreso
2. Actualizar el status de las tareas en las que avanzó ayer
3. Marcar como completadas las tareas que terminó
4. Crear las tareas nuevas que surgieron ayer y todavía no están en ClickUp

**Vista recomendada para el check-in**: ir a "My Tasks" en el menú lateral de ClickUp. Muestra todas las tareas asignadas a vos ordenadas por deadline.

### Reunión semanal de ClickUp — lunes

**Responsable de correrla**: Bauti R
**Dueño del sistema**: Valentin
**Duración**: 15-20 minutos

Agenda:
1. Tareas vencidas de la semana pasada que no se completaron → ¿qué pasó?
2. Tareas con deadline esta semana → ¿están en progreso? ¿hay bloqueos?
3. Clientes sin actividad en los últimos 5 días → señal de que algo se cayó
4. Valentin actualiza el pipeline comercial → prospectos que avanzaron o se perdieron
5. Actualizar OKRs si corresponde

Esta reunión no es para resolver problemas. Es para verlos. Si hay un problema, se resuelve fuera de la reunión.

### Cosas que hace Bauti R cada semana (ClickUp)

| Cuándo | Qué |
|---|---|
| Cada lunes antes de las 10am | Crear tarea de Reporte semanal para cada cliente activo (Template 4) |
| Cada lunes antes de las 10am | Crear tarea de Revisión semanal de campañas para cada cliente activo |
| Cada viernes | Confirmar que los reportes fueron enviados y el cliente los recibió |
| Cada 14 días | Crear tarea de Check-in quincenal con cada cliente |
| Cuando corresponda | Onboardear nuevos integrantes al uso de ClickUp |

---

## PARTE 6 — REGLAS DE USO {#parte-6}

### Cómo nombrar una tarea correctamente

Una tarea mal nombrada es peor que una tarea no creada.

**Toda tarea tiene obligatoriamente:**
- Nombre descriptivo (no "revisar cosa de Martínez")
- Responsable asignado (una persona, no un equipo)
- Deadline con fecha
- Status actualizado

**Formato del nombre:**
`[CLIENTE] — [Tipo de tarea] — [Período o versión]`

| Mal | Bien |
|---|---|
| "Editar video" | "Abitat — Editar Reel home staging — Abril W2" |
| "Llamar a cliente" | "Lopez Props — Check-in quincenal — 22 Abr" |
| "Hacer reporte" | "Zipcode — Reporte semanal — 21 Abr 2026" |

### Cómo usar los comentarios

- Los comentarios de una tarea son el historial de esa tarea
- Si algo importante se habló en WhatsApp sobre esa tarea, copiarlo como comentario
- Para notificar a alguien: usar @nombre en el comentario
- Al completar algo de la tarea, escribir un comentario corto: "Video subido a Drive, listo para revisión"
- No usar comentarios para conversaciones largas → esas van por WhatsApp, y el resumen del acuerdo va como comentario en ClickUp

### Escalamiento

- **Decisiones comerciales, financieras, de scope** → Valentin
- **Decisiones creativas** (guiones, tono, concepto visual) → Nico
- **Decisiones de pauta** (campañas, presupuesto Meta, segmentación) → Felipe
- **Operativas de cliente** (seguimiento, aprobaciones, comunicación) → Elias

### Nota sobre el plan

El workspace está en el plan gratuito de ClickUp (límite de 5 spaces). MANAGEMENT, PAUTA y DELIVERY viven como carpetas dentro del space OPERACIONES. Si el equipo crece y se necesita más estructura, considerar el plan Unlimited (spaces ilimitados).

---

*Última actualización: Abril 2026 — Digital View*
*Responsable del documento: Valentin Hechter*
