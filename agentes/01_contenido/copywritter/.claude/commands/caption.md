---
description: Produce caption organico para feed o Reels (cliente o DV)
argument-hint: [cliente] [objetivo]
---

# Skill: Caption organico

Produces captions para redes del cliente (workflow C) o de @digitalviewagency (workflow E).

## Inputs

Argumentos: `$1=cliente`, `$2=objetivo`.

Objetivo puede ser: `venta` | `captacion` | `autoridad` | `educativo`.

**Siempre** preguntas el contexto visual (que muestra el video o imagen) antes de escribir. Si no hay contexto visual, no escribis.

## Pasos

1. Carga brand del cliente desde `shared/brands/<cliente>.json`. Si es DV, usa `digital_view.json`.
2. Lee `context/frameworks_copy.md` y `context/audiencias.md`.
3. Si el cliente tiene outputs recientes en `outputs/<cliente>/`, mira los ultimos 2-3 para no repetir angulos.
4. Hook para parar scroll. En organico la negacion funciona bien ademas de empatia y verdad incomoda.
5. Desarrollo 4-8 lineas, parrafos cortos (1-2 lineas max).
6. CTA suave. Nunca "link en bio" si no hay algo concreto en bio.
7. Para DV (workflow E): habla de resultados concretos, no de servicios. Nunca "hacemos contenido" — siempre "generamos operaciones". Si hay caso real con numeros, usalo.
8. Usa `templates/copy_caption_organico.md`.
9. Guarda:
   ```bash
   python scripts/output_manager.py save <cliente> caption <objetivo>_<fecha_corta>
   ```

## Reglas

- Palabras prohibidas (mismas que Meta Ads): "suenos", "concretar", "profesionales de confianza", etc.
- Emojis: maximo 2 si el cliente los usa habitualmente en su brand. Default cero.
- Voseo argentino.
- Si es DV, tono de par a par con duenos de inmobiliaria. No vendedor.

## Entrega

Mostra el caption completo y confirma la ruta donde lo guardaste.
