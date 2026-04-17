"""
output_manager.py — Gestion de brands y outputs del DV Media Buyer.

Funciones principales:
- list_brands(): lista los clientes disponibles.
- load_brand(cliente): carga el JSON del brand system.
- save_output(cliente, tipo, nombre, contenido): guarda un output.
- load_creative_outputs(cliente): lista outputs de Creative Director y Design.
"""

import json
from datetime import date
from pathlib import Path

# scripts → 04_pauta → agentes → ROOT
ROOT_DIR = Path(__file__).resolve().parents[3]
BRANDS_DIR = ROOT_DIR / "shared" / "brands"
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"

# Outputs de otros agentes
CREATIVE_DIR_OUTPUTS = ROOT_DIR / "agentes" / "01_contenido" / "creative_director" / "outputs"
DESIGN_OUTPUTS = ROOT_DIR / "agentes" / "01_contenido" / "design" / "output"

TIPOS_VALIDOS = {
    "plan_campana",
    "reporte_semanal",
    "reporte_mensual",
    "brief_creativo",
    "brief_diseno",
    "analisis",
    "otro",
}


def list_brands() -> list[str]:
    """Lista los clientes disponibles en shared/brands/."""
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


def save_output(cliente: str, tipo: str, nombre: str, contenido: str) -> Path:
    """
    Guarda un output en outputs/[cliente]/[YYYY-MM-DD]/[tipo]_[nombre].md

    Returns:
        Path al archivo guardado.
    """
    if tipo not in TIPOS_VALIDOS:
        raise ValueError(
            f"Tipo '{tipo}' invalido. Tipos validos: {', '.join(sorted(TIPOS_VALIDOS))}"
        )

    fecha = date.today().isoformat()
    dir_destino = OUTPUTS_DIR / cliente / fecha
    dir_destino.mkdir(parents=True, exist_ok=True)

    nombre_archivo = f"{tipo}_{nombre}.md"
    path = dir_destino / nombre_archivo

    with open(path, "w", encoding="utf-8") as f:
        f.write(contenido)

    return path


def list_recent_outputs(cliente: str, limit: int = 10) -> list[Path]:
    """Lista los outputs mas recientes de un cliente."""
    cliente_dir = OUTPUTS_DIR / cliente
    if not cliente_dir.exists():
        return []
    archivos = []
    for fecha_dir in sorted(cliente_dir.iterdir(), reverse=True):
        if not fecha_dir.is_dir():
            continue
        for archivo in sorted(fecha_dir.iterdir()):
            if archivo.is_file():
                archivos.append(archivo)
                if len(archivos) >= limit:
                    return archivos
    return archivos


def load_creative_outputs(cliente: str) -> dict[str, list[Path]]:
    """
    Lista outputs disponibles de Creative Director y Design para un cliente.

    Returns:
        Dict con keys 'creative_director' y 'design', cada una con lista de Paths.
    """
    result = {"creative_director": [], "design": []}

    # Creative Director outputs
    cd_dir = CREATIVE_DIR_OUTPUTS / cliente
    if cd_dir.exists():
        for fecha_dir in sorted(cd_dir.iterdir(), reverse=True):
            if not fecha_dir.is_dir():
                continue
            for archivo in sorted(fecha_dir.iterdir()):
                if archivo.is_file():
                    result["creative_director"].append(archivo)

    # Design outputs
    d_dir = DESIGN_OUTPUTS / cliente
    if d_dir.exists():
        for fecha_dir in sorted(d_dir.iterdir(), reverse=True):
            if not fecha_dir.is_dir():
                continue
            for archivo in sorted(fecha_dir.rglob("*")):
                if archivo.is_file():
                    result["design"].append(archivo)

    return result


if __name__ == "__main__":
    print("Brands disponibles:")
    for b in list_brands():
        print(f"  - {b}")
    print(f"\nDirectorio de outputs: {OUTPUTS_DIR}")
    print(f"Directorio de brands:  {BRANDS_DIR}")
    print(f"Creative Director:     {CREATIVE_DIR_OUTPUTS}")
    print(f"Design:                {DESIGN_OUTPUTS}")
