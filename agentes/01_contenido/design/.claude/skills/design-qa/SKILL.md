---
name: design-qa
description: Use this skill to validate any rendered design piece against DV's design_principles.md checklist BEFORE showing to user or uploading to Drive. Auto-runs the 10-point visual checklist (jerarquia, margenes, contraste, paleta <=3, peso >=700, sin elementos prohibidos, logo correcto, lectura en 2s) y devuelve PASS / FLAG / BLOCK por punto. NO reescribe — solo audita. Triggers "validame esta pieza", "chequeame el diseño", "design qa de [pieza]", "esta lista para subir?", "auditame el carrusel/placa/flyer/creativo". Usar proactivamente despues de renderizar cualquier pieza de las otras skills (carrusel-*, placa-*, flyer-*, meta-ad-*, reel-cover, testimonio-placa, reporte-semanal) y antes del OK del usuario.
---

# Skill: Design QA — validador visual

Audita una pieza renderizada contra el checklist de `context/design_principles.md` y el brand system del cliente. Devuelve veredicto por punto. NO modifica la pieza.

## Cuando correr

- Despues de renderizar cualquier pieza, antes de mostrarla al usuario.
- Cuando el usuario pide "validame", "chequeame", "esta lista".
- Antes de subir a Drive (gate duro).

## Inputs

1. **Path(s) de la(s) pieza(s)** renderizada(s) (PNG/JPG en `output/...`).
2. **Cliente** (para cargar `shared/brands/<cliente>.json`).
3. **Tipo de pieza** (carrusel-captacion, carrusel-educativo, placa, flyer, meta-ad, reel-cover, testimonio, reporte). Define reglas especificas (ej: logo solo en slide final aplica a carrusel; margen 200px aplica a flyer A4).

Si falta alguno, pedi antes de auditar.

## Checklist a evaluar

Cada item devuelve PASS / FLAG / BLOCK.

### Composicion
1. **Jerarquia clara** — un solo elemento dominante (50-70% area visual). BLOCK si dos elementos compiten.
2. **Margen seguro respetado** — segun tipo (80px cuadrado/vertical, 100px stories, 60px placa, 200px flyer A4). BLOCK si texto toca borde.
3. **Espacio negativo** — la pieza respira. FLAG si esta saturada.
4. **Rotacion sutil** — al menos 1 elemento entre 0.5° y 3° (o scribble hasta -8°). FLAG si simetria perfecta total.

### Tipografia
5. **Tamaños minimos** — headline ≥80px, numero gigante ≥150px (ideal 300-420), body ≥22px. BLOCK si headline <80px.
6. **Pesos** — headlines 800/900, subheadlines 700/800. BLOCK si headline en 400 o thin/light.
7. **Maximo 2 tipografias** distintas en la pieza. BLOCK si hay 3+.

### Color
8. **Maximo 3 colores efectivos** (1 fondo + 1 texto + 1 acento). BLOCK si hay 4+ colores compitiendo.
9. **Contraste suficiente** texto vs fondo (ratio WCAG AA minimo 4.5:1 para body, 3:1 headline). BLOCK si insuficiente.
10. **Paleta del brand** — colores HEX coinciden con `shared/brands/<cliente>.json`. BLOCK si hay colores fuera del sistema.

### Elementos prohibidos universales DV (cualquiera = BLOCK, no overridables)
- Gradientes multicolor.
- Drop shadows >4px blur o efectos 3D/bisel.
- Emojis.
- Tipografias prohibidas globales (Comic Sans, Papyrus, Impact, Bradley Hand, scripts cursivas).
- Borders >16px (excepto botones puntuales).
- Stock photos cliche ("familia feliz frente a casa").

### Elementos prohibidos por default DV (overridables por brand JSON)
Estas reglas se aplican salvo que el brand JSON las permita explicitamente via `visual_style`:
- Pasteles/tierra como paleta principal → BLOCK salvo `visual_style.allow_pastels: true`.
- Dorado como primario → BLOCK salvo `visual_style.allow_gold_primary: true`.
- Tipografias serif decorativas → BLOCK salvo el brand defina una serif en `typography`.

Si el brand JSON tiene una regla que contradice estos defaults, el brand manda. Documentar en el output de QA que la regla viene del brand: "Pastel approved by brand JSON (visual_style.allow_pastels)".

### Reglas por tipo de pieza
- **Carrusel**: logo solo en slide final. Numeracion (02/06) en slides intermedios. BLOCK si logo en todos los slides.
- **Placa propiedad**: precio con moneda explicita ("USD 285.000"). BLOCK si "$" sin aclarar.
- **Flyer A4**: 300dpi (verificar via metadata). BLOCK si <300dpi.
- **Meta Ad**: zona segura UI Stories (20% top/bottom libre en vertical). BLOCK si CTA en zona de UI.
- **Reel cover**: hook ocupa 50%+ del area. BLOCK si hook chico.

### Lectura
- **Test 2 segundos** — el mensaje principal se lee en <=2s. Si dudas, FLAG.

## Output

Devolver tabla markdown:

```
| # | Item | Veredicto | Detalle |
|---|------|-----------|---------|
| 1 | Jerarquia clara | PASS | precio domina 60% |
| 2 | Margen seguro | BLOCK | "USD 285.000" toca borde derecho |
| ... |
```

Cerrar con UNO de tres veredictos globales:
- **PASS** — 0 BLOCK, 0-2 FLAG. Lista para mostrar/subir.
- **FLAG** — 0 BLOCK, 3+ FLAG. Mostrar al usuario marcando issues.
- **BLOCK** — 1+ BLOCK. NO mostrar/subir. Listar que arreglar.

## Como inspeccionar la pieza

Para chequeos automatizables, usar `mcp__plugin_context-mode_context-mode__ctx_execute_file` con Python + Pillow:
- Tamaño/dpi: `Image.open(path).size`, `.info.get('dpi')`.
- Paleta dominante: `Image.quantize` + contar colores.
- Contraste: extraer pixels en zonas de texto (requiere coords del template).

Para chequeos visuales (jerarquia, lectura 2s, rotacion), usar Read sobre el PNG y juicio del modelo.

## Reglas no negociables

- NO modifica la pieza. Solo audita.
- NO marca PASS si hay duda — preferir FLAG.
- BLOCK siempre que un item sea binario (margen, dpi, peso tipografico).
- Si falta el brand JSON, BLOCK global con mensaje "falta shared/brands/<cliente>.json — invocar skill `brand-system`".

## Entrega

Mostrar la tabla + veredicto. Si BLOCK, listar concretamente que cambiar. Cerrar: "Pieza [path] — veredicto: [PASS/FLAG/BLOCK]. [Si BLOCK] No subas hasta arreglar items 2, 5, 8."
