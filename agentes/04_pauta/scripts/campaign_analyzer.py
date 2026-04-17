"""
campaign_analyzer.py — Motor de analisis de campanas de Meta Ads.

Clasifica ads y ad sets como SCALE / KILL / ITERATE / HOLD
segun los benchmarks de DV definidos en context/metricas_benchmarks.md.
"""

from dataclasses import dataclass, field


@dataclass
class Benchmarks:
    """Thresholds de decision. Ajustables por cliente."""
    cpl_target: float = 5.0       # USD
    ctr_min: float = 0.5          # % — debajo de esto, KILL
    ctr_good: float = 1.5         # % — arriba de esto, aceptable
    hook_rate_min: float = 10.0   # % — debajo de esto, KILL
    hook_rate_good: float = 30.0  # %
    frequency_alert: float = 3.0  # — alerta de fatiga
    frequency_critical: float = 4.0
    min_impressions_for_decision: int = 1000
    min_spend_for_scale: float = 30.0  # USD


DEFAULT_BENCHMARKS = Benchmarks()


@dataclass
class AdAnalysis:
    """Resultado de analisis de un ad individual."""
    ad_id: str
    ad_name: str
    classification: str  # SCALE, KILL, ITERATE, HOLD
    reason: str
    metrics: dict = field(default_factory=dict)
    recommendation: str = ""
    score: float = 0.0


def _extract_leads(actions: list[dict] | None) -> int:
    """Extrae cantidad de leads de la lista de actions de Meta."""
    if not actions:
        return 0
    for action in actions:
        if action.get("action_type") in ("lead", "onsite_conversion.lead_grouped"):
            return int(action.get("value", 0))
    return 0


def _extract_cost_per_lead(cost_per_action: list[dict] | None) -> float | None:
    """Extrae CPL de cost_per_action_type."""
    if not cost_per_action:
        return None
    for action in cost_per_action:
        if action.get("action_type") in ("lead", "onsite_conversion.lead_grouped"):
            return float(action.get("value", 0))
    return None


def _extract_3s_views(video_play_actions: list[dict] | None) -> int:
    """Extrae 3-second video views."""
    if not video_play_actions:
        return 0
    for action in video_play_actions:
        if action.get("action_type") == "video_view":
            return int(action.get("value", 0))
    return 0


def _calculate_hook_rate(impressions: int, video_3s_views: int) -> float | None:
    """Calcula hook rate (3s views / impressions * 100)."""
    if impressions == 0:
        return None
    return (video_3s_views / impressions) * 100


def _calculate_score(
    cpl: float | None,
    ctr: float,
    hook_rate: float | None,
    impressions: int,
    benchmarks: Benchmarks,
) -> float:
    """Score compuesto para ranking (0-100)."""
    # CPL score (40%)
    if cpl is None or cpl == 0:
        cpl_score = 50.0  # sin data, neutro
    else:
        max_cpl = benchmarks.cpl_target * 2
        cpl_score = max(0, min(100, (1 - cpl / max_cpl) * 100))

    # CTR score (25%)
    ctr_score = min(100, (ctr / 4.0) * 100)

    # Hook rate score (20%)
    if hook_rate is None:
        hr_score = 50.0
    else:
        hr_score = min(100, (hook_rate / 60.0) * 100)

    # Volume score (15%)
    vol_score = min(100, (impressions / 10000) * 100)

    return (cpl_score * 0.40) + (ctr_score * 0.25) + (hr_score * 0.20) + (vol_score * 0.15)


