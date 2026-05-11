# Post Production — DV

Scripts ffmpeg/Whisper que asisten a los editores: multi-format, thumbnails y subtítulos automáticos.

NO reemplaza la edición creativa. Toma un **master editado** (mp4) y produce los entregables operativos del cliente.

## Estructura

```
post_production/
├── scripts/
│   ├── multiformat.py     # 9:16 / 1:1 / 16:9 desde master
│   ├── thumbnail.py       # PNG snapshot
│   ├── subtitles.py       # SRT via OpenAI Whisper API
│   └── process_master.py  # orquesta los 3
├── outputs/<cliente>/<fecha>/
└── .env.example
```

## Naming convention

Todos los scripts respetan el naming Drive de DV:
```
<CLIENTE>_<TipoContenido>_V<n>.<ext>
```

Ejemplo: `LopezProps_RecorridoVO_V1_9x16.mp4`, `LopezProps_RecorridoVO_V1_thumb.png`, `LopezProps_RecorridoVO_V1.srt`.

El validador `pre_commit_validators.py` ya bloquea naming malformado al commitear.

## Setup

```
pip install requests
cp .env.example .env
# editar .env con OPENAI_API_KEY
```

ffmpeg debe estar en PATH.

## Uso típico

```
# Master editado por Bauti / Gian / Fran:
master.mp4

python scripts/process_master.py \
  --input master.mp4 \
  --cliente lopez_propiedades \
  --tipo RecorridoVO \
  --version 1 \
  --thumb-at 3 \
  --transcribe
```

Genera en `outputs/lopez_propiedades/<fecha>/`:
- `LopezProps_RecorridoVO_V1_9x16.mp4`
- `LopezProps_RecorridoVO_V1_1x1.mp4`
- `LopezProps_RecorridoVO_V1_16x9.mp4`
- `LopezProps_RecorridoVO_V1_thumb.png`
- `LopezProps_RecorridoVO_V1.srt`

## Política

- Cada subproceso ffmpeg tiene timeout de 600s. Si un master tarda más, falla loud.
- Whisper API solo se invoca si `--transcribe` y hay `OPENAI_API_KEY`. Sin esos, skipea con warning.
- El master original NUNCA se modifica. Todos los outputs van a `outputs/`.
