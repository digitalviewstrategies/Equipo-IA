---
description: Produce copy de Meta Ads (2 variantes) para cliente de DV o para DV misma
argument-hint: [cliente] [objetivo] [placement]
---

# Skill: Meta Ad

Produces copy de Meta Ads siguiendo el Metodo DV. Cubre workflows A (venta propiedad), B (captacion propietario) y D (captacion inmobiliaria para DV).

## Inputs

Argumentos posicionales: `$1=cliente`, `$2=objetivo`, `$3=placement`.

Objetivo puede ser: `venta_propiedad` | `captacion_propietario` | `captacion_inmobiliaria`.
Placement puede ser: `feed` | `stories` | `reels`.

Si falta cualquiera, preguntalos antes de continuar. Si el objetivo es `captacion_inmobiliaria` el cliente es siempre `digital_view`.

Ademas pedi datos especificos si aplica: para venta (zona, tipologia, precio/metros/diferencial si los hay); para captacion (zona objetivo, diferencial, resultados recientes con numeros); para DV (audiencia frio/retargeting, performance anterior si hay).

## Pasos

1. Carga el brand con `shared/brands/<cliente>.json`. Si no existe, pedi el nombre correcto. No produzcas copy sin brand.
2. Lee en orden: `context/frameworks_copy.md`, `context/audiencias.md`, `context/banco_hooks.md`, `context/mercado_inmobiliario_arg.md`.
3. Chequea briefs del Media Buyer en `../../04_pauta/outputs/<cliente>/`. Si hay briefs recientes con angulos ganadores, usalos.
4. Identifica el perfil de audiencia segun objetivo:
   - `venta_propiedad` → Perfil 1 (comprador)
   - `captacion_propietario` → Perfil 2 (propietario)
   - `captacion_inmobiliaria` → Perfil 3 (dueno de inmobiliaria)
5. Elegi el dolor principal y el tipo de hook (empatia o verdad incomoda para Meta Ads; no negacion).
6. Escribi 2 variantes con estructura Hook → Cuerpo (Dolor/Consecuencia/Solucion/Prueba) → CTA. Usa `templates/copy_meta_ads.md`.
7. Para `captacion_inmobiliaria`: la garantia 45 dias cierra, no abre. Primero dolor, despues solucion.
8. Guarda con:
   ```bash
   python scripts/output_manager.py save <cliente> meta_ad <objetivo>_<zona_o_variante>_v1
   ```
   O directamente usando el modulo (ver `scripts/output_manager.py`).

## Reglas criticas (no las violes)

- No inventes datos de propiedad (precio, metros, caracteristicas). Si no te los dieron, trabaja angulos de proceso/servicio.
- Palabras prohibidas: "suenos", "concretar", "profesionales de confianza", "acompanamiento personalizado", "pasion por el rubro".
- No emojis. No exclamaciones de entusiasmo. No urgencia artificial.
- No "leads" en copy cliente-final: usa "consultas", "interesados", "prospectos".
- Max 150 palabras por variante en feed sin justificacion.
- Voseo argentino, tuteo, sin "usted".
- El CTA no menciona precio salvo que sea diferencial real.

## Entrega

Mostra las 2 variantes en pantalla y confirma la ruta donde las guardaste.
