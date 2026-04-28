---
name: optimizar
description: Use this skill when Felipe asks to analyze campaign performance and get actionable decisions (SCALE/KILL/ITERATE/HOLD) for a client's active Meta campaigns. Triggers "optimizar [cliente]", "analizar campanas de [cliente]", "que hacemos con [cliente]", "como estan las campanas de [cliente]", "dame el analisis de [cliente]", "que pausamos de [cliente]", "que escalamos de [cliente]", "revision de performance de [cliente]".
---

# Skill: Optimizar Campañas

Une el análisis de performance, la clasificación SCALE/KILL/ITERATE/HOLD y las recomendaciones accionables en un solo flujo. El resultado es una tabla de decisiones lista para ejecutar — con o sin acceso a la API de Meta.

## Antes de ejecutar

Necesitás:
1. **Cliente** (nombre exacto en `shared/brands/`).
2. **Período de análisis** (default: últimos 7 días).
3. **Datos de performance**: pueden venir de dos fuentes:
   - **Opción A (con API):** se pullea directamente de Meta — solo necesitás el `campaign_id` o trabajás a nivel cuenta.
   - **Opción B (sin API / manual):** el usuario pega los datos de Meta Ads Manager — se los pedís en formato tabla.

Si no te dicen qué opción usar, preguntá si hay acceso activo a la API.

## Pasos

### 1. Cargar el brand y los benchmarks

```python
from scripts.output_manager import load_brand
brand = load_brand(cliente)
ad_account_id = brand["meta_ads"]["ad_account_id"]
```

Los benchmarks default son los de DV (CPL target USD 5, CTR min 0.5%, hook rate min 10%). Si el cliente tiene targets específicos, preguntá o buscalos en outputs anteriores.

### 2A. Opción A — Pull desde Meta API

```python
from scripts.meta_api import MetaAdsAPI
from scripts.campaign_analyzer import analyze_campaign, detect_fatigue, generate_recommendations

api = MetaAdsAPI(ad_account_id=ad_account_id)

# Pull insights de los últimos 7 días a nivel ad
insights = api.get_insights(
    campaign_id=campaign_id,  # o None para toda la cuenta
    date_range={"date_preset": "last_7d"},
    fields=[
        "ad_name", "spend", "impressions", "reach", "frequency",
        "clicks", "ctr", "actions", "cost_per_action_type", "video_play_actions"
    ],
    breakdowns=[]
)
```

### 2B. Opción B — Datos manuales

Pedile al usuario que pegue los datos en este formato (copiable desde Meta Ads Manager):

```
Nombre del anuncio | Impresiones | Alcance | Frecuencia | Clics | CTR | Gasto | Leads | CPL | Hook Rate (3s)
```

Una fila por anuncio. Los datos que no estén disponibles se dejan en blanco.

### 3. Correr el análisis

```python
from scripts.campaign_analyzer import analyze_campaign, detect_fatigue, generate_recommendations

analyses = analyze_campaign(insights)
fatigued = detect_fatigue(insights)
recs = generate_recommendations(analyses)
```

### 4. Generar la tabla de decisiones

Mostrá el resultado en este formato:

```markdown
# Análisis de Performance — [Cliente]
**Período:** [fechas]
**Fecha del análisis:** [hoy]

## Tabla de decisiones

| Anuncio | CPL | CTR | Hook Rate | Gasto | Leads | Decisión | Acción inmediata |
|---|---|---|---|---|---|---|---|
| [nombre] | USD X | X% | X% | USD X | N | SCALE | Subir budget 20% |
| [nombre] | USD X | X% | X% | USD X | N | KILL | Pausar |
| [nombre] | USD X | X% | X% | USD X | N | ITERATE | Pedir variante al Creative Director |
| [nombre] | USD X | X% | X% | USD X | N | HOLD | Esperar 48hs |

## Resumen

- **SCALE (N):** [nombres]
- **KILL (N):** [nombres]
- **ITERATE (N):** [nombres]
- **HOLD (N):** [nombres]

## Recomendaciones

[Lista de recomendaciones generadas por generate_recommendations()]

## Creativos con fatiga

[Si detect_fatigue() encontró algo, listarlo acá con nivel ALERTA/CRITICO]

## Necesidades de producción

[Cuántos creativos nuevos hacen falta para reemplazar KILL + ITERATE]
```

### 5. Preguntar si ejecutar los cambios

Antes de tocar algo en Meta, preguntá:

```
¿Ejecutamos los cambios en Meta? Podemos:
- Pausar los KILL directamente (via API)
- Escalar budget de los SCALE (via API)
- Generar el brief creativo para los ITERATE (para Creative Director)

¿Qué hacemos?
```

### 6. Ejecución (si confirma)

**Pausar KILL:**
```python
api.pause_ad(ad_id)  # o api.update_ad_status(ad_id, "PAUSED")
```

**Escalar SCALE:**
```python
# Aumentar budget del ad set un 20%
api.update_ad_set_budget(ad_set_id, nuevo_budget)
```

**Brief para ITERATE:**
```python
from scripts.brief_generator import generate_creative_brief
from scripts.output_manager import save_output

brief = generate_creative_brief(cliente, analyses, date_start, date_end)
save_output(cliente, "brief_creativo", "feedback_loop", brief)
```

### 7. Guardar el análisis

```python
from scripts.output_manager import save_output
save_output(cliente, "analisis", f"performance_{periodo}", contenido_analisis)
```

## Entrega

Mostrá la tabla de decisiones completa. Cerrá con el estado de ejecución:

```
Análisis completo. [N] ads analizados: [N] SCALE, [N] KILL, [N] ITERATE, [N] HOLD.
[Si se ejecutaron cambios]: Pausados [nombres]. Budget escalado en [nombres].
[Si hay brief creativo generado]: Brief creativo guardado en outputs/[cliente]/. Va para Creative Director.
```

Si no se ejecutaron cambios, indicalo claramente para que Felipe sepa que está pendiente.
