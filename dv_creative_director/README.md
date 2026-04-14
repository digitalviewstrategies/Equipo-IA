# DV Creative Director

Agente de IA para ideación, estrategia y desarrollo de contenido de los clientes de Digital View.

## Qué hace

- Desarrolla guiones completos para producciones audiovisuales (video selfie, entrevista, b-roll, reels).
- Crea briefs de carrusel listos para pasarle al `dv_design_agent`.
- Genera estrategias de contenido mensual con calendario y ideas desarrolladas.
- Investiga el mercado y tendencias antes de proponer ideas.
- Comparte el contexto de clientes con el agente de diseño vía la carpeta `brands/` compartida.

## Instalación

### Requisitos

- Claude Code instalado y configurado.
- Python 3.10+.
- Acceso a internet (usa web search para research de mercado).
- `dv_design_agent` instalado en el mismo directorio padre (para compartir brand systems).

### Setup

```bash
# Clonar o copiar el directorio dv_creative_director
cd dv_creative_director

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus claves si usás APIs externas
```

### Estructura de directorios recomendada

```
digital_view_agents/
├── dv_design_agent/        # Agente de diseño (ya instalado)
│   └── brands/             # Brand systems compartidos
└── dv_creative_director/   # Este agente
    └── CLAUDE.md
```

Si los agentes están en directorios separados, el director creativo busca los brand systems en `../dv_design_agent/brands/`. Si tu estructura es distinta, actualizá la ruta en `CLAUDE.md`.

## Uso básico

Abrís Claude Code en el directorio `dv_creative_director/` y le hablás al agente directamente.

### Pedido mínimo

```
Cliente: [nombre]
Objetivo: [qué quiere lograr]
Formato: [video / carrusel / estrategia mensual / lo que veas mejor]
Cantidad: [cuántas piezas o ideas]
```

### Ejemplos reales

```
Cliente: Soldati Vista
Objetivo: captar mandatos en Palermo y Villa Crespo
Formato: guion para video selfie + carrusel
Cantidad: 1 de cada uno
```

```
Cliente: Matias Di Meola
Objetivo: construir marca personal como house flipper
Formato: estrategia mensual completa
Cantidad: 1 mes
```

```
Cliente: nuevo cliente sin brand system
Contexto: inmobiliaria familiar en Martínez, dos socias, ticket promedio USD 250k, quieren captar propietarios
Objetivo: arrancar con contenido de captación
Formato: lo que veas mejor
```

## Outputs

Todos los outputs se guardan en `outputs/[cliente]/[fecha]/`:

- `guion_[titulo].md` — guion completo con notas de producción.
- `brief_carrusel_[titulo].md` — brief listo para el agente de diseño.
- `estrategia_[mes].md` — estrategia mensual con calendario.
- `ideas_[objetivo].md` — las 3 ideas iniciales antes de desarrollar.

## Flujo con el agente de diseño

Cuando el director creativo produce un brief de carrusel, podés pasárselo directamente al agente de diseño:

```
# En dv_design_agent/
# Le pasás el brief generado por el director creativo
# El agente de diseño lee el brand system del mismo cliente y produce las piezas
```

## Notas

- El agente hace research de mercado antes de proponer ideas. Esto puede tomar 1-2 minutos extra pero mejora mucho la calidad de las ideas.
- Siempre propone 3 ideas antes de desarrollar. Elegís una y ahí profundiza.
- Los guiones incluyen siempre al menos dos variantes del hook para testear.
- El tono se calibra automáticamente según el brand system del cliente.
