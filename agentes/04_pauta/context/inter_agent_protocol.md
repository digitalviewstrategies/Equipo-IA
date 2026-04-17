# Protocolo de Comunicacion Inter-Agente — Media Buyer

## Como funciona

La comunicacion entre agentes es via archivos compartidos en el monorepo. No hay APIs ni mensajes directos. Cada agente lee y escribe en sus propios outputs, y los otros agentes pueden leer esos outputs.

---

## Paths de outputs de cada agente

| Agente | Path de outputs |
|---|---|
| Creative Director | `agentes/01_contenido/creative_director/outputs/[cliente]/[fecha]/` |
| Design | `agentes/01_contenido/design/output/[cliente]/[fecha]/` |
| Media Buyer (vos) | `agentes/04_pauta/outputs/[cliente]/[fecha]/` |

**Path relativo desde scripts de Media Buyer:**

```python
# Desde 04_pauta/scripts/ hacia otros agentes
CREATIVE_DIR_OUTPUTS = Path(__file__).resolve().parents[2] / "01_contenido" / "creative_director" / "outputs"
DESIGN_OUTPUTS = Path(__file__).resolve().parents[2] / "01_contenido" / "design" / "output"
```

---

## Que lees de Creative Director

**Guiones** (`guion_*.md`):

- Estructura del video con bloques y lineas de dialogo.
- Hook variants (3 opciones).
- Angulo de dolor usado.
- Formato del sistema de video ads.
- Brief de produccion y edicion.

**Estrategias** (`estrategia_*.md`):

- Pilares de contenido del mes.
- Mix de formatos.
- Calendario.

**Ideas** (`ideas_*.md`):

- Las 3 ideas propuestas con angulo, formato, emocion.

**Para que los usas:** para saber que creativos se estan produciendo, que angulos se exploraron, y para mapear creativos a ads en tu plan de campana.

---

## Que lees de Design

**Creativos renderizados** (archivos `.png`):

- Carruseles (sets de 5-6 imagenes).
- Placas Meta Ads (cuadrado y vertical).
- Flyers.

**Para que los usas:** para saber que piezas visuales estan listas para subir a Meta como creativos de ads.

---

## Que escribis para Creative Director

### Brief creativo (`brief_creativo_*.md`)

Este es el documento mas importante del feedback loop. Formato obligatorio:

```markdown
# Brief Creativo — [Cliente] — [Fecha]

## Contexto de campana
- Objetivo: [Leads/Traffic/Conversions]
- Periodo analizado: [fecha inicio] a [fecha fin]
- Presupuesto del periodo: USD [X]
- Leads generados: [N]
- CPL promedio: USD [X]

## Creativos ganadores (SCALE)

| Creativo | Formato | Angulo | CPL | CTR | Hook Rate | Impresiones | Score |
|----------|---------|--------|-----|-----|-----------|-------------|-------|
| [nombre] | [tipo]  | [angulo] | USD X | X% | X% | X | X |

**Que funciono:**
- [Insight 1 basado en datos, no opinion]
- [Insight 2]

## Creativos perdedores (KILL)

| Creativo | Formato | Angulo | CPL | CTR | Hook Rate | Impresiones | Score |
|----------|---------|--------|-----|-----|-----------|-------------|-------|
| [nombre] | [tipo]  | [angulo] | USD X | X% | X% | X | X |

**Que no funciono:**
- [Insight 1 basado en datos]
- [Insight 2]

## Creativos en iteracion (ITERATE)

| Creativo | Problema detectado | Sugerencia |
|----------|-------------------|------------|
| [nombre] | [ej: buen hook pero body no retiene] | [ej: mantener hook, acortar body] |

## Lo que necesito
- [N] creativos nuevos para [formato]
- Angulos sugeridos basados en data:
  1. [Angulo que funciono, explorar variante]
  2. [Angulo nuevo que no se probo]
- Evitar: [angulos/formatos que no funcionaron, con razon]

## Insights del buyer persona (actualizados por performance)
- [Que resuena con la audiencia real vs la teorica del brand system]
- [Ej: "Los hooks de miedo funcionan 2x mejor que los de aspiracion para este cliente"]
```

---

## Que escribis para Design

### Brief de diseno (`brief_diseno_*.md`)

Formato mas simple, porque Design recibe el copy del Creative Director:

```markdown
# Brief Diseno — [Cliente] — [Fecha]

## Piezas necesarias
- [N] creativos Meta Ads formato [cuadrado/vertical/ambos]
- Tamano: [1080x1080 / 1080x1350 / 1080x1920]
- Tipo: [imagen estatica / carrusel / placa]

## Referencia de performance
- Mejor formato visual reciente: [cual, con metricas]
- Texto overlay vs imagen limpia: [que funciono mejor, con datos]
- Colores/estilos que performaron: [si hay data]

## Copy/guion a usar
- Ver: `agentes/01_contenido/creative_director/outputs/[cliente]/[fecha]/[archivo]`
- O copy inline si es una pieza simple:
  - Headline: [texto]
  - Body: [texto]
  - CTA: [texto]

## Notas de produccion
- [Especificaciones adicionales para el diseno]
- [Ej: "Probar version con y sin precio visible"]
```

---

## Flujo completo del loop

```
1. Media Buyer analiza performance (Workflow C)
       ↓
2. Media Buyer genera brief_creativo (Workflow E)
       ↓ guardado en 04_pauta/outputs/[cliente]/[fecha]/
3. Creative Director lee el brief
       ↓
4. Creative Director genera nuevas ideas y guiones
       ↓ guardado en creative_director/outputs/[cliente]/[fecha]/
5. Design recibe brief del Creative Director (o brief_diseno del Media Buyer)
       ↓
6. Design produce creativos visuales
       ↓ guardado en design/output/[cliente]/[fecha]/
7. Media Buyer toma los creativos y los sube a Meta (Workflow B)
       ↓
8. Volver al paso 1 despues de 7-14 dias de data
```

**Tiempo tipico del ciclo:** 2-3 semanas completas. La velocidad depende de la produccion de creativos.

---

## Reglas de comunicacion

1. **Siempre con datos.** Nunca pidas creativos nuevos sin incluir metricas de por que los necesitas.
2. **Sin opiniones vagas.** "No funciono" no es un insight. "CPL USD 12 vs target USD 5, hook rate 8% — el hook no engancha" si lo es.
3. **Sugerencias, no ordenes.** El Creative Director decide los angulos y formatos. Vos le das data para que tome mejores decisiones.
4. **Respeta los tiempos.** Producir un video toma 1-2 semanas. No pidas creativos nuevos como si fueran instantaneos.
5. **Un brief por pedido.** No mezcles pedidos de varios clientes en un solo brief.
