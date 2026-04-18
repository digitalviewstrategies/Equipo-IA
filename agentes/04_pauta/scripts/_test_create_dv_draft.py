"""
One-off: crea la campana DV_Leads_2026-04 en modo borrador (PAUSED) para que
Felipe inspeccione la config en Ads Manager antes de lanzar.

- Campaign: DV_Leads_2026-04 (OUTCOME_LEADS, PAUSED, special_ad_categories=[])
- Ad Set:   DV_DuenosInmobiliariasCABAZN_AllPlacements (PAUSED, USD 6/dia,
            LEAD_GENERATION, placements Feed/Stories/Reels FB+IG, sin AN)
- Ads:      no se crean (creativos pendientes).

Uso: python scripts/_test_create_dv_draft.py
"""

import json
from pathlib import Path
from meta_api import MetaAdsAPI, MetaAPIError
from output_manager import load_brand


def main() -> int:
    brand = load_brand("digital_view")
    ma = brand["meta_ads"]
    account_id = ma["ad_account_id"]
    page_id = ma["page_id"]

    print(f"Cuenta destino: {account_id} ({ma['ad_account_name']}, {ma['currency']})")
    print(f"Page: {page_id}")

    api = MetaAdsAPI(ad_account_id=account_id)

    # 1) Campana
    # Naming DV: "Nombre quien crea / Objetivo / ABO-CBO / [palabra clave creativo]"
    campaign_name = "MB Claude / Leads / ABO / DV"
    print(f"\n[1/2] Creando campana {campaign_name}...")
    import requests
    from meta_api import BASE_URL

    camp_params = {
        "name": campaign_name,
        "objective": "OUTCOME_LEADS",
        "status": "PAUSED",
        "special_ad_categories": json.dumps([]),
        "is_adset_budget_sharing_enabled": "false",
        "access_token": api.access_token,
    }
    camp_resp = requests.post(
        f"{BASE_URL}/{account_id}/campaigns", params=camp_params, timeout=30
    ).json()
    if "error" in camp_resp:
        print(f"ERROR creando campana: {camp_resp['error']}")
        return 1
    campaign_id = camp_resp["id"]
    print(f"  campaign_id = {campaign_id}")

    # 2) Ad Set
    # Naming DV: "Nombre quien crea / donde apunta"
    adset_name = "MB Claude / CABA+ZN DueñosInmo"
    # Geo keys encontradas via /search?type=adgeolocation
    targeting = {
        "geo_locations": {
            "regions": [
                {"key": "103", "name": "Ciudad Autonoma de Buenos Aires", "country": "AR"},
            ],
            "cities": [
                {"key": "90988", "radius": 20, "distance_unit": "kilometer"},  # Vicente Lopez
                {"key": "89977", "radius": 20, "distance_unit": "kilometer"},  # San Isidro
                {"key": "89927", "radius": 20, "distance_unit": "kilometer"},  # San Fernando (BA)
            ],
            "location_types": ["home", "recent"],
        },
        "age_min": 30,
        "age_max": 60,
        "publisher_platforms": ["facebook", "instagram"],
        "facebook_positions": ["feed", "story"],
        "instagram_positions": ["stream", "story", "reels"],
        # Advantage+ Audience off por politica DV (CLAUDE.md).
        "targeting_automation": {"advantage_audience": 0},
    }

    print(f"\n[2/2] Creando ad set {adset_name}...")
    # Meta daily_budget va en unidades minimas de la moneda. USD 6.00 = 600 centavos.
    daily_budget_cents = 600

    # Lead ads a nivel ad set requieren promoted_object.page_id en OUTCOME_LEADS.
    # El wrapper no expone promoted_object, asi que hacemos el request directo.
    # Nota: NO pasamos promoted_object/destination_type. Esos quedan para
    # cuando se cree el ad con el lead form. El page_id 61557477811665 no
    # fue aceptado a nivel ad set (business distinto al del ad account).
    # Felipe lo configura en la UI o al crear el ad con el lead form.
    params = {
        "campaign_id": campaign_id,
        "name": adset_name,
        "targeting": json.dumps(targeting),
        "daily_budget": daily_budget_cents,
        "optimization_goal": "LEAD_GENERATION",
        "billing_event": "IMPRESSIONS",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "destination_type": "ON_AD",  # Formularios instantaneos (conversion unico)
        "status": "PAUSED",
        "access_token": api.access_token,
    }
    resp = requests.post(
        f"{BASE_URL}/{account_id}/adsets", params=params, timeout=30
    ).json()

    if "error" in resp:
        print(f"ERROR creando ad set: {resp['error']}")
        print(f"  Limpieza: pausa/borra la campana {campaign_id} manualmente si hace falta.")
        return 1

    adset_id = resp["id"]
    print(f"  adset_id = {adset_id}")

    print("\n=== OK ===")
    print(f"Campaign : {campaign_id}")
    print(f"Ad Set   : {adset_id}")
    print(f"URL Ads Manager: https://business.facebook.com/adsmanager/manage/campaigns?act={account_id.replace('act_', '')}&selected_campaign_ids={campaign_id}")

    out = Path(__file__).resolve().parent.parent / "outputs" / "digital_view" / "_draft_ids.json"
    out.write_text(json.dumps({
        "campaign_id": campaign_id,
        "adset_id": adset_id,
        "ad_account_id": account_id,
        "status": "PAUSED",
        "created_at": "2026-04-18",
    }, indent=2), encoding="utf-8")
    print(f"IDs guardados en: {out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except MetaAPIError as e:
        print(f"Meta API error: {e}")
        if e.response:
            print(json.dumps(e.response, indent=2))
        raise SystemExit(1)
