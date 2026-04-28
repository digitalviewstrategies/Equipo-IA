---
name: meta-ad
description: Use this skill when the user asks to produce Meta Ads copy for a real estate client of Digital View or for DV itself. Covers workflows A (property sale), B (property capture) and D (immobiliaria capture for DV). Triggers "armame un meta ad", "copy para pauta", "anuncio de meta", "ad de venta de propiedad", "ad de captacion", "copy para captar inmobiliarias", "pauta para [cliente]", "hace un ad".
---

# Skill: Meta Ad

Produces copy de Meta Ads siguiendo el Metodo DV (Dolor -> Consecuencia -> Solucion -> Prueba).

## Antes de producir

Necesitas tres datos. Si no los tenes del prompt, preguntalos en una sola vuelta:

1. **Cliente** (nombre tal cual aparece en `shared/brands/`). Si el objetivo es captar inmobiliarias, el cliente es `digital_view`.
2. **Objetivo**: `venta_propiedad` | `captacion_propietario` | `captacion_inmobiliaria`.
3. **Placement**: `feed` | `stories` | `reels`.

Pedi tambien datos especificos si aplica: para venta (zona, tipologia, precio/metros/diferencial); para captacion (zona objetivo, diferencial, resultados recientes con numeros); para DV (audiencia frio/retargeting, performance anterior).

## Pasos

1. Carga el brand con `shared/brands/<cliente>.json`. Si no existe, pedi el nombre correcto. No produzcas copy sin brand.
2. Lee en orden: `context/frameworks_copy.md`, `context/audiencias.md`, `context/banco_hooks.md`, `shared/contexto_inmobiliario.md`.
3. Chequea briefs del Media Buyer en `../../04_pauta/outputs/<cliente>/`. Si hay briefs recientes con angulos ganadores, usalos.
4. Identifica el perfil de audiencia segun objetivo:
   - `venta_propiedad` -> Perfil 1 (comprador)
   - `captacion_propietario` -> Perfil 2 (propietario)
   - `captacion_inmobiliaria` -> Perfil 3 (dueno de inmobiliaria)
5. Elegi el dolor principal y el tipo de hook (empatia o verdad incomoda; no negacion para Meta Ads).
6. Escribi 2 variantes con estructura Hook -> Cuerpo (Dolor/Consecuencia/Solucion/Prueba) -> CTA. Usa `templates/copy_meta_ads.md`.
7. Para `captacion_inmobiliaria`: la garantia 45 dias cierra, no abre. Primero dolor, despues solucion.
8. Guarda el archivo con el tool Write en `outputs/<cliente>/<YYYY-MM-DD>/meta_ad_<objetivo>_<zona_o_variante>_v1.md` (fecha de hoy en ISO).

## Reglas criticas

- No inventes datos de propiedad (precio, metros, caracteristicas). Si no te los dieron, angulos de proceso/servicio.
- Palabras prohibidas: "suenos", "concretar", "profesionales de confianza", "acompanamiento personalizado", "pasion por el rubro".
- No emojis. No exclamaciones de entusiasmo. No urgencia artificial.
- No "leads" en copy cliente-final: usa "consultas", "interesados", "prospectos".
- Max 150 palabras por variante en feed sin justificacion.
- Voseo argentino, tuteo, sin "usted".
- El CTA no menciona precio salvo diferencial real.

## Entrega

Mostra las 2 variantes en pantalla y confirma la ruta donde las guardaste.
