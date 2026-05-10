---
name: kickoff
description: Use this skill when a new client needs to be onboarded — to scaffold the brand JSON, leads/state files, create Drive folder structure via MCP, and notify the team. Triggers "kickoff [cliente]", "onboarding de [cliente]", "arrancamos con cliente nuevo [nombre]", "que falta para empezar con [cliente]", "validar onboarding de [cliente]", "chequea si [cliente] esta onboardeado", "init kickoff [cliente]".
---

# Skill: Kickoff de cliente nuevo (full auto)

Tiene dos modos:

- **Modo VALIDAR** (default): chequea que el cliente ya tiene todo listo y devuelve checklist con lo que falta. No toca nada.
- **Modo INIT** (`--init` o pedido explícito "arrancá kickoff de X" cuando el cliente no existe): scaffold automático end-to-end. Crea brand JSON desde template, leads_clientes JSON, state JSON, estructura Drive vía MCP, y notifica a Elias/Nico por WA.

## Antes de ejecutar

Necesitás:
- **`cliente_id`**: snake_case sin espacios (ej. `lopez_propiedades`, `viviana_sasia`).
- **`brand_name`** (display): cómo aparece en el mundo real (ej. "López Propiedades").

Si el usuario no los dio, preguntalos.

## Flujo

### Paso 1 — Resolver modo

```python
from pathlib import Path
brand_path = Path("shared/brands") / f"{cliente_id}.json"
existe = brand_path.exists()
```

- Si NO existe Y el usuario pidió "init"/"arrancar"/"crear" → modo INIT.
- Si NO existe Y el usuario pidió validar → reportá que falta scaffold y ofrecé correr INIT.
- Si SÍ existe → modo VALIDAR.

### Paso 2A — Modo INIT (scaffold + Drive + notify)

**2A.1 — Scaffold local** (Bash):

```bash
python agentes/00_coordinador/scripts/kickoff_init.py <cliente_id> --name "<Brand Display>" --notify
```

El script crea:
- `shared/brands/<cliente_id>.json` (clonado de `toribio_achaval.json`, campos cliente-específicos marcados como `<TODO_KICKOFF>`)
- `agentes/02_comercial/data/leads_clientes/<cliente_id>.json`
- `shared/state/<cliente_id>.json`
- Manda WA a Elias y Nico con el resumen + lista de TODOs.

Capturá el JSON output. Tiene `pendings[]` (campos a completar) y `next_step`.

**2A.2 — Estructura Drive vía MCP**:

Usá las tools `mcp__claude_ai_Google_Drive__*`. Estructura estándar DV:

```
<Brand Display>/
├── 00 Ficha del Cliente/
├── 01 Estrategia/
├── 02 Producciones/
├── 03 Estaticos/
├── 04 Campanas Meta/
└── 05 Reportes/
```

Pseudo-flujo:
1. `search_files` para chequear si la carpeta raíz `<Brand Display>` ya existe.
2. Si no, `create_file` con MIME folder (o el equivalente del MCP server) en raíz Drive DV.
3. Para cada subcarpeta 00-05, `create_file` dentro de la raíz creada.
4. Capturá los `folder_id` para reportar.

**Si el MCP de Drive no está disponible** (tool no listado / error de auth): no falles. Reportá "Drive: no se creó automáticamente, hacelo a mano en `<carpeta DV>`" como TODO para Elias.

**2A.3 — Reportá el resultado**:

```
# Kickoff INIT — <Brand Display> — <fecha>

## Scaffold local
- shared/brands/<cliente_id>.json (creado, con TODOs)
- agentes/02_comercial/data/leads_clientes/<cliente_id>.json
- shared/state/<cliente_id>.json

## Drive
- Carpeta raíz: <link o "manual">
- Subcarpetas 00-05: <ok | manual>

## WA enviado a
- Elias: <numero>
- Nico: <numero>

## Pendientes (orden de prioridad)
1. Elias: completar formulario CORE + identidad visual + accesos Meta
2. Felipe: confirmar ad_account_id (act_XXX) y page_id en el brand JSON
3. Nico: revisar tone_of_voice heredado del template y ajustar al cliente real
4. Bauti: subir referencias visuales del cliente a 00 Ficha del Cliente

## Próximo paso
Cuando Elias confirme CORE completado, correr `/kickoff <cliente_id>` (modo validar)
para chequear que todo está listo antes de pasar a producción.
```

### Paso 2B — Modo VALIDAR

Mismo checklist que la versión vieja del skill. Cargá el brand JSON, chequeá:

| Campo | Requerido por | OK si |
|---|---|---|
| `brand_id` | todos | == cliente_id |
| `brand_name` | todos | no es `<TODO_KICKOFF>` |
| `positioning` | Creative/Copy | no es `<TODO_KICKOFF>` |
| `meta_ads.ad_account_id` | Media Buyer | tiene prefix `act_` |
| `meta_ads.page_id` | Media Buyer | no es `<TODO_KICKOFF>` |
| `colors.primary` | Design | HEX válido |
| `tone_of_voice.forbidden_words` | Validators | lista no vacía |
| `tone_of_voice.preferred_words` | Validators | lista no vacía |
| `tone_of_voice.hook_frameworks` | Creative | dict no vacío |
| `references` | Design | dict con al menos 1 entrada |

Verificación adicional:
- Drive (a confirmar por Elias): no se puede automatizar el chequeo de existencia de subcarpetas sin MCP.
- Pipeline: chequeá que `agentes/02_comercial/data/leads_clientes/<cliente_id>.json` exista.

Devolvé el checklist con bloqueantes y siguiente acción.

## Tono

Directo. Sin frases de relleno. Cada salida cierra con: "Va para [persona]. Próximo paso: [acción concreta]."

## Lo que NUNCA hacés en este skill

- No tocás `tone_of_voice.forbidden_words` heredado del template salvo que el usuario lo pida explícito (es base segura).
- No mandás WA si `--notify` falló: reportá el error y dejá que Elias avise a mano.
- No avanzás a fase 3 (Preproducción) si quedan TODOs en el brand JSON.
- No creás campañas en Meta. Eso lo hace Felipe cuando recibe el handoff.
