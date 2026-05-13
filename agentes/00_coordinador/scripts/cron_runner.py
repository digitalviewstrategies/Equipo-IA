"""
cron_runner.py — Orquestador de tareas recurrentes de DV.

Tareas (subcomandos):
    recompute-state    Recalcula shared/state/<cliente>.json para todos los brands.
    daily-monitor      Trae insights de los ultimos N dias por cliente con campanas
                       activas y escribe alertas si detecta fatigue/KILL.
    weekly-report      Genera reporte semanal por cliente con campanas activas.

Cada corrida loggea a shared/state/cron_log.jsonl (timestamp, task, status, detalle).

Pensado para Windows Task Scheduler. Ejemplo de tarea diaria:
    schtasks /Create /SC DAILY /ST 08:30 /TN "DV-DailyMonitor" \
        /TR "python C:\\...\\cron_runner.py daily-monitor"
"""

from __future__ import annotations

import json
import sys
import traceback
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SHARED = ROOT / "shared"
BRANDS = SHARED / "brands"
STATE_DIR = SHARED / "state"
LOG = STATE_DIR / "cron_log.jsonl"
PA_OUT = ROOT / "agentes" / "04_pauta" / "outputs"

sys.path.insert(0, str(ROOT / "agentes" / "04_pauta"))
sys.path.insert(0, str(Path(__file__).parent))


def _trigger_auto_deliver(path: Path) -> None:
    """Dispara auto_deliver del agente delivery (genera reporte cliente + WA)."""
    try:
        import importlib.util
        ad_path = ROOT / "agentes" / "03_delivery_reporting" / "scripts" / "auto_deliver.py"
        spec = importlib.util.spec_from_file_location("auto_deliver_mod", ad_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.trigger_for_path(str(path))
    except Exception as e:
        _log("auto-deliver", "warn", f"{path.name}: {e}")


def _log(task: str, status: str, detail: dict | str = "") -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "task": task,
        "status": status,
        "detail": detail,
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"[{entry['ts']}] {task} {status} :: {detail}")


def _brands_con_campanas() -> list[tuple[str, str]]:
    """Lista (cliente, ad_account_id) de brands con ad_account configurado."""
    out = []
    for p in BRANDS.glob("*.json"):
        if p.stem.startswith("_"):
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        ad_id = (data.get("meta_ads") or {}).get("ad_account_id")
        if ad_id:
            out.append((p.stem, ad_id))
    return out


# ---------- Tareas ----------

def recompute_state() -> int:
    from state_manager import compute, listar_clientes, write
    n = 0
    for c in listar_clientes():
        try:
            write(compute(c))
            n += 1
        except Exception as e:
            _log("recompute-state", "error", f"{c}: {e}")

    # reindex de assets (FTS5)
    try:
        import importlib.util
        ai = ROOT / "shared" / "scripts" / "asset_index.py"
        spec = importlib.util.spec_from_file_location("asset_index", ai)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        r = mod.index_all()
        _log("recompute-state", "ok", {"clientes": n, "assets_indexados": r["total"]})
    except Exception as e:
        _log("recompute-state", "warn", f"asset_index: {e}")
    return 0


def _load_brand_creative_hints(cliente: str) -> dict:
    """Lee hook_frameworks + narrative_structure del brand JSON para enriquecer el brief."""
    p = BRANDS / f"{cliente}.json"
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    tov = data.get("tone_of_voice") or {}
    return {
        "hook_frameworks": tov.get("hook_frameworks") or {},
        "narrative_structure": tov.get("narrative_structure") or {},
        "preferred_words": tov.get("preferred_words") or [],
    }


