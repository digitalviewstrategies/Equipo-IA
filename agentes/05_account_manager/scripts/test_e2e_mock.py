"""Test E2E mockeado del account_manager — sin Meta API, sin Anthropic.

Mockea wa_client.send_text e intent_router.classify para validar el flow:
  webhook._process_message -> resolver -> router -> handler -> policy -> wa_client / approval_channel

Corrida:
  cd agentes/05_account_manager && python -m scripts.test_e2e_mock

Salida: PASS/FAIL por escenario + resumen final.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from . import config, conversation_log, approval_channel, wa_client, intent_router, webhook

# ---- Sandbox dirs (no toca shared/brands ni outputs reales) ---------------
_TMP = Path(tempfile.mkdtemp(prefix="dv_am_test_"))
TEST_BRANDS = _TMP / "brands"
TEST_OUTPUTS = _TMP / "outputs"
TEST_BRANDS.mkdir()
TEST_OUTPUTS.mkdir()

config.BRANDS_DIR = TEST_BRANDS
config.OUTPUTS_DIR = TEST_OUTPUTS
config.FELIPE_WA_NUMBER = "+5491155551234"
config.WABA_TOKEN = "TEST_TOKEN"  # truthy para que approval_channel intente mandar
config.APP_SECRET = ""  # bypass signature en _verify_signature

# Brand de prueba: cliente_test con dos contactos
(TEST_BRANDS / "cliente_test.json").write_text(json.dumps({
    "brand_id": "cliente_test",
    "brand_name": "Cliente Test",
    "whatsapp": {
        "contacts": ["+5491166667777"],
        "primary_contact_name": "Juan Test",
        "trello_board_id": None,
    },
    "meta_ads": {"ad_account_id": "act_TEST"},
}, ensure_ascii=False), encoding="utf-8")

# Pending file vive en config.OUTPUTS_DIR; approval_channel ya lo recompone.
approval_channel.PENDING_FILE = config.OUTPUTS_DIR / "_pending_approvals.jsonl"

# ---- Mocks ----------------------------------------------------------------
SENT: list[tuple[str, str]] = []  # (to, body)


def _mock_send(to: str, body: str) -> dict:
    SENT.append((to, body))
    return {"ok": True, "to": to}


wa_client.send_text = _mock_send
# webhook + approval_channel importaron wa_client como modulo, pero llaman wa_client.send_text — el reemplazo del atributo del modulo basta.

# Mock classifier: deterministico por keyword del texto
def _mock_classify(text: str) -> dict:
    t = text.lower()
    # keyword escalamiento se procesa ANTES del classifier en el router real,
    # asi que aca no lo replicamos — viene como fallback.
    if "video" in t or "reel" in t or "edicion" in t:
        return {"intent": "status_produccion", "confidence": 0.92, "entities": {"pieza": "reel"}}
    if "horario" in t or "donde" in t or "como funciona" in t:
        return {"intent": "faq", "confidence": 0.95, "entities": {}}
    if "cpl" in t or "leads" in t or "campana" in t:
        return {"intent": "performance_campana", "confidence": 0.9, "entities": {"periodo": "ultimos 7 dias"}}
    if "filmar" in t or "filmacion" in t:
        return {"intent": "coordinacion_filmacion", "confidence": 0.88, "entities": {"fecha": "manana"}}
    return {"intent": "desconocido", "confidence": 0.3, "entities": {}}


intent_router.classify = _mock_classify
# webhook lo importo "from . import intent_router" -> el lookup runtime usa el modulo, OK.

# Mock FAQ handler para evitar leer faqs.md y llamar a Claude
from .handlers import faq as _faq_mod  # noqa: E402

_faq_mod.handle = lambda text, contact_name: {"text": "Los videos estan en la carpeta de Drive del mes.", "ok": True}

# ---- Test harness ---------------------------------------------------------
RESULTS: list[tuple[str, bool, str]] = []


def _reset():
    SENT.clear()
    if approval_channel.PENDING_FILE.exists():
        approval_channel.PENDING_FILE.unlink()


def _case(name: str, fn):
    try:
        fn()
        RESULTS.append((name, True, ""))
        print(f"  PASS  {name}")
    except AssertionError as e:
        RESULTS.append((name, False, str(e)))
        print(f"  FAIL  {name} — {e}")
    except Exception as e:
        RESULTS.append((name, False, f"{type(e).__name__}: {e}"))
        print(f"  ERROR {name} — {type(e).__name__}: {e}")


# ---- Escenarios -----------------------------------------------------------
def test_faq_auto():
    _reset()
    webhook._process_message({"type": "text", "from": "5491166667777", "text": {"body": "que horarios tienen"}})
    assert len(SENT) == 1, f"esperaba 1 envio, hubo {len(SENT)}"
    to, body = SENT[0]
    assert to == "+5491166667777", f"deberia mandar al cliente, mando a {to}"
    assert "Drive" in body, "deberia incluir la respuesta FAQ"
    assert not approval_channel.PENDING_FILE.exists(), "FAQ auto no deberia crear pending"


def test_status_borrador():
    _reset()
    webhook._process_message({"type": "text", "from": "5491166667777", "text": {"body": "como va el reel de la propiedad"}})
    # Status sin trello_board_id -> handler_ok=False -> borrador
    assert len(SENT) == 1
    to, body = SENT[0]
    assert to == config.FELIPE_WA_NUMBER, f"deberia ir a Felipe, fue a {to}"
    assert "Borrador" in body or "borrador" in body.lower()
    assert approval_channel.PENDING_FILE.exists()
    pendings = [json.loads(l) for l in approval_channel.PENDING_FILE.read_text(encoding="utf-8").splitlines() if l]
    assert len(pendings) == 1
    assert pendings[0]["status"] == "pending"


def test_escalamiento_keyword():
    _reset()
    webhook._process_message({"type": "text", "from": "5491166667777", "text": {"body": "esto es urgente, necesito hablar"}})
    assert len(SENT) == 1
    to, _ = SENT[0]
    assert to == config.FELIPE_WA_NUMBER


def test_cliente_desconocido_va_a_borrador():
    _reset()
    webhook._process_message({"type": "text", "from": "5491199999999", "text": {"body": "donde estan los videos"}})
    assert len(SENT) == 1
    to, body = SENT[0]
    assert to == config.FELIPE_WA_NUMBER
    assert "DESCONOCIDO" in body


def test_felipe_ok_resuelve_pending():
    _reset()
    # 1) Crear pending mandando status
    webhook._process_message({"type": "text", "from": "5491166667777", "text": {"body": "como va la edicion"}})
    SENT.clear()
    # 2) Felipe responde OK
    webhook._process_message({"type": "text", "from": config.FELIPE_WA_NUMBER.lstrip("+"), "text": {"body": "OK"}})
    # Espera 2 envios: respuesta al cliente + confirmacion a Felipe
    tos = [s[0] for s in SENT]
    assert "+5491166667777" in tos, f"deberia haber mandado al cliente, sent={tos}"
    assert config.FELIPE_WA_NUMBER in tos
    pendings = [json.loads(l) for l in approval_channel.PENDING_FILE.read_text(encoding="utf-8").splitlines() if l]
    assert pendings[-1]["status"] == "sent"


def test_felipe_editar_envia_custom():
    _reset()
    webhook._process_message({"type": "text", "from": "5491166667777", "text": {"body": "como va el reel"}})
    SENT.clear()
    webhook._process_message({
        "type": "text",
        "from": config.FELIPE_WA_NUMBER.lstrip("+"),
        "text": {"body": "EDITAR Te paso el link en 30 minutos."}
    })
    # El primer envio deberia ser al cliente con el texto custom
    cliente_msgs = [s for s in SENT if s[0] == "+5491166667777"]
    assert cliente_msgs, "deberia mandar al cliente"
    assert "30 minutos" in cliente_msgs[0][1]


def test_felipe_descartar_no_envia():
    _reset()
    webhook._process_message({"type": "text", "from": "5491166667777", "text": {"body": "como va el reel"}})
    SENT.clear()
    webhook._process_message({"type": "text", "from": config.FELIPE_WA_NUMBER.lstrip("+"), "text": {"body": "DESCARTAR"}})
    # No deberia mandar al cliente; solo confirmacion a Felipe
    cliente_msgs = [s for s in SENT if s[0] == "+5491166667777"]
    assert not cliente_msgs, "no deberia mandar al cliente tras DESCARTAR"
    pendings = [json.loads(l) for l in approval_channel.PENDING_FILE.read_text(encoding="utf-8").splitlines() if l]
    assert pendings[-1]["status"] == "discarded"


def test_performance_siempre_borrador():
    _reset()
    webhook._process_message({"type": "text", "from": "5491166667777", "text": {"body": "como van los leads esta semana"}})
    assert len(SENT) == 1
    to, _ = SENT[0]
    assert to == config.FELIPE_WA_NUMBER, "performance siempre va a borrador"


def test_non_text_ignorado():
    _reset()
    webhook._process_message({"type": "image", "from": "5491166667777"})
    assert not SENT, "tipos no-texto deberian ignorarse en etapa 1"


def main():
    print("=== E2E mock test — account_manager ===")
    print(f"Sandbox: {_TMP}")
    print()
    _case("faq -> auto-respuesta al cliente", test_faq_auto)
    _case("status_produccion -> borrador a Felipe", test_status_borrador)
    _case("keyword urgente -> escalamiento a Felipe", test_escalamiento_keyword)
    _case("cliente desconocido -> borrador a Felipe", test_cliente_desconocido_va_a_borrador)
    _case("Felipe OK -> envia al cliente y marca sent", test_felipe_ok_resuelve_pending)
    _case("Felipe EDITAR <texto> -> envia custom", test_felipe_editar_envia_custom)
    _case("Felipe DESCARTAR -> no envia, marca discarded", test_felipe_descartar_no_envia)
    _case("performance_campana -> siempre borrador", test_performance_siempre_borrador)
    _case("mensaje no-texto -> ignorado", test_non_text_ignorado)

    print()
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    print(f"=== {passed}/{total} OK ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
