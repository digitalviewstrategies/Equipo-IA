---
description: Plan de angulos y mensajes de copy para una campana o periodo
argument-hint: [cliente] [periodo_o_campana]
---

# Skill: Estrategia de Copy

Produce un plan de 4-6 angulos para guiar la produccion de copy de un cliente durante un periodo o campana especifica.

## Inputs

Argumentos: `$1=cliente`, `$2=periodo_o_campana` (ej. `mayo_2026`, `campana_captacion_martinez`).

Pregunta antes de empezar:
- Objetivo principal del periodo (venta / captacion / autoridad / mix).
- Audiencia prioritaria.
- Budget o cantidad de piezas estimada (ayuda a dimensionar los angulos).
- Contexto especifico: lanzamiento de proyecto, zona nueva, caso reciente, etc.

## Pasos

1. Carga `shared/brands/<cliente>.json`.
2. Lee los 4 archivos de `context/` completos.
3. Lee outputs recientes en `outputs/<cliente>/` (ultimos 30 dias). Detecta angulos ya usados para no repetir.
4. Chequea briefs del Media Buyer en `../../04_pauta/outputs/<cliente>/` — los angulos con performance validada entran al plan.
5. Propone 4-6 angulos distintos. Por cada angulo:
   - **Nombre del angulo** (descriptivo, no generico)
   - **Dolor especifico** que ataca
   - **Tipo de hook recomendado** (negacion / empatia / verdad incomoda)
   - **Ejemplo de hook** (1 linea)
   - **Estructura del cuerpo** (que usar en Dolor/Consecuencia/Solucion/Prueba)
   - **CTA sugerido**
   - **Formatos recomendados** (Meta Ad feed, caption Reel, carrusel, etc.)
6. Cerra con un calendario sugerido (que angulo pegar primero y por que).
7. Guarda:
   ```bash
   python scripts/output_manager.py save <cliente> estrategia_copy <periodo>
   ```

## Reglas

- Los angulos tienen que ser mutuamente distintos. Si dos atacan el mismo dolor, fusionalos.
- No propongas "mix de contenido" generico. Cada angulo es una idea fuerte.
- Si no hay caso real disponible para el cliente, marcalo explicitamente en los angulos que lo requieren.

## Entrega

Mostra el plan completo en pantalla y confirma la ruta.
