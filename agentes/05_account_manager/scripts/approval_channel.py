"""Manda borradores a Felipe por WA y procesa su respuesta (OK / EDITAR / DESCARTAR).

Flow:
1. send_for_approval() -> guarda entry pending y manda mensaje a Felipe con ID al final.
2. Felipe responde OK / EDITAR <texto> / DESCARTAR (opcionalmente con el ID).
3. handle_felipe_reply() parsea la accion.
4. resolve() recupera el pending, manda al cliente original y marca como resuelto.
"""
import json
import re
from datetime import datetime
from . import config, wa_client

PENDING_FILE = config.OUTPUTS_DIR / "_pending_approvals.jsonl"


def send_for_approval(cliente: str, contact_name: str, from_number: str,
                       intent: str, confidence: float,
                       pregunta: str, borrador: str) -> str:
    approval_id = f"{from_number.lstrip('+')}_{int(datetime.utcnow().timestamp())}"
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


_ID_RE = re.compile(r"\b(\d{8,}_\d{10})\b")


def handle_felipe_reply(text: str) -> dict | None:
    """Devuelve {action, [text], [id]} o None si el mensaje no es comando."""
    t = text.strip()
    upper = t.upper()
    id_match = _ID_RE.search(t)
    approval_id = id_match.group(1) if id_match else None

    if upper.startswith("OK"):
        return {"action": "send_as_is", "id": approval_id}
    if upper.startswith("EDITAR "):
        custom = t[7:].strip()
        # Si el ID estaba pegado al final, sacarlo del texto custom.
        if approval_id:
            custom = custom.replace(approval_id, "").strip()
        return {"action": "send_custom", "text": custom, "id": approval_id}
    if upper.startswith("DESCARTAR"):
        return {"action": "discard", "id": approval_id}
    return None


def _read_pending() -> list[dict]:
    if not PENDING_FILE.exists():
        return []
    out = []
    for line in PENDING_FILE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _write_pending(entries: list[dict]) -> None:
    with PENDING_FILE.open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def _find_target(entries: list[dict], approval_id: str | None) -> dict | None:
    """Si hay ID, busca por ID; si no, devuelve el ultimo pending."""
    pendings = [e for e in entries if e.get("status") == "pending"]
    if approval_id:
        for e in pendings:
            if e["id"] == approval_id:
                return e
        return None
    return pendings[-1] if pendings else None


def resolve(action: dict) -> dict:
    """Ejecuta la accion de Felipe: manda al cliente y marca pending como resuelto.
    Devuelve {ok, sent_to, text} o {ok: False, reason}.
    """
    entries = _read_pending()
    target = _find_target(entries, action.get("id"))
    if target is None:
        return {"ok": False, "reason": "no pending matching"}

    if action["action"] == "discard":
        target["status"] = "discarded"
        _write_pending(entries)
        return {"ok": True, "sent_to": None, "text": None}

    text_to_send = target["borrador"] if action["action"] == "send_as_is" else action.get("text", "").strip()
    if not text_to_send:
        return {"ok": False, "reason": "empty text"}

    if config.WABA_TOKEN:
        wa_client.send_text(target["from"], text_to_send)

    target["status"] = "sent"
    target["resolved_ts"] = datetime.utcnow().isoformat()
    target["sent_text"] = text_to_send
    _write_pending(entries)
    return {"ok": True, "sent_to": target["from"], "text": text_to_send, "cliente": target["cliente"]}
