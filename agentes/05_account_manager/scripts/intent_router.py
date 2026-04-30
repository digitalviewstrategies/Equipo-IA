"""Clasifica mensajes entrantes en intents usando Claude Haiku."""
import json
from anthropic import Anthropic
from . import config

INTENTS = [
    "faq",
    "status_produccion",
    "performance_campana",
    "coordinacion_filmacion",
    "escalamiento_humano",
    "desconocido",
]

ESCALAMIENTO_KEYWORDS = [
    "urgente", "queja", "reclamo", "cancelar", "cancelacion",
    "molesto", "enojado", "hablar con valentin", "hablar con alguien",
    "esto no puede ser", "no puede ser",
]

SYSTEM = """Sos un clasificador de intents para un bot de WhatsApp de Digital View (DV), agencia de marketing inmobiliario.

Clasifica el mensaje entrante en uno de estos intents:
- faq: pregunta operativa estandar (horarios, proceso, donde estan los videos, cuando llega el reporte)
- status_produccion: consulta sobre estado de un video, edicion, estatico (cuando sale, ya esta?, como va)
- performance_campana: consulta sobre numeros de Meta Ads (leads, CPL, gasto, como van los anuncios)
- coordinacion_filmacion: consulta sobre fecha/hora/lugar de filmacion programada
- escalamiento_humano: el cliente pide hablar con alguien, esta enojado, plantea queja, urgencia o tema comercial
- desconocido: no matchea ninguno con confianza

Devolve SOLO JSON valido, sin texto previo ni posterior:
{"intent": "<uno de la lista>", "confidence": <0.0-1.0>, "entities": {<key>: <value>}}

confidence < 0.7 si no estas seguro."""


def classify(text: str) -> dict:
    """Devuelve {intent, confidence, entities}. Aplica override por keywords primero."""
    lower = text.lower()
    for kw in ESCALAMIENTO_KEYWORDS:
        if kw in lower:
            return {"intent": "escalamiento_humano", "confidence": 0.99, "entities": {"trigger": kw}}

    if not config.ANTHROPIC_API_KEY:
        return {"intent": "desconocido", "confidence": 0.0, "entities": {}}

    client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
    msg = client.messages.create(
        model=config.INTENT_MODEL,
        max_tokens=200,
        system=SYSTEM,
        messages=[{"role": "user", "content": text}],
    )
    raw = msg.content[0].text.strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"intent": "desconocido", "confidence": 0.0, "entities": {"raw": raw}}

    if data.get("intent") not in INTENTS:
        data["intent"] = "desconocido"
    if data.get("confidence", 0) < 0.7:
        data["intent"] = "desconocido"
    return data
