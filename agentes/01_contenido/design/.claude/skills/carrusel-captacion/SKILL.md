---
name: carrusel-captacion
description: Use this skill when the user asks for a captacion carrusel for a DV client — 6 slides 1080x1080 with the DOLOR-CONSECUENCIA-SOLUCION-PRUEBA framework. Triggers "armame un carrusel de captacion para [cliente]", "carrusel para captar de [cliente]", "carrusel de captacion [cliente]", "carrusel feed [cliente] captacion".
---

# Skill: Carrusel de captacion

Pieza estrella del metodo DV. 6 slides 1080x1080 estructurados DOLOR -> CONSECUENCIA -> SOLUCION -> PRUEBA, mas hook inicial y CTA final.

## Antes de producir

Pedi si falta:
1. **Cliente** (debe existir `shared/brands/<cliente>.json`; si no, parar y avisar que hay que onboardear con la skill `brand-system`).
2. **Tema o angulo** (captacion de mandatos, dolor del propietario, etc.). Si es ambiguo, hace 1 sola pregunta.

## Pasos

1. Carga el brand: leer `shared/brands/<cliente>.json` (colores HEX, tipografias, reglas).
2. Carga reglas: leer `context/copy_framework.md` y `context/design_principles.md`.
3. Escribi el copy primero — 6 slides en bloque de texto. Hook con una de las 3 estructuras Hormozi (negacion / empatia / verdad incomoda). Tono argentino juvenil, voseo, sin clichés.
4. Decidi color por slide: azules (apertura + prueba), negros (dolor/consecuencia/CTA), off-white (solucion). Acento secundario en max 2 de 6 slides.
5. Pipeline: si `mcp__claude_ai_Canva__list-brand-kits` tiene el cliente -> Canva MCP. Si no -> `templates/carrusel_captacion.html` + `scripts/render.py`.
6. Renderiza a `output/<cliente>/<YYYY-MM-DD>/carrusel_captacion/`.
7. Revisa cada PNG: legibilidad, contraste, numeracion (02/06...05/06, sin numero en 01 y 06), logo solo en slide final.
8. Mostra al usuario en chat. No expliques cada slide.
9. Iterar segun feedback (un slide a la vez si el cambio es puntual).
10. Subir a Drive solo con OK explicito: `CLIENTE/03 Estaticos/Carruseles/`.

## Reglas no negociables

- Nunca emojis, nunca gradientes, nunca drop shadows 3D, nunca tipografias serif decorativas.
- Headlines minimo 80px, numeros minimo 300px.
- Un mensaje por slide. Si no se entiende en 2 segundos, esta mal.
- Lista negra de copy: "suenos", "concretar", "profesionales de confianza", "tu hogar te espera".
- Voseo argentino siempre.

## Entrega

Mostra los 6 PNGs en orden y cerra con: "Carrusel de captacion para [cliente] listo en `output/...`. Decime si va o que cambiamos."
