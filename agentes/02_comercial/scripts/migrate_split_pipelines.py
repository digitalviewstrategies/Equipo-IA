"""
migrate_split_pipelines.py — One-shot. Separa pipeline.json mezclado.

Mueve a leads_clientes/<cliente>.json todos los prospectos cuya fuente
sea `meta_lead_ads:<cliente>` con cliente != digital_view.
Deja intactos los del servicio DV (B2B) en pipeline.json.

Idempotente: si ya migro, no duplica (chequea meta_lead_id).
Hace backup en data/pipeline.backup.<ts>.json antes de tocar nada.
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).parent))

import pipeline as pipe  # noqa: E402
import leads_clientes as lc  # noqa: E402

B2B_BRANDS = {"digital_view"}


def _cliente_de_fuente(fuente: str) -> str | None:
    if not fuente.startswith("meta_lead_ads:"):
        return None
    return fuente.split(":", 1)[1]


def migrate(dry_run: bool = False) -> dict:
    data = pipe._load()
    prospectos = data.get("prospectos", [])

    a_mover = []
    a_dejar = []
    for p in prospectos:
        cliente = _cliente_de_fuente(p.get("fuente", ""))
        if cliente and cliente not in B2B_BRANDS:
            a_mover.append((cliente, p))
        else:
            a_dejar.append(p)

    resumen = {
        "total_inicial": len(prospectos),
        "movidos": 0,
        "ya_existian_en_destino": 0,
        "quedan_en_b2b": len(a_dejar),
        "por_cliente": {},
    }

    if not dry_run and a_mover:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup = pipe.PIPELINE_FILE.with_name(f"pipeline.backup.{ts}.json")
        shutil.copy2(pipe.PIPELINE_FILE, backup)
        print(f"Backup: {backup}")

    for cliente, p in a_mover:
        meta_lead_id = p.get("meta_lead_id", "")
        if lc.already_imported(cliente, meta_lead_id):
            resumen["ya_existian_en_destino"] += 1
            resumen["por_cliente"].setdefault(cliente, {"movidos": 0, "ya_existian": 0})["ya_existian"] += 1
            continue

        if dry_run:
            resumen["por_cliente"].setdefault(cliente, {"movidos": 0, "ya_existian": 0})["movidos"] += 1
            resumen["movidos"] += 1
            continue

        lc.add_lead(
            cliente=cliente,
            nombre=p.get("nombre", "Sin nombre"),
            telefono=p.get("telefono", ""),
            email=p.get("email", ""),
            meta_lead_id=meta_lead_id,
            meta_campaign_id=p.get("meta_campaign_id", ""),
            meta_ad_id=p.get("meta_ad_id", ""),
            fuente=p.get("fuente", ""),
            notas=p.get("notas", ""),
        )
        resumen["movidos"] += 1
        resumen["por_cliente"].setdefault(cliente, {"movidos": 0, "ya_existian": 0})["movidos"] += 1

    if not dry_run:
        pipe._save({"prospectos": a_dejar})

    return resumen


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    r = migrate(dry_run=dry)
    print(json.dumps(r, indent=2, ensure_ascii=False))
