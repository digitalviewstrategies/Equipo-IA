"""
output_manager.py — Gestion de outputs para el agente de Delivery y Reporting.

Lee datos del Media Buyer para construir reportes de cliente.
"""

import json
from datetime import date
from pathlib import Path

# scripts → 03_delivery_reporting → agentes → ROOT
ROOT_DIR = Path(__file__).resolve().parents[3]
BRANDS_DIR = ROOT_DIR / "shared" / "brands"
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"

PAUTA_OUTPUTS = ROOT_DIR / "agentes" / "04_pauta" / "outputs"
CREATIVE_OUTPUTS = ROOT_DIR / "agentes" / "01_contenido" / "creative_director" / "outputs"
DESIGN_OUTPUTS = ROOT_DIR / "agentes" / "01_contenido" / "design" / "output"
COPYWRITER_OUTPUTS = ROOT_DIR / "agentes" / "01_contenido" / "copywritter" / "outputs"


def list_brands() -> list[str]:
    if not BRANDS_DIR.exists():
        return []
    return [f.stem for f in sorted(BRANDS_DIR.glob("*.json")) if not f.stem.startswith("_")]


def load_brand(cliente: str) -> dict | None:
    path = BRANDS_DIR / f"{cliente}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_latest_pauta_output(cliente: str, tipo: str) -> Path | None:
    """
    Devuelve el output más reciente de un tipo dado del Media Buyer para un cliente.

    Args:
        tipo: prefijo del archivo (ej. 'reporte_semanal', 'reporte_mensual', 'analisis', 'brief_creativo')
    """
    cliente_dir = PAUTA_OUTPUTS / cliente
    if not cliente_dir.exists():
        return None
    for fecha_dir in sorted(cliente_dir.iterdir(), reverse=True):
        if not fecha_dir.is_dir():
            continue
        for archivo in sorted(fecha_dir.iterdir(), reverse=True):
            if archivo.is_file() and archivo.name.startswith(tipo):
                return archivo
    return None


def list_pauta_outputs(cliente: str, limit: int = 10) -> list[Path]:
    """Lista los outputs más recientes del Media Buyer para un cliente."""
    cliente_dir = PAUTA_OUTPUTS / cliente
    if not cliente_dir.exists():
        return []
    archivos = []
    for fecha_dir in sorted(cliente_dir.iterdir(), reverse=True):
        if not fecha_dir.is_dir():
            continue
        for archivo in sorted(fecha_dir.iterdir(), reverse=True):
            if archivo.is_file():
                archivos.append(archivo)
                if len(archivos) >= limit:
                    return archivos
    return archivos


def get_phase_outputs(cliente: str) -> dict[str, list[Path]]:
    """
    Devuelve todos los outputs por agente para usar en el checklist de fases.
    """
    result = {
        "creative_director": [],
        "copywriter": [],
        "design": [],
        "pauta": [],
    }

    for agent_name, base_dir in [
        ("creative_director", CREATIVE_OUTPUTS),
        ("copywriter", COPYWRITER_OUTPUTS),
        ("design", DESIGN_OUTPUTS),
        ("pauta", PAUTA_OUTPUTS),
    ]:
        cliente_dir = base_dir / cliente
        if not cliente_dir.exists():
            continue
        for fecha_dir in sorted(cliente_dir.iterdir(), reverse=True):
            if not fecha_dir.is_dir():
                continue
            for archivo in sorted(fecha_dir.rglob("*")):
                if archivo.is_file():
                    result[agent_name].append(archivo)

    return result


PHASE_NAMES = {
    1: "Comercial",
    2: "Onboarding",
    3: "Preproduccion",
    4: "Produccion",
    5: "Pauta",
    6: "Seguimiento",
}

PHASE_RESPONSABLE = {
    1: "Valentin",
    2: "Elias",
    3: "Nico",
    4: "Nico / Editores",
    5: "Felipe",
    6: "Elias",
}


