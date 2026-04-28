# Mapa de Agentes DV

Referencia operativa para el Coordinador. Describe cada agente: ubicación, inputs que necesita, outputs que produce, paths reales para leer su data.

---

## Shared

**Brand system de cada cliente:**
```
shared/brands/<cliente>.json
```
Campos clave: `name`, `colors`, `fonts`, `meta_ads.ad_account_id`, `meta_ads.page_id`, `buyer_persona`.

Los clientes activos son los archivos `.json` en `shared/brands/` que no empiezan con `_`.

---

## 01 — Creative Director

**Path:** `agentes/01_contenido/creative_director/`

**Qué necesita para trabajar:**
- Brand del cliente en `shared/brands/<cliente>.json`
- Objetivo de la producción (Meta Ads, organic, estrategia mensual)
- Contexto adicional si hay (resultados de campañas previas, brief de pauta)

**Qué produce:**
- Guiones de video (briefs de producción completos)
- Briefs de carrusel (para Design)
- Estrategias de contenido mensuales

**Dónde guarda sus outputs:**
```
agentes/01_contenido/creative_director/outputs/<cliente>/<YYYY-MM-DD>/
```
Tipos de archivo: `guion_*.md`, `brief_carrusel_*.md`, `estrategia_*.md`

**Trigger para pedirle trabajo:**
- Cliente nuevo sin guiones
- Feedback loop del Media Buyer (brief_creativo disponible en pauta/outputs)
- Estrategia mensual nueva

---

## 02 — Copywriter

**Path:** `agentes/01_contenido/copywritter/`

**Qué necesita para trabajar:**
- Brand del cliente
- Objetivo del ad (venta_propiedad / captacion_propietario / captacion_inmobiliaria)
- Placement (feed / stories / reels)
- Datos opcionales: zona, tipología, precio, diferencial, resultados recientes

**Qué produce:**
- Meta Ads copy (2 variantes por objetivo)
- Captions orgánicos
- Banco de hooks
- Estrategia de copy

**Dónde guarda sus outputs:**
```
agentes/01_contenido/copywritter/outputs/<cliente>/<YYYY-MM-DD>/
```
Tipos de archivo: `meta_ad_*.md`, `caption_*.md`, `banco_hooks_*.md`, `estrategia_copy_*.md`

**Skills disponibles:**
- `/meta-ad` → copy para Meta Ads
- `/caption` → caption orgánico
- `/banco-hooks` → banco de hooks
- `/estrategia-copy` → estrategia de copy

**Trigger para pedirle trabajo:**
- Antes de lanzar una campaña nueva (necesita copy aprobado)
- Cuando hay brief de performance del Media Buyer con ángulos ganadores

---

## 03 — Design

**Path:** `agentes/01_contenido/design/`

**Qué necesita para trabajar:**
- Brand del cliente (colores, tipografías)
- Brief de carrusel del Creative Director O pedido directo de pieza
- Copy del Copywriter (para carruseles y Meta Ads estáticos)

**Qué produce (tipos de pieza):**
- Carruseles de captación (6 slides, 1080x1080)
- Carruseles educativos (6-8 slides)
- Meta Ads estáticos (1080x1080 feed + 1080x1920 vertical)
- Flyers de lanzamiento (A4 vertical)
- Placas de propiedad (1080x1080 o 1080x1350)

**Dónde guarda sus outputs:**
```
agentes/01_contenido/design/output/<cliente>/<YYYY-MM-DD>/<tipo_pieza>/slide_NN.png
```

**Tecnología:** HTML templates → Playwright → PNG (no Figma, no Canva)

**Trigger para pedirle trabajo:**
- Cuando el Creative Director entregó un brief de carrusel
- Cuando el Copywriter entregó copy aprobado para estático
- Cuando el Media Buyer detectó fatiga y pide nuevas piezas visuales

---

## 04 — Media Buyer (Pauta)

**Path:** `agentes/04_pauta/`

**Qué necesita para trabajar:**
- Brand del cliente (con `meta_ads.ad_account_id`)
- Creativos aprobados (videos en Drive o PNGs del Design)
- Copy aprobado del Copywriter
- Plan de campaña o brief de Google Sheets

**Qué produce:**
- Planes de campaña
- Campañas en Meta (via API)
- Análisis SCALE/KILL/ITERATE/HOLD
- Reportes semanales y mensuales
- Briefs creativos y de diseño para el feedback loop

**Dónde guarda sus outputs:**
```
agentes/04_pauta/outputs/<cliente>/<YYYY-MM-DD>/
```
Tipos de archivo: `plan_campana_*.md`, `analisis_*.md`, `reporte_semanal_*.md`, `reporte_mensual_*.md`, `brief_creativo_*.md`, `brief_diseno_*.md`

**Dueño humano:** Felipe (Director de Campañas)

**Trigger para pedirle trabajo:**
- Cuando hay creativos + copy aprobados y listos para subir
- Para análisis semanal de performance
- Para reportes a clientes

---

## Orden de producción (flujo completo)

```
NUEVO CLIENTE
     │
     ▼
[Kickoff] → brand JSON + ficha Drive + CORE completado
     │
     ▼
[Creative Director] → guiones + briefs de carrusel
     │
     ├──► [Copywriter] → copy Meta Ads + captions
     │
     └──► [Design] → PNG carruseles + estáticos
               │
               ▼
          [Media Buyer] → plan campaña → crea en Meta → monitorea
               │
               ▼ (si detecta fatiga o resultados)
          [brief_creativo] → vuelve al Creative Director
```

**Regla de oro:** Ningún agente trabaja sin que el anterior haya terminado. Design no arranca sin brief de Creative Director. Media Buyer no lanza sin creativos + copy aprobados.

---

## Señales de alerta (para el `/status`)

| Señal | Qué significa |
|---|---|
| No hay JSON en `shared/brands/` | Cliente no onboardeado |
| No hay outputs en `creative_director/outputs/` | No hay contenido generado aún |
| No hay outputs en `copywritter/outputs/` | No hay copy listo |
| No hay PNGs en `design/output/` | No hay piezas visuales |
| Solo hay `brief_creativo_*.md` en `04_pauta/outputs/` | El Media Buyer pide creativos nuevos |
| Hay `reporte_semanal_*.md` reciente | Campaña activa, reportes corriendo |
