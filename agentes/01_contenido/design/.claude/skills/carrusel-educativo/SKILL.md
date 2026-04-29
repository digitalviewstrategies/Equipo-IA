---
name: carrusel-educativo
description: Use this skill when the user asks for an educational/authority carrusel for a DV client — 6-8 slides 1080x1080 with HOOK-PROBLEMA-TIPS-CIERRE structure. Tone less aggressive than captacion. Triggers "armame un carrusel educativo para [cliente]", "carrusel de tips de [cliente]", "carrusel de autoridad para [cliente]", "carrusel educativo [cliente] sobre [tema]".
---

# Skill: Carrusel educativo / autoridad

6-8 slides cuadrados que posicionan al cliente como experto del rubro. Estructura HOOK -> PROBLEMA -> 3-4 TIPS O PASOS -> CIERRE. Mas informativo, menos agresivo en copy, sin perder el tono DV.

## Antes de producir

Pedi si falta:
1. **Cliente** (con `shared/brands/<cliente>.json` existente).
2. **Tema** del carrusel (ej: "como elegir tasador", "errores al vender depto", "que mirar antes de firmar reserva").
3. **Cantidad de tips/pasos** si tiene preferencia (default 3).

## Pasos

1. Carga brand y reglas (`shared/brands/<cliente>.json`, `context/copy_framework.md`, `context/design_principles.md`).
2. Escribi copy primero. Estructura: slide 1 hook, slide 2 problema, slides 3-N tips numerados (1 idea por slide), slide final cierre + CTA suave.
3. Tono: educativo pero argentino. Voseo, frases cortas. No suena a manual corporativo, suena a un experto explicando rapido.
4. Color por slide: hook en color primario, tips en off-white o negro alternando, cierre en color de marca.
5. Pipeline: Canva MCP si hay brand kit; si no, `templates/carrusel_educativo.html` + `scripts/render.py`.
6. Renderiza a `output/<cliente>/<YYYY-MM-DD>/carrusel_educativo/`.
7. Numeracion: slides intermedios numerados (02/08...07/08). Hook (01) y cierre (final) sin numero. Logo solo en cierre.
8. Mostra al usuario.
9. Iterar.
10. Subir a Drive con OK: `CLIENTE/03 Estaticos/Carruseles/`.

## Reglas no negociables

- A diferencia de captacion: el hook puede ser pregunta directa o lista (ej: "3 cosas que nadie te dice antes de vender"). Pero NUNCA pregunta retorica vacia tipo "¿sabias que vender es dificil?".
- Tips concretos. Sin generalidades. Si decis "ojo con la documentacion", el slide siguiente lo aterriza.
- Sin emojis, sin clichés inmobiliarios, sin gradientes.

## Entrega

Mostra los slides en orden. Cierra: "Carrusel educativo de [tema] para [cliente] en `output/...`. Decime si va."
