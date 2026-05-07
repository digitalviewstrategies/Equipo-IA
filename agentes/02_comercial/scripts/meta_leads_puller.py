"""
meta_leads_puller.py — Trae leads de Meta Lead Ads y los carga al pipeline comercial.

Para cada brand con `meta_ads.page_id`, lista los leadgen_forms del page,
trae leads creados en las ultimas N horas y los inserta como prospectos
en `02_comercial/data/pipeline.json` (etapa pre_filtro).

Idempotente: cada lead trae un id unico de Meta. Antes de crear un prospecto
verifica que ese lead_id no este ya cargado.

Uso:
    python meta_leads_puller.py            # ultimas 24h
    python meta_leads_puller.py --hours 48
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BRANDS = ROOT / "shared" / "brands"

sys.path.insert(0, str(ROOT / "agentes" / "04_pauta"))
sys.path.insert(0, str(Path(__file__).parent))

from scripts.meta_api import MetaAdsAPI, MetaAPIError  # noqa: E402
import pipeline as pipe  # noqa: E402


def _normalize_field_data(field_data: list[dict]) -> dict[str, str]:
    """field_data viene como [{name: 'email', values: ['x@y.com']}, ...]."""
    out: dict[str, str] = {}
    for f in field_data or []:
        name = (f.get("name") or "").lower()
        vals = f.get("values") or []
        if vals:
            out[name] = vals[0]
    return out


def _already_imported(lead_id: str) -> bool:
    data = pipe._load()
    for p in data.get("prospectos", []):
        if p.get("meta_lead_id") == lead_id:
            return True
    return False


def _add_prospecto_from_lead(cliente: str, lead: dict) -> dict | None:
    if _already_imported(lead["id"]):
        return None

    fd = _normalize_field_data(lead.get("field_data", []))
    nombre = fd.get("full_name") or fd.get("nombre") or fd.get("first_name") or "Sin nombre"
    if fd.get("first_name") and fd.get("last_name"):
        nombre = f"{fd['first_name']} {fd['last_name']}"

    prospecto = pipe.add_prospecto(
        nombre=nombre,
        empresa=fd.get("company_name") or "",
        tipo="otro",
        zona="desconocida",
        telefono=fd.get("phone_number") or fd.get("telefono") or "",
        email=fd.get("email") or "",
        fuente=f"meta_lead_ads:{cliente}",
        notas=f"Lead Meta - campaign_id={lead.get('campaign_id', '')} ad_id={lead.get('ad_id', '')} created={lead.get('created_time', '')}",
    )

    # marcador de origen para idempotencia
    data = pipe._load()
    for p in data["prospectos"]:
        if p["id"] == prospecto["id"]:
            p["meta_lead_id"] = lead["id"]
            p["meta_campaign_id"] = lead.get("campaign_id", "")
            p["meta_ad_id"] = lead.get("ad_id", "")
            break
    pipe._save(data)
    return prospecto


def pull_recent_leads(hours: int = 24) -> dict:
    since_unix = int(time.time()) - hours * 3600
    resumen = {"forms_revisados": 0, "leads_traidos": 0, "prospectos_nuevos": 0, "por_cliente": {}}

    for brand_path in sorted(BRANDS.glob("*.json")):
        if brand_path.stem.startswith("_"):
            continue
        try:
            brand = json.loads(brand_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        meta = brand.get("meta_ads") or {}
        page_id = meta.get("page_id")
        if not page_id:
            continue

        cliente = brand_path.stem
        try:
            api = MetaAdsAPI()
            page_token = api.get_page_access_token(page_id)
            forms = api.get_leadgen_forms(page_id, page_token=page_token)
        except MetaAPIError as e:
            resumen["por_cliente"][cliente] = {"status": "error", "msg": str(e)[:200]}
            continue

        nuevos = 0
        for form in forms:
            if form.get("status") != "ACTIVE":
                continue
            try:
                leads = api.get_form_leads(form["id"], page_token=page_token, since_unix=since_unix)
            except MetaAPIError as e:
                resumen["por_cliente"].setdefault(cliente, {})[form["id"]] = f"err: {str(e)[:120]}"
                continue
            resumen["forms_revisados"] += 1
            resumen["leads_traidos"] += len(leads)
            for l in leads:
                p = _add_prospecto_from_lead(cliente, l)
                if p:
                    nuevos += 1

        resumen["por_cliente"][cliente] = {"status": "ok", "nuevos": nuevos}
        resumen["prospectos_nuevos"] += nuevos

    return resumen


def main(argv: list[str]) -> int:
    hours = 24
    if "--hours" in argv:
        i = argv.index("--hours")
        hours = int(argv[i + 1])
    r = pull_recent_leads(hours=hours)
    print(json.dumps(r, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
