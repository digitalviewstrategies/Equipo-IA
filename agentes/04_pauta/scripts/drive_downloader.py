"""
drive_downloader.py — Descarga videos desde Google Drive para DV Media Buyer.

Usa la misma service account que sheets_reader.py.
Los archivos se descargan a una carpeta temporal local antes de subirse a Meta.
"""

import re
import tempfile
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def _extract_file_id(drive_url: str) -> str:
    """Extrae el file ID de un link de Google Drive."""
    patterns = [
        r"/file/d/([a-zA-Z0-9_-]+)",
        r"id=([a-zA-Z0-9_-]+)",
        r"/d/([a-zA-Z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, drive_url)
        if match:
            return match.group(1)
    raise ValueError(f"No se pudo extraer el file ID del link: {drive_url}")


def _get_drive_service(credentials_path: str):
    creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def detect_resolution(filename: str) -> str | None:
    """
    Detecta la resolucion por el nombre del archivo.
    Retorna '9x16', '1x1', o None si no se detecta.
    """
    name_lower = filename.lower()
    if "9x16" in name_lower:
        return "9x16"
    if "1x1" in name_lower:
        return "1x1"
    return None


def extract_base_name(filename: str) -> str:
    """
    Extrae el nombre base quitando sufijos de resolucion y extension.
    Ej: 'video_01_9x16.mp4' -> 'video_01'
    """
    stem = Path(filename).stem
    base = re.sub(r"[_\-]?(9x16|1x1)$", "", stem, flags=re.IGNORECASE)
    return base.strip("_-")


def download_video(drive_url: str, credentials_path: str, dest_dir: str | None = None) -> Path:
    """
    Descarga un video de Drive al disco local.

    Args:
        drive_url: URL del archivo en Drive.
        credentials_path: Path absoluto al JSON de service account.
        dest_dir: Carpeta destino. Si None, usa un directorio temporal.

    Returns:
        Path al archivo descargado.
    """
    file_id = _extract_file_id(drive_url)
    service = _get_drive_service(credentials_path)

    # Obtener metadata para saber el nombre del archivo
    metadata = service.files().get(fileId=file_id, fields="name,mimeType").execute()
    filename = metadata.get("name", f"{file_id}.mp4")

    if dest_dir:
        dest_path = Path(dest_dir) / filename
    else:
        tmp = tempfile.mkdtemp(prefix="dv_media_")
        dest_path = Path(tmp) / filename

    request = service.files().get_media(fileId=file_id)

    with open(dest_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request, chunksize=10 * 1024 * 1024)
        done = False
        while not done:
            _, done = downloader.next_chunk()

    return dest_path


def group_videos_by_creative(drive_links: list[str], credentials_path: str) -> list[dict]:
    """
    Agrupa los links de Drive por nombre base de creativo.

    Por cada link obtiene el nombre del archivo en Drive (sin descargarlo),
    extrae el nombre base y la resolucion, y agrupa.

    Returns:
        Lista de dicts, uno por creativo:
        {
            "base_name": str,
            "9x16": str | None,   # drive URL del vertical
            "1x1": str | None,    # drive URL del cuadrado
        }
    """
    service = _get_drive_service(credentials_path)
    groups: dict[str, dict] = {}

    for url in drive_links:
        try:
            file_id = _extract_file_id(url)
            metadata = service.files().get(fileId=file_id, fields="name").execute()
            filename = metadata.get("name", "")
        except Exception as e:
            print(f"    [WARN] No se pudo obtener metadata de {url}: {e}")
            continue

        resolution = detect_resolution(filename)
        if not resolution:
            print(
                f"    [WARN] No se detecta resolucion en '{filename}'. "
                "El nombre debe incluir '9x16' o '1x1'. Se omite."
            )
            continue

        base = extract_base_name(filename)
        if base not in groups:
            groups[base] = {"base_name": base, "9x16": None, "1x1": None}
        groups[base][resolution] = url

    return list(groups.values())
