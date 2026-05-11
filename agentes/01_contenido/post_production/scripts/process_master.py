"""
process_master.py — Orquesta multiformat + thumbnail + subtitles sobre un master.

Uso:
    python process_master.py --input master.mp4 --cliente lopez_propiedades \
        --tipo RecorridoVO --version 1 [--thumb-at 3.0] [--transcribe] \
        [--language es] [--profiles 9x16 1x1 16x9]

Si --transcribe falta, NO llama a Whisper API. Sin OPENAI_API_KEY tampoco.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import multiformat  # type: ignore
import thumbnail    # type: ignore
import subtitles    # type: ignore


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--cliente", required=True)
    p.add_argument("--tipo", required=True)
    p.add_argument("--version", type=int, default=1)
    p.add_argument("--out-dir")
    p.add_argument("--thumb-at", type=float, default=1.0)
    p.add_argument("--profiles", nargs="*",
                   choices=list(multiformat.PROFILES))
    p.add_argument("--transcribe", action="store_true")
    p.add_argument("--language", default="es")
    a = p.parse_args(argv)

    common = dict(input_path=a.input, cliente=a.cliente, tipo=a.tipo,
                  version=a.version, out_dir=a.out_dir)

    result = {
        "multiformat": multiformat.run(profiles=a.profiles, **common),
        "thumbnail":   thumbnail.run(at=a.thumb_at, **common),
    }
    if a.transcribe:
        result["subtitles"] = subtitles.run(language=a.language, **common)
    else:
        result["subtitles"] = {"skipped": "use --transcribe to enable"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
    failed = any(
        isinstance(v, dict) and v.get("error") for v in result.values()
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
