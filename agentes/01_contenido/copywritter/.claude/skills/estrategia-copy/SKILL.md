---
name: estrategia-copy
description: Use this skill when the user asks to build a copy strategy or plan of angles for a client's campaign or period. Produces 4-6 distinct angles with hook type, body structure and recommended formats. Triggers "armame la estrategia de copy", "plan de angulos", "estrategia de contenido para [cliente]", "plan mensual de copy", "que angulos uso para [cliente]", "estrategia de campana".
---

# Skill: Estrategia de Copy

Produce un plan de 4-6 angulos para guiar la produccion de copy de un cliente durante un periodo o campana.

## Antes de producir

Pedi si falta:
1. **Cliente**.
2. **Periodo o campana** (ej. `mayo_2026`, `campana_captacion_martinez`).
3. **Objetivo principal** (venta / captacion / autoridad / mix).
4. **Audiencia prioritaria**.
5. **Budget o cantidad de piezas** (dimensiona los angulos).
6. **Contexto especifico**: lanzamiento de proyecto, zona nueva, caso reciente.

## Pasos

1. Carga `shared/brands/<cliente>.json`.
2. Lee los 4 archivos de `context/` completos.
3. Lee outputs recientes en `outputs/<cliente>/` (ultimos 30 dias). Detecta angulos ya usados para no repetir.
4. Chequea briefs del Media Buyer en `../../04_pauta/outputs/<cliente>/`. Angulos con performance validada entran al plan.
5. Propone 4-6 angulos distintos. Por cada angulo:
   - **Nombre del angulo** (descriptivo, no generico)
   - **Dolor especifico** que ataca
   - **Tipo de hook recomendado** (negacion / empatia / verdad incomoda)
   - **Ejemplo de hook** (1 linea)
   - **Estructura del cuerpo** (Dolor/Consecuencia/Solucion/Prueba)
   - **CTA sugerido**
   - **Formatos recomendados** (Meta Ad feed, caption Reel, carrusel, etc.)
6. Cerra con un calendario sugerido (que angulo pegar primero y por que).
7. Guarda el archivo con el tool Write en `outputs/<cliente>/<YYYY-MM-DD>/estrategia_copy_<periodo>.md` (fecha de hoy en ISO).

## Reglas

- Los angulos deben ser mutuamente distintos. Si dos atacan el mismo dolor, fusionalos.
- No "mix de contenido" generico. Cada angulo es una idea fuerte.
- Si no hay caso real disponible, marcalo en los angulos que lo requieren.

## Entrega

Mostra el plan completo y confirma la ruta.
