---
description: Genera un banco de hooks para un cliente y audiencia target
argument-hint: [cliente] [audiencia] [cantidad]
---

# Skill: Banco de Hooks

Produce un set de hooks validados para alimentar campanas y contenido organico de un cliente.

## Inputs

Argumentos: `$1=cliente`, `$2=audiencia`, `$3=cantidad` (default 10).

Audiencia: `comprador` | `propietario` | `inmobiliaria`.

## Pasos

1. Carga brand del cliente (`shared/brands/<cliente>.json`) para ajustar tono, lexico y diferencial.
2. Lee `context/banco_hooks.md` como referencia. No dupliques los hooks existentes — generá variaciones o angulos nuevos.
3. Lee `context/audiencias.md` y enfoca el dolor especifico de la audiencia elegida.
4. Produci `cantidad` hooks distribuidos en los 3 tipos:
   - **Negacion**: romper creencia instalada
   - **Empatia**: nombrar el dolor mejor que el propio cliente
   - **Verdad incomoda**: lo que nadie dice en voz alta
5. Cada hook debe poder leerse en 3 segundos. Una o dos lineas.
6. Agrupa por tipo en el output. Agrega 1 linea debajo de cada hook explicando el angulo (para decidir cual usar).
7. Guarda:
   ```bash
   python scripts/output_manager.py save <cliente> banco_hooks <audiencia>_v1
   ```

## Reglas

- Especificidad del rubro (reserva, captacion, tasacion, top producer, boca en boca) genera mas resonancia que generico.
- No palabras prohibidas.
- Sin clisses.

## Entrega

Mostra el banco completo agrupado por tipo y confirma la ruta.
