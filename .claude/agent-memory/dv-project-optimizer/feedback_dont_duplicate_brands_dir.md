---
name: No duplicar shared/brands dentro de pauta
description: agentes/04_pauta/shared/brands/ contiene un toribio_achaval.json desactualizado (28 lineas) vs el real en shared/brands/toribio_achaval.json (10KB)
type: feedback
---

Existe `agentes/04_pauta/shared/brands/toribio_achaval.json` con un schema viejo y minimo (solo `meta_ads`, `geo`, `buyer_persona`, `presupuesto_default`). El brand "real" vive en `shared/brands/toribio_achaval.json` con el schema completo de DV (10KB con colors, voice, narrative, etc).

**Why:** un agente que lea el wrong path va a usar info incompleta o desactualizada. Output_manager de pauta ya apunta correctamente a `ROOT/shared/brands/`, asi que `agentes/04_pauta/shared/brands/` es 100% basura legacy.

**How to apply:** proponer eliminar `agentes/04_pauta/shared/` completo. Confirmar con grep que ningun script lo usa antes de borrar. Si tiene info utica (campos meta_ads especificos) integrarla al brand JSON oficial primero.
