"""Handler status_produccion: lee ClickUp del cliente y devuelve estado.

Etapa 1: stub que devuelve borrador. Integracion ClickUp se hace en etapa 1.5 una vez
que tengamos `clickup_list_id` en cada brand y `CLICKUP_TOKEN` en .env.

Nota: en evaluacion ClickUp vs alternativas; el campo del brand puede cambiar de nombre.
"""


def handle(text: str, entities: dict, brand: dict | None, contact_name: str | None) -> dict:
    if not brand or not brand.get("whatsapp", {}).get("clickup_list_id"):
        return {
            "text": "Lo chequeo con el equipo de edicion y te confirmo el estado.",
            "ok": False,
        }
    # TODO etapa 1.5: GET /list/{id}/task via ClickUp API v2, filtrar por entities['referencia']
    #   headers: {"Authorization": CLICKUP_TOKEN}
    #   endpoint: https://api.clickup.com/api/v2/list/{list_id}/task
    referencia = entities.get("referencia", "lo que pediste")
    pieza = entities.get("pieza", "la pieza")
    return {
        "text": f"Lo chequeo con edicion y te confirmo el estado de {pieza} de {referencia}.",
        "ok": False,  # ok=False fuerza borrador hasta tener integracion ClickUp real
    }
