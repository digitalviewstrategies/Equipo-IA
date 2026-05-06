---
name: reporte-semanal
description: Use this skill to produce the visual weekly report for fase 6 (Lanzamiento y Seguimiento) — placa o carrusel 3-5 slides 1080x1080 con KPIs de la semana de campañas Meta + contenido organico (leads, CPL, CTR, alcance, mejor creativo, top placa). Cierra el loop con el cliente y materializa lo que Felipe + Elias trackean. NO sustituye al reporte completo del Sheet — es el resumen visual mandable por WhatsApp / posteable. Triggers "reporte semanal de [cliente]", "armame el reporte de la semana", "placa de KPIs de [cliente]", "reporte visual de la campaña", "resumen de la semana para [cliente]".
---

# Skill: Reporte semanal visual

Pieza de cierre de fase 6. Resume la semana en formato visual mandable por WhatsApp o posteable. Es la prueba al cliente de que la guita esta trabajando.

## Formatos cubiertos

1. **Placa unica** (1080x1080) — 3-5 KPIs principales en grilla. Para semanas standard.
2. **Carrusel 3-5 slides** (1080x1080) — slide portada + slide por bloque (pauta, organico, top creativo, proximos pasos). Para semanas con mas que mostrar.

## Antes de producir

Pedi si falta CUALQUIERA:
1. **Cliente**.
2. **Periodo** (ej: "semana 28/04 - 04/05").
3. **KPIs de pauta** (los que tengamos del Sheet de Felipe):
   - Leads generados.
   - CPL (costo por lead).
   - Inversion total.
   - Alcance / impresiones.
   - CTR.
4. **KPIs de organico** (opcional segun cliente):
   - Alcance organico.
   - Engagement.
   - Mejor pieza (placa/reel/carrusel) con metrica.
5. **Comparativa** (opcional pero potente): vs semana anterior (delta %).
6. **Proximos pasos** (1-3 bullets cortos): que se va a optimizar la semana que viene.

NO inventes numeros. Si falta CPL o leads, parar y pedir.

## Pasos

1. **Cargar brand** segun protocolo `context/brand_loader.md`. Extraer paleta y tipografias (en reporte el tono no aplica, son numeros).
2. Decidir formato: placa unica si hay 3-5 KPIs simples; carrusel si hay narrativa (pauta + organico + creativos + planes).
3. Layout placa unica:
   - Tag arriba: "REPORTE SEMANAL" + periodo.
   - Grilla 2x2 o 2x3 con KPIs. Cada KPI: numero gigante 200-280px + label corta abajo + delta % en acento (verde si mejora, color brand si neutral, NO rojo agresivo).
   - Logo cliente esquina inferior.
4. Layout carrusel:
   - Slide 1 (portada): "Resumen [periodo]" + cliente.
   - Slide 2: KPIs pauta (grilla con leads, CPL, inversion, CTR).
   - Slide 3: top creativo de la semana (thumbnail + metrica destacada).
   - Slide 4: organico (alcance + mejor pieza) — opcional.
   - Slide 5: proximos pasos (3 bullets) + logo DV pequeño abajo.
5. Pipeline: HTML + Playwright. Crear template `templates/reporte_semanal.html` (placa) y `templates/reporte_semanal_carrusel.html` (multi-slide).
6. Renderiza a `output/<cliente>/<YYYY-MM-DD>/reporte_semanal/`. Naming: `reporte_<cliente>_<YYYY-WW>.png` o por slide.
7. Invocar skill `design-qa`.
8. Mostra al usuario.
9. Iterar.
10. Subir a Drive con OK: `CLIENTE/05 Reportes/Reporte semana <YYYY-MM-DD>/`.

## Reglas no negociables

- NO inventes numeros. Cada KPI viene del Sheet de Felipe o del reporte de Elias.
- NO redondees al alza. CPL real, leads reales.
- Delta % siempre comparable (misma metrica semana anterior, mismo periodo).
- Moneda explicita en CPL e inversion ("USD 4.2", "ARS 3.500").
- Si hay metrica negativa (CPL subio, leads bajaron), NO la escondas — mostrala con el plan de optimizacion al lado. Honestidad > cosmetica.
- NO emojis (ni ✅ ni 📈 ni 🚀). Tipografia + flechas tipograficas (↑ ↓ →) si hace falta indicar direccion.
- Logo cliente principal. Logo DV chico, abajo, "by Digital View".

## Diferencia con el reporte completo

El reporte completo es el Sheet/doc que Elias arma para el cliente con tablas, comentarios y plan. ESTA pieza es el resumen visual mandable. Si el cliente quiere detalle, va al Sheet. Si quiere un screenshot rapido para mandar al socio o postear, usa esta.

## Entrega

Mostra el PNG (o set de PNGs si carrusel). Cierra: "Reporte [periodo] para [cliente] en `output/...`. Numeros cruzados con [Sheet/fuente]. Va asi o ajustamos algun KPI?"
