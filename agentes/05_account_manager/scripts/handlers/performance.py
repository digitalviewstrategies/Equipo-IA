"""Handler performance_campana: invoca 04_pauta para traer numeros de Meta Ads.

Etapa 1: siempre devuelve borrador (auto=False) porque numeros sensibles
deberian pasar por revision humana antes de salir al cliente.
"""
import sys
from pathlib import Path

# Permitir import del modulo del agente 04_pauta
PAUTA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "04_pauta"
if str(PAUTA_DIR) not in sys.path:
    sys.path.insert(0, str(PAUTA_DIR))


def handle(text: str, entities: dict, brand: dict | None, contact_name: str | None) -> dict:
    ad_account = (brand or {}).get("meta_ads", {}).get("ad_account_id")
    if not ad_account:
        return {
            "text": "Te paso los numeros actualizados en un rato, los chequeo con Felipe.",
            "ok": False,
        }
    periodo = entities.get("periodo", "ultimos 7 dias")
    try:
        from scripts.meta_api import MetaAdsAPI  # type: ignore
        api = MetaAdsAPI(ad_account_id=ad_account)
        # TODO etapa 1.5: definir el metodo summary() en 04_pauta/scripts/meta_api.py
        # Por ahora siempre fallback.
        raise NotImplementedError
    except Exception:
        return {
            "text": f"Te paso los numeros de {periodo} en un rato, los chequeo con Felipe.",
            "ok": False,
        }
