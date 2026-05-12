# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Digital View — Contexto para Agentes de IA

## Identidad

Digital View (DV) es una consultora de marketing y contenido especializada en el mercado inmobiliario argentino. Ayudamos a inmobiliarias y top producers a dejar de depender del boca en boca y a generar prospectos propios todos los dias, combinando contenido hecho a medida, campanas de Meta Ads y tecnologia que acelera la operacion comercial.

- **Fundadores**: Valentin Hechter (CEO) y Nicolas Caillet-Bois (COO)
- **Foco geografico**: CABA y Zona Norte del GBA
- **Clientes**: duenos de agencias inmobiliarias, top producers, desarrolladores inmobiliarios
- **Web**: digitalviewstrategies.com
- **Instagram**: @digitalviewagency

## Repositorio: arquitectura para Claude Code

Este repo (`Equipo-IA/`) NO es un producto de software clasico. Es un **sistema de agentes de IA internos de DV**, organizado por las 6 fases operativas. Cada agente vive bajo `agentes/<fase>_<nombre>/` y se opera abriendo Claude Code dentro de ese subdirectorio (cada uno tiene su propio `CLAUDE.md` + `.claude/skills/`).

### Layout mental

```
agentes/00_coordinador/        # Orquesta + crons (Windows Task Scheduler)
agentes/01_contenido/          # Creative Director, Copywritter, Design, Video AI, Post Production
agentes/02_comercial/          # Pipeline B2B/B2C, prescore leads, drafts WA
agentes/03_delivery_reporting/ # Reporte semanal end-to-end (HTML→PDF→Drive→WA)
agentes/04_pauta/              # Media Buyer Meta API (analyzer SCALE/KILL/ITERATE/HOLD)
agentes/05_account_manager/    # Chatbot WA 1-1 (scaffold)
shared/brands/<cliente>.json   # Brand system = single source of truth de tono, forbidden_words, ad_account_id, hook_frameworks
shared/state/<cliente>.json    # State machine por cliente (recalculado cada 6h)
shared/wa/client.py            # Cliente WhatsApp Business compartido
.claude/agents/                # Subagents (validators + dv-project-optimizer)
.claude/scripts/               # Hooks pre-commit, auto_approve sidecar, resolve_active_client
docs/                          # autonomy_map.md, auto_approval_policy.md, hooks_validators_scope.md
DV_Manual_Operativo.docx       # Manual operativo (fuente de verdad humana)
README.md                      # Setup, comandos completos, troubleshooting (LEE ESTO PARA DETALLE)
```

### Conceptos transversales (no obvios leyendo codigo)

- **Brand JSONs (`shared/brands/<cliente>.json`)**: TODOS los agentes leen este archivo dinamicamente. Es donde vive el tono real del cliente (no en el CLAUDE.md). Si vas a producir copy/hooks/guion para un cliente, leelo primero. Los validators (`tono-brand-validator`, `hook-scorer`, `guion-validator`) tambien lo leen para no estar hardcodeados a DV.
- **Active client (`.claude/state/active_client`)**: pointer a cliente activo (archivo de una linea con `brand_id`). Usado por los validators cuando no se les pasa explicito. Script `resolve_active_client.py` lo resuelve (fallback: inferir desde cwd si contiene `outputs/<brand_id>/`).
- **Sidecar `.status.json`**: cada output `.md` bajo `agentes/**/outputs/<cliente>/<fecha>/` tiene un sidecar generado por `.claude/scripts/auto_approve.py`. Marca `ready_for_handoff` (pasa entre agentes DV sin OK humano) o `needs_human` (bloquea). Politica completa en `docs/auto_approval_policy.md`.
- **Pre-commit hook (Windows-prod)**: en la maquina Windows esta instalado `.git/hooks/pre-commit` que llama a `.claude/scripts/pre_commit_validators.py` (valida tono + naming sobre staged files). En Mac-dev no esta instalado por default (`.git/hooks/` no se versiona). Esto es SEPARADO de la regla "invocar `dv-project-optimizer` antes de commit" — el subagent es el gate semantico de arquitectura, el hook es el gate sintactico de tono/naming.
- **Crons (Windows Task Scheduler)**: `recompute-state`, `pull-leads`, `prescore-leads`, `lead-followups`, `daily-monitor`, `weekly-report`, `auto-approve`, `health`. Entry point unico: `agentes/00_coordinador/scripts/cron_runner.py <task>`. Setup en `agentes/00_coordinador/scripts/CRON_SETUP.md`.
- **Outputs gitignorados**: todo bajo `agentes/**/outputs/`, `**/_tmp/`, `**/_scratch/`, `**/.env`, `**/credentials/`, `*.status.json`, `agentes/02_comercial/data/leads_clientes/*.json` (PII). No commitees nada ahi.