def analyze_ad(insight: dict, benchmarks: Benchmarks | None = None) -> AdAnalysis:
    """
    Analiza un ad individual y lo clasifica.

    Args:
        insight: dict de insights de la API de Meta para un ad.
        benchmarks: thresholds (usa defaults si no se pasan).

    Returns:
        AdAnalysis con clasificacion y recomendacion.
    """
    b = benchmarks or DEFAULT_BENCHMARKS

    ad_id = insight.get("ad_id", insight.get("id", "unknown"))
    ad_name = insight.get("ad_name", "unknown")
    impressions = int(insight.get("impressions", 0))
    spend = float(insight.get("spend", 0))
    ctr = float(insight.get("ctr", 0))
    frequency = float(insight.get("frequency", 0))

    leads = _extract_leads(insight.get("actions"))
    cpl = _extract_cost_per_lead(insight.get("cost_per_action_type"))
    if cpl is None and leads > 0 and spend > 0:
        cpl = spend / leads

    video_3s = _extract_3s_views(insight.get("video_play_actions"))
    hook_rate = _calculate_hook_rate(impressions, video_3s)

    metrics = {
        "impressions": impressions,
        "spend": spend,
        "ctr": ctr,
        "cpl": cpl,
        "leads": leads,
        "frequency": frequency,
        "hook_rate": hook_rate,
        "video_3s_views": video_3s,
    }

    score = _calculate_score(cpl, ctr, hook_rate, impressions, b)

    # Clasificacion
    if impressions < b.min_impressions_for_decision and spend < b.min_spend_for_scale:
        return AdAnalysis(
            ad_id=ad_id,
            ad_name=ad_name,
            classification="HOLD",
            reason=f"Data insuficiente: {impressions} impresiones, USD {spend:.2f} gastados.",
            metrics=metrics,
            recommendation="Esperar 48-72hs mas de data antes de tomar decisiones.",
            score=score,
        )

    # KILL checks
    if cpl is not None and cpl > b.cpl_target * 2:
        return AdAnalysis(
            ad_id=ad_id,
            ad_name=ad_name,
            classification="KILL",
            reason=f"CPL USD {cpl:.2f} supera 2x el target (USD {b.cpl_target}).",
            metrics=metrics,
            recommendation="Pausar. El angulo o creativo no resuena con la audiencia.",
            score=score,
        )

    if hook_rate is not None and hook_rate < b.hook_rate_min:
        return AdAnalysis(
            ad_id=ad_id,
            ad_name=ad_name,
            classification="KILL",
            reason=f"Hook rate {hook_rate:.1f}% debajo del minimo ({b.hook_rate_min}%).",
            metrics=metrics,
            recommendation="Pausar. El hook no engancha. Probar hook completamente distinto.",
            score=score,
        )

    if ctr < b.ctr_min:
        return AdAnalysis(
            ad_id=ad_id,
            ad_name=ad_name,
            classification="KILL",
            reason=f"CTR {ctr:.2f}% debajo del minimo ({b.ctr_min}%).",
            metrics=metrics,
            recommendation="Pausar. El creativo no genera clicks.",
            score=score,
        )

    if spend >= 20 and leads == 0:
        return AdAnalysis(
            ad_id=ad_id,
            ad_name=ad_name,
            classification="KILL",
            reason=f"USD {spend:.2f} gastados sin generar un solo lead.",
            metrics=metrics,
            recommendation="Pausar. Revisar lead form, landing, y creativo.",
            score=score,
        )

    # SCALE checks
    if (
        cpl is not None
        and cpl <= b.cpl_target
        and ctr >= b.ctr_good
        and spend >= b.min_spend_for_scale
    ):
        return AdAnalysis(
            ad_id=ad_id,
            ad_name=ad_name,
            classification="SCALE",
            reason=f"CPL USD {cpl:.2f} bajo target, CTR {ctr:.2f}% bueno, USD {spend:.2f} gastados.",
            metrics=metrics,
            recommendation="Subir budget 20% en 3 dias. No duplicar de golpe.",
            score=score,
        )

    # ITERATE — entre SCALE y KILL
    reasons = []
    if cpl is not None and b.cpl_target < cpl <= b.cpl_target * 1.5:
        reasons.append(f"CPL USD {cpl:.2f} cerca del target pero no lo alcanza")
    if hook_rate is not None and hook_rate >= b.hook_rate_good and ctr < b.ctr_good:
        reasons.append(f"Buen hook rate ({hook_rate:.1f}%) pero CTR bajo ({ctr:.2f}%)")
    if frequency >= b.frequency_alert:
        reasons.append(f"Frequency {frequency:.1f} indica fatiga temprana")

    if reasons:
        return AdAnalysis(
            ad_id=ad_id,
            ad_name=ad_name,
            classification="ITERATE",
            reason=". ".join(reasons) + ".",
            metrics=metrics,
            recommendation="Pedir variante al Creative Director. No matar hasta tener reemplazo.",
            score=score,
        )

    # Default: HOLD con data suficiente pero sin señal clara
    return AdAnalysis(
        ad_id=ad_id,
        ad_name=ad_name,
        classification="HOLD",
        reason="Metricas dentro de rango aceptable pero sin señal clara de SCALE.",
        metrics=metrics,
        recommendation="Mantener activo. Revisar en 48-72hs.",
        score=score,
    )


def analyze_campaign(
    insights: list[dict],
    benchmarks: Benchmarks | None = None,
) -> list[AdAnalysis]:
    """Analiza todos los ads de una campana y devuelve clasificaciones."""
    return [analyze_ad(insight, benchmarks) for insight in insights]


def detect_fatigue(
    insights: list[dict],
    frequency_threshold: float = 3.0,
) -> list[dict]:
    """
    Detecta ads con fatiga creativa.

    Returns:
        Lista de dicts con ad_name, frequency, y nivel de alerta.
    """
    fatigued = []
    for insight in insights:
        freq = float(insight.get("frequency", 0))
        if freq >= frequency_threshold:
            fatigued.append({
                "ad_name": insight.get("ad_name", "unknown"),
                "ad_id": insight.get("ad_id", insight.get("id", "unknown")),
                "frequency": freq,
                "alert_level": "CRITICO" if freq >= 4.0 else "ALERTA",
            })
    return sorted(fatigued, key=lambda x: x["frequency"], reverse=True)


def compare_creatives(
    insights: list[dict],
    benchmarks: Benchmarks | None = None,
) -> list[AdAnalysis]:
    """Analiza y rankea creativos por score compuesto descendente."""
    analyses = analyze_campaign(insights, benchmarks)
    return sorted(analyses, key=lambda a: a.score, reverse=True)


def generate_recommendations(analyses: list[AdAnalysis]) -> list[str]:
    """Genera lista de recomendaciones accionables a partir del analisis."""
    recs = []

    scale = [a for a in analyses if a.classification == "SCALE"]
    kill = [a for a in analyses if a.classification == "KILL"]
    iterate = [a for a in analyses if a.classification == "ITERATE"]
    hold = [a for a in analyses if a.classification == "HOLD"]

    if scale:
        names = ", ".join(a.ad_name for a in scale)
        recs.append(f"ESCALAR: {names}. Subir budget 20% en los proximos 3 dias.")

    if kill:
        names = ", ".join(a.ad_name for a in kill)
        recs.append(f"PAUSAR: {names}. Motivos: {'; '.join(a.reason for a in kill)}")

    if iterate:
        names = ", ".join(a.ad_name for a in iterate)
        recs.append(
            f"ITERAR: {names}. Generar brief para Creative Director con variantes."
        )

    if hold:
        names = ", ".join(a.ad_name for a in hold)
        recs.append(f"HOLD: {names}. Revisar en 48-72hs con mas data.")

    if kill or iterate:
        recs.append(
            f"CREATIVOS NUEVOS: necesitas {len(kill) + len(iterate)} creativos "
            f"para reemplazar los que se pausan/iteran."
        )

    return recs
