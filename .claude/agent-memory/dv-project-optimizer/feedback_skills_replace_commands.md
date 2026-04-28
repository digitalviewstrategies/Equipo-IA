---
name: Skills reemplazan a commands, no convivir
description: Copywriter tiene los 4 skills duplicados como slash commands en .claude/commands/ con contenido casi identico
type: feedback
---

En `agentes/01_contenido/copywritter/.claude/` conviven:
- `commands/{caption,banco-hooks,estrategia-copy,meta-ad}.md` (slash commands legacy)
- `skills/{caption,banco-hooks,estrategia-copy,meta-ad}/SKILL.md` (skills modernos)

Los pares son ~95% identicos. Diff confirma que solo cambian el frontmatter (description vs name+description+triggers) y el formato del campo "Inputs" (argumentos posicionales vs preguntas).

**Why:** el sistema de skills modernos con triggers en description hace innecesarios los commands. Mantener ambos duplica tokens en el descubrimiento del modelo y crea confusion sobre cual es la fuente de verdad. La mtime confirma que el commands/meta-ad.md fue actualizado hoy 2026-04-27 (15:20 vs 23:16) — ese cambio nunca llego al skill, drift activo.

**How to apply:** eliminar `commands/` completo en copywriter (4 archivos, ~7KB). El skill ya esta correctamente configurado con triggers en su description.
