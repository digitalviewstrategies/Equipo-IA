"""
lead_prescore.py — Pre-scoring automatico de leads del pipeline DV Comercial.

NO reemplaza el scorecard de 41 puntos (eso requiere discovery call con humano).
Lo que hace:
  - Para leads en etapa `pre_filtro`, agrega:
      prescore_source: "meta_lead_ads" | "csv_frio" | "manual" | "desconocido"
      prescore_priority: 1 (urgente <24h) | 2 (<48h) | 3 (<72h) | "stale" (>72h)
      prescore_red_flags: lista de red flags detectados desde notas/campos
      prescore_knockouts: lista de knockouts auto-detectados
      prescore_at: iso ts
  - NO toca: etapa, puntaje_scorecard, clasificacion (esos son territorio del
    skill /calificar manual).

Uso:
    python agentes/02_comercial/scripts/lead_prescore.py             # corre sobre pipeline.json
    python agentes/02_comercial/scripts/lead_prescore.py --dry-run   # no escribe

Idempotente: re-procesa leads ya prescoreados solo si su prioridad cambia
(ventana de tiempo se mueve), no toca el resto.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PIPELINE = ROOT / "agentes" / "02_comercial" / "data" / "pipeline.json"

# Heuristica simple sobre notas. Los red flags duros estan en
# context/icp_y_scoring.md, esta lista cubre los detectables por texto.
RED_FLAG_PATTERNS = [
    (r"\b30\s*d[ií]as\b", "Quiere resultados en 30 dias o menos"),
    (r"solo\s+(el\s+)?(contenido\s+)?org[aá]nic", "No quiere invertir en pauta"),
    (r"community\s*management", "Busca community management"),
    (r"gesti[oó]n\s+de\s+redes", "Busca gestion de redes generica"),
    (r"garant[ií]a.*ventas", "Pide garantia de ventas especificas"),
    (r"segunda\s+actividad", "Inmobiliario es actividad secundaria"),
    (r"no\s+tengo\s+tiempo", "No tiene tiempo para revisar contenido"),
]

KNOCKOUT_PATTERNS = [
    (r"\bzona\s*:\s*(?:interior|cordoba|mendoza|rosario|tucum)", "Fuera de CABA/GBA"),
    (r"presupuesto\s*:\s*(?:0|<\s*800|menor)", "Presupuesto pauta < USD 800/mes"),
]


def _norm(s: str) -> str:
    return (s or "").lower()


def _parse_ingreso(p: dict) -> datetime | None:
    """Trata de extraer timestamp del lead. Prioriza fecha_ingreso, sino notas."""
    f = p.get("fecha_ingreso")
    if f:
        try:
            return datetime.fromisoformat(f).replace(tzinfo=timezone.utc)
        except Exception:
            pass
    # Fallback: parsear "created=2026-05-06T10:12:25+0000" del nota
    notas = p.get("notas") or ""
    m = re.search(r"created=([0-9T:+\-]+)", notas)
    if m:
        try:
            return datetime.fromisoformat(m.group(1).replace("+0000", "+00:00"))
        except Exception:
            pass
    return None


def _priority(ingreso: datetime | None, etapa: str) -> str | int:
    """1 = urgente, 2/3 = backlog, 'stale' = abandonado."""
    if etapa not in ("pre_filtro", "fit_call"):
        return 0  # ya esta siendo trabajado
    if not ingreso:
        return 2
    age = (datetime.now(timezone.utc) - ingreso).total_seconds() / 3600.0
    if age < 24:
        return 1
    if age < 48:
        return 2
    if age < 72:
        return 3
    return "stale"


def _detect_source(p: dict) -> str:
    fuente = _norm(p.get("fuente", ""))
    if fuente.startswith("meta_lead_ads"):
        return "meta_lead_ads"
    if "csv" in fuente or fuente.startswith("csv"):
        return "csv_frio"
    if fuente:
        return "manual"
    return "desconocido"


def _detect_red_flags(p: dict) -> list[str]:
    text = " ".join([_norm(p.get(k, "")) for k in ("notas", "empresa", "nombre")])
    found = []
    for pat, label in RED_FLAG_PATTERNS:
        if re.search(pat, text):
            found.append(label)
    return found


def _detect_knockouts(p: dict) -> list[str]:
    text = " ".join([_norm(p.get(k, "")) for k in ("notas", "empresa")])
    zona = _norm(p.get("zona", ""))
    found = []
    if zona and zona not in ("caba", "gba_norte", "desconocida", ""):
        found.append(f"Zona declarada fuera de CABA/GBA Norte: {p.get('zona')}")
    for pat, label in KNOCKOUT_PATTERNS:
        if re.search(pat, text):
            found.append(label)
    return found


def _process(p: dict) -> tuple[dict, bool]:
    """Devuelve (prospecto_actualizado, cambio?). Idempotente: solo escribe si difiere."""
    etapa = p.get("etapa", "")
    if etapa not in ("pre_filtro", "fit_call"):
        return p, False

    ingreso = _parse_ingreso(p)
    new = {
        "prescore_source": _detect_source(p),
        "prescore_priority": _priority(ingreso, etapa),
        "prescore_red_flags": _detect_red_flags(p),
        "prescore_knockouts": _detect_knockouts(p),
        "prescore_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    changed = False
    for k, v in new.items():
        if k == "prescore_at":
            continue
        if p.get(k) != v:
            changed = True
            break
    if changed:
        p.update(new)
    else:
        # solo refrescar timestamp si nada cambio? No, mantenemos original para idempotencia.
        pass
    return p, changed


def run(dry_run: bool = False) -> dict:
    if not PIPELINE.exists():
        return {"status": "no_pipeline", "processed": 0}
    data = json.loads(PIPELINE.read_text(encoding="utf-8"))
    prospectos = data.get("prospectos", [])
    changed = 0
    by_priority = {1: 0, 2: 0, 3: 0, "stale": 0, 0: 0}
    knockouts_total = 0
    flags_total = 0
    for p in prospectos:
        p, ch = _process(p)
        if ch:
            changed += 1
        pr = p.get("prescore_priority", 0)
        if pr in by_priority:
            by_priority[pr] += 1
        knockouts_total += len(p.get("prescore_knockouts", []) or [])
        flags_total += len(p.get("prescore_red_flags", []) or [])
    if changed and not dry_run:
        PIPELINE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "total": len(prospectos),
        "updated": changed,
        "by_priority": {str(k): v for k, v in by_priority.items()},
        "knockouts_detected": knockouts_total,
        "red_flags_detected": flags_total,
        "dry_run": dry_run,
    }


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    r = run(dry_run=dry)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
