"""
sheets_reader.py — Lee el Google Sheet de campanas de DV Media Buyer.

Requiere en .env:
    GOOGLE_SHEET_ID=...
    GOOGLE_CREDENTIALS_PATH=credentials/google_service_account.json

Columnas del sheet (case-insensitive):
    Encargado             -> encargado
    Fecha de inicio       -> fecha_inicio
    Direccion             -> direccion        (nombre de campana)
    Cliente               -> cliente
    Material              -> material         (formatos: carrusel1x1 | video9x16 | ...)
    Ficha                 -> ficha            (link de la propiedad)
    Corredor inmobiliario -> corredor
    Estado                -> estado
    Presupuesto           -> presupuesto_raw  (ej: "40K x una semana")
    Comentarios Correcciones -> comentarios
    Prioridad             -> prioridad
"""

import os
import re
from pathlib import Path

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

_COLUMN_MAP = {
    "encargado": "encargado",
    "fecha de inicio": "fecha_inicio",
    "dirección": "direccion",
    "direccion": "direccion",
    "cliente": "cliente",
    "material": "material",
    "ficha": "ficha",
    "corredor inmobiliario": "corredor",
    "estado": "estado",
    "presupuesto": "presupuesto_raw",
    "comentarios correcciones": "comentarios",
    "prioridad": "prioridad",
}

# campana nueva con material listo
ESTADOS_NUEVA = {"material cargado"}
# campana existente a reactivar/repautar
ESTADOS_REPAUTAR = {"repautar"}
ESTADOS_ACTIVOS = ESTADOS_NUEVA | ESTADOS_REPAUTAR


def _get_credentials(credentials_path: str | None = None) -> Credentials:
    creds_path = credentials_path or os.getenv("GOOGLE_CREDENTIALS_PATH")
    if not creds_path:
        raise ValueError(
            "GOOGLE_CREDENTIALS_PATH no configurado. "
            "Agrega la variable al .env o pasa credentials_path al llamar la funcion."
        )
    full_path = Path(__file__).resolve().parent.parent / creds_path
    if not full_path.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo de credenciales en: {full_path}\n"
            "Descarga el JSON de la service account desde Google Cloud Console "
            "y guardalo en ese path."
        )
    return Credentials.from_service_account_file(str(full_path), scopes=SCOPES)


def _parse_presupuesto(raw: str) -> dict:
    """
    Parsea presupuesto en formato libre a valores utiles.

    Ejemplos:
        "40K x una semana"  -> {total_ars: 40000, periodo: "semana", diario_ars: 5714}
        "80k x dos semanas" -> {total_ars: 80000, periodo: "dos semanas", diario_ars: 5714}
        "20k x mes"         -> {total_ars: 20000, periodo: "mes", diario_ars: 667}

    Devuelve dict con raw original si no puede parsear.
    """
    raw_lower = raw.lower().strip()

    # Extraer monto (ej: 40k -> 40000, 40000)
    match_monto = re.search(r"(\d+(?:[.,]\d+)?)\s*k?", raw_lower)
    if not match_monto:
        return {"presupuesto_raw": raw}

    monto_str = match_monto.group(1).replace(",", ".")
    monto = float(monto_str)
    if "k" in raw_lower[match_monto.start():match_monto.end() + 1]:
        monto *= 1000

    # Determinar periodo en dias
    if "mes" in raw_lower:
        dias = 30
        periodo = "mes"
    elif "dos semanas" in raw_lower or "2 semanas" in raw_lower:
        dias = 14
        periodo = "dos semanas"
    elif "semana" in raw_lower:
        dias = 7
        periodo = "semana"
    else:
        dias = 7
        periodo = "semana"

    return {
        "presupuesto_raw": raw,
        "presupuesto_total_ars": int(monto),
        "presupuesto_periodo": periodo,
        "presupuesto_diario_ars": round(monto / dias),
    }


def _parse_formatos(raw: str) -> list[str]:
    """Extrae lista de formatos de Material. Separador: | o coma."""
    parts = re.split(r"[|\n,]+", raw)
    return [p.strip() for p in parts if p.strip()]


def _normalize_headers(row: list[str]) -> dict[int, str]:
    mapping = {}
    for i, header in enumerate(row):
        normalized = header.strip().lower()
        if normalized in _COLUMN_MAP:
            mapping[i] = _COLUMN_MAP[normalized]
    return mapping


def get_campaign_rows(
    sheet_id: str | None = None,
    credentials_path: str | None = None,
    worksheet_index: int = 0,
    solo_activos: bool = True,
) -> list[dict]:
    """
    Lee el sheet y devuelve lista de campanas a procesar.

    Args:
        solo_activos: Si True, solo devuelve filas con estado en ESTADOS_ACTIVOS.

    Returns:
        Lista de dicts con keys: encargado, fecha_inicio, direccion, cliente,
        material (list[str]), ficha, corredor, estado, presupuesto_raw,
        comentarios, prioridad.
        Salta filas sin cliente o sin direccion.
    """
    sheet_id = sheet_id or os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID no configurado. Agrega la variable al .env.")

    creds = _get_credentials(credentials_path)
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(sheet_id).get_worksheet(worksheet_index)
    all_rows = ws.get_all_values()

    if not all_rows:
        return []

    headers = _normalize_headers(all_rows[0])

    rows = []
    for row_num, row in enumerate(all_rows[1:], start=2):
        record: dict = {}
        for idx, key in headers.items():
            record[key] = row[idx].strip() if idx < len(row) else ""

        if not record.get("cliente"):
            continue

        if not record.get("direccion"):
            print(f"  [SKIP] Fila {row_num}: sin direccion.")
            continue

        estado = record.get("estado", "").lower()
        if solo_activos and estado not in ESTADOS_ACTIVOS:
            print(f"  [SKIP] Fila {row_num} ({record['cliente']} - {record['direccion']}): estado '{record.get('estado', '')}'.")
            continue

        formatos = _parse_formatos(record.get("material", ""))
        if not formatos:
            print(f"  [SKIP] Fila {row_num} ({record['cliente']}): sin formatos en Material.")
            continue
        record["material"] = formatos

        record["accion"] = "repautar" if estado in ESTADOS_REPAUTAR else "nueva"

        presupuesto = _parse_presupuesto(record.get("presupuesto_raw", ""))
        record.update(presupuesto)

        rows.append(record)

    return rows
