# DV Design Agent

Agente de diseño autónomo para Digital View y sus clientes. Produce carruseles, creativos para Meta Ads, flyers y placas de propiedad con calidad profesional, siguiendo el sistema de marca de cada cliente y el método DV.

Construido para correr en Claude Code.

## Qué hace

Cuando le das un pedido en lenguaje natural:

- "Hacé un carrusel de captación para Digital View sobre el problema de las operaciones compartidas."
- "Placa para López Props: dpto 3 amb en Belgrano, USD 185.000, 85m², 2 dorm, 1 baño, con cochera."
- "Creativo Meta cuadrado y vertical para la campaña de captación de RE/MAX sobre rotación de propiedades."
- "Nuevo cliente: Estudio Alvarez, logo acá adjunto."

El agente lee el brand system del cliente, aplica el framework de copy, escribe el contenido, renderiza las piezas, te las muestra en chat para aprobar, y cuando le das OK sube todo al Drive del cliente en la carpeta correcta.

## Instalación en 5 pasos

### 1. Clonar o descargar el directorio

Ponelo en la ubicación que prefieras. Por ejemplo:

```bash
cd ~/Documents
# Si descargás el ZIP, descomprimí acá
# Si usás git, clonalo acá
```

### 2. Instalar dependencias de Python

Desde dentro del directorio `dv_design_agent/`:

```bash
cd dv_design_agent
pip install playwright pillow google-genai python-dotenv
playwright install chromium
```

La instalación de Playwright tarda 1-2 minutos la primera vez porque baja Chromium. Es de una sola vez.

### 3. Obtener la API key de Google Gemini (gratis)

1. Andá a https://aistudio.google.com/app/apikey
2. Iniciá sesión con tu cuenta de Google.
3. Clickeá "Create API Key".
4. Copiá la key.

El uso hasta cierto volumen es gratis. Para el uso interno de DV va a sobrar con el tier gratuito.

### 4. Configurar el archivo .env

Copiá `.env.example` a `.env` y pegá tu API key:

```bash
cp .env.example .env
```

Después editá `.env` con cualquier editor de texto y reemplazá `tu_key_aca` con la key que copiaste.

### 5. Abrir en Claude Code

Desde la terminal, estando dentro del directorio del agente:

```bash
cd dv_design_agent
claude
```

Claude Code va a leer automáticamente el archivo `CLAUDE.md` que contiene todas las instrucciones del agente. En ese momento ya podés pedirle cosas.

## Primer uso: tu primer carrusel en 30 segundos

Una vez dentro de Claude Code, probá:

```
Hacé un carrusel de captación para Digital View con el tema de dependencia del boca en boca.
```

El agente va a:

1. Leer `brands/digital_view.json` para el sistema de marca.
2. Leer `context/copy_framework.md` para el tono.
3. Escribir el copy completo de los 6 slides siguiendo Método DV.
4. Cargar la plantilla `templates/carrusel_captacion.html`.
5. Reemplazar el contenido.
6. Renderizar los 6 PNGs con Playwright.
7. Mostrártelos en el chat.
8. Esperar tu OK para subirlos a Drive (o guardarlos local si Drive MCP no está activo).

## Comandos típicos

```
Hacé un carrusel de captación para [cliente] sobre [tema].

Placa de propiedad para [cliente]: [datos].

Creativo Meta cuadrado y vertical para [cliente] sobre [tema].

Carrusel educativo para [cliente] sobre [tema].

Flyer para la propiedad [descripción] de [cliente].

Nuevo cliente: [nombre]. [adjuntar logo]

Cambiá el slide [N] del último carrusel.

Subilo al Drive.
```

## Estructura del proyecto

```
dv_design_agent/
├── CLAUDE.md                    # Instrucciones maestras (el "cerebro" del agente)
├── README.md                    # Este archivo
├── .env.example                 # Template de variables de entorno
├── .gitignore
│
├── context/                     # Lo que el agente sabe siempre
│   ├── dv_manual.md             # Contexto de Digital View
│   ├── copy_framework.md        # Tono, hooks, estructura narrativa
│   ├── design_principles.md     # Reglas visuales inamovibles
│   └── inmobiliario_glosario.md # Vocabulario del rubro
│
├── brands/                      # Un archivo por cliente
│   ├── digital_view.json        # Brand system de DV
│   ├── _template.json           # Para crear nuevos
│   └── _onboarding.md           # Cómo onboardear clientes
│
├── templates/                   # HTML base por tipo de pieza
│   ├── carrusel_captacion.html
│   ├── carrusel_educativo.html
│   ├── creativo_meta.html
│   ├── creativo_meta_vertical.html
│   ├── placa_propiedad.html
│   └── flyer_propiedad.html
│
├── scripts/
│   ├── render.py                # HTML → PNG con Playwright
│   ├── generate.py              # Orquestador principal
│   ├── brand.py                 # Cargar brand systems
│   ├── generate_image.py        # Wrapper de Nano Banana
│   └── upload_drive.py          # Helper para mapear carpetas
│
├── examples/                    # Referencias visuales
│   └── dv_carrusel_referencia/  # Los 6 slides aprobados
│
└── output/                      # Piezas generadas (auto-creado)
    └── [cliente]/[fecha]/[tipo]/
```