### Niveles de autonomia

Cada agente declara su nivel L0-L4 en `docs/autonomy_map.md`. Esto define que puede correr sin gate humano. Antes de elevar la autonomia de algo, leer ese doc.

### Donde corre cada cosa (importante para no diagnosticar mal)

El repo se sincroniza por git entre dos maquinas:

- **Windows (produccion)**: corre todos los crons via Task Scheduler. Ahi viven los archivos gitignored: `*.status.json` (sidecars), `shared/state/cron_log.jsonl`, `agentes/**/outputs/`, `**/_tmp/`, `**/credentials/`, `.env`.
- **Mac (dev remoto de Felipe)**: solo edicion + commits. **No** corre crons. La ausencia de sidecars / cron_log / outputs en Mac es esperable y NO indica bug. Para diagnosticar el estado de produccion, chequear desde la Windows.

## Comandos y donde trabajar

### Patron: abrir Claude en el directorio del agente

Cada agente tiene sus propias slash commands. Para usarlas, abri sesion Claude dentro del subdirectorio:

```bash
cd agentes/<fase>_<agente> && claude
```

Slash commands principales (lista completa en `README.md`):

| Agente | Skills |
|---|---|
| `00_coordinador` | `/kickoff <cliente>`, `/nueva-campana <cliente>`, `/status <cliente>`, `/buscar <keywords>` |
| `01_contenido/copywritter` | `/meta-ad`, `/caption`, `/banco-hooks`, `/estrategia-copy` |
| `01_contenido/creative_director` | (mismo patron, guiones + briefs carrusel) |
| `01_contenido/design` | (mismo patron, render Canva/HTML) |
| `02_comercial` | `/calificar`, `/preparar-reunion`, `/pipeline` |
| `03_delivery_reporting` | `/reporte-semanal`, `/reporte-mensual`, `/checklist-fase` |
| `04_pauta` | `/planificar`, `/analizar`, `/crear-campana`, `/optimizar` |

### Scripts Python CLI (sin sesion Claude)

```bash
# Onboarding cliente nuevo
python agentes/00_coordinador/scripts/kickoff_init.py <cliente_id> --name "<Display>" --notify

# Reporte semanal de un cliente (pipeline end-to-end: insights -> PDF -> Drive -> WA)
python agentes/03_delivery_reporting/scripts/weekly_report_deliver.py \
  --cliente <cliente> --destinatario-wa 549XXXXXXXXX --destinatario-nombre Elias

# Validators batch (sidecar .status.json sobre outputs)
python .claude/scripts/auto_approve.py [<cliente>] [<YYYY-MM-DD>] [--rerun]

# Correr una cron task manualmente (sin schtask)
python agentes/00_coordinador/scripts/cron_runner.py <task-name>

# Comercial: prescore + drafts WA
python agentes/02_comercial/scripts/lead_prescore.py
python agentes/02_comercial/scripts/followup_drafts.py

# Post-produccion video (master -> multi-format + thumb + subs)
python agentes/01_contenido/post_production/scripts/process_master.py \
  --input master.mp4 --cliente <cliente> --tipo RecorridoVO --version 1 --thumb-at 3 --transcribe
```

### Tests / lint

No hay suite de tests formal. Validacion ocurre via:
1. Pre-commit hook (`.claude/scripts/pre_commit_validators.py`) sobre staged `.md`/copy.
2. Subagent `dv-project-optimizer` antes del commit (regla mas abajo).
3. Sidecar `.status.json` por output via `auto_approve.py` (cron cada 6h).

Bypass del pre-commit hook solo si es deliberado: `git commit --no-verify`.

### Setup inicial

Detalle completo en `README.md` (Setup inicial). Resumen: instalar deps Python (`requests`, `google-auth*`, `playwright`), copiar `.env.example` -> `.env` en `04_pauta/` (Meta Ads), `03_delivery_reporting/` (WA Business), `01_contenido/post_production/` (Whisper), service account Google en `04_pauta/credentials/`, OAuth Drive en `03_delivery_reporting/credentials/`.

## Mision

Liberar a las inmobiliarias y a los agentes inmobiliarios de la dependencia del boca en boca, dandoles un sistema propio, predecible y escalable para generar prospectos, cerrar operaciones mas rapido y cobrar mejores comisiones.

