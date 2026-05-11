---
name: outputs dirs deben ir a .gitignore
description: Cada modulo que produce outputs binarios debe tener su carpeta outputs/ en .gitignore antes del primer commit
type: feedback
---

Todo modulo nuevo que genere artefactos (mp4, png, srt, json grandes) en una carpeta `outputs/` debe agregar esa ruta a `.gitignore` ANTES del primer commit del modulo.

**Why:** `03_delivery_reporting/outputs/` ya esta ignorado (line 19). En sprint 4 (post_production) la carpeta se creo vacia y no se ignoro — riesgo de que se cuelen .mp4/.srt en commits futuros una vez que se corra el script.

**How to apply:** en pre-commit audit, si veo un modulo nuevo con subcarpeta `outputs/` (vacia o no), FLAG hasta que este en `.gitignore`. Patron canonico: `agentes/<NN_agente>/<modulo>/outputs/`.
