# Equipo IA — Digital View

Sistema de agentes de IA internos de Digital View. Cubre las 6 fases operativas (Comercial → Lanzamiento) con un mix de skills de Claude Code + scripts Python + crons automáticos.

> Contexto completo de la agencia, tono y fases: `CLAUDE.md` (fuente de verdad para todos los agentes). Manual operativo: `DV_Manual_Operativo.docx`.

---

## Setup inicial (una sola vez)

```bash
# 1. Deps Python (los scripts asumen Python 3.11+)
pip install requests google-auth google-auth-oauthlib google-api-python-client python-dotenv playwright
playwright install chromium

# 2. Credenciales Meta Ads
cp agentes/04_pauta/.env.example agentes/04_pauta/.env
# Vars requeridas (ver .env.example): META_ACCESS_TOKEN, META_APP_ID,
# META_APP_SECRET, META_BUSINESS_ID. Token del System User DV con scopes
# ads_management, ads_read, business_management.

# 3. Service account Google (Sheets / Drive read)
# Copiar a: agentes/04_pauta/credentials/google_service_account.json

# 4. Credenciales WhatsApp Business
cp agentes/03_delivery_reporting/.env.example agentes/03_delivery_reporting/.env
# Vars en .env.example: REPORTES_WABA_TOKEN, REPORTES_PHONE_NUMBER_ID,
# ELIAS_WA_NUMBER. Adicional para alertas de validators y briefs:
# FELIPE_WA_NUMBER, NICO_WA_NUMBER (agregar a mano al .env real).

# 5. OAuth Drive (para upload de PDFs de reportes - usa cuenta DV, no SA)
# Crear OAuth Client tipo "Aplicacion de escritorio" en GCP Console del
# proyecto DV. Descargar JSON y guardar como:
#   agentes/03_delivery_reporting/credentials/oauth_client.json
python agentes/03_delivery_reporting/scripts/drive_upload.py --auth
# Abre browser, pedis consentimiento, guarda drive_token.json (con refresh).

# 6. (Opcional) OpenAI Whisper API para subtitulos automaticos
cp agentes/01_contenido/post_production/.env.example agentes/01_contenido/post_production/.env
# Var: OPENAI_API_KEY

# 7. Pre-commit hook (gate de validators)
# Ya viene instalado en .git/hooks/pre-commit. Llama a
# .claude/scripts/pre_commit_validators.py para validar tono + naming.
# Bypass solo si es deliberado: git commit --no-verify

# 8. Crons Windows Task Scheduler (requiere PS admin)
# Ver: agentes/00_coordinador/scripts/CRON_SETUP.md
```

### Qué se gitignorea (sensible / runtime)

- `**/.env`, `**/credentials/`, `**/_tmp/`, `**/_scratch/`
- `shared/state/*.jsonl` (cron logs)
- `agentes/*/outputs/`, `agentes/03_delivery_reporting/outputs/*.log`
- `*.status.json` (sidecars de validators)
- `agentes/02_comercial/data/pipeline.backup.*.json`

---

## Estructura del repo