def _write_brief_creativo(cliente: str, since, until, analyses: list) -> Path:
    """Genera brief_creativo_*.md auto-derivado del analisis para feedback loop."""
    from scripts.campaign_analyzer import generate_recommendations

    scales = [a for a in analyses if a.classification == "SCALE"]
    kills = [a for a in analyses if a.classification == "KILL"]
    iterates = [a for a in analyses if a.classification == "ITERATE"]

    total_spend = sum(a.metrics.get("spend", 0) for a in analyses)
    total_leads = sum(a.metrics.get("leads", 0) for a in analyses)
    avg_cpl = (total_spend / total_leads) if total_leads else 0.0

    def _row(a):
        m = a.metrics
        cpl = f"USD {m['cpl']:.2f}" if m.get("cpl") else "N/A"
        hr = f"{m['hook_rate']:.1f}%" if m.get("hook_rate") is not None else "N/A"
        return f"| {a.ad_name} | - | - | {cpl} | {m.get('ctr', 0):.2f}% | {hr} | {m.get('impressions', 0):,} | {a.score:.1f} |"

    lines = [
        f"# Brief Creativo — {cliente} — {date.today().isoformat()}",
        f"_Auto-generado por cron daily-monitor a partir del periodo {since} a {until}._",
        "",
        "## Contexto de campana",
        f"- Periodo analizado: {since} a {until}",
        f"- Gasto del periodo: USD {total_spend:.2f}",
        f"- Leads generados: {total_leads}",
        f"- CPL promedio: USD {avg_cpl:.2f}",
        "",
        "## Creativos ganadores (SCALE)",
        "",
        "| Creativo | Formato | Angulo | CPL | CTR | Hook Rate | Impresiones | Score |",
        "|----------|---------|--------|-----|-----|-----------|-------------|-------|",
    ]
    lines += [_row(a) for a in scales] or ["| _(ninguno todavia)_ |  |  |  |  |  |  |  |"]
    lines += [
        "",
        "## Creativos perdedores (KILL)",
        "",
        "| Creativo | Formato | Angulo | CPL | CTR | Hook Rate | Impresiones | Score |",
        "|----------|---------|--------|-----|-----|-----------|-------------|-------|",
    ]
    lines += [_row(a) for a in kills] or ["| _(ninguno)_ |  |  |  |  |  |  |  |"]
    lines += [
        "",
        "## Creativos en iteracion (ITERATE)",
        "",
        "| Creativo | Problema detectado | Sugerencia |",
        "|----------|-------------------|------------|",
    ]
    lines += [f"| {a.ad_name} | {a.reason} | Variar hook/formato |" for a in iterates] or ["| _(ninguno)_ |  |  |"]
    lines += [
        "",
        "## Lo que necesito",
        f"- {max(3, len(kills))} creativos nuevos que reemplacen a los KILL",
        "- Angulos sugeridos basados en data:",
    ]
    if scales:
        lines.append(f"  1. Variantes del top performer: {scales[0].ad_name}")
    lines.append("  2. Probar nuevo angulo no testeado")
    lines += [
        "- Evitar:",
        *[f"  - {a.ad_name}: {a.reason}" for a in kills[:3]],
        "",
        "## Recomendaciones del analyzer",
        *[f"- {r}" for r in generate_recommendations(analyses)],
    ]

    hints = _load_brand_creative_hints(cliente)
    fw = hints.get("hook_frameworks") or {}
    if fw:
        lines += ["", "## Hook frameworks de la brand (elegir 2-3 para los nuevos)"]
        for name, body in fw.items():
            if isinstance(body, dict):
                desc = body.get("description", "")
                ex = body.get("example", "")
                lines.append(f"- **{name}** — {desc}")
                if ex:
                    lines.append(f"  - Ejemplo: _{ex}_")
            else:
                lines.append(f"- **{name}** — {body}")
    ns = hints.get("narrative_structure") or {}
    if ns:
        steps = ns.get("steps") or []
        if steps:
            lines += [
                "",
                f"## Estructura narrativa: {ns.get('name', 'estructura')}",
                " -> ".join(steps),
            ]
    pw = hints.get("preferred_words") or []
    if pw:
        lines += [
            "",
            "## Vocabulario preferido (usar)",
            ", ".join(pw[:25]),
        ]
    lines += [
        "",
        "Va para Nico (Creative Director). Proximo paso: ideacion de nuevos guiones/conceptos para reemplazar los KILL.",
    ]

    out_dir = PA_OUT / cliente / date.today().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"brief_creativo_auto_{date.today().isoformat()}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def daily_monitor(days: int = 1) -> int:
    """Trae insights del dia anterior, clasifica ads y escribe alertas + brief si hay KILL."""
    try:
        from scripts.meta_api import MetaAdsAPI
        from scripts.campaign_analyzer import analyze_ad
    except Exception as e:
        _log("daily-monitor", "error", f"import: {e}")
        return 1

    until = date.today() - timedelta(days=1)
    since = until - timedelta(days=days - 1)
    date_range = {"since": since.isoformat(), "until": until.isoformat()}

    resumen = []
    for cliente, ad_id in _brands_con_campanas():
        try:
            api = MetaAdsAPI(ad_account_id=ad_id)
            insights = api.get_insights(ad_id, date_range=date_range, level="ad")
        except Exception as e:
            resumen.append({"cliente": cliente, "status": "error", "msg": str(e)[:200]})
            continue

        if not insights:
            resumen.append({"cliente": cliente, "status": "sin_insights"})
            continue

        analyses = [analyze_ad(i) for i in insights]
        kills = [a for a in analyses if a.classification in ("KILL", "ITERATE")]
        fatiga = [a for a in analyses if a.metrics.get("frequency", 0) >= 3.0]

        if kills or fatiga:
            # cierra el loop: brief automatico para Creative Director
            try:
                _write_brief_creativo(cliente, since, until, analyses)
            except Exception as e:
                _log("daily-monitor", "warn", f"{cliente}: brief no generado: {e}")

            out_dir = PA_OUT / cliente / date.today().isoformat()
            out_dir.mkdir(parents=True, exist_ok=True)
            alert_path = out_dir / f"alerta_daily_{date.today().isoformat()}.md"
            lines = [
                f"# Alerta diaria — {cliente}",
                f"Periodo analizado: {since} a {until}",
                f"Generado: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
                "",
                f"## Ads a revisar ({len(kills)})",
            ]
            for a in kills:
                cpl = a.metrics.get("cpl")
                cpl_s = f"USD {cpl:.2f}" if cpl else "N/A"
                lines.append(f"- **{a.ad_name}** — {a.classification}. CPL {cpl_s}. {a.reason}")
            if fatiga:
                lines.append("")
                lines.append(f"## Fatiga (frequency >= 3.0)")
                for a in fatiga:
                    lines.append(f"- {a.ad_name}: freq {a.metrics.get('frequency', 0):.2f}")
            lines += ["", "Va para Felipe. Proximo paso: revisar y decidir SCALE/KILL/ITERATE."]
            alert_path.write_text("\n".join(lines), encoding="utf-8")
            resumen.append({"cliente": cliente, "status": "alerta", "kills": len(kills), "fatiga": len(fatiga)})
        else:
            resumen.append({"cliente": cliente, "status": "ok", "ads": len(analyses)})

    _log("daily-monitor", "ok", {"clientes": len(resumen), "resumen": resumen})

    # Alerta WA a Felipe si hay clientes con KILL/fatiga (fail-open).
    try:
        import importlib.util
        pa_path = Path(__file__).parent / "pauta_alerts.py"
        spec = importlib.util.spec_from_file_location("pauta_alerts", pa_path)
        pa = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pa)
        alert_r = pa.notify(resumen)
        if alert_r.get("status") == "ok":
            _log("daily-monitor-alert", "ok", {"to": alert_r["to"], "alertas": alert_r["alertas"]})
        elif alert_r.get("status") not in ("skip",):
            _log("daily-monitor-alert", "warn", alert_r)
    except Exception as e:
        _log("daily-monitor-alert", "warn", str(e)[:300])

    return 0


