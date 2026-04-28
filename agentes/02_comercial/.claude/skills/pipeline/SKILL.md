---
name: pipeline
description: Use this skill to show the current state of all prospects in the commercial pipeline, update stages, or add notes. Triggers "pipeline", "como esta el pipeline", "estado del pipeline", "que prospectos tenemos", "donde estan los prospectos", "actualizar etapa de [nombre]", "agregar nota de [nombre]", "pasar [nombre] a discovery", "cerrar [nombre]".
---

# Skill: Pipeline Comercial

Muestra y gestiona el estado de todos los prospectos en el pipeline de DV.

## Casos de uso

### A) Ver el pipeline completo

```python
import sys
sys.path.insert(0, "scripts")
from pipeline import format_pipeline_report

reporte = format_pipeline_report()
print(reporte)
```

Mostrá el reporte completo. No hace falta más procesamiento.

---

### B) Buscar un prospecto específico

```python
from pipeline import get_prospecto
prospecto = get_prospecto(nombre)
```

Si lo encontrás, mostrá su estado completo:

```markdown
## [Nombre] — [Empresa]
- **Etapa:** [etapa]
- **Puntaje:** [X]/41 ([clasificación])
- **Zona:** [zona]
- **Tipo:** [perfil]
- **Ingresó:** [fecha]
- **Última actualización:** [fecha]
- **Red flags:** [lista o "Ninguno"]
- **Notas:** [notas o "Sin notas"]
```

---

### C) Avanzar la etapa de un prospecto

Si el usuario dice "pasá a [nombre] a [etapa]" o similar:

```python
from pipeline import update_etapa
prospecto = update_etapa(nombre_o_id, nueva_etapa)
```

Etapas válidas: `pre_filtro` → `fit_call` → `discovery` → `scoring` → `propuesta` → `negociacion` → `cerrado_ganado` | `cerrado_perdido`

Confirmá el cambio: "[Nombre] movido a [etapa nueva]."

---

### D) Agregar un prospecto nuevo

Si el usuario dice "agregá a [nombre]" o da datos de un prospecto nuevo:

```python
from pipeline import add_prospecto
prospecto = add_prospecto(nombre=..., empresa=..., zona=..., tipo=..., fuente=...)
```

Confirmá: "[Nombre] agregado al pipeline en etapa pre_filtro."

---

### E) Agregar una nota

Si el usuario dice "agregá nota de [nombre]: [texto]":

```python
from pipeline import add_nota
prospecto = add_nota(nombre_o_id, nota)
```

Confirmá: "Nota agregada a [Nombre]."

---

### F) Marcar como cerrado

Si el usuario dice "cerrar [nombre] como [ganado/perdido]":

```python
from pipeline import update_etapa
etapa = "cerrado_ganado" if ganado else "cerrado_perdido"
update_etapa(nombre_o_id, etapa)
```

Si es cerrado ganado: "¿Querés que avise al agente Coordinador para arrancar el kickoff de [nombre]?"
Si es cerrado perdido: "¿Querés registrar el motivo de pérdida como nota?"

---

## Entrega

Para el reporte completo: mostrá todo sin filtrar.
Para operaciones puntuales: confirmá la acción realizada en una línea.

Si el pipeline está vacío: "No hay prospectos registrados todavía. Usá `/calificar <nombre>` para agregar el primero."