```
Equipo-IA/
├── CLAUDE.md                            # Contexto DV (todos los agentes lo leen)
├── README.md                            # Este archivo
├── DV_Manual_Operativo.docx             # Manual operativo completo
├── docs/
│   ├── autonomy_map.md                  # Mapa de autonomía por fase + roadmap
│   ├── auto_approval_policy.md          # Política sidecar handoff interno
│   ├── hooks_validators_scope.md        # Scope de validators y hooks
│   └── onboarding/                      # Onboarding de clientes nuevos
├── agentes/
│   ├── 00_coordinador/                  # Orquestador entre agentes + crons
│   │   ├── scripts/
│   │   │   ├── cron_runner.py           # Tasks recurrentes (entry point)
│   │   │   ├── kickoff_init.py          # Scaffold cliente nuevo
│   │   │   ├── health_check.py          # SLA cron
│   │   │   └── CRON_SETUP.md            # Cómo registrar schtasks Windows
│   │   └── .claude/skills/
│   │       ├── kickoff/                 # /kickoff <cliente>
│   │       ├── nueva-campana/           # /nueva-campana <cliente>
│   │       ├── status/                  # /status <cliente>
│   │       └── buscar/                  # /buscar <keywords>
│   ├── 01_contenido/
│   │   ├── creative_director/           # Ideación guiones + briefs carrusel
│   │   ├── copywritter/                 # Copy Meta Ads + captions + hooks
│   │   ├── design/                      # Render Canva/HTML carruseles
│   │   ├── video_ai/                    # Storyboards + prompts Veo3
│   │   └── post_production/             # ffmpeg + Whisper API (multi-format)
│   ├── 02_comercial/
│   │   ├── scripts/
│   │   │   ├── lead_prescore.py         # Priority + knockouts + red flags auto
│   │   │   ├── followup_drafts.py       # Drafts WA primer contacto
│   │   │   ├── meta_leads_puller.py     # Ingesta Meta Lead Ads
│   │   │   └── pipeline.py              # CRUD del pipeline.json
│   │   └── data/
│   │       ├── pipeline.json            # Pipeline comercial DV
│   │       └── leads_clientes/          # Leads por cliente
│   ├── 03_delivery_reporting/
│   │   ├── scripts/
│   │   │   ├── weekly_report_deliver.py # Pipeline reporte semanal
│   │   │   ├── render_pdf.py            # HTML+CSS DV-strict → PDF (Playwright)
│   │   │   ├── drive_upload.py          # OAuth user → Drive
│   │   │   ├── wa_reportes.py           # Wrapper WA template + texto
│   │   │   └── auto_deliver.py          # Hook PostToolUse + flow cron
│   │   └── templates/reporte_semanal/   # HTML + CSS del reporte
│   ├── 04_pauta/                        # Media Buyer Meta API
│   │   ├── scripts/
│   │   │   ├── meta_api.py
│   │   │   ├── campaign_analyzer.py     # SCALE/KILL/ITERATE/HOLD
│   │   │   └── report_generator.py
│   │   └── credentials/google_service_account.json
│   └── 05_account_manager/              # Chatbot WhatsApp 1-1 (scaffold)
├── shared/
│   ├── brands/<cliente>.json            # Brand systems (single source of truth)
│   ├── state/<cliente>.json             # State machine por cliente
│   ├── wa/                              # Cliente WhatsApp compartido
│   ├── scripts/asset_index.py           # FTS5 cross-agent
│   └── contexto_inmobiliario.md
└── .claude/
    ├── agents/                          # Subagents (validators + optimizer)
    ├── skills/                          # Skills cross-agent
    ├── scripts/
    │   ├── auto_approve.py              # Sidecar validator batch
    │   └── pre_commit_validators.py     # Hook git pre-commit
    └── agent-memory/                    # Memoria persistente por subagent
```

---

## Flujos automáticos (qué corre solo)

Registrados como Windows Task Scheduler (`/RU SYSTEM`). Detalle de comandos en `agentes/00_coordinador/scripts/CRON_SETUP.md`.

| Tarea | Frecuencia | Qué hace |
|---|---|---|
| `recompute-state` | cada 6h | Reindex assets + recalcula state por cliente |
| `pull-leads` | cada 4h | Trae leads de Meta Lead Ads → `pipeline.json` |
| `prescore-leads` | cada 4h | Priority + knockouts + red flags sobre leads en pre_filtro |
| `lead-followups` | cada 4h | Drafts WA primer contacto para priority 1/2 sin knockouts |
| `daily-monitor` | diario 08:30 | Insights día anterior. Si KILL/fatiga: alerta + brief auto a Creative Director |
| `process-creative-briefs` | diario 09:00 | Notifica a Nico por WA los briefs auto pendientes |
| `weekly-report` | lunes 09:00 | Pipeline end-to-end: insights → PDF Canva-strict → Drive → WA template Elias |
| `auto-approve` | cada 6h | Valida tono+naming en outputs/, escribe sidecar `.status.json` |
| `health` | cada 6h | Chequea SLA. Alerta a Felipe si algo no corrió |