def weekly_report() -> int:
    """Genera reporte semanal markdown por cliente con campanas."""
    try:
        from scripts.meta_api import MetaAdsAPI
        from scripts.campaign_analyzer import analyze_ad, generate_recommendations
        from scripts.report_generator import generate_weekly_report
    except Exception as e:
        _log("weekly-report", "error", f"import: {e}")
        return 1

    until = date.today() - timedelta(days=1)
    since = until - timedelta(days=6)
    date_range = {"since": since.isoformat(), "until": until.isoformat()}

    resumen = []
    for cliente, ad_id in _brands_con_campanas():
        try:
            api = MetaAdsAPI(ad_account_id=ad_id)
            insights = api.get_insights(ad_id, date_range=date_range, level="ad")
        except Exception as e:
            resumen.append({"cliente": cliente, "status": "error", "msg": str(e)[:200]})
            continue

        if not insights:
            resumen.append({"cliente": cliente, "status": "sin_data"})
            continue

        analyses = [analyze_ad(i) for i in insights]
        total_spend = sum(float(i.get("spend", 0) or 0) for i in insights)
        total_imp = sum(int(i.get("impressions", 0) or 0) for i in insights)
        total_reach = sum(int(i.get("reach", 0) or 0) for i in insights)
        total_leads = sum(a.metrics.get("leads", 0) for a in analyses)
        avg_cpl = (total_spend / total_leads) if total_leads else 0.0

        report = generate_weekly_report(
            cliente=cliente,
            date_start=since.isoformat(),
            date_end=until.isoformat(),
            total_spend=total_spend,
            total_leads=total_leads,
            avg_cpl=avg_cpl,
            total_impressions=total_imp,
            total_reach=total_reach,
            analyses=analyses,
            recommendations=generate_recommendations(analyses),
            next_actions=["Revisar bottom 3 y decidir KILL", "Confirmar top 3 para escalar"],
        )

        out_dir = PA_OUT / cliente / date.today().isoformat()
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"reporte_semanal_{since.isoformat()}_{until.isoformat()}.md"
        path.write_text(report, encoding="utf-8")
        _trigger_auto_deliver(path)
        resumen.append({"cliente": cliente, "status": "ok", "leads": total_leads, "spend": round(total_spend, 2)})

    _log("weekly-report", "ok", {"clientes": len(resumen), "resumen": resumen})
    return 0


