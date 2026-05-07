"""
csv_importer.py — Carga una lista fria de prospectos al pipeline comercial.

CSV esperado (header obligatorio, columnas opcionales):
    nombre,empresa,telefono,email,zona,tipo,fuente,notas

Uso:
    python csv_importer.py path/a/lista.csv
    python csv_importer.py path/a/lista.csv --fuente "lista_top_producers_2026"

Idempotente por (nombre + empresa + telefono): si ya existe un prospecto con
ese match exacto, no se duplica.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pipeline as pipe  # noqa: E402


def _ya_existe(data: dict, nombre: str, empresa: str, telefono: str) -> bool:
    for p in data.get("prospectos", []):
        if (
            p.get("nombre", "").strip().lower() == nombre.strip().lower()
            and p.get("empresa", "").strip().lower() == empresa.strip().lower()
            and p.get("telefono", "").strip() == telefono.strip()
        ):
            return True
    return False


def import_csv(path: Path, fuente_default: str = "lista_fria") -> dict:
    if not path.exists():
        return {"error": f"no existe: {path}"}

    nuevos, duplicados, errores = 0, 0, 0
    data = pipe._load()

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                nombre = (row.get("nombre") or "").strip()
                if not nombre:
                    errores += 1
                    continue
                empresa = (row.get("empresa") or "").strip()
                telefono = (row.get("telefono") or "").strip()
                if _ya_existe(data, nombre, empresa, telefono):
                    duplicados += 1
                    continue
                pipe.add_prospecto(
                    nombre=nombre,
                    empresa=empresa,
                    tipo=(row.get("tipo") or "otro").strip() or "otro",
                    zona=(row.get("zona") or "desconocida").strip() or "desconocida",
                    telefono=telefono,
                    email=(row.get("email") or "").strip(),
                    fuente=(row.get("fuente") or fuente_default).strip(),
                    notas=(row.get("notas") or "").strip(),
                )
                nuevos += 1
                data = pipe._load()
            except Exception as e:
                print(f"  [error] fila {nombre}: {e}")
                errores += 1

    return {"nuevos": nuevos, "duplicados": duplicados, "errores": errores}


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    path = Path(argv[0])
    fuente = "lista_fria"
    if "--fuente" in argv:
        fuente = argv[argv.index("--fuente") + 1]
    r = import_csv(path, fuente_default=fuente)
    print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
