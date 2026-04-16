# Principios de Diseño — DV Design Agent

Reglas visuales inamovibles que el agente sigue en todas las piezas, sin importar el cliente.

## Principios generales (aplican a toda marca)

### 1. Jerarquía tipográfica brutal

En cualquier pieza hay UNA cosa que es lo más importante, y esa cosa ocupa entre el 50% y el 70% del área visual. Todo lo demás orbita alrededor.

- Si es un slide de hook, lo más importante es el titular.
- Si es un slide de dato, lo más importante es el número.
- Si es una placa de propiedad, lo más importante es el precio.
- Si es un flyer, lo más importante es la foto + el precio.

**Nunca hay 2 elementos compitiendo por ser lo más importante.**

### 2. Contraste máximo

Cada pieza usa una regla de 3 colores:

- 1 color de fondo.
- 1 color principal de texto (blanco o negro, dependiendo del fondo).
- 1 color de acento para destacar.

Nunca usar 5 colores en una pieza. Nunca. Si el brand system tiene 5 colores, tenés que elegir cuáles 3 aplican a esta pieza específica.

### 3. Un mensaje por slide

Un slide = una idea. Si querés comunicar dos ideas, son dos slides.

Señales de que estás violando esta regla:
- El slide tiene más de 2 bloques de texto.
- El lector tiene que hacer pausa para procesar.
- Hay un "y también" en el copy.

### 4. Espacio negativo generoso

Los slides respiran. El texto nunca toca los bordes. El margen de seguridad es de al menos 80px para slides cuadrados 1080x1080, y 60px para placas de propiedad.

Si el texto no entra en el margen de seguridad, el problema es que hay demasiado texto. Reducí el texto, no el margen.

### 5. Grillas sutilmente rotas

La simetría perfecta es aburrida. Cualquier pieza debe tener al menos UN elemento rotado entre 0.5° y -3° para romper la perfección. Opciones típicas:

- El botón CTA rotado -1.5°.
- Uno de los cuadrantes de la grilla de prueba rotado 0.5°.
- El highlight de una palabra rotado -1°.
- Un scribble a mano alzada rotado -8°.

**Nunca rotar más de 15° nada**, salvo scribbles cursivos.

### 6. Consistencia entre slides de una misma pieza

Los slides de un carrusel deben verse como parte del mismo sistema visual. Formas de asegurar consistencia:

- Mismo top tag con línea horizontal en todos los slides.
- Mismo formato de número de página (ej: "02 / 06") en todos.
- Mismo grid de márgenes.
- Paleta consistente según la distribución definida en el brand system.

## Reglas de composición

### Márgenes seguros

| Formato | Tamaño | Margen seguro mínimo |
|---|---|---|
| Carrusel cuadrado | 1080x1080 | 80px |
| Carrusel vertical | 1080x1350 | 80px |
| Meta Ad vertical (stories) | 1080x1920 | 100px, + 20% top/bottom libre para UI |
| Placa propiedad cuadrada | 1080x1080 | 60px |
| Placa propiedad vertical | 1080x1350 | 60px |
| Flyer A4 | 2480x3508 | 200px |

### Tamaños de tipografía mínimos

| Uso | Tamaño mínimo | Tamaño ideal |
|---|---|---|
| Headline principal | 80px | 100-140px |
| Subheadline | 30px | 40-60px |
| Body copy | 22px | 28-36px |
| Caption / metadata | 16px | 18-22px |
| Número gigante (dato) | 150px | 300-420px |

**Si un texto es menor a 16px, el agente tiene que cuestionarse si realmente hace falta.** La respuesta suele ser que no.

### Pesos tipográficos

- Headlines: siempre 800 o 900 (extra bold / black).
- Subheadlines: 700 o 800.
- Body bold: 700.
- Body regular: 500.
- Captions: 400 o 500.

**Nunca usar pesos 100, 200 o 300 (thin, light).** No sobreviven al formato mobile.

### Jerarquía visual por orden de importancia

