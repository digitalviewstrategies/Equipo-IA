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

Usá el `name` del brand para el encabezado del reporte.

### 3. Extraer métricas clave del reporte interno

Del reporte interno, extraé:
- Gasto total (USD)
- Leads / consultas generadas
- CPL (costo por consulta)
- Impresiones y alcance (si están)
- Clasificación general: cuántos creativos en SCALE, KILL, ITERATE, HOLD
- Top creativo de la semana (nombre + CPL)
- Creativo que se pausó (si hay KILL)

### 4. Generar el reporte de cliente (versión completa)

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

## Esta próxima semana

[1-2 líneas de qué se va a hacer diferente o qué se va a mantener. Concreto, no genérico.]
```

**Reglas:**
- Sin términos de pauta (no CTR, no hook rate, no ad set, no CPM).
- "Consultas" en lugar de "leads".
- "Anuncios" en lugar de "ads" o "creativos".
- Si el CPL estuvo sobre el target, decilo directamente y explicá qué se hace.
- Si no hubo leads, decilo. No lo endulces.

### 5. Generar el mensaje de WhatsApp

5-8 líneas de texto plano, sin markdown:

```
Hola [nombre del contacto del cliente], acá el resumen de esta semana:

[N] consultas generadas
Inversión: USD [X]
Costo por consulta: USD [X]

[Una línea de contexto honesta: si fue buena semana o no, y por qué en términos simples.]

La próxima semana [acción concreta que se va a tomar].
```

Si no sabés el nombre del contacto del cliente, usá "Hola!" o dejá el espacio marcado con `[nombre]`.

### 6. Guardar

```python
from scripts.output_manager import save_output
# Guardar reporte completo
save_output(cliente, "reporte_semanal_cliente", f"{periodo}", reporte_completo)
# Guardar mensaje de WhatsApp
save_output(cliente, "whatsapp_semanal", f"{periodo}", mensaje_wa)
```

## Entrega

Mostrá ambas versiones en pantalla, claramente separadas. Cerrá con:
```
Va para Elias para revisión y envío al cliente.
```

Indicá si hay alguna alerta que Elias debería mencionar en la llamada/mensaje (ej: "Esta semana el costo fue alto — recomiendo que Elias le explique que se están probando nuevos anuncios").
