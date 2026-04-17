"""
brief_generator.py — Genera briefs estructurados para Creative Director y Design
basados en data de performance de campanas.

El brief creativo es el documento central del feedback loop entre Media Buyer
y Creative Director. Siempre incluye datos concretos, nunca opiniones vagas.
"""

from datetime import date

from campaign_analyzer import AdAnalysis


def generate_creative_brief(
    cliente: str,
    campaign_objective: str,
    date_start: str,
    date_end: str,
    total_spend: float,
    total_leads: int,
    avg_cpl: float,
    analyses: list[AdAnalysis],
    creatives_needed: int,
    formats_needed: list[str],
    angles_to_try: list[str],
    angles_to_avoid: list[str],
    buyer_persona_insights: list[str],
) -> str:
    """
    Genera un brief creativo en markdown para Creative Director.

    Returns:
        String con el brief completo listo para guardar.
    """
    today = date.today().isoformat()

    scale = [a for a in analyses if a.classification == "SCALE"]
    kill = [a for a in analyses if a.classification == "KILL"]
    iterate = [a for a in analyses if a.classification == "ITERATE"]

    lines = [
        f"# Brief Creativo — {cliente} — {today}",
        "",
        "## Contexto de campana",
        f"- Objetivo: {campaign_objective}",
        f"- Periodo analizado: {date_start} a {date_end}",
        f"- Presupuesto del periodo: USD {total_spend:.2f}",
        f"- Leads generados: {total_leads}",
        f"- CPL promedio: USD {avg_cpl:.2f}",
        "",
    ]

    # Ganadores
    if scale:
        lines.append("## Creativos ganadores (SCALE)")
        lines.append("")
        lines.append("| Creativo | CPL | CTR | Hook Rate | Impresiones | Score |")
        lines.append("|----------|-----|-----|-----------|-------------|-------|")
        for a in scale:
            m = a.metrics
            cpl = f"USD {m['cpl']:.2f}" if m.get("cpl") else "N/A"
            hr = f"{m['hook_rate']:.1f}%" if m.get("hook_rate") is not None else "N/A"
            lines.append(
                f"| {a.ad_name} | {cpl} | {m.get('ctr', 0):.2f}% | {hr} "
                f"| {m.get('impressions', 0):,} | {a.score:.1f} |"
            )
        lines.append("")
        lines.append("**Que funciono:**")
        for a in scale:
            lines.append(f"- {a.ad_name}: {a.reason}")
        lines.append("")

    # Perdedores
    if kill:
        lines.append("## Creativos perdedores (KILL)")
        lines.append("")
        lines.append("| Creativo | CPL | CTR | Hook Rate | Impresiones | Score |")
        lines.append("|----------|-----|-----|-----------|-------------|-------|")
        for a in kill:
            m = a.metrics
            cpl = f"USD {m['cpl']:.2f}" if m.get("cpl") else "N/A"
            hr = f"{m['hook_rate']:.1f}%" if m.get("hook_rate") is not None else "N/A"
            lines.append(
                f"| {a.ad_name} | {cpl} | {m.get('ctr', 0):.2f}% | {hr} "
                f"| {m.get('impressions', 0):,} | {a.score:.1f} |"
            )
        lines.append("")
        lines.append("**Que no funciono:**")
        for a in kill:
            lines.append(f"- {a.ad_name}: {a.reason}")
        lines.append("")

    # Iteracion
    if iterate:
        lines.append("## Creativos en iteracion (ITERATE)")
        lines.append("")
        lines.append("| Creativo | Problema detectado | Sugerencia |")
        lines.append("|----------|--------------------|------------|")
        for a in iterate:
            lines.append(f"| {a.ad_name} | {a.reason} | {a.recommendation} |")
        lines.append("")

    # Pedido
    lines.append("## Lo que necesito")
    lines.append(f"- {creatives_needed} creativos nuevos para: {', '.join(formats_needed)}")
    lines.append("- Angulos sugeridos basados en data:")
    for i, angle in enumerate(angles_to_try, 1):
        lines.append(f"  {i}. {angle}")
    if angles_to_avoid:
        lines.append(f"- Evitar: {', '.join(angles_to_avoid)}")
    lines.append("")

    # Insights del buyer persona
    if buyer_persona_insights:
        lines.append("## Insights del buyer persona (actualizados por performance)")
        for insight in buyer_persona_insights:
            lines.append(f"- {insight}")
        lines.append("")

    return "\n".join(lines)


def generate_design_brief(
    cliente: str,
    pieces_needed: int,
    format_type: str,
    sizes: list[str],
    piece_type: str,
    best_visual_format: str,
    best_visual_metrics: str,
    text_vs_clean: str,
    copy_source_path: str,
    inline_copy: dict | None = None,
    production_notes: list[str] | None = None,
) -> str:
    """
    Genera un brief de diseno en markdown para el agente de Design.

    Returns:
        String con el brief completo listo para guardar.
    """
    today = date.today().isoformat()

    lines = [
        f"# Brief Diseno — {cliente} — {today}",
        "",
        "## Piezas necesarias",
        f"- {pieces_needed} creativos Meta Ads formato {format_type}",
        f"- Tamano: {', '.join(sizes)}",
        f"- Tipo: {piece_type}",
        "",
        "## Referencia de performance",
        f"- Mejor formato visual reciente: {best_visual_format} ({best_visual_metrics})",
        f"- Texto overlay vs imagen limpia: {text_vs_clean}",
        "",
    ]

    if inline_copy:
        lines.append("## Copy")
        if inline_copy.get("headline"):
            lines.append(f"- Headline: {inline_copy['headline']}")
        if inline_copy.get("body"):
            lines.append(f"- Body: {inline_copy['body']}")
        if inline_copy.get("cta"):
            lines.append(f"- CTA: {inline_copy['cta']}")
        lines.append("")
    else:
        lines.append("## Copy/guion a usar")
        lines.append(f"- Ver: `{copy_source_path}`")
        lines.append("")

    if production_notes:
        lines.append("## Notas de produccion")
        for note in production_notes:
            lines.append(f"- {note}")
        lines.append("")

    return "\n".join(lines)
