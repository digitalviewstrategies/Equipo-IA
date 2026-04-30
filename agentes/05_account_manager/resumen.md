# Resumen — Creacion agente 05_account_manager (WhatsApp 1-1)

## Tema
Crear agente que gestione clientes DV via WhatsApp.

## Decisiones tomadas
- Migrar de grupos a 1-1 con numero nuevo dedicado "DV Asistente".
- Conexion via WhatsApp Cloud API oficial de Meta (no Baileys).
- Modo mixto: auto-respuesta en FAQs claras, borrador para aprobacion en el resto.
- Scope etapa 1: status produccion, performance campanas, FAQs, coordinacion filmacion.
- Vive en `agentes/05_account_manager/` (carpeta scaffold ya existente, vacia al iniciar).

## Archivos creados
- Plan: `~/.claude/plans/quiero-crear-un-agente-playful-goose.md`
- `CLAUDE.md`, `README.md`, `.env.example`, `requirements.txt`, `resumen.md`
- `context/`: `faqs.md`, `tono_whatsapp.md`, `intents.md`
- `scripts/`: `webhook.py`, `wa_client.py`, `client_resolver.py`, `intent_router.py`, `policy.py`, `approval_channel.py`, `conversation_log.py`, `config.py`, `__init__.py`
- `scripts/handlers/`: `faq.py`, `status_produccion.py`, `performance.py`, `filmacion.py`, `__init__.py`
- `templates/borrador_aprobacion.md`

## Archivos editados
- `agentes/README.md` — fase 05 marcada como "En desarrollo".

## Pendientes
- Setup humano en Meta: comprar numero, alta WhatsApp Business Account, System User token, webhook URL, aprobar templates iniciales.
- Etapa 1.5:
  - Integrar Trello API en `handlers/status_produccion.py`.
  - Definir metodo `summary()` en `agentes/04_pauta/scripts/meta_api.py` para `handlers/performance.py`.
  - Integrar Sheets API (agenda) en `handlers/filmacion.py`.
  - Logica real de `_execute_approval` en `scripts/webhook.py` (parsear ID del pending, recuperar destino, enviar).
- Agregar bloque `whatsapp.contacts[]` a cada `shared/brands/<cliente>.json`.

## Como probar
```bash
cd agentes/05_account_manager
pip install -r requirements.txt
cp .env.example .env  # completar
uvicorn scripts.webhook:app --reload --port 8000
ngrok http 8000
# configurar webhook URL en Meta App Dashboard
```
