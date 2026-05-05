---
name: crear-campana
description: Use this skill when Felipe wants to create a campaign in Meta Ads from an approved plan. Takes the plan output and executes the structure via Meta API. Triggers "crear campana en meta", "ejecutar el plan de [cliente]", "lanzar campana de [cliente]", "crear la estructura en meta", "ejecutar el plan aprobado", "subir la campana a meta".
---

# Skill: Crear Campaña en Meta — Workflow B

Ejecuta en Meta Ads la estructura definida en el plan aprobado. El plan ya fue validado por Felipe. Tu trabajo es leerlo, verificar que está completo, y ejecutar la creación vía API.

## Antes de ejecutar

Necesitás:
1. **Cliente** (nombre exacto en `shared/brands/`).
2. **Plan aprobado**: debe existir en `outputs/<cliente>/` como `plan_campana_<nombre>.md`.
3. **`.env` configurado** con `META_ACCESS_TOKEN`, `META_APP_ID`, `META_APP_SECRET`, `META_BUSINESS_ID`.

Si el plan no existe o no está aprobado, parás y pedís el plan. No creés nada sin un plan aprobado.

Si el `.env` no existe o el token venció, avisás a Felipe y no ejecutás.

## Pasos

### 1. Cargar el brand y el plan

```python
from scripts.output_manager import load_brand, load_latest_output

brand = load_brand(cliente)
ad_account_id = brand["meta_ads"]["ad_account_id"]
plan = load_latest_output(cliente, "plan_campana")
```

Antes de tocar nada, mostrá un resumen del plan que vas a ejecutar:

```
Voy a crear en Meta:
- Campaña: [nombre]
- Objetivo: [OUTCOME_LEADS / OUTCOME_TRAFFIC / OUTCOME_SALES]
- Ad account: [ad_account_id]
- Ad sets: [N] ([nombres])
- Ads por ad set: [N] ([descripción de creativos])
- Budget total diario: USD [X]

¿Confirmamos?
```

Esperá confirmación explícita antes de ejecutar. Si Felipe dice "sí" o equivalente, arrancás.

### 2. Crear la campaña

```python
from scripts.meta_api import MetaAdsAPI

api = MetaAdsAPI(ad_account_id=ad_account_id)

campaign = api.create_campaign(
    name=plan["campaign"]["name"],
    objective=plan["campaign"]["objective"],
    special_ad_categories=[]
)
campaign_id = campaign["id"]
```

No declarar HOUSING salvo que Felipe lo pida explicitamente para una campana puntual.

### 3. Crear los ad sets

Por cada ad set del plan:

```python
ad_set = api.create_ad_set(
    campaign_id=campaign_id,
    name=ad_set_data["name"],
    targeting=ad_set_data["targeting"],
    daily_budget=ad_set_data["daily_budget_cents"],
    placements=ad_set_data["placements"]
)
```

El targeting debe incluir `geo_locations` con lat/lng + radio (17km default para inmobiliario CABA/GBA). Ver `context/audiencias_inmobiliario.md` para los segmentos prearmados.

### 4. Subir imágenes y crear ads

Por cada ad:

```python
# Subir imagen
image_hash = api.upload_image(image_path)["images"][image_name]["hash"]

# Crear el ad
ad = api.create_ad(
    ad_set_id=ad_set["id"],
    name=ad_data["name"],
    creative_spec={
        "page_id": brand["meta_ads"]["page_id"],
        "image_hash": image_hash,
        "title": ad_data["title"],
        "body": ad_data["body"],
        "call_to_action_type": ad_data["cta"]
    }
)
```

Si `page_id` es null en el brand system, parás antes de crear ads y avisás: "Falta configurar el page_id de [cliente] en shared/brands/. No puedo crear ads sin él."

Si los creativos no existen en `../../01_contenido/design/output/<cliente>/`, avisás y pausás la creación de ads (la campaña y los ad sets ya creados quedan en PAUSED hasta tener creativos).

### 5. Verificar la estructura creada

Después de crear todo, verificá contra el plan:

```python
campaigns = api.get_campaigns(status="ALL")
```

Mostrá la verificación:

```
Estructura creada en Meta:

Campaña: [nombre] — ID: [campaign_id] — Status: PAUSED
├── Ad Set: [nombre] — ID: [adset_id] — Budget: USD X/día
│   ├── Ad: [nombre] — ID: [ad_id]
│   └── Ad: [nombre] — ID: [ad_id]
└── Ad Set: [nombre] — ID: [adset_id] — Budget: USD X/día
    └── Ad: [nombre] — ID: [ad_id]
```

### 6. Guardar los IDs

```python
from scripts.output_manager import save_output
import json

ids = {
    "campaign_id": campaign_id,
    "ad_sets": [{"name": ..., "id": ...}],
    "ads": [{"name": ..., "id": ...}]
}
save_output(cliente, "draft_ids", "estructura", json.dumps(ids, indent=2))
```

### 7. Activar cuando estén los creativos

La campaña se crea en PAUSED por default. Para activar:

```python
api.update_campaign_status(campaign_id, "ACTIVE")
```

Nunca activés sin que Felipe lo confirme y sin que todos los ads tengan creativos aprobados.

## Entrega

Cerrá con:

```
Campaña [nombre] creada en Meta.
Status: PAUSED (esperando activación de Felipe).
IDs guardados en outputs/[cliente]/[fecha]/draft_ids_estructura.md.

Próximo paso: cuando estén los creativos aprobados de Design, activamos.
Si faltó algún creativo: brief_creativo para Creative Director.
```
