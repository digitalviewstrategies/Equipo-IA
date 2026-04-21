"""
Crea draft de campana DV B2B (servicios a inmobiliarias / agentes en Zona Norte).

- Campaign: DV / Leads / ABO / ZonaNorte  (sin HOUSING, B2B)
- Ad set:   DV / ZonaNorte
- Budget:   USD 6/dia, 30 dias
- Destino:  Lead Form "Cp Digital View Nuevo" (se busca por nombre en la page)
- Status:   PAUSED (review manual antes de activar)

Los ads NO se crean en este paso. Se agregan cuando haya creativos aprobados.
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from meta_api import MetaAdsAPI, MetaAPIError  # noqa: E402
from output_manager import load_brand  # noqa: E402

FORM_NAME = "Cp Digital View Nuevo"
ZN_CITY_QUERIES = ["Vicente Lopez", "San Isidro", "San Fernando", "Tigre", "San Martin"]
CAMPAIGN_NAME = "DV / Leads / ABO / ZonaNorte"
ADSET_NAME = "DV / ZonaNorte"
DAILY_BUDGET_CENTS = 600  # USD 6.00


def get_page_access_token(api: MetaAdsAPI, page_id: str) -> str:
    result = api._request("GET", page_id, params={"fields": "access_token"})
    token = result.get("access_token")
    if not token:
        raise MetaAPIError(
            f"No pude obtener page access token para {page_id}. "
            f"Verifica que el System User tenga permiso 'Manage Page' asignado."
        )
    return token


def find_lead_form(api: MetaAdsAPI, page_id: str, form_name: str) -> str:
    page_token = get_page_access_token(api, page_id)
    page_api = MetaAdsAPI(access_token=page_token, ad_account_id=api.ad_account_id)
    result = page_api._request(
        "GET", f"{page_id}/leadgen_forms",
        params={"fields": "id,name,status", "limit": 200},
    )
    forms = result.get("data", [])
    for f in forms:
        if f.get("name", "").strip().lower() == form_name.strip().lower():
            return f["id"]
    available = ", ".join(f.get("name", "") for f in forms[:20])
    raise MetaAPIError(
        f"No encontre el form '{form_name}' en la page {page_id}. "
        f"Forms disponibles: {available}"
    )


def find_city_keys(api: MetaAdsAPI, queries: list[str]) -> list[dict]:
    """Busca cities en AR y filtra por region Buenos Aires (provincia)."""
    keys: list[dict] = []
    for q in queries:
        result = api._request(
            "GET", "search",
            params={
                "type": "adgeolocation",
                "q": q,
                "location_types": json.dumps(["city"]),
                "country_code": "AR",
                "limit": 10,
            },
        )
        data = result.get("data", [])
        ba = [c for c in data if "Buenos Aires" in c.get("region", "")]
        pick = ba[0] if ba else None
        if not pick:
            avail = ", ".join(f"{c.get('name')} ({c.get('region')})" for c in data[:5])
            print(f"  ! sin match en Buenos Aires para '{q}'. Opciones: {avail}")
            continue
        keys.append({
            "key": pick["key"],
            "name": pick.get("name", q),
            "radius": 5,
            "distance_unit": "mile",  # 5 mi ~= 8 km
        })
        print(f"  + {q} -> {pick.get('name')}, {pick.get('region')} ({pick['key']})")
    if not keys:
        raise MetaAPIError("No se pudo resolver ninguna city key en Buenos Aires.")
    return keys


def main():
    brand = load_brand("digital_view")
    meta = brand["meta_ads"]
    ad_account_id = meta["ad_account_id"]
    page_id = meta["page_id"]

    api = MetaAdsAPI(ad_account_id=ad_account_id)

    print(f"\n[1/4] Buscando lead form '{FORM_NAME}' en page {page_id}...")
    form_id = find_lead_form(api, page_id, FORM_NAME)
    print(f"  form_id: {form_id}")

    print(f"\n[2/4] Resolviendo city keys de Zona Norte...")
    cities = find_city_keys(api, ZN_CITY_QUERIES)

    reuse_id = os.environ.get("REUSE_CAMPAIGN_ID")
    if reuse_id:
        print(f"\n[3/4] Reusando campana existente {reuse_id}")
        campaign_id = reuse_id
    else:
        print(f"\n[3/4] Creando campana '{CAMPAIGN_NAME}' (sin HOUSING)...")
        campaign = api._request("POST", f"{ad_account_id}/campaigns", params={
            "name": CAMPAIGN_NAME,
            "objective": "OUTCOME_LEADS",
            "status": "PAUSED",
            "special_ad_categories": json.dumps([]),
            "is_adset_budget_sharing_enabled": "false",
            "buying_type": "AUCTION",
        })
        campaign_id = campaign["id"]
        print(f"  campaign_id: {campaign_id}")

    start = datetime.now(timezone.utc).replace(microsecond=0)
    end = start + timedelta(days=30)

    targeting = {
        "geo_locations": {"cities": cities},
        "age_min": 25,
        "age_max": 65,
        "targeting_automation": {"advantage_audience": 1},
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "story", "facebook_reels"],
        "instagram_positions": ["stream", "story", "reels", "explore"],
    }

    print(f"\n[4/4] Creando ad set '{ADSET_NAME}'...")
    adset_params = {
        "campaign_id": campaign_id,
        "name": ADSET_NAME,
        "targeting": json.dumps(targeting),
        "daily_budget": DAILY_BUDGET_CENTS,
        "optimization_goal": "LEAD_GENERATION",
        "billing_event": "IMPRESSIONS",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "status": "PAUSED",
        "start_time": start.strftime("%Y-%m-%dT%H:%M:%S+0000"),
        "end_time": end.strftime("%Y-%m-%dT%H:%M:%S+0000"),
        "destination_type": "ON_AD",
        "promoted_object": json.dumps({"page_id": page_id}),
        "is_adset_budget_sharing_enabled": False,
    }
    adset = api._request("POST", f"{ad_account_id}/adsets", params=adset_params)
    adset_id = adset["id"]
    print(f"  adset_id: {adset_id}")

    ids_path = Path(__file__).resolve().parent.parent / "outputs" / "digital_view" / "_draft_ids.json"
    ids_path.parent.mkdir(parents=True, exist_ok=True)
    ids_path.write_text(json.dumps({
        "campaign_id": campaign_id,
        "adset_id": adset_id,
        "ad_account_id": ad_account_id,
        "page_id": page_id,
        "lead_form_id": form_id,
        "lead_form_name": FORM_NAME,
        "status": "PAUSED",
        "created_at": datetime.now().strftime("%Y-%m-%d"),
        "notes": "B2B servicios DV a inmobiliarias/agentes ZN. Ads pendientes hasta tener creativos.",
    }, indent=2, ensure_ascii=False))
    print(f"\nGuardado en {ids_path}")
    print("\nListo. Revisa en Ads Manager y me decis que corregir.")


if __name__ == "__main__":
    try:
        main()
    except MetaAPIError as e:
        print(f"\nERROR: {e}")
        if e.response:
            print(f"Response: {json.dumps(e.response, indent=2)}")
        sys.exit(1)
