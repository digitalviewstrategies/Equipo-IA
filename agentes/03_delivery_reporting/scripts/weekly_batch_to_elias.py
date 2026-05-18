"""
weekly_batch_to_elias.py — Orquestador semanal de reportes para el account manager.

Modelo: AUTO → ELIAS → (reenvío manual a clientes).

Recorre todos los clientes con brand JSON, genera el reporte semanal de cada uno
(Meta → PDF → Drive) reutilizando weekly_report_deliver.deliver(), y le manda a
Elias UN mensaje template aprobado por cliente con el link al PDF, más un digest
de texto plano consolidado (si la ventana de 24hs está abierta).

NO manda nada a los clientes. Elias revisa y reenvía a mano. Esto respeta la
regla de oro de DV: "no mandás el reporte directamente al cliente".

Uso:
    python scripts/weekly_batch_to_elias.py            # todos los clientes
    python scripts/weekly_batch_to_elias.py --only digital_view abitat_puertos
    python scripts/weekly_batch_to_elias.py --dry-run  # genera pero no manda WA
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

DELIVERY_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
BRANDS_DIR = REPO_ROOT / "shared" / "brands"
LOG_PATH = DELIVERY_ROOT / "outputs" / "_weekly_batch.log"

sys.path.insert(0, str(DELIVERY_ROOT / "scripts"))


def _log(msg: str) -> None:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def list_clientes() -> list[str]:
    return sorted(
        f.stem for f in BRANDS_DIR.glob("*.json") if not f.stem.startswith("_")
    )


def _fmt_money(v) -> str:
    try:
        return f"USD {float(v):,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    except (TypeError, ValueError):
        return "USD -"


def run(only: list[str] | None = None, dry_run: bool = False) -> dict:
    from weekly_report_deliver import deliver
    from wa_reportes import send_to_elias, send_reporte_semanal_template, ELIAS_WA_NUMBER

    clientes = only or list_clientes()
    delivered: list[dict] = []
    skipped: list[dict] = []
    failed: list[dict] = []

    for cliente in clientes:
        try:
            # send_wa=False: el orquestador maneja el envío a Elias, no a cada cliente.
            r = deliver(cliente, send_wa=False, upload=not dry_run)
        except Exception as e:  # noqa: BLE001
            failed.append({"cliente": cliente, "error": str(e)[:300]})
            _log(f"FAIL cliente={cliente} error={str(e)[:200]}")
            continue

        status = r.get("status")
        if status == "skip":
            skipped.append({"cliente": cliente, "reason": r.get("reason")})
            _log(f"SKIP cliente={cliente} reason={r.get('reason')}")
            continue
        if status != "ok":
            failed.append({"cliente": cliente, "error": r.get("error") or status})
            _log(f"FAIL cliente={cliente} status={status} error={r.get('error')}")
            continue

        delivered.append(r)
        _log(
            f"GENERATED cliente={cliente} periodo={r.get('periodo')} "
            f"drive={r.get('pdf_share_url')}"
        )

    # --- Envío a Elias: un template aprobado por cliente (funciona fuera de 24hs) ---
    if not dry_run and ELIAS_WA_NUMBER:
        for r in delivered:
            url = r.get("pdf_share_url")
            if not url:
                _log(f"WARN cliente={r['cliente']} sin pdf_share_url, no se manda a Elias")
                continue
            try:
                resp = send_reporte_semanal_template(
                    ELIAS_WA_NUMBER, "Elias", url
                )
                r["wa_to_elias"] = resp
                _log(f"SENT_TO_ELIAS cliente={r['cliente']} url={url}")
            except Exception as e:  # noqa: BLE001
                r["wa_to_elias"] = {"error": str(e)[:300]}
                _log(f"WA_FAIL cliente={r['cliente']} error={str(e)[:200]}")

        # Digest de texto plano (solo entra si la ventana de 24hs está abierta).
        digest = _build_digest(delivered, skipped, failed)
        try:
            send_to_elias(digest)
            _log("DIGEST_SENT")
        except Exception as e:  # noqa: BLE001
            _log(f"DIGEST_SKIP (ventana 24hs cerrada o error): {str(e)[:160]}")

    summary = {
        "ran_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "delivered": [
            {
                "cliente": r["cliente"],
                "periodo": r.get("periodo"),
                "pdf_share_url": r.get("pdf_share_url"),
                "leads": (r.get("metrics") or {}).get("leads"),
                "cpl": (r.get("metrics") or {}).get("cpl"),
            }
            for r in delivered
        ],
        "skipped": skipped,
        "failed": failed,
        "dry_run": dry_run,
    }
    _log(
        f"DONE delivered={len(delivered)} skipped={len(skipped)} "
        f"failed={len(failed)} dry_run={dry_run}"
    )
    return summary


def _build_digest(delivered: list[dict], skipped: list[dict], failed: list[dict]) -> str:
    hoy = date.today().strftime("%d/%m/%Y")
    lines = [f"Reportes semanales listos — {hoy}", ""]
    if delivered:
        lines.append(f"{len(delivered)} reporte(s) generado(s). Revisá y reenviá:")
        for r in delivered:
            m = r.get("metrics") or {}
            leads = m.get("leads", "-")
            cpl = _fmt_money(m.get("cpl")) if m.get("cpl") is not None else "CPL -"
            lines.append(
                f"- {r.get('cliente_display') or r['cliente']}: "
                f"{leads} consultas, {cpl}. Te llegó el PDF aparte."
            )
    else:
        lines.append("No se generó ningún reporte esta semana.")
    if skipped:
        lines.append("")
        lines.append("Sin actividad (no se reportan): " + ", ".join(s["cliente"] for s in skipped))
    if failed:
        lines.append("")
        lines.append("Con error (revisar): " + ", ".join(f["cliente"] for f in failed))
    lines.append("")
    lines.append("Cada PDF te llegó como mensaje aparte con el link de Drive.")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Orquestador semanal de reportes a Elias")
    ap.add_argument("--only", nargs="*", help="Lista de clientes (default: todos)")
    ap.add_argument("--dry-run", action="store_true", help="Genera pero no sube ni manda WA")
    args = ap.parse_args(argv)

    summary = run(only=args.only, dry_run=args.dry_run)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if not summary["failed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
