---
name: Modelos recomendados por agente DV
description: Recomendaciones actuales de modelo en CLAUDE.md de cada agente, gaps detectados
type: reference
---

Estado actual de recomendaciones de modelo en los 8 CLAUDE.md:

| Agente | Recomendacion actual | Comentario |
|---|---|---|
| Coordinador (00) | (no especifica) | Tareas operativas/orquestacion. Candidato a Haiku 4.5 para `/status` (lectura rapida) |
| Copywriter (01) | sonnet-4-6 estandar / opus-4-7 estrategia | Bien |
| Creative Director (01) | Sonnet 4.6 default / Opus 4.6 estrategia mensual | Bien |
| Design (01) | Sonnet 4.6 / Opus 4.6 onboardings | Bien |
| Comercial (02) | (no especifica) | `/calificar` es scoring estructurado: Haiku 4.5 podria bastar. `/preparar-reunion` requiere Sonnet |
| Delivery Reporting (03) | Sonnet 4.6 / Opus 4.6 mensual complejo | Bien. `/checklist-fase` es boolean, candidato a Haiku |
| Media Buyer (04) | (no especifica) | `/analizar` con tablas y benchmarks: Sonnet correcto. Reportes formateados podrian Haiku |

**Gaps:**
- 3 de 8 agentes (00, 02, 04) no declaran modelo recomendado en CLAUDE.md
- Ninguno aprovecha Haiku 4.5 para tareas estructuradas/repetitivas (status, checklist, scoring de prospecto)
- La nomenclatura mezcla "Sonnet 4.6" / "claude-sonnet-4-6" — falta uniformidad

**How to apply:** para cada agente, agregar seccion "Modelo" con tabla por skill. Tareas estructuradas (formato fijo, lectura → tabla) van Haiku; ideacion/criterio van Sonnet; estrategia profunda va Opus.
