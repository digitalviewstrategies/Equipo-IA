---
name: Unificar contexto inmobiliario en shared/
description: Existen 4 archivos con info del rubro inmobiliario que se solapan
type: feedback
---

Cuatro archivos con info del rubro inmobiliario argentino:

1. `shared/contexto_inmobiliario.md` (11KB) — fuente activa, completa. Su header dice explicitamente "Reemplaza creative_director/context/inmobiliario_mercado.md, copywritter/context/mercado_inmobiliario_arg.md y design/context/inmobiliario_glosario.md"
2. `agentes/01_contenido/creative_director/context/inmobiliario_mercado.md` (8.5KB) — viejo, ya reemplazado, deberia eliminarse
3. `agentes/01_contenido/copywritter/context/mercado_inmobiliario_arg.md` (5.7KB) — viejo, ya reemplazado, deberia eliminarse
4. `agentes/01_contenido/design/context/inmobiliario_glosario.md` (5.7KB) — viejo, ya reemplazado, deberia eliminarse

Adicionalmente, `agentes/01_contenido/copywritter/context/audiencias.md` se solapa parcialmente con `agentes/04_pauta/context/audiencias_inmobiliario.md` (perfiles de audiencias).

**Why:** los 3 archivos viejos siguen ahi consumiendo tokens cuando algun agente carga "todo el context/". Ya estan marcados como obsoletos en el header del archivo nuevo. El usuario confirmo que la migracion ya se hizo, falta limpiar.

**How to apply:** proponer borrar los 3 archivos legacy. Para audiencias.md vs audiencias_inmobiliario.md, definir uno como master (la version pauta tiene info geo/lat-lng concreta, la copywriter tiene perfiles de dolor/objeciones — son complementarias, no duplicadas; mantener ambas pero referenciar shared/contexto_inmobiliario.md desde ambas).
