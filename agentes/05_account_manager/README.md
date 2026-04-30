# 05 Account Manager — WhatsApp 1-1

Agente que atiende a clientes DV via WhatsApp en chats 1-1 desde el numero "DV Asistente". Modo mixto: auto-respuesta en FAQs, borrador para aprobacion en el resto.

## Quick start (dev)

```bash
cd agentes/05_account_manager
pip install -r requirements.txt
cp .env.example .env  # completar con tokens reales
uvicorn scripts.webhook:app --reload --port 8000
ngrok http 8000
# configurar webhook URL en Meta App Dashboard
```

## Estructura

```
05_account_manager/
├── CLAUDE.md            # instrucciones del agente
├── context/             # FAQs, tono WA, definicion de intents
├── scripts/             # webhook, wa_client, router, handlers
├── outputs/             # logs de conversaciones por cliente
└── templates/           # formato del borrador a Felipe
```

## Setup en Meta (humano, no automatizable)

1. Comprar numero nuevo dedicado.
2. Alta WhatsApp Business Account en Business Portfolio DV.
3. Registrar numero → obtener `PHONE_NUMBER_ID`, `WABA_ID`.
4. System User token con `whatsapp_business_messaging`, `whatsapp_business_management`.
5. Configurar webhook URL + verify token.
6. Aprobar templates iniciales (solo si necesitamos iniciar conversacion).

## Scope etapa 1

Incluye: recepcion 1-1, clasificacion, handlers FAQ/status/performance/filmacion, borrador a Felipe, logs.
No incluye: mensajes proactivos, multimedia entrante, leads desconocidos, migracion automatica de grupos.

Ver plan completo: `~/.claude/plans/quiero-crear-un-agente-playful-goose.md`.
