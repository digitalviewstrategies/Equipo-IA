"""
Crea 3 campanas en borrador (PAUSED) para Toribio Achaval.

Estructura por campana:
  - Campaign PAUSED  (HOUSING, OUTCOME_LEADS)
  - Ad Set PAUSED    (geo lat/lng CABA+ZN, sin ads hasta que llegue el material)

Naming: Pipe / Leads / ABO / Direccion
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.meta_api import MetaAdsAPI
from scripts.fx import get_ccl, ars_a_usd_centavos

AD_ACCOUNT_ID = "act_2390281541415930"

# Presupuesto: 100k ARS / semana = 14286 ARS/dia -> convertido a USD al CCL del dia
ARS_DIARIO = 100_000 / 7
ccl = get_ccl()
DAILY_BUDGET_CENTAVOS = ars_a_usd_centavos(ARS_DIARIO, ccl)
print(f"CCL: ${ccl:,.2f} | Budget diario: {ARS_DIARIO:.0f} ARS = {DAILY_BUDGET_CENTAVOS} centavos USD (~USD {DAILY_BUDGET_CENTAVOS/100:.2f})")

# Geo estandar CABA/ZN via lat/lng (radio 8km por punto)
GEO_LOCATIONS = {
    "custom_locations": [
        {"latitude": -34.6037, "longitude": -58.3816, "radius": 17, "distance_unit": "kilometer"},
        {"latitude": -34.4706, "longitude": -58.5131, "radius": 17, "distance_unit": "kilometer"},
    ]
}

TARGETING_BASE = {
    "geo_locations": GEO_LOCATIONS,
    "age_min": 30,
    "age_max": 60,
}

CAMPANAS = [
    {
        "direccion": "9 DE JULIO",
        "campaign_name": "Pipe / Leads / ABO / 9 DE JULIO",
        "adset_name": "Pipe / CABA+ZN",
    },
    {
        "direccion": "NICOLAS AVELLANEDA",
        "campaign_name": "Pipe / Leads / ABO / NICOLAS AVELLANEDA",
        "adset_name": "Pipe / CABA+ZN",
    },
    {
        "direccion": "PARANA",
        "campaign_name": "Pipe / Leads / ABO / PARANA",
        "adset_name": "Pipe / CABA+ZN",
    },
]


def main():
    api = MetaAdsAPI(ad_account_id=AD_ACCOUNT_ID)

    resultados = []

    for camp in CAMPANAS:
        print(f"\n--- Creando borrador: {camp['direccion']} ---")

        # 1. Campana
        campaign = api.create_campaign(
            name=camp["campaign_name"],
            objective="OUTCOME_LEADS",
            status="PAUSED",
            special_ad_categories=["HOUSING"],
            is_adset_budget_sharing_enabled=True,
            bid_strategy="LOWEST_COST_WITHOUT_CAP",
        )
        campaign_id = campaign["id"]
        print(f"  Campaign ID: {campaign_id}")

        # 2. Ad set
        ad_set = api.create_ad_set(
            campaign_id=campaign_id,
            name=camp["adset_name"],
            targeting=TARGETING_BASE,
            daily_budget=DAILY_BUDGET_CENTAVOS,
            optimization_goal="LEAD_GENERATION",
            billing_event="IMPRESSIONS",
            status="PAUSED",
        )
        ad_set_id = ad_set["id"]
        print(f"  Ad Set ID:   {ad_set_id}")

        resultados.append({
            "direccion": camp["direccion"],
            "campaign_name": camp["campaign_name"],
            "campaign_id": campaign_id,
            "adset_name": camp["adset_name"],
            "adset_id": ad_set_id,
            "status": "PAUSED",
        })

    print("\n=== RESUMEN ===")
    for r in resultados:
        print(f"\n{r['direccion']}")
        print(f"  Campaign: {r['campaign_id']} — {r['campaign_name']}")
        print(f"  Ad Set:   {r['adset_id']} — {r['adset_name']}")

    # Guardar IDs para referencia
    output_path = Path(__file__).resolve().parent.parent / "outputs" / "toribio_achaval" / "draft_ids.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"\nIDs guardados en: {output_path}")


if __name__ == "__main__":
    main()
