---
name: testimonio-placa
description: Use this skill for social proof / prueba pieces — single placa or 2-3 slide carrusel that materializes the "PRUEBA" step of the DV method. Formats: testimonio textual de cliente (1080x1080 o 1080x1350), operacion cerrada (precio + dias + barrio), captura de WhatsApp con consentimiento, NPS / numero de operaciones. Triggers "placa de testimonio de [cliente]", "armame la prueba social de [caso]", "placa de operacion cerrada [direccion]", "testimonio para feed", "captura WhatsApp prueba social", "placa de caso de exito".
---

# Skill: Placa de testimonio / prueba social

Pieza que materializa el paso PRUEBA del Metodo DV. Es el cierre del funnel narrativo: dolor → consecuencia → solucion → **prueba**. Sin esta pieza, el resto del contenido es promesa sin respaldo.

## Tipos cubiertos

1. **Testimonio textual** — quote de cliente con nombre + foto (o silueta) + cargo/rol.
2. **Operacion cerrada** — direccion + precio cerrado + dias en mercado + barrio. Sin datos sensibles del cliente comprador/vendedor.
3. **Captura WhatsApp** — screenshot anonimizado de mensaje real (con consentimiento explicito).
4. **Numero hito** — "73 operaciones en 2025", "NPS 9.2", "USD 4.2M cerrados". Numero gigante.

## Antes de producir

1. **Cliente** (la inmobiliaria/agente que muestra la prueba).
2. **Tipo** de los 4 anteriores.
3. **Datos especificos** segun tipo:
   - Testimonio: quote textual literal (NO reescribir), nombre cliente, rol/contexto (ej: "compro depto en Belgrano").
   - Operacion: direccion (puede ser barrio si hay confidencialidad), precio cerrado, dias en mercado, mes/año.
   - WhatsApp: screenshot original + confirmacion de consentimiento del cliente.
   - Numero: la metrica + periodo + contexto.
4. **Consentimiento** — confirmar que el cliente autoriza usar su nombre/cara/quote. Si no hay confirmacion, ofrecer version anonimizada ("Cliente, Belgrano").

## Pasos

1. **Cargar brand** segun protocolo `context/brand_loader.md`. Extraer paleta, tipografias, regla `prueba_social.anonimizar` si existe.
2. Layout segun tipo:
   - **Testimonio textual**: quote en 60-80px con comillas tipograficas grandes (200px+ acento), nombre + rol abajo en 28-36px. Foto circular 200px (opcional).
   - **Operacion cerrada**: tag arriba "OPERACION CERRADA" / "VENDIDO". Direccion 60px. Precio gigante 280-380px en acento. Stats abajo (dias en mercado, barrio).
   - **WhatsApp**: screenshot recortado y anonimizado al centro, marco simple, tag arriba "MENSAJE REAL", logo cliente abajo.
   - **Numero hito**: numero gigante 380-480px ocupando 60% del area, label corta abajo (ej: "operaciones en 2025"), micro-tag arriba ("RESULTADOS").
3. Pipeline: HTML + Playwright. Crear template `templates/testimonio_placa.html` con 4 variantes (puede ser un template con `data-tipo` que renderea distinto via CSS).
4. Renderiza a `output/<cliente>/<YYYY-MM-DD>/testimonio/`. Naming: `testimonio_<tipo>_<id-corto>.png`.
5. Invocar skill `design-qa`.
6. Mostra al usuario.
7. Iterar.
8. Subir a Drive con OK: `CLIENTE/03 Estaticos/Pruebas Sociales/`.

## Reglas no negociables

- NO reescribas el quote textual. Va literal. Si tiene un error de ortografia gracioso, dejalo (suma autenticidad).
- NO inventes operaciones. Si falta el dato real, parar y pedir.
- NO uses fotos genericas de gente sonriendo (cliche stock). Si no hay foto del cliente, va silueta o sin foto.
- Anonimizar WhatsApp SIEMPRE (numero, foto perfil, datos sensibles tachados o reemplazados).
- Precio con moneda explicita.
- Si el cliente prohibe mostrar nombres reales en su brand JSON (`prueba_social.anonimizar = true`), forzar version anonimizada.

## Hook copy sugerido por tipo

- Testimonio: usar la frase mas punzante del quote como acento.
- Operacion cerrada: tag corto contundente ("VENDIDO EN 18 DIAS").
- WhatsApp: tag "MENSAJE REAL" o "ASI ESCRIBEN LOS CLIENTES".
- Numero: la metrica habla sola, tag explicativo corto.

## Entrega

Mostra el PNG. Cierra: "Testimonio [tipo] para [cliente] en `output/...`. Datos cruzados con [fuente]. Va asi o cambiamos?"