En cada slide debe quedar claro en qué orden el lector debe procesar la información:

1. Lo primero que ve.
2. Lo segundo.
3. Lo tercero.

Si en tu diseño esto no es obvio, está mal compuesto. Ajustá tamaños, pesos o colores hasta que sea obvio.

## Prohibiciones absolutas

Estas cosas **nunca** aparecen en piezas del agente:

### Tipografía

- Comic Sans, Papyrus, Impact, Bradley Hand, cursivas script elegantes.
- Más de 2 tipografías distintas en una misma pieza.
- Pesos thin o extra light como tipografía principal.
- Letter-spacing positivo extremo en headlines (tipo "A N U N C I O"). Solo para tags cortos de metadata.

### Color

- Gradientes multicolor (amarillo → rosa → celeste).
- Paletas pasteles o tierra (beige, crema, salmón, verde agua).
- Dorado como color primario (cliché inmobiliario).
- Más de 2 colores de acento en una pieza.
- Texto azul oscuro sobre fondo azul oscuro (contraste insuficiente).

### Elementos gráficos

- Drop shadows exagerados (más de 4px de blur).
- Efectos 3D, bisel, relieve.
- Stock photos de "familia feliz frente a casa" o "señor saludando con llaves".
- Emojis (todos).
- Iconos mal dibujados o pixelados.
- Borders redondeados mayores a 16px (excepto en botones específicos).

### Composición

- Textos que llenan todo el slide hasta los bordes.
- Slides con 5+ bloques de información.
- Texto sobre imagen sin overlay de contraste cuando la foto es compleja.
- Simetría perfecta sin ningún elemento que la rompa.
- Listas con bullets tradicionales (círculo, cuadrado, guión).

## Cuándo usar IA generativa (Nano Banana)

El agente puede usar Gemini 2.5 Flash Image en estos casos:

### Sí usar

- **Mejorar una foto de propiedad** que el cliente envió con mala iluminación. Prompt tipo: "Enhance this real estate photo: improve lighting, fix white balance, make colors more vibrant while keeping it realistic."
- **Generar un fondo abstracto** cuando se necesita uno que no sea una foto. Prompt tipo: "Abstract minimalist background, deep cobalt blue with subtle gradient, high contrast, editorial design style."
- **Sacar un objeto molesto** de una foto existente (auto, cable, persona). Prompt tipo: "Remove the [object] from this image while keeping the rest exactly the same."
- **Extender una imagen** para encajarla en un formato vertical cuando la original es horizontal. Prompt tipo: "Extend this image vertically while maintaining the same style and lighting."

### No usar

- **NO generar propiedades que no existen.** Si el cliente pide una placa de una propiedad, la foto tiene que ser real. No inventar.
- **NO generar caras humanas.** Riesgo de parecer stock photo genérico y de caer en el valle inquietante.
- **NO generar logos.** El logo siempre viene del cliente.
- **NO generar texto dentro de la imagen.** Todo el texto se hace con HTML después.
- **NO generar "ambientes" genéricos para reemplazar propiedades reales.** Es engaño al lector.

## Checklist visual antes de aprobar una pieza

- [ ] ¿Hay jerarquía clara (un solo elemento dominante)?
- [ ] ¿El texto entra dentro del margen de seguridad?
- [ ] ¿Hay al menos un elemento con rotación sutil?
- [ ] ¿La paleta usa máximo 3 colores efectivos?
- [ ] ¿El tamaño de headline es de al menos 80px?
- [ ] ¿Los pesos tipográficos son 700 o más para headlines?
- [ ] ¿No hay ningún elemento prohibido (gradiente, sombra 3D, emoji, etc.)?
- [ ] ¿El logo aparece solo en el último slide (en carruseles)?
- [ ] ¿El número de slide está en la posición correcta?
- [ ] ¿Se lee el mensaje en 2 segundos o menos?

Si alguna respuesta es NO, ajustá antes de mostrar al usuario.
