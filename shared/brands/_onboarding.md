# Onboarding de una marca nueva

Este documento define el flujo que seguís cuando onboardeás un cliente nuevo en Digital View. El objetivo es minimizar la cantidad de intervención del usuario: **ideal es 3 mensajes del usuario en total** para cerrar el brand system.

## Cuándo activar este flujo

Cuando el usuario diga algo como:

- "Nuevo cliente: [nombre]"
- "Onboardeá a [cliente]"
- "Armame el brand system de [cliente]"
- "Hacé un carrusel para [cliente]" pero no existe `brands/[cliente_id].json`

En el último caso, detené el pedido de la pieza, avisá que no hay brand system, y preguntá si querés hacer el onboarding primero.

## Lo que idealmente recibís del usuario en el primer mensaje

El usuario te va a pasar en un solo mensaje:

1. **Nombre comercial del cliente.**
2. **Contexto en 1-3 oraciones:** tipo de negocio, zona geográfica, estructura del equipo, decisor principal (nombre, edad aproximada, perfil), rango de precios de propiedades, objetivo, restricciones.
3. **Logo del cliente** como archivo adjunto.
4. **Screenshots del Instagram del cliente** (idealmente 4-6): grid completo, bio, 2-3 posts individuales, alguna story destacada.

Con eso es suficiente. No necesitás más.

## Si falta información crítica

Si el usuario te pide onboardear un cliente y no te pasa logo ni screenshots, pedílos **una sola vez en un solo mensaje**:

> Para armar el brand system necesito dos cosas: el logo del cliente (PNG o JPG) y 4-6 screenshots del Instagram del cliente. Con eso ya arranco.

No pidas más que eso en esta etapa. Si el cliente no tiene Instagram, aceptá trabajar solo con el logo y el contexto, y avisá que la propuesta va a tener más margen de incertidumbre.

## Flujo de 4 pasos

### Paso 1 — Análisis silencioso (vos solo, sin hablar con el usuario)

Con la información que tenés, hacé estos análisis internamente antes de responder:

**Análisis del logo:**

1. Abrilo con la herramienta `view`.
2. Identificá colores dominantes (HEX aproximados).
3. Identificá estilo tipográfico (serif clásica, sans-serif bold, script, lettering custom, etc.).
4. Identificá la forma (wordmark, isotipo, combinación).
5. Evaluá el nivel corporate-vs-disruptivo (escala 1-10, donde 1 es conservador tradicional y 10 es punk zine).

**Análisis de los screenshots del Instagram:**

1. Abrí cada screenshot con `view`.
2. Mirá el grid completo primero: ¿qué colores dominan?, ¿qué tipo de contenido hay (propiedades, agente en cámara, reels, carruseles)?, ¿hay coherencia visual o es desordenado?
3. Mirá posts individuales: ¿cómo son las captions?, ¿qué tono usan?, ¿usan emojis?, ¿aparece el nombre del agente?
4. Evaluá el estado actual del Instagram (escala 1-10): ¿es cliché inmobiliario tradicional (9-10), balanceado (5-7), ya disruptivo (1-4)?
5. Identificá los errores obvios que tienen y que DV puede resolver.

**Cruce de contexto:**

1. ¿Quién es el decisor (edad, perfil)? Esto define cuánto podés empujar el tono.
2. ¿Qué tipo de cliente final atraen (compradores tradicionales, inversores jóvenes, desarrolladores)? Esto define el target visual.
3. ¿La red de referidos actual del cliente es tradicional (abogados, escribanos) o moderna (emprendedores, ejecutivos)? Esto define cuánta disrupción pueden tolerar sin romper su red.
4. ¿Tiene alguna restricción de branding externa (franquicia tipo RE/MAX, afiliación a algún colegio)?

### Paso 2 — Primera respuesta al usuario: análisis + 3 sistemas propuestos

Esta es tu **primera intervención hacia el usuario**. Es el mensaje más importante de todo el onboarding.

Estructurala exactamente así:

```
Analicé todo. Resumen de lo que vi:

**Logo:** [descripción en 2-3 líneas: forma, colores, estilo tipográfico, nivel corporate-vs-disruptivo, qué transmite]

**Instagram actual:** [descripción en 3-5 líneas: estado del grid, tipo de contenido, tono de captions, nivel de cliché, qué están haciendo bien, qué están haciendo mal]

**Mi lectura:** [1 párrafo con tu análisis estratégico: dónde están parados hoy, qué necesitan, qué pueden tolerar, qué los diferenciaría sin romper su red actual]

Te propongo 3 sistemas, ordenados de más conservador a más disruptivo. [Si hay una continuidad valiosa que mantener, como el color del logo, mencionalo acá].

---

**Sistema A — [Nombre descriptivo]**
Paleta: [HEX primario], [HEX secundario/neutros], [HEX acento]
Tipografías: [primaria] + [secundaria]
Filosofía: [1-2 frases]
Mejor para: [1 frase sobre para qué audiencia funciona]

**Sistema B — [Nombre descriptivo]** [marcar con estrella si es la recomendación]
[mismo formato]

**Sistema C — [Nombre descriptivo]**
[mismo formato]

---

¿Cuál vamos?
```

**Reglas para los 3 sistemas:**

- **Deben ser realmente distintos.** No 3 variantes del mismo sistema. Típicamente: A es más conservador, B balanceado, C más disruptivo.
- **Marcá tu recomendación con una estrella**. Siempre dale tu opinión, no seas neutral. El usuario tiene que poder elegir rápido.
- **Si hay un color del logo que tiene valor, respetalo** en al menos 2 de los 3 sistemas.
- **Si el cliente es franquicia con restricciones** (RE/MAX, Century 21), los 3 sistemas deben respetar las restricciones pero diferenciarse en layout, tipografía y acentos.
- **Nunca propongas los colores exactos de Digital View** (#0033CC, #C8FF00, #FF0080) para otro cliente. Esos son de DV.

### Paso 3 — Segunda respuesta: slide de muestra del sistema elegido

Cuando el usuario elige uno de los sistemas, **NO guardes el JSON todavía**. Primero generá UN solo slide de muestra.

Típicamente el slide 1 de un carrusel de captación es el mejor para validar porque muestra: color de fondo, tipografía de headline, tono de copy y estructura general.

**Cómo generar la muestra:**

1. Cargá `templates/carrusel_captacion.html`.
2. Reemplazá en memoria (sin guardar todavía el JSON) los colores y tipografías del sistema elegido.
3. Escribí un copy breve adaptado al tono del cliente (no al tono DV). Si el cliente es tradicional, no uses muletillas argentinas fuertes. Si el cliente es moderno, podés ir más agresivo.
4. Renderizá con `scripts/render.py`.
5. Mostrá solo ese slide en chat.

**Tu mensaje al usuario con la muestra:**

```
Acá va el slide 1 con Sistema [X] aplicado. Fijate el nivel de disrupción: [breve descripción de qué decisiones tomaste y por qué].

[imagen del slide]

¿Va así o ajusto algo?
```

Si el usuario pide ajustes, hacelos en el sistema propuesto (cambiar un color, cambiar la tipografía, cambiar el nivel de agresividad del copy), volvé a renderizar y mostrá de nuevo. No guardes el JSON hasta que apruebe.

### Paso 4 — Guardado final

Cuando el usuario dice "dale", "guardalo", "va" o equivalente:

1. Generá el `brand_id`: todo en minúsculas, espacios como guión bajo, sin tildes ni caracteres especiales.
   - "Alvarez Propiedades" → `alvarez_propiedades`
   - "RE/MAX Pilar Elite" → `remax_pilar_elite`
   - "López & Asociados" → `lopez_asociados`
2. Cargá `brands/_template.json` como base.
3. Completá todos los campos con los datos del sistema aprobado.
4. Guardá el archivo como `brands/[brand_id].json`.
5. Creá la carpeta `brands/assets/[brand_id]/` y copiá el logo ahí con el nombre `logo.png` (o el formato original si es otro).
6. Confirmá al usuario con un mensaje corto:

```
Listo. Brand system de [nombre del cliente] guardado en `brands/[brand_id].json`.
Logo en `brands/assets/[brand_id]/logo.png`.

Ya podés pedirme piezas para esta marca. Ejemplos:
- "Hacé un carrusel de captación para [cliente] sobre [tema]"
- "Placa de propiedad para [cliente]: [datos]"

Tono registrado: [resumen de 1 línea del tono que va a usar].
```

## Reglas generales del onboarding

### Máximo de intervenciones del usuario

El usuario **no debería tener que intervenir más de 3 veces** en todo el flujo:

1. Mensaje inicial con contexto + adjuntos.
2. Elección del sistema (A, B o C).
3. Aprobación de la muestra (o 1-2 ajustes si hace falta).

Si te encontrás pidiendo una cuarta intervención, revisá qué información te falta deducir vos. El objetivo es minimizar carga cognitiva del usuario.

### Preguntas obligatorias (ninguna)

**No hagas las preguntas genéricas "¿qué tono querés?", "¿qué audiencia?", "¿qué referencias?"**. Esas preguntas se deducen del contexto + logo + screenshots. El viejo flujo de 3 preguntas obligatorias queda deprecado.

### Preguntas solo si es estrictamente necesario

Las únicas preguntas válidas son las que no podés deducir vos:

- Si el cliente tiene una restricción de branding no mencionada (franquicia, colegio profesional).
- Si hay una contradicción entre el logo y el contexto que no sabés resolver (ej: logo super tradicional pero el dueño pide full disruptivo).
- Si falta un dato crítico específico (ej: no sabés si es venta o alquiler).

En esos casos hacé **una sola pregunta**, lo más puntual posible, y esperá la respuesta.

### Qué hacer si el cliente no tiene Instagram

Si el usuario dice "el cliente todavía no tiene Instagram" o "la cuenta está vacía":

1. Trabajá solo con el logo y el contexto.
2. Avisá en tu primera respuesta: "Como no hay Instagram actual para analizar, los 3 sistemas que te propongo se basan solo en el logo y el contexto que me diste. Si después tenés referencias específicas o cuentas que te gustan, las incorporamos."
3. Seguí el flujo normal.

### Qué hacer si el cliente tiene restricciones de franquicia

Ejemplos típicos: RE/MAX (rojo, azul, blanco), Century 21 (dorado, negro), Keller Williams.

1. Reconocé la restricción en tu análisis del logo: "Veo que es una franquicia [X], así que los colores corporativos son obligatorios."
2. Los 3 sistemas deben respetar los colores base pero diferenciarse en:
   - Proporción de uso de cada color (ej: RE/MAX usa 60% blanco + 40% rojo/azul en sistema A, al revés en sistema C).
   - Tipografía (diferentes elecciones dentro de lo permitido).
   - Layout (grilla simétrica vs asimétrica, texto grande vs moderado).
   - Tono de copy (más tradicional vs más disruptivo).
3. Explicá al usuario qué elementos **no podés cambiar** y en qué tenés libertad.

### Nivel de disrupción por tipo de cliente

Usá esta tabla mental como guía:

| Perfil del cliente | Nivel de disrupción recomendado |
|---|---|
| Inmobiliaria familiar tradicional (dueño 50+, red abogados/escribanos) | 3-5 (balanceado) |
| Agencia mediana con equipo mixto | 5-7 (moderno) |
| Top producer joven individual (25-40) | 7-9 (disruptivo) |
| Desarrollador premium torres de lujo | 4-6 (sofisticado moderno) |
| Franquicia internacional | 4-6 (dentro de restricciones) |
| Agencia nueva que quiere romper | 8-10 (full disruptivo, tipo DV) |

Donde 1 es conservador total, 10 es tipo DV full disruptivo.

### Tono de copy por tipo de cliente

- **Cliente tradicional:** sin muletillas argentinas fuertes. Nada de "che", "carajo", "posta", "chamuyo". Usar voseo neutro, frases firmes pero profesionales.
- **Cliente moderno balanceado:** voseo argentino natural, algunas muletillas suaves. Sin "carajo" ni "posta". Sí "dale", "mirá".
- **Cliente joven disruptivo:** tono completo DV con muletillas argentinas, humor negro, confrontación directa.
- **Cliente premium:** voseo neutro, tono aspiracional pero no cliché. Sin muletillas.

El agente debe **guardar el perfil de tono en el campo `tone_of_voice.principles`** del JSON del brand para aplicarlo automáticamente en cada pieza futura.

## Ejemplo completo simulado

Para que tengas una referencia concreta, este es cómo se ve un onboarding perfecto de punta a punta.

### Mensaje del usuario (mensaje 1 de 3)

> Nuevo cliente: Alvarez Propiedades.
> Inmobiliaria familiar de San Isidro, 3 asesores, operan Zona Norte. Dueña Marcela Alvarez, 52 años. Propiedades USD 180k-700k. Quieren modernizarse sin perder seriedad (red de abogados y escribanos).
> Adjunto: logo + 6 screenshots del Instagram @alvarezpropiedades.
> Armame el brand system.

### Respuesta del agente (respuesta 1 de 3)

> Analicé todo. Resumen de lo que vi:
>
> **Logo:** wordmark "ALVAREZ" en serif clásica, color verde oliva oscuro, con línea decorativa debajo. Transmite tradición, establecimiento, confianza. Corporate nivel 8/10.
>
> **Instagram actual:** grid con fotos de propiedades estilo real estate tradicional, fondos blancos con precios en beige, tipografías serif finas. Captions con emojis de casas y llaves. Ningún reel con Marcela o el equipo en cámara. Es el cliché inmobiliario de Zona Norte, bien ejecutado pero indistinguible de 30 cuentas similares.
>
> **Mi lectura:** están bien posicionados pero mimetizados. Necesitan diferenciarse sin romper el rapport con abogados y escribanos. No pueden ir full DV, pero sí modernizarse con autoridad.
>
> Los 3 sistemas mantienen el verde oliva del logo porque es valioso preservar continuidad.
>
> ---
>
> **Sistema A — Editorial Clásico Moderno**
> Paleta: #3D4F2B verde oliva, #F2EDE4 crema, #1A1A1A negro, #C9A961 dorado champagne
> Tipografías: Playfair Display + Inter
> Filosofía: elegancia serif con jerarquías modernas, estilo revista The Gentlewoman.
> Mejor para: mantener público actual + sumar compradores que valoran buen diseño.
>
> **Sistema B — Minimalismo Autoritario** (recomendación)
> Paleta: #3D4F2B verde oliva, #FFFFFF blanco, #0A0A0A negro, #D2691E terracota
> Tipografías: Inter ExtraBold + Inter Regular
> Filosofía: limpio, sin adornos, contraste brutal entre espacios vacíos y tipografía grande.
> Mejor para: audiencia mixta. Abogados no se incomodan, top producers ven la diferencia.
>
> **Sistema C — Moderno Disruptivo Controlado**
> Paleta: #3D4F2B verde oliva, #0A0A0A negro, #F5F5F5 off-white, #E8B923 mostaza
> Tipografías: Space Grotesk ExtraBold + Inter
> Filosofía: grilla rota, números gigantes, highlights con marker, estilo DV con paleta terrosa.
> Mejor para: si Marcela quiere reinventar completamente el posicionamiento.
>
> ---
>
> ¿Cuál vamos?

### Mensaje del usuario (mensaje 2 de 3)

> Sistema B. Mostrame una muestra antes de guardar.

### Respuesta del agente (respuesta 2 de 3)

> [Genera slide 1 con Sistema B]
>
> Acá va el slide 1. Fijate: verde oliva del logo como fondo, terracota en el botón/acento, tipografía Inter ExtraBold grande, tono de copy firme pero sin jerga argentina fuerte porque la audiencia tradicional no lo pediría.
>
> [imagen]
>
> ¿Va así o ajusto algo?

### Mensaje del usuario (mensaje 3 de 3)

> Dale, guardalo.

### Respuesta del agente (respuesta 3 de 3)

> Listo. Brand system de Alvarez Propiedades guardado en `brands/alvarez_propiedades.json`.
> Logo en `brands/assets/alvarez_propiedades/logo.png`.
>
> Ya podés pedirme piezas. Ejemplos:
> - "Carrusel de captación para Alvarez Propiedades sobre el valor de vender con exclusividad"
> - "Placa de propiedad para Alvarez Propiedades: [datos]"
>
> Tono registrado: firme, profesional, moderno, sin jerga juvenil argentina. Voseo neutro.

---

## Checklist interno antes de responder

Antes de mandar tu primera respuesta al usuario, chequeá:

- ¿Abrí y miré todos los screenshots con `view`?
- ¿Abrí y miré el logo con `view`?
- ¿Los 3 sistemas que propongo son realmente distintos entre sí?
- ¿Mi recomendación está marcada claramente?
- ¿Mantengo al menos 1 color del logo en al menos 2 de los 3 sistemas?
- ¿Ninguno de los sistemas usa los colores exactos de Digital View (#0033CC, #C8FF00, #FF0080)?
- ¿El análisis estratégico es específico (no genérico) al cliente?
- ¿Consideré la audiencia y la red del cliente para definir el nivel de disrupción?

Antes de mandar la segunda respuesta (con la muestra):

- ¿El copy del slide está adaptado al tono del cliente (no al tono DV)?
- ¿Los colores del render coinciden con el sistema elegido?
- ¿Renderizaste UN solo slide, no los 6?

Antes de guardar el JSON final:

- ¿El `brand_id` está bien formado (minúsculas, sin tildes, sin caracteres especiales)?
- ¿Todos los campos del template están completos?
- ¿El logo está copiado en `brands/assets/[brand_id]/`?
- ¿El campo `tone_of_voice` refleja el nivel de disrupción correcto para el cliente?
