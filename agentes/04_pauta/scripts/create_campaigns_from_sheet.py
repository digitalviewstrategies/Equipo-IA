"""
create_campaigns_from_sheet.py — Crea campanas en Meta Ads a partir del Google Sheet de DV.

Uso:
    python scripts/create_campaigns_from_sheet.py

Por cada fila del sheet (Cliente, Direccion, Material, Presupuesto):
  1. Valida que el cliente tenga brand en shared/brands/.
  2. Agrupa los videos de Drive por nombre base (resolucion _9x16 y _1x1).
  3. Crea la campana y el ad set en Meta (PAUSED).
  4. Por cada creativo: descarga los videos, los sube a Meta y crea el ad.
  5. Guarda el plan de campana en outputs/ y los IDs en _draft_ids.json.

Naming:
  Campaign: [Cliente] / Leads / ABO / [Direccion]
  Ad set:   [Cliente] / [Geolocalizacion]
  Ad:       [Direccion] / [nombre_base]
"""

import json
import os
import re
import tempfile
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from drive_downloader import download_video, group_videos_by_creative
from meta_api import MetaAdsAPI, MetaAPIError
from output_manager import load_brand, save_output
from sheets_reader import get_campaign_rows

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)

AGENT_DIR = Path(__file__).resolve().parent.parent
DRAFT_IDS_DIR = AGENT_DIR / "outputs"

# Presupuesto minimo diario en USD (Meta exige minimo)
MIN_DAILY_BUDGET_USD = 5.0

# Targeting base para real estate argentino (fallback si no hay brand)
DEFAULT_TARGETING = {
    "geo_locations": {
        "cities": [
            {"key": "2657340", "name": "Buenos Aires", "country": "AR"},
        ]
    },
    "age_min": 30,
    "age_max": 60,
}

# Placements por resolucion
PLACEMENTS_9x16 = {
    "publisher_platforms": ["facebook", "instagram"],
    "facebook_positions": ["story", "reels"],
    "instagram_positions": ["story", "reels"],
}

PLACEMENTS_1x1 = {
    "publisher_platforms": ["facebook", "instagram"],
    "facebook_positions": ["feed"],
    "instagram_positions": ["feed"],
}


def _slug(text: str) -> str:
    """Convierte texto a slug para nombres de archivo."""
    text = text.lower().strip()
    text = re.sub(r"[áàä]", "a", text)
    text = re.sub(r"[éèë]", "e", text)
    text = re.sub(r"[íìï]", "i", text)
    text = re.sub(r"[óòö]", "o", text)
    text = re.sub(r"[úùü]", "u", text)
    text = re.sub(r"[ñ]", "n", text)
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def _daily_budget_cents(presupuesto_usd: float) -> int:
    """Convierte presupuesto mensual USD a centavos diarios. Minimo $5/dia."""
    daily = presupuesto_usd / 30
    daily = max(daily, MIN_DAILY_BUDGET_USD)
    return int(round(daily * 100))


def _infer_geo(direccion: str, brand: dict) -> str:
    """
    Intenta inferir barrio/zona de la direccion para el nombre del ad set.
    Fallback: usa default_geo del brand.
    """
    barrios_conocidos = [
        "Palermo", "Belgrano", "Recoleta", "Nunez", "Nuñez", "Caballito",
        "San Isidro", "Vicente Lopez", "Olivos", "Tigre", "San Fernando",
        "Pilar", "Martinez", "Florida", "Munro", "Villa Urquiza",
    ]
    for barrio in barrios_conocidos:
        if barrio.lower() in direccion.lower():
            return barrio

    geo = brand.get("meta_ads", {}).get("default_geo", [])
    return geo[0] if geo else "CABA"


def _build_targeting(brand: dict) -> dict:
    """Construye el targeting base desde el brand system."""
    meta = brand.get("meta_ads", {})
    targeting = dict(DEFAULT_TARGETING)
    targeting["age_min"] = meta.get("default_age_min", 30)
    targeting["age_max"] = meta.get("default_age_max", 60)
    return targeting


