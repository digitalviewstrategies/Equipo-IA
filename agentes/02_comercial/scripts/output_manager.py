"""
output_manager.py — Gestión de outputs del agente comercial DV.
"""

from datetime import date
from pathlib import Path

# scripts → 02_comercial → agentes → ROOT
ROOT_DIR = Path(__file__).resolve().parents[3]
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"

TIPOS_VALIDOS = {
    "calificacion",
    "brief_reunion",
    "propuesta",
    "nota_pipeline",
    "otro",
}


def save_output(prospecto: str, tipo: str, nombre: str, contenido: str) -> Path:
    """
    Guarda un output en outputs/[prospecto]/[YYYY-MM-DD]/[tipo]_[nombre].md

    El nombre del prospecto se normaliza (minúsculas, guiones).
    """
    if tipo not in TIPOS_VALIDOS:
        raise ValueError(f"Tipo '{tipo}' inválido. Válidos: {', '.join(sorted(TIPOS_VALIDOS))}")

    prospecto_key = prospecto.lower().replace(" ", "_").replace("/", "_")
    fecha = date.today().isoformat()
    dir_destino = OUTPUTS_DIR / prospecto_key / fecha
    dir_destino.mkdir(parents=True, exist_ok=True)

    path = dir_destino / f"{tipo}_{nombre}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenido)
    return path


def list_outputs(prospecto: str) -> list[Path]:
    """Lista todos los outputs de un prospecto."""
    prospecto_key = prospecto.lower().replace(" ", "_").replace("/", "_")
    cliente_dir = OUTPUTS_DIR / prospecto_key
    if not cliente_dir.exists():
        return []
    archivos = []
    for fecha_dir in sorted(cliente_dir.iterdir(), reverse=True):
        if not fecha_dir.is_dir():
            continue
        for archivo in sorted(fecha_dir.iterdir()):
            if archivo.is_file():
                archivos.append(archivo)
    return archivos


if __name__ == "__main__":
    print(f"Directorio de outputs: {OUTPUTS_DIR}")
    print(f"Raíz del proyecto: {ROOT_DIR}")
