---
name: kickoff
description: Use this skill when a new client needs to be onboarded — to validate that everything required for other agents to work exists. Triggers "kickoff [cliente]", "onboarding de [cliente]", "arrancamos con cliente nuevo [nombre]", "que falta para empezar con [cliente]", "validar onboarding de [cliente]", "chequea si [cliente] esta onboardeado".
---

# Skill: Kickoff de cliente nuevo

Valida que un cliente tiene todo lo necesario para que los agentes especializados puedan trabajar. Genera el checklist de onboarding y marca qué falta.

## Antes de ejecutar

Necesitás el **nombre del cliente** (tal como debería aparecer en `shared/brands/`, ej. `lopez_propiedades`, `mauro_peralta`). Si no lo recibiste, preguntalo. Si el nombre tiene espacios, usá guiones bajos.

## Pasos

### 1. Verificar brand JSON

```python
from scripts.output_manager import brand_exists, load_brand, list_brands

existe = brand_exists(cliente)
brand = load_brand(cliente) if existe else None
```

Si no existe, el primer paso bloqueante es crear el JSON. Mostrá el template vacío que hay que completar:

```json
{
  "name": "Nombre visible del cliente",
  "logo_url": "",
  "colors": {
    "primary": "#000000",
    "secondary": "#FFFFFF",
    "accent": "#000000",
    "text": "#000000"
  },
  "fonts": {
    "headline": "Poppins",
    "body": "Inter"
  },
  "meta_ads": {
    "ad_account_id": "act_XXXXXXXXXX",
    "page_id": "XXXXXXXXXX"
  },
  "buyer_persona": {
    "age_min": 30,
    "age_max": 60,
    "pain_points": [],
    "aspirations": []
  },
  "messaging": {
    "tone": "",
    "pain_angles": [],
    "ctas": []
  }
}
```

Indicá que el archivo va en `shared/brands/<cliente>.json`.

### 2. Validar campos del brand (si existe)

Si el brand existe, revisá campo por campo:

| Campo | Requerido por | OK? |
|---|---|---|
| `meta_ads.ad_account_id` | Media Buyer | Tiene `act_` prefix? |
| `meta_ads.page_id` | Media Buyer | Está completado? |
| `colors.primary` | Design | Es un HEX válido? |
| `fonts.headline` | Design | Tiene nombre de fuente? |
| `buyer_persona.pain_points` | Creative Director / Copywriter | Tiene al menos 2 items? |
| `buyer_persona.aspirations` | Creative Director / Copywriter | Tiene al menos 1 item? |
| `messaging.tone` | Copywriter | Está descrito? |
| `messaging.pain_angles` | Creative Director | Tiene al menos 2 items? |

### 3. Verificar estructura de carpetas de Drive

Indicá que hay que crear (o verificar que existe) la estructura estándar en Drive:

```
CLIENTE/
├── 00 Ficha del Cliente/
│   ├── Formulario CORE completado
│   ├── Identidad visual (logos, colores, referencias)
│   └── Accesos y contactos
├── 01 Estrategia/
├── 02 Producciones/
├── 03 Estaticos/
├── 04 Campanas Meta/
└── 05 Reportes/
```

No podés verificar Drive automáticamente — marcalo como "a confirmar por Elias/Bauti".

### 4. Generar checklist de onboarding

Armá un documento Markdown con el estado de cada item:

```markdown
# Kickoff — [Cliente] — [Fecha]

## Brand System
- [x] JSON existe en shared/brands/<cliente>.json
- [ ] Ad account ID configurado (act_XXXXX)
- [ ] Page ID configurado
- [x] Colores primarios definidos
- [ ] Buyer persona completo (pain points + aspirations)
- [ ] Ángulos de dolor definidos (mínimo 2)

## Drive
- [ ] Carpeta del cliente creada
- [ ] Ficha del Cliente / Formulario CORE completado
- [ ] Identidad visual subida (logos, colores)
- [ ] Accesos y contactos cargados

## Meta
- [ ] Ad account accesible desde el Business Portfolio DV
- [ ] Página de Facebook conectada
- [ ] Pixel configurado (si aplica)

## Listo para arrancar con:
- [ ] Creative Director (necesita: buyer persona + ángulos)
- [ ] Copywriter (necesita: brand system completo)
- [ ] Design (necesita: colores + fuentes + logos)
- [ ] Media Buyer (necesita: ad_account_id + creativos)

## Bloqueantes
[Lista de lo que falta antes de poder arrancar]
```

### 5. Guardar

```python
from scripts.output_manager import save_output
save_output(cliente, "kickoff", "onboarding", contenido_checklist)
```

## Entrega

Mostrá el checklist completo con el estado de cada item. Indicá claramente:
- Qué está listo
- Qué está bloqueando el arranque
- Quién tiene que resolver cada cosa pendiente

Cerrá con:
```
Para arrancar con producción necesitamos: [lista de bloqueantes]. Va para [Elias / Bauti según el item].
```

Si todo está completo: "Cliente listo. Podés correr `/nueva-campana <cliente>` para arrancar el flujo de producción."
