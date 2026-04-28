---
name: feedback-loop
description: Use this skill when the Creative Director needs to generate new creative ideas based on real campaign performance data from the Media Buyer. Triggers "feedback loop de [cliente]", "procesar brief de performance de [cliente]", "que nuevas ideas sacamos de los datos de [cliente]", "el media buyer mando un brief", "hay un brief creativo de [cliente]", "que hacemos con los datos de [cliente]".
---

# Skill: Feedback Loop de Performance

Convierte los datos de performance del Media Buyer en ideas de contenido nuevas, basadas en qué ángulos y formatos están funcionando realmente — no en intuición.

Este skill cierra el loop: Media Buyer → datos → Creative Director → ideas mejores → Media Buyer.

## Antes de ejecutar

Necesitás:
1. **Cliente** (nombre exacto en `shared/brands/`).
2. El **brief creativo** más reciente del Media Buyer (se busca automáticamente).

## Pasos

### 1. Cargar el brief creativo del Media Buyer

```python
import sys
sys.path.insert(0, "scripts")
from output_manager import load_brand

# Buscar el brief_creativo más reciente en 04_pauta/outputs/<cliente>/
# El path desde creative_director: ../../../../agentes/04_pauta/outputs/<cliente>/
```

Buscá el archivo `brief_creativo_*.md` más reciente en `agentes/04_pauta/outputs/<cliente>/`. Si no existe, avisá que no hay brief del Media Buyer y que el flujo normal de ideación aplica.

### 2. Cargar el brand del cliente

```python
from output_manager import load_brand
brand = load_brand(cliente)
```

### 3. Leer el brief completo y extraer los insights clave

Del brief creativo del Media Buyer, extraé:

**Ángulos ganadores (SCALE):**
- Cuáles son, con qué métricas (CPL, CTR, hook rate)
- Por qué están funcionando (en términos de ángulo de dolor, no de formato)

**Ángulos que no funcionaron (KILL):**
- Cuáles son, por qué fallaron (¿el hook? ¿el cuerpo? ¿el CTA? ¿el formato?)
- Qué no repetir

**Insights del buyer persona real:**
- Qué le resonó a la audiencia real vs. lo que teníamos en el brand system
- Qué ángulos de dolor mostraron engagement real

**Necesidades concretas:**
- Cuántos creativos nuevos pide el Media Buyer
- Qué formatos
- Qué ángulos explorar

### 4. Generar nuevas ideas basadas en data

Seguís el proceso estándar del Creative Director (CLAUDE.md pasos 3-6), pero con las restricciones y privilegios que da la data:

**Restricciones:**
- No repitas ángulos que fueron KILL (documentá por qué)
- Si un formato específico falló consistentemente, no lo propongas sin justificación

**Privilegios:**
- Los ángulos que fueron SCALE ya están validados — podés proponer variantes del mismo ángulo con hook distinto, o el mismo hook con formato distinto
- Si el brief menciona que cierto tipo de hook (empátía, verdad incómoda) funcionó mejor, priorizalo

Producís mínimo 3 ideas nuevas, cada una con:
- Ángulo de dolor (de los 5+ estándar, o uno nuevo revelado por la data)
- Qué aprendiste de la performance que justifica este ángulo
- Formato del sistema (de los 13)
- Hook tentativo (distinto a los que ya fallaron)
- Por qué creés que va a funcionar (con datos, no intuición)

### 5. Estructura del output

```markdown
# Ideas basadas en Performance — [Cliente]
**Fecha:** [hoy]
**Brief del Media Buyer:** [nombre del archivo fuente]

---

## Qué nos dice la data

**Ángulos validados (funcionaron):**
- [Ángulo 1]: CPL USD X, [por qué resonó]
- [Ángulo 2]: ...

**Ángulos descartados (no funcionaron):**
- [Ángulo 1]: [por qué falló — hook, cuerpo, formato, o audiencia]
- [Ángulo 2]: ...

**Insights del buyer persona real:**
- [Insight 1]
- [Insight 2]

---

## Ideas nuevas

### Idea 1 — [Título interno]
- **Ángulo:** [nombre del ángulo]
- **Por qué funciona (data):** [referencia a los datos]
- **Formato:** [uno de los 13]
- **Hook tentativo:** [una línea]
- **Diferencia vs. lo que ya probamos:** [qué es distinto]

### Idea 2 — [Título interno]
[mismo formato]

### Idea 3 — [Título interno]
[mismo formato]

---

## Qué evitar en estas nuevas piezas

- [Elemento concreto que mostró los datos: ej. "hooks de pregunta no engancharon"]
- [Otro]
```

### 6. Guardar

```python
from output_manager import save_output
save_output(cliente, "feedback_loop", f"ideas_performance_{fecha}", contenido)
```

### 7. Esperar elección

Esperás que Nico o Valen elijan la idea. A partir de ahí, seguís el proceso estándar del Creative Director (paso 7: desarrollar el output completo).

## Entrega

Mostrá las ideas completas. Cerrá con:
```
Ideas basadas en los datos del Media Buyer para [cliente]. Va para Nico para elección.
Próximo paso: una vez elegida la idea, desarrollo el guion completo / brief de carrusel.
```
