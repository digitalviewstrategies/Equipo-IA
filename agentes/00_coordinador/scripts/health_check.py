"""
health_check.py — Verifica que el cron este vivo.

Lee shared/state/cron_log.jsonl. Para cada tarea esperada chequea que
haya corrido OK dentro del SLA. Si no, manda WA a Felipe.

SLA por tarea (horas desde ultima ejecucion ok):
    recompute-state         : 12
    daily-monitor           : 36
    weekly-report           : 192   (8 dias — corre lunes)
    pull-leads              : 8
    process-creative-briefs : 36
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOG = ROOT / "shared" / "state" / "cron_log.jsonl"
DELIVERY_SCRIPTS = ROOT / "agentes" / "03_delivery_reporting" / "scripts"

SLA_HOURS = {
    "recompute-state": 12,
    "daily-monitor": 36,
    "weekly-report": 192,
    "pull-leads": 8,
    "process-creative-briefs": 36,
}


def _load_log() -> list[dict]:
    if not LOG.exists():
        return []
    out = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _last_ok(entries: list[dict], task: str) -> datetime | None:
    for e in reversed(entries):
        if e.get("task") == task and e.get("status") == "ok":
            try:
                return datetime.fromisoformat(e["ts"])
            except Exception:
                continue
    return None


def _send_alert(body: str) -> None:
    sys.path.insert(0, str(DELIVERY_SCRIPTS))
    sys.path.insert(0, str(ROOT))
    from dotenv import load_dotenv
    load_dotenv(ROOT / "agentes" / "03_delivery_reporting" / ".env")
    felipe = os.getenv("FELIPE_WA_NUMBER")
    if not felipe:
        print(f"[ALERT NO WA] {body}")
        return
    import wa_reportes  # type: ignore
    wa_reportes.send_text(felipe, body)


def check() -> dict:
    entries = _load_log()
    now = datetime.now(timezone.utc)
    stale = []
    ok = []

    for task, sla in SLA_HOURS.items():
        last = _last_ok(entries, task)
        if last is None:
            stale.append({"task": task, "last_ok": None, "hours": None})
            continue
        hours = (now - last).total_seconds() / 3600
        if hours > sla:
            stale.append({"task": task, "last_ok": last.isoformat(), "hours": round(hours, 1), "sla": sla})
        else:
            ok.append({"task": task, "hours": round(hours, 1)})

    if stale:
        lines = ["[DV] Cron health: tareas atrasadas", ""]
        for s in stale:
            if s["last_ok"] is None:
                lines.append(f"- {s['task']}: nunca corrio OK")
            else:
                lines.append(f"- {s['task']}: hace {s['hours']}h (SLA {s['sla']}h)")
        lines.append("")
        lines.append("Revisa Task Scheduler en la PC.")
        _send_alert("\n".join(lines))

    return {"stale": stale, "ok_count": len(ok)}


if __name__ == "__main__":
    print(check())
