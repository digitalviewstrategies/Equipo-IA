"""
Resuelve el brand_id activo para la sesion.

Orden:
1. .claude/state/active_client (archivo de una linea con el brand_id).
2. Inferencia desde el cwd: si cwd contiene .../outputs/<brand_id>/... y existe shared/brands/<brand_id>.json, devuelve ese brand_id.
3. Vacio (caller decide).

Uso CLI:
    python .claude/scripts/resolve_active_client.py            -> imprime brand_id o nada
    python .claude/scripts/resolve_active_client.py --set X    -> escribe X en state/active_client
    python .claude/scripts/resolve_active_client.py --clear    -> borra state/active_client
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = REPO_ROOT / ".claude" / "state" / "active_client"
BRANDS_DIR = REPO_ROOT / "shared" / "brands"


def list_brand_ids() -> list[str]:
    if not BRANDS_DIR.exists():
        return []
    return [p.stem for p in BRANDS_DIR.glob("*.json") if not p.stem.startswith("_")]


def from_state_file() -> str:
    if not STATE_FILE.exists():
        return ""
    val = STATE_FILE.read_text(encoding="utf-8").strip()
    if val and (BRANDS_DIR / f"{val}.json").exists():
        return val
    return ""


def from_cwd() -> str:
    cwd = Path.cwd().as_posix()
    valid = set(list_brand_ids())
    m = re.search(r"/outputs/([^/]+)/", cwd)
    if m and m.group(1) in valid:
        return m.group(1)
    return ""


def resolve() -> str:
    return from_state_file() or from_cwd() or ""


def set_active(brand_id: str) -> None:
    valid = list_brand_ids()
    if brand_id not in valid:
        print(f"Brand desconocida: {brand_id}. Validas: {', '.join(valid)}", file=sys.stderr)
        sys.exit(1)
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(brand_id + "\n", encoding="utf-8")
    print(brand_id)


def clear() -> None:
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(resolve())
        return
    if args[0] == "--set" and len(args) == 2:
        set_active(args[1])
        return
    if args[0] == "--clear":
        clear()
        return
    if args[0] == "--list":
        print("\n".join(list_brand_ids()))
        return
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
