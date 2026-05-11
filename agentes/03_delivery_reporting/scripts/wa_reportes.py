"""
Wrapper especifico de WhatsApp para 03_delivery_reporting.

Usa el cliente compartido (shared/wa/) y carga credenciales desde .env local
(app Reportes, separado del Chatbot-Digital de 05_account_manager).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# shared/wa esta en la raiz del repo (3 niveles arriba de scripts/)
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared.wa import WAClient  # noqa: E402

REPORTES_WABA_TOKEN = os.getenv("REPORTES_WABA_TOKEN", "")
REPORTES_PHONE_NUMBER_ID = os.getenv("REPORTES_PHONE_NUMBER_ID", "")
ELIAS_WA_NUMBER = os.getenv("ELIAS_WA_NUMBER", "")


def _client() -> WAClient:
    return WAClient(REPORTES_WABA_TOKEN, REPORTES_PHONE_NUMBER_ID)


def send_to_elias(body: str) -> dict:
    """Manda un texto a Elias por WhatsApp. Solo funciona dentro de la ventana de 24hs."""
    if not ELIAS_WA_NUMBER:
        raise RuntimeError("Falta ELIAS_WA_NUMBER en .env")
    return _client().send_text(ELIAS_WA_NUMBER, body)


def send_text(to: str, body: str) -> dict:
    return _client().send_text(to, body)


def send_reporte_semanal_template(to: str, nombre: str, url_pdf: str) -> dict:
    """
    Envia el template aprobado 'reportes_semanales_digital' (es_AR).
    Body var {{1}} = nombre destinatario.
    Button URL var = link al PDF del reporte.
    Funciona fuera de la ventana de 24hs.
    """
    components = [
        {
            "type": "body",
            "parameters": [{"type": "text", "text": nombre}],
        },
        {
            "type": "button",
            "sub_type": "url",
            "index": "0",
            "parameters": [{"type": "text", "text": url_pdf}],
        },
    ]
    return _client().send_template(
        to,
        template_name="reportes_semanales_digital",
        language="es_AR",
        components=components,
    )


if __name__ == "__main__":
    print("REPORTES_PHONE_NUMBER_ID:", REPORTES_PHONE_NUMBER_ID)
    print("ELIAS_WA_NUMBER:", ELIAS_WA_NUMBER)
    print("Token cargado:", bool(REPORTES_WABA_TOKEN))
