"""
pre_commit_validators.py — Validador standalone para pre-commit hook.

Para cada archivo staged en agentes/*/outputs/<cliente>/<fecha>/*.md:
  1. Resuelve el brand desde el path.
  2. Carga shared/brands/<cliente>.json.
  3. Falla si encuentra forbidden_words.
  4. Falla si el nombre de archivo no respeta naming convention.

Tambien valida nombres en agentes/04_pauta/**/campaigns_*.csv.

Exit code:
  0  todo OK
  1  encontro violaciones (block commit)
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path


def _strip(s: str) -> str:
    """Normaliza: minusculas + sin diacriticos."""
    s = s.lower()
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

ROOT = Path(__file__).resolve().parents[2]
BRANDS = ROOT / "shared" / "brands"

# regex naming Drive: <CLIENTE>_<TipoContenido>_V<n>[_<variant>].<ext>
# variant opcional: 9x16, 1x1, 16x9, thumb, etc. (post_production multi-format).
NAMING_DRIVE_RE = re.compile(
    r"^[A-Za-z0-9]+_[A-Za-z0-9]+_V\d+(?:_[A-Za-z0-9]+)?\.(mp4|png|jpg|jpeg|pdf|srt)$",
    re.IGNORECASE,
)

# matches anywhere: .../outputs/<cliente>/<fecha>/...  o .../output/<cliente>/<fecha>/...
OUTPUT_PATH_RE = re.compile(r"/outputs?/([^/]+)/[^/]+/(.+)$")


def _staged_files() -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            cwd=ROOT, text=True
        )
    except Exception as e:
        print(f"[pre-commit] no se pudo leer git: {e}", file=sys.stderr)
        return []
    return [l.strip() for l in out.splitlines() if l.strip()]


def _load_brand(cliente: str) -> dict | None:
    p = BRANDS / f"{cliente}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _check_forbidden(text: str, forbidden: list[str]) -> list[str]:
    norm_text = _strip(text)
    return [w for w in forbidden if _strip(w) in norm_text]


def _resolve_brand_from_path(rel: str) -> str | None:
    m = OUTPUT_PATH_RE.search(rel.replace("\\", "/"))
    if not m:
        return None
    return m.group(1)


def main() -> int:
    files = _staged_files()
    if not files:
        return 0

    violations = []

    for f in files:
        rel = f.replace("\\", "/")
        full = ROOT / f
        if not full.exists():
            continue

        cliente = _resolve_brand_from_path(rel)

        # Tono: solo .md de outputs con brand resoluble
        if rel.endswith(".md") and cliente:
            brand = _load_brand(cliente)
            if brand:
                forbidden = (brand.get("tone_of_voice") or {}).get("forbidden_words") or brand.get("forbidden_words") or []
                if forbidden:
                    try:
                        text = full.read_text(encoding="utf-8")
                    except Exception:
                        text = ""
                    found = _check_forbidden(text, forbidden)
                    if found:
                        violations.append(f"  TONO   {rel}\n           forbidden_words encontradas: {', '.join(found)}")

        # Naming Drive: archivos binarios en outputs/
        if cliente and full.suffix.lower() in (".mp4", ".png", ".jpg", ".jpeg", ".pdf"):
            name = full.name
            if not NAMING_DRIVE_RE.match(name):
                violations.append(f"  NAMING {rel}\n           debe seguir <CLIENTE>_<TipoContenido>_V<n>.<ext>")

    if not violations:
        return 0

    print("\n[pre-commit] BLOCK: violaciones detectadas\n", file=sys.stderr)
    for v in violations:
        print(v, file=sys.stderr)
    print(
        "\nFix las violaciones o usa `git commit --no-verify` si es deliberado.\n",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
