"""Redactor de borradores con Sonnet 4.6 en tono WA Felipe.

El handler devuelve un draft "base" (`raw`). draft_writer.compose() lo pasa por
Sonnet para que salga en tono natural, voseo, sin emojis, frases cortas. Cae al
texto raw si no hay ANTHROPIC_API_KEY o si el LLM falla — fail-open, nunca bloquea.
"""
from __future__ import annotations

from anthropic import Anthropic

from . import config

_TONO_CACHE: str | None = None


def _load_tono() -> str:
    global _TONO_CACHE
    if _TONO_CACHE is None:
        tono_file = config.CONTEXT_DIR / "tono_whatsapp.md"
        _TONO_CACHE = tono_file.read_text(encoding="utf-8") if tono_file.exists() else ""
    return _TONO_CACHE


_SYSTEM = """Sos el asistente de cuentas WhatsApp de Digital View (DV), agencia de marketing inmobiliario.

Te paso:
- El mensaje del cliente
- Un borrador "base" generado por el sistema
- Datos extra (numeros, nombres, fechas) si los hay

Tu tarea: reescribir el borrador en tono natural WA Felipe DV, manteniendo TODA la informacion factica del borrador base. No inventes datos. No agregues numeros, fechas o nombres que no esten en el borrador o en los datos extra.

REGLAS DURAS (no negociables):
- Voseo argentino siempre.
- CERO emojis.
- 1 a 3 frases, cortas.
- Sin cliches inmobiliarios ("hogar sonado", "concretar tu sueno", "te acompanamos en cada paso").
- Sin anglicismos: ASAP -> lo antes posible / feedback -> comentarios / update -> novedad.
- Sin urgencia falsa.
- Cerrar con apertura concreta ("cualquier cosa me decis", "te confirmo cuando este").

Si el borrador base ya esta perfecto, devolvelo igual.
Devolve SOLO el texto final del mensaje, sin comillas, sin prefijo, sin explicacion."""


def compose(
    cliente_msg: str,
    raw_draft: str,
    intent: str,
    contact_name: str | None = None,
    extra: dict | None = None,
) -> str:
    """Devuelve el borrador final. Fail-open al raw_draft si LLM no esta disponible."""
    if not config.ANTHROPIC_API_KEY:
        return raw_draft

    tono = _load_tono()
    parts = [
        f"Mensaje del cliente: {cliente_msg!r}",
        f"Intent detectado: {intent}",
        f"Contact name: {contact_name or '(desconocido)'}",
        f"Borrador base a refinar:\n{raw_draft}",
    ]
    if extra:
        parts.append(f"Datos factuales disponibles (no inventes nada fuera de aca):\n{extra}")
    if tono:
        parts.append(f"Guia de tono completa:\n{tono}")
    user = "\n\n".join(parts)

    try:
        client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        resp = client.messages.create(
            model=config.DRAFT_MODEL,
            max_tokens=400,
            system=_SYSTEM,
            messages=[{"role": "user", "content": user}],
        )
        return resp.content[0].text.strip()
    except Exception:
        return raw_draft
