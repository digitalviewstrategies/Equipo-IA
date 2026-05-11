---
name: Pre-commit gate role
description: dv-project-optimizer se invoca SIEMPRE antes de cualquier git commit. Auditar staged + working tree con foco en estructura, naming y duplicacion.
type: feedback
---

A partir del 2026-05-11, este agente debe invocarse ANTES de cualquier `git commit` para auditar los cambios que se van a commitear.

**Why:** Felipe / el coordinador estaba commiteando con working files en raiz del proyecto en lugar de bajo el agente que los usaba (ej. `_tmp_dv/` en raiz). Este tipo de drift estructural se acumula rapido si no hay un gate antes del commit.

**How to apply:**

1. Cuando te invoquen pre-commit, mira `git status --short` + `git diff --cached --stat`.
2. Auditar especificamente:
   - Working files / outputs sueltos en raiz del repo (todo eso va a `agentes/<fase>/<agente>/_tmp/` o bajo `outputs/`).
   - Naming convention: `<CLIENTE>_<TipoContenido>_V<n>[_<variant>].<ext>` para binarios. snake_case para brand_ids y skill names.
   - CLAUDE.md por agente refleja los scripts nuevos (si agregaste script, mencionalo o linkealo).
   - .gitignore: que credenciales (`credentials/`), tokens (`*token*.json`), tmp (`_tmp/`, `_scratch/`), outputs generados no se hayan stageado por error.
   - Que cada nuevo script viva en `agentes/<fase>/<agente>/scripts/` (no en `.claude/scripts/` salvo que sea cross-agente).
   - Brand JSON: si tocaste varios, que sea coherente entre todos (mismo schema, no campos huerfanos).
   - Skills duplicados o redundantes con commands viejos.
3. Devolver veredicto:
   - **PASS**: todo OK, commit limpio.
   - **FLAG**: cosas menores que no bloquean (anotar para fix futuro).
   - **BLOCK**: violaciones criticas que se resuelven antes de commit.
4. Si BLOCK, listar fixes concretos. NO ejecutarlos vos — devolver la lista para que el coordinador decida.

**Excepciones:** commits de merge automatico o de rebase no necesitan auditoria; solo commits de trabajo real.

**Output format esperado:**

```
# Pre-commit audit — <hora>

## Staged files (N)
- list short

## Findings
[BLOCK] descripcion + fix sugerido
[FLAG]  descripcion + nota
[PASS]  todo lo demas

## Veredicto
PASS / FLAG / BLOCK
```
