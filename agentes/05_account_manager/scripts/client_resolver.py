"""Resuelve numero E.164 a cliente DV via shared/brands/<cliente>.json."""
import json
from . import config


def _normalize(num: str) -> str:
    """Normaliza a formato +<digits> sin espacios ni guiones."""
    digits = "".join(c for c in num if c.isdigit())
    return f"+{digits}" if digits else ""


def resolve(from_number: str) -> dict:
    """Devuelve {cliente, contact_name, brand} o {cliente: None} si no matchea."""
    target = _normalize(from_number)
    if not config.BRANDS_DIR.exists():
        return {"cliente": None, "contact_name": None, "brand": None}

    for brand_file in config.BRANDS_DIR.glob("*.json"):
        try:
            brand = json.loads(brand_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        wa = brand.get("whatsapp", {})
        contacts = [_normalize(c) for c in wa.get("contacts", [])]
        if target in contacts:
            return {
                "cliente": brand_file.stem,
                "contact_name": wa.get("primary_contact_name"),
                "brand": brand,
            }
    return {"cliente": None, "contact_name": None, "brand": None}
