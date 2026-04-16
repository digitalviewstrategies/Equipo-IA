# Shared

Datos y recursos compartidos por más de un agente. **Regla**: algo solo vive acá si lo consumen al menos dos agentes, o si es data canónica del negocio (no del agente).

## Contenido

- **`brands/`** — brand systems por cliente (JSON + assets). Fuente única de verdad para colores, tipografías, buyer persona, ángulos de dolor y demás. Consumido hoy por `agentes/01_contenido/creative_director/` y `agentes/01_contenido/design/`.

## Cómo se accede desde los scripts

Los scripts resuelven `shared/brands/` relativo a la raíz del repo, subiendo desde la carpeta del agente:

```python
from pathlib import Path
# scripts → agente → fase → agentes → ROOT
BRANDS_DIR = Path(__file__).resolve().parents[4] / "shared" / "brands"
```

No hardcodear paths absolutos y no duplicar archivos acá adentro en cada agente.
