---
name: reporte-semanal
description: Use this skill when Elias asks to generate a weekly performance report for a client, including a WhatsApp summary. Triggers "reporte semanal de [cliente]", "reporte de esta semana para [cliente]", "genera el reporte de [cliente]", "armame el reporte semanal", "reportar a [cliente]", "que tal fue la semana de [cliente]".
---

# Skill: Reporte Semanal de Cliente

Genera el reporte semanal de performance para un cliente en dos versiones: documento completo para archivo + resumen de WhatsApp para mandar directamente.

## Antes de ejecutar

Necesitás:
1. **Cliente** (nombre exacto en `shared/brands/`).
2. **Período** (fechas de inicio y fin de la semana). Si no las recibiste, usá los últimos 7 días.

## Pasos

### 1. Buscar el reporte interno del Media Buyer

```python
from scripts.output_manager import get_latest_pauta_output
reporte_interno = get_latest_pauta_output(cliente, "reporte_semanal")
analisis = get_latest_pauta_output(cliente, "analisis")
```

Si existe un `reporte_semanal_*.md` reciente, ese es el insumo principal. Leelo completo.

Si no existe:
- Buscá un `analisis_*.md` reciente.
- Si tampoco hay nada, le avisás a Elias que el Media Buyer tiene que generar el análisis primero (Felipe tiene que correr el Workflow C del agente de pauta).

### 2. Cargar el brand del cliente

```python
from scripts.output_manager import load_brand
brand = load_brand(cliente)
```

Usá el `name` del brand para el encabezado del reporte. Guardate también:
- `brand["content_pillars"]` (si existe) → para la sección de recomendaciones de contenido.
- `brand["target_audience"]` y `brand["meta_ads"]["cpl_target_usd"]` → para contextualizar resultados.

Si algún campo no existe, omití la sección dependiente con un aviso explícito (no rompas, no inventes).

### 3. Evaluar gaps de fase activa

```python
from scripts.output_manager import get_phase_gaps
gaps_info = get_phase_gaps(cliente)  # infiere fase activa automáticamente
```

`gaps_info` trae:
- `fase` y `fase_nombre` (ej. 6, "Seguimiento")
- `gaps`: entregables faltantes o no verificables
- `gaps_criticos`: solo los críticos que pueden frenar la próxima semana

Usá `gaps_criticos` para la sección "Atención para la próxima semana" del reporte y para la línea extra del WhatsApp.

### 4. Extraer métricas clave del reporte interno

Del reporte interno, extraé:
- Gasto total (USD)
- Leads / consultas generadas
- CPL (costo por consulta)
- Impresiones y alcance (si están)
- Clasificación general: cuántos creativos en SCALE, KILL, ITERATE, HOLD
- Top creativo de la semana (nombre + CPL)
- Creativo que se pausó (si hay KILL)

### 5. Generar el reporte de cliente (versión completa)

Estructura (siguiendo `context/tono_cliente.md`):

```markdown
# Reporte Semanal — [Nombre del cliente]
**Semana:** [fecha inicio] al [fecha fin]

---

## Resultados de la semana

| | Valor |
|---|---|
| Consultas generadas | [N] |
| Inversión en pauta | USD [X] |
| Costo por consulta | USD [X] |
| Personas alcanzadas | [N] |

---

## Qué funcionó

- [Bullet concreto. Ej: "El anuncio sobre [tema] generó [N] consultas a USD [X] cada una."]
- [Si aplica, segundo bullet]

## Qué ajustamos

- [Bullet concreto. Ej: "Pausamos el anuncio de [tema] porque el costo era de USD [X], por encima del objetivo."]
- [Si aplica, segundo bullet]

## Recomendaciones de contenido

[Si hay `content_pillars` en el brand: cruzar el top creativo de la semana con el pilar al que pertenece y sugerir reforzar ese pilar. Ej: "El anuncio sobre [tema] (pilar: [X]) fue el de mejor performance — sugerimos producir 2 piezas más sobre ese mismo ángulo la próxima semana." Si KILL: sugerir alternativa basada en otro pilar.]
[Si no hay content_pillars: omitir la sección con el aviso `[contenido: sin pilares definidos en brand]`.]

> Para Nico: validar dirección creativa antes del próximo bloque de producción.

## Atención para la próxima semana

[Solo si `gaps_info["gaps_criticos"]` no está vacío. Para cada gap crítico: bullet con el entregable + responsable + acción concreta. Ej: "Falta confirmar Page ID de Facebook → Elias coordina con el cliente esta semana."]
[Si no hay gaps críticos: omitir esta sección o poner "Sin bloqueantes operativos. La operación corre normal."]

## Esta próxima semana

[1-2 líneas de qué se va a hacer diferente o qué se va a mantener. Concreto, no genérico.]
```

**Reglas:**
- Sin términos de pauta (no CTR, no hook rate, no ad set, no CPM).
- "Consultas" en lugar de "leads".
- "Anuncios" en lugar de "ads" o "creativos".
- Si el CPL estuvo sobre el target, decilo directamente y explicá qué se hace.
- Si no hubo leads, decilo. No lo endulces.

### 6. Generar el mensaje de WhatsApp

5-8 líneas de texto plano, sin markdown:

```
Hola [nombre del contacto del cliente], acá el resumen de esta semana:

[N] consultas generadas
Inversión: USD [X]
Costo por consulta: USD [X]

[Una línea de contexto honesta: si fue buena semana o no, y por qué en términos simples.]

La próxima semana [acción concreta que se va a tomar].
```

Si hay al menos un gap crítico en `gaps_info["gaps_criticos"]`, sumá una línea adicional al final, antes del cierre, con tono directo. Ej:
```
Te aviso: necesitamos [entregable concreto] esta semana para no frenar.
```
No listes más de un gap en el WhatsApp — el más crítico. El resto va en el documento completo.

Si no sabés el nombre del contacto del cliente, usá "Hola!" o dejá el espacio marcado con `[nombre]`.

### 7. Guardar

```python
from scripts.output_manager import save_output
# Guardar reporte completo
save_output(cliente, "reporte_semanal_cliente", f"{periodo}", reporte_completo)
# Guardar mensaje de WhatsApp
save_output(cliente, "whatsapp_semanal", f"{periodo}", mensaje_wa)
```

### 8. Enviar a Elias por WhatsApp (opcional)

Si el usuario pide explícitamente "mandalo a Elias", "envialo por WhatsApp" o equivalente, mandá el bloque de WhatsApp generado en el paso 6 al número de Elias usando el cliente de la app Reportes:

```python
from scripts.wa_reportes import send_to_elias
resp = send_to_elias(mensaje_wa)
```

Reglas:
- No envíes sin pedido explícito. Por default, dejás solo el borrador.
- Si Meta devuelve error 100 ("Invalid parameter"), informá al usuario que la ventana de 24hs de WhatsApp Business está cerrada y que Elias tiene que mandar primero un mensaje al número de la app Reportes.
- Si `REPORTES_WABA_TOKEN` no está cargado, avisá que falta configurar `.env`.

## Entrega

Mostrá ambas versiones en pantalla, claramente separadas. Cerrá con:
```
Va para Elias para revisión y envío al cliente.
```

Indicá si hay alguna alerta que Elias debería mencionar en la llamada/mensaje (ej: "Esta semana el costo fue alto — recomiendo que Elias le explique que se están probando nuevos anuncios").
