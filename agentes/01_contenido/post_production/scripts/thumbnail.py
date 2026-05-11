"""
thumbnail.py — Snapshot PNG desde un master a un timestamp dado.

Naming output:
    <CLIENTE>_<TipoContenido>_V<n>_thumb.png

Uso:
    python thumbnail.py --input master.mp4 --cliente lopez_propiedades \
        --tipo RecorridoVO --version 1 --at 3.0
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUT = Path(__file__).resolve().parents[1] / "outputs"


def _pascal_cliente(cliente: str) -> str:
    return "".join(p.capitalize() for p in cliente.split("_") if p)


def run(input_path: str, cliente: str, tipo: str, version: int,
        at: float = 1.0, out_dir: str | None = None) -> dict:
    master = Path(input_path)
    if not master.exists():
        return {"error": f"input no existe: {input_path}"}

    base = _pascal_cliente(cliente)
    fecha = date.today().isoformat()
    out_root = Path(out_dir) if out_dir else (DEFAULT_OUT / cliente / fecha)
    out_root.mkdir(parents=True, exist_ok=True)
    out_file = out_root / f"{base}_{tipo}_V{version}_thumb.png"

    cmd = [
        "ffmpeg", "-y", "-ss", str(at), "-i", str(master),
        "-vframes", "1", "-q:v", "2", str(out_file),
    ]
    try:
        subprocess.run(cmd, check=True, timeout=60,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return {"error": f"ffmpeg fallo: {e.stderr.decode('utf-8', 'ignore')[:200]}"}
    except subprocess.TimeoutExpired:
        return {"error": "timeout 60s"}

    return {"input": str(master), "at": at, "output": str(out_file.relative_to(ROOT)).replace("\\", "/")}


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--cliente", required=True)
    p.add_argument("--tipo", required=True)
    p.add_argument("--version", type=int, default=1)
    p.add_argument("--at", type=float, default=1.0)
    p.add_argument("--out-dir")
    a = p.parse_args(argv)
    r = run(a.input, a.cliente, a.tipo, a.version, a.at, a.out_dir)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if "error" not in r else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