## Diferencial

DV es la unica agencia que conoce el mercado inmobiliario argentino como deberia conocerse, combinando grupo humano + disciplina y constancia para generar resultados reales y sostenidos. Tres cosas concretas nos diferencian:

1. Entendemos el lenguaje del rubro (reserva, sena, comision compartida, captacion, top producer).
2. Tecnologia propia: chatbots, CRMs en Sheets, agentes de IA internos.
3. Garantia concreta: si en 45 dias no hay una operacion generada por nuestro trabajo, devolvemos el dinero.

## Equipo

| Nombre | Rol | Apodo |
|---|---|---|
| Valentin Hechter | CEO / Director Comercializacion / Delivery | Valen |
| Nicolas Caillet-Bois | COO / Director de Contenido | Nico |
| Felipe Probaos | Director de Campanas (Meta Ads) | Pipe / Felipe |
| Elias RM | PM - Relaciones con clientes | Elias |
| Bauti R | PM - Editor / Produccion audiovisual | Bauti |
| Bautista Caillet-Bois | Produccion audiovisual en campo | Bauti CB |
| Fefi | Diseno y contenido estatico | Fefi |
| Gian Luca | Edicion de video | Gian |
| Fran | Edicion de video | Fran |
| Eze | Edicion de video | Eze / Titi |

**IMPORTANTE**: "Bauti" = Bauti R (PM). "Bauti CB" o "Bautista" = Bautista Caillet-Bois (produccion en campo). No confundir.

## Escalamiento de decisiones

- **Comerciales, financieras, estrategicas** → Valentin
- **Creativas** (guiones, tono, concepto visual) → Nico
- **Pauta** (campanas, presupuesto Meta, segmentacion) → Felipe
- **Operativas de cliente** (seguimiento, aprobaciones, comunicacion) → Elias

## Servicios

Paquete integral que combina tres capas:

1. **Contenido estrategico**: videos verticales (Reels, TikTok, Meta Ads) + estaticos (carruseles, placas).
   - Track A: el cliente filma, DV edita.
   - Track B: DV produce en campo.
2. **Performance**: campanas de Meta Ads con segmentacion, test de creativos y optimizacion semanal.
3. **Operativa**: CRM en Sheets, chatbots, reportes semanales, training al equipo del cliente.

## Fases operativas

| Fase | Nombre | Responsable |
|---|---|---|
| 1 | Comercial | Valentin (+ Nico segun necesidad) |
| 2 | Onboarding | Elias / Bauti |
| 3 | Preproduccion y estaticos | Nico |
| 4 | Produccion y postproduccion | Nico / Elias + Editores |
| 5 | Pauta | Elias → Felipe |
| 6 | Lanzamiento y seguimiento | Elias / Bauti + Felipe |

**Regla de oro**: ninguna fase avanza si los controles de la fase anterior no estan completos.

## Tono de comunicacion

- **Directo**: sin rodeos, sin anglicismos innecesarios, sin corporate speak.
- **Humano**: frases cotidianas, chistes ocasionales, referencias del dia a dia del rubro.
- **Disruptivo sin ser careta**: rompemos con lo esperable pero no mentimos ni inflamos.
- **Sin cliches**: nada de "suenos", "concretar tu hogar", "profesionales que te acompanan".
- **High ticket framing**: hablamos como alguien que vale lo que cobra.
- **Sin emojis** en comunicacion profesional.
- **Voseo argentino**, tuteo siempre, sin "usted".

### Frameworks de contenido

**Hooks (Hormozi-style)** — primeros 3 segundos:
- Negacion: romper una creencia instalada.
- Empatia: nombrar el dolor del cliente mejor que el mismo.
- Verdad incomoda: decir en voz alta lo que nadie del rubro dice.

**Funnel narrativo** — toda pieza de contenido:
DOLOR → CONSECUENCIA → SOLUCION → PRUEBA

## Cliente ideal (ICP)

- Duenos de inmobiliarias pequenas/medianas (1-20 agentes)
- Top producers individuales que quieren escalar
- Desarrolladores inmobiliarios con proyectos en pozo o terminados
- Zona: CABA, GBA Zona Norte (corredor Vicente Lopez - San Fernando ideal)
- Ticket de propiedades: USD 80.000+
- Capacidad de inversion: fee DV + minimo USD 300/mes de pauta

## Stack tecnologico

