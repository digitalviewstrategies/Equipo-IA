"""
generate_image.py — Wrapper de Gemini 2.5 Flash Image (Nano Banana)

Usa la API de Google Gemini para:
- Mejorar fotos de propiedades existentes (iluminación, color, limpieza).
- Generar fondos abstractos.
- Sacar objetos molestos de fotos.

Requiere GOOGLE_API_KEY en el entorno.

Instalación:
    pip install google-genai python-dotenv Pillow

Uso desde CLI:
    python scripts/generate_image.py --prompt "mejorá esta foto" --input foto.jpg --out resultado.png
    python scripts/generate_image.py --prompt "fondo abstracto azul" --out fondo.png

Uso programático:
    from scripts.generate_image import generate_image
    path = generate_image("mejorá la luz", input_path="foto.jpg", out_path="result.png")
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from google import genai
    from google.genai import types
    from PIL import Image
    from dotenv import load_dotenv
except ImportError as e:
    print(f"ERROR: faltan dependencias. Ejecutá: pip install google-genai python-dotenv Pillow", file=sys.stderr)
    print(f"Detalle: {e}", file=sys.stderr)
    sys.exit(1)

load_dotenv()

MODEL = "gemini-2.5-flash-image"


def generate_image(prompt: str, input_path: str = None, out_path: str = "output.png") -> str:
    """
    Genera o edita una imagen con Gemini 2.5 Flash Image.

    Args:
        prompt: Descripción en lenguaje natural de lo que querés.
        input_path: Opcional. Si existe, la imagen se usa como base para edición.
        out_path: Path donde guardar el resultado.

    Returns:
        Path del archivo generado.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Falta GOOGLE_API_KEY en el entorno. Creá un archivo .env con:\n"
            "GOOGLE_API_KEY=tu_key_aca\n"
            "Obtené una key gratis en https://aistudio.google.com/app/apikey"
        )

    client = genai.Client(api_key=api_key)

    # Preparar inputs
    contents = [prompt]
    if input_path and Path(input_path).exists():
        img = Image.open(input_path)
        contents.append(img)
        print(f"Editando imagen base: {input_path}")
    else:
        print("Generando imagen nueva desde prompt.")

    # Llamada al modelo
    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
    )

    # Extraer imagen de la respuesta
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            out_file = Path(out_path)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with open(out_file, "wb") as f:
                f.write(part.inline_data.data)
            print(f"OK: imagen guardada en {out_file}")
            return str(out_file)

    raise RuntimeError("El modelo no devolvió imagen. Revisá el prompt.")


def main():
    parser = argparse.ArgumentParser(description="Generar/editar imágenes con Gemini 2.5 Flash Image.")
    parser.add_argument("--prompt", required=True, help="Descripción del resultado deseado.")
    parser.add_argument("--input", default=None, help="Imagen base opcional para edición.")
    parser.add_argument("--out", default="output.png", help="Path del archivo de salida.")
    args = parser.parse_args()

    try:
        generate_image(args.prompt, args.input, args.out)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
