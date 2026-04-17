# Audiencias para Real Estate Argentino — DV

## Segmentos pre-armados

Estos son los segmentos base que DV usa para campanas inmobiliarias. Se personalizan por cliente usando el buyer persona de su brand system.

---

### 1. Compradores CABA

**Quien es:** persona buscando comprar departamento o casa en Capital Federal.

| Campo | Valor |
|---|---|
| Geo | Buenos Aires, Argentina (radio 25km del centro) |
| Edad | 28-55 |
| Genero | Todos |
| Intereses | Real estate, Property investment, Apartment, Moving, Home buying, Inmobiliaria, Propiedad, ZonaProp, Argenprop, Mercado Libre Inmuebles |
| Excluir | Intereses en alquiler temporal, Airbnb hosting |

**Variantes:**

- **Premium CABA**: agregar intereses en luxury brands, business news, viajes internacionales. Filtra por propiedades USD 150k+.
- **Inversor CABA**: agregar intereses en investment, finance, rental income, passive income.

---

### 2. Compradores Zona Norte

**Quien es:** persona buscando comprar en el corredor Vicente Lopez - San Fernando.

| Campo | Valor |
|---|---|
| Geo | Vicente Lopez, Olivos, San Isidro, Acassuso, Beccar, Martinez, San Fernando (radio por municipio) |
| Edad | 30-55 |
| Genero | Todos |
| Intereses | Real estate, Casa, Country, Barrio privado, Mudanza, Home improvement + los de CABA |
| Excluir | Intereses en alquiler temporal |

**Variantes:**

- **Familia ZN**: agregar intereses en family, parenting, schools, kids activities. Para casas/countries.
- **Downsize ZN**: edad 50-65, intereses en retirement, simplificar, departamento chico.

---

### 3. Inversores inmobiliarios

**Quien es:** persona que busca rentabilidad via real estate (pozo, renta, flipping).

| Campo | Valor |
|---|---|
| Geo | CABA + Zona Norte (o segun proyecto) |
| Edad | 30-60 |
| Genero | Todos |
| Intereses | Investment, Real estate investing, Financial planning, Passive income, Rental property, Fideicomiso, Pozo, Construccion |
| Comportamientos | Engaged shoppers, Business page admins |

---

### 4. Vendedores (captacion)

**Quien es:** propietario que quiere vender su propiedad. Es el segmento mas dificil de targetear.

| Campo | Valor |
|---|---|
| Geo | Segun zona del cliente |
| Edad | 35-65 |
| Genero | Todos |
| Intereses | Home selling, Real estate agent, Property valuation, Home improvement, Moving, Mudanza |
| Comportamientos | Homeowners (si disponible en AR), Recently moved |

**Nota:** la captacion suele funcionar mejor con retargeting y contenido educativo ("como vender tu propiedad al mejor precio") que con cold targeting.

---

### 5. Lookalike audiences

Construidas a partir de listas de leads del cliente.

| Fuente | Lookalike | Uso |
|---|---|---|
| Lista de leads (email + tel) | 1% lookalike | Audiencia principal de prospeccion |
| Leads calificados (los que respondieron) | 1% lookalike | Audiencia premium |
| Clientes cerrados | 1-2% lookalike | Si hay volumen suficiente (min 100 contactos) |

**Requisitos:**

- Minimo 100 contactos en la lista fuente.
- Actualizar la lista cada 30 dias.
- No usar listas de mas de 6 meses sin actualizar.

---

### 6. Retargeting

| Audiencia | Ventana | Uso |
|---|---|---|
| IG engagers (todos) | 90 dias | Retargeting amplio |
| IG engagers (perfil visitado) | 30 dias | Retargeting caliente |
| Video viewers (75%+) | 30 dias | Vieron contenido completo, alta intencion |
| Video viewers (25%+) | 60 dias | Hook los atrapo pero no completaron |
| Website visitors | 30 dias | Si hay pixel instalado |
| Lead form openers (no enviaron) | 30 dias | Abandonaron el formulario |

**Reglas de retargeting:**

- Siempre excluir leads ya generados (custom audience de leads existentes).
- Retargeting funciona mejor con creativos distintos a los de prospeccion (testimonio, caso de exito, oferta directa).
- No retargetear con el mismo creativo que ya vieron.

---

## Personalizacion por cliente

Para cada cliente nuevo:

1. Leer el buyer persona del brand system (`shared/brands/[cliente].json`).
2. Elegir 1-2 segmentos base de esta guia.
3. Ajustar intereses y geo segun el tipo de propiedades y zona del cliente.
4. Si el cliente tiene lista de leads: crear lookalike.
5. Si el cliente tiene Instagram activo: crear retargeting de IG engagers.

---

## Exclusiones estandar

Aplicar en todos los ad sets:

- Custom audience de leads existentes del cliente (para no gastar en gente que ya contacto).
- Empleados del cliente (si hay lista).
- Competidores directos (si se pueden identificar).

---

## Restricciones HOUSING

Con la categoria HOUSING activada, algunas opciones de targeting pueden estar limitadas:

- En Argentina, las restricciones son menores que en USA/EU.
- Si una opcion de targeting no esta disponible, usar la alternativa mas cercana.
- Documentar cualquier restriccion encontrada para referencia futura.
