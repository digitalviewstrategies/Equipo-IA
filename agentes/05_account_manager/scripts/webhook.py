"""FastAPI webhook entrypoint para Meta WhatsApp Cloud API."""
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Response
from . import config, client_resolver, intent_router, policy, approval_channel, wa_client, conversation_log
from .handlers import faq, status_produccion, performance, filmacion

app = FastAPI(title="DV Account Manager Webhook")


@app.get("/webhook")
async def verify(request: Request):
    """Verificacion inicial del webhook (Meta manda GET con hub.challenge)."""
    params = request.query_params
    if (params.get("hub.mode") == "subscribe"
            and params.get("hub.verify_token") == config.VERIFY_TOKEN):
        return Response(content=params.get("hub.challenge", ""), media_type="text/plain")
    raise HTTPException(status_code=403, detail="verify token mismatch")


@app.post("/webhook")
async def receive(request: Request):
    raw = await request.body()
    _verify_signature(raw, request.headers.get("x-hub-signature-256", ""))
    payload = await request.json()

    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for msg in value.get("messages", []) or []:
                _process_message(msg)

    return {"status": "ok"}


def _verify_signature(raw: bytes, header: str) -> None:
    if not config.APP_SECRET:
        return  # dev mode
    if not header.startswith("sha256="):
        raise HTTPException(status_code=403, detail="missing signature")
    expected = "sha256=" + hmac.new(
        config.APP_SECRET.encode(), raw, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, header):
        raise HTTPException(status_code=403, detail="bad signature")


def _process_message(msg: dict) -> None:
    if msg.get("type") != "text":
        return  # etapa 1 solo texto
    from_number = "+" + msg["from"]
    text = msg["text"]["body"]

    if from_number == config.FELIPE_WA_NUMBER:
        action = approval_channel.handle_felipe_reply(text)
        if action:
            _execute_approval(action, text)
        return

    resolved = client_resolver.resolve(from_number)
    cliente = resolved["cliente"]
    contact_name = resolved["contact_name"]
    brand = resolved["brand"]

    intent_data = intent_router.classify(text)
    intent = intent_data["intent"]
    confidence = intent_data["confidence"]
    entities = intent_data.get("entities", {})

    conversation_log.log(cliente, "in", from_number, text, intent, confidence)

    handler_result = _dispatch(intent, text, entities, brand, contact_name)
    borrador = handler_result["text"]
    handler_ok = handler_result["ok"]

    auto = policy.should_auto_reply(intent, confidence, cliente, handler_ok)

    if auto:
        wa_client.send_text(from_number, borrador)
        conversation_log.log(cliente, "out", from_number, borrador, intent, confidence, auto=True)
    else:
        approval_channel.send_for_approval(
            cliente or "DESCONOCIDO", contact_name or "", from_number,
            intent, confidence, text, borrador,
        )
        conversation_log.log(cliente, "draft", from_number, borrador, intent, confidence, auto=False)


def _dispatch(intent: str, text: str, entities: dict, brand: dict | None, contact_name: str | None) -> dict:
    if intent == "faq":
        return faq.handle(text, contact_name)
    if intent == "status_produccion":
        return status_produccion.handle(text, entities, brand, contact_name)
    if intent == "performance_campana":
        return performance.handle(text, entities, brand, contact_name)
    if intent == "coordinacion_filmacion":
        return filmacion.handle(text, entities, brand, contact_name)
    if intent == "escalamiento_humano":
        return {"text": "Te paso con Felipe ahora, en un rato te escribe.", "ok": True}
    return {"text": "Lo chequeo y te confirmo.", "ok": False}


def _execute_approval(action: dict, original: str) -> None:
    """Etapa 1: stub. La logica real necesita parsear el ID y recuperar el destino del pending file."""
    # TODO etapa 2: leer _pending_approvals.jsonl, marcar como resuelto, enviar al cliente original.
    pass
