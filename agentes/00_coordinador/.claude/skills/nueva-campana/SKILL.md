---
name: nueva-campana
description: Use this skill when the user wants to start or coordinate a full campaign production flow for a client — from creative ideation through Meta Ads execution. Triggers "nueva campana para [cliente]", "arrancamos con [cliente]", "iniciar flujo para [cliente]", "que necesitamos para lanzar [cliente]", "coordina la produccion de [cliente]", "armame el flujo de campana para [cliente]".
---

# Skill: Nueva Campaña

Coordina el flujo completo de producción para un cliente: desde brief creativo hasta piezas listas para pauta. No produce contenido — determina qué hay disponible, qué falta y qué orden seguir.

## Antes de ejecutar

Necesitás:
1. **Cliente** (nombre exacto en `shared/brands/`).
2. **Objetivo de la campaña**: `venta_propiedad` | `captacion_propietario` | `captacion_inmobiliaria`. Si no lo recibiste, preguntalo.
3. **Datos adicionales opcionales**: zona, tipología, presupuesto, fecha de inicio estimada.

## Pasos

### 1. Validar que el cliente está onboardeado

```python
from scripts.output_manager import brand_exists, load_brand
if not brand_exists(cliente):
    # Para acá. El cliente necesita kickoff primero (/kickoff <cliente>)
```

Si no existe el brand, indicá que hay que correr `/kickoff <cliente>` antes de continuar.

### 2. Cargar brand y revisar configuración

```python
brand = load_brand(cliente)
```

Verificá que tiene `meta_ads.ad_account_id`. Si no lo tiene, el Media Buyer no va a poder crear la campaña — avisalo como alerta.

### 3. Auditar outputs existentes

```python
from scripts.output_manager import get_client_outputs, get_latest_output
outputs = get_client_outputs(cliente)
```

Para cada agente, determiná:

| Agente | Qué buscar | Está listo? |
|---|---|---|
| Creative Director | Guiones o briefs de carrusel recientes | SI / NO |
| Copywriter | `meta_ad_*.md` del objetivo actual | SI / NO |
| Design | PNGs en `design/output/<cliente>/` | SI / NO |
| Pauta | `brief_creativo_*.md` (feedback loop activo?) | SI / NO |

### 4. Determinar punto de entrada

Según lo que encontraste, el flujo arranca en el primer agente que no tiene output:

**Caso A — Cliente sin nada:**
```
Creative Director → Copywriter → Design → Media Buyer
```
Indicá que hay que arrancar por Creative Director.

**Caso B — Hay guiones pero no copy ni diseño:**
```
Copywriter (en paralelo con Design si el brief de carrusel ya existe) → Media Buyer
```

**Caso C — Hay copy y guiones pero no diseño:**
```
Design → Media Buyer
```

**Caso D — Hay brief_creativo del Media Buyer (feedback loop):**
```
Creative Director primero (procesando el brief) → Copywriter → Design → Media Buyer
```
Esto tiene prioridad sobre cualquier otro flujo en progreso.

**Caso E — Todo listo:**
```
Media Buyer puede arrancar ahora.
```

### 5. Armar el plan de ejecución

Generá un documento con:

```markdown
# Plan de Campaña — [Cliente] — [Objetivo] — [Fecha]

## Estado actual
[Resumen de qué hay y qué falta]

## Flujo de producción
[Orden de agentes con pasos concretos]

## Paso inmediato
[Qué hacer ahora mismo, quién lo hace]

## Checklist de aprobaciones
- [ ] Guiones/brief aprobado por Nico
- [ ] Copy aprobado por Nico/Valen
- [ ] Piezas aprobadas por el cliente
- [ ] Plan de campaña aprobado por Felipe
```

### 6. Guardar

```python
from scripts.output_manager import save_output
save_output(cliente, "plan_ejecucion", f"{objetivo}_{fecha}", contenido)
```

## Entrega

Mostrá el plan completo. Cerrá con:
```
Paso inmediato: [acción específica]. Va para [Nico / Elias / Felipe según el caso].
```

Si hay varias cosas para hacer en paralelo, indicalo explícitamente. El objetivo es que Elias tenga todo claro sin tener que preguntar.
