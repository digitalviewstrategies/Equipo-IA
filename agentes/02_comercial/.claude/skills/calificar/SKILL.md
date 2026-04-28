---
name: calificar
description: Use this skill when Valentin or Elias wants to score a prospect against DV's 41-point scorecard to decide whether to advance them. Triggers "calificar a [nombre]", "scorecard de [nombre]", "que puntaje tiene [nombre]", "es buen prospecto [nombre]", "armame la calificacion de [nombre]", "tenemos fit con [nombre]", "debemos avanzar con [nombre]".
---

# Skill: Calificar Prospecto

Aplica el scorecard de 41 puntos de DV a un prospecto y devuelve una decisión clara: Ideal, Normal o No Go.

## Antes de ejecutar

Necesitás datos del prospecto. Recibís lo que haya disponible:
- Nombre / empresa
- Zona de operación
- Tipo de perfil (agencia, top producer, desarrollador)
- Ticket promedio de propiedades
- Presupuesto disponible para pauta (USD/mes)
- Fuente de ingreso principal (inmobiliario como actividad core?)
- Tiempo en el mercado
- Operaciones mensuales actuales
- Marketing actual (qué hace hoy, cuánto invierte)
- Urgencia (por qué busca esto ahora)
- Disposición a filmar o producir contenido
- Equipo disponible para seguimiento de leads

Si faltan datos clave, marcalos como "no informado" en el scorecard — no los asumís.

## Pasos

### 1. Verificar knock-outs primero

Antes de calcular el puntaje, revisá si hay algún knock-out que descalifica directamente:

- ¿Zona fuera de CABA/GBA? → No Go inmediato.
- ¿Presupuesto de pauta < USD 800/mes? → No Go inmediato.
- ¿Fee de DV imposible de pagar? → No Go inmediato.
- ¿Más de 3 red flags de `context/icp_y_scoring.md`? → No Go inmediato.

Si hay knock-out, informalo directamente y no hagas el scorecard.

### 2. Calcular el puntaje por categoría

Para cada categoría del scorecard (de `context/icp_y_scoring.md`), asigná el puntaje que corresponde según los datos disponibles. Si un dato no está disponible, marcalo como "sin dato" y asignás el puntaje mínimo de esa categoría.

| Categoría | Pts máx | Puntaje asignado |
|---|---|---|
| Zona geográfica | 3 | [X] |
| Historial de facturación | 2 | [X] |
| Volumen operativo actual | 3 | [X] |
| Fuente de ingreso principal | 3 | [X] |
| Organización comercial/marketing | 2 | [X] |
| Inversión actual en marketing | 3 | [X] |
| Urgencia | 3 | [X] |
| Ticket promedio de propiedades | 3 | [X] |
| Presupuesto de pauta disponible | 4 | [X] |
| Tamaño del equipo | 2 | [X] |
| Disposición a filmar/producir | 3 | [X] |
| Capacidad de seguimiento de leads | 3 | [X] |
| Mentalidad y expectativas | 5 | [X] |
| Fee de DV | 2 | [X] |
| **TOTAL** | **41** | **[X]** |

### 3. Evaluar red flags

Lista los red flags presentes (si alguno aplica) referenciando `context/icp_y_scoring.md`.

### 4. Generar el output de calificación

```markdown
# Calificación — [Nombre] ([Empresa])
**Fecha:** [hoy]
**Evaluado por:** Agente Comercial DV

---

## Resultado

**Puntaje:** [X]/41
**Clasificación:** [IDEAL / NORMAL / NO GO]
**Recomendación:** [Avanzar rápido / Avanzar con análisis de riesgos / No avanzar]

---

## Scorecard detallado

[Tabla con puntaje por categoría + justificación breve de cada uno]

---

## Red flags detectados

[Lista de red flags si los hay, o "Sin red flags detectados."]

---

## Datos faltantes para completar el scorecard

[Lista de qué información faltó, si algo. Estos son puntos a aclarar en la Fit Call.]

---

## Próximo paso recomendado

[Si IDEAL o NORMAL: "Fit Call con Valentin para confirmar datos faltantes y avanzar a discovery."]
[Si NO GO: razón concreta por la cual no avanzar.]
```

### 5. Registrar en el pipeline

```python
import sys
sys.path.insert(0, "scripts")
from pipeline import add_prospecto, update_scoring, get_prospecto

# Si el prospecto ya existe, actualizar scoring
# Si no existe, agregar al pipeline
prospecto = get_prospecto(nombre)
if not prospecto:
    prospecto = add_prospecto(nombre=nombre, empresa=empresa, zona=zona, ...)

update_scoring(
    nombre_o_id=prospecto["id"],
    puntaje=puntaje_total,
    clasificacion=clasificacion,
    red_flags=red_flags_detectados,
)
```

### 6. Guardar el output

```python
from output_manager import save_output
save_output(nombre, "calificacion", "scorecard", contenido)
```

## Entrega

Mostrá el resultado completo. Cerrá con:

```
Va para Valentin para decisión final.
[Si IDEAL/NORMAL]: Próximo paso sugerido: Fit Call para confirmar [datos faltantes].
[Si NO GO]: Razón: [motivo concreto]. No avanzar.
```

Sé directo con el No Go. Si no es cliente, decilo sin vueltas.
