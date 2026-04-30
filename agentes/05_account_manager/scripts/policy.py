"""Decide auto-respuesta vs borrador a Felipe."""

AUTO_INTENTS = {"faq", "status_produccion"}
NEVER_AUTO = {"escalamiento_humano", "desconocido", "performance_campana", "coordinacion_filmacion"}


def should_auto_reply(intent: str, confidence: float, cliente: str | None, handler_ok: bool) -> bool:
    """
    handler_ok: el handler pudo generar respuesta concreta y verificada (e.g., card encontrada).
    """
    if cliente is None:
        return False
    if intent in NEVER_AUTO:
        return False
    if intent not in AUTO_INTENTS:
        return False
    if confidence < 0.85:
        return False
    return handler_ok