## Cómo el agente sabe qué hacer

Cuando abrís Claude Code en este directorio, el archivo `CLAUDE.md` de la raíz se carga automáticamente como contexto. Ese archivo le dice al agente:

- Quién es (agente de diseño de DV).
- Qué puede hacer (los 5 tipos de pieza).
- Cómo debe hacerlo (flujo de 10 pasos).
- Qué no puede hacer (generar imágenes con texto, inventar datos, subir sin aprobación).
- Cómo onboardear clientes nuevos.
- Cómo usar Nano Banana.
- Cómo integrarse con Drive MCP.

Cada vez que el agente trabaja en una pieza, sigue ese flujo sin que se lo repitas.

## Configurar Google Drive MCP (opcional pero recomendado)

Cuando estés listo para que el agente suba directo al Drive de cada cliente:

1. Desde Claude Code ejecutá `/mcp` y seleccioná Google Drive.
2. Autorizá con tu cuenta.
3. Verificá que las carpetas de cada cliente existan con la estructura estándar (el agente las crea si no existen).

Mientras Drive MCP no esté configurado, el agente guarda todo en `output/[cliente]/[fecha]/` y te dice dónde están los archivos. Vos los subís a mano las primeras veces hasta que actives el MCP.

## Onboarding de un cliente nuevo

Cuando agregues un cliente nuevo:

```
Nuevo cliente: Estudio Alvarez
```

Adjuntá el logo en la misma conversación. El agente va a:

1. Analizar el logo (colores dominantes, estilo tipográfico).
2. Hacerte 3 preguntas (tono, audiencia, referencia visual).
3. Proponer 3 sistemas de marca distintos.
4. Renderizar un slide de muestra del sistema elegido.
5. Cuando aprobás, guardar el sistema en `brands/estudio_alvarez.json`.

A partir de ese momento cualquier pedido para Estudio Alvarez usa automáticamente ese sistema.

## Modificar el brand system de un cliente

Si querés ajustar los colores, tipografías o reglas visuales de un cliente existente, abrí el JSON en `brands/` y editalo directamente. La próxima pieza que genere el agente ya va a usar los cambios.

No hace falta reiniciar nada.

## Limitaciones conocidas

- **IA generativa para imágenes finales:** el agente no genera carruseles enteros con IA generativa. Usa HTML/CSS para todo el texto y IA solo para fotos, fondos e ilustraciones. Esto es una decisión de calidad, no una limitación técnica.
- **Tipografías:** el agente usa tipografías de Google Fonts. No soporta fuentes custom sin configurarlas previamente.
- **Aprobación humana:** el agente nunca sube a Drive sin confirmación explícita. Esto es por diseño, para evitar publicar material sin revisar.
- **Sonnet vs Opus:** por default corre en Sonnet 4.6. Para onboardings de clientes nuevos o briefs muy ambiguos conviene cambiar a Opus 4.6 manualmente.

## Troubleshooting

**"Playwright no encuentra Chromium"**
Ejecutá `playwright install chromium` dentro del directorio.

**"Falta GOOGLE_API_KEY"**
Revisá que tengas el archivo `.env` con la key. No uses comillas alrededor del valor.

**"No existe brand system para [cliente]"**
El agente te lo va a decir. Pedile "nuevo cliente [nombre]" y te va a guiar en el onboarding.

**"Los slides salen sin las tipografías correctas"**
El script de render espera 2 segundos por las fuentes de Google. Si tu conexión es lenta, podés aumentar el timeout en `scripts/render.py` línea `await page.wait_for_timeout(2000)`.

**"El carrusel se ve distinto al ejemplo aprobado"**
Mirá los archivos en `examples/dv_carrusel_referencia/` para comparar. Si hay diferencias visuales, probablemente cambiaste algo en el template o en el brand system sin querer.

## Créditos

Sistema de marca de Digital View desarrollado en colaboración con Valentin Hechter.
Framework de copy basado en el Método DV (DOLOR → CONSECUENCIA → SOLUCIÓN → PRUEBA) y en estructuras de hook tipo Hormozi.
