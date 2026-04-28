# Skill: planificar — Workflow A

Planificar una campaña nueva de Meta Ads para un cliente.

## Contexto necesario

Antes de empezar, cargá estos archivos:

1. `context/meta_ads_framework.md` — estructura de campañas, naming, objetivos, placements, categoría HOUSING.
2. `context/audiencias_inmobiliario.md` — segmentos de audiencia para real estate argentino.
3. `context/presupuestos_guia.md` — reglas de presupuesto, scaling, redistribución.

Si hay contradicción entre tu criterio y lo que dicen estos archivos, ganan los archivos.

## Pasos

### 1. Entender el pedido

Si falta cliente, objetivo, presupuesto mensual o propiedades/servicios a publicitar, preguntás todo en un solo mensaje. Si está completo, arrancás.

### 2. Cargar el brand system del cliente

```python
from scripts.output_manager import load_brand
brand = load_brand(cliente)
```

Si el cliente no existe en `shared/brands/`, parás y avisás que falta onboardearlo. Nunca inventés contexto.

### 3. Definir estructura de campaña

Siguiendo `meta_ads_framework.md`:

- **Objetivo**: Leads (mayoría de clientes DV), Traffic o Conversions.
- **Ad sets**: 2-4 por campaña, segmentados por audiencia o ubicación.
- **Ads por ad set**: 3-5 creativos para testear.
- **Budget split**: 70% audiencias probadas, 30% testing.
- **Placements**: Feed + Stories + Reels como default. Audience Network siempre off.
- **Categoría especial**: HOUSING obligatorio para todos los clientes DV.

### 4. Definir audiencias

Consultá `audiencias_inmobiliario.md` y el buyer persona del brand system. Definí:

- Audiencia core (datos demográficos + intereses).
- Audiencia lookalike (si hay lista de leads del cliente).
- Audiencia retargeting (IG engagers, web visitors, video viewers).
- Exclusiones (clientes existentes, competidores).

### 5. Revisar creativos disponibles

```python
from scripts.output_manager import load_creative_outputs
outputs = load_creative_outputs(cliente)
```

Buscá también en:
- `../../01_contenido/creative_director/outputs/<cliente>/` para guiones y briefs.
- `../../01_contenido/design/output/<cliente>/` para creativos renderizados.

- Si hay creativos suficientes y aprobados: los asignás al plan.
- Si faltan: generás un brief creativo (skill `/optimizar`) antes de avanzar.

### 6. Armar plan de campaña

Usá el template `templates/plan_campana.md`. Incluye:

- Naming de cada elemento (campaign, ad sets, ads).
- Estructura en árbol.
- Audiencias detalladas.
- Placements.
- Schedule.
- Budget diario y mensual.
- Creativos asignados a cada ad.

### 7. Guardar

```python
from scripts.output_manager import save_output
save_output(cliente, "plan_campana", nombre, contenido)
```

Cerrá con: "Va para Felipe. Próximo paso: aprobación del plan antes de crear en Meta."