**Log**: `shared/state/cron_log.jsonl` (gitignored).

---

## Comandos clave (skills + scripts CLI)

### Slash commands de Claude (abrir Claude en el directorio del agente correspondiente)

```bash
# Coordinador
cd agentes/00_coordinador && claude
/kickoff <cliente_id> --init     # Onboarding scaffold + Drive + WA
/nueva-campana <cliente>         # Flujo completo producción → pauta
/status <cliente>                # Estado del cliente
/buscar <keywords>               # Busca assets cross-agente (FTS5)

# Copywritter
cd agentes/01_contenido/copywritter && claude
/meta-ad <cliente>               # Copy Meta Ads (2 variantes por objetivo)
/caption <cliente>               # Caption orgánico
/banco-hooks <cliente>           # Banco de hooks Hormozi-style
/estrategia-copy <cliente>       # Estrategia narrativa

# Creative Director (mismo patrón)
# Design (mismo patrón)

# Comercial
cd agentes/02_comercial && claude
/calificar <nombre>              # Scorecard 41 puntos
/preparar-reunion <nombre>       # Brief discovery/fit call
/pipeline                        # Estado actual del pipeline

# Delivery / Reporting
cd agentes/03_delivery_reporting && claude
/reporte-semanal <cliente>       # Reporte legacy markdown
/reporte-mensual <cliente>       # Cierre de mes
/checklist-fase <cliente> <fase> # Validador checklist fase

# Pauta
cd agentes/04_pauta && claude
/planificar <cliente>            # Plan de campaña nuevo
/analizar <cliente>              # SCALE/KILL/ITERATE/HOLD
/crear-campana                   # Push aprobado a Meta API
/optimizar <cliente>             # Revisión performance + feedback loop
```

### Scripts Python CLI

```bash
# Onboarding cliente nuevo (sin sesión Claude)
python agentes/00_coordinador/scripts/kickoff_init.py <cliente_id> --name "<Display>" --notify

# Reporte semanal manual (un cliente)
python agentes/03_delivery_reporting/scripts/weekly_report_deliver.py \
  --cliente digital_view --destinatario-wa 549XXXXXXXXX --destinatario-nombre Elias

# Render PDF aislado (sin upload Drive)
python agentes/03_delivery_reporting/scripts/render_pdf.py \
  --data-json data.json --out reporte.pdf

# Upload manual Drive
python agentes/03_delivery_reporting/scripts/drive_upload.py \
  --file reporte.pdf --cliente digital_view --name "Reporte Y.pdf"

# Post-producción video (master → multi-format + thumb + subs)
python agentes/01_contenido/post_production/scripts/process_master.py \
  --input master.mp4 --cliente lopez_propiedades --tipo RecorridoVO --version 1 \
  --thumb-at 3 --transcribe

# Comercial: prescore leads
python agentes/02_comercial/scripts/lead_prescore.py
python agentes/02_comercial/scripts/followup_drafts.py

# Validators batch (manual)
python .claude/scripts/auto_approve.py [<cliente>] [<YYYY-MM-DD>] [--rerun]

# Cron runner (testear una tarea sin schtask)
python agentes/00_coordinador/scripts/cron_runner.py weekly-report
python agentes/00_coordinador/scripts/cron_runner.py daily-monitor
```

---

## Cómo agregar un cliente nuevo (kickoff)

Desde sesión Claude en el coordinador:

```bash
cd agentes/00_coordinador && claude
/kickoff <cliente_id> --init
```

