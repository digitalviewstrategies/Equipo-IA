---
name: status
description: Use this skill when the user asks for the current status of a client — what outputs exist, what phase they are in, what is missing or pending. Triggers "status [cliente]", "como estamos con [cliente]", "que hay de [cliente]", "en que fase esta [cliente]", "que falta para [cliente]", "mostrame el estado de [cliente]".
---

# Skill: Status de cliente

Muestra el estado operativo completo de un cliente: qué hay, qué falta, qué alertas hay.

## Antes de ejecutar

Necesitas un dato: el **nombre del cliente** tal como aparece en `shared/brands/` (ej. `toribio_achaval`, `zipcode`, `ini_propiedades`). Si no lo recibiste, preguntalo.

Si no sabés el nombre exacto, ejecuta:
```python
from scripts.output_manager import list_brands
print(list_brands())
```

## Pasos

1. Verificá que el brand existe:
```python
from scripts.output_manager import brand_exists, load_brand
if not brand_exists(cliente):
    # Informa que el cliente no está onboardeado y detente
```

2. Generá el reporte de estado:
```python
from scripts.output_manager import format_status_report
reporte = format_status_report(cliente)
print(reporte)
```

3. Completá el reporte con el análisis de fase:

   - Si solo hay brand JSON y nada más → **Fase 1: Brand configurado, sin contenido**. Próximo paso: Creative Director.
   - Si hay outputs de creative_director pero no de copywriter → **Fase 2: Contenido ideado, sin copy**. Próximo paso: Copywriter.
   - Si hay outputs de creative_director y copywriter pero no de design → **Fase 3: Copy listo, sin piezas gráficas**. Próximo paso: Design.
   - Si hay outputs de los tres pero no de pauta → **Fase 4: Producción lista, sin campaña**. Próximo paso: Media Buyer.
   - Si hay outputs de pauta (plan_campana o reporte) → **Fase 5: Campaña activa**. Revisar si hay brief_creativo pendiente.

4. Si hay un `brief_creativo_*.md` reciente en `agentes/04_pauta/outputs/<cliente>/`, mencionalo explícitamente: el Media Buyer pidió creativos nuevos y el Creative Director tiene que procesarlo.

## Entrega

Mostrá el reporte completo en pantalla. Cerrá con una línea de acción:

```
Va para [Elias / Nico / Felipe según el caso]. Próximo paso: [acción concreta y específica].
```

No suavices la info. Si falta algo, decí exactamente qué falta. Si todo está en orden, decilo.
