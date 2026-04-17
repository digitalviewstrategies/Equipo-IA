"""
report_generator.py — Genera reportes semanales y mensuales de performance
en formato markdown.
"""

from datetime import date

from campaign_analyzer import AdAnalysis, Benchmarks, DEFAULT_BENCHMARKS


def _metrics_table(analyses: list[AdAnalysis]) -> str:
    """Genera tabla markdown con metricas de todos los ads."""
    lines = [
        "| Ad | CPL | CTR | Hook Rate | Impresiones | Gasto | Leads | Clasificacion |",
        "|----|-----|-----|-----------|-------------|-------|-------|---------------|",
    ]
    for a in sorted(analyses, key=lambda x: x.score, reverse=True):
        m = a.metrics
        cpl = f"USD {m['cpl']:.2f}" if m.get("cpl") else "N/A"
        hr = f"{m['hook_rate']:.1f}%" if m.get("hook_rate") is not None else "N/A"
        lines.append(
            f"| {a.ad_name} | {cpl} | {m.get('ctr', 0):.2f}% | {hr} "
            f"| {m.get('impressions', 0):,} | USD {m.get('spend', 0):.2f} "
            f"| {m.get('leads', 0)} | {a.classification} |"
        )
    return "\n".join(lines)


def _classification_summary(analyses: list[AdAnalysis]) -> str:
    """Resumen por clasificacion."""
    counts = {"SCALE": 0, "KILL": 0, "ITERATE": 0, "HOLD": 0}
    for a in analyses:
        counts[a.classification] = counts.get(a.classification, 0) + 1

    lines = []
    for cls, count in counts.items():
        if count > 0:
            ads = [a.ad_name for a in analyses if a.classification == cls]
            lines.append(f"- **{cls}** ({count}): {', '.join(ads)}")
    return "\n".join(lines)


def generate_weekly_report(
    cliente: str,
    date_start: str,
    date_end: str,
    total_spend: float,
    total_leads: int,
    avg_cpl: float,
    total_impressions: int,
    total_reach: int,
    analyses: list[AdAnalysis],
    recommendations: list[str],
    next_actions: list[str],
    benchmarks: Benchmarks | None = None,
) -> str:
    """Genera reporte semanal en markdown."""
    b = benchmarks or DEFAULT_BENCHMARKS
    today = date.today().isoformat()

    # Evaluar CPL vs target
    cpl_status = "OK" if avg_cpl <= b.cpl_target else "ALERTA"
    if total_leads == 0:
        cpl_status = "SIN LEADS"

    lines = [
        f"# Reporte Semanal — {cliente}",
        f"**Periodo:** {date_start} a {date_end}",
        f"**Generado:** {today}",
        "",
        "---",
        "",
        "## Resumen ejecutivo",
        "",
        f"| Metrica | Valor | Status |",
        f"|---------|-------|--------|",
        f"| Gasto total | USD {total_spend:.2f} | - |",
        f"| Leads | {total_leads} | - |",
        f"| CPL promedio | USD {avg_cpl:.2f} | {cpl_status} (target: USD {b.cpl_target}) |",
        f"| Impresiones | {total_impressions:,} | - |",
        f"| Alcance | {total_reach:,} | - |",
        "",
        "---",
        "",
        "## Performance por creativo",
        "",
        _metrics_table(analyses),
        "",
        "---",
        "",
        "## Clasificacion",
        "",
        _classification_summary(analyses),
        "",
        "---",
        "",
        "## Top 3 creativos",
        "",
    ]

    top3 = sorted(analyses, key=lambda a: a.score, reverse=True)[:3]
    for i, a in enumerate(top3, 1):
        m = a.metrics
        cpl = f"USD {m['cpl']:.2f}" if m.get("cpl") else "N/A"
        lines.append(f"{i}. **{a.ad_name}** — CPL {cpl}, Score {a.score:.1f}")

    lines.extend([
        "",
        "## Bottom 3 creativos",
        "",
    ])

    bottom3 = sorted(analyses, key=lambda a: a.score)[:3]
    for i, a in enumerate(bottom3, 1):
        m = a.metrics
        cpl = f"USD {m['cpl']:.2f}" if m.get("cpl") else "N/A"
        lines.append(f"{i}. **{a.ad_name}** — CPL {cpl}, Score {a.score:.1f}. {a.reason}")

    lines.extend([
        "",
        "---",
        "",
        "## Recomendaciones",
        "",
    ])
    for rec in recommendations:
        lines.append(f"- {rec}")

    lines.extend([
        "",
        "## Proximas acciones",
        "",
    ])
    for action in next_actions:
        lines.append(f"- [ ] {action}")

    lines.append("")
    return "\n".join(lines)


def generate_monthly_report(
    cliente: str,
    month: str,
    total_spend: float,
    total_leads: int,
    avg_cpl: float,
    total_impressions: int,
    total_reach: int,
    budget_planned: float,
    analyses: list[AdAnalysis],
    weekly_trends: list[dict],
    recommendations: list[str],
    next_month_plan: list[str],
    benchmarks: Benchmarks | None = None,
) -> str:
    """Genera reporte mensual en markdown."""
    b = benchmarks or DEFAULT_BENCHMARKS
    today = date.today().isoformat()

    budget_used_pct = (total_spend / budget_planned * 100) if budget_planned > 0 else 0
    cpl_vs_target = ((avg_cpl / b.cpl_target - 1) * 100) if b.cpl_target > 0 else 0

    lines = [
        f"# Reporte Mensual — {cliente}",
        f"**Mes:** {month}",
        f"**Generado:** {today}",
        "",
        "---",
        "",
        "## Resumen del mes",
        "",
        "| Metrica | Valor | vs Target |",
        "|---------|-------|-----------|",
        f"| Gasto total | USD {total_spend:.2f} | {budget_used_pct:.0f}% del presupuesto (USD {budget_planned:.2f}) |",
        f"| Leads totales | {total_leads} | - |",
        f"| CPL promedio | USD {avg_cpl:.2f} | {'+' if cpl_vs_target > 0 else ''}{cpl_vs_target:.0f}% vs target (USD {b.cpl_target}) |",
        f"| Impresiones | {total_impressions:,} | - |",
        f"| Alcance | {total_reach:,} | - |",
        "",
        "---",
        "",
        "## Tendencia semanal",
        "",
        "| Semana | Gasto | Leads | CPL |",
        "|--------|-------|-------|-----|",
    ]

    for week in weekly_trends:
        lines.append(
            f"| {week.get('week', '-')} | USD {week.get('spend', 0):.2f} "
            f"| {week.get('leads', 0)} | USD {week.get('cpl', 0):.2f} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## Performance por creativo (mes completo)",
        "",
        _metrics_table(analyses),
        "",
        "---",
        "",
        "## Clasificacion final del mes",
        "",
        _classification_summary(analyses),
        "",
        "---",
        "",
        "## Recomendaciones",
        "",
    ])
    for rec in recommendations:
        lines.append(f"- {rec}")

    lines.extend([
        "",
        "## Plan para el mes siguiente",
        "",
    ])
    for item in next_month_plan:
        lines.append(f"- [ ] {item}")

    lines.append("")
    return "\n".join(lines)
