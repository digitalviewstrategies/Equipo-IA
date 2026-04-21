"""
sheets_reader.py — Lee el Google Sheet de campanas de DV Media Buyer.

Requiere en .env:
    GOOGLE_SHEET_ID=...
    GOOGLE_CREDENTIALS_PATH=credentials/google_service_account.json

La service account necesita acceso de lectura al sheet y a los archivos de Drive
que esten referenciados en la columna Material.

Columnas esperadas en el sheet (case-insensitive):
    Cliente     -> cliente
    Direccion   -> direccion
    Material    -> material  (links de Drive separados por salto de linea o coma)
    Presupuesto -> presupuesto_usd (float, se limpian $, puntos y comas)
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
    "cliente": "cliente",
    "dirección": "direccion",
    "direccion": "direccion",
    "material": "material",
    "presupuesto": "presupuesto_usd",
}


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


def _clean_budget(raw: str) -> float:
    """Convierte '$ 1.500' o '1500,00' o '1500' a float."""
    cleaned = re.sub(r"[^\d,.]", "", raw)
    # Si tiene coma como separador decimal (1500,00) la convierte
    if "," in cleaned and "." not in cleaned:
        cleaned = cleaned.replace(",", ".")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        raise ValueError(f"No se pudo convertir '{raw}' a presupuesto numerico.")


def _parse_drive_links(raw: str) -> list[str]:
    """Extrae links de Google Drive de una celda. Soporta separacion por coma o newline."""
    separators = re.split(r"[\n,]+", raw)
    links = []
    for item in separators:
        item = item.strip()
        if "drive.google.com" in item or "docs.google.com" in item:
            links.append(item)
    return links


def _normalize_headers(row: list[str]) -> dict[int, str]:
    """Mapea indices de columna a nombres normalizados."""
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
) -> list[dict]:
    """
    Lee el sheet y devuelve lista de campanas a crear.

    Returns:
        Lista de dicts con keys: cliente, direccion, material (list[str]), presupuesto_usd.
        Salta filas vacias o sin cliente.
    """
    sheet_id = sheet_id or os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        raise ValueError(
            "GOOGLE_SHEET_ID no configurado. Agrega la variable al .env."
        )

    creds = _get_credentials(credentials_path)
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(sheet_id).get_worksheet(worksheet_index)
    all_rows = ws.get_all_values()

    if not all_rows:
        return []

    headers = _normalize_headers(all_rows[0])
    required = {"cliente", "direccion", "material", "presupuesto_usd"}
    found = set(headers.values())
    missing = required - found
    if missing:
        raise ValueError(
            f"Columnas faltantes en el sheet: {', '.join(sorted(missing))}. "
            f"Columnas encontradas: {', '.join(all_rows[0])}"
        )

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

        if not record.get("material"):
            print(f"  [SKIP] Fila {row_num} ({record['cliente']}): sin material.")
            continue

        try:
            record["presupuesto_usd"] = _clean_budget(record["presupuesto_usd"])
        except ValueError as e:
            print(f"  [SKIP] Fila {row_num} ({record['cliente']}): {e}")
            continue

        links = _parse_drive_links(record["material"])
        if not links:
            print(
                f"  [SKIP] Fila {row_num} ({record['cliente']}): "
                "no se encontraron links de Drive en Material."
            )
            continue
        record["material"] = links

        rows.append(record)

    return rows