def _save_draft_ids(cliente: str, entry: dict) -> None:
    """Agrega o actualiza una entrada en el _draft_ids.json del cliente."""
    draft_file = DRAFT_IDS_DIR / cliente / "_draft_ids.json"
    draft_file.parent.mkdir(parents=True, exist_ok=True)

    existing: list = []
    if draft_file.exists():
        try:
            with open(draft_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                existing = data if isinstance(data, list) else [data]
        except Exception:
            existing = []

    existing.append(entry)
    with open(draft_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)


def _build_plan_md(
    cliente: str,
    direccion: str,
    campaign_name: str,
    adset_name: str,
    ads: list[dict],
    presupuesto_usd: float,
    campaign_id: str,
    adset_id: str,
) -> str:
    ads_lines = "\n".join(
        f"  - {a['name']} | video_id: {a.get('video_id', 'pendiente')} | "
        f"placement: {a['placement']} | status: PAUSED"
        for a in ads
    )
    return f"""# Plan de Campana — {cliente} — {direccion} — {date.today()}

## Nomenclatura
- **Campaign:** {campaign_name}
- **Ad Set:** {adset_name}

## IDs
- campaign_id: {campaign_id}
- adset_id: {adset_id}

## Presupuesto
- Mensual: USD {presupuesto_usd:.2f}
- Diario: USD {presupuesto_usd / 30:.2f}

## Ads creados
{ads_lines}

## Placements
- 9x16 → Stories + Reels (Facebook + Instagram)
- 1x1  → Feed (Facebook + Instagram)

## Notas
- Estado inicial: PAUSED. Activar manualmente tras revision.
- special_ad_categories: HOUSING
"""


def process_row(row: dict, credentials_path: str) -> dict:
    """
    Procesa una fila del sheet y crea la campana en Meta.

    Returns:
        Dict con status ('ok', 'skip', 'error') y detalle.
    """
    cliente = row["cliente"]
    direccion = row["direccion"]
    presupuesto_usd = row["presupuesto_usd"]
    drive_links = row["material"]

    # 1. Validar brand
    brand = load_brand(cliente)
    if brand is None:
        return {
            "status": "skip",
            "cliente": cliente,
            "direccion": direccion,
            "mensaje": (
                f"Cliente '{cliente}' no encontrado en shared/brands/. "
                "Onboardearlo antes de continuar."
            ),
        }

    meta_cfg = brand.get("meta_ads", {})
    ad_account_id = meta_cfg.get("ad_account_id")
    page_id = meta_cfg.get("page_id")

    if not ad_account_id:
        return {
            "status": "skip",
            "cliente": cliente,
            "direccion": direccion,
            "mensaje": f"Brand de '{cliente}' no tiene ad_account_id configurado.",
        }

    # 2. Agrupar videos por creativo
    print(f"  Agrupando videos desde Drive...")
    groups = group_videos_by_creative(drive_links, credentials_path)
    if not groups:
        return {
            "status": "error",
            "cliente": cliente,
            "direccion": direccion,
            "mensaje": "No se pudo agrupar ningun video. Verificar nombres (_9x16, _1x1) y permisos.",
        }

    # 3. Nombres de campana, ad set
    campaign_name = f"{cliente} / Leads / ABO / {direccion}"
    geo = _infer_geo(direccion, brand)
    adset_name = f"{cliente} / {geo}"

    # 4. Crear campana
    api = MetaAdsAPI(ad_account_id=ad_account_id)
    print(f"  Creando campana: {campaign_name}")
    campaign_result = api.create_campaign(
        name=campaign_name,
        objective="OUTCOME_LEADS",
        status="PAUSED",
        special_ad_categories=["HOUSING"],
    )
    campaign_id = campaign_result["id"]

    # 5. Crear ad set
    targeting = _build_targeting(brand)
    daily_budget_cents = _daily_budget_cents(presupuesto_usd)
    print(f"  Creando ad set: {adset_name} | budget: ${daily_budget_cents/100:.2f}/dia")
    adset_result = api.create_ad_set(
        campaign_id=campaign_id,
        name=adset_name,
        targeting=targeting,
        daily_budget=daily_budget_cents,
        optimization_goal="LEAD_GENERATION",
        status="PAUSED",
    )
    adset_id = adset_result["id"]

    # 6. Crear ads por creativo
    ads_created = []
    with tempfile.TemporaryDirectory(prefix="dv_media_") as tmp_dir:
        for group in groups:
            base_name = group["base_name"]
            ad_name = f"{direccion} / {base_name}"
            print(f"  Procesando creativo: {base_name}")

            for resolution, url in [("9x16", group["9x16"]), ("1x1", group["1x1"])]:
                if not url:
                    print(f"    [WARN] Sin video {resolution} para '{base_name}'. Se omite este placement.")
                    continue

                placement_label = "Stories + Reels" if resolution == "9x16" else "Feed"
                placements = PLACEMENTS_9x16 if resolution == "9x16" else PLACEMENTS_1x1

                print(f"    Descargando {resolution}...")
                local_path = download_video(url, credentials_path, dest_dir=tmp_dir)

                print(f"    Subiendo a Meta...")
                video_result = api.upload_video(str(local_path), title=ad_name)
                video_id = video_result.get("id") or video_result.get("video_id")

                # Creative spec con video y placement customization
                creative_spec = {
                    "name": f"Creative {ad_name} {resolution}",
                    "object_story_spec": {
                        "page_id": page_id,
                        "video_data": {
                            "video_id": video_id,
                            "message": "",
                            "call_to_action": {"type": "LEARN_MORE"},
                        },
                    },
                }

                ad_result = api.create_ad_with_creative(
                    ad_set_id=adset_id,
                    name=f"{ad_name} / {resolution}",
                    creative_spec={"creative": creative_spec},
                    status="PAUSED",
                )
                ad_id = ad_result.get("id", "")

                ads_created.append({
                    "name": f"{ad_name} / {resolution}",
                    "ad_id": ad_id,
                    "video_id": video_id,
                    "placement": placement_label,
                    "resolution": resolution,
                })
                print(f"    Ad creado: {ad_id} ({placement_label})")

    # 7. Guardar plan de campana
    plan_md = _build_plan_md(
        cliente, direccion, campaign_name, adset_name,
        ads_created, presupuesto_usd, campaign_id, adset_id,
    )
    plan_nombre = _slug(f"{direccion}_{date.today()}")
    save_output(cliente, "plan_campana", plan_nombre, plan_md)

    # 8. Guardar draft IDs
    draft_entry = {
        "campaign_id": campaign_id,
        "adset_id": adset_id,
        "ad_account_id": ad_account_id,
        "campaign_name": campaign_name,
        "adset_name": adset_name,
        "direccion": direccion,
        "presupuesto_mensual_usd": presupuesto_usd,
        "ads": ads_created,
        "status": "PAUSED",
        "created_at": date.today().isoformat(),
    }
    _save_draft_ids(cliente, draft_entry)

    return {
        "status": "ok",
        "cliente": cliente,
        "direccion": direccion,
        "campaign_id": campaign_id,
        "adset_id": adset_id,
        "ads_count": len(ads_created),
    }


def main():
    credentials_path_rel = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials/google_service_account.json")
    credentials_path = str(AGENT_DIR / credentials_path_rel)

    print("DV Media Buyer — Creacion de campanas desde Google Sheet")
    print("=" * 60)

    print("Leyendo sheet...")
    rows = get_campaign_rows()
    if not rows:
        print("No se encontraron filas validas en el sheet.")
        return

    print(f"Filas encontradas: {len(rows)}\n")

    results = []
    for i, row in enumerate(rows, start=1):
        print(f"[{i}/{len(rows)}] {row['cliente']} | {row['direccion']} | USD {row['presupuesto_usd']:.0f}/mes")
        try:
            result = process_row(row, credentials_path)
        except MetaAPIError as e:
            result = {
                "status": "error",
                "cliente": row["cliente"],
                "direccion": row["direccion"],
                "mensaje": str(e),
            }
        except Exception as e:
            result = {
                "status": "error",
                "cliente": row["cliente"],
                "direccion": row["direccion"],
                "mensaje": f"Error inesperado: {e}",
            }
        results.append(result)
        print()

    # Resumen final
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    ok = [r for r in results if r["status"] == "ok"]
    skip = [r for r in results if r["status"] == "skip"]
    error = [r for r in results if r["status"] == "error"]

    for r in ok:
        print(f"  OK    {r['cliente']} | {r['direccion']} | campaign: {r['campaign_id']} | {r['ads_count']} ads")
    for r in skip:
        print(f"  SKIP  {r['cliente']} | {r['direccion']} | {r['mensaje']}")
    for r in error:
        print(f"  ERROR {r['cliente']} | {r['direccion']} | {r['mensaje']}")

    print(f"\nTotal: {len(ok)} OK, {len(skip)} omitidas, {len(error)} errores.")


if __name__ == "__main__":
    main()
