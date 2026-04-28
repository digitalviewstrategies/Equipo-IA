---
name: Estructura monorepo DV
description: Layout actual de agentes y carpetas del proyecto Digital View al 2026-04-27
type: project
---

Layout principal del proyecto Digital View (raiz `/Users/FelipeProbaos/Documents/Claude Digital View/`):

- `CLAUDE.md` (175 lineas) — instrucciones globales del proyecto
- `DV_Manual_Operativo.docx` — fuente de verdad operativa (no tocar)
- `Docs DV/` — docs corporativos (.docx + BIBLIA_DV_MAESTRA.md de 1138 lineas, 56KB)
- `docs/onboarding/` — solo tiene un .docx de 13MB y screenshots extraidos
- `shared/`
  - `contexto_inmobiliario.md` (11KB) — fuente unica del rubro inmobiliario, ya activado
  - `brands/` — 13 JSONs de brand (clientes), `_template.json`, `_onboarding.md` (16KB)
- `agentes/`
  - `00_coordinador/` — orquesta flujos (status, kickoff, nueva-campana). NUEVO, no estaba en sesion previa
  - `01_contenido/copywritter/` (con doble t) — 4 skills + 4 commands (duplicados), CLAUDE.md 128 lineas
  - `01_contenido/creative_director/` — 9 archivos en context/ (incluyendo sistema_video_ads_parteN.md)
  - `01_contenido/design/` — CLAUDE.md 227 lineas (el mas grande), README 223 lineas, MCPs Canva+Drive
  - `02_comercial/` — Valentin como user primary, 3 skills (calificar/preparar-reunion/pipeline)
  - `03_delivery_reporting/` — Elias como user primary, 3 skills (reporte semanal/mensual, checklist-fase)
  - `04_pauta/` — Felipe, MCP server custom meta_ads_mcp.py + 4 skills + scripts/

Fases operativas: 1 Comercial, 2 Onboarding, 3 Preproduccion/estaticos, 4 Produccion/postproduccion, 5 Pauta, 6 Lanzamiento.
