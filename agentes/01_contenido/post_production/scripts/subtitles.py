"""
subtitles.py — Transcribe audio de un master via OpenAI Whisper API a SRT.

Extrae audio con ffmpeg a un mp3 temporal, lo manda a la API (response_format=srt)
y guarda el .srt al lado del master con el naming DV.

Naming output:
    <CLIENTE>_<TipoContenido>_V<n>.srt

Requiere OPENAI_API_KEY en agentes/01_contenido/post_production/.env
o en el environment.

Uso:
    python subtitles.py --input master.mp4 --cliente lopez_propiedades \
        --tipo RecorridoVO --version 1 --language es
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
POST_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = POST_ROOT / "outputs"

OPENAI_URL = "https://api.openai.com/v1/audio/transcriptions"
MODEL = "whisper-1"


def _pascal_cliente(cliente: str) -> str:
    return "".join(p.capitalize() for p in cliente.split("_") if p)


def _load_key() -> str | None:
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    env = POST_ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def _extract_audio(master: Path) -> Path:
    tmp = Path(tempfile.gettempdir()) / f"dv_subs_{master.stem}.mp3"
    cmd = [
        "ffmpeg", "-y", "-i", str(master),
        "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k",
        str(tmp),
    ]
    subprocess.run(cmd, check=True, timeout=300,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    return tmp


def _whisper_srt(audio: Path, language: str, key: str) -> str:
    """Llama Whisper API y devuelve el texto SRT."""
    import requests  # lazy import
    with audio.open("rb") as f:
        files = {"file": (audio.name, f, "audio/mpeg")}
        data = {
            "model": MODEL,
            "response_format": "srt",
            "language": language,
        }
        headers = {"Authorization": f"Bearer {key}"}
        r = requests.post(OPENAI_URL, headers=headers, files=files, data=data, timeout=600)
    if r.status_code != 200:
        raise RuntimeError(f"OpenAI API {r.status_code}: {r.text[:300]}")
    return r.text


def run(input_path: str, cliente: str, tipo: str, version: int,
        language: str = "es", out_dir: str | None = None) -> dict:
    master = Path(input_path)
    if not master.exists():
        return {"error": f"input no existe: {input_path}"}

    key = _load_key()
    if not key:
        return {"error": "OPENAI_API_KEY no encontrada (env o .env)", "skipped": True}

    base = _pascal_cliente(cliente)
    fecha = date.today().isoformat()
    out_root = Path(out_dir) if out_dir else (DEFAULT_OUT / cliente / fecha)
    out_root.mkdir(parents=True, exist_ok=True)
    out_file = out_root / f"{base}_{tipo}_V{version}.srt"

    audio = None
    try:
        audio = _extract_audio(master)
        srt_text = _whisper_srt(audio, language, key)
        out_file.write_text(srt_text, encoding="utf-8")
        return {
            "input": str(master),
            "language": language,
            "output": str(out_file.relative_to(ROOT)).replace("\\", "/"),
            "lines": len([l for l in srt_text.splitlines() if "-->" in l]),
        }
    except subprocess.CalledProcessError as e:
        return {"error": f"ffmpeg extract fallo: {e.stderr.decode('utf-8', 'ignore')[:200]}"}
    except Exception as e:
        return {"error": str(e)[:300]}
    finally:
        if audio and audio.exists():
            try:
                audio.unlink()
            except Exception:
                pass


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--cliente", required=True)
    p.add_argument("--tipo", required=True)
    p.add_argument("--version", type=int, default=1)
    p.add_argument("--language", default="es")
    p.add_argument("--out-dir")
    a = p.parse_args(argv)
    r = run(a.input, a.cliente, a.tipo, a.version, a.language, a.out_dir)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if "error" not in r else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
