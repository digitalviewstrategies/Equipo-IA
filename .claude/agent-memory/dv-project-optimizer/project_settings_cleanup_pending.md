---
name: settings.local.json con permisos legacy
description: 100 lineas con 76 permisos Bash, 44 son rutas historicas /home/valentin/ del 2026-04-13
type: project
---

`/Users/FelipeProbaos/Documents/Claude Digital View/.claude/settings.local.json` tiene:
- 100 lineas
- 76 permisos en `permissions.allow` (mayormente Bash specific)
- 44 entradas con paths viejos `/home/valentin/Documents/Equipo IA DV/` (de cuando el proyecto vivia en otra maquina/usuario)
- 12 entradas son `curl -sL https://images.unsplash.com/...` con URLs hardcoded de fotos especificas
- Multiples entradas de `python3 scripts/render.py --html "output/toribio_achaval/2026-04-13/..."` que solo aplicaron a un onboarding puntual

**Why:** las entradas con paths absolutos `/home/valentin/...` ya no existen en este sistema. Cada permiso ocupa lineas pero nunca matchea, lo que genera prompts de permisos cuando el modelo intenta operaciones similares con paths nuevos.

**How to apply:** proponer reemplazar todo el `permissions.allow` por una lista corta de patrones genericos: `Bash(python3 scripts/render.py:*)`, `Bash(curl -sL:*)`, `WebSearch`, `WebFetch(domain:unsplash.com)`, etc. Reduce de 100 lineas a ~25. Aplicar via skill `update-config` o `fewer-permission-prompts`.
