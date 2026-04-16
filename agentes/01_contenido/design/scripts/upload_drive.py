"""
upload_drive.py — Helper para subir piezas al Google Drive del cliente.

IMPORTANTE: Este script NO hace la autenticación directa con Drive API.
El flujo correcto en Claude Code es usar Google Drive MCP, que Claude ya
tiene disponible como herramienta cuando está configurado.

Este archivo documenta la lógica de dónde va cada cosa, para que el agente
sepa a qué carpeta subir automáticamente según el tipo de pieza.

Estructura estándar de DV en Drive (debe existir en cada carpeta de cliente):

    CLIENTE/
    ├── 00 Ficha del Cliente/
    ├── 01 Estrategia/
    ├── 02 Producciones/
    ├── 03 Estaticos/
    │   ├── Carruseles/
    │   ├── Placas/
    │   └── Flyers/
    ├── 04 Campañas Meta/
    └── 05 Reportes/
"""

from pathlib import Path


# Mapeo: tipo de pieza → subcarpeta dentro de "03 Estaticos"
DRIVE_FOLDER_MAP = {
    "carrusel_captacion": "03 Estaticos/Carruseles",
    "carrusel_educativo": "03 Estaticos/Carruseles",
    "creativo_meta": "03 Estaticos/Creativos Meta",
    "creativo_meta_vertical": "03 Estaticos/Creativos Meta",
    "placa_propiedad": "03 Estaticos/Placas",
    "flyer_propiedad": "03 Estaticos/Flyers",
}


def get_drive_target_folder(client_name: str, piece_type: str) -> str:
    """
    Devuelve el path relativo de la carpeta destino dentro del Drive del cliente.

    Args:
        client_name: Nombre del cliente tal como figura en Drive (ej: "Digital View").
        piece_type: Tipo de pieza (key de DRIVE_FOLDER_MAP).

    Returns:
        Path relativo tipo "Digital View/03 Estaticos/Carruseles".
    """
    if piece_type not in DRIVE_FOLDER_MAP:
        raise ValueError(f"Tipo de pieza '{piece_type}' no mapeado a carpeta de Drive.")
    return f"{client_name}/{DRIVE_FOLDER_MAP[piece_type]}"


def build_upload_instruction(client_name: str, piece_type: str, local_files: list) -> str:
    """
    Genera un bloque de instrucciones que el agente puede ejecutar usando
    Google Drive MCP para subir los archivos a la carpeta correcta.

    El agente debe usar esta instrucción como guía cuando invoque las tools
    de Drive MCP.
    """
    target = get_drive_target_folder(client_name, piece_type)
    lines = [
        f"UPLOAD INSTRUCTION",
        f"Target folder: {target}",
        f"Files to upload:",
    ]
    for f in local_files:
        lines.append(f"  - {f}")
    lines.append("")
    lines.append(
        "Ejecutar con: mcp__google_drive__upload_file para cada archivo, "
        "asegurándose que la carpeta destino exista (crearla si no existe)."
    )
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Uso: python scripts/upload_drive.py <cliente> <tipo_pieza> <file1> [file2...]")
        sys.exit(1)
    client = sys.argv[1]
    piece = sys.argv[2]
    files = sys.argv[3:]
    print(build_upload_instruction(client, piece, files))
