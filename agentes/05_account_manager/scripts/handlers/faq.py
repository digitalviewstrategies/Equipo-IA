"""Handler FAQ: matchea pregunta contra context/faqs.md via Claude."""
from anthropic import Anthropic
from .. import config

SYSTEM = """Sos un asistente de WhatsApp de Digital View (DV).

Recibis una pregunta de un cliente y un knowledge base de FAQs. Si la pregunta matchea claramente alguna FAQ, devolve la respuesta tal cual esta escrita ahi (respeta el tono: voseo, sin emojis, corto).

Si no matchea con confianza, devolve EXACTAMENTE: NULL

Reglas:
- Personaliza con el nombre del contacto cuando sea natural.
- No inventes datos que no estan en el FAQ.
- Maximo 3 frases."""


def handle(text: str, contact_name: str | None) -> dict:
    """Devuelve {text, ok}. ok=True si encontro respuesta concreta."""
    if not config.ANTHROPIC_API_KEY:
        return {"text": "Lo chequeo y te confirmo.", "ok": False}

    faqs = (config.CONTEXT_DIR / "faqs.md").read_text(encoding="utf-8")
    client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
    prompt = f"FAQs:\n{faqs}\n\nContacto: {contact_name or 'sin nombre'}\nPregunta: {text}"
    msg = client.messages.create(
        model=config.DRAFT_MODEL,
        max_tokens=400,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    answer = msg.content[0].text.strip()
    if answer == "NULL" or not answer:
        return {"text": "Lo chequeo y te confirmo.", "ok": False}
    return {"text": answer, "ok": True}