def pull_leads(hours: int = 24) -> int:
    """Trae leads de Meta de las ultimas N horas y los inserta en el pipeline comercial.

    Si hay leads nuevos, dispara alerta WA a Elias (lead_alerts.notify).
    """
    try:
        import importlib.util
        p = ROOT / "agentes" / "02_comercial" / "scripts" / "meta_leads_puller.py"
        spec = importlib.util.spec_from_file_location("meta_leads_puller", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        r = mod.pull_recent_leads(hours=hours)
        _log("pull-leads", "ok", r)
    except Exception as e:
        _log("pull-leads", "error", str(e)[:300])
        return 1

    # Alerta WA si hay leads nuevos (fail-open: si falla, no rompe el cron)
    try:
        import importlib.util
        la_path = Path(__file__).parent / "lead_alerts.py"
        spec = importlib.util.spec_from_file_location("lead_alerts", la_path)
        la = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(la)
        alert_r = la.notify(r)
        if alert_r.get("status") not in ("skip", "ok"):
            _log("pull-leads-alert", "warn", alert_r)
        elif alert_r.get("status") == "ok":
            _log("pull-leads-alert", "ok", {"to": alert_r["to"], "total": alert_r["total"]})
    except Exception as e:
        _log("pull-leads-alert", "warn", str(e)[:300])

    return 0


def process_creative_briefs() -> int:
    """Notifica a Nico por WA los briefs auto pendientes (no genera guiones)."""
    try:
        import importlib.util
        p = Path(__file__).parent / "process_creative_briefs.py"
        spec = importlib.util.spec_from_file_location("process_creative_briefs", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        r = mod.process()
        status = "ok" if not r.get("errores") else "warn"
        _log("process-creative-briefs", status, r)
        return 0
    except Exception as e:
        _log("process-creative-briefs", "error", str(e)[:300])
        return 1


def prescore_leads() -> int:
    """Auto-prescore de leads en pre_filtro: priority + knockouts + red_flags."""
    try:
        import importlib.util
        p = ROOT / "agentes" / "02_comercial" / "scripts" / "lead_prescore.py"
        spec = importlib.util.spec_from_file_location("lead_prescore", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        r = mod.run(dry_run=False)
        status = "warn" if r.get("knockouts_detected") or r.get("by_priority", {}).get("stale") else "ok"
        _log("prescore-leads", status, r)
        return 0
    except Exception as e:
        _log("prescore-leads", "error", str(e)[:300])
        return 1


def lead_followups() -> int:
    """Genera drafts WA primer contacto para leads priority 1/2 sin trabajar."""
    try:
        import importlib.util
        p = ROOT / "agentes" / "02_comercial" / "scripts" / "followup_drafts.py"
        spec = importlib.util.spec_from_file_location("followup_drafts", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        r = mod.run(dry_run=False)
        _log("lead-followups", "ok", r)
        return 0
    except Exception as e:
        _log("lead-followups", "error", str(e)[:300])
        return 1


def auto_approve() -> int:
    """Corre validators sobre outputs recientes y escribe sidecar .status.json."""
    try:
        import importlib.util
        p = ROOT / ".claude" / "scripts" / "auto_approve.py"
        spec = importlib.util.spec_from_file_location("auto_approve", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        today = date.today()
        yest = today - timedelta(days=1)
        agg = {"candidates": 0, "processed": 0, "ready_for_handoff": 0, "needs_human": 0, "flagged": []}
        for d in (today.isoformat(), yest.isoformat()):
            r = mod.run(None, d, False)
            for k in ("candidates", "processed", "ready_for_handoff", "needs_human"):
                agg[k] += r[k]
            agg["flagged"].extend(r["flagged"])
        status = "warn" if agg["needs_human"] else "ok"
        # corta flagged en log para no inflar jsonl
        log_payload = dict(agg)
        log_payload["flagged"] = log_payload["flagged"][:5]
        _log("auto-approve", status, log_payload)
        return 0
    except Exception as e:
        _log("auto-approve", "error", str(e)[:300])
        return 1


def health() -> int:
    """Chequea que las tareas cron hayan corrido OK dentro del SLA."""
    try:
        import importlib.util
        p = Path(__file__).parent / "health_check.py"
        spec = importlib.util.spec_from_file_location("health_check", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        r = mod.check()
        status = "warn" if r.get("stale") else "ok"
        _log("health", status, r)
        return 0
    except Exception as e:
        _log("health", "error", str(e)[:300])
        return 1


TASKS = {
    "recompute-state": recompute_state,
    "daily-monitor": daily_monitor,
    "weekly-report": weekly_report,
    "pull-leads": pull_leads,
    "process-creative-briefs": process_creative_briefs,
    "prescore-leads": prescore_leads,
    "lead-followups": lead_followups,
    "auto-approve": auto_approve,
    "health": health,
}


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in TASKS:
        print(__doc__)
        print(f"Tareas disponibles: {', '.join(TASKS)}")
        return 1
    task = argv[0]
    try:
        return TASKS[task]()
    except Exception as e:
        _log(task, "fatal", traceback.format_exc()[:500])
        print(f"FATAL: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
