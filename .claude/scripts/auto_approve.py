"""
auto_approve.py — Validador batch + auto-aprobacion interna de outputs DV.

Por cada output .md bajo agentes/**/outputs/<cliente>/<fecha>/ sin sidecar,
corre validators (tono + naming + reglas universales) y escribe sidecar
<archivo>.status.json con veredicto.

Uso:
    python .claude/scripts/auto_approve.py                  # todos los clientes, hoy y ayer
    python .claude/scripts/auto_approve.py <cliente>        # un cliente, todas las fechas
    python .claude/scripts/auto_approve.py <cliente> <YYYY-MM-DD>
    python .claude/scripts/auto_approve.py --rerun          # ignora sidecars previos

Sidecar schema (v1):
{
  "schema_version": 1,
  "output_path": "agentes/.../outputs/<cliente>/<fecha>/<file>.md",
  "brand": "<cliente>",
  "validators": {
    "tono":   {"status": "PASS"|"FAIL", "violations": [...]},
    "naming": {"status": "PASS"|"FAIL"|"N/A", "detail": "..."}
  },
  "status": "ready_for_handoff" | "needs_human",
  "approved_at": "<iso8601>",
  "approved_by": "auto-validators-v1",
  "notes": ""
}

Politica:
  - Tono PASS + Naming PASS/N/A  -> ready_for_handoff
  - cualquier FAIL               -> needs_human
  - El sidecar NO marca "aprobado para cliente". Solo handoff INTERNO entre
    agentes DV. Touchpoints con cliente requieren OK humano explicito (ver
    docs/auto_approval_policy.md).

Exit: 0 siempre (no bloquea). Logguea a shared/state/cron_log.jsonl si se
invoca via cron_runner.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import datetime, timezone, date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRANDS_DIR = ROOT / "shared" / "brands"
SCHEMA_VERSION = 1
APPROVER = "auto-validators-v1"

# outputs/ y output/ (design usa singular)
OUTPUT_GLOBS = [
    "agentes/*/outputs/*/*",
    "agentes/*/output/*/*",
    "agentes/*/*/outputs/*/*",
    "agentes/*/*/output/*/*",
]

NAMING_BIN_RE = re.compile(
    r"^[A-Za-z0-9]+_[A-Za-z0-9]+_V\d+\.(mp4|png|jpg|jpeg|pdf)$",
    re.IGNORECASE,
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _strip(s: str) -> str:
    s = s.lower()
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def _load_brand(cliente: str) -> dict | None:
    p = BRANDS_DIR / f"{cliente}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _check_forbidden(text: str, forbidden: list[str]) -> list[str]:
    norm = _strip(text)
    return [w for w in forbidden if _strip(w) in norm]


def _resolve_brand_and_date(path: Path) -> tuple[str | None, str | None]:
    """
    De un path tipo agentes/01_contenido/copywritter/outputs/<cliente>/<fecha>/file.md
    devuelve (cliente, fecha). Tolera 'outputs' u 'output'.
    """
    parts = path.parts
    for i, p in enumerate(parts):
        if p in ("outputs", "output") and i + 2 < len(parts):
            cliente = parts[i + 1]
            fecha = parts[i + 2]
            if DATE_RE.match(fecha):
                return cliente, fecha
    return None, None


def _validate_md(md_path: Path, brand: dict | None) -> dict:
    """Valida un .md: forbidden_words. Devuelve dict con status + violations."""
    if not brand:
        return {"status": "FAIL", "violations": ["brand JSON inexistente"]}
    tov = brand.get("tone_of_voice") or {}
    forbidden = tov.get("forbidden_words") or brand.get("forbidden_words") or []
    if not forbidden:
        return {"status": "PASS", "violations": [], "note": "brand sin forbidden_words"}
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception as e:
        return {"status": "FAIL", "violations": [f"read error: {e}"]}
    hits = _check_forbidden(text, forbidden)
    if hits:
        return {"status": "FAIL", "violations": hits}
    return {"status": "PASS", "violations": []}


def _validate_naming(path: Path) -> dict:
    """Naming aplica solo a binarios. .md no requiere naming Drive."""
    if path.suffix.lower() not in (".mp4", ".png", ".jpg", ".jpeg", ".pdf"):
        return {"status": "N/A", "detail": "no aplica naming Drive"}
    if NAMING_BIN_RE.match(path.name):
        return {"status": "PASS", "detail": "match <CLIENTE>_<TipoContenido>_V<n>.<ext>"}
    return {"status": "FAIL", "detail": "no respeta <CLIENTE>_<TipoContenido>_V<n>.<ext>"}


def _sidecar_path(p: Path) -> Path:
    return p.with_suffix(p.suffix + ".status.json")


def _process_file(p: Path, rerun: bool) -> dict | None:
    sidecar = _sidecar_path(p)
    if sidecar.exists() and not rerun:
        return None  # ya validado

    cliente, _fecha = _resolve_brand_and_date(p)
    if not cliente:
        return None

    brand = _load_brand(cliente)

    is_md = p.suffix.lower() == ".md"
    tono = _validate_md(p, brand) if is_md else {"status": "N/A", "violations": []}
    naming = _validate_naming(p)

    bad = tono["status"] == "FAIL" or naming["status"] == "FAIL"
    status = "needs_human" if bad else "ready_for_handoff"

    record = {
        "schema_version": SCHEMA_VERSION,
        "output_path": str(p.relative_to(ROOT)).replace("\\", "/"),
        "brand": cliente,
        "validators": {"tono": tono, "naming": naming},
        "status": status,
        "approved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "approved_by": APPROVER,
        "notes": "",
    }
    sidecar.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def _candidate_files(cliente_filter: str | None, fecha_filter: str | None) -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for pat in OUTPUT_GLOBS:
        for p in ROOT.glob(pat + "/*"):
            if not p.is_file():
                continue
            if p.suffix.lower() == ".json" and p.name.endswith(".status.json"):
                continue
            if p.suffix.lower() not in (".md", ".mp4", ".png", ".jpg", ".jpeg", ".pdf"):
                continue
            if p in seen:
                continue
            cliente, fecha = _resolve_brand_and_date(p)
            if not cliente:
                continue
            if cliente_filter and cliente != cliente_filter:
                continue
            if fecha_filter and fecha != fecha_filter:
                continue
            seen.add(p)
            out.append(p)
    return out


def run(cliente: str | None = None, fecha: str | None = None, rerun: bool = False) -> dict:
    files = _candidate_files(cliente, fecha)
    processed = 0
    ready = 0
    needs_human = 0
    flagged: list[dict] = []
    for p in files:
        rec = _process_file(p, rerun=rerun)
        if rec is None:
            continue
        processed += 1
        if rec["status"] == "ready_for_handoff":
            ready += 1
        else:
            needs_human += 1
            flagged.append({
                "path": rec["output_path"],
                "brand": rec["brand"],
                "tono": rec["validators"]["tono"],
                "naming": rec["validators"]["naming"],
            })
    return {
        "candidates": len(files),
        "processed": processed,
        "ready_for_handoff": ready,
        "needs_human": needs_human,
        "flagged": flagged[:20],
    }


def _parse_args(argv: list[str]) -> tuple[str | None, str | None, bool]:
    rerun = "--rerun" in argv
    args = [a for a in argv if a != "--rerun"]
    cliente = args[0] if args else None
    fecha = args[1] if len(args) > 1 else None
    if fecha and not DATE_RE.match(fecha):
        print(f"fecha invalida: {fecha} (esperado YYYY-MM-DD)", file=sys.stderr)
        sys.exit(2)
    return cliente, fecha, rerun


def main(argv: list[str]) -> int:
    cliente, fecha, rerun = _parse_args(argv)
    # default: si no se pasa nada, barre hoy + ayer (ventana corta para cron)
    if cliente is None and fecha is None:
        today = date.today()
        yest = today - timedelta(days=1)
        agg = {"candidates": 0, "processed": 0, "ready_for_handoff": 0, "needs_human": 0, "flagged": []}
        for d in (today.isoformat(), yest.isoformat()):
            r = run(None, d, rerun)
            for k in ("candidates", "processed", "ready_for_handoff", "needs_human"):
                agg[k] += r[k]
            agg["flagged"].extend(r["flagged"])
        print(json.dumps(agg, ensure_ascii=False, indent=2))
        return 0
    r = run(cliente, fecha, rerun)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
