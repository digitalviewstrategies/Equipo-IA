---
name: canva-reporte-semanal
description: Use this skill when the weekly-report cron has just generated reporte_semanal_*.md for a client and now needs to be delivered as a Canva-rendered PDF via WhatsApp. Reads the .md, autofills the client's Canva template via MCP, exports PDF, uploads to Drive, sends WA template. Triggers "canva reporte semanal de [cliente]", "render canva report [cliente]", or invocation from auto_deliver subprocess.
---

# Skill: Canva weekly report — render + deliver

Orquesta el flujo completo de entrega del reporte semanal:
markdown -> autofill Canva -> export PDF -> upload Drive -> WA template.

Diseñado para ser invocado desde `auto_deliver.py` cuando el cron `weekly-report` termina de generar el `.md` en `agentes/04_pauta/outputs/<cliente>/<fecha>/reporte_semanal_*.md`.

## Inputs requeridos

- `cliente` (snake_case, ej. `digital_view`).
- Path del `.md` recién generado (opcional — si no, busca el más nuevo de la semana actual).

## Pre-flight checks (BLOQUEANTES)

1. **Brand JSON tiene `reporting.canva`**: leer `shared/brands/<cliente>.json` y verificar que `reporting.canva.design_id` y `reporting.canva.elements` existan. Sin eso, no hay template — abortar y reportar.
2. **`.md` existe**: si no, abortar.
3. **Sidecar valida**: leer `<md>.status.json`. Si `status != "ready_for_handoff"`, NO entregar. Alertar al humano dueño y abortar.

## Pasos

### 1. Extraer métricas del `.md`

Parsear el `reporte_semanal_*.md` para sacar:
- Periodo (fecha desde-hasta).
- GASTO total (USD).
- LEADS totales.
- CPL promedio (USD).
- CTR (%).
- Alcance, impresiones.
- Variación leads vs semana anterior (si está, sino `+0%`).
- Top 3 ads con CPL + leads cada uno.
- Top 3 acciones tomadas.

El parser puede ser regex o un helper de Python (`agentes/04_pauta/scripts/report_generator.py` ya tiene la lógica inversa — reusar si tiene sentido).

### 2. Autofill Canva

Cargar `reporting.canva.design_id` y el mapping `elements`.

Llamar MCP Canva:

```
start-editing-transaction(design_id=<id>)
-> obtenés transaction_id + pages
```

Construir array de `operations` con un `replace_text` por cada placeholder:

```
[
  {type: "update_title", title: "Reporte <Cliente> <fecha>"},
  {type: "replace_text", element_id: <GASTO id>, text: "$<gasto>"},
  {type: "replace_text", element_id: <LEADS id>, text: "<leads>"},
  {type: "replace_text", element_id: <DELTA_LEADS id>, text: "<+X%>"},
  {type: "replace_text", element_id: <CPL id>, text: "$<cpl>"},
  {type: "replace_text", element_id: <CTR id>, text: "<x.xx>%"},
  {type: "replace_text", element_id: <ALCANCE id>, text: "<alcance>"},
  {type: "replace_text", element_id: <TOP1 id>, text: "<nombre> obtuvo un CPL de $<cpl> y generó <leads> leads esta semana."},
  {type: "replace_text", element_id: <TOP2 id>, text: "<nombre> logró un CPL de $<cpl> con un total de <leads> leads en su rendimiento."},
  {type: "replace_text", element_id: <TOP3 id>, text: "<nombre> alcanzó un CPL de $<cpl> y atrajo <leads> leads en nuestra campaña."},
  {type: "replace_text", element_id: <ACCIONES id>, text: "<lista de acciones>"},
  // Cover: actualizar periodo en el slot reutilizado
  {type: "replace_text", element_id: <cliente_subtitle id>, text: "<Cliente Display>"}
]
```

Llamar `perform-editing-operations` con todas las ops en bulk, page_index=1, pages=<lista de pages del start-transaction>.

Verificar que todas devuelvan `status: success`. Si alguna falla, `cancel-editing-transaction` y abortar con detalle.

Si todas OK, `commit-editing-transaction(transaction_id)`.

### 3. Export PDF

```
export-design(design_id=<id>, format={type: "pdf", size: "a4", export_quality: "regular"})
-> obtenés URL temporal del PDF (~21h válida)
```

### 4. Upload a Drive

Descargar el PDF a `/tmp` con `requests.get(url)`. Después llamar al helper Python:

```bash
python agentes/03_delivery_reporting/scripts/drive_upload.py \
  --file /tmp/<archivo>.pdf \
  --cliente <cliente> \
  --name "Reporte <Cliente Display> <YYYY-MM-DD>.pdf"
```

El helper devuelve `drive_file_id` y `share_url` permanente.

**Si el helper falla** (OAuth no setup todavía), fallback: usar la URL temporal Canva como WA button. Loguear el fallback claramente.

### 5. WA template

```python
from scripts.wa_reportes import send_reporte_semanal_template
send_reporte_semanal_template(
    to=<destinatario_number>,
    nombre=<destinatario_nombre>,
    url_pdf=<share_url o url_temporal>,
)
```

Destinatario: por default `ELIAS_WA_NUMBER` del `.env`. Si el brand JSON define `reporting.canva.wa_destinatario` puntual, usar ese.

### 6. Reportar y persistir

Output al stdout (capturado por auto_deliver log):

```
# Entrega reporte semanal — <Cliente> — <fecha>

## Métricas entregadas
- Gasto: $X
- Leads: X
- CPL: $X
- CTR: X%

## Artefactos
- Canva design: <view_url>
- PDF Drive: <share_url> (o "fallback temporal")
- WA enviado a: <numero>

Va para Elias. El reporte ya está en el WhatsApp del cliente.
```

Persistir en el sidecar del `.md`:

```json
{
  ...resto del status.json...,
  "delivered": {
    "at": "<iso ts>",
    "canva_design_id": "...",
    "pdf_url": "...",
    "wa_to": "...",
    "wa_message_id": "wamid.HBg..."
  }
}
```

## Errores comunes

- **MCP Canva falla**: token vencido o design borrado. Abortar y alertar a Felipe.
- **PDF download falla**: URL Canva ya expiró (raro, >21h). Re-exportar.
- **Drive upload falla**: OAuth user no configurado. Usar fallback temporal y advertir en el output.
- **WA template falla 404**: nombre de template o idioma no matchea con Meta. Verificar status del template en WhatsApp Manager.
- **WA template falla 24h-window**: no aplica para templates aprobados — si pasa, el template no está APPROVED.

## Lo que NUNCA hacés

- No modifiques el brand JSON desde acá.
- No mandes WA si validators fallaron.
- No bypass del sidecar gate.
- No commits a Canva si alguna replace_text falló.
- No mandes texto libre como fallback si el template no funciona — alertá a Felipe para que renueve el template.
