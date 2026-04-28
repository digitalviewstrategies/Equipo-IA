# Contexto de sesion — Agente Copywriter

**Fecha:** 2026-04-21
**Estado:** Implementacion completa. Listo para usar.

---

## Que se hizo

Se creo el agente copywriter de DV desde cero en `agentes/01_contenido/copywritter/`.

### Archivos creados

```
agentes/01_contenido/copywritter/
├── CLAUDE.md                          ← Instrucciones del agente (workflows, reglas, outputs)
├── context/
│   ├── frameworks_copy.md             ← Metodo DV, hooks Hormozi, estructuras de copy
│   ├── audiencias.md                  ← 4 perfiles: comprador, propietario, inmobiliaria, DV
│   └── banco_hooks.md                 ← ~45 hooks por audiencia y tipo listos para usar
│   (terminologia/dolores/estacionalidad: ver shared/contexto_inmobiliario.md)
├── templates/
│   ├── copy_meta_ads.md               ← Template de output para Meta Ads
│   └── copy_caption_organico.md       ← Template de output para captions
├── examples/
│   └── ejemplos_output.md             ← 6 ejemplos completos de referencia de calidad
└── scripts/
    └── output_manager.py              ← Carga brands, guarda outputs (patron identico a 04_pauta)
```

### Capacidades del agente

Cinco workflows:
- **A**: Meta Ads venta de propiedades (para clientes de DV)
- **B**: Meta Ads captacion de mandatos (para clientes de DV)
- **C**: Captions organicos (para clientes de DV)
- **D**: Meta Ads de DV para captar nuevas inmobiliarias
- **E**: Captions organicos de DV para captar nuevas inmobiliarias

Lee `shared/brands/<cliente>.json` para tono y contexto. Guarda outputs en `outputs/<cliente>/<YYYY-MM-DD>/`.

---

## Como usarlo

Abrilo con `claude` desde la carpeta `agentes/01_contenido/copywritter/`.

Pedidos de ejemplo:
- "Generá 2 opciones de Meta Ad para digital_view, objetivo: captar una inmobiliaria nueva, audiencia fria en CABA"
- "Escribi un caption organico para Abitat, el video muestra un recorrido de departamento en Palermo"
- "Armame un banco de hooks para captacion de propietarios para Rubica, zona Vicente Lopez"

---

## Que falta / posibles mejoras

- No tiene `.claude/settings.local.json` (se puede agregar si se necesitan permisos especificos).
- No tiene `README.md` (no es necesario para operar).
- El banco de hooks es un punto de partida; crecer con los que funcionen en pauta (coordinado con Felipe/Media Buyer).
- Si se quiere integracion bidireccional con Design, agregar un workflow F para formatear el copy en brief para Fefi.
