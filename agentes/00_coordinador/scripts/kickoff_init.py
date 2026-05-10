"""
kickoff_init.py — Scaffold inicial de un cliente nuevo de DV.

Que hace:
  1. Clona shared/brands/toribio_achaval.json a shared/brands/<cliente>.json
     reseteando los campos cliente-especificos (brand_id, brand_name, positioning,
     meta_ads, references) para que queden como TODO claros.
  2. Crea agentes/02_comercial/data/leads_clientes/<cliente>.json vacio.
  3. Crea shared/state/<cliente>.json minimo.
  4. Devuelve la lista de campos pendientes (TODO_KICKOFF) para completar.
  5. --notify: manda WA a Elias y Nico avisando que el scaffold esta listo.

Lo que NO hace:
  - NO toca Drive (eso es responsabilidad del skill /kickoff con MCP).
  - NO crea ad_account_id ni page_id en Meta (Felipe / Elias).
  - NO completa el formulario CORE (Elias).

Uso:
    python kickoff_init.py <cliente_id> --name "<Brand Display Name>"
    python kickoff_init.py <cliente_id> --name "..." --notify
    python kickoff_init.py <cliente_id> --force      # sobrescribe si ya existe
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEMPLATE = ROOT / "shared" / "brands" / "toribio_achaval.json"
BRANDS_DIR = ROOT / "shared" / "brands"
STATE_DIR = ROOT / "shared" / "state"
LEADS_DIR = ROOT / "agentes" / "02_comercial" / "data" / "leads_clientes"

TODO_MARKER = "<TODO_KICKOFF>"

# Campos que SIEMPRE deben resetearse al clonar (cliente-especificos).
RESET_FIELDS_PATHS = [
    "brand_id",
    "brand_name",
    "brand_tagline",
    "positioning",
    "meta_ads.ad_account_id",
    "meta_ads.page_id",
    "meta_ads.page_name",
    "logo.path",
    "logo.url",
    "references",
]


def _set_path(d: dict, path: str, value):
    parts = path.split(".")
    cur = d
    for p in parts[:-1]:
        if p not in cur or not isinstance(cur[p], dict):
            cur[p] = {}
        cur = cur[p]
    cur[parts[-1]] = value


def _get_path(d: dict, path: str):
    cur = d
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def _reset_brand(brand: dict, cliente_id: str, brand_name: str) -> list[str]:
    """Resetea campos cliente-especificos a TODO. Devuelve lista de paths reseteados."""
    pendings: list[str] = []
    brand["brand_id"] = cliente_id
    brand["brand_name"] = brand_name
    brand["brand_tagline"] = TODO_MARKER
    brand["version"] = "0.1"
    brand["last_updated"] = date.today().isoformat()
    brand["positioning"] = TODO_MARKER
    pendings += ["brand_tagline", "positioning"]

    # meta_ads
    if "meta_ads" not in brand or not isinstance(brand["meta_ads"], dict):
        brand["meta_ads"] = {}
    brand["meta_ads"]["ad_account_id"] = TODO_MARKER
    brand["meta_ads"]["page_id"] = TODO_MARKER
    brand["meta_ads"]["page_name"] = TODO_MARKER
    pendings += ["meta_ads.ad_account_id", "meta_ads.page_id", "meta_ads.page_name"]

    # logo
    if "logo" not in brand or not isinstance(brand["logo"], dict):
        brand["logo"] = {}
    brand["logo"]["path"] = TODO_MARKER
    brand["logo"]["url"] = TODO_MARKER
    pendings += ["logo.path", "logo.url"]

    # references — borrar para que se carguen frescas
    brand["references"] = {}
    pendings.append("references (cargar referencias visuales del cliente)")

    # tone_of_voice queda heredado del template como punto de partida.
    # forbidden_words y preferred_words: explicitamente marcar como base
    tov = brand.setdefault("tone_of_voice", {})
    tov["_kickoff_note"] = (
        "Heredado de toribio_achaval template. Revisar forbidden_words/preferred_words "
        "y ajustar al cliente real antes de validar tono."
    )

    return pendings


def _create_leads_file(cliente_id: str, force: bool) -> Path:
    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    path = LEADS_DIR / f"{cliente_id}.json"
    if path.exists() and not force:
        return path
    payload = {
        "cliente": cliente_id,
        "leads": [],
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _create_state_file(cliente_id: str, force: bool) -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = STATE_DIR / f"{cliente_id}.json"
    if path.exists() and not force:
        return path
    payload = {
        "cliente": cliente_id,
        "fase_actual": 2,
        "fase_nombre": "onboarding",
        "kickoff_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "outputs_count": {},
        "campanas_activas": [],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _notify_team(cliente_id: str, brand_name: str, pendings: list[str]) -> dict:
    """Manda WA a Elias y Nico con resumen del scaffold y TODO list."""
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / "agentes" / "03_delivery_reporting" / ".env")
        sys.path.insert(0, str(ROOT / "agentes" / "03_delivery_reporting" / "scripts"))
        import wa_reportes  # type: ignore

        elias = os.getenv("ELIAS_WA_NUMBER")
        nico = os.getenv("NICO_WA_NUMBER")
        msg = (
            f"[DV] Kickoff iniciado: {brand_name}\n\n"
            f"Brand JSON: shared/brands/{cliente_id}.json (scaffold listo)\n"
            f"Pipeline leads: agentes/02_comercial/data/leads_clientes/{cliente_id}.json\n\n"
            f"Falta completar antes de avanzar:\n"
            + "\n".join(f"- {p}" for p in pendings[:8])
            + ("\n..." if len(pendings) > 8 else "")
            + "\n\nVa para Elias: completar formulario CORE + identidad visual + accesos Meta."
        )
        sent = []
        for n in (elias, nico):
            if n:
                try:
                    wa_reportes.send_text(n, msg)
                    sent.append(n)
                except Exception as e:
                    sent.append(f"FAIL:{n}:{e}")
        return {"sent_to": sent}
    except Exception as e:
        return {"error": str(e)[:200]}


def run(cliente_id: str, brand_name: str, force: bool = False, notify: bool = False) -> dict:
    if not TEMPLATE.exists():
        return {"error": f"template inexistente: {TEMPLATE}"}
    brand_path = BRANDS_DIR / f"{cliente_id}.json"
    if brand_path.exists() and not force:
        return {"error": f"ya existe {brand_path.name}. Usa --force para sobrescribir."}

    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    pendings = _reset_brand(template, cliente_id, brand_name)
    BRANDS_DIR.mkdir(parents=True, exist_ok=True)
    brand_path.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")

    leads_path = _create_leads_file(cliente_id, force)
    state_path = _create_state_file(cliente_id, force)

    notify_result = None
    if notify:
        notify_result = _notify_team(cliente_id, brand_name, pendings)

    return {
        "cliente": cliente_id,
        "brand_name": brand_name,
        "files_created": {
            "brand": str(brand_path.relative_to(ROOT)).replace("\\", "/"),
            "leads": str(leads_path.relative_to(ROOT)).replace("\\", "/"),
            "state": str(state_path.relative_to(ROOT)).replace("\\", "/"),
        },
        "pendings": pendings,
        "notify": notify_result,
        "next_step": (
            "1. Completar TODO_KICKOFF en el brand JSON. "
            "2. Crear estructura Drive 00-05 (skill /kickoff via MCP). "
            "3. Configurar ad_account_id y page_id en Meta. "
            "4. Avisar a Felipe cuando este listo para campanas."
        ),
    }


def _parse_args(argv: list[str]) -> tuple[str, str, bool, bool]:
    if not argv:
        print("uso: kickoff_init.py <cliente_id> --name '<Brand Display>' [--force] [--notify]", file=sys.stderr)
        sys.exit(2)
    cliente_id = argv[0]
    name = cliente_id.replace("_", " ").title()
    force = "--force" in argv
    notify = "--notify" in argv
    if "--name" in argv:
        i = argv.index("--name")
        if i + 1 < len(argv):
            name = argv[i + 1]
    return cliente_id, name, force, notify


def main(argv: list[str]) -> int:
    cliente, name, force, notify = _parse_args(argv)
    r = run(cliente, name, force=force, notify=notify)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if "error" not in r else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
