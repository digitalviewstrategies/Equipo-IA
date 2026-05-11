"""
multiformat.py — Renderiza un master a 9:16, 1:1 y 16:9 con ffmpeg.

Estrategia por formato (sin recortes que pierdan info crítica del master):
  - 9:16 (1080x1920): si master es horizontal, usa background blur del propio
    frame escalado y video centrado. Si es vertical, escala simple.
  - 1:1  (1080x1080): pad o crop según orientación, default crop centrado.
  - 16:9 (1920x1080): si master es horizontal, escala. Si es vertical,
    background blur + video centrado.

Naming output:
    <CLIENTE>_<TipoContenido>_V<n>_<aspect>.mp4
    aspect ∈ {9x16, 1x1, 16x9}

Uso:
    python multiformat.py --input master.mp4 --cliente lopez_propiedades \
        --tipo RecorridoVO --version 1 [--out-dir outputs/...]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "outputs"

PROFILES = {
    "9x16": (1080, 1920),
    "1x1":  (1080, 1080),
    "16x9": (1920, 1080),
}

NAMING_RE = re.compile(r"^[A-Za-z0-9]+$")


def _probe(path: Path) -> tuple[int, int]:
    """Devuelve (w, h) del primer video stream."""
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height", "-of", "json", str(path),
    ]
    out = subprocess.check_output(cmd, text=True, timeout=30)
    data = json.loads(out)
    s = data["streams"][0]
    return int(s["width"]), int(s["height"])


def _pascal_cliente(cliente: str) -> str:
    """lopez_propiedades -> LopezPropiedades para el naming."""
    return "".join(p.capitalize() for p in cliente.split("_") if p)


def _vf(src_w: int, src_h: int, target_w: int, target_h: int) -> str:
    """
    Filter chain. Si src y target tienen orientación distinta, usa background
    blur escalado del propio video + video centrado. Si misma orientación,
    crop centrado.
    """
    src_landscape = src_w >= src_h
    target_landscape = target_w >= target_h
    if src_landscape == target_landscape:
        # Misma orientación: scale + crop centrado para llenar.
        return (
            f"scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
            f"crop={target_w}:{target_h}"
        )
    # Orientación distinta: background blur + video centrado encima.
    return (
        f"split[bg][fg];"
        f"[bg]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
        f"crop={target_w}:{target_h},gblur=sigma=30[bg2];"
        f"[fg]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease[fg2];"
        f"[bg2][fg2]overlay=(W-w)/2:(H-h)/2"
    )


def _render(master: Path, profile: str, out_path: Path, src_dims: tuple[int, int]) -> None:
    tw, th = PROFILES[profile]
    sw, sh = src_dims
    vf = _vf(sw, sh, tw, th)
    cmd = [
        "ffmpeg", "-y", "-i", str(master),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, timeout=600,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def run(input_path: str, cliente: str, tipo: str, version: int,
        out_dir: str | None = None, profiles: list[str] | None = None) -> dict:
    master = Path(input_path)
    if not master.exists():
        return {"error": f"input no existe: {input_path}"}
    if not NAMING_RE.match(tipo):
        return {"error": f"tipo invalido: {tipo} (solo alfanumerico, sin espacios)"}

    src_dims = _probe(master)
    base = _pascal_cliente(cliente)
    name_stem = f"{base}_{tipo}_V{version}"
    fecha = date.today().isoformat()
    out_root = Path(out_dir) if out_dir else (DEFAULT_OUT / cliente / fecha)
    out_root.mkdir(parents=True, exist_ok=True)

    targets = profiles or list(PROFILES.keys())
    results = {}
    for prof in targets:
        out_file = out_root / f"{name_stem}_{prof}.mp4"
        try:
            _render(master, prof, out_file, src_dims)
            results[prof] = str(out_file.relative_to(ROOT)).replace("\\", "/")
        except subprocess.CalledProcessError as e:
            results[prof] = f"FAIL: {e.stderr.decode('utf-8', 'ignore')[:200]}"
        except subprocess.TimeoutExpired:
            results[prof] = "FAIL: timeout 600s"
    return {"input": str(master), "src_dims": src_dims, "outputs": results}


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--cliente", required=True)
    p.add_argument("--tipo", required=True)
    p.add_argument("--version", type=int, default=1)
    p.add_argument("--out-dir")
    p.add_argument("--profiles", nargs="*", choices=list(PROFILES))
    a = p.parse_args(argv)
    r = run(a.input, a.cliente, a.tipo, a.version, a.out_dir, a.profiles)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if "error" not in r else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
