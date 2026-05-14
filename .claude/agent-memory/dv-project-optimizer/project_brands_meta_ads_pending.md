---
name: Brands sin meta_ads block configurado
description: Solo digital_view tiene meta_ads completo, el resto necesita page_id/pixel_id (y muchos ad_account_id) para que pauta funcione
type: project
---

[ACTUALIZADO 2026-05-14] Estado actual: los brand JSONs sin `meta_ads.ad_account_id` quedaron en 3: `fidez_group`, `matias_di_meola`, `zipcode`. Los 16 restantes (incluyendo team_noia, que unifica turco + jose_maria_chaher post-merge 2026-05-14) tienen al menos `ad_account_id` cargado. Falta validar `page_id` y `pixel_id` por cliente.

Historico (pre-merge): de los 13 brands originales, solo `digital_view.json` tenia el bloque meta_ads completo. Los otros (toribio_achaval, abitat, fidez_group, juan_caillet_bois, matias_di_meola, ini_propiedades, jose_maria_chaher, mauro_peralta, viviana_sasia, rubica_inmobiliaria, zipcode) NO tenian bloque meta_ads.

Caso especial: `agentes/04_pauta/shared/brands/toribio_achaval.json` (que es legacy y debe borrarse) tiene `ad_account_id` valido pero `page_id: null` y `pixel_id: null`.

**Why:** el agente Media Buyer falla al lanzar campañas reales si no encuentra `brand["meta_ads"]["ad_account_id"]`. Hoy esta operando solo para digital_view y toribio (parcial).

**How to apply:** este es un onboarding tecnico, no codigo. Felipe debe completar para cada cliente: ad_account_id (con prefijo `act_`), page_id (Facebook Page de la inmobiliaria), pixel_id (Meta pixel del cliente). Trabajo manual en Meta Business Manager. Escalar a Felipe.
