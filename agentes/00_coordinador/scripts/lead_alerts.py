"""lead_alerts.py — Notifica a Elias por WA cuando llegan leads nuevos.

Se invoca al final de cron_runner.pull_leads(). Recibe el resumen del puller
(estructura `{prospectos_nuevos, por_cliente: {cliente: {status, nuevos}}}`) y
envia un solo mensaje WA a Elias con el desglose por cliente.

Idempotencia: corre por ejecucion del cron; cada corrida con leads nuevos
manda un mensaje. No spam: si prospectos_nuevos == 0, return silencioso.

Reusa wa_reportes (app Reportes, mismo cliente que process-creative-briefs).
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
    # Prioridad: ELIAS (PM relaciones con clientes) -> FELIPE como fallback
    return os.getenv("ELIAS_WA_NUMBER") or os.getenv("FELIPE_WA_NUMBER")


def _build_message(resumen: dict) -> str:
    total = resumen.get("prospectos_nuevos", 0)
    por_cliente = resumen.get("por_cliente", {}) or {}

    nuevos_por_cliente = [
        (c, info.get("nuevos", 0))
        for c, info in por_cliente.items()
        if isinstance(info, dict) and info.get("nuevos", 0) > 0
    ]
    nuevos_por_cliente.sort(key=lambda x: -x[1])

    plural = "leads nuevos" if total != 1 else "lead nuevo"
    lines = [f"[DV] {total} {plural} en Meta", ""]
    for cliente, n in nuevos_por_cliente:
        lines.append(f"- {cliente}: {n}")
    lines += [
        "",
        "Cargados al pipeline. Pasan por prescore automatico en el proximo run.",
    ]
    return "\n".join(lines)


def notify(resumen: dict, dry_run: bool = False) -> dict:
    total = resumen.get("prospectos_nuevos", 0)
    if total <= 0:
        return {"status": "skip", "reason": "sin_leads_nuevos"}

    dest = _destinatario()
    if not dest:
        return {"status": "error", "reason": "falta_ELIAS_WA_NUMBER_o_FELIPE_WA_NUMBER"}

    msg = _build_message(resumen)
    if dry_run:
        return {"status": "dry_run", "to": dest, "preview": msg}

    try:
        wa = _load_wa()
        wa.send_text(dest, msg)
        return {"status": "ok", "to": dest, "total": total}
    except Exception as e:
        return {"status": "error", "reason": str(e)[:200]}


if __name__ == "__main__":
    # Smoke manual con resumen fake
    fake = {
        "prospectos_nuevos": 7,
        "por_cliente": {
            "lopez_props": {"status": "ok", "nuevos": 4},
            "toribio_achaval": {"status": "ok", "nuevos": 3},
            "ini_propiedades": {"status": "ok", "nuevos": 0},
        },
    }
    print(notify(fake, dry_run="--dry-run" in sys.argv))
