---
name: reel-cover
description: Use this skill when the user asks for a Reel cover / portada de reel — pieza estatica 1080x1350 (formato cover IG feed 4:5) que define como aparece el reel en el grid de Instagram. Hook gigante ocupando 50%+ del area, sin foto de la propiedad (eso es el video), enfoque en titular punzante. Triggers "portada del reel [tema]", "reel cover para [cliente]", "cover del reel sobre [X]", "tapa del reel", "thumbnail de reel".
---

# Skill: Portada de Reel (1080x1350)

Pieza estatica que actua como tapa del reel en el grid de feed de Instagram. NO es la pieza completa del video — es la primera frame visible cuando el reel esta inactivo. Define si alguien clickea o sigue scrolleando.

## Por que importa

El grid de IG es 4:5. Si la portada no engancha en el grid, el reel no se reproduce. La portada es el hook visual + titular antes del hook hablado del video.

## Antes de producir

1. **Cliente**.
2. **Tema/angulo del reel** (ej: "operaciones compartidas", "captacion en zona norte").
3. **Hook escrito** — el titular que va en la portada. Si no esta, escribilo usando uno de los `tone_of_voice.hook_frameworks` del brand JSON (si el brand no los define, fallback a Hormozi: negacion / empatia / verdad incomoda). Maximo 8 palabras.
4. **Quien aparece en el reel** (Valen, Nico, cliente, voz en off). Define si va foto o solo tipografia.

Si falta hook, lo escribis vos pero confirmas con usuario antes de renderizar.

## Pasos

1. **Cargar brand** segun protocolo `context/brand_loader.md`. Extraer paleta, tipografias, hook_frameworks, forbidden_words.
2. Definir layout segun si hay foto o no:
   - **Solo tipografia** (default DV): hook gigante centrado, fondo color brand, acento subrayando 1-2 palabras clave, micro-tag arriba ("REEL" / "CAPTACION" / "CASO REAL"), logo abajo derecha chico.
   - **Con foto** (si hay frame del reel disponible): foto al 60-70% como background con overlay oscuro 40%, hook arriba o abajo, acento en palabra clave.
3. Layout fijo: formato 1080x1350. Margen 80px. Hook ocupa 50-70% del area (jerarquia brutal). Tamaño hook: 110-160px segun cantidad de palabras.
4. Pipeline: HTML + Playwright. Crear template `templates/reel_cover.html` si no existe, basado en estructura de `creativo_meta.html` adaptada a 1080x1350.
5. Renderiza a `output/<cliente>/<YYYY-MM-DD>/reel_cover/`. Naming: `reel_cover_<tema-corto>.png`.
6. Invocar skill `design-qa` antes de mostrar.
7. Mostra al usuario.
8. Iterar.
9. Subir a Drive con OK: `CLIENTE/03 Estaticos/Reel Covers/`.

## Reglas no negociables

- Hook MAXIMO 8 palabras. Si pasa de 8, reescribir.
- 1 sola tipografia para el hook. Peso 800/900.
- Subrayado/highlight en MAXIMO 2 palabras clave del hook (acento brand).
- NO poner CTA tipo "miralo" — la portada es el hook, el CTA va en el video.
- NO logo gigante. El logo va chico abajo, no compite con el hook.
- NO emojis.
- NO foto sin overlay si la foto tiene mucho detalle (el texto se pierde).

## Diferencia con creativo Meta vertical

`meta-ad-creativo` vertical es 1080x1920 con CTA + zona segura UI Stories. `reel-cover` es 1080x1350 sin zona segura porque vive en el feed grid, no en stories.

## Entrega

Mostra el PNG. Cierra: "Reel cover [tema] para [cliente] en `output/...`. Hook: '[hook]'. Va asi o cambiamos?"
