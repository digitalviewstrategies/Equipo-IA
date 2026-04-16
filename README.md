# Equipo IA — Digital View

Monorepo de los agentes de IA internos de Digital View (DV). Cada agente cubre una fase del flujo operativo de DV (ver `CLAUDE.md` para el contexto completo de la agencia y las fases).

## Mapa del repo

```
Equipo-IA/
├── CLAUDE.md                     # Contexto DV (fuente de verdad para todos los agentes)
├── DV_Manual_Operativo.docx      # Manual operativo completo
├── agentes/                      # Un directorio por fase operativa
│   ├── 01_contenido/
│   │   ├── creative_director/    # Ideación y guiones
│   │   └── design/               # Carruseles, placas, flyers
│   ├── 02_comercial/             # (pendiente)
│   ├── 03_delivery_reporting/    # (pendiente)
│   └── 04_pauta/                 # (pendiente) — Media Buyer Meta
├── shared/
│   └── brands/                   # Brand systems por cliente (datos compartidos)
└── docs/
    └── onboarding/               # Docs de onboarding de clientes nuevos
```

## Cómo usar un agente

Cada agente maduro tiene su propio `CLAUDE.md` y `README.md`. Abrí Claude Code apuntando al directorio del agente:

```bash
# Ejemplo: creative director
cd agentes/01_contenido/creative_director
claude
```

Claude carga automáticamente el `CLAUDE.md` del agente como instrucciones.

## Datos compartidos

Los **brand systems** de los clientes viven en `shared/brands/` y son leídos por los dos agentes de contenido. Para agregar un cliente nuevo seguí `shared/brands/_onboarding.md`.

## Estado de los agentes

| Fase | Directorio | Estado |
|---|---|---|
| 01 Contenido — Creative Director | `agentes/01_contenido/creative_director/` | Maduro |
| 01 Contenido — Design | `agentes/01_contenido/design/` | Maduro |
| 02 Comercial | `agentes/02_comercial/` | Scaffold |
| 03 Delivery & Reporting | `agentes/03_delivery_reporting/` | Scaffold |
| 04 Pauta (Media Buyer Meta) | `agentes/04_pauta/` | Scaffold — próximo |
