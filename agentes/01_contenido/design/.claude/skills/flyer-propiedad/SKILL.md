---
name: flyer-propiedad
description: Use this skill when the user asks for an A4 property flyer — 2480x3508 at 300dpi, for printing or WhatsApp. Hero photo, title, location, price, 3-4 key data, contact, client logo. Triggers "flyer de [propiedad]", "flyer A4 para [cliente]", "armame un flyer", "flyer para imprimir de [propiedad]", "flyer para mandar por whatsapp".
---

# Skill: Flyer de lanzamiento de propiedad

Formato A4 vertical (2480x3508 a 300dpi). Pensado para imprimir o mandar por WhatsApp. Pieza mas detallada que la placa: jerarquia visual fuerte con foto hero, datos completos, contacto.

## Antes de producir

Pedi si falta:
1. **Cliente**.
2. **Datos de propiedad**: direccion, precio, m2 (totales y cubiertos si difieren), dormitorios, banos, cochera, ano de construccion si suma, amenities clave si suma.
3. **Foto principal** (hero) y opcionalmente 1-2 fotos secundarias.
4. **Contacto**: telefono y/o email del agente o inmobiliaria.
5. **Destino**: imprenta o WhatsApp/digital. Si es imprenta, confirmar 300dpi.

No completes ningun dato. Si falta uno critico, parar.

## Pasos

1. Carga brand: `shared/brands/<cliente>.json`.
2. Si fotos son de celular/calidad baja, invoca skill `mejorar-foto`.
3. Layout A4 vertical:
   - Tercio superior: foto hero + titulo + ubicacion.
   - Tercio medio: precio destacado + 3-4 datos clave en iconos.
   - Tercio inferior: amenities/extras si los hay + contacto + logo.
4. Pipeline: HTML + Playwright es preferible al Canva MCP para A4 a 300dpi (control de resolucion). `templates/flyer_propiedad.html` + `scripts/render.py` con `--dpi 300`.
5. Renderiza a `output/<cliente>/<YYYY-MM-DD>/flyer_propiedad/`. Naming: `flyer_<direccion-corta>.png` y `.pdf` si el cliente lo pide para imprenta.
6. Revisa: margenes seguros (no cortar texto en bordes de imprenta), texto legible a tamano impreso, logo no pixelado.
7. Mostra al usuario.
8. Iterar.
9. Subir a Drive con OK: `CLIENTE/03 Estaticos/Flyers/`.

## Reglas no negociables

- 300dpi obligatorio si el destino es imprenta.
- Margenes seguros minimo 80px (en pixeles a 300dpi).
- NO inventes amenities ni datos.
- Telefono con formato argentino claro: `+54 9 11 ...`.

## Entrega

Mostra el render (puede ser preview reducido en chat) y avisa donde esta el archivo full-res. "Flyer de [direccion] en `output/...`. Apto imprenta a 300dpi. Va asi?"
