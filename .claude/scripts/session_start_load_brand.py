"""
Hook SessionStart: imprime un resumen compacto de la brand activa para que Claude
arranque la sesion con el contexto cargado, sin tener que re-leer el JSON entero.

Salida via stdout en formato JSON con hookSpecificOutput.additionalContext.

Si no hay brand activa resoluble, imprime un mensaje neutro y exit 0 (no bloquea).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / ".claude" / "scripts"))

from resolve_active_client import resolve, BRANDS_DIR  # noqa: E402


def build_context(brand_id: str) -> str:
    json_path = BRANDS_DIR / f"{brand_id}.json"
    if not json_path.exists():
        return f"[active_client] {brand_id} (sin JSON encontrado en shared/brands/)"
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        return f"[active_client] {brand_id} (JSON ilegible: {e})"

    tov = data.get("tone_of_voice", {})
    principles = tov.get("principles", [])
    forbidden = tov.get("forbidden_words", [])
    preferred = tov.get("preferred_words", [])

    lines = [
        f"# Brand activa: {data.get('brand_name', brand_id)} ({brand_id})",
        f"Fuente: shared/brands/{brand_id}.json",
        "",
        f"**Posicionamiento:** {data.get('positioning', '—')}",
        "",
        "**Tono — principios:**",
    ]
    lines += [f"- {p}" for p in principles[:10]]
    if forbidden:
        lines += ["", "**Forbidden words (no usar):** " + ", ".join(forbidden)]
    if preferred:
        lines += ["", "**Preferred words (usar):** " + ", ".join(preferred)]
    lines += [
        "",
        "Validacion de tono: tono-brand-validator lee este JSON dinamicamente.",
        "Para cambiar la brand activa: `python .claude/scripts/resolve_active_client.py --set <brand_id>`",
    ]
    return "\n".join(lines)


def main() -> None:
    brand_id = resolve()
    if not brand_id:
        ctx = (
            "[active_client] Sin brand activa. "
            "Seteala con: python .claude/scripts/resolve_active_client.py --set <brand_id>. "
            "Listar brands: python .claude/scripts/resolve_active_client.py --list"
        )
    else:
        ctx = build_context(brand_id)

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": ctx,
        }
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
