# DV Creative Director (v2)

Agente de IA que funciona como Director Creativo de Digital View. Investiga, piensa y desarrolla ideas y guiones de contenido para los clientes de DV usando el **Sistema de Producción de Video Ads** (13 formatos ganadores basados en Hormozi $100M Leads + Meta Best Practices 2025 + Facu Winer).

Produce tres tipos de output:

1. **Guiones de video** para producciones audiovisuales (Bauti CB + editores).
2. **Briefs de carrusel** listos para el agente de diseño (`agentes/01_contenido/design/`).
3. **Estrategias de contenido mensuales** con pilares, mix y calendario.

Comparte el contexto de clientes con el agente de diseño leyendo los brand systems desde `shared/brands/` (directorio compartido en la raíz del repo).

## Qué cambió respecto a v1

- **Sistema de video ads completo**: el framework anterior (DCSP/HPTC/HTRM) fue reemplazado por los 13 formatos ganadores del documento de Nico, con estructuras, guiones fórmula, banco de hooks y métricas por formato.
- **Paso obligatorio nuevo**: antes de proponer ideas, el agente genera mínimo 5 ángulos de dolor distintos desde el buyer persona del cliente, usando las 6 familias de ángulos (económico, oportunidad perdida, social/vergüenza, miedo/pérdida futura, ira/traición, cansancio/proceso). Ver `context/angulos_de_dolor.md`.
- **Research de tendencias en TikTok e Instagram**: nuevo bloque en el research previo a la ideación, con declaración explícita de las limitaciones de WebSearch (no entra a TikTok Creative Center ni al feed en vivo, sí lee blogs de Later/Hootsuite/Social Insider/Tom Orbach/etc. con 1-3 semanas de rezago).
- **Decisión manufacturado vs documentado**, **What-Who-When** y **paleta de emociones** son ahora pasos explícitos del proceso, no background.
- **Template de guion** alineado al Brief de Producción del sistema, con validación de ratio valor:tiempo y checklist de set.

## Instalación

Este agente vive dentro del monorepo `Equipo-IA` en `agentes/01_contenido/creative_director/`. Comparte `shared/brands/` con el agente de diseño:

```
Equipo-IA/
├── shared/
│   └── brands/
│       ├── digital_view.json
│       ├── matias_di_meola.json
│       └── ...
└── agentes/
    └── 01_contenido/
        ├── creative_director/      ← este agente
        └── design/
```

Abrí Claude Code en `agentes/01_contenido/creative_director/`. El agente lee `CLAUDE.md` automáticamente al arrancar.

No necesita dependencias externas: el research lo hace con la herramienta WebSearch nativa de Claude Code.

## Uso

Pedido mínimo para ideación completa:

```
Cliente: matias_di_meola
Objetivo: posicionar marca personal en Vicente López
Formato: a definir
Cantidad: 3 ideas para reels este mes
```

El agente:
1. Carga el brand system del cliente.
2. Construye el Core (objetivo, buyer persona, servicio, dolor, What-Who-When).
3. **Genera 5+ ángulos de dolor** desde el buyer persona.
4. Hace research de mercado + research de tendencias TikTok/IG.
5. Propone 3 ideas en ángulos distintos, con formato del sistema, estilo, emoción y hook tentativo.
6. Vos elegís una.
7. Desarrolla el output completo y lo guarda en `outputs/[cliente]/[fecha]/`.

Si el pedido viene cerrado y no necesita ideación, decilo y va directo al desarrollo:

```
Cliente: soldati_vista
Hacé el guion del video del depto de 2 amb en Núñez.
Formato: Antes/Después tipo 2 (métricas).
Datos: USD 145.000, 48m2, balcón, cochera, vendido en 22 días.
```

## Estructura

```
agentes/01_contenido/creative_director/
├── CLAUDE.md                              # Cerebro del agente (proceso de 8 pasos)
├── README.md                              # Esto
├── .gitignore / .env.example
├── context/
│   ├── sistema_video_ads.md               # Índice
│   ├── sistema_video_ads_parte1.md        # Core del cliente
│   ├── sistema_video_ads_parte2.md        # Formatos 1-7
│   ├── sistema_video_ads_parte3.md        # Formatos 8-13
│   ├── sistema_video_ads_parte4.md        # Hooks, títulos, brief, testing, producción
│   ├── angulos_de_dolor.md                # Cómo generar 5+ ángulos (NUEVO)
│   └── ejemplos_output.md                 # Casos reales de referencia
│   (mercado/vocabulario: ver shared/contexto_inmobiliario.md)
├── scripts/
│   ├── template_guion.md                  # Brief de producción v2
│   ├── output_manager.py                  # Cargar brands + guardar outputs
│   └── market_research.py                 # Research de mercado + tendencias sociales
├── examples/
└── outputs/                               # Auto-creado por cliente y fecha
```

## El proceso de 8 pasos del agente

1. Entender el pedido (preguntar solo si falta info crítica).
2. Cargar brand system del cliente.
3. Construir el Core (5 elementos).
4. **Generar 5+ ángulos de dolor** (paso obligatorio).
5. Research (mercado + tendencias sociales).
6. Proponer 3 ideas en ángulos distintos.
7. Desarrollar el output completo (guion / brief / estrategia).
8. Guardar y cerrar indicando a quién va dentro del equipo.

## Integración con el resto del equipo

- **Guiones de video** → Bauti CB (producción) y editores (Gian Luca, Fran, Eze).
- **Briefs de carrusel** → agente de diseño (`agentes/01_contenido/design/`) directamente.
- **Estrategias mensuales** → Elias o Bauti R (PMs).
- **Brainstorm libre** → Nico (COO, Director de Contenido).

## Modelo

Sonnet 4.6 por default. Opus 4.6 para estrategia mensual completa, cliente nuevo sin norte creativo, o ideación de campaña grande con múltiples formatos combinados.
