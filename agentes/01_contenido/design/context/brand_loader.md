# Brand Loader — protocolo comun

Toda skill creativa debe arrancar leyendo `shared/brands/<cliente>.json` y extraer los campos brand-specific. Lo que el JSON define manda. Lo que el JSON no define, cae al default DV.

## Campos a leer del brand JSON

| Campo JSON | Que define | Default DV si no existe |
|---|---|---|
| `colors` | paleta HEX (primary, dark, accent_primary, accent_secondary, light, gray, white) | DV: #0033CC, #C8FF00, #FF0080, #0A0A0A, #F5F5F0 |
| `color_distribution_rules` | que color va por slide / por bloque | reglas DV (azul apertura+prueba, negro dolor+CTA, off-white solucion) |
| `typography.primary` | tipografia de headlines + body | Plus Jakarta Sans 800/500 |
| `typography.display` | tipografia de numeros gigantes | Space Grotesk 700 |
| `typography_rules` | tamaños minimos, tracking, line-height | defaults design_principles.md |
| `tone_of_voice.principles` | tono y registro | DV: directo, voseo argentino juvenil, sin clichés |
| `tone_of_voice.forbidden_words` | palabras prohibidas | DV: "suenos", "concretar", "tu hogar te espera", "profesionales de confianza" |
| `tone_of_voice.preferred_words` | palabras preferidas | DV: ninguna obligatoria |
| `tone_of_voice.hook_frameworks` | frameworks de hook validos | DV: negacion, empatia, verdad_incomoda (Hormozi) |
| `tone_of_voice.narrative_structure` | estructura narrativa para piezas largas | DV: DOLOR → CONSECUENCIA → SOLUCION → PRUEBA |
| `layouts` | layouts permitidos por tipo de pieza | defaults estructurales |
| `logo` | path, variantes, min_size, clearspace, placement | usar logo.png, min 140px, solo en cierre |
| `visual_style` | reglas visuales especificas (rotaciones, formas, etc.) | defaults design_principles.md |

## Pseudocodigo de carga

```
1. Leer shared/brands/<cliente>.json
2. Si no existe: PARAR. Avisar "no existe el brand system de <cliente>, invocar skill `brand-system`".
3. Extraer:
   - colors → usar HEX literales del JSON, jamas inventar.
   - typography → cargar Google Fonts urls del JSON.
   - tone_of_voice.narrative_structure → si existe, usar esa estructura. Si NO existe, usar DCSP de DV.
   - tone_of_voice.hook_frameworks → si existe, los hooks deben pertenecer a alguno de esos frameworks. Si NO existe, usar Hormozi.
   - tone_of_voice.forbidden_words → unir con la lista negra global de DV (suma, no reemplaza).
   - tone_of_voice.preferred_words → priorizar estas palabras en copy.
   - color_distribution_rules → si existe, mappear color por slide segun esa regla. Si NO, usar mapping default DV.
4. Cualquier copy generado debe pasar por validacion contra forbidden_words antes de renderizar.
```

## Regla de oro

**El brand JSON manda sobre el default DV.** Si el cliente tiene `narrative_structure: "Estructura Achaval"` con steps `[DATO/AUTORIDAD, PROBLEMA MERCADO, VISION EXPERTA, PRUEBA/CTA]`, **no escribas DCSP**. Si tiene `hook_frameworks: [authority, data_driven, market_truth]`, **no uses negacion/empatia/verdad incomoda de Hormozi**.

## Defaults DV (cuando aplican)

Solo cuando el brand JSON NO define el campo correspondiente.

- **Narrativa**: DOLOR → CONSECUENCIA → SOLUCION → PRUEBA
- **Hooks**: negacion (romper creencia) | empatia (nombrar dolor) | verdad_incomoda (decir lo no dicho)
- **Tono**: directo, voseo argentino, sin emojis, sin clichés
- **Forbidden global** (suma a la del brand): "suenos", "concretar", "tu hogar te espera", "profesionales de confianza", "calidad y confianza", "tradicion y experiencia", "acompanamiento personalizado"
- **Color distribution carrusel 6 slides**: slide 1 (primary) | slides 2-3 dolor/consecuencia (dark) | slide 4 solucion (light) | slide 5 prueba (primary) | slide 6 CTA (dark)

## Reglas universales DV (NO overridables por brand)

Estas valen para todo cliente, sin excepcion:

- Sin emojis.
- Sin gradientes multicolor.
- Sin drop shadows >4px o efectos 3D.
- Sin tipografias prohibidas (Comic Sans, Papyrus, Impact, scripts cursivas).
- Headlines minimo 80px, numeros minimo 150px.
- Margen seguro: 80px cuadrado/vertical, 100px stories, 60px placa, 200px flyer A4.
- Maximo 2 tipografias por pieza.
- Maximo 3 colores efectivos por pieza.
- Contraste WCAG AA minimo (4.5:1 body, 3:1 headline).
- Logo solo en cierre de carrusel.
- NUNCA inventar datos (precio, m2, amenities, KPIs).
- NUNCA usar los colores DV exactos para otro cliente.

Estas son las unicas reglas hardcoded en las skills. Todo lo demas viene del brand JSON.
