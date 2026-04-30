"""Wrapper Meta WhatsApp Cloud API (Graph v21)."""
import requests
from . import config

GRAPH_URL = f"https://graph.facebook.com/v21.0/{config.PHONE_NUMBER_ID}/messages"


def send_text(to: str, body: str) -> dict:
    """Envia texto a un numero E.164. Devuelve respuesta de la API."""
    headers = {
        "Authorization": f"Bearer {config.WABA_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to.lstrip("+"),
        "type": "text",
        "text": {"body": body, "preview_url": False},
    }
    r = requests.post(GRAPH_URL, headers=headers, json=payload, timeout=15)
    r.raise_for_status()
    return r.json()
