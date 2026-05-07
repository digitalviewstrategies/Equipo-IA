---
name: buscar
description: Use this skill when the user wants to find assets across all DV agents — past guiones, briefs, copy, planes, reportes, designs. Triggers "buscar [keywords]", "tenemos algo de [tema]", "donde esta [pieza]", "que produjimos para [cliente] sobre [tema]", "ultimos outputs de [cliente]", "hay un guion sobre [tema]".
---

# Skill: Buscar assets

Buscador full-text sobre todos los outputs de los agentes (Creative Director, Copywriter, Design, Pauta).

## Comandos

```bash
# busqueda libre
python shared/scripts/asset_index.py search "captacion zona norte"

# filtros opcionales
python shared/scripts/asset_index.py search --cliente toribio_achaval "balcon"
python shared/scripts/asset_index.py search --tipo guion "captacion"
python shared/scripts/asset_index.py search --agente pauta "fatiga"

# ultimos outputs de un cliente
python shared/scripts/asset_index.py recent --cliente ini_propiedades 10

# rebuild manual (el cron lo reindexa cada 6 hs)
python shared/scripts/asset_index.py index
```

## Tipos disponibles
`guion`, `brief_carrusel`, `estrategia`, `meta_ad`, `caption`, `banco_hooks`,
`estrategia_copy`, `plan_campana`, `analisis`, `reporte_semanal`,
`reporte_mensual`, `brief_creativo`, `brief_diseno`, `alerta_daily`, `otro`.

## Entrega

Mostrá los resultados tal cual. Si el usuario pide el contenido completo de un asset, leelo con la tool `Read` desde el path.
