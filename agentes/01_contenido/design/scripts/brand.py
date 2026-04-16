"""
brand.py — Helpers para cargar y usar brand systems.

Uso programático:
    from scripts.brand import load_brand, brand_to_css_vars
    brand = load_brand("digital_view")
    css = brand_to_css_vars(brand)
"""

import json
from pathlib import Path


# scripts → design → 01_contenido → agentes → ROOT
BRANDS_DIR = Path(__file__).resolve().parents[4] / "shared" / "brands"


def load_brand(brand_id: str) -> dict:
    """Carga el archivo JSON del brand system de un cliente."""
    path = BRANDS_DIR / f"{brand_id}.json"
    if not path.exists():
        available = [p.stem for p in BRANDS_DIR.glob("*.json") if not p.stem.startswith("_")]
        raise FileNotFoundError(
            f"No existe brand system para '{brand_id}'. "
            f"Marcas disponibles: {', '.join(available)}. "
            f"Para crear una nueva, seguí shared/brands/_onboarding.md"
        )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def brand_to_css_vars(brand: dict) -> str:
    """
    Convierte los colores del brand system en un bloque de CSS variables
    listo para inyectar en un template HTML.
    """
    colors = brand.get("colors", {})
    css_vars = [":root {"]
    for color_key, color_data in colors.items():
        if isinstance(color_data, dict) and "hex" in color_data:
            var_name = f"--{color_key.replace('_', '-')}"
            css_vars.append(f"  {var_name}: {color_data['hex']};")
    css_vars.append("}")
    return "\n".join(css_vars)


def get_color(brand: dict, color_key: str) -> str:
    """Devuelve el HEX de un color específico del brand."""
    colors = brand.get("colors", {})
    if color_key not in colors:
        raise KeyError(f"Color '{color_key}' no existe en el brand system.")
    return colors[color_key]["hex"]


def get_font_import(brand: dict) -> str:
    """
    Genera el tag <link> de Google Fonts con todas las tipografías del brand.
    """
    typography = brand.get("typography", {})
    urls = set()
    for font_data in typography.values():
        if isinstance(font_data, dict) and "google_font_url" in font_data:
            urls.add(font_data["google_font_url"])
    links = [f'<link href="{url}" rel="stylesheet">' for url in urls]
    return "\n".join(links)


def list_brands() -> list:
    """Lista todos los brands disponibles (excluyendo templates)."""
    return sorted([p.stem for p in BRANDS_DIR.glob("*.json") if not p.stem.startswith("_")])


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python scripts/brand.py <brand_id>")
        print(f"Brands disponibles: {', '.join(list_brands())}")
        sys.exit(1)
    brand = load_brand(sys.argv[1])
    print(f"Brand: {brand['brand_name']}")
    print(f"Positioning: {brand['positioning']}")
    print()
    print("CSS Vars:")
    print(brand_to_css_vars(brand))
    print()
    print("Font imports:")
    print(get_font_import(brand))
