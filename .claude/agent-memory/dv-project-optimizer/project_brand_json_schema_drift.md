---
name: Brand JSON schema drift entre brands DV
description: Sprint 5 personalizo 5 brands; abitat_puertos tiene disruption_scale extra; brain_soluciones esta fuera de rubro sin marker; abitat_puertos duplica abitat sin alias_of
type: project
---

Sprint 5 (2026-05-11) personalizo 5 brand JSONs (vistalaguna, turco, brain_soluciones, abitat_puertos, lucila_taratuty). NOTA 2026-05-14: turco fue mergeado en team_noia.json junto con jose_maria_chaher (unifica todo a un solo brand). Drift detectado:

- `abitat_puertos.tone_of_voice` incluye `disruption_scale` que los otros 4 no tienen (heredado de abitat.json).
- `brain_soluciones` es consultoria B2B PyMEs, NO inmobiliario. Hoy el marker esta solo en `_brand_notes.rubro` como string libre; ningun validator/skill lo lee. Falta campo top-level `industry` y lista `excluded_workflows`.
- `abitat_puertos.json` es copia completa (309 lineas) de `abitat.json` (303 lineas). Riesgo de drift al actualizar uno y no el otro. Falta campo `alias_of: abitat` y loader que haga merge.
- Convencion `_brand_notes` (prefijo `_` = privado) no esta documentada en `shared/brands/CLAUDE.md` o schema. Riesgo: agentes que iteran keys pueden filtrarlo a outputs cliente-facing.

**Why:** Sin schema formal de brand JSON, cada personalizacion mete drift. Validators y skills asumen estructura uniforme.

**How to apply:** Cuando se audite shared/brands/ o se agreguen brands nuevos, chequear: (a) keys de tone_of_voice consistentes, (b) campo `industry` presente y validators que lo respeten, (c) brands clonados usan `alias_of` + overrides en vez de copia full, (d) keys con `_` documentadas como privadas.
