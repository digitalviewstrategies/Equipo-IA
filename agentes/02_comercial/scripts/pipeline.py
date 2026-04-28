"""
pipeline.py — Gestión del pipeline comercial de DV.

Almacena y consulta el estado de todos los prospectos en un JSON local.
"""

import json
import uuid
from datetime import date
from pathlib import Path

# scripts → 02_comercial → agentes → ROOT
PIPELINE_FILE = Path(__file__).resolve().parent.parent / "data" / "pipeline.json"

ETAPAS_VALIDAS = [
    "pre_filtro",
    "fit_call",
    "discovery",
    "scoring",
    "propuesta",
    "negociacion",
    "cerrado_ganado",
    "cerrado_perdido",
]

TIPOS_VALIDOS = ["agencia_pequena", "top_producer", "desarrollador", "otro"]
ZONAS_VALIDAS = ["CABA", "GBA_norte", "GBA_otro", "interior", "desconocida"]


def _load() -> dict:
    if not PIPELINE_FILE.exists():
        PIPELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
        return {"prospectos": []}
    with open(PIPELINE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    PIPELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PIPELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_prospecto(
    nombre: str,
    empresa: str = "",
    tipo: str = "otro",
    zona: str = "desconocida",
    telefono: str = "",
    email: str = "",
    fuente: str = "",
    notas: str = "",
) -> dict:
    """Agrega un prospecto nuevo al pipeline en etapa pre_filtro."""
    data = _load()
    prospecto = {
        "id": str(uuid.uuid4())[:8],
        "nombre": nombre,
        "empresa": empresa,
        "tipo": tipo if tipo in TIPOS_VALIDOS else "otro",
        "zona": zona if zona in ZONAS_VALIDAS else "desconocida",
        "telefono": telefono,
        "email": email,
        "fuente": fuente,
        "etapa": "pre_filtro",
        "puntaje_scorecard": None,
        "clasificacion": None,
        "red_flags": [],
        "fecha_ingreso": date.today().isoformat(),
        "fecha_ultima_actualizacion": date.today().isoformat(),
        "notas": notas,
        "outputs": [],
    }
    data["prospectos"].append(prospecto)
    _save(data)
    return prospecto


def get_prospecto(nombre_o_id: str) -> dict | None:
    """Busca un prospecto por nombre (parcial) o ID."""
    data = _load()
    busqueda = nombre_o_id.lower()
    for p in data["prospectos"]:
        if p["id"] == busqueda:
            return p
        if busqueda in p["nombre"].lower() or busqueda in p["empresa"].lower():
            return p
    return None


def update_etapa(nombre_o_id: str, nueva_etapa: str) -> dict | None:
    """Avanza o retrocede la etapa de un prospecto."""
    if nueva_etapa not in ETAPAS_VALIDAS:
        raise ValueError(f"Etapa inválida: {nueva_etapa}. Válidas: {ETAPAS_VALIDAS}")
    data = _load()
    for p in data["prospectos"]:
        if p["id"] == nombre_o_id or nombre_o_id.lower() in p["nombre"].lower():
            p["etapa"] = nueva_etapa
            p["fecha_ultima_actualizacion"] = date.today().isoformat()
            _save(data)
            return p
    return None


def update_scoring(
    nombre_o_id: str,
    puntaje: int,
    clasificacion: str,
    red_flags: list[str] | None = None,
) -> dict | None:
    """Actualiza el scorecard de un prospecto."""
    data = _load()
    for p in data["prospectos"]:
        if p["id"] == nombre_o_id or nombre_o_id.lower() in p["nombre"].lower():
            p["puntaje_scorecard"] = puntaje
            p["clasificacion"] = clasificacion
            if red_flags:
                p["red_flags"] = red_flags
            p["fecha_ultima_actualizacion"] = date.today().isoformat()
            _save(data)
            return p
    return None


def add_nota(nombre_o_id: str, nota: str) -> dict | None:
    """Agrega una nota a un prospecto."""
    data = _load()
    for p in data["prospectos"]:
        if p["id"] == nombre_o_id or nombre_o_id.lower() in p["nombre"].lower():
            fecha = date.today().isoformat()
            if p["notas"]:
                p["notas"] += f"\n\n[{fecha}] {nota}"
            else:
                p["notas"] = f"[{fecha}] {nota}"
            p["fecha_ultima_actualizacion"] = fecha
            _save(data)
            return p
    return None


def list_pipeline(etapa: str | None = None, activos_only: bool = True) -> list[dict]:
    """
    Lista prospectos del pipeline.

    Args:
        etapa: filtrar por etapa específica.
        activos_only: si True, excluye cerrado_ganado y cerrado_perdido.
    """
    data = _load()
    prospectos = data["prospectos"]

    if activos_only:
        prospectos = [
            p for p in prospectos
            if p["etapa"] not in ("cerrado_ganado", "cerrado_perdido")
        ]

    if etapa:
        prospectos = [p for p in prospectos if p["etapa"] == etapa]

    return sorted(prospectos, key=lambda p: p["fecha_ultima_actualizacion"], reverse=True)


def pipeline_summary() -> dict:
    """Devuelve un resumen del pipeline por etapa."""
    data = _load()
    summary = {etapa: [] for etapa in ETAPAS_VALIDAS}
    for p in data["prospectos"]:
        etapa = p.get("etapa", "pre_filtro")
        if etapa in summary:
            summary[etapa].append(p)
    return summary


def format_pipeline_report() -> str:
    """Genera un reporte textual del pipeline para mostrar en pantalla."""
    summary = pipeline_summary()
    activos = [
        etapa for etapa in ETAPAS_VALIDAS
        if etapa not in ("cerrado_ganado", "cerrado_perdido")
    ]

    lineas = ["# Pipeline Comercial DV", f"**Actualizado:** {date.today().isoformat()}", ""]

    etapas_display = {
        "pre_filtro": "Pre-filtro",
        "fit_call": "Fit Call",
        "discovery": "Discovery Call",
        "scoring": "Scoring",
        "propuesta": "Propuesta enviada",
        "negociacion": "Negociación",
        "cerrado_ganado": "Cerrados (ganados)",
        "cerrado_perdido": "Cerrados (perdidos)",
    }

    total_activos = sum(len(summary[e]) for e in activos)
    lineas.append(f"**Prospectos activos:** {total_activos}")
    lineas.append("")

    for etapa in activos:
        prospectos = summary[etapa]
        if not prospectos:
            continue
        lineas.append(f"## {etapas_display[etapa]} ({len(prospectos)})")
        for p in prospectos:
            score_str = f" — Score: {p['puntaje_scorecard']}/41 ({p['clasificacion']})" if p["puntaje_scorecard"] else ""
            lineas.append(f"- **{p['nombre']}** ({p['empresa']}) | {p['zona']}{score_str}")
            if p.get("notas"):
                ultima_nota = p["notas"].split("\n\n")[-1]
                lineas.append(f"  Nota: {ultima_nota[:100]}{'...' if len(ultima_nota) > 100 else ''}")
        lineas.append("")

    # Cerrados del mes
    ganados = summary["cerrado_ganado"]
    perdidos = summary["cerrado_perdido"]
    if ganados or perdidos:
        lineas.append(f"## Cerrados — Ganados ({len(ganados)}) / Perdidos ({len(perdidos)})")
        for p in ganados:
            lineas.append(f"- [GANADO] **{p['nombre']}** ({p['empresa']})")
        for p in perdidos:
            lineas.append(f"- [PERDIDO] **{p['nombre']}** ({p['empresa']})")

    return "\n".join(lineas)
