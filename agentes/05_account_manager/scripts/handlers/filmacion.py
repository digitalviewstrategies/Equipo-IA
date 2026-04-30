"""Handler coordinacion_filmacion: lee Sheet de agenda compartido.

Etapa 1: stub. Integracion Sheets API en etapa 1.5 una vez definido el ID
del Sheet maestro de agenda en `agenda_sheet_id` (config global) y service account.
"""


def handle(text: str, entities: dict, brand: dict | None, contact_name: str | None) -> dict:
    fecha = entities.get("fecha", "la proxima")
    return {
        "text": f"Lo chequeo con Bauti CB y te confirmo {fecha}.",
        "ok": False,
    }
