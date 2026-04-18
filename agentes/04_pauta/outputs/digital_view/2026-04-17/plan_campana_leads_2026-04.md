# Plan de Campana — Digital View — 2026-04-17

## Objetivo

- Objetivo de campana: **Leads** (OUTCOME_LEADS)
- Meta de leads/mes: **60** (USD 180 / USD 3 CPL)
- CPL target: **USD 3** (target del brand; primer lanzamiento — validar en semana 2, el piso realista para B2B suele estar en USD 5-10)
- Presupuesto mensual: **USD 180**
- Presupuesto diario: **USD 6**
- Ciclo: mensual, renovar en mayo

## Estructura

```
DV_Leads_2026-04 — USD 6/dia
└── DV_DuenosInmobiliariasCABAZN_AllPlacements — USD 6/dia (100%)
    ├── DV_Reel_VerdadIncomoda_V1      (Pendiente — brief a Creative Director)
    ├── DV_Reel_EmpatiaZonaprop_V2     (Pendiente)
    └── DV_Carrusel_NegacionMarketing_V3 (Pendiente)
```

Nota sobre la estructura reducida: el framework DV pide 2-4 ad sets y minimo USD 300/mes. Con USD 180/mes la unica estructura que entrega data es **1 ad set con 3 creativos variantes**. Si se duplican ad sets, no hay delivery suficiente por ad set para evaluar (<1000 impresiones / ad set).

## Audiencias

### Ad Set 1: DV_DuenosInmobiliariasCABAZN_AllPlacements

- **Tipo**: Prospeccion (primer lanzamiento, sin lista de leads para lookalike).
- **Geo**: CABA + GBA Zona Norte (Vicente Lopez, Olivos, San Isidro, Acassuso, Beccar, Martinez, San Fernando).
- **Edad**: 30-60.
- **Genero**: Todos.
- **Intereses**: Real estate agent, Real estate broker, Real estate investment, Property management, Meta Ads, Instagram marketing, Lead generation, CRM, Small business, Zonaprop, Argenprop, Mercado Libre Inmuebles.
- **Comportamientos**: Small business owners, Business page admins, Engaged shoppers.
- **Exclusiones**: Empleados DV (si existe custom audience), leads DV actuales (si hay lista).
- **Budget**: USD 6/dia.
- **Optimization goal**: LEAD_GENERATION.
- **Bid strategy**: Lowest cost.

Buyer persona base (del CLAUDE.md del equipo): duenos de inmobiliarias pequenas/medianas (1-20 agentes), top producers individuales que quieren escalar, desarrolladores inmobiliarios con proyectos en pozo o terminados. Capacidad de invertir fee DV + minimo USD 300/mes de pauta — o sea este anuncio filtra por nivel economico via intereses y comportamientos business.

## Creativos

| Ad | Formato | Angulo | Archivo fuente | Estado |
|----|---------|--------|----------------|--------|
| DV_Reel_VerdadIncomoda_V1      | Reel 1080x1920     | Verdad incomoda sobre boca en boca | Pendiente | Brief enviado |
| DV_Reel_EmpatiaZonaprop_V2     | Reel 1080x1920     | Empatia con espera de Zonaprop     | Pendiente | Brief enviado |
| DV_Carrusel_NegacionMarketing_V3 | Carrusel 1080x1080 | Negacion "subir placas no es marketing" | Pendiente | Brief enviado |

Los creativos aprobados reemplazan los placeholders antes de activar (ver `brief_creativo_leads_2026-04.md`).

## Placements

- Feed (Facebook + Instagram): si
- Stories (Facebook + Instagram): si
- Reels (Facebook + Instagram): si
- Audience Network: no

## Schedule

- Inicio: TBD (depende de creativos listos + billing resuelto).
- Fin: ongoing (renovacion mensual).
- Horarios: 6:00 a 23:00 hora Argentina (UTC-3).

## Lead Form

- Campos:
  1. Nombre completo
  2. Telefono (con prefijo)
  3. Email
  4. Pregunta personalizada: "Cuantos agentes tiene tu inmobiliaria?" (4 opciones: 1-3 / 4-10 / 11-20 / +20 / soy top producer independiente).
- Tipo: **Higher Intent** (paso de confirmacion extra).
- Mensaje de agradecimiento: "Listo. Un asesor de DV te escribe en las proximas 24hs."

## Categoria especial

- `special_ad_categories: []` — DV anuncia servicios B2B de consultoria, no anuncia propiedades. HOUSING no aplica.
- Si Meta rechaza el anuncio pidiendo categoria especial, reevaluar (documentar en `context/meta_ads_framework.md` como excepcion).

## Flags antes de activar

- **Cuenta en grace period** (account_status=9 al 2026-04-17). Regularizar billing de `act_881977527791996` antes de activar.
- **Sin pixel** instalado. Optimizacion por instant form nativo (no se puede usar Conversions API ni retargeting por web).
- **CPL target USD 3** es optimista para B2B (target profesional, pool chico). Evaluar al cierre de semana 2 y ajustar expectativa si el realista resulta USD 5-10.
- **Page ID**: 61557477811665 (facebook.com) vinculada a @digitalviewagency.

## Checklist pre-lanzamiento

- [ ] Creativos aprobados por Felipe (pendiente brief creativo)
- [ ] Billing de la cuenta `act_881977527791996` regularizado
- [ ] Page 61557477811665 vinculada al ad set
- [ ] Lead form creado y testeado con lead de prueba
- [ ] Naming correcto en todos los niveles
- [ ] Placements correctos (sin Audience Network)
- [ ] Horarios configurados (6:00-23:00 UTC-3)
- [ ] Audiencia sin overlap (solo 1 ad set, no aplica overlap interno)
- [ ] `special_ad_categories: []` confirmado

## Metricas de evaluacion

En semana 2 evaluar con matriz SCALE/KILL/ITERATE/HOLD (ver `context/metricas_benchmarks.md`):

- SCALE: CPL < USD 3 + CTR > benchmark + delivery >1000 impresiones.
- KILL: CPL > USD 6 despues de 1000 impresiones, O hook rate <10%, O CTR <0.5%.
- ITERATE: CPL cerca de USD 3 con tendencia negativa → pedir variante al Creative Director.
- HOLD: <1000 impresiones, mantener 48hs mas.

## Proximos pasos

1. **Creative Director** define guiones concretos por cada angulo (ver brief).
2. **Design** produce las 3 piezas siguiendo brand system DV.
3. **Elias / Felipe** aprueba creativos.
4. Valen/Felipe regulariza billing de la cuenta.
5. **Media Buyer** ejecuta Workflow B (crear campana en Meta API).
6. Activar y monitorear semana 1.
