---
name: caption
description: Use this skill when the user asks to produce an organic caption for feed or Reels, either for a DV client's immobiliaria account or for @digitalviewagency. Covers workflows C and E. Triggers "armame un caption", "copy para instagram", "caption para reel", "caption organico", "texto para post", "copy para feed", "pie de foto", "caption de autoridad", "post para [cliente]".
---

# Skill: Caption organico

Produces captions para redes del cliente (workflow C) o de @digitalviewagency (workflow E).

## Antes de producir

Pedi si falta:
1. **Cliente** (o `digital_view`).
2. **Objetivo**: `venta` | `captacion` | `autoridad` | `educativo`.
3. **Contexto visual** (que muestra el video o imagen). **Siempre** lo pedis antes de escribir. Sin contexto visual no escribis.

## Pasos

1. Carga brand del cliente desde `shared/brands/<cliente>.json`.
2. Lee `context/frameworks_copy.md` y `context/audiencias.md`.
3. Si el cliente tiene outputs recientes en `outputs/<cliente>/`, mira los ultimos 2-3 para no repetir angulos.
4. Hook para parar scroll. En organico la negacion funciona bien ademas de empatia y verdad incomoda.
5. Desarrollo 4-8 lineas, parrafos cortos (1-2 lineas max).
6. CTA suave. Nunca "link en bio" si no hay algo concreto en bio.
7. Para DV (workflow E): habla de resultados concretos, no de servicios. Nunca "hacemos contenido" - siempre "generamos operaciones". Si hay caso real con numeros, usalo.
8. Usa `templates/copy_caption_organico.md`.
9. Guarda el archivo con el tool Write en `outputs/<cliente>/<YYYY-MM-DD>/caption_<objetivo>_<fecha_corta>.md` (fecha de hoy en ISO).

## Reglas

- Palabras prohibidas: "suenos", "concretar", "profesionales de confianza", etc.
- Emojis: maximo 2 si el cliente los usa habitualmente. Default cero.
- Voseo argentino.
- Si es DV, tono de par a par con duenos de inmobiliaria. No vendedor.

## Entrega

Mostra el caption completo y confirma la ruta.
