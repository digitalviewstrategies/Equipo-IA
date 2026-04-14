"""
render.py — Motor de renderizado HTML → PNG

Toma un archivo HTML con elementos de clase .slide y renderiza cada uno a PNG
usando Playwright + Chromium.

Uso desde CLI:
    python scripts/render.py --html input.html --out output_dir --width 1080 --height 1080

Uso programático desde el agente:
    from scripts.render import render_html_to_pngs
    pngs = render_html_to_pngs("input.html", "output/", 1080, 1080)
"""

import argparse
import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright


async def _render(html_path: Path, out_dir: Path, width: int, height: int, prefix: str = "slide"):
    """Renderiza cada elemento .slide del HTML como PNG separado."""
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=2,  # Retina quality
        )
        page = await context.new_page()
        await page.goto(f"file://{html_path.absolute()}")
        await page.wait_for_load_state("networkidle")
        # Esperar que las fuentes de Google carguen
        await page.wait_for_timeout(2000)

        slides = await page.query_selector_all(".slide")
        if not slides:
            print(f"WARNING: No se encontraron elementos .slide en {html_path}", file=sys.stderr)
            await browser.close()
            return []

        for i, slide in enumerate(slides, start=1):
            filename = f"{prefix}_{i:02d}.png"
            out_path = out_dir / filename
            await slide.screenshot(path=str(out_path))
            saved.append(out_path)
            print(f"OK {out_path}")

        await browser.close()

    return saved


def render_html_to_pngs(html_file, out_dir, width=1080, height=1080, prefix="slide"):
    """API programática para ser llamada desde otros scripts."""
    html_path = Path(html_file)
    out_path = Path(out_dir)
    return asyncio.run(_render(html_path, out_path, width, height, prefix))


def main():
    parser = argparse.ArgumentParser(description="Render HTML slides to PNG.")
    parser.add_argument("--html", required=True, help="Archivo HTML con elementos .slide")
    parser.add_argument("--out", required=True, help="Directorio de salida")
    parser.add_argument("--width", type=int, default=1080, help="Ancho del viewport")
    parser.add_argument("--height", type=int, default=1080, help="Alto del viewport")
    parser.add_argument("--prefix", default="slide", help="Prefijo de nombre de archivo")
    args = parser.parse_args()

    render_html_to_pngs(args.html, args.out, args.width, args.height, args.prefix)


if __name__ == "__main__":
    main()
