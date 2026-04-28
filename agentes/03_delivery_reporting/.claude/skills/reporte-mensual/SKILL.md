---
name: reporte-mensual
description: Use this skill to generate a monthly performance report for a client, including executive summary and next month plan. Triggers "reporte mensual de [cliente]", "cierre de mes de [cliente]", "reporte de [mes] para [cliente]", "genera el reporte mensual", "cierre mensual de [cliente]".
---

# Skill: Reporte Mensual de Cliente

Genera el reporte mensual de performance para un cliente: resumen del mes, tendencia semanal, análisis de creativos, y plan del mes siguiente.

## Antes de ejecutar

Necesitás:
1. **Cliente** (nombre exacto en `shared/brands/`).
2. **Mes** (ej. "Abril 2026"). Si no lo recibiste, usá el mes anterior al actual.

## Pasos

### 1. Recopilar todos los reportes del mes

```python
from scripts.output_manager import list_pauta_outputs, load_brand
outputs = list_pauta_outputs(cliente, limit=20)
```

Buscá:
- `reporte_semanal_*.md` del mes en cuestión (debería haber 4).
- `reporte_mensual_*.md` del Media Buyer si ya existe.
- `analisis_*.md` del mes.

Si hay un `reporte_mensual_*.md` del Media Buyer, ese es el insumo principal. Si no hay, consolidá los reportes semanales.

### 2. Consolidar métricas del mes

Del contenido de los reportes, extraé:
- Gasto total del mes (USD)
- Total de consultas generadas
- CPL promedio del mes
- CPL por semana (para mostrar tendencia)
- Presupuesto planificado vs ejecutado (si está en el reporte interno)
- Los 3 mejores creativos del mes (CPL + por qué funcionaron)
- Los creativos que se pausaron y por qué

### 3. Generar el reporte mensual de cliente

```markdown
# Reporte Mensual — [Nombre del cliente]
**Mes:** [Mes y año]

---

## Resumen del mes

| | Valor |
|---|---|
| Consultas generadas | [N] |
| Inversión total | USD [X] |
| Costo por consulta | USD [X] |
| Personas alcanzadas | [N] (estimado) |

---

## Tendencia semanal

| Semana | Consultas | Costo por consulta |
|---|---|---|
| Semana 1 ([fechas]) | [N] | USD [X] |
| Semana 2 ([fechas]) | [N] | USD [X] |
| Semana 3 ([fechas]) | [N] | USD [X] |
| Semana 4 ([fechas]) | [N] | USD [X] |

---

## Anuncios del mes

**Los que mejor funcionaron:**
1. [Nombre o descripción del anuncio] — [N] consultas a USD [X] cada una
2. [Si aplica]

**Los que pausamos:**
- [Descripción] — el costo estaba muy por encima del objetivo, pausamos para probar variantes nuevas.

---

## Qué aprendimos este mes

[2-3 bullets de insights concretos. Ej: "Los anuncios que hablan de [tema] generaron más consultas que los de [otro tema]." Esto informa la estrategia del mes siguiente.]

---

## Plan para [mes siguiente]

- [Acción concreta 1. Ej: "Lanzamos 2 nuevos anuncios con el ángulo de [X]."]
- [Acción concreta 2. Ej: "Aumentamos el presupuesto de [anuncio que funcionó]."]
- [Acción concreta 3 si aplica.]

---

## Próximos pasos

- [ ] [Lo que necesita el cliente hacer o aprobar, si algo]
- [ ] Reporte de la semana 1 de [mes siguiente] el [fecha aproximada]
```

**Reglas de tono:**
- Sin términos técnicos de pauta.
- Ser honesto con la tendencia: si hubo semanas malas, explicarlo en términos simples.
- Los "aprendizajes" deben ser concretos, no genéricos. "Aprendimos que funciona el contenido de valor" no sirve.

### 4. Guardar

```python
from scripts.output_manager import save_output
save_output(cliente, "reporte_mensual_cliente", f"{mes}", reporte)
```

## Entrega

Mostrá el reporte completo. Cerrá con:
```
Va para Elias para revisión y envío al cliente. Si hay algo que requiera decisión de pauta (ej. cambio de presupuesto para el mes siguiente), marcalo para que Elias lo coordine con Felipe.
```
