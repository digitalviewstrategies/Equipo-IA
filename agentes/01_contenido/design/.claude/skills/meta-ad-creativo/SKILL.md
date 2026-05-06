---
name: meta-ad-creativo
description: Use this skill when the user asks for a static Meta Ads creative — produces both square 1080x1080 (feed) and vertical 1080x1920 (stories/reels) versions. This is the visual piece, NOT the copy (copy is owned by the copywriter agent). Triggers "creativo de meta ads para [cliente]", "ad estatico para [cliente]", "armame el creativo para pauta", "creativo meta cuadrado y vertical", "estatico de pauta para [cliente]".
---

# Skill: Creativo estatico para Meta Ads

Genera DOS versiones por pedido: cuadrado 1080x1080 (feed) y vertical 1080x1920 (stories/reels). Es scroll-stopper: 1-2 elementos de texto, 1 imagen o color solido de fondo, 1 CTA. Mas simple que un carrusel.

Distinto de la skill `meta-ad` del agente copywriter — esa produce copy, esta produce el visual.

## Antes de producir

Pedi si falta:
1. **Cliente**.
2. **Copy** (hook + CTA). Si el usuario no lo paso, preguntale si lo pidio al copywriter o si vos tenes que improvisar uno corto. Mejor que venga del copywriter.
3. **Angulo o tema** (venta, captacion de propietarios, captacion de inmobiliarias para DV).
4. **Recurso visual**: foto de propiedad / foto manufactured / color solido. Si no hay, default color solido del brand.

## Pasos

1. **Cargar brand** segun protocolo `context/brand_loader.md`. Extraer paleta, tipografias, hook_frameworks (si vas a improvisar copy).
2. Si hay foto base y necesita mejora, invoca skill `mejorar-foto`.
3. Layout cuadrado: hook arriba grande, recurso visual al medio, CTA abajo o sobre el recurso. Maximo 2 bloques de texto. Margenes seguros porque Meta corta bordes en algunas placements.
4. Layout vertical: hook arriba (zona segura: primer cuarto), recurso visual al medio, CTA en zona segura inferior (no en los ultimos 250px porque tapan el boton de Meta).
5. Pipeline: Canva MCP si hay brand kit y placements simples; HTML + `scripts/render.py` si necesitas control fino.
6. Renderiza ambas versiones en paralelo a `output/<cliente>/<YYYY-MM-DD>/meta_ad_creativo/`. Naming: `creativo_<tema>_cuadrado.png` y `creativo_<tema>_vertical.png`.
7. Revisa: hook se entiende sin sonido, CTA visible en thumbnail, contraste alto.
8. Mostra ambas versiones al usuario.
9. Iterar.
10. Subir a Drive con OK: `CLIENTE/04 Campanas Meta/Creativos/` (no a 03 Estaticos — los creativos de pauta van con la campana).

## Reglas no negociables

- Hook minimo 100px en cuadrado, 120px en vertical (legible en mobile).
- Sin emojis, sin gradientes, sin drop shadow 3D.
- Zona segura vertical: no poner texto critico en los ultimos 250px ni en los primeros 250px.
- Si el copy fue producido por el copywriter, no lo modifiques sin avisar.

## Entrega

Mostra las 2 versiones lado a lado si es posible. Cierra: "Creativos de pauta para [cliente] (cuadrado + vertical) en `output/...`. Listos para subir a Meta cuando aprueben."
