---
name: preparar-reunion
description: Use this skill when Valentin needs a pre-meeting brief for a Fit Call, Discovery Call, or Offer Call with a prospect. Triggers "preparar reunion con [nombre]", "brief para la call de [nombre]", "que pregunto en la reunion con [nombre]", "preparame para ver a [nombre]", "tengo una discovery con [nombre]", "voy a presentarle a [nombre]", "brief de [nombre]".
---

# Skill: Preparar Reunión

Genera el brief de reunión para que Valentin entre preparado a cualquier etapa del proceso comercial: Fit Call, Discovery Call, u Offer Call.

## Antes de ejecutar

Necesitás:
1. **Nombre del prospecto**.
2. **Tipo de reunión**: `fit_call` | `discovery` | `propuesta`.

Si no te dicen el tipo, preguntá en qué etapa está el prospecto.

## Pasos

### 1. Cargar el estado del prospecto

```python
import sys
sys.path.insert(0, "scripts")
from pipeline import get_prospecto
from output_manager import list_outputs

prospecto = get_prospecto(nombre)
outputs_anteriores = list_outputs(nombre) if prospecto else []
```

Si el prospecto no existe en el pipeline, pedí los datos básicos antes de continuar (o generá el brief solo con lo que tenés).

### 2. Generar el brief según el tipo de reunión

---

#### Para Fit Call (15 minutos)

```markdown
# Brief Fit Call — [Nombre] ([Empresa])
**Fecha de la call:** [si se sabe]
**Objetivo:** Confirmar fit básico. Go / No Go para discovery.

---

## Contexto del prospecto

[Resumen breve de lo que se sabe: zona, perfil, cómo llegó, qué se sabe de su negocio]

## Preguntas clave para confirmar

1. ¿En qué zona operás? (verificar CABA o GBA Norte)
2. ¿Cuál es el ticket promedio de tus propiedades? (verificar > USD 80k)
3. ¿Podés invertir USD 800/mes en pauta como mínimo? (knock-out)
4. ¿Por qué estás buscando apoyo en marketing justo ahora?
5. ¿Sos vos quien toma la decisión de contratar o hay alguien más involucrado?

## Señales de Go

- Zona ok + ticket ok + presupuesto ok + urgencia real + es el decisor

## Señales de No Go

[Lista de red flags que aplican a este prospecto según lo que se sabe]

## Próximo paso si es Go

Discovery Call: 45-60 min. Coordinar en los próximos 3 días hábiles.
```

---

#### Para Discovery Call (45-60 minutos)

```markdown
# Brief Discovery Call — [Nombre] ([Empresa])
**Fecha de la call:** [si se sabe]
**Objetivo:** Diagnóstico profundo. Completar el scorecard de 41 puntos.

---

## Contexto del prospecto

[Todo lo que se sabe hasta ahora: zona, perfil, resultado de la fit call, notas anteriores]

## Scorecard actual (si ya se aplicó)

[Puntaje parcial y categorías que faltan confirmar]

## Preguntas para completar el scorecard

**Sobre el negocio:**
[Lista de preguntas de discovery de `context/icp_y_scoring.md` que todavía no se tienen respuesta]

**Sobre el marketing actual:**
[Preguntas específicas según el perfil del prospecto]

**Sobre las expectativas:**
[Preguntas clave]

**Preguntas de mentalidad (importante para el scorecard):**
- ¿Entendés que el sistema tarda 45-60 días en madurar antes de dar resultados?
- ¿Podés dedicar tiempo a revisar y aprobar materiales?
- ¿Tenés equipo para responder leads en menos de 2 horas?

## Datos faltantes del scorecard

[Lista de categorías del scorecard sin información — son las que hay que resolver en esta call]

## Señales de alerta durante la call

[Red flags conocidos o sospechados, qué preguntar para confirmarlos o descartarlos]

## Próximo paso si el scorecard supera 25 puntos

Offer Call con la propuesta. Preparar en base a lo que se descubra hoy.
```

---

#### Para Offer Call / Presentación Comercial

```markdown
# Brief Offer Call — [Nombre] ([Empresa])
**Fecha:** [si se sabe]
**Objetivo:** Presentar la propuesta y cerrar.

---

## Resumen del prospecto

[Nombre, empresa, zona, perfil, puntaje del scorecard, clasificación]

## Los problemas que DV le resuelve (sus palabras)

[Basado en las notas de la discovery call: ¿qué dolores expresó? ¿qué lo frustra? Usamos sus propias palabras en la presentación]

## Diagnóstico personalizado para este prospecto

[Qué necesita específicamente este cliente, basado en lo que se descubrió. No genérico.]

## Propuesta recomendada

- **Track de producción:** [A (cliente filma) / B (DV produce)]
- **Precio sugerido:** USD [X] (rango USD 3.000 - USD 4.500)
- **Opción de pago recomendada:** [cuotas / anticipo según perfil]
- **Qué incluir de especial si aplica:** [ej. más piezas si paga anticipado]

## La garantía aplicada a este caso

[Cómo explicar la garantía de 45 días en términos del negocio de este cliente]

## Posibles objeciones y cómo responderlas

| Objeción | Respuesta |
|---|---|
| "Es caro para mí" | [respuesta basada en el negocio del prospecto] |
| "Necesito pensarlo" | [respuesta] |
| "No tengo tiempo para contenido" | [respuesta] |
| "Ya probé con una agencia y no funcionó" | [respuesta] |

## Señales de cierre (qué buscar)

[Indicadores de que el prospecto está listo para cerrar]

## Próximo paso si cierra

Contrato + primer pago. Kickoff de onboarding con Elias dentro de los 5 días hábiles.
```

### 3. Guardar el brief

```python
from output_manager import save_output
tipo_output = "brief_reunion"
save_output(nombre, tipo_output, f"{tipo_reunion}_{fecha}", contenido_brief)
```

## Entrega

Mostrá el brief completo, listo para que Valentin lo lea antes de la reunión. Cerrá con:

```
Brief listo. Va para Valentin.
```

Si hay información que falta y que podría cambiar la preparación, marcalo explícitamente al final del brief.
