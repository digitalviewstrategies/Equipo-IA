# Guia de Presupuestos — DV Meta Ads

## Presupuesto minimo

- **Por ad set:** USD 5/dia. Menos que esto no genera data suficiente.
- **Por campana (minimo viable):** USD 10/dia (2 ad sets x USD 5).
- **Recomendado por campana:** USD 15-25/dia (3 ad sets con margen).
- **Presupuesto mensual minimo del cliente:** USD 300/mes de pauta (requisito DV).

---

## Distribucion de presupuesto

### Split prospeccion vs testing

| Tipo | % del presupuesto | Descripcion |
|---|---|---|
| **Proven** | 70% | Audiencias que ya generaron leads. Budget estable o en scale. |
| **Testing** | 30% | Audiencias nuevas, creativos nuevos, angulos nuevos. |

### Split por ad set (ejemplo con USD 20/dia)

```
Campana: ClienteX_Leads_2026-04 — USD 20/dia total

Ad Set 1: CompradoresCABA (proven)    — USD 8/dia (40%)
Ad Set 2: RetargetingIG (proven)      — USD 6/dia (30%)
Ad Set 3: LookalikeLeads (testing)    — USD 6/dia (30%)
```

---

## Reglas de scaling

### Subir presupuesto

- **Maximo:** +20% cada 3 dias en ad sets con status SCALE.
- **Nunca** duplicar presupuesto de golpe. Meta penaliza saltos bruscos con CPL alto temporal.
- **Secuencia ejemplo:** USD 5 → USD 6 → USD 7.20 → USD 8.60 → USD 10.30

### Bajar presupuesto

- Si un ad set esta en KILL, pausarlo directamente (no bajar budget gradualmente).
- Si un ad set esta en ITERATE, mantener el budget actual mientras se preparan variantes.

### Redistribuir

Cuando se pausa un ad set, redistribuir su presupuesto:

1. Primero a ad sets en SCALE (proporcionalmente).
2. Si no hay ad sets en SCALE, a ad sets en HOLD (para acelerar data).
3. No crear ad sets nuevos con budget redistribuido sin creativos listos.

---

## Presupuesto a nivel campana vs ad set

**Default DV: presupuesto a nivel de ad set (ABO — Ad Set Budget Optimization).**

Razones:

- Control granular de cuanto gasta cada audiencia.
- Evita que Meta concentre todo el gasto en un solo ad set.
- Permite escalar y pausar ad sets individualmente.

**Cuando usar CBO (Campaign Budget Optimization):**

- Solo si Felipe lo indica explicitamente.
- Util cuando hay 4+ ad sets similares y se quiere que Meta optimice distribucion.
- Requiere que todos los ad sets tengan el mismo objetivo y metricas comparables.

---

## Planning mensual

### Template de planificacion

Para cada cliente, al inicio del mes:

```
Cliente: [nombre]
Presupuesto mensual: USD [X]
Presupuesto diario promedio: USD [X/30]

Campanas activas:
1. [nombre] — USD [Y]/dia — objetivo: [leads/traffic]

Distribucion:
- Prospeccion: USD [70% de X] — [N] ad sets
- Testing: USD [30% de X] — [N] ad sets
- Retargeting: incluido en prospeccion o separado segun volumen

Meta del mes:
- Leads esperados: [presupuesto / CPL target]
- CPL target: USD [X]
```

### Ajustes mid-month

- Semana 1: lanzar y observar. No tocar nada los primeros 3 dias.
- Semana 2: primera ronda de optimizacion (SCALE/KILL/ITERATE).
- Semana 3: segunda ronda + pedido de creativos nuevos si hay fatiga.
- Semana 4: consolidar ganadores, preparar plan del mes siguiente.

---

## Regla de oro

**Nunca cambiar el presupuesto de una campana sin avisar a Felipe primero.** El presupuesto afecta la facturacion del cliente y las expectativas de resultados. Siempre informar antes de ejecutar.
