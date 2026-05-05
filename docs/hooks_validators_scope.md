# Hooks + Validators — Scope cerrado

**Fecha**: 2026-05-04
**Contexto**: definicion del set final de hooks Claude Code y validators (agents) para mejorar el flow operativo de DV. Sale de exploracion `/gsd-explore`.

## Decisiones

| Decision | Eleccion | Por que |
|---|---|---|
| Modo de los hooks | **Hibrido**: hard gate para errores duros, soft warning para el resto | No traba iteracion rapida; bloquea solo lo critico |
| Identificacion de cliente | **`active_client` explicito + fallback cwd** | Auto-mageria falla silenciosamente; explicito es trazable |
| Dedupe | **Nivel 1 (filename + fecha <14d)** | Caso A es el unico real. Hash y embeddings son sobre-ingenieria |
| Fase-gate | **Skill manual `/check-fase-gate`**, no hook automatico | Saltar fases es valido en sesiones de prueba; hook bloqueante rompe flujo |
| Validador de tono | **Multi-brand: lee `shared/brands/<active_client>.json`** | Cada brand tiene su `tone_of_voice` distinto. Un solo validator hardcodeado-DV no servia |

## Hooks finales (4)

| Hook | Trigger | Accion |
|---|---|---|
| `SessionStart` | inicio de sesion | Carga ficha compacta de la brand activa (positioning + principles + forbidden + preferred) via `additionalContext` |
| `UserPromptSubmit` | cada prompt | (Pendiente) re-inyecta brand activa si no esta en contexto |
| `PreToolUse Write` | `outputs/<cliente>/**` | Dedupe nivel 1 + naming-validator (hard gate) |
| `PostToolUse Write` | por patron de archivo | Auto-invoca el validator correspondiente |

### Tabla de auto-validacion en PostToolUse

| Patron archivo | Validator | Modo | Aplica a |
|---|---|---|---|
| `plan_campana*.md` | brief-pauta-validator | **Hard gate** | 04_pauta |
| `*guion*.md`, `*script*.md` | guion-validator | Soft | 01_contenido |
| `*hook*.md` | hook-scorer | Soft | 01_contenido + 04_pauta |
| `*caption*.md`, `*copy*.md`, `*reporte*.md` | tono-brand-validator | Soft | todos |

## Validators (estado actual)

| Validator | Estado | Notas |
|---|---|---|
| `brief-pauta-validator` | existente | Sin cambios |
| `hook-scorer` | existente | Pendiente refactor menor: leer `hook_frameworks` de la brand |
| `tono-brand-validator` | **refactorizado de tono-dv-validator** | Lee brand JSON dinamicamente. 4 capas: universal / forbidden_words regex / principles semantico / visual_style.dont |
| `guion-validator` | **a crear** | Estructura DCSP + hook Hormozi en primeros 3s. Soft |
| `naming-validator` | **a crear** | `CLIENTE_TipoContenido_Vx.ext`. Hard gate |
| `dv-project-optimizer` | existente | Sin cambios |

## Dedupe + fase-gate

- `dedupe-validator` **descartado como agent**. Se vuelve funcion adentro del PreToolUse hook (filename match + mtime <14d).
- `fase-gate-validator` **descartado como hook**. Se vuelve skill manual `/check-fase-gate <cliente>`.

## Foco de aplicacion

Los validators automaticos cubren intensivamente **01_contenido + 04_pauta** (donde se generan guiones, hooks, captions, planes de pauta). Los demas agentes (00, 02, 03, 05) heredan solo `tono-brand-validator` + `active_client`.

## Plan de implementacion (orden)

1. ~~Refactor `tono-dv-validator` -> `tono-brand-validator`~~ **DONE**
2. ~~Mecanismo `active_client` + SessionStart hook~~ **DONE**
3. Validator nuevo: `guion-validator`
4. Validator nuevo: `naming-validator`
5. Hooks PostToolUse para auto-invocar validators
6. Hook PreToolUse con dedupe + naming
7. Skill manual `/check-fase-gate`
8. (Opcional) UserPromptSubmit re-inyectar brand
9. Pasada `fewer-permission-prompts` para no llenar de prompts al usuario

## Pendientes menores

- Agregar `disruption_scale` a `digital_view.json` y `toribio_achaval.json` (los unicos 2 brands sin ese campo).
- Excluir `zipcode.json` (no es brand) de la lista que devuelve `resolve_active_client.py --list`. Hoy se cuela.
- Refactor de `hook-scorer` para leer `hook_frameworks` de la brand activa en vez de tener Hormozi hardcodeado.

## Archivos creados/modificados en esta vuelta

- `.claude/agents/tono-brand-validator.md` (nuevo)
- `.claude/agents/tono-dv-validator.md` (eliminado)
- `.claude/scripts/resolve_active_client.py` (nuevo)
- `.claude/scripts/session_start_load_brand.py` (nuevo)
- `.claude/settings.json` (agregado SessionStart hook)
- `.gitignore` (agregado `**/.claude/state/`)
- `docs/hooks_validators_scope.md` (este archivo)