| Herramienta | Uso |
|---|---|
| Google Drive | Almacenamiento de crudos, editados, fichas de cliente |
| Google Sheets | CRM de leads, brief de pauta, tracking de tareas |
| WhatsApp Business | Comunicacion con clientes |
| Trello | Flujo de edicion (cards con briefs y estados) |
| Meta Business Manager / Ads | Gestion y ejecucion de campanas |
| Adobe Premiere / CapCut | Edicion de video |
| Illustrator / Photoshop / Figma | Diseno de estaticos |
| Claude / ChatGPT | Ideacion de copys, hooks, estructuras |

## Estructura de carpetas por cliente en Drive

```
CLIENTE/
├── 00 Ficha del Cliente/
│   ├── Formulario CORE completado
│   ├── Identidad visual (logos, colores, referencias)
│   └── Accesos y contactos
├── 01 Estrategia/
│   ├── Estrategia de contenido
│   └── Bank de hooks y guiones aprobados
├── 02 Producciones/
│   └── Produccion YYYY-MM-DD/
│       ├── NUEVOS (crudos)
│       └── EDITADOS (finales)
├── 03 Estaticos/
│   ├── Carruseles
│   └── Placas
├── 04 Campanas Meta/
│   └── Brief de pauta
└── 05 Reportes/
    └── Reporte semana YYYY-MM-DD
```

**Nomenclatura**: `CLIENTE_TipoContenido_Version.extension`
Ejemplo: `LopezProps_RecorridoVO_V1.mp4`

## Prioridades de automatizacion con IA

1. **Contenido** (foco inicial): ideacion de guiones, ideacion de estaticos, asistente de edicion, generacion de disenos.
2. **Comercial**: calificacion de prospectos, preparacion de reuniones, seguimiento de pipeline.
3. **Delivery y Reporting**: reportes semanales automaticos, seguimiento de leads, feedback/NPS.
4. **Pauta**: monitoreo de campanas, testeo de creativos.

## Glosario rapido

| Termino | Significado |
|---|---|
| Top producer | Agente inmobiliario de alto rendimiento individual |
| Captacion | Conseguir propiedades nuevas para vender |
| Reserva / Sena | Pago inicial del comprador para bloquear propiedad |
| Comision compartida | Dos inmobiliarias cierran operacion y reparten comision |
| Metodo DV | Dolor → Consecuencia → Solucion → Prueba + hooks Hormozi |
| Track A | Cliente filma, DV edita |
| Track B | DV produce en campo |
| Ficha del Cliente | Documento central en Drive con todo el contexto del cliente |
| Brief de pauta | Documento con campos para que Felipe ejecute campana sin preguntar |
| CORE | Formulario de 15 preguntas del onboarding |

## Reglas para agentes de IA

1. Respeta los procesos. Los controles de fase son el filtro que evita reproceso. No saltes fases.
2. Nombra las cosas como el equipo las nombra. Usa los apodos internos.
3. Escala cuando la decision no sea operativa (ver seccion de escalamiento).
4. No agregues cosas que no estan pedidas. Cuando Valentin da instrucciones exactas, seguilas al pie de la letra.
5. Respeta el tono: sin emojis, cercano, original, directo, sin cliches, voseo argentino.
6. Si no sabes a que cliente se refiere algo, pedi el nombre antes de actuar.
7. Si una decision parece comercial (afecta fee, scope o contrato), escalaselo a Valentin.

## Antes de cualquier `git commit`

REGLA DURA: antes de ejecutar `git commit`, invoca el agente `dv-project-optimizer`
(definido en `.claude/agents/_shared/dv-project-optimizer.md`) usando el tool `Agent` con
`subagent_type: "dv-project-optimizer"`. El agente revisa:

- Estructura de carpetas y nombres de archivos (que esten bajo el agente que los usa, no en raiz).
- Naming conventions (snake_case, `<CLIENTE>_<Tipo>_V<n>.<ext>`, etc.).
- CLAUDE.md por agente actualizado si corresponde.
- Que los agentes consuman info de donde debe (no duplicacion).
- Que outputs/working files vivan donde corresponde (no en raiz).
- Eficiencia: que no haya scripts duplicados o configuracion redundante.

Si el agente reporta findings criticos (BLOCK), los resolves ANTES de commitear.
Si reporta findings menores (FLAG), los anotas y commiteas con nota en el mensaje.
Si reporta PASS, commiteas normal.

Esta regla aplica para TODOS los commits, incluso los aparentemente triviales.

## Documento fuente de verdad

El manual operativo completo esta en `DV_Manual_Operativo.docx` en la raiz del proyecto. Este CLAUDE.md es un resumen operativo. Ante dudas, consultar el manual.
