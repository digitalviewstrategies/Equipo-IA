"""Logs de conversacion en outputs/<cliente>/conversaciones/YYYY-MM-DD.jsonl."""
import json
from datetime import datetime
from . import config


def log(cliente: str | None, direction: str, from_number: str, text: str,
        intent: str | None = None, confidence: float | None = None,
        auto: bool | None = None) -> None:
    folder = config.OUTPUTS_DIR / (cliente or "_desconocido") / "conversaciones"
    folder.mkdir(parents=True, exist_ok=True)
    f = folder / f"{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"
    entry = {
        "ts": datetime.utcnow().isoformat(),
        "direction": direction,
        "from": from_number,
        "intent": intent,
        "confidence": confidence,
        "auto": auto,
        "text": text,
    }
    with f.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
