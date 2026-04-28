---
name: analizar
description: Use this skill when Felipe needs to analyze Meta campaign performance and get SCALE/KILL/ITERATE/HOLD recommendations for a client. Triggers "analizar [cliente]", "que pasa con las campanas de [cliente]", "dame el analisis de [cliente]", "como estan los ads de [cliente]", "que matamos de [cliente]", "revision de [cliente]".
---

# Skill: analizar — Workflow C

Analizar rendimiento de campañas activas y generar recomendaciones accionables (SCALE / KILL / ITERATE / HOLD).

## Contexto necesario

Antes de empezar, cargá estos archivos:

1. `context/metricas_benchmarks.md` — KPIs, benchmarks, matriz de decisión SCALE/KILL/ITERATE/HOLD.
2. `context/presupuestos_guia.md` — reglas de presupuesto y scaling.

Si hay contradicción entre tu criterio y lo que dicen estos archivos, ganan los archivos.

## Pasos

### 1. Pullear data

```python
from scripts.meta_api import MetaAdsAPI
from scripts.output_manager import load_brand

brand = load_brand(cliente)
api = MetaAdsAPI(ad_account_id=brand["meta_ads"]["ad_account_id"])
insights = api.get_insights(campaign_id, date_range, fields, breakdowns)
```

Si no tenés los IDs de campaña, preguntá a Felipe o consultá los outputs de planificación en `outputs/<cliente>/`.

### 2. Clasificar cada ad y ad set

Usá `scripts/campaign_analyzer.py`:

```python
from scripts.campaign_analyzer import analyze_campaign, detect_fatigue
results = analyze_campaign(insights, benchmarks)
fatigued = detect_fatigue(insights)
```

Criterios de clasificación (ver detalle en `metricas_benchmarks.md`):

| Clasificación | Criterio |
|---|---|
| **SCALE** | CPL < target AND CTR > benchmark AND +500 USD spend |
| **KILL** | CPL > 2x target después de 1000+ impresiones, O hook rate <10%, O CTR <0.5% |
| **ITERATE** | CPL cerca del target pero tendencia negativa, O buen hook rate pero bajo CTR |
| **HOLD** | <1000 impresiones, data insuficiente |

### 3. Generar recomendaciones

Para cada ad/ad set clasificado, una acción concreta:

- **SCALE**: "Subir budget 20% en 3 días." (nunca más del 20% por vez)
- **KILL**: "Pausar. El ángulo X no resuena con esta audiencia."
- **ITERATE**: "Pedir variante nueva al Creative Director con el mismo ángulo pero hook distinto."
- **HOLD**: "Esperar 48hs más de data antes de decidir."

### 4. Identificar fatiga

Si `detect_fatigue` devuelve ads con frequency >3.0: marcarlos como candidatos a rotar aunque estén en SCALE. Incluir en el output.

### 5. Guardar

```python
from scripts.output_manager import save_output
save_output(cliente, "analisis", nombre, contenido)
```

Cerrá con: "Va para Felipe. Si hay creativos para KILL o ITERATE, próximo paso: brief creativo para el Creative Director."
