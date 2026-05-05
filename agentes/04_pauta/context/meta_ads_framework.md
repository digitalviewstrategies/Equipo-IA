# Framework de Meta Ads — DV

## Estructura de campana

Toda campana de Meta Ads de DV sigue esta jerarquia:

```
Campaign (1 por objetivo por cliente)
├── Ad Set 1 (audiencia/segmento A)
│   ├── Ad 1 (creativo variante 1)
│   ├── Ad 2 (creativo variante 2)
│   └── Ad 3 (creativo variante 3)
├── Ad Set 2 (audiencia/segmento B)
│   ├── Ad 1
│   ├── Ad 2
│   └── Ad 3
└── Ad Set 3 (testing/lookalike)
    ├── Ad 1
    ├── Ad 2
    └── Ad 3
```

**Reglas de estructura:**

- 1 campana por objetivo por cliente. No mezclar Leads y Traffic en la misma campana.
- 2-4 ad sets por campana. Cada ad set testea una audiencia o segmento distinto.
- 3-5 ads por ad set. Cada ad testea un creativo distinto (angulo, formato, o variante de hook).
- Si un ad set tiene menos de 3 ads activos, hay que pedir creativos nuevos.

---

## Objetivos de campana

| Objetivo Meta | Cuando usarlo | Clientes DV tipicos |
|---|---|---|
| **Leads** | Generar formularios de contacto. El 80% de campanas DV usan esto. | Inmobiliarias, top producers, desarrolladores |
| **Traffic** | Enviar trafico al sitio web o perfil de IG. Para awareness o contenido. | Clientes en fase de brand building |
| **Conversions** | Acciones en sitio web (agendar visita, descargar brochure). Requiere pixel + evento configurado. | Desarrolladores con landing pages |

**Default DV: Leads.** Solo cambiar si Felipe lo indica o si el brief del cliente lo requiere.

---

## Categoria especial

**Default DV: `special_ad_categories: []` (sin categoria especial).**

No declarar HOUSING salvo que Felipe lo pida explicitamente para una campana puntual. Declarar HOUSING activa restricciones de targeting (edad, genero, radio minimo 17km, codigo postal limitado) y achica reach. Para el grueso de campanas DV en Argentina no es necesario.

Si en algun caso se declara HOUSING, tener en cuenta:
- Radio minimo 17km en geo targeting.
- Sin segmentacion por edad/genero en algunos mercados.
- Advantage+ audience con limitaciones adicionales.

---

## Naming convention

```
Campaign: [CLIENTE]_[OBJETIVO]_[YYYY-MM]
Ad Set:   [CLIENTE]_[AUDIENCIA]_[UBICACION]
Ad:       [CLIENTE]_[FORMATO]_[ANGULO]_V[N]
```

**Reglas:**

- CLIENTE: nombre corto del brand system (ej: `LopezProps`, `DV`, `Toribio`).
- OBJETIVO: `Leads`, `Traffic`, `Conversions`.
- AUDIENCIA: nombre descriptivo del segmento (ej: `CompradoresCABA`, `InversoresZN`, `RetargetingIG`).
- UBICACION: `FeedStories`, `Reels`, `AllPlacements`.
- FORMATO: tipo de creativo (ej: `Reel`, `Carrusel`, `ImagenCuadrada`, `Video`).
- ANGULO: angulo de dolor o concepto (ej: `CostoOportunidad`, `MiedoAlquilar`, `PrecioM2`).
- V[N]: version del creativo (V1, V2, V3...).

Ejemplos completos:

- `Toribio_Leads_2026-04`
- `Toribio_CompradoresZN_FeedStories`
- `Toribio_Reel_CostoOportunidad_V1`

---

## Placements

**Default DV:**

| Placement | Incluido | Notas |
|---|---|---|
| Feed (Facebook + Instagram) | Si | Siempre |
| Stories (Facebook + Instagram) | Si | Siempre |
| Reels (Facebook + Instagram) | Si | Siempre |
| Audience Network | **No** | Trafico basura, nunca activar |
| Messenger | Opcional | Solo si el cliente usa Messenger para atencion |
| Search | Opcional | Bajo volumen, no priorizar |

**Formatos por placement:**

- Feed: cuadrado (1080x1080) o vertical (1080x1350).
- Stories/Reels: vertical (1080x1920).
- Si un creativo es video, el aspect ratio correcto para cada placement es critico.

---

## Configuracion de ad set

### Presupuesto

- Presupuesto a nivel de ad set (no CBO salvo que Felipe indique lo contrario).
- Minimo USD 5/dia por ad set.
- Split: 70% en audiencias probadas, 30% en testing.

### Schedule

- Start date: dia de lanzamiento.
- End date: sin fecha de fin (ongoing) salvo campanas puntuales (lanzamiento de proyecto, evento).
- Horarios: 6:00 a 23:00 hora Argentina (UTC-3). No correr ads de madrugada.

### Optimizacion

- Para Leads: optimizar por "Leads" (no link clicks).
- Para Traffic: optimizar por "Landing Page Views" (no link clicks).
- Bid strategy: "Lowest cost" como default. Solo usar "Cost cap" si Felipe lo pide.

---

## Configuracion de ad

### Formato de creativo

| Formato | Uso | Specs |
|---|---|---|
| Imagen unica | Testeo rapido, placas | 1080x1080 o 1080x1350, <30MB |
| Video | Reels, testimonios, demos | 1080x1920 (vertical), <4GB, <240min |
| Carrusel | Educativo, recorridos | 2-10 cards, 1080x1080 cada una |

### Copy del ad

- **Primary text**: 1-3 lineas. Hook primero, beneficio despues, CTA al final. Sin emojis.
- **Headline**: max 40 caracteres. Directo, sin cliches.
- **Description**: opcional, 1 linea de soporte.
- **CTA button**: "Mas informacion" para traffic, "Enviar mensaje" o "Registrarte" para leads.

### Lead form (para objetivo Leads)

Campos estandar DV:

1. Nombre completo
2. Telefono (con prefijo)
3. Email
4. Pregunta personalizada: "Que tipo de propiedad buscas?" o "Que zona te interesa?"

Configurar como "Higher intent" (agrega paso de confirmacion, mejora calidad del lead).

---

## Checklist pre-lanzamiento

Antes de activar cualquier campana, verificar:

- [ ] special_ad_categories definido (default: [])
- [ ] Naming correcto en todos los niveles
- [ ] Creativos aprobados por el cliente (via Elias)
- [ ] Pixel/evento configurado (si aplica)
- [ ] Presupuesto confirmado con Felipe
- [ ] Lead form configurado y testeado
- [ ] Placements correctos (sin Audience Network)
- [ ] Horarios configurados
- [ ] Audiencias revisadas (sin overlap significativo entre ad sets)
- [ ] Link de destino funcionando (si aplica)
