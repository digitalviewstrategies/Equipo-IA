---
name: carrusel-captacion
description: Use this skill when the user asks for a captacion carrusel for any DV client — 6 slides 1080x1080 with the brand's narrative_structure (default DCSP if brand has none). Triggers "armame un carrusel de captacion para [cliente]", "carrusel para captar de [cliente]", "carrusel de captacion [cliente]", "carrusel feed [cliente] captacion".
---

# Skill: Carrusel de captacion

Pieza estrella del agente. 6 slides 1080x1080. La estructura narrativa, los frameworks de hook, la paleta y el tono **vienen del brand JSON del cliente**, no estan hardcoded en esta skill. Lo unico universal aca es la cantidad de slides, los formatos, los margenes y las reglas de QA visual.

## Antes de producir

Pedi si falta:
1. **Cliente** (debe existir `shared/brands/<cliente>.json`; si no, parar y derivar a skill `brand-system`).
2. **Tema o angulo** del carrusel (captacion de mandatos, captacion en zona X, etc.). Si es ambiguo, hace 1 sola pregunta.

## Pasos

1. **Cargar brand**. Leer `shared/brands/<cliente>.json` y aplicar el protocolo de `context/brand_loader.md`. Extraer:
   - `tone_of_voice.narrative_structure` → si existe, esa es la estructura del carrusel. Si no, usar default DV (DOLOR → CONSECUENCIA → SOLUCION → PRUEBA).
   - `tone_of_voice.hook_frameworks` → los hooks deben pertenecer a uno de esos frameworks. Si no existe, usar Hormozi (negacion / empatia / verdad incomoda).
   - `tone_of_voice.principles` → registro y voz (formal vs juvenil, etc.).
   - `tone_of_voice.forbidden_words` y `preferred_words` → restricciones de copy.
   - `colors` y `color_distribution_rules` → paleta y mapping de color por slide.
   - `typography` → tipografias del brand.
2. **Cargar contexto comun**: `context/copy_framework.md` (validacion final del copy), `context/design_principles.md` (reglas universales DV).
3. **Escribir copy primero**. 6 slides en bloque de texto. Aplicar la `narrative_structure` del brand a los 6 slides (mappear cada step a 1-2 slides segun longitud). Hook (slide 1) usa uno de los `hook_frameworks` del brand. Respetar `principles` y `forbidden_words`.
4. **Decidir color por slide** segun `color_distribution_rules` del brand. Si el brand no define mapping, usar default DV: slide 1 primary, slides 2-3 dark, slide 4 light, slide 5 primary, slide 6 dark. Acento secundario en max 2 de 6 slides.
5. **Pipeline**: si `mcp__claude_ai_Canva__list-brand-kits` tiene el cliente → Canva MCP. Si no → `templates/carrusel_captacion.html` + `scripts/render.py`. El template debe consumir el brand JSON via `scripts/brand.py` para que colores y tipografias salgan dinamicas.
6. **Renderizar** a `output/<cliente>/<YYYY-MM-DD>/carrusel_captacion/`.
7. **QA**: invocar skill `design-qa` antes de mostrar. Bloquear si hay BLOCK.
8. **Mostrar al usuario** los 6 PNGs en orden. No expliques cada slide.
9. **Iterar** segun feedback (un slide a la vez si el cambio es puntual).
10. **Subir a Drive solo con OK explicito**: `CLIENTE/03 Estaticos/Carruseles/`.

## Reglas universales DV (no negociables, hardcoded)

Estas valen para todo cliente, no se overriden por brand JSON:

- 6 slides, 1080x1080.
- Numeracion de slides intermedios (02/06...05/06). Slide 1 y 6 sin numero.
- Logo solo en slide final (slide 6).
- Margen seguro 80px en todos los lados.
- Headlines minimo 80px, numeros minimo 150px.
- Maximo 2 tipografias por pieza.
- Maximo 3 colores efectivos por slide (1 fondo + 1 texto + 1 acento).
- Sin emojis, sin gradientes multicolor, sin drop shadows >4px, sin tipografias prohibidas.
- Un mensaje por slide. Si no se entiende en 2 segundos, esta mal.
- Forbidden words globales DV (suma a las del brand): "suenos", "concretar", "tu hogar te espera", "profesionales de confianza", "calidad y confianza", "tradicion y experiencia", "acompanamiento personalizado".
- Voseo argentino siempre (jamas "tu", jamas "usted").
- NUNCA inventar datos. Si falta un dato citado en el carrusel, parar y pedir.

## Entrega

Mostra los 6 PNGs en orden y cerra con: "Carrusel de captacion para [cliente] listo en `output/...`. Decime si va o que cambiamos."
