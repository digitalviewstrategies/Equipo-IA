"""Handler performance_campana: invoca 04_pauta/meta_api.summary() para traer numeros reales.

Politica: siempre devuelve borrador (ok=False) — numeros sensibles deben pasar por
revision humana antes de salir al cliente. El valor del handler es que el borrador
viene con los numeros ya extraidos, no con "te paso en un rato".
"""
import sys
from pathlib import Path

# Permitir import del modulo del agente 04_pauta
PAUTA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "04_pauta"
if str(PAUTA_DIR) not in sys.path:
    sys.path.insert(0, str(PAUTA_DIR))


_FALLBACK = "Te paso los numeros actualizados en un rato, los chequeo con Felipe."


def handle(text: str, entities: dict, brand: dict | None, contact_name: str | None) -> dict:
    ad_account = (brand or {}).get("meta_ads", {}).get("ad_account_id")
    if not ad_account:
        return {"text": _FALLBACK, "ok": False}

    # Mapeo simple de periodo -> dias
    periodo_str = (entities.get("periodo") or "").lower()
    if "30" in periodo_str or "mes" in periodo_str:
        days, label = 30, "ultimos 30 dias"
    elif "14" in periodo_str or "2 sem" in periodo_str:
        days, label = 14, "ultimos 14 dias"
    else:
        days, label = 7, "ultimos 7 dias"

    try:
        from scripts.meta_api import MetaAdsAPI  # type: ignore
        api = MetaAdsAPI(ad_account_id=ad_account)
        s = api.summary(last_n_days=days)
    except Exception:
        return {"text": _FALLBACK, "ok": False}

    return {"text": _format(s, label), "ok": False}


def _format(s: dict, label: str) -> str:
    """Tono WA Felipe: voseo, sin emojis, frases cortas, datos concretos."""
    if s.get("impressions", 0) == 0:
        return f"En {label} la cuenta no tuvo delivery. Lo reviso con Felipe y te confirmo."

    leads = s.get("leads", 0)
    spend = s.get("spend_usd", 0)
    cpl = s.get("cpl_usd")
    ctr = s.get("ctr", 0)

    lines = [f"Van los numeros de {label}:"]
    lines.append(f"- Gasto: USD {spend:.0f}")
    if leads > 0:
        lines.append(f"- Leads: {leads} (CPL USD {cpl:.2f})")
    else:
        lines.append("- Leads: 0 todavia, revisamos creativos")
    lines.append(f"- CTR: {ctr:.2f}%")
    return "\n".join(lines)
