"""
market_research.py — Guía estructurada de research para el agente.

Este NO es un script ejecutable que hace requests. Es una guía de prompts
y queries que el agente sigue cuando usa la herramienta WebSearch nativa
de Claude Code antes de proponer ideas.

Dos tipos de research, siempre en orden:
    1. Research de mercado (según tipo de cliente)
    2. Research de tendencias TikTok + Instagram

El agente lee este archivo, identifica el tipo de cliente, y ejecuta los
queries sugeridos con WebSearch. Los resultados se sintetizan en 3-5
bullets antes de la ideación.
"""

# =============================================================================
# PARTE 1: RESEARCH DE MERCADO POR TIPO DE CLIENTE
# =============================================================================

RESEARCH_INMOBILIARIA_TRADICIONAL = """
Para inmobiliarias tradicionales (8-30 años, equipo de 3-15, oficina física):

Queries sugeridos (ejecutar con WebSearch):

1. Mercado de la zona del cliente:
   - "precio metro cuadrado [ZONA] 2026"
   - "tiempo promedio venta departamento [ZONA]"
   - "stock inmobiliario [ZONA] tendencia"

2. Competencia local:
   - "inmobiliarias [ZONA] instagram"
   - "inmobiliarias top [ZONA] reseñas"

3. Tendencias del rubro:
   - "captacion mandatos inmobiliaria argentina 2026"
   - "comision inmobiliaria caba ley actual"

4. Datos duros para hooks:
   - "porcentaje propietarios venden por inmobiliaria argentina"
   - "tiempo promedio operacion inmobiliaria caba"

Lo que el agente busca:
- Un dato duro de la zona que se pueda usar como hook de verdad incómoda.
- Tendencia de precios para anclar el discurso.
- Qué está haciendo la competencia local en redes (para hacer lo opuesto).
- Cualquier cambio regulatorio reciente que afecte al cliente.
"""


RESEARCH_TOP_PRODUCER = """
Para top producers (broker individual de alto rendimiento, 35-50 años):

Queries sugeridos:

1. Mercado en su nicho:
   - "departamentos premium [ZONA] 2026"
   - "inversores propiedades [ZONA] tendencia"
   - "compradores extranjeros [ZONA] inmobiliario"

2. Tendencias de marca personal:
   - "marca personal broker inmobiliario argentina"
   - "top producer real estate personal branding"

3. Datos duros para autoridad:
   - "ranking inmobiliario argentina 2026"
   - "diferencia comision operacion compartida vs directa"

4. Casos de referencia:
   - "top producer inmobiliario instagram argentina"

Lo que el agente busca:
- Datos del mercado premium del nicho del top producer.
- Insights sobre marca personal aplicables a su perfil.
- Un dato comparativo que muestre el costo de no tener marca personal.
- Referencias de cómo otros top producers están comunicando.
"""


RESEARCH_DESARROLLADOR = """
Para desarrolladores (de pozo o emprendimientos terminados):

Queries sugeridos:

1. Mercado de pozo / inversión:
   - "inversion pozo [ZONA] 2026 rentabilidad"
   - "valor metro cuadrado pozo vs terminado argentina"
   - "credito hipotecario argentina 2026"

2. Tendencias de demanda:
   - "demanda emprendimientos [ZONA]"
   - "perfil inversor inmobiliario argentina 2026"

3. Datos duros:
   - "rentabilidad alquiler temporario vs tradicional caba"
   - "evolucion precio metro cuadrado [ZONA] ultimos 5 anos"

4. Competencia:
   - "emprendimientos en pozo [ZONA] activos"

Lo que el agente busca:
- Datos macro que justifiquen la inversión en el momento actual.
- Tendencias de demanda en la zona específica del proyecto.
- Comparativos de rentabilidad.
- Qué emprendimientos compiten directo con el del cliente.
"""


RESEARCH_HOUSE_FLIPPER = """
Para house flippers (compra, refacciona, revende):

Queries sugeridos:

1. Mercado de compra (oportunidades):
   - "departamentos venta urgente [ZONA]"
   - "tiempo promedio venta caba 2026"
   - "rebajas precio departamentos [ZONA]"

2. Costos de obra:
   - "costo refaccion departamento argentina 2026"
   - "precio mano de obra construccion buenos aires"

3. Tendencias de comprador:
   - "departamentos llave en mano demanda caba"
   - "preferencias compradores jovenes departamento argentina"

4. Datos para hooks:
   - "porcentaje propietarios venden con apuro argentina"
   - "diferencia precio publicado vs precio venta inmobiliario"

Lo que el agente busca:
- Datos sobre el spread entre precio publicado y precio cerrado.
- Tendencias de costo de obra (afecta el margen del flip).
- Qué busca hoy el comprador joven en un depto refaccionado.
- Datos para hooks tipo "te están dejando plata sobre la mesa".
"""


RESEARCH_POR_TIPO = {
    "inmobiliaria_tradicional": RESEARCH_INMOBILIARIA_TRADICIONAL,
    "top_producer": RESEARCH_TOP_PRODUCER,
    "desarrollador": RESEARCH_DESARROLLADOR,
    "house_flipper": RESEARCH_HOUSE_FLIPPER,
}


def get_research_guide(tipo_cliente: str) -> str:
    """
    Devuelve la guía de research para un tipo de cliente.
    Tipos válidos: inmobiliaria_tradicional, top_producer, desarrollador,
    house_flipper.
    """
    return RESEARCH_POR_TIPO.get(
        tipo_cliente,
        "Tipo de cliente no reconocido. Usá criterio general: investigá zona, "
        "competencia, tendencias del rubro y un dato duro para el hook."
    )


