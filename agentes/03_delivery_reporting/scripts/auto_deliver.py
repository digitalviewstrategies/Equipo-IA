"""
Hook PostToolUse handler.

Cuando el agente de pauta escribe un reporte (reporte_semanal_*.md, reporte_mensual_*.md
o analisis_*.md en agentes/04_pauta/outputs/<cliente>/<fecha>/), dispara un subproceso
claude headless que ejecuta la skill correspondiente del agente 03_delivery_reporting
con envio automatico a WhatsApp.

Idempotente: si el mismo path ya disparo hace <60s, lo ignora.
No bloqueante: spawnea el subproceso y sale inmediatamente (exit 0).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DELIVERY_ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = DELIVERY_ROOT / "outputs" / "_auto_deliver.log"
DEDUP_FILE = DELIVERY_ROOT / "outputs" / "_auto_deliver_dedup.json"
DEDUP_WINDOW_SECONDS = 60

PATH_RE = re.compile(
    r"agentes[\\/]04_pauta[\\/]outputs[\\/](?P<cliente>[^\\/]+)[\\/](?P<fecha>[^\\/]+)[\\/](?P<file>(reporte_semanal|reporte_mensual|analisis)_[^\\/]+\.md)$"
)


def log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {msg}\n")


def load_dedup() -> dict:
    if not DEDUP_FILE.exists():
        return {}
    try:
        return json.loads(DEDUP_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_dedup(data: dict) -> None:
    DEDUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    DEDUP_FILE.write_text(json.dumps(data), encoding="utf-8")


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except Exception:
        return 0  # nunca bloquear

    tool = payload.get("tool_name", "")
    if tool not in ("Write", "Edit"):
        return 0

    file_path = (
        payload.get("tool_response", {}).get("filePath")
        or payload.get("tool_input", {}).get("file_path", "")
    )
    if not file_path:
        return 0

    norm = str(file_path).replace("\\", "/")
    m = PATH_RE.search(norm.replace("/", "\\"))
    if not m:
        # intento con separador unix
        m = PATH_RE.search(norm)
        if not m:
            return 0

    cliente = m.group("cliente")
    fname = m.group("file")
    tipo = "mensual" if fname.startswith("reporte_mensual") else "semanal"

    # Dedup
    now = time.time()
    dedup = {k: v for k, v in load_dedup().items() if now - v < DEDUP_WINDOW_SECONDS}
    if file_path in dedup:
        log(f"DEDUP skip {file_path}")
        save_dedup(dedup)
        return 0
    dedup[file_path] = now
    save_dedup(dedup)

    prompt = (
        f"Ejecuta /reporte-{tipo} {cliente}. "
        f"Al terminar, enviá automáticamente el bloque WhatsApp generado a Elias usando "
        f"`from scripts.wa_reportes import send_to_elias; send_to_elias(mensaje_wa)`. "
        f"No pidas confirmación."
    )

    cmd = ["claude", "-p", prompt]
    log(f"FIRE cliente={cliente} tipo={tipo} file={file_path}")

    try:
        # Spawn no bloqueante: el hook async:true ya corre en background,
        # pero ademas spawneamos detached para no atar el proceso del hook a la sesion claude.
        subprocess.Popen(
            cmd,
            cwd=str(DELIVERY_ROOT),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "DETACHED_PROCESS", 0)
            | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
    except Exception as e:
        log(f"SPAWN_ERROR {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
