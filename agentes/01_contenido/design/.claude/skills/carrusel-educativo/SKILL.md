---
name: carrusel-educativo
description: Use this skill when the user asks for an educational/authority carrusel for any DV client — 6-8 slides 1080x1080 with HOOK-PROBLEMA-TIPS-CIERRE structure. Tone, paleta, hooks y narrativa vienen del brand JSON. Triggers "armame un carrusel educativo para [cliente]", "carrusel de tips de [cliente]", "carrusel de autoridad para [cliente]", "carrusel educativo [cliente] sobre [tema]".
---

# Skill: Carrusel educativo / autoridad

6-8 slides cuadrados que posicionan al cliente como experto. Estructura macro **HOOK → PROBLEMA → 3-4 TIPS → CIERRE** (universal a este formato), pero el tono, los frameworks de hook, la paleta y el copy salen del brand JSON.

## Antes de producir

Pedi si falta:
1. **Cliente** (con `shared/brands/<cliente>.json` existente).
2. **Tema** del carrusel (ej: "como elegir tasador", "errores al vender depto").
3. **Cantidad de tips/pasos** si tiene preferencia (default 3).

## Pasos

1. **Cargar brand**. Aplicar protocolo de `context/brand_loader.md`. Extraer:
   - `tone_of_voice.principles` → registro educativo segun el brand (puede ser cercano-juvenil o formal-corporate, depende del cliente).
   - `tone_of_voice.hook_frameworks` → el hook del slide 1 debe pertenecer a uno de esos frameworks.
   - `tone_of_voice.forbidden_words` y `preferred_words`.
   - `colors`, `color_distribution_rules`, `typography`.
2. **Cargar contexto comun**: `context/copy_framework.md`, `context/design_principles.md`.
3. **Escribir copy primero**:
   - Slide 1 (hook): puede ser pregunta directa, lista contundente o dato — dentro de los `hook_frameworks` del brand.
   - Slide 2 (problema): nombrar el problema concreto que los tips resuelven.
   - Slides 3 a N (tips numerados): 1 idea por slide, concreta y aterrizada. Si decis "ojo con la documentacion", el slide siguiente lo resuelve.
   - Slide final (cierre): sintesis + CTA suave alineado al brand.
4. **Color por slide**: aplicar `color_distribution_rules` del brand. Si no existe, default DV: hook en color primario, tips alternando off-white y dark, cierre en color de marca.
5. **Pipeline**: Canva MCP si hay brand kit; si no, `templates/carrusel_educativo.html` + `scripts/render.py` (template consume brand JSON via `scripts/brand.py`).
6. **Renderizar** a `output/<cliente>/<YYYY-MM-DD>/carrusel_educativo/`.
7. **Numeracion**: slides intermedios numerados (02/08...07/08). Hook (01) y cierre (final) sin numero. Logo solo en cierre.
8. **QA**: invocar skill `design-qa`.
9. Mostrar al usuario.
10. Iterar.
11. Subir a Drive con OK: `CLIENTE/03 Estaticos/Carruseles/`.

## Reglas universales DV (no negociables, hardcoded)

- 6-8 slides, 1080x1080.
- Numeracion en slides intermedios. Logo solo en cierre.
- Margen seguro 80px.
- Headlines minimo 80px, numeros minimo 150px.
- Maximo 2 tipografias, maximo 3 colores efectivos por slide.
- Sin emojis, sin gradientes, sin drop shadows >4px.
- NUNCA pregunta retorica vacia tipo "¿sabias que vender es dificil?". El hook abre con sustancia (dato, declaracion, lista).
- Tips concretos. Cero generalidades.
- Forbidden words globales DV (suma a las del brand).
- Voseo argentino.
- NUNCA inventar datos.

## Entrega

Mostra los slides en orden. Cierra: "Carrusel educativo de [tema] para [cliente] en `output/...`. Decime si va."
