# Agentes

Cada subcarpeta es una fase del flujo operativo de DV (ver `../CLAUDE.md`). La numeración coincide con las fases del manual operativo.

| Fase | Directorio | Agentes | Estado |
|---|---|---|---|
| 01 | `01_contenido/` | `creative_director/`, `design/` | Maduro |
| 02 | `02_comercial/` | — | Scaffold |
| 03 | `03_delivery_reporting/` | — | Scaffold |
| 04 | `04_pauta/` | Media Buyer Meta (próximo) | Scaffold |

## Cómo agregar un agente nuevo

1. Crear el directorio dentro de la fase que corresponde (ej: `04_pauta/media_buyer/`).
2. Replicar el patrón estándar:
   ```
   <agente>/
   ├── CLAUDE.md          # Instrucciones del agente
   ├── README.md
   ├── context/           # Knowledge base
   ├── scripts/           # Código (Python, SDK calls, etc.)
   ├── examples/
   └── .env.example       # Si necesita credenciales
   ```
3. Si usa brand systems, leelos desde `shared/brands/` (nunca duplicar).
4. Actualizar la tabla de arriba y el `README.md` raíz.
