"""
Wrapper Meta WhatsApp Cloud API para 05_account_manager (app Chatbot-Digital).

Usa el cliente compartido (shared/wa/) instanciado con las credenciales del .env local.
Mantiene la interfaz historica `send_text(to, body)` para no romper handlers existentes.
"""
from __future__ import annotations

import sys
from pathlib import Path

from . import config

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from shared.wa import WAClient  # noqa: E402

_client: WAClient | None = None


def _get_client() -> WAClient:
    global _client
    if _client is None:
        _client = WAClient(config.WABA_TOKEN, config.PHONE_NUMBER_ID)
    return _client


def send_text(to: str, body: str) -> dict:
    """Envia texto a un numero E.164. Devuelve respuesta de la API."""
    return _get_client().send_text(to, body)
