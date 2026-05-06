---
name: placa-propiedad
description: Use this skill when the user asks for an individual property card — 1080x1080 or 1080x1350 with photo, price, m2, location and 4 data icons. Most repetitive day-to-day deliverable. Triggers "placa de la propiedad [X]", "placa de [direccion]", "armame una placa para [cliente]", "placa para [propiedad] de [cliente]", "placa individual".
---

# Skill: Placa de propiedad individual

Pieza unica cuadrada (1080x1080) o vertical (1080x1350). Foto de la propiedad, titulo, precio gigante, 4 iconos con datos (dormitorios, banos, m2, cochera), ubicacion, logo del cliente. Es la pieza mas repetitiva del dia a dia.

## Antes de producir

Pedi si falta CUALQUIERA de estos datos. No completes con placeholders ni "USD ?":
1. **Cliente**.
2. **Direccion / barrio**.
3. **Precio** (USD o ARS, indicar moneda).
4. **m2** (totales y/o cubiertos segun como lo pase el cliente).
5. **Dormitorios, banos, cochera**.
6. **Foto de la propiedad** (url, path local, o aviso de "no tengo, generala").
7. **Formato**: cuadrado (feed) o vertical (story). Default cuadrado.

## Pasos

1. **Cargar brand** segun protocolo `context/brand_loader.md`. Extraer paleta, tipografias, layouts permitidos para placa.
2. Si la foto es de baja calidad o el cliente la marca como "mejorala", invoca skill `mejorar-foto` antes.
3. Layout: foto hero arriba o de fondo (segun brand), precio en jerarquia maxima (300-420px), 4 iconos con datos en grilla, direccion abajo, logo cliente en esquina.
4. Pipeline: Canva MCP si hay brand kit; si no, `templates/placa_propiedad.html` + `scripts/render.py`.
5. Renderiza a `output/<cliente>/<YYYY-MM-DD>/placa_propiedad/`. Naming: `placa_<direccion-corta>_<formato>.png`.
6. Revisa: legibilidad del precio a 2 segundos, iconos no se confunden, foto no esta cortada en partes criticas.
7. Mostra al usuario.
8. Iterar.
9. Subir a Drive con OK: `CLIENTE/03 Estaticos/Placas/`.

## Reglas no negociables

- NO inventes datos. Si falta, parar y pedir.
- Precio con moneda explicita ("USD 285.000" no "$285.000").
- Si el cliente tiene reglas de precio (ej: solo USD, o "consulta" en vez de precio), respetar el brand JSON.
- Sin gradientes en el fondo de precio. Plano siempre.
- Una sola tipografia para precio + datos (la del brand para titulares).

## Entrega

Mostra el PNG. Cierra: "Placa de [direccion] para [cliente] en `output/...`. Va asi o cambiamos algo?"
