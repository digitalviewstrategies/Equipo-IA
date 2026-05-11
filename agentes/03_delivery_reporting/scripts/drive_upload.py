"""
drive_upload.py - Sube PDFs a Drive via OAuth user delegated (no SA).

Por que no usamos service account: los SAs no tienen storage quota propio en
Drive personal. OAuth user delegated permite subir como el dueno del Drive
(probaosfelipe@gmail.com) sin limitaciones.

Setup (una sola vez):
  1. GCP Console -> Credenciales -> Crear OAuth Client (Desktop app).
  2. Descargar JSON a: agentes/03_delivery_reporting/credentials/oauth_client.json
  3. Correr: python drive_upload.py --auth
     Esto abre browser, pedis consentimiento, guarda token.json local.

Uso (cada vez que subis):
  python drive_upload.py --file path/to/x.pdf --cliente digital_view \
      --name "Reporte Digital View 2026-05-11.pdf"

Devuelve JSON con file_id y share_url permanente.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).resolve().parents[3]
DELIVERY_ROOT = Path(__file__).resolve().parents[1]
CRED_DIR = DELIVERY_ROOT / "credentials"
OAUTH_CLIENT = CRED_DIR / "oauth_client.json"
TOKEN_FILE = CRED_DIR / "drive_token.json"

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def _load_credentials() -> Credentials:
    """Carga creds desde token.json, refresca si vencidas. Si no hay token, corre OAuth flow."""
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        return creds
    if not OAUTH_CLIENT.exists():
        raise FileNotFoundError(
            f"Falta {OAUTH_CLIENT}. Descargalo de GCP Console (OAuth Desktop client) "
            f"o usa --auth para guiarme."
        )
    flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_CLIENT), SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True, prompt="consent")
    CRED_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    return creds


def _resolve_folder_for_cliente(svc, cliente: str) -> str | None:
    """Lee shared/brands/<cliente>.json y devuelve drive_folder_id si esta definido."""
    bp = ROOT / "shared" / "brands" / f"{cliente}.json"
    if not bp.exists():
        return None
    try:
        d = json.loads(bp.read_text(encoding="utf-8"))
        folder = (d.get("reporting") or {}).get("canva", {}).get("drive_folder_id")
        if folder and folder != "<TODO_KICKOFF>":
            # Verificar acceso
            try:
                svc.files().get(fileId=folder, fields="id,name", supportsAllDrives=True).execute()
                return folder
            except Exception:
                return None
    except Exception:
        pass
    return None


def upload(file_path: str, cliente: str, name: str | None = None,
           folder_id: str | None = None, make_public: bool = True) -> dict:
    creds = _load_credentials()
    svc = build("drive", "v3", credentials=creds, cache_discovery=False)

    src = Path(file_path)
    if not src.exists():
        return {"error": f"no existe: {file_path}"}

    final_name = name or src.name
    parent = folder_id or _resolve_folder_for_cliente(svc, cliente)

    body = {"name": final_name}
    if parent:
        body["parents"] = [parent]

    media = MediaFileUpload(str(src), mimetype="application/pdf", resumable=False)
    file = svc.files().create(
        body=body, media_body=media,
        fields="id,name,webViewLink,webContentLink,parents",
        supportsAllDrives=True,
    ).execute()

    if make_public:
        svc.permissions().create(
            fileId=file["id"],
            body={"role": "reader", "type": "anyone"},
            supportsAllDrives=True,
        ).execute()

    file_full = svc.files().get(
        fileId=file["id"],
        fields="id,name,webViewLink,webContentLink,parents,owners",
        supportsAllDrives=True,
    ).execute()

    return {
        "file_id": file_full["id"],
        "name": file_full["name"],
        "webViewLink": file_full.get("webViewLink"),
        "webContentLink": file_full.get("webContentLink"),
        "parents": file_full.get("parents"),
        "owner": (file_full.get("owners") or [{}])[0].get("emailAddress"),
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--auth", action="store_true", help="Corre OAuth flow y guarda token")
    p.add_argument("--file", help="Path al PDF a subir")
    p.add_argument("--cliente", help="brand_id del cliente (resuelve drive_folder_id)")
    p.add_argument("--name", help="Nombre del archivo en Drive (default: nombre original)")
    p.add_argument("--folder", help="Override del folder_id de destino")
    p.add_argument("--private", action="store_true", help="No hacer publico el link")
    a = p.parse_args(argv)

    if a.auth:
        try:
            creds = _load_credentials()
            print(json.dumps({"status": "ok", "valid": creds.valid, "token_path": str(TOKEN_FILE)}, indent=2))
            return 0
        except Exception as e:
            print(json.dumps({"status": "error", "msg": str(e)[:300]}, indent=2))
            return 1

    if not a.file or not a.cliente:
        p.print_help()
        return 2

    r = upload(a.file, a.cliente, a.name, a.folder, make_public=not a.private)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if "error" not in r else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