# =============================================================================
# PARTE 2: RESEARCH DE TENDENCIAS TIKTOK + INSTAGRAM
# =============================================================================

RESEARCH_TENDENCIAS_SOCIAL = """
Research de tendencias TikTok + Instagram.

## Limitación importante (leer antes de empezar)

WebSearch nativo de Claude Code NO puede:
- Entrar a TikTok Creative Center directamente.
- Scrapear el feed "Para ti" ni el explorador de Instagram Reels.
- Ver en vivo qué está performando en las últimas 24-48 horas.

WebSearch SÍ puede:
- Leer blogs y newsletters que analizan tendencias con 1-3 semanas de rezago.
- Encontrar artículos de Later, Hootsuite, Social Insider, Exploding Topics,
  Hubspot, Metricool, Sprout Social.
- Leer posts de creadores que analizan lo que funciona (ej: Tom Orbach
  Marketing Ideas, posts de IG/LinkedIn de gente como Alex Lieberman,
  Jack Appleby, etc.).
- Encontrar análisis de formatos virales publicados en Medium, blogs
  personales, newsletters.

En la práctica: el agente se entera de tendencias con 1-3 semanas de
rezago, que es lo suficientemente fresco para contenido de marca
(que igual tarda 1-2 semanas en producirse y publicarse).

Si el research no devuelve nada útil, el agente avisa y sigue con
formatos consolidados del sistema. NUNCA inventa una tendencia ni
la presenta como "de la última semana" sin fuente citable.

## Queries sugeridos (3-5 máximo por sesión)

### Tendencias generales de formatos
- "instagram reels trends 2026"
- "tiktok trends marketing 2026"
- "viral video formats social media 2026"
- "reels hooks that work 2026"

### Tendencias específicas para el rubro (ajustar según tipo de cliente)
- "real estate instagram reels ideas 2026"
- "real estate tiktok viral 2026"
- "real estate video ads format trending"
- "house flipping instagram content ideas"

### Tendencias de hooks
- "best instagram reels hooks 2026"
- "viral tiktok hook formulas"

### Tendencias de audio (solo si el formato lo requiere)
- "trending audio instagram reels" (cuidado: casi imposible de verificar
  sin acceso directo, mejor decir "audio tendencia actual" sin nombrar
  específico)

### Fuentes que suelen tener info buena (usar site: si hace falta)
- later.com blog
- hootsuite.com blog
- socialinsider.io
- explodingtopics.com/blog
- hubspot.com/marketing/social-media
- metricool.com/blog
- sproutsocial.com/insights
- tomorbach.com / newsletter Marketing Ideas
- medium.com (posts de creadores)

## Cómo usar los resultados

Después de 2-4 queries, el agente escribe 2-3 bullets sintéticos:

- "Formato X está funcionando para [razón], fuente: [blog]."
- "Hook Y está replicándose en el rubro, visto en [2-3 casos]."
- "Tendencia de [sonido/efecto/estilo] mencionada en [fuente]."

Si solo encuentra cosas genéricas o viejas, escribe:
"No encontré tendencias verificables recientes específicas para este
caso. Me voy con formatos consolidados del sistema."

## Reglas estrictas

1. NO inventes una tendencia. Si no la podés citar, no existe para el
   agente.
2. NO digas "últimos 7 días" si la fuente es de hace 3 semanas. Decí
   "últimas semanas".
3. NO uses tendencias como excusa para copiar. Las tendencias son
   insumo para adaptar, no plantilla para replicar. El criterio del
   sistema siempre manda.
4. Si una tendencia contradice el tono del cliente (ej: un formato
   humorístico para un cliente nivel 2 de disrupción), la ignorás.
"""


# =============================================================================
# PARTE 3: REGLAS GENERALES DE RESEARCH
# =============================================================================

REGLAS_RESEARCH = """
Reglas generales de research (aplicar siempre):

1. Hacé research ANTES de proponer ideas. No después. Las ideas sin
   research son opiniones disfrazadas.

2. Cantidad total: MÁXIMO 6-8 queries por sesión (3-5 de mercado + 2-4
   de tendencias). Más es procrastinación.

3. Si encontrás un dato duro que vas a usar como hook, anotá la fuente.
   Si después no podés citar la fuente, no usás el dato.

4. Si los resultados son vagos o contradictorios, NO inventes el dato.
   Cambiá el ángulo del hook hacia algo que sí podés sostener.

5. Mirá qué está haciendo la competencia directa del cliente en redes.
   Si hay un patrón obvio (todas hacen tours de propiedad), proponé el
   opuesto.

6. Datos que sirven para hooks: porcentajes, tiempos promedio,
   comparativos, tendencias claras. Datos que NO sirven: opiniones de
   "expertos", proyecciones muy a futuro, datos sin fuente verificable.

7. Si el cliente pide algo muy puntual (un guion para un depto
   específico), el research se reduce a buscar datos de ESA zona y ESE
   tipo de propiedad, no del rubro entero.

8. Para tendencias sociales: declará la limitación temporal. Si
   encontraste algo de hace 2 semanas, decí "hace 2 semanas", no
   "esta semana".
"""


if __name__ == "__main__":
    print("Tipos de cliente disponibles:")
    for tipo in RESEARCH_POR_TIPO:
        print(f"  - {tipo}")
    print("\n--- Reglas generales ---")
    print(REGLAS_RESEARCH)
    print("\n--- Tendencias sociales ---")
    print(RESEARCH_TENDENCIAS_SOCIAL[:500] + "...")
