"""Manda borradores a Felipe por WA y procesa su respuesta (OK / EDITAR / DESCARTAR)."""
import json
from datetime import datetime
from . import config, wa_client

PENDING_FILE = config.OUTPUTS_DIR / "_pending_approvals.jsonl"


def send_for_approval(cliente: str, contact_name: str, from_number: str,
                       intent: str, confidence: float,
                       pregunta: str, borrador: str) -> str:
    """Manda borrador a Felipe. Devuelve approval_id."""
    approval_id = f"{from_number}_{int(datetime.utcnow().timestamp())}"
    template = (config.TEMPLATES_DIR / "borrador_aprobacion.md").read_text(encoding="utf-8")
    body = (template
            .replace("{{cliente}}", cliente or "DESCONOCIDO")
            .replace("{{contact_name}}", contact_name or "")
            .replace("{{from}}", from_number)
            .replace("{{intent}}", intent)
            .replace("{{confidence}}", f"{confidence:.2f}")
            .replace("{{pregunta}}", pregunta)
            .replace("{{borrador}}", borrador))
    body += f"\n\nID: {approval_id}"

    if config.FELIPE_WA_NUMBER and config.WABA_TOKEN:
        wa_client.send_text(config.FELIPE_WA_NUMBER, body)

    PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PENDING_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "id": approval_id,
            "ts": datetime.utcnow().isoformat(),
            "cliente": cliente,
            "from": from_number,
            "intent": intent,
            "pregunta": pregunta,
            "borrador": borrador,
            "status": "pending",
        }) + "\n")
    return approval_id


def handle_felipe_reply(text: str) -> dict | None:
    """Procesa respuesta de Felipe: OK / EDITAR <texto> / DESCARTAR. Devuelve accion."""
    t = text.strip()
    upper = t.upper()
    if upper.startswith("OK"):
        return {"action": "send_as_is"}
    if upper.startswith("EDITAR "):
        return {"action": "send_custom", "text": t[7:].strip()}
    if upper.startswith("DESCARTAR"):
        return {"action": "discard"}
    return None
