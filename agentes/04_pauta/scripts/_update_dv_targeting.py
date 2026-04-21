"""Patchea el targeting del ad set existente (cities BA + radio 8km)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meta_api import MetaAdsAPI, MetaAPIError  # noqa: E402
from output_manager import load_brand  # noqa: E402
brand = load_brand("digital_view")
api = MetaAdsAPI(ad_account_id=brand["meta_ads"]["ad_account_id"])

ids = json.loads((Path(__file__).resolve().parent.parent / "outputs/digital_view/_draft_ids.json").read_text())
adset_id = ids["adset_id"]

ZN_POINTS = [
    {"name": "Vicente Lopez", "latitude": -34.5267, "longitude": -58.4836, "radius": 8, "distance_unit": "kilometer"},
    {"name": "San Isidro",    "latitude": -34.4714, "longitude": -58.5076, "radius": 8, "distance_unit": "kilometer"},
    {"name": "Tigre",         "latitude": -34.4264, "longitude": -58.5796, "radius": 8, "distance_unit": "kilometer"},
]

targeting = {
    "geo_locations": {"custom_locations": ZN_POINTS, "location_types": ["home", "recent"]},
    "age_min": 25,
    "age_max": 65,
    "targeting_automation": {"advantage_audience": 1},
    "publisher_platforms": ["facebook", "instagram"],
    "facebook_positions": ["feed", "story", "facebook_reels"],
    "instagram_positions": ["stream", "story", "reels", "explore"],
}

print(f"\nActualizando ad set {adset_id}...")
try:
    api._request("POST", adset_id, params={"targeting": json.dumps(targeting)})
    print("OK. Targeting actualizado.")
except MetaAPIError as e:
    print(f"ERROR: {e}")
    if e.response:
        print(json.dumps(e.response, indent=2))
    sys.exit(1)
