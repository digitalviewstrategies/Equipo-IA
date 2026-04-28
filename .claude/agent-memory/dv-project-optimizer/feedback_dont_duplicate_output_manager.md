---
name: No duplicar output_manager.py por agente
description: Existen 6 copias divergentes de output_manager.py con drift entre agentes
type: feedback
---

Existen 6 copias de `output_manager.py` con drift confirmado por md5: 00_coordinador, 02_comercial, 03_delivery_reporting, 04_pauta, 01_contenido/copywritter, 01_contenido/creative_director. Todos exponen `load_brand` y `save_output` pero con `TIPOS_VALIDOS` distintos por agente, calculo de path raiz distinto (`parents[3]` vs `parents[4]`) y contenidos divergentes.

**Why:** cada vez que se cambia la firma o un nuevo tipo de output se introduce, hay que tocar 6 archivos. Es la receta clasica de bugs silenciosos. Ya hubo drift comprobado.

**How to apply:** proponer un modulo unico `shared/lib/output_manager.py` con `load_brand`, `save_output(agente, cliente, tipo, ...)` que reciba el agente como parametro. Cada agente importa via `sys.path` o symlink. Los `TIPOS_VALIDOS` por agente se mantienen en una constante exportada por agente, no se hardcodean.
