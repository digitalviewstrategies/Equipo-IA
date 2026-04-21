---
name: banco-hooks
description: Use this skill when the user asks to generate a bank of hooks for a client's campaign or content. Produces hooks organized by type (negacion, empatia, verdad incomoda) for a specific target audience. Triggers "armame hooks", "banco de hooks", "ideas de ganchos", "hooks para [cliente]", "generame hooks para captacion", "dame hooks de propietarios", "hooks para compradores".
---

# Skill: Banco de Hooks

Produce un set de hooks validados para alimentar campanas y contenido organico.

## Antes de producir

Pedi si falta:
1. **Cliente**.
2. **Audiencia**: `comprador` | `propietario` | `inmobiliaria`.
3. **Cantidad** (default 10).

## Pasos

1. Carga brand (`shared/brands/<cliente>.json`) para ajustar tono, lexico y diferencial.
2. Lee `context/banco_hooks.md` como referencia. No dupliques hooks existentes - generá variaciones o angulos nuevos.
3. Lee `context/audiencias.md` y enfoca el dolor especifico de la audiencia elegida.
4. Produci `cantidad` hooks distribuidos en los 3 tipos:
   - **Negacion**: romper creencia instalada
   - **Empatia**: nombrar el dolor mejor que el propio cliente
   - **Verdad incomoda**: lo que nadie dice en voz alta
5. Cada hook debe leerse en 3 segundos. Una o dos lineas.
6. Agrupa por tipo en el output. Agrega 1 linea debajo de cada hook explicando el angulo.
7. Guarda el archivo con el tool Write en `outputs/<cliente>/<YYYY-MM-DD>/banco_hooks_<audiencia>_v1.md` (fecha de hoy en ISO).

## Reglas

- Especificidad del rubro (reserva, captacion, tasacion, top producer, boca en boca) genera mas resonancia que generico.
- No palabras prohibidas. Sin cliches.

## Entrega

Mostra el banco agrupado por tipo y confirma la ruta.
