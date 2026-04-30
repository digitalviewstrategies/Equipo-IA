"""Handler status_produccion: lee Trello del cliente y devuelve estado.

Etapa 1: stub que devuelve borrador. Trello API se integra en etapa 1.5 una vez
que tengamos `trello_board_id` en cada brand y el TRELLO_TOKEN en .env.
"""


def handle(text: str, entities: dict, brand: dict | None, contact_name: str | None) -> dict:
    if not brand or not brand.get("whatsapp", {}).get("trello_board_id"):
        return {
            "text": "Lo chequeo con el equipo de edicion y te confirmo el estado.",
            "ok": False,
        }
    # TODO etapa 1.5: GET /boards/{id}/cards via Trello API, filtrar por entities['referencia']
    referencia = entities.get("referencia", "lo que pediste")
    pieza = entities.get("pieza", "la pieza")
    return {
        "text": f"Lo chequeo con edicion y te confirmo el estado de {pieza} de {referencia}.",
        "ok": False,  # ok=False fuerza borrador hasta tener integracion Trello real
    }
