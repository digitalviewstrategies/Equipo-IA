"""
state_manager.py — Estado operativo por cliente, derivado del filesystem.

No edita estado a mano: lo recomputa escaneando outputs de cada agente.
Persiste un snapshot en shared/state/<cliente>.json para consumo rapido del
coordinador y para tracking historico.

Uso CLI:
    python state_manager.py <cliente>             # imprime estado
    python state_manager.py <cliente> --json      # JSON puro
    python state_manager.py --all                 # todos los clientes
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SHARED = ROOT / "shared"
BRANDS = SHARED / "brands"
STATE_DIR = SHARED / "state"

CD_OUT = ROOT / "agentes" / "01_contenido" / "creative_director" / "outputs"
CW_OUT = ROOT / "agentes" / "01_contenido" / "copywritter" / "outputs"
DS_OUT = ROOT / "agentes" / "01_contenido" / "design" / "output"
PA_OUT = ROOT / "agentes" / "04_pauta" / "outputs"


GATES_ORDER = [
    "1_comercial",
    "2_onboarding",
    "3_preproduccion",
    "4_produccion",
    "5_pauta",
    "6_lanzamiento",
]


def _count_glob(path: Path, pattern: str) -> int:
    if not path.exists():
        return 0
    return sum(1 for _ in path.rglob(pattern))


def _has_brand(cliente: str) -> bool:
    return (BRANDS / f"{cliente}.json").exists()


def _evidencia(cliente: str) -> dict:
    return {
        "brand_json": _has_brand(cliente),
        "guiones": _count_glob(CD_OUT / cliente, "guion_*.md"),
        "briefs_carrusel": _count_glob(CD_OUT / cliente, "brief_carrusel_*.md"),
        "estrategias": _count_glob(CD_OUT / cliente, "estrategia_*.md"),
        "copy_meta_ads": _count_glob(CW_OUT / cliente, "meta_ad_*.md"),
        "captions": _count_glob(CW_OUT / cliente, "caption_*.md"),
        "disenos_png": _count_glob(DS_OUT / cliente, "*.png"),
        "plan_campana": _count_glob(PA_OUT / cliente, "plan_campana_*.md"),
        "brief_creativo_pauta": _count_glob(PA_OUT / cliente, "brief_creativo_*.md"),
        "campanas_meta_creadas": (PA_OUT / cliente / "draft_ids.json").exists(),
        "reporte_reciente": _count_glob(PA_OUT / cliente, "reporte_*.md") > 0,
    }


def _derivar_gates(ev: dict) -> dict:
    """
    Determina por evidencia. Si hay evidencia de una fase posterior, las
    anteriores quedan cerradas implicitamente (clientes que entraron sin
    pasar formalmente por todos los gates).
    """
    g = {k: "blocked" for k in GATES_ORDER}

    has = {
        "1_comercial": ev["brand_json"],
        "2_onboarding": ev["brand_json"],
        "3_preproduccion": bool(ev["guiones"] or ev["briefs_carrusel"] or ev["estrategias"]),
        "4_produccion": bool((ev["copy_meta_ads"] or ev["captions"]) and ev["disenos_png"]),
        "5_pauta": bool(ev["plan_campana"]),
        "6_lanzamiento": bool(ev["campanas_meta_creadas"]),
    }

    # cierro hacia atras: si la fase N tiene evidencia, todas las <= N quedan closed
    ultimo_idx = -1
    for i, fase in enumerate(GATES_ORDER):
        if has[fase]:
            ultimo_idx = i
    for i, fase in enumerate(GATES_ORDER):
        if i <= ultimo_idx:
            g[fase] = "closed"

    # primera fase sin evidencia despues del ultimo cierre = open
    siguiente = ultimo_idx + 1
    if siguiente < len(GATES_ORDER):
        g[GATES_ORDER[siguiente]] = "open"

    # si nada tiene evidencia, abrir la primera
    if ultimo_idx == -1:
        g[GATES_ORDER[0]] = "open"

    return g


def _siguiente_accion(gates: dict, ev: dict) -> dict:
    """Primer gate 'open' define el owner y el trigger."""
    fase_open = next((k for k in GATES_ORDER if gates[k] == "open"), None)

    mapping = {
        "1_comercial": ("Valentin", "Onboardear cliente y crear brand JSON", "Crear shared/brands/<cliente>.json"),
        "2_onboarding": ("Elias", "Validar onboarding completo", "/kickoff <cliente>"),
        "3_preproduccion": ("Nico (Creative Director)", "Generar guiones y briefs de carrusel", "creative_director: estrategia mensual"),
        "4_produccion": (
            "Copywriter + Design",
            "Faltan copies o disenos" if not (ev["copy_meta_ads"] and ev["disenos_png"]) else "Cerrar produccion",
            "/meta-ad y design generate",
        ),
        "5_pauta": ("Felipe (Media Buyer)", "Armar plan de campana", "media_buyer: /planificar"),
        "6_lanzamiento": ("Felipe (Media Buyer)", "Crear campana en Meta", "/crear-campana"),
    }

    if not fase_open:
        return {"owner": "Elias", "tarea": "Cliente con todas las fases cerradas. Monitoreo y reportes.", "trigger": "media_buyer: /analizar"}

    owner, tarea, trigger = mapping[fase_open]
    return {"fase_pendiente": fase_open, "owner": owner, "tarea": tarea, "trigger": trigger}


def compute(cliente: str) -> dict:
    ev = _evidencia(cliente)
    gates = _derivar_gates(ev)
    fase_actual = next((k for k in reversed(GATES_ORDER) if gates[k] == "closed"), None) or "0_pre_kickoff"
    return {
        "cliente": cliente,
        "fase_actual": fase_actual,
        "actualizado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "gates": gates,
        "evidencia": ev,
        "siguiente_accion": _siguiente_accion(gates, ev),
    }


def write(state: dict) -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = STATE_DIR / f"{state['cliente']}.json"
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def listar_clientes() -> list[str]:
    return sorted(p.stem for p in BRANDS.glob("*.json") if not p.stem.startswith("_"))


def _format_human(state: dict) -> str:
    g = state["gates"]
    sa = state["siguiente_accion"]
    lines = [
        f"Cliente: {state['cliente']}",
        f"Fase actual: {state['fase_actual']}",
        "",
        "Gates:",
    ]
    for k in GATES_ORDER:
        marker = {"closed": "[X]", "open": "[>]", "blocked": "[ ]"}[g[k]]
        lines.append(f"  {marker} {k:20s} {g[k]}")
    lines += [
        "",
        f"Siguiente accion: {sa.get('tarea', '-')}",
        f"  Owner:   {sa.get('owner', '-')}",
        f"  Trigger: {sa.get('trigger', '-')}",
        "",
        "Evidencia:",
    ]
    for k, v in state["evidencia"].items():
        lines.append(f"  {k:25s} {v}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1

    as_json = "--json" in argv
    if "--all" in argv:
        for c in listar_clientes():
            s = compute(c)
            write(s)
            if as_json:
                print(json.dumps(s, ensure_ascii=False))
            else:
                print(_format_human(s))
                print("-" * 60)
        return 0

    cliente = argv[0]
    if cliente not in listar_clientes():
        print(f"Cliente '{cliente}' no encontrado en shared/brands/.")
        print(f"Disponibles: {', '.join(listar_clientes())}")
        return 2

    s = compute(cliente)
    write(s)
    print(json.dumps(s, indent=2, ensure_ascii=False) if as_json else _format_human(s))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
