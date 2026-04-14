"""
output_manager.py
Organiza y guarda los outputs del DV Creative Director.
"""

import os
import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
BRANDS_DIR = BASE_DIR.parent / "dv_design_agent" / "brands"


def get_output_dir(client_name: str) -> Path:
    """Crea y retorna el directorio de output para un cliente y fecha."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    client_slug = client_name.lower().replace(" ", "_")
    output_dir = OUTPUTS_DIR / client_slug / date_str
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def save_guion(client_name: str, titulo: str, content: str) -> Path:
    """Guarda un guion de video como archivo markdown."""
    output_dir = get_output_dir(client_name)
    titulo_slug = titulo.lower().replace(" ", "_")[:40]
    filename = f"guion_{titulo_slug}.md"
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"Guion guardado: {filepath}")
    return filepath


def save_brief_carrusel(client_name: str, titulo: str, content: str) -> Path:
    """Guarda un brief de carrusel como archivo markdown."""
    output_dir = get_output_dir(client_name)
    titulo_slug = titulo.lower().replace(" ", "_")[:40]
    filename = f"brief_carrusel_{titulo_slug}.md"
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"Brief guardado: {filepath}")
    return filepath


def save_estrategia(client_name: str, mes: str, content: str) -> Path:
    """Guarda una estrategia mensual como archivo markdown."""
    output_dir = get_output_dir(client_name)
    mes_slug = mes.lower().replace(" ", "_")
    filename = f"estrategia_{mes_slug}.md"
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"Estrategia guardada: {filepath}")
    return filepath


def save_ideas(client_name: str, objetivo: str, content: str) -> Path:
    """Guarda las ideas iniciales (antes de desarrollar) como archivo markdown."""
    output_dir = get_output_dir(client_name)
    objetivo_slug = objetivo.lower().replace(" ", "_")[:40]
    filename = f"ideas_{objetivo_slug}.md"
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"Ideas guardadas: {filepath}")
    return filepath


def load_brand_system(client_name: str) -> dict | None:
    """
    Carga el brand system de un cliente desde la carpeta compartida con dv_design_agent.
    Retorna None si no existe.
    """
    client_slug = client_name.lower().replace(" ", "_")
    brand_file = BRANDS_DIR / f"{client_slug}.json"

    if not brand_file.exists():
        # Intenta con el nombre exacto
        for f in BRANDS_DIR.glob("*.json"):
            if client_name.lower() in f.stem.lower():
                brand_file = f
                break
        else:
            print(f"Brand system no encontrado para: {client_name}")
            print(f"Buscado en: {BRANDS_DIR}")
            return None

    with open(brand_file, encoding="utf-8") as f:
        return json.load(f)


def list_clients() -> list[str]:
    """Lista todos los clientes con brand system disponible."""
    if not BRANDS_DIR.exists():
        return []
    return [
        f.stem
        for f in BRANDS_DIR.glob("*.json")
        if not f.stem.startswith("_")
    ]


def list_outputs(client_name: str = None) -> list[Path]:
    """Lista los outputs guardados, opcionalmente filtrado por cliente."""
    if not OUTPUTS_DIR.exists():
        return []

    if client_name:
        client_slug = client_name.lower().replace(" ", "_")
        search_dir = OUTPUTS_DIR / client_slug
        if not search_dir.exists():
            return []
        return sorted(search_dir.rglob("*.md"))

    return sorted(OUTPUTS_DIR.rglob("*.md"))


if __name__ == "__main__":
    print("Clientes con brand system disponible:")
    clients = list_clients()
    if clients:
        for c in clients:
            print(f"  - {c}")
    else:
        print("  (ninguno todavía)")

    print(f"\nDirectorio de outputs: {OUTPUTS_DIR}")
    print(f"Directorio de brand systems: {BRANDS_DIR}")
