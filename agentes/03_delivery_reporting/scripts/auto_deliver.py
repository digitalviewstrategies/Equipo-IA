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
AUTO_APPROVE = REPO_ROOT / ".claude" / "scripts" / "auto_approve.py"


def _check_sidecar_gate(path: Path) -> tuple[bool, dict | None]:
    """Devuelve (puede_disparar, sidecar_dict).

    Corre auto_approve si el sidecar no existe. Bloquea si status != ready_for_handoff.
    Si no hay brand resoluble o el sidecar no se puede generar, deja pasar (fail-open
    para no romper el pipeline existente; queda visible en log).
    """
    sidecar = path.with_suffix(path.suffix + ".status.json")
    if not sidecar.exists():
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("auto_approve", AUTO_APPROVE)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            cliente = path.parts[-3] if len(path.parts) >= 3 else None
            fecha = path.parts[-2] if len(path.parts) >= 2 else None
            if cliente and fecha:
                mod.run(cliente, fecha, False)
        except Exception as e:
            log(f"SIDECAR_GEN_ERROR {path.name}: {e}")
            return True, None
    if not sidecar.exists():
        return True, None
    try:
        sc = json.loads(sidecar.read_text(encoding="utf-8"))
    except Exception:
        return True, None
    return sc.get("status") == "ready_for_handoff", sc


def _alert_felipe_blocked(path: Path, sidecar: dict) -> None:
    """Alerta a Felipe que un reporte fue bloqueado por validators."""
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv(DELIVERY_ROOT / ".env")
        felipe = os.getenv("FELIPE_WA_NUMBER")
        if not felipe:
            log(f"BLOCKED_NO_FELIPE_NUMBER {path.name}")
            return
        sys.path.insert(0, str(DELIVERY_ROOT / "scripts"))
        import wa_reportes  # type: ignore
        viols = (sidecar.get("validators", {}).get("tono", {}) or {}).get("violations", [])
        msg = (
            "[DV] Auto-deliver BLOQUEADO\n\n"
            f"Reporte: {path.relative_to(REPO_ROOT)}\n"
            f"Violaciones tono: {', '.join(viols[:5]) or 'ver sidecar'}\n\n"
            "No se disparo a Elias. Revisar reporte o forbidden_words."
        )
        wa_reportes.send_text(felipe, msg)
        log(f"BLOCKED_ALERTED_FELIPE {path.name}")
    except Exception as e:
        log(f"ALERT_FELIPE_ERROR {e}")

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


def trigger_for_path(file_path: str) -> bool:
    """Dispara auto_deliver para un path. Reusable por hook y por cron."""
    if not file_path:
        return False

    norm = str(file_path).replace("\\", "/")
    m = PATH_RE.search(norm.replace("/", "\\"))
    if not m:
        m = PATH_RE.search(norm)
        if not m:
            return False

    cliente = m.group("cliente")
    fname = m.group("file")
    tipo = "mensual" if fname.startswith("reporte_mensual") else "semanal"

    now = time.time()
    dedup = {k: v for k, v in load_dedup().items() if now - v < DEDUP_WINDOW_SECONDS}
    if file_path in dedup:
        log(f"DEDUP skip {file_path}")
        save_dedup(dedup)
        return False
    dedup[file_path] = now
    save_dedup(dedup)

    # Gate: validators del sidecar
    can_fire, sc = _check_sidecar_gate(Path(file_path))
    if not can_fire:
        log(f"BLOCKED_BY_SIDECAR cliente={cliente} tipo={tipo} file={file_path}")
        if sc:
            _alert_felipe_blocked(Path(file_path), sc)
        return False

    prompt = (
        f"Ejecuta /reporte-{tipo} {cliente}. "
        f"Al terminar, enviá automáticamente el bloque WhatsApp generado a Elias usando "
        f"`from scripts.wa_reportes import send_to_elias; send_to_elias(mensaje_wa)`. "
        f"No pidas confirmación."
    )

    cmd = ["claude", "-p", prompt]
    log(f"FIRE cliente={cliente} tipo={tipo} file={file_path}")

    try:
        subprocess.Popen(
            cmd,
            cwd=str(DELIVERY_ROOT),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "DETACHED_PROCESS", 0)
            | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
        )
        return True
    except Exception as e:
        log(f"SPAWN_ERROR {e}")
        return False


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except Exception:
        return 0

    if payload.get("tool_name", "") not in ("Write", "Edit"):
        return 0

    file_path = (
        payload.get("tool_response", {}).get("filePath")
        or payload.get("tool_input", {}).get("file_path", "")
    )
    trigger_for_path(file_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
