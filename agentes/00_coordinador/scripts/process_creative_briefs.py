"""
process_creative_briefs.py — Cierra el loop de daily-monitor.

daily-monitor escribe brief_creativo_auto_*.md cuando detecta KILL/fatiga.
Este script escanea esos briefs, notifica a Nico por WA y deja sentinel
.notified para no avisar dos veces.

No genera guiones. La ideacion sigue siendo de Nico (criterio creativo
es el diferencial de DV). Solo cierra la brecha entre "brief escrito"
y "Nico se entera".
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PA_OUT = ROOT / "agentes" / "04_pauta" / "outputs"
DELIVERY_SCRIPTS = ROOT / "agentes" / "03_delivery_reporting" / "scripts"
AUTO_APPROVE = ROOT / ".claude" / "scripts" / "auto_approve.py"


def _ensure_sidecar(brief: Path) -> dict | None:
    """Corre auto_approve sobre el brief si no tiene sidecar. Devuelve el sidecar dict."""
    sidecar = brief.with_suffix(brief.suffix + ".status.json")
    if not sidecar.exists():
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("auto_approve", AUTO_APPROVE)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            cliente = brief.parts[-3] if len(brief.parts) >= 3 else None
            fecha = brief.parts[-2] if len(brief.parts) >= 2 else None
            if cliente and fecha:
                mod.run(cliente, fecha, False)
        except Exception:
            return None
    if not sidecar.exists():
        return None
    try:
        return json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_wa():
    """Reusa wa_reportes (app Reportes) para mandarle a Nico."""
    sys.path.insert(0, str(DELIVERY_SCRIPTS))
    sys.path.insert(0, str(ROOT))
    import wa_reportes  # type: ignore
    return wa_reportes


def _nico_number() -> str | None:
    from dotenv import load_dotenv
    load_dotenv(ROOT / "agentes" / "03_delivery_reporting" / ".env")
    return os.getenv("NICO_WA_NUMBER") or os.getenv("ELIAS_WA_NUMBER")


def _felipe_number() -> str | None:
    from dotenv import load_dotenv
    load_dotenv(ROOT / "agentes" / "03_delivery_reporting" / ".env")
    return os.getenv("FELIPE_WA_NUMBER")


def _extract_summary(brief_path: Path) -> dict:
    """Saca cliente, kills, cpl del brief md."""
    text = brief_path.read_text(encoding="utf-8", errors="ignore")
    cliente = brief_path.parts[-3] if len(brief_path.parts) >= 3 else "?"

    kills = 0
    cpl_avg = ""
    leads = 0
    in_kill = False
    for line in text.splitlines():
        if line.startswith("## Creativos perdedores"):
            in_kill = True
            continue
        if line.startswith("## ") and in_kill:
            in_kill = False
        if in_kill and line.startswith("| ") and "_(ninguno)_" not in line and "Creativo" not in line and "----" not in line:
            kills += 1
        m = re.search(r"CPL promedio: USD ([\d.]+)", line)
        if m:
            cpl_avg = m.group(1)
        m = re.search(r"Leads generados: (\d+)", line)
        if m:
            leads = int(m.group(1))

    return {"cliente": cliente, "kills": kills, "cpl_avg": cpl_avg, "leads": leads}


def _build_message(brief_path: Path, info: dict) -> str:
    rel = brief_path.relative_to(ROOT)
    lines = [
        "[DV] Brief creativo automatico pendiente",
        "",
        f"Cliente: {info['cliente']}",
        f"KILLs detectados: {info['kills']}",
        f"CPL periodo: USD {info['cpl_avg'] or '?'}",
        f"Leads: {info['leads']}",
        "",
        f"Brief: {rel}",
        "",
        "Para procesarlo:",
        "1. cd agentes/01_contenido/creative_director",
        "2. claude",
        "3. /feedback-loop",
        "4. Pasale el path del brief",
        "",
        "Va para Nico.",
    ]
    return "\n".join(lines)


def process(days_back: int = 7, dry_run: bool = False) -> dict:
    """Escanea briefs auto recientes y notifica los no procesados.

    Returns dict con resumen para cron_runner._log.
    """
    if not PA_OUT.exists():
        return {"status": "no_outputs", "briefs": 0}

    cutoff = date.today() - timedelta(days=days_back)
    briefs = []
    for cliente_dir in PA_OUT.iterdir():
        if not cliente_dir.is_dir():
            continue
        for fecha_dir in cliente_dir.iterdir():
            if not fecha_dir.is_dir():
                continue
            try:
                fecha = date.fromisoformat(fecha_dir.name)
            except ValueError:
                continue
            if fecha < cutoff:
                continue
            briefs.extend(fecha_dir.glob("brief_creativo_auto_*.md"))

    notificados = 0
    saltados = 0
    blocked_to_felipe = 0
    errores = []

    wa = None
    nico = _nico_number()
    felipe = _felipe_number()

    for brief in sorted(briefs):
        sentinel = brief.with_suffix(brief.suffix + ".notified")
        if sentinel.exists():
            saltados += 1
            continue

        info = _extract_summary(brief)
        msg = _build_message(brief, info)

        # Gate: si el sidecar marca needs_human (tono fail), no spamear a Nico.
        # Alertar a Felipe que el brief tiene problemas antes de pasarlo.
        sc = _ensure_sidecar(brief)
        brief_blocked = bool(sc and sc.get("status") == "needs_human")

        if dry_run:
            print(f"[DRY] {brief.relative_to(ROOT)} -> {'BLOCKED' if brief_blocked else 'NICO'}")
            print(msg)
            print("---")
            continue

        if brief_blocked:
            if not felipe:
                errores.append(f"{brief.name}: brief con violaciones tono y falta FELIPE_WA_NUMBER")
                continue
            try:
                if wa is None:
                    wa = _load_wa()
                viols = (sc.get("validators", {}).get("tono", {}) or {}).get("violations", [])
                alert = (
                    "[DV] Brief auto BLOQUEADO por tono\n\n"
                    f"Cliente: {info['cliente']}\n"
                    f"Brief: {brief.relative_to(ROOT)}\n"
                    f"Violaciones: {', '.join(viols[:5])}\n\n"
                    "No fue enviado a Nico. Revisar el brief o forbidden_words del brand JSON."
                )
                wa.send_text(felipe, alert)
                sentinel.write_text(
                    f"BLOCKED:{datetime.now(timezone.utc).isoformat(timespec='seconds')}",
                    encoding="utf-8",
                )
                blocked_to_felipe += 1
            except Exception as e:
                errores.append(f"{brief.name}: alerta Felipe fallo: {e}")
            continue

        if not nico:
            errores.append(f"{brief.name}: falta NICO_WA_NUMBER/ELIAS_WA_NUMBER en .env")
            continue

        try:
            if wa is None:
                wa = _load_wa()
            wa.send_text(nico, msg)
            sentinel.write_text(
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                encoding="utf-8",
            )
            notificados += 1
        except Exception as e:
            errores.append(f"{brief.name}: {e}")

    return {
        "briefs_encontrados": len(briefs),
        "notificados": notificados,
        "saltados_ya_notificados": saltados,
        "blocked_to_felipe": blocked_to_felipe,
        "errores": errores,
    }


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    r = process(dry_run=dry)
    print(r)
