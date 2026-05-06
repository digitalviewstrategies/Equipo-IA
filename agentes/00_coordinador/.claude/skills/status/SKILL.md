---
name: status
description: Use this skill when the user asks for the current status of a client — what outputs exist, what phase they are in, what is missing or pending. Triggers "status [cliente]", "como estamos con [cliente]", "que hay de [cliente]", "en que fase esta [cliente]", "que falta para [cliente]", "mostrame el estado de [cliente]".
---

# Skill: Status de cliente

Muestra el estado operativo completo de un cliente derivado del filesystem (gates, evidencia, siguiente accion).

## Antes de ejecutar

Necesitas el **nombre del cliente** tal como aparece en `shared/brands/` (ej. `toribio_achaval`, `ini_propiedades`). Si no lo recibiste, preguntalo. Para listar disponibles: `python agentes/00_coordinador/scripts/state_manager.py --all`.

## Pasos

1. Corre el state manager (deriva todo automaticamente del filesystem y persiste snapshot en `shared/state/<cliente>.json`):

```bash
python agentes/00_coordinador/scripts/state_manager.py <cliente>
```

Si el cliente no existe en `shared/brands/`, el script avisa y lista los disponibles. Pará ahí.

2. Leé el output. Trae:
   - `fase_actual` (ultima fase cerrada)
   - `gates` (1-6, cada uno: `closed` / `open` / `blocked`)
   - `evidencia` (counts reales: guiones, copy, disenos, plan, campanas)
   - `siguiente_accion` (owner + tarea + trigger concreto)

3. Si hay un `brief_creativo_*.md` reciente en `agentes/04_pauta/outputs/<cliente>/`, mencionalo: el Media Buyer pidio creativos nuevos y el Creative Director tiene que procesarlo (este caso no lo cubre el state manager linealmente — es un loop lateral).

## Entrega

Mostrá el output del state manager tal cual. Cerrá con la linea de la `siguiente_accion`:

```
Va para [owner]. Proximo paso: [tarea]. Trigger: [trigger].
```

No suavices. Si la fase actual es `0_pre_kickoff`, el cliente no esta onboardeado. Si todas las fases estan `closed`, decilo.
