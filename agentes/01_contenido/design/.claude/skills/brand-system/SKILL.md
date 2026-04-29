---
name: brand-system
description: Use this skill when a new client needs a visual brand system created — analyzes logo + Instagram screenshots, proposes 3 systems ordered by disruption level, and saves the chosen one as JSON. Triggers "armame el brand system de [cliente]", "onboardear visualmente a [cliente]", "nuevo cliente: [nombre]", "nuevo brand system para [cliente]", "no existe el JSON de [cliente]".
---

# Skill: Onboarding de brand system para cliente nuevo

Cuando llega un cliente nuevo y no existe `shared/brands/<cliente>.json`. Analizas logo + referencias del Instagram del cliente y proponés 3 sistemas visuales (conservador, balanceado, disruptivo). Guardas el elegido como JSON + assets.

**Maximo 3 intervenciones del usuario** en todo el flujo: input inicial, eleccion de sistema, aprobacion de slide de muestra.

## Antes de empezar

Pedi en UN SOLO mensaje (todo junto, no en partes):
1. **Nombre del cliente** (brand_id en snake_case).
2. **Contexto breve** (que hace, donde, que vende, target).
3. **Logo** (path o adjunto).
4. **4-6 screenshots** del Instagram del cliente (o aviso de "no tiene Instagram").
5. **Restricciones de franquicia o casa matriz** si aplica.

Si falta algo critico (logo o contexto), parar y pedir solo eso.

## Pasos

1. Analiza en silencio: el logo con `view`, cada screenshot con `view`, cruzas con el contexto. NO hagas preguntas genericas tipo "¿que tono querés?". Deducilo.
2. Genera 3 propuestas ordenadas por disrupcion:
   - **A — Conservador**: paleta sobria, tipografia neutra, layouts clasicos. Para clientes tradicionales o franquicias.
   - **B — Balanceado**: paleta con un acento, tipografias mixtas, layouts con personalidad pero no extremos. Default para la mayoria.
   - **C — Disruptivo**: paleta contrastada, tipografias bold, layouts con quiebre. Para clientes jovenes que quieren romper.
   Marca cual recomendas y por que en una linea.
3. Cada propuesta lleva: 3-5 colores HEX literales, 1-2 tipografias (Google Fonts), tono de comunicacion (1 linea), regla de uso del color secundario.
4. **NUNCA uses los colores exactos de DV** (#0033CC, #C8FF00, #FF0080) para otro cliente.
5. Esperas la eleccion. Si el usuario pide hibridos, los aceptas pero no proponés un cuarto sistema completo nuevo.
6. Una vez elegido, generas UN slide de muestra (slide 1 estilo carrusel de captacion del sistema elegido) con `scripts/render.py`. Mostralo.
7. Si aprueba: guardas `shared/brands/<brand_id>.json` con la estructura estandar (colores, tipografias, tono, reglas) y copias el logo a `shared/brands/assets/<brand_id>/logo.png` (o el formato que vino).
8. Si pide ajustes en el slide: ajustas y volves a renderizar. No volves al paso de 3 propuestas.

## Estructura del JSON

```json
{
  "brand_id": "...",
  "nombre": "...",
  "contexto": "...",
  "colores": { "primario": "#...", "secundario": "#...", "fondo": "#...", "texto": "#..." },
  "tipografias": { "headline": "...", "body": "..." },
  "tono": "...",
  "reglas": ["...", "..."]
}
```

## Reglas no negociables

- 3 intervenciones del usuario maximo.
- Si no hay Instagram: trabajas con logo + contexto y avisas "sin referencias de IG, basado solo en logo".
- Tipografias solo de Google Fonts.
- Colores siempre HEX (no nombres, no hsl).

## Entrega

Cerras: "Brand system de [cliente] guardado en `shared/brands/<brand_id>.json`. Listo para producir piezas. Si queres arrancar con un carrusel de captacion, decime."
