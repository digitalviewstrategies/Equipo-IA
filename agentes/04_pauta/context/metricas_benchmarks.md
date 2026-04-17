# Metricas y Benchmarks — DV Real Estate

## KPIs principales

| Metrica | Definicion | Como se calcula |
|---|---|---|
| **CPL** | Cost per Lead | Gasto total / Leads generados |
| **CTR** | Click-Through Rate | Clicks / Impresiones x 100 |
| **CPC** | Cost per Click | Gasto total / Clicks |
| **CPM** | Cost per Mille | Gasto / Impresiones x 1000 |
| **Hook Rate** | Tasa de enganche (video) | Video views 3s / Impresiones x 100 |
| **Hold Rate** | Tasa de retencion (video) | ThruPlay / Video views 3s x 100 |
| **Frequency** | Frecuencia promedio | Impresiones / Alcance |
| **Lead Quality Rate** | Calidad de leads | Leads calificados / Leads totales x 100 |

---

## Benchmarks DV para real estate argentino

Estos son los benchmarks internos de DV basados en campanas de inmobiliarias en CABA y Zona Norte. Se actualizan trimestralmente.

### Leads (objetivo principal)

| Metrica | Malo | Aceptable | Bueno | Excelente |
|---|---|---|---|---|
| CPL | >USD 10 | USD 6-10 | USD 3-6 | <USD 3 |
| CTR (feed) | <0.8% | 0.8-1.5% | 1.5-3% | >3% |
| CTR (stories) | <0.5% | 0.5-0.8% | 0.8-1.5% | >1.5% |
| Hook Rate | <15% | 15-30% | 30-50% | >50% |
| Hold Rate | <10% | 10-20% | 20-35% | >35% |
| Frequency (7 dias) | >4.0 | 2.5-4.0 | 1.5-2.5 | 1.0-1.5 |
| Lead Quality Rate | <10% | 10-25% | 25-40% | >40% |

### Traffic

| Metrica | Malo | Aceptable | Bueno | Excelente |
|---|---|---|---|---|
| CPC | >USD 0.80 | USD 0.40-0.80 | USD 0.15-0.40 | <USD 0.15 |
| CTR | <1% | 1-2% | 2-4% | >4% |

---

## Matriz de decision: SCALE / KILL / ITERATE / HOLD

### SCALE — Escalar presupuesto

**Criterios (todos deben cumplirse):**

- CPL < target del cliente (default USD 5).
- CTR > benchmark "Aceptable" para su placement.
- Minimo USD 30 gastados (o 500+ impresiones con resultados consistentes).
- Tendencia estable o mejorando en los ultimos 3 dias.

**Accion:** subir budget 20% maximo cada 3 dias. No duplicar de golpe.

### KILL — Pausar

**Criterios (cualquiera es suficiente):**

- CPL > 2x target despues de 1000+ impresiones.
- Hook rate <10% despues de 1000+ impresiones.
- CTR <0.5% despues de 1000+ impresiones.
- 0 leads despues de USD 20 gastados.
- Frequency >5.0 (fatiga extrema).

**Accion:** pausar el ad. Documentar por que fallo. No borrar (mantener data).

### ITERATE — Pedir variante nueva

**Criterios:**

- CPL entre 1x y 1.5x del target (cerca pero no alcanza).
- Buen hook rate (>25%) pero bajo CTR (problema en el body del video o copy).
- Buena CTR pero mal CPL (problema en el lead form o landing).
- Tendencia de CPL subiendo gradualmente (fatiga temprana).

**Accion:** generar brief para Creative Director pidiendo variante del mismo angulo con hook diferente, o mismo hook con body distinto. No matar el original hasta que la variante este activa.

### HOLD — Esperar mas data

**Criterios:**

- <1000 impresiones.
- <48 horas de delivery.
- <USD 10 gastados.
- Metricas volatiles (sube y baja dia a dia).

**Accion:** no tocar nada. Revisar en 48-72 horas.

---

## Fatiga creativa

**Indicadores de fatiga:**

| Indicador | Threshold | Que hacer |
|---|---|---|
| Frequency >3.0 (7 dias) | Alerta | Preparar nuevos creativos |
| Frequency >4.0 (7 dias) | Critico | Rotar creativos ya |
| CTR cayendo >30% vs semana anterior | Alerta | Monitorear 48hs mas |
| CPL subiendo >40% vs semana anterior | Critico | Pausar y rotar |
| Hook rate cayendo >25% vs semana anterior | Alerta | El hook se quemo, pedir variante |

**Regla general:** un creativo dura 2-4 semanas antes de fatigarse en audiencias de real estate argentino. Tener siempre 2-3 creativos en reserva.

---

## Score compuesto para ranking de creativos

Cuando necesites comparar creativos entre si, usa este score:

```
Score = (CPL_score x 0.40) + (CTR_score x 0.25) + (HookRate_score x 0.20) + (Volume_score x 0.15)
```

Donde cada componente se normaliza de 0 a 100:

- **CPL_score**: 100 si CPL = 0, 0 si CPL >= 2x target. Lineal entre ambos.
- **CTR_score**: 0 si CTR = 0, 100 si CTR >= 4%. Lineal.
- **HookRate_score**: 0 si hook rate = 0, 100 si hook rate >= 60%. Lineal.
- **Volume_score**: 0 si impresiones = 0, 100 si impresiones >= 10000. Lineal, cap en 100.

Uso: ordenar ads por score para reportes y decisiones de rotacion.

---

## Campos de insights de la API

Para pullear data, estos son los campos mas usados:

```python
FIELDS_STANDARD = [
    "campaign_name", "adset_name", "ad_name",
    "spend", "impressions", "reach", "frequency",
    "clicks", "ctr", "cpc", "cpm",
    "actions", "cost_per_action_type",
    "video_p25_watched_actions", "video_p50_watched_actions",
    "video_p75_watched_actions", "video_p100_watched_actions",
    "video_play_actions",  # 3-second views
]

BREAKDOWNS_STANDARD = ["publisher_platform", "platform_position"]
```

**Nota:** `actions` contiene los leads (filtrar por `action_type == "lead"`). `video_play_actions` son los 3-second views para calcular hook rate.
