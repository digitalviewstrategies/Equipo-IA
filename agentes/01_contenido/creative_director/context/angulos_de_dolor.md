# Cómo generar 5+ ángulos de dolor desde el buyer persona

Este es un paso obligatorio del proceso, no un "nice to have". Antes de proponer ideas, el agente genera mínimo 5 ángulos de dolor distintos a partir del buyer persona del cliente. Ese banco es la materia prima de toda la ideación posterior.

## Por qué 5+ ángulos y no uno solo

El documento de Core del cliente pide un dolor primario, un dolor secundario y un estado deseado. Eso es 1 ángulo. Un ángulo es una entrada al dolor core del buyer persona. Pero el mismo dolor se puede atacar desde entradas muy distintas, y cada entrada habilita hooks distintos, formatos distintos y emociones distintas.

**Ejemplo concreto**. Buyer persona: propietario de 50 años, depto de 3 ambientes en Núñez, lleva 5 meses publicado, bajó el precio dos veces, no entran visitas.

Un ángulo sería: "tu depto no se vende porque no lo ve la gente correcta." Ese es un ángulo. Pero el mismo dolor core (depto sin vender) tiene al menos estas entradas distintas:

1. **Costo acumulado de expensas e impuestos** → entrada económica fría, dato duro. Emoción: racional, ira leve. Formato: Beneficios, Identificación.
2. **Oportunidad perdida de comprar lo que quiere** → entrada de comparación con su propio estado deseado. Emoción: arrepentimiento, deseo frustrado. Formato: Aspiracional, Historia Personal.
3. **Vergüenza social / preguntas del entorno** → entrada social. "Los vecinos me preguntan por qué no lo vendo." Emoción: vergüenza, comparación. Formato: Culpa, Escena.
4. **Miedo a que el mercado siga bajando** → entrada de escasez / pérdida futura. Emoción: miedo, urgencia. Formato: Warning (variante de Identificación), Antes/Después.
5. **Frustración con la inmobiliaria actual** → entrada de traición / abandono. "Nunca me llaman, pago la comisión igual." Emoción: ira, desconfianza. Formato: Verdad incómoda (Educativo), Conflicto (Ranking).
6. **Cansancio emocional de mostrar el depto a curiosos** → entrada del proceso, no del resultado. Emoción: agotamiento, ganas de rendirse. Formato: Persona Mirror, Empatía.

Seis entradas. El mismo dolor core. Seis campañas potencialmente distintas. Seis videos que no compiten entre sí sino que cubren distintos momentos emocionales del mismo buyer persona.

## Las 6 familias de ángulos (usalas como checklist)

Cada ángulo que generás tiene que poder mapearse a una de estas familias. Si las 5 ideas que sacaste caen todas en la misma familia, no son 5 ángulos, son 1.

### 1. Económico / racional
El costo concreto del problema. Números. Pérdida medible. ¿Cuánto le cuesta al buyer persona no actuar, por mes, en plata real?
**Emociones que activa**: ira, urgencia, cálculo.
**Formatos que calzan**: Beneficios, Antes/Después con números, Conversión BOF.

### 2. Oportunidad perdida / comparación con uno mismo
Lo que el buyer persona podría estar haciendo con el problema resuelto y no está. No es dolor por lo que tiene, es dolor por lo que no tiene.
**Emociones que activa**: arrepentimiento, deseo frustrado, FOMO hacia uno mismo.
**Formatos que calzan**: Aspiracional, Historia Personal, Pantalla Dividida.

### 3. Social / vergüenza / comparación con otros
Lo que otros ya tienen, lo que otros ya saben, lo que otros están comentando. El buyer persona se siente atrás del resto.
**Emociones que activa**: vergüenza, comparación, FOMO social.
**Formatos que calzan**: Culpa, Escena, Ranking.

### 4. Miedo / pérdida futura
Lo que va a empeorar si no actúa. La proyección del costo que viene. El tren que se pasa.
**Emociones que activa**: miedo, urgencia, anticipación al dolor.
**Formatos que calzan**: Warning, Identificación, Antes/Después (en negativo).

### 5. Ira / traición / injusticia
Alguien ya le falló al buyer persona en este dolor. Una inmobiliaria, una experiencia previa, un consejo que le dieron y no funcionó. Hay un villano identificable.
**Emociones que activa**: ira, desconfianza, ganas de tener razón.
**Formatos que calzan**: Educativo contraintuitivo, Verdad incómoda, Ranking polémico, Historia Personal de error.

### 6. Cansancio / proceso / agotamiento
No es el resultado, es el esfuerzo diario de convivir con el problema. El desgaste emocional de "estar en esto". La fatiga acumulada.
**Emociones que activa**: agotamiento, ganas de rendirse, búsqueda de alivio.
**Formatos que calzan**: Persona Mirror, Culpa con normalización fuerte, Testimonial empático.

## Cómo generás los 5+ ángulos en la práctica

Paso a paso, cuando el agente llega al paso 4 del proceso.

### Paso 1: Leer bien el buyer persona
De `output_manager.load_brand(cliente)` sacás la info del buyer persona. Si el brand system no tiene buyer persona definido (a veces pasa en clientes viejos del agente de diseño), pedís esa info al usuario antes de seguir. No adivinás.

