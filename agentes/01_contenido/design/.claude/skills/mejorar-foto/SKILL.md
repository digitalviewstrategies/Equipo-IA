---
name: mejorar-foto
description: Use this skill to improve property photos or generate backgrounds using Nano Banana (Gemini 2.5 Flash Image). Use cases: improve light/color of cellphone photos, remove unwanted objects, change time of day, generate abstract backgrounds. Triggers "mejora esta foto", "limpiar el fondo de [foto]", "sacar [objeto] de la foto", "mejorar la foto de [propiedad]", "generame un fondo abstracto", "llevar esta foto a calidad profesional".
---

# Skill: Mejorar foto con Nano Banana (Gemini 2.5 Flash Image)

Wrapper sobre `scripts/generate_image.py`. Usa Gemini 2.5 Flash Image para mejorar fotos de propiedad o generar fondos. Requiere `GOOGLE_API_KEY` en `.env`.

## Cuando usar

- Mejorar luz/color de fotos de celular (cliente manda baja calidad).
- Sacar objetos molestos del fondo (autos, cables, gente).
- Cambiar hora del dia o angulo de luz.
- Generar fondos abstractos cuando no hay foto de propiedad.

## Cuando NO usar

- NO generar propiedades que no existen.
- NO inventar caras de personas reales.
- NO generar logos de clientes.
- NO generar texto dentro de la imagen (el texto siempre va en HTML, nunca embebido en pixeles).

## Antes de producir

Pedi si falta:
1. **Foto base** (path local o url) — salvo que sea generacion de fondo desde cero.
2. **Que mejorar puntualmente** — "luz mas calida", "sacar el auto del frente", "fondo limpio sin cables", "atardecer". No aceptes "mejorala" generico sin un eje.

## Pasos

1. Identifica la operacion: mejora puntual / cambio de luz / remocion de objeto / generacion de fondo.
2. Construi el prompt para Gemini en ingles, descriptivo y especifico. Ejemplos:
   - Mejora luz: "professional real estate photo of the same room, balanced exposure, warm natural light, no people, no clutter".
   - Remocion: "same property exterior, remove the parked car in the foreground, keep all architecture exact".
   - Fondo: "abstract minimal background, soft gradient of [hex colors del brand], no figures, no text".
3. Llama `scripts/generate_image.py` con el prompt y la imagen base si aplica.
4. Compara output vs original. Validar:
   - Que NO haya inventado partes de la propiedad que no existen (ventanas extra, paredes nuevas).
   - Que NO haya cambiado el numero de piso, la disposicion estructural o detalles arquitectonicos.
   - Que la luz sea creible.
5. Si el output altera la propiedad real, descartalo y reintenta con prompt mas restrictivo ("preserve all architectural details exactly").
6. Guarda en `output/<cliente>/<YYYY-MM-DD>/fotos/<nombre>_mejorada.png`. Conserva el original tambien.
7. Mostra al usuario antes/despues lado a lado.

## Reglas no negociables

- Fidelidad arquitectonica: la propiedad post-mejora debe ser la misma propiedad. Cambios de luz si, cambios estructurales no.
- Si el usuario duda de la fidelidad, descartar y usar la foto original.
- Sin texto generado por IA en la imagen.

## Entrega

"Foto mejorada de [propiedad/cliente] en `output/.../fotos/`. Original conservado al lado. Decime si va o probamos otro angulo."