def _phase_definition(fase: int) -> list[dict]:
    """
    Entregables verificables por fase. Cada item: {id, label, check, responsable, criticidad}.
    `check` es 'auto' (verificable contra repo) o 'manual' (requiere confirmacion humana).
    `criticidad` es 'critica' (bloquea avance / la prox semana frena) o 'normal'.
    """
    if fase == 1:
        return [
            {"id": "propuesta_aceptada", "label": "Propuesta aceptada", "check": "manual", "responsable": "Valentin", "criticidad": "critica"},
            {"id": "contrato_firmado", "label": "Contrato firmado", "check": "manual", "responsable": "Valentin", "criticidad": "critica"},
            {"id": "fee_recibido", "label": "Fee inicial recibido o comprometido", "check": "manual", "responsable": "Valentin", "criticidad": "critica"},
            {"id": "presupuesto_pauta", "label": "Presupuesto de pauta confirmado (min USD 300/mes)", "check": "auto:brand.meta_ads.monthly_budget_usd", "responsable": "Valentin", "criticidad": "critica"},
        ]
    if fase == 2:
        return [
            {"id": "brand_json", "label": "Brand JSON creado en shared/brands/", "check": "auto:brand", "responsable": "Elias", "criticidad": "critica"},
            {"id": "ad_account_id", "label": "Ad Account ID confirmado", "check": "auto:brand.meta_ads.ad_account_id", "responsable": "Elias", "criticidad": "critica"},
            {"id": "page_id", "label": "Page ID de Facebook confirmado", "check": "auto:brand.meta_ads.page_id", "responsable": "Elias", "criticidad": "critica"},
            {"id": "colors", "label": "Identidad visual cargada (colors)", "check": "auto:brand.colors", "responsable": "Elias", "criticidad": "normal"},
            {"id": "buyer_persona", "label": "Buyer persona / target_audience definido", "check": "auto:brand.target_audience", "responsable": "Elias", "criticidad": "normal"},
            {"id": "drive_estructurado", "label": "Carpeta de Drive completa (00 a 05)", "check": "manual", "responsable": "Bauti R", "criticidad": "normal"},
        ]
    if fase == 3:
        return [
            {"id": "guiones", "label": "Guiones aprobados por Nico", "check": "auto:outputs.creative_director.guion", "responsable": "Nico", "criticidad": "critica"},
            {"id": "copy", "label": "Copy de Meta Ads generado", "check": "auto:outputs.copywriter.copy", "responsable": "Copywriter", "criticidad": "critica"},
            {"id": "piezas_diseno", "label": "Piezas de diseno renderizadas", "check": "auto:outputs.design", "responsable": "Design", "criticidad": "normal"},
        ]
    if fase == 4:
        return [
            {"id": "videos_editados", "label": "Videos editados y aprobados en Drive", "check": "manual", "responsable": "Nico", "criticidad": "critica"},
            {"id": "nomenclatura", "label": "Nomenclatura correcta CLIENTE_Tipo_Vn", "check": "manual", "responsable": "Editores", "criticidad": "normal"},
        ]
    if fase == 5:
        return [
            {"id": "plan_campana", "label": "Plan de campana aprobado por Felipe", "check": "auto:outputs.pauta.plan_campana", "responsable": "Felipe", "criticidad": "critica"},
            {"id": "creativos_subidos", "label": "Creativos subidos a Meta", "check": "manual", "responsable": "Felipe", "criticidad": "critica"},
            {"id": "campana_activa", "label": "Campana activada en Meta (ACTIVE)", "check": "manual", "responsable": "Felipe", "criticidad": "critica"},
            {"id": "lead_form_testeado", "label": "Lead form testeado antes de escalar", "check": "manual", "responsable": "Felipe", "criticidad": "critica"},
        ]
    if fase == 6:
        return [
            {"id": "analisis_semanal", "label": "Analisis semanal corrido por Media Buyer", "check": "auto:outputs.pauta.analisis", "responsable": "Felipe", "criticidad": "critica"},
            {"id": "reporte_semanal", "label": "Reporte semanal del Media Buyer disponible", "check": "auto:outputs.pauta.reporte_semanal", "responsable": "Felipe", "criticidad": "critica"},
            {"id": "reporte_enviado", "label": "Reporte semanal enviado al cliente", "check": "manual", "responsable": "Elias", "criticidad": "normal"},
        ]
    return []