### Paso 2: Identificar el dolor core
Uno solo. No el dolor primario/secundario del sistema, sino el dolor de raíz del cual todos los otros emanan. Ejemplo: "mi depto no se vende", "no consigo clientes nuevos", "mi cartera de propiedades está estancada". Una oración.

### Paso 3: Generar una entrada por familia
Tomás cada una de las 6 familias y te preguntás: ¿cómo se expresaría este dolor core desde esta familia? Si una familia no aplica de forma natural al buyer persona (ej: si el perfil no es sensible a lo social, la familia 3 puede no dar), saltala y anotá por qué. Al final tenés entre 5 y 6 ángulos.

### Paso 4: Escribir cada ángulo con la ficha completa
Para cada ángulo, estos 5 campos:

- **Título del ángulo** (4-8 palabras, concreto). Ej: "Costo acumulado de expensas".
- **Frase en voz del buyer persona** (cómo lo diría él, no cómo lo describís vos). Ej: "Son 800 dólares por mes que me siguen volando y el depto sigue ahí."
- **Familia** (1 de las 6 de arriba).
- **Emoción dominante**.
- **Formato del sistema que mejor le calza** (1 o 2 de los 13).
- **Hook tentativo** (una línea, aplicando banco de hooks o una familia de hooks).

### Paso 5: Chequear que son distintos de verdad
Antes de entregar al usuario, revisás el banco y te hacés esta pregunta: "¿estos 5 ángulos habilitan 5 campañas distintas o son variantes del mismo video?". Si 3 caen en la misma familia, reemplazás uno. Si 2 tienen la misma emoción dominante y el mismo formato, reemplazás uno.

## Ejemplo de salida completa (para soldati_vista, captación de mandatos)

**Dolor core**: "mi depto no se vende hace meses y no sé por qué."

**Ángulo 1 — Costo acumulado de expensas**
- Frase: "Son 800 dólares por mes en expensas e impuestos que me siguen volando y el depto sigue ahí."
- Familia: económico / racional.
- Emoción: ira, urgencia, cálculo.
- Formato: Beneficios (variación B con dato en pantalla) o Culpa con escalada numérica.
- Hook: "Cada mes que tu depto sigue publicado son 800 dólares que te estás regalando."

**Ángulo 2 — Oportunidad perdida de comprar lo que querés**
- Frase: "Yo quería cambiar de barrio, pero hasta que no venda esto no me puedo mover."
- Familia: oportunidad perdida.
- Emoción: arrepentimiento, deseo frustrado.
- Formato: Aspiracional o Historia Personal.
- Hook: "Tenés el próximo depto elegido. Y hace 5 meses que no te podés mover."

**Ángulo 3 — Vergüenza social de los que ya lo notaron**
- Frase: "Ya los vecinos me preguntan cuándo lo vendo. Me da un poco de vergüenza."
- Familia: social / vergüenza.
- Emoción: vergüenza, comparación con el entorno.
- Formato: Culpa con normalización fuerte, o Escena (el vecino que pregunta).
- Hook: "¿Cuántas veces esta semana alguien te preguntó si al fin vendiste?"

**Ángulo 4 — Miedo a que el mercado siga bajando**
- Frase: "Si bajo más, pierdo. Si no bajo, no entra nadie. No sé qué hacer."
- Familia: miedo / pérdida futura.
- Emoción: miedo, parálisis, urgencia.
- Formato: Identificación (variación B - warning) o Educativo contraintuitivo.
- Hook: "Bajar el precio no acelera la venta. La mayoría de las veces la mata."

**Ángulo 5 — Traición de la inmobiliaria actual**
- Frase: "La inmobiliaria no me llama nunca. Cada tanto me mandan un mensaje genérico."
- Familia: ira / traición.
- Emoción: ira, desconfianza.
- Formato: Verdad incómoda (Educativo) o Ranking polémico de "formas de vender".
- Hook: "Tu inmobiliaria cobra igual si vende en 30 días o en 8 meses. Adiviná qué le conviene."

**Ángulo 6 — Cansancio de mostrar el depto a curiosos**
- Frase: "Ya no quiero ordenar el depto un sábado más para que vengan a ver y no compren."
- Familia: cansancio / proceso.
- Emoción: agotamiento, ganas de rendirse.
- Formato: Persona Mirror o Testimonial empático (cliente que contó esto).
- Hook: "Si ya no tenés ganas de ordenar el depto un sábado más para curiosos que no compran, te entiendo."

Con este banco, el agente propone las 3 ideas del paso 6 eligiendo 3 de los 6 ángulos, y justifica por qué esos 3 y no los otros. Los que sobran quedan en reserva para la siguiente tanda de contenido o para la estrategia mensual.

## Qué NO es un ángulo de dolor

- No es un formato. "Testimonial del cliente que vendió" no es un ángulo, es un formato que podés usar desde varios ángulos.
- No es un hook. Un hook es la expresión literal de un ángulo, no el ángulo mismo.
- No es un beneficio. "Vendé rápido" no es un ángulo de dolor, es la promesa del servicio.
- No es un dato. "73% de las inmobiliarias viven del boca en boca" es un dato duro que puede apoyar un ángulo (ej: traición de la inmobiliaria actual), pero el dato por sí solo no es el ángulo.

Un ángulo de dolor es una manera específica en que el buyer persona siente el dolor core, con su propia voz y su propia emoción dominante.
