"""
market_research.py
Hace research de mercado antes de desarrollar ideas de contenido.
El director creativo llama esto antes de proponer ideas para un cliente.
"""

import json
import os
import urllib.request
import urllib.parse


def research_tendencias_contenido(nicho: str, zona: str = "Argentina") -> str:
    """
    Investiga qué tipo de contenido está funcionando en el rubro inmobiliario.
    
    Args:
        nicho: tipo de cliente (inmobiliaria, top_producer, desarrollador, house_flipper)
        zona: contexto geográfico
    
    Returns:
        Resumen del research como string markdown
    """
    # Esta función es un wrapper para que Claude Code pueda hacer web search
    # El agente la usa como guía de qué buscar, no como llamada directa a API
    
    queries = {
        "inmobiliaria": [
            f"tendencias contenido redes sociales inmobiliarias {zona} 2025",
            f"marketing digital inmobiliario {zona} casos de éxito",
            f"instagram inmobiliaria argentina viral 2025",
        ],
        "top_producer": [
            f"marca personal broker inmobiliario {zona} 2025",
            f"contenido broker inmobiliario instagram argentina",
            f"top producer inmobiliario argentina redes sociales",
        ],
        "desarrollador": [
            f"marketing pozo desarrolladora inmobiliaria argentina 2025",
            f"contenido redes sociales proyecto inmobiliario argentina",
            f"leads inversores inmobiliarios argentina digital",
        ],
        "house_flipper": [
            f"house flipping argentina contenido redes 2025",
            f"inversión inmobiliaria argentina youtube instagram",
            f"flipping casas argentina comunidad",
        ],
    }
    
    selected_queries = queries.get(nicho, queries["inmobiliaria"])
    
    research_prompt = f"""
## Research de mercado — {nicho} en {zona}

Antes de desarrollar ideas, investigá estos temas específicamente:

### Qué buscar
{chr(10).join(f"- {q}" for q in selected_queries)}

### Qué necesito saber
1. ¿Qué tipo de contenido está generando más engagement en cuentas del rubro ahora mismo?
2. ¿Qué ángulos o temas están sobreexplotados (para evitarlos)?
3. ¿Hay algún formato emergente que no esté saturado todavía?
4. ¿Qué está haciendo el top 3 de cuentas del rubro en Argentina?

### Output esperado
Un resumen de máximo 300 palabras con los insights más útiles para desarrollar contenido diferencial.
"""
    
    return research_prompt


def research_competencia(cliente_nombre: str, zona: str, handle_ig: str = None) -> str:
    """
    Investiga la competencia directa de un cliente específico.
    """
    
    queries = [
        f"inmobiliaria {zona} instagram mejores cuentas",
        f"broker inmobiliario {zona} redes sociales contenido",
    ]
    
    if handle_ig:
        queries.append(f"@{handle_ig} instagram estrategia contenido")
    
    research_prompt = f"""
## Research de competencia — {cliente_nombre} ({zona})

### Qué buscar
{chr(10).join(f"- {q}" for q in queries)}

### Qué necesito saber
1. ¿Qué está haciendo la competencia directa en redes en esta zona?
2. ¿Qué gaps o espacios están desocupados que el cliente puede ocupar?
3. ¿Qué formatos o temas están saturados en esta zona específica?

### Output esperado
3-5 bullets con los insights más accionables para diferenciarse.
"""
    
    return research_prompt


def research_tendencias_mercado_inmobiliario() -> str:
    """
    Investiga el contexto del mercado inmobiliario actual en Argentina.
    Útil para contenido de análisis de mercado y educación.
    """
    
    research_prompt = """
## Research de mercado inmobiliario — Contexto actual Argentina

### Qué buscar
- "mercado inmobiliario Argentina 2025 precios tendencias"
- "compraventa propiedades CABA 2025 estadísticas"
- "dólar propiedades Argentina actualidad"
- "alquileres CABA 2025"

### Qué necesito saber
1. ¿Qué está pasando con los precios ahora mismo?
2. ¿Hay alguna noticia o cambio reciente que la audiencia esté procesando?
3. ¿Qué preguntas se está haciendo la gente sobre el mercado ahora?

### Output esperado
Bullets concretos con datos y contexto que se puedan usar en contenido educativo.
El dato más reciente disponible con su fuente.
"""
    
    return research_prompt


if __name__ == "__main__":
    # Test básico
    print(research_tendencias_contenido("top_producer", "Buenos Aires"))
    print("\n" + "="*50 + "\n")
    print(research_competencia("Soldati Vista", "CABA"))
