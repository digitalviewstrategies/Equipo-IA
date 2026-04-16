"""
generate.py — Orquestador del agente.

Función principal: tomar un tipo de pieza, un brand id y un diccionario de
contenido, renderizar los PNGs y devolver los paths.

Uso desde el agente:
    from scripts.generate import generate_piece
    paths = generate_piece(
        piece_type="carrusel_captacion",
        brand_id="digital_view",
        content={
            "TAG_HOOK": "Método DV · 001",
            "HOOK_HEADLINE": "...",
            ...
        },
        output_name="mi_carrusel"
    )

Uso desde CLI (para tests):
    python scripts/generate.py --type carrusel_captacion --brand digital_view --content content.json
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Hacer importables los módulos locales
sys.path.insert(0, str(Path(__file__).parent))
from render import render_html_to_pngs
from brand import load_brand


ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"


PIECE_CONFIG = {
    "carrusel_captacion": {
        "template": "carrusel_captacion.html",
        "width": 1080,
        "height": 1080,
        "prefix": "slide",
        "description": "Carrusel de 6 slides con estructura DOLOR→CONSECUENCIA→SOLUCIÓN→PRUEBA",
    },
    "carrusel_educativo": {
        "template": "carrusel_educativo.html",
        "width": 1080,
        "height": 1080,
        "prefix": "slide",
        "description": "Carrusel educativo con estructura HOOK→PROBLEMA→TIPS→CIERRE",
    },
    "creativo_meta": {
        "template": "creativo_meta.html",
        "width": 1080,
        "height": 1080,
        "prefix": "creativo",
        "description": "Creativo estático cuadrado para feed Meta Ads",
    },
    "creativo_meta_vertical": {
        "template": "creativo_meta_vertical.html",
        "width": 1080,
        "height": 1920,
        "prefix": "creativo_v",
        "description": "Creativo vertical para stories/reels Meta Ads",
    },
    "placa_propiedad": {
        "template": "placa_propiedad.html",
        "width": 1080,
        "height": 1350,
        "prefix": "placa",
        "description": "Placa individual de propiedad",
    },
    "flyer_propiedad": {
        "template": "flyer_propiedad.html",
        "width": 2480,
        "height": 3508,
        "prefix": "flyer",
        "description": "Flyer A4 de lanzamiento de propiedad",
    },
}


def generate_piece(piece_type: str, brand_id: str, content: dict, output_name: str = None):
    """
    Genera una pieza aplicando el template correspondiente al brand dado.

    Args:
        piece_type: Uno de los keys de PIECE_CONFIG.
        brand_id: Identificador del brand (ej: "digital_view").
        content: Diccionario de placeholders a reemplazar en el template.
        output_name: Nombre base de los archivos. Si no se pasa, usa el piece_type.

    Returns:
        Lista de paths de los PNGs generados.
    """
    if piece_type not in PIECE_CONFIG:
        raise ValueError(
            f"Tipo de pieza '{piece_type}' desconocido. "
            f"Opciones: {', '.join(PIECE_CONFIG.keys())}"
        )

    config = PIECE_CONFIG[piece_type]
    brand = load_brand(brand_id)

    # Merge de contenido: agregar datos del brand al content si no vienen
    if "BRAND_NAME" not in content:
        content["BRAND_NAME"] = brand["brand_name"].upper()
    if "BRAND_TAGLINE" not in content:
        content["BRAND_TAGLINE"] = brand.get("brand_tagline", "")

    # Cargar template y reemplazar placeholders
    template_path = TEMPLATES_DIR / config["template"]
    html = template_path.read_text(encoding="utf-8")
    for key, value in content.items():
        placeholder = "{{" + key + "}}"
        html = html.replace(placeholder, str(value))

    # Detectar placeholders sin reemplazar para alertar al agente
    import re
    missing = re.findall(r"\{\{[A-Z_0-9]+\}\}", html)
    if missing:
        print(f"AVISO: placeholders sin reemplazar: {set(missing)}", file=sys.stderr)

    # Escribir HTML temporal
    today = date.today().isoformat()
    work_name = output_name or piece_type
    out_dir = OUTPUT_DIR / brand_id / today / piece_type
    out_dir.mkdir(parents=True, exist_ok=True)
    html_file = out_dir / f"{work_name}.html"
    html_file.write_text(html, encoding="utf-8")

    # Renderizar
    png_paths = render_html_to_pngs(
        str(html_file),
        str(out_dir),
        width=config["width"],
        height=config["height"],
        prefix=config["prefix"],
    )

    return [str(p) for p in png_paths]


def main():
    parser = argparse.ArgumentParser(description="Generar pieza del agente DV Design.")
    parser.add_argument("--type", required=True, choices=list(PIECE_CONFIG.keys()))
    parser.add_argument("--brand", required=True, help="brand_id (ej: digital_view)")
    parser.add_argument("--content", required=True, help="Path a JSON con los placeholders")
    parser.add_argument("--name", default=None, help="Nombre del output")
    args = parser.parse_args()

    with open(args.content, "r", encoding="utf-8") as f:
        content = json.load(f)

    paths = generate_piece(args.type, args.brand, content, args.name)
    print(f"\nListo. {len(paths)} archivo(s) generado(s):")
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
