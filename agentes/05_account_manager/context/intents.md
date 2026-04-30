# Intents

El router clasifica cada mensaje entrante en uno de estos intents. Definicion + ejemplos para el prompt de clasificacion (Haiku).

## `faq`

Pregunta operativa estandar respondible desde `faqs.md`.

Ejemplos:
- "que horario tienen?"
- "cuanto tarda la edicion?"
- "donde veo los videos?"
- "cuando me mandan el reporte?"

## `status_produccion`

Consulta sobre el estado de un video, edicion, estatico o produccion en curso.

Ejemplos:
- "che cuando sale el reel del depto de Belgrano?"
- "como va la edicion del recorrido?"
- "ya esta el carrusel?"
- "termino el video del jueves?"

Entities: `pieza` (reel, recorrido, carrusel, placa), `referencia` (depto Belgrano, recorrido VL, etc).

## `performance_campana`

Consulta sobre numeros de Meta Ads del cliente.

Ejemplos:
- "como van los anuncios?"
- "cuantos leads esta semana?"
- "como esta el CPL?"
- "cuanto gastamos hasta ahora?"

Entities: `periodo` (hoy, esta semana, este mes, ultimos 7 dias).

## `coordinacion_filmacion`

Consulta sobre fechas, horarios, locaciones de filmaciones programadas.

Ejemplos:
- "a que hora es la filmacion del jueves?"
- "donde es la grabacion?"
- "puedo cambiar el horario?"
- "viene Bauti a filmar?"

Entities: `fecha`, `locacion`.

## `escalamiento_humano`

El cliente pide hablar con una persona, esta enojado, plantea queja, urgencia o tema comercial.

Disparadores: "urgente", "queja", "reclamo", "cancelar", "hablar con Valentin", "hablar con alguien", "esto no puede ser".

→ Siempre escalamiento a Felipe inmediato, sin borrador automatico (le mando aviso a Felipe con el mensaje completo y un sugerido).

## `desconocido`

No matchea ninguno de los anteriores con confianza. → Borrador siempre.

---

## Salida del clasificador

```json
{
  "intent": "status_produccion",
  "confidence": 0.92,
  "entities": {"pieza": "reel", "referencia": "depto Belgrano"}
}
```

Si confidence < 0.7 → tratar como `desconocido`.
