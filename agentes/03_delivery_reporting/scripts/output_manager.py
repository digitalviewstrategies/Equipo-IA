"""
output_manager.py — Gestion de outputs para el agente de Delivery y Reporting.

Lee datos del Media Buyer para construir reportes de cliente.
"""

import json
from datetime import date
from pathlib import Path

# scripts → 03_delivery_reporting → agentes → ROOT
ROOT_DIR = Path(__file__).resolve().parents[3]
BRANDS_DIR = ROOT_DIR / "shared" / "brands"
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"

PAUTA_OUTPUTS = ROOT_DIR / "agentes" / "04_pauta" / "outputs"
CREATIVE_OUTPUTS = ROOT_DIR / "agentes" / "01_contenido" / "creative_director" / "outputs"
DESIGN_OUTPUTS = ROOT_DIR / "agentes" / "01_contenido" / "design" / "output"
COPYWRITER_OUTPUTS = ROOT_DIR / "agentes" / "01_contenido" / "copywritter" / "outputs"


def list_brands() -> list[str]:
    if not BRANDS_DIR.exists():
        return []
    return [f.stem for f in sorted(BRANDS_DIR.glob("*.json")) if not f.stem.startswith("_")]


def load_brand(cliente: str) -> dict | None:
    path = BRANDS_DIR / f"{cliente}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_latest_pauta_output(cliente: str, tipo: str) -> Path | None:
    """
    Devuelve el output más reciente de un tipo dado del Media Buyer para un cliente.

    Args:
        tipo: prefijo del archivo (ej. 'reporte_semanal', 'reporte_mensual', 'analisis', 'brief_creativo')
    """
    cliente_dir = PAUTA_OUTPUTS / cliente
    if not cliente_dir.exists():
        return None
    for fecha_dir in sorted(cliente_dir.iterdir(), reverse=True):
        if not fecha_dir.is_dir():
            continue
        for archivo in sorted(fecha_dir.iterdir(), reverse=True):
            if archivo.is_file() and archivo.name.startswith(tipo):
                return archivo
    return None


def list_pauta_outputs(cliente: str, limit: int = 10) -> list[Path]:
    """Lista los outputs más recientes del Media Buyer para un cliente."""
    cliente_dir = PAUTA_OUTPUTS / cliente
    if not cliente_dir.exists():
        return []
    archivos = []
    for fecha_dir in sorted(cliente_dir.iterdir(), reverse=True):
        if not fecha_dir.is_dir():
            continue
        for archivo in sorted(fecha_dir.iterdir(), reverse=True):
            if archivo.is_file():
                archivos.append(archivo)
                if len(archivos) >= limit:
                    return archivos
    return archivos


def get_phase_outputs(cliente: str) -> dict[str, list[Path]]:
    """
    Devuelve todos los outputs por agente para usar en el checklist de fases.
    """
    result = {
        "creative_director": [],
        "copywriter": [],
        "design": [],
        "pauta": [],
    }

    for agent_name, base_dir in [
        ("creative_director", CREATIVE_OUTPUTS),
        ("copywriter", COPYWRITER_OUTPUTS),
        ("design", DESIGN_OUTPUTS),
        ("pauta", PAUTA_OUTPUTS),
    ]:
        cliente_dir = base_dir / cliente
        if not cliente_dir.exists():
            continue
        for fecha_dir in sorted(cliente_dir.iterdir(), reverse=True):
            if not fecha_dir.is_dir():
                continue
            for archivo in sorted(fecha_dir.rglob("*")):
                if archivo.is_file():
                    result[agent_name].append(archivo)

    return result


def save_output(cliente: str, tipo: str, nombre: str, contenido: str) -> Path:
    """Guarda un output de delivery/reporting."""
    fecha = date.today().isoformat()
    dir_destino = OUTPUTS_DIR / cliente / fecha
    dir_destino.mkdir(parents=True, exist_ok=True)
    path = dir_destino / f"{tipo}_{nombre}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenido)
    return path


if __name__ == "__main__":
    print("Clientes disponibles:")
    for b in list_brands():
        print(f"  - {b}")
    print(f"\nRaiz del proyecto: {ROOT_DIR}")
    print(f"Pauta outputs: {PAUTA_OUTPUTS}")
    print(f"Delivery outputs: {OUTPUTS_DIR}")