def _resolve_check(check: str, brand: dict | None, outputs: dict[str, list[Path]]) -> bool | None:
    """Devuelve True/False si se puede verificar automaticamente, None si es manual."""
    if check == "manual":
        return None
    if not check.startswith("auto:"):
        return None
    target = check[5:]

    if target == "brand":
        return brand is not None

    if target.startswith("brand."):
        if brand is None:
            return False
        # ej: brand.meta_ads.ad_account_id
        keys = target.split(".")[1:]
        cursor = brand
        for k in keys:
            if not isinstance(cursor, dict) or k not in cursor:
                return False
            cursor = cursor[k]
        return bool(cursor)

    if target.startswith("outputs."):
        # ej: outputs.creative_director.guion  / outputs.pauta.reporte_semanal / outputs.design
        parts = target.split(".")
        agente = parts[1]
        prefijo = parts[2] if len(parts) > 2 else None
        archivos = outputs.get(agente, [])
        if prefijo:
            return any(p.name.startswith(prefijo) for p in archivos)
        return len(archivos) > 0

    return None


def infer_active_phase(cliente: str) -> int:
    """Infiere la fase activa del cliente segun outputs presentes."""
    outputs = get_phase_outputs(cliente)
    if any(p.name.startswith("reporte_semanal") for p in outputs.get("pauta", [])):
        return 6
    if any(p.name.startswith("plan_campana") for p in outputs.get("pauta", [])):
        return 5
    if outputs.get("design"):
        return 4
    if outputs.get("creative_director") or outputs.get("copywriter"):
        return 3
    if load_brand(cliente):
        return 2
    return 1


def get_phase_gaps(cliente: str, fase: int | None = None) -> dict:
    """
    Evalua los entregables de la fase y devuelve los gaps detectados.

    Returns:
        {
            "fase": int,
            "fase_nombre": str,
            "items": [{id, label, status, responsable, criticidad}, ...],
            "gaps": [items con status != 'ok'],  # solo los faltantes
            "gaps_criticos": [items criticos faltantes],
            "puede_avanzar": bool,
        }
    `status` es 'ok' | 'falta' | 'manual' (no verificable automaticamente).
    """
    if fase is None:
        fase = infer_active_phase(cliente)

    brand = load_brand(cliente)
    outputs = get_phase_outputs(cliente)
    definition = _phase_definition(fase)

    items = []
    for entregable in definition:
        resultado = _resolve_check(entregable["check"], brand, outputs)
        if resultado is True:
            status = "ok"
        elif resultado is False:
            status = "falta"
        else:
            status = "manual"
        items.append({**entregable, "status": status})

    gaps = [it for it in items if it["status"] != "ok"]
    gaps_criticos = [it for it in gaps if it["criticidad"] == "critica" and it["status"] == "falta"]

    return {
        "fase": fase,
        "fase_nombre": PHASE_NAMES.get(fase, f"Fase {fase}"),
        "items": items,
        "gaps": gaps,
        "gaps_criticos": gaps_criticos,
        "puede_avanzar": len(gaps_criticos) == 0,
    }


def save_output(cliente: str, tipo: str, nombre: str, contenido: str) -> Path:
    """Guarda un output de delivery/reporting."""
    fecha = date.today().isoformat()
    dir_destino = OUTPUTS_DIR / cliente / fecha
    dir_destino.mkdir(parents=True, exist_ok=True)
    path = dir_destino / f"{tipo}_{nombre}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(contenido)
    return path


if __name__ == "__main__":
    print("Clientes disponibles:")
    for b in list_brands():
        print(f"  - {b}")
    print(f"\nRaiz del proyecto: {ROOT_DIR}")
    print(f"Pauta outputs: {PAUTA_OUTPUTS}")
    print(f"Delivery outputs: {OUTPUTS_DIR}")
