"""
output_manager.py — Gestión de brands y outputs del DV Creative Director.

Funciones principales:
- list_brands(): lista los clientes disponibles leyendo brand systems desde
  ../dv_design_agent/brands/.
- load_brand(cliente): carga el JSON del brand system de un cliente.
- save_output(cliente, tipo, nombre, contenido): guarda un output en
  outputs/[cliente]/[fecha]/.

El agente NUNCA inventa contexto del cliente. Si load_brand() devuelve None,
el agente para y avisa que falta el onboarding en el agente de diseño.
"""

import json
import os
from datetime import date
from pathlib import Path

# Path al directorio de brands del agente de diseño (fuente única de verdad).
BRANDS_DIR = Path(__file__).resolve().parent.parent.parent / "dv_design_agent" / "brands"

# Path al directorio de outputs de este agente.
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"

# Tipos de output válidos. Define las subcarpetas dentro de cada cliente/fecha.
TIPOS_VALIDOS = {"guion", "brief_carrusel", "estrategia", "ideas", "otro"}


def list_brands() -> list[str]:
    """
    Lista los clientes disponibles leyendo los archivos .json del directorio
    de brands del agente de diseño. Excluye archivos que empiecen con '_'
    (templates y onboardings).
    """
    if not BRANDS_DIR.exists():
        return []
    brands = []
    for f in sorted(BRANDS_DIR.glob("*.json")):
        if f.stem.startswith("_"):
            continue
        brands.append(f.stem)
    return brands


def load_brand(cliente: str) -> dict | None:
    """
    Carga el brand system de un cliente. Devuelve el dict del JSON o None
    si no existe. El agente debe parar y avisar si devuelve None.
    """
    path = BRANDS_DIR / f"{cliente}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_output(cliente: str, tipo: str, nombre: str, contenido: str) -> Path:
    """
    Guarda un output en outputs/[cliente]/[YYYY-MM-DD]/[tipo]_[nombre].md

    Args:
        cliente: nombre del cliente (mismo que el brand system).
        tipo: uno de TIPOS_VALIDOS.
        nombre: nombre descriptivo del output, en snake_case sin extensión.
        contenido: el markdown del output.

    Returns:
        Path al archivo guardado.
    """
    if tipo not in TIPOS_VALIDOS:
        raise ValueError(
            f"Tipo '{tipo}' inválido. Tipos válidos: {', '.join(sorted(TIPOS_VALIDOS))}"
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
    """
    Lista los outputs más recientes de un cliente, ordenados por fecha
    descendente. Útil para el agente cuando quiere ver qué se entregó antes.
    """
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


if __name__ == "__main__":
    # Self-check rápido cuando se corre el script directamente.
    print("Brands disponibles:")
    for b in list_brands():
        print(f"  - {b}")
    print(f"\nDirectorio de outputs: {OUTPUTS_DIR}")
    print(f"Directorio de brands:   {BRANDS_DIR}")
