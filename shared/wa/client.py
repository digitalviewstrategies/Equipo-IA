"""
Cliente unico de Meta WhatsApp Cloud API (Graph v21).

Lo instancia cada agente con sus propios token y phone_number_id.
- 05_account_manager usa la app Chatbot-Digital (conversaciones 1-1).
- 03_delivery_reporting usa la app Reportes (envio de reportes a Elias / cliente).
"""
from __future__ import annotations

import requests


class WAClient:
    def __init__(self, token: str, phone_number_id: str, api_version: str = "v21.0"):
        if not token or not phone_number_id:
            raise ValueError("WAClient requiere token y phone_number_id no vacios.")
        self.token = token
        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def send_text(self, to: str, body: str) -> dict:
        """Envia texto libre. Solo funciona dentro de la ventana de 24hs."""
        payload = {
            "messaging_product": "whatsapp",
            "to": to.lstrip("+"),
            "type": "text",
            "text": {"body": body, "preview_url": False},
        }
        r = requests.post(self.base_url, headers=self._headers(), json=payload, timeout=15)
        r.raise_for_status()
        return r.json()

    def send_template(self, to: str, template_name: str, language: str = "es_AR", components: list | None = None) -> dict:
        """Envia template aprobado por Meta. Sirve fuera de la ventana de 24hs."""
        template_payload: dict = {"name": template_name, "language": {"code": language}}
        if components:
            template_payload["components"] = components
        payload = {
            "messaging_product": "whatsapp",
            "to": to.lstrip("+"),
            "type": "template",
            "template": template_payload,
        }
        r = requests.post(self.base_url, headers=self._headers(), json=payload, timeout=15)
        r.raise_for_status()
        return r.json()
