"""
output_manager.py — Gestion centralizada de outputs y brands para el DV Coordinador.

Agrega outputs de los 4 agentes especializados para dar una vista completa del estado de un cliente.
"""

import json
from datetime import date
from pathlib import Path

# scripts → 00_coordinador → agentes → ROOT
ROOT_DIR = Path(__file__).resolve().parents[3]
BRANDS_DIR = ROOT_DIR / "shared" / "brands"
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"

AGENT_OUTPUTS = {
    "creative_director": ROOT_DIR / "agentes" / "01_contenido" / "creative_director" / "outputs",
    "copywriter": ROOT_DIR / "agentes" / "01_contenido" / "copywritter" / "outputs",
    "design": ROOT_DIR / "agentes" / "01_contenido" / "design" / "output",
    "pauta": ROOT_DIR / "agentes" / "04_pauta" / "outputs",
}


def list_brands() -> list[str]:
    """Lista los clientes onboardeados en shared/brands/."""
    if not BRANDS_DIR.exists():
        return []
    return [
        f.stem
        for f in sorted(BRANDS_DIR.glob("*.json"))
        if not f.stem.startswith("_")
    ]


def load_brand(cliente: str) -> dict | None:
    """Carga el brand system de un cliente. None si no existe."""
    path = BRANDS_DIR / f"{cliente}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def brand_exists(cliente: str) -> bool:
    return (BRANDS_DIR / f"{cliente}.json").exists()


def get_client_outputs(cliente: str, limit_per_agent: int = 10) -> dict[str, list[Path]]:
    """
    Devuelve todos los outputs de un cliente agrupados por agente.

    Returns:
        Dict con keys 'creative_director', 'copywriter', 'design', 'pauta'.
        Cada valor es una lista de Paths, ordenados del más reciente al más antiguo.
    """
    result = {agent: [] for agent in AGENT_OUTPUTS}

    for agent, base_dir in AGENT_OUTPUTS.items():
        cliente_dir = base_dir / cliente
        if not cliente_dir.exists():
            continue
        archivos = []
        for fecha_dir in sorted(cliente_dir.iterdir(), reverse=True):
            if not fecha_dir.is_dir():
                continue
            for archivo in sorted(fecha_dir.rglob("*")):
                if archivo.is_file():
                    archivos.append(archivo)
                    if len(archivos) >= limit_per_agent:
                        break
            if len(archivos) >= limit_per_agent:
                break
        result[agent] = archivos

    return result


def get_latest_output(cliente: str, agent: str, tipo: str | None = None) -> Path | None:
    """
    Devuelve el output más reciente de un agente para un cliente.

    Args:
        cliente: nombre del cliente.
        agent: 'creative_director' | 'copywriter' | 'design' | 'pauta'.
        tipo: prefijo del tipo de archivo (ej. 'brief_creativo', 'reporte_semanal'). None = cualquiera.
    """
    base_dir = AGENT_OUTPUTS.get(agent)
    if not base_dir:
        return None
    cliente_dir = base_dir / cliente
    if not cliente_dir.exists():
        return None
    for fecha_dir in sorted(cliente_dir.iterdir(), reverse=True):
        if not fecha_dir.is_dir():
            continue
        for archivo in sorted(fecha_dir.rglob("*"), reverse=True):
            if archivo.is_file():
                if tipo is None or archivo.name.startswith(tipo):
                    return archivo
    return None


def save_output(cliente: str, tipo: str, nombre: str, contenido: str) -> Path:
    """Guarda un output del coordinador en outputs/[cliente]/[YYYY-MM-DD]/[tipo]_[nombre].md"""
    fecha = date.today().isoformat()
    dir_destino = OUTPUTS_DIR / cliente / fecha
    dir_destino.mkdir(parents=True, exist_ok=True)
    path = dir_destino / f"{tipo}_{nombre}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenido)
    return path


def format_status_report(cliente: str) -> str:
    """
    Genera un reporte de estado textual para un cliente.
    Usado por el skill /status.
    """
    brand = load_brand(cliente)
    outputs = get_client_outputs(cliente)

    lineas = [f"# Estado — {cliente}", ""]

    # Brand
    if brand:
        ad_account = brand.get("meta_ads", {}).get("ad_account_id", "no configurado")
        lineas += [f"**Brand:** OK — Ad Account: `{ad_account}`", ""]
    else:
        lineas += ["**Brand:** NO EXISTE — cliente no onboardeado en shared/brands/", ""]
        return "\n".join(lineas)

    # Outputs por agente
    agentes_display = {
        "creative_director": "Creative Director",
        "copywriter": "Copywriter",
        "design": "Design",
        "pauta": "Media Buyer (Pauta)",
    }

    for agent_key, agent_name in agentes_display.items():
        archivos = outputs[agent_key]
        if not archivos:
            lineas.append(f"**{agent_name}:** sin outputs")
        else:
            lineas.append(f"**{agent_name}:** {len(archivos)} archivo(s)")
            for a in archivos[:3]:
                # Mostrar path relativo desde la raiz del agent
                try:
                    rel = a.relative_to(ROOT_DIR)
                except ValueError:
                    rel = a
                lineas.append(f"  - `{rel}`")
            if len(archivos) > 3:
                lineas.append(f"  - ... y {len(archivos) - 3} más")
        lineas.append("")

    # Alertas
    alertas = []
    if not outputs["creative_director"]:
        alertas.append("No hay contenido del Creative Director. Arranca por ahi.")
    if not outputs["copywriter"]:
        alertas.append("No hay copy. Pedi al Copywriter antes de pauta.")
    if not outputs["design"]:
        alertas.append("No hay piezas de Design.")
    brief_creativo = get_latest_output(cliente, "pauta", "brief_creativo")
    if brief_creativo:
        alertas.append(f"Media Buyer tiene un brief creativo pendiente: `{brief_creativo.name}` — Creative Director tiene que procesarlo.")

    if alertas:
        lineas.append("**Alertas:**")
        for a in alertas:
            lineas.append(f"  - {a}")
        lineas.append("")

    return "\n".join(lineas)


if __name__ == "__main__":
    print("Clientes onboardeados:")
    for b in list_brands():
        print(f"  - {b}")
    print(f"\nRaiz del proyecto: {ROOT_DIR}")
    print(f"Brands: {BRANDS_DIR}")
    print(f"Outputs coordinador: {OUTPUTS_DIR}")
