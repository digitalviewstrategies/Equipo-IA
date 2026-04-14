# Framework de Copy — Método DV

## El principio base

Cada pieza de contenido tiene una sola audiencia, un solo problema, y un solo objetivo. Si intentás hablarle a todos, no le hablás a nadie. Si intentás decir todo, no decís nada.

Antes de escribir cualquier cosa, respondé estas tres preguntas:
1. ¿A quién específicamente le hablo? (No "propietarios". "Propietario hombre 50 años Palermo que tiene el depto publicado en ZonaProp hace 4 meses y no cierra nada.")
2. ¿Qué problema exacto tiene esta persona ahora mismo?
3. ¿Qué quiero que haga después de ver esto?

## Estructuras narrativas

### DOLOR → CONSECUENCIA → SOLUCIÓN → PRUEBA
Para captación y conversión. Funciona porque sigue el proceso mental real del cliente antes de comprar.

- **Dolor:** el problema que tiene, dicho sin rodeos. No el problema que cree que tiene, el real.
- **Consecuencia:** qué pasa si no lo resuelve. Hacelo tangible, no abstracto.
- **Solución:** lo que hace el cliente de DV para resolverlo. Específico, no genérico.
- **Prueba:** número, testimonio, caso real, resultado concreto.

Ejemplo aplicado (captación de mandatos):
- Dolor: "Publicaste el depto, pusiste el precio que querías, y no cierra nadie."
- Consecuencia: "Cada mes que pasa el mercado te dice que valía menos. Y vos bajás el precio."
- Solución: "Nosotros arrancamos con la tasación real y el plan de comunicación antes de publicar."
- Prueba: "42 días promedio para cerrar en nuestra cartera. El mercado tarda 180."

### HOOK → PROBLEMA → TIPS → CIERRE
Para contenido educativo. Construye autoridad.

- **Hook:** interrumpe el scroll. Dato raro, afirmación que confronta, pregunta que genera tensión.
- **Problema:** expandís el problema que plantea el hook. Mostrás que entendés bien de qué se trata.
- **Tips:** valor real. No "buscá asesoramiento profesional". Cosas concretas que la persona puede usar.
- **Cierre:** CTA o posicionamiento. Sin mendigar seguimiento.

### HISTORIA → TENSIÓN → RESOLUCIÓN → MORALEJA
Para marca personal y storytelling.

- **Historia:** situación real o verosímil. Contexto mínimo, no más de dos líneas.
- **Tensión:** el momento donde algo podría salir mal. Acá es donde la gente deja de scrollear.
- **Resolución:** cómo se resolvió. Honesto, no perfecto. Las resoluciones demasiado perfectas no se creen.
- **Moraleja:** el aprendizaje que deja para la audiencia.

## Sistema de hooks

El hook es la primera línea. Si la primera línea no para el scroll, el resto no importa.

### Tipo 1: Negación
Contradecís algo que el target cree que es verdad o que hace habitualmente.

Fórmula: "[Cosa que creen que funciona] no [resultado que esperan]."

Ejemplos:
- "Las fotos profesionales del depto no venden un carajo si no tenés distribución."
- "Más propiedades en cartera no significa más ingresos."
- "El boca en boca no escala."

### Tipo 2: Empatía
Nombrás una situación específica que el target vivió. Que sienta que lo estás mirando.

Fórmula: "Si alguna vez [situación específica], lo que sigue es para vos."

Ejemplos:
- "Si cerraste una operación y sentiste que podrías haber pedido más, seguí."
- "Si tenés el depto publicado hace más de 60 días y no cerró, no es el mercado."
- "Si trabajás solo y sentís que el volumen no escala, el problema no es el esfuerzo."

### Tipo 3: Verdad incómoda
Un dato o afirmación que incomoda porque es real y la audiencia lo sabe pero no lo dice.

Fórmula: "[Número o afirmación dura] + contexto que lo hace más incómodo."

Ejemplos:
- "73% de las inmobiliarias argentinas todavía vive del boca en boca. En 2026."
- "La mayoría de los brokers gana lo mismo hace tres años aunque cierra más operaciones."
- "Tu competidor con peor cartera que vos vende más porque tiene mejor presencia digital."

## Reglas de tono DV

### Lo que siempre aplica
- Voseo. Siempre. Sin excepción.
- Frases cortas. Máximo 15 palabras por frase en contenido de redes.
- Sin adjetivos vacíos: "exclusivo", "premium", "de calidad", "único". Si no lo podés demostrar, no lo decís.
- Los datos van sin fuente si son internos de DV, con fuente si son externos.
- Humor negro cuando suma, no como relleno.

### Lo que nunca aplica
- "Tu hogar ideal" — cliché total.
- "Invertí en tu futuro" — genérico y vacío.
- "Propiedades de alta gama" — cualquier inmobiliaria lo dice.
- "Calidad de vida" — no significa nada.
- "Estamos para ayudarte" — suena a call center.
- "¿Querés comprar/vender/alquilar?" — pregunta demasiado obvia, no interrumpe.
- Tres signos de exclamación seguidos. Nunca.

### Calibración por cliente (escala 1-6)

Ver `../CLAUDE.md` para la escala completa.

**Señales en el brand system que indican nivel de disrupción:**
- Logo con serif o colores sobrios → 1-2
- Años en el mercado como diferencial → 1-3
- Broker joven, foto en ropa casual → 3-5
- Humor en el Instagram actual → 4-5
- Sin Instagram o con fotos solo de propiedades → evaluar por contexto del cliente

## Estructura de carrusel slide por slide

### Carrusel de captación (6 slides)

| Slide | Función | Elemento protagonista | Copy |
|-------|---------|----------------------|------|
| 1 | Hook | Afirmación disruptiva o dato duro | 1 frase, máximo 8 palabras |
| 2 | Dolor | El problema real del target | 2-3 líneas, específico |
| 3 | Consecuencia | Qué pasa si no actúa | Dato o imagen mental poderosa |
| 4 | Solución | Lo que hace el cliente de DV | Específico, no genérico |
| 5 | Prueba | Números, resultados, testimonios | Datos concretos en formato visual |
| 6 | CTA | Llamada a la acción | Directo, sin rodeos |

### Carrusel educativo (6 slides)

| Slide | Función | Elemento protagonista | Copy |
|-------|---------|----------------------|------|
| 1 | Hook | Pregunta o afirmación que confronta | Máximo 10 palabras |
| 2 | Problema | El problema que vas a resolver | Contexto breve |
| 3-5 | Tips | 1 tip por slide, con título | Práctico y accionable |
| 6 | Cierre | Posicionamiento o CTA suave | Sin mendigar |

## Briefing para el agente de diseño

Cuando generás un brief de carrusel para pasarle al `dv_design_agent`, el formato es:

```markdown
# Brief Carrusel — [Nombre del cliente] — [Título del carrusel]

## Objetivo
[Qué acción querés que tome quien lo lee]

## Audiencia específica
[Descripción precisa, no genérica]

## Tono
Nivel [N] en escala DV — [descripción breve]

## Estructura slide por slide

### Slide 1 — Hook
Headline: [copy exacto]
Elemento visual protagonista: [qué debe destacarse visualmente]
Fondo recomendado: [según paleta del brand system]

### Slide 2 — [función]
Headline: [copy]
Cuerpo: [copy si aplica]
Elemento visual: [descripción]

[...continúa por cada slide]

## Notas visuales adicionales
[Cualquier cosa específica que el agente de diseño necesita saber]
```