El skill orquesta:
1. **Scaffold local** (`kickoff_init.py`): clona `toribio_achaval.json` como template → `shared/brands/<cliente>.json` con TODOs.
2. **Estructura Drive 00-05** vía MCP.
3. **`leads_clientes/<cliente>.json`** + `state/<cliente>.json`.
4. **WA notify** a Elias + Nico con resumen.

Después tenés que completar manualmente en el brand JSON:
- `brand_tagline`, `positioning` (los TODOs).
- `meta_ads.ad_account_id` (con prefijo `act_`).
- `meta_ads.page_id`.
- `tone_of_voice` (ajustar al cliente real: principles, forbidden_words, preferred_words, hook_frameworks).
- `references` (visuales del cliente).

Cuando estén todos los campos, podés correr el flujo `/nueva-campana <cliente>`.

---

## Cómo trabajar día a día

### Elias (relaciones con clientes)
- WA: recibe alertas del cron (reportes semanales listos, briefs pendientes, alertas KILL).
- Sesión Claude en `03_delivery_reporting/`: corre `/reporte-semanal` legacy si necesita texto, `/checklist-fase` para gates.
- Pipeline comercial: `/pipeline` desde `02_comercial/`.

### Felipe (pauta)
- Sesión Claude en `04_pauta/`: `/planificar`, `/crear-campana`, `/optimizar`.
- WA: recibe alertas de validators bloqueados (briefs con tono FAIL, reportes con violaciones).

### Nico (contenido)
- Sesión Claude en `01_contenido/creative_director/` o `copywritter/`.
- WA: recibe briefs creativos auto generados por `daily-monitor` cuando un ad muere.
- Lee `shared/brands/<cliente>.json` para tono específico.

### Valentin (comercial)
- Sesión Claude en `02_comercial/`: `/calificar`, `/preparar-reunion`.
- Lee `outputs/digital_view/<fecha>/followup_*.md` para drafts WA listos.

---

## Validators y gates (calidad output)

1. **Sidecar `.status.json`** — Cada output `.md` bajo `agentes/**/outputs/<cliente>/<fecha>/` tiene un sidecar con resultado de validators:
   - `ready_for_handoff` → pasa entre agentes DV sin OK humano.
   - `needs_human` → bloquea hasta que alguien corrige.
2. **Tono** — Forbidden words por brand. `tono-brand-validator` (LLM) para capa semántica.
3. **Naming** — Regex `<CLIENTE>_<Tipo>_V<n>[_<variant>].<ext>`. Hook pre-commit bloquea commit si naming roto.
4. **Hook scoring** — `hook-scorer` evalúa hooks 1-5 contra frameworks del brand.
5. **Brief de pauta** — `brief-pauta-validator` chequea 9 ítems críticos antes de mandar a Felipe.

**Política completa**: `docs/auto_approval_policy.md`.

---

## Pre-commit gate

Antes de cualquier `git commit`, invocá el subagent **`dv-project-optimizer`** (regla en `CLAUDE.md`). Audita estructura, naming, _tmp en raíz, duplicación. Devuelve PASS / FLAG / BLOCK.

```bash
# En sesión Claude:
# Subagent tool con subagent_type=dv-project-optimizer
# Pasale el git status + intención del commit.
```

---

## Estado de los agentes

| Fase | Directorio | Estado | Autonomía |
|---|---|---|---|
| 00 Coordinador | `agentes/00_coordinador/` | Maduro | L3 (orquesta + crons) |
| 01 Creative Director | `agentes/01_contenido/creative_director/` | Maduro | L2 |
| 01 Copywritter | `agentes/01_contenido/copywritter/` | Maduro | L2 |
| 01 Design | `agentes/01_contenido/design/` | Maduro | L2 |
| 01 Video AI | `agentes/01_contenido/video_ai/` | Beta | L1 |
| 01 Post Production | `agentes/01_contenido/post_production/` | Beta | L1 (CLI manual) |
| 02 Comercial | `agentes/02_comercial/` | Maduro | L2.5 (prescore + drafts auto) |
| 03 Delivery & Reporting | `agentes/03_delivery_reporting/` | Maduro | L3 (reporte semanal full auto) |
| 04 Pauta (Media Buyer) | `agentes/04_pauta/` | Maduro | L2 (gate humano push Meta) |
| 05 Account Manager | `agentes/05_account_manager/` | Scaffold | L0 |

