"""
leads_clientes.py — Pipeline B2C por cliente.

Cada cliente DV (inmobiliaria/top producer) tiene su propio store de
leads que vienen de su pauta de Meta. Distinto de `pipeline.py`, que
es el pipeline B2B para vender el servicio DV.

Modelo:
- Estado simple (nuevo, contactado, agendado, descalificado, ganado, perdido)
- KPIs: tiempo_primera_respuesta, tiempo_a_agendado
- Sin scorecard 41pt (eso es B2B)

Storage: data/leads_clientes/<cliente>.json
"""
from __future__ import annotations

import json
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "leads_clientes"

ESTADOS_VALIDOS = [
    "nuevo",
    "contactado",
    "agendado",
    "descalificado",
    "ganado",
    "perdido",
]


def _path(cliente: str) -> Path:
    return DATA_DIR / f"{cliente}.json"


def _load(cliente: str) -> dict:
    p = _path(cliente)
    if not p.exists():
        return {"cliente": cliente, "leads": []}
    return json.loads(p.read_text(encoding="utf-8"))


def _save(cliente: str, data: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    _path(cliente).write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def already_imported(cliente: str, meta_lead_id: str) -> bool:
    if not meta_lead_id:
        return False
    for l in _load(cliente).get("leads", []):
        if l.get("meta_lead_id") == meta_lead_id:
            return True
    return False


def add_lead(
    cliente: str,
    nombre: str,
    telefono: str = "",
    email: str = "",
    meta_lead_id: str = "",
    meta_campaign_id: str = "",
    meta_ad_id: str = "",
    meta_form_id: str = "",
    fuente: str = "",
    notas: str = "",
    raw_field_data: dict | None = None,
) -> dict:
    """Agrega lead nuevo en estado 'nuevo'. Idempotente por meta_lead_id."""
    data = _load(cliente)
    if meta_lead_id and already_imported(cliente, meta_lead_id):
        for l in data["leads"]:
            if l.get("meta_lead_id") == meta_lead_id:
                return l

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lead = {
        "id": str(uuid.uuid4())[:8],
        "cliente": cliente,
        "nombre": nombre,
        "telefono": telefono,
        "email": email,
        "meta_lead_id": meta_lead_id,
        "meta_campaign_id": meta_campaign_id,
        "meta_ad_id": meta_ad_id,
        "meta_form_id": meta_form_id,
        "fuente": fuente or f"meta_lead_ads:{cliente}",
        "estado": "nuevo",
        "fecha_ingreso": now,
        "fecha_ultima_actualizacion": now,
        "primera_respuesta_ts": None,
        "agendado_ts": None,
        "cerrado_ts": None,
        "notas": notas,
        "raw_field_data": raw_field_data or {},
    }
    data["leads"].append(lead)
    _save(cliente, data)
    return lead


def update_estado(cliente: str, lead_id: str, nuevo_estado: str, nota: str = "") -> dict | None:
    if nuevo_estado not in ESTADOS_VALIDOS:
        raise ValueError(f"Estado invalido: {nuevo_estado}. Validos: {ESTADOS_VALIDOS}")
    data = _load(cliente)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for l in data["leads"]:
        if l["id"] == lead_id or l.get("meta_lead_id") == lead_id:
            l["estado"] = nuevo_estado
            l["fecha_ultima_actualizacion"] = now
            if nuevo_estado == "contactado" and not l.get("primera_respuesta_ts"):
                l["primera_respuesta_ts"] = now
            if nuevo_estado == "agendado":
                l["agendado_ts"] = now
            if nuevo_estado in ("ganado", "perdido", "descalificado"):
                l["cerrado_ts"] = now
            if nota:
                fecha = date.today().isoformat()
                l["notas"] = (l.get("notas", "") + f"\n[{fecha}] {nota}").strip()
            _save(cliente, data)
            return l
    return None


def list_leads(cliente: str, estado: str | None = None) -> list[dict]:
    data = _load(cliente)
    leads = data.get("leads", [])
    if estado:
        leads = [l for l in leads if l.get("estado") == estado]
    return sorted(leads, key=lambda l: l.get("fecha_ingreso", ""), reverse=True)


def listar_clientes() -> list[str]:
    if not DATA_DIR.exists():
        return []
    return sorted(p.stem for p in DATA_DIR.glob("*.json"))


def summary_cliente(cliente: str) -> dict:
    data = _load(cliente)
    leads = data.get("leads", [])
    by_estado = {e: 0 for e in ESTADOS_VALIDOS}
    for l in leads:
        by_estado[l.get("estado", "nuevo")] = by_estado.get(l.get("estado", "nuevo"), 0) + 1
    return {
        "cliente": cliente,
        "total": len(leads),
        "por_estado": by_estado,
    }
