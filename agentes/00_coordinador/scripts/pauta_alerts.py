"""pauta_alerts.py — Notifica a Felipe por WA cuando daily-monitor detecta KILL/fatiga.

Se invoca al final de cron_runner.daily_monitor(). Recibe lista de resumenes
por cliente (`[{cliente, status, kills, fatiga}]`) y manda un solo WA a Felipe
si hay al menos un cliente con status=alerta.

Patron: mismo que lead_alerts. Reusa wa_reportes (app Reportes).
Fail-open: si falla el WA, NO rompe el cron.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DELIVERY_SCRIPTS = ROOT / "agentes" / "03_delivery_reporting" / "scripts"


def _load_wa():
    sys.path.insert(0, str(DELIVERY_SCRIPTS))
    sys.path.insert(0, str(ROOT))
    import wa_reportes  # type: ignore
    return wa_reportes


def _destinatario() -> str | None:
    from dotenv import load_dotenv
    load_dotenv(ROOT / "agentes" / "03_delivery_reporting" / ".env")
    return os.getenv("FELIPE_WA_NUMBER")


def _build_message(resumen: list[dict]) -> str:
    alertas = [r for r in resumen if r.get("status") == "alerta"]
    alertas.sort(key=lambda r: -(r.get("kills", 0) + r.get("fatiga", 0)))

    total_kills = sum(r.get("kills", 0) for r in alertas)
    total_fatiga = sum(r.get("fatiga", 0) for r in alertas)

    lines = [f"[DV] {len(alertas)} cliente(s) con creativos para revisar hoy", ""]
    for r in alertas:
        k = r.get("kills", 0)
        f = r.get("fatiga", 0)
        partes = []
        if k:
            partes.append(f"{k} KILL/ITERATE")
        if f:
            partes.append(f"{f} con fatiga")
        lines.append(f"- {r['cliente']}: {', '.join(partes)}")

    lines += [
        "",
        f"Total: {total_kills} ads a revisar, {total_fatiga} con frequency >= 3.0.",
        "Brief auto + alerta_daily.md en outputs/04_pauta. Va para Felipe.",
    ]
    return "\n".join(lines)


def notify(resumen: list[dict], dry_run: bool = False) -> dict:
    alertas = [r for r in (resumen or []) if r.get("status") == "alerta"]
    if not alertas:
        return {"status": "skip", "reason": "sin_alertas"}

    dest = _destinatario()
    if not dest:
        return {"status": "error", "reason": "falta_FELIPE_WA_NUMBER"}

    msg = _build_message(resumen)
    if dry_run:
        return {"status": "dry_run", "to": dest, "preview": msg}

    try:
        wa = _load_wa()
        wa.send_text(dest, msg)
        return {"status": "ok", "to": dest, "alertas": len(alertas)}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:200]}


if __name__ == "__main__":
    fake = [
        {"cliente": "lopez_props", "status": "alerta", "kills": 2, "fatiga": 1},
        {"cliente": "toribio_achaval", "status": "alerta", "kills": 1, "fatiga": 0},
        {"cliente": "ini_propiedades", "status": "ok", "ads": 8},
        {"cliente": "abitat", "status": "sin_insights"},
    ]
    print(notify(fake, dry_run="--dry-run" in sys.argv))