Niveles de autonomía L0–L4 definidos en `docs/autonomy_map.md`.

---

## Clientes operativos

16 brand JSONs en `shared/brands/` — **12 con `ad_account_id` configurado** (reciben crons automáticos):

| Cliente | Tipo | Ticket | Tono |
|---|---|---|---|
| digital_view | DV mismo (agencia) | n/a | Disruptivo Hormozi |
| ini_propiedades | Inmobiliaria | medio | Cercano profesional |
| toribio_achaval | Inmobiliaria premium | alto | Premium institucional |
| abitat | Inmobiliaria home staging | medio | Aspiracional tangible |
| abitat_puertos | (alias_of abitat) | medio | Aspiracional tangible |
| vistalaguna | Boutique ultra premium | USD 1M+ | Lujo silencioso |
| turco | Top producer individual | medio | Cordial pro |
| lucila_taratuty | Top producer individual | medio | Cordial pro |
| viviana_sasia | Inmobiliaria | medio | (heredado) |
| juan_caillet_bois | Top producer | medio | (heredado) |
| rubica_inmobiliaria | Inmobiliaria | medio | (heredado) |
| brain_soluciones | **Consultoría B2B PyMEs** (fuera de rubro) | n/a | Operativo PyME |

**4 brand JSONs sin `ad_account_id`** (en onboarding o pausados): `fidez_group`, `jose_maria_chaher`, `matias_di_meola`, `zipcode`. No los procesa el cron hasta que se complete el bloque `meta_ads` en su JSON.

---

## Troubleshooting

- **Cron no corre**: verificá `schtasks /Query /FO LIST | findstr DV-`. Tareas viejas pueden estar en "Solo interactivo"; recrearlas con `/RU SYSTEM` (ver `CRON_SETUP.md`).
- **Token Meta expirado**: regenerar token System User en Business Manager DV, actualizar `agentes/04_pauta/.env`. El error típico es `(#190) Token expirado`.
- **WA template no llega**: verificar status del template en WhatsApp Manager (debe estar APPROVED, no PENDING). Idioma exacto: `es_AR`.
- **OAuth Drive vencido**: el refresh token se renueva solo. Si falla, re-correr `drive_upload.py --auth`.
- **Validators bloquean output**: leer el sidecar `<file>.md.status.json` para ver qué violación. Forbidden words se ajustan en el brand JSON del cliente.

---

## Roadmap

Próximos sprints planificados (ver `docs/autonomy_map.md` y tasks abiertos):

- **Sprint 6** (en curso): loop creativo cerrado, hook scoring auto en copywritter, skill `/proceso-video`.
- **Sprint 7**: reporte mensual análogo al semanal, account manager WhatsApp 1-1.
- **Sprint 8**: dashboard `/status` ampliado, métricas reales del autonomy_map.
- **Sprint 9**: recovery tokens Meta auto, backup pipeline, tests.
- **Sprint 10**: MCP server DV propio (expone state vía MCP).

---

## Convenciones

- **Carpetas tmp / working files**: `agentes/<fase>/<agente>/_tmp/`. Nunca en raíz del repo.
- **Outputs generados**: `agentes/<fase>/<agente>/outputs/<cliente>/<fecha>/`. Gitignored.
- **Credenciales / tokens**: `agentes/<fase>/<agente>/credentials/`. Gitignored.
- **Naming binarios**: `<CLIENTE>_<TipoContenido>_V<n>[_<variant>].<ext>`.
- **Naming brand_id**: snake_case.
- **Voseo argentino** en todo output cliente-facing.
- **Sin emojis** en comunicación profesional (excepción: account manager WA en algunos contextos).
