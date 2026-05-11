"""
render_pdf.py - Renderiza reporte semanal HTML -> PDF con Playwright.

Por que NO Canva: el AI de Canva no respeta paleta DV. Con HTML/CSS tenemos
total control de colores (#0033CC, #C8FF00, #0A0A0A) y tipografias
(Inter + Space Grotesk).

Uso programatico:
    from scripts.render_pdf import render_reporte_semanal
    pdf_bytes = render_reporte_semanal(data)
    # data: dict con todos los placeholders (GASTO, LEADS, CPL, etc.)

Uso CLI:
    python render_pdf.py --data-json data.json --out reporte.pdf

Funciona en cron porque playwright corre browser headless local
(no requiere MCP ni autenticacion externa).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from datetime import date
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
DELIVERY_ROOT = THIS_DIR.parent
TEMPLATE_DIR = DELIVERY_ROOT / "templates" / "reporte_semanal"
TEMPLATE_HTML = TEMPLATE_DIR / "index.html"


def _delta_classify(value: float, lower_is_better: bool = False) -> tuple[str, str]:
    """Devuelve (clase_css, arrow) segun valor y direccion deseada."""
    if value > 0:
        cls = "down" if lower_is_better else "up"
        arrow = "↑"
    elif value < 0:
        cls = "up" if lower_is_better else "down"
        arrow = "↓"
    else:
        cls = "flat"
        arrow = "→"
    return cls, arrow


def _fmt_pct(v: float) -> str:
    sign = "+" if v > 0 else ("" if v < 0 else "")
    return f"{sign}{v:.1f}%"


def _fmt_num(n: int | float) -> str:
    """1234567 -> 1.234.567 (formato AR con punto separador)."""
    return f"{n:,.0f}".replace(",", ".")


def _fmt_money(n: float) -> str:
    return f"{n:,.0f}".replace(",", ".")


def build_data(metrics: dict, prev_metrics: dict | None = None,
               cliente_display: str = "", periodo: str = "",
               insight: str = "", creativos: list[dict] | None = None,
               acciones_hechas: list[str] | None = None,
               plan_proximo: list[str] | None = None) -> dict:
    """
    metrics: {gasto, leads, cpl, ctr, alcance, impresiones}
    prev_metrics: idem para semana anterior (para deltas). None = mostrar +0%.
    creativos: lista de {name, leads, cpl, ctr, status} (status: SCALE|ITERATE|KILL).
    """
    creativos = creativos or []
    acciones_hechas = (acciones_hechas or []) + [""] * 3
    plan_proximo = (plan_proximo or []) + [""] * 3

    def delta(curr, prev, lower_better=False):
        if not prev or prev == 0:
            return 0.0, "flat", "→"
        d = (curr - prev) / prev * 100.0
        cls, arrow = _delta_classify(d, lower_is_better=lower_better)
        return d, cls, arrow

    p = prev_metrics or {}
    g_d, g_c, g_a = delta(metrics.get("gasto", 0), p.get("gasto", 0))
    l_d, l_c, l_a = delta(metrics.get("leads", 0), p.get("leads", 0))
    cpl_d, cpl_c, cpl_a = delta(metrics.get("cpl", 0), p.get("cpl", 0), lower_better=True)
    ctr_d, ctr_c, ctr_a = delta(metrics.get("ctr", 0), p.get("ctr", 0))
    al_d, al_c, al_a = delta(metrics.get("alcance", 0), p.get("alcance", 0))
    im_d, im_c, im_a = delta(metrics.get("impresiones", 0), p.get("impresiones", 0))

    rows = []
    for c in creativos[:6]:
        status = (c.get("status") or "ITERATE").upper()
        badge_cls = {"SCALE": "scale", "ITERATE": "iterate", "KILL": "kill"}.get(status, "iterate")
        name = (c.get("name") or "-")[:48]
        rows.append(
            f"<tr>"
            f"<td>{name}</td>"
            f"<td class=\"num\">{c.get('leads', 0)}</td>"
            f"<td class=\"num\">USD {_fmt_money(c.get('cpl') or 0)}</td>"
            f"<td class=\"num\">{(c.get('ctr') or 0):.2f}%</td>"
            f"<td><span class=\"badge {badge_cls}\">{status}</span></td>"
            f"</tr>"
        )
    if not rows:
        rows = ["<tr><td colspan=\"5\" style=\"color:#9CA3AF;font-style:italic\">Sin creativos con data esta semana.</td></tr>"]

    return {
        "CLIENTE_DISPLAY": cliente_display,
        "PERIODO": periodo,
        "FECHA_GENERACION": date.today().strftime("%d/%m/%Y"),
        "INSIGHT": insight or "Sin insight cargado.",
        "GASTO": _fmt_money(metrics.get("gasto", 0)),
        "LEADS": _fmt_num(metrics.get("leads", 0)),
        "CPL": f"{metrics.get('cpl', 0):.2f}",
        "CTR": f"{metrics.get('ctr', 0):.2f}",
        "ALCANCE": _fmt_num(metrics.get("alcance", 0)),
        "IMPRESIONES": _fmt_num(metrics.get("impresiones", 0)),
        "DELTA_GASTO": _fmt_pct(g_d), "DELTA_GASTO_CLS": g_c, "DELTA_GASTO_ARROW": g_a,
        "DELTA_LEADS": _fmt_pct(l_d), "DELTA_LEADS_CLS": l_c, "DELTA_LEADS_ARROW": l_a,
        "DELTA_CPL": _fmt_pct(cpl_d), "DELTA_CPL_CLS": cpl_c, "DELTA_CPL_ARROW": cpl_a,
        "DELTA_CTR": _fmt_pct(ctr_d), "DELTA_CTR_CLS": ctr_c, "DELTA_CTR_ARROW": ctr_a,
        "DELTA_ALCANCE": _fmt_pct(al_d), "DELTA_ALCANCE_CLS": al_c, "DELTA_ALCANCE_ARROW": al_a,
        "DELTA_IMP": _fmt_pct(im_d), "DELTA_IMP_CLS": im_c, "DELTA_IMP_ARROW": im_a,
        "TABLA_CREATIVOS": "\n".join(rows),
        "ACCION_HECHA_1": acciones_hechas[0] or "—",
        "ACCION_HECHA_2": acciones_hechas[1] or "—",
        "ACCION_HECHA_3": acciones_hechas[2] or "—",
        "PLAN_1": plan_proximo[0] or "—",
        "PLAN_2": plan_proximo[1] or "—",
        "PLAN_3": plan_proximo[2] or "—",
    }


def _apply(template: str, data: dict) -> str:
    def repl(m):
        key = m.group(1)
        return str(data.get(key, m.group(0)))
    return re.sub(r"\{\{([A-Z0-9_]+)\}\}", repl, template)


def render_html_to_pdf(html_path: Path, pdf_out: Path) -> None:
    """Usa playwright sync para renderizar el HTML a PDF respetando CSS."""
    from playwright.sync_api import sync_playwright
    url = html_path.resolve().as_uri()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.pdf(
            path=str(pdf_out),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def render_reporte_semanal(data: dict, pdf_out: Path) -> Path:
    """Render principal: data dict (de build_data) -> PDF en pdf_out."""
    template_text = TEMPLATE_HTML.read_text(encoding="utf-8")
    filled = _apply(template_text, data)
    # Renderiza desde un dir temporal para que el href relativo a style.css funcione
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        html_path = td_path / "index.html"
        css_path = td_path / "style.css"
        css_path.write_text((TEMPLATE_DIR / "style.css").read_text(encoding="utf-8"), encoding="utf-8")
        html_path.write_text(filled, encoding="utf-8")
        render_html_to_pdf(html_path, pdf_out)
    return pdf_out


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--data-json", required=True, help="Path JSON con metrics + opcionales")
    p.add_argument("--out", required=True, help="Path PDF salida")
    p.add_argument("--cliente-display", default="")
    p.add_argument("--periodo", default="")
    p.add_argument("--insight", default="")
    a = p.parse_args(argv)

    raw = json.loads(Path(a.data_json).read_text(encoding="utf-8"))
    metrics = raw.get("metrics", {})
    prev = raw.get("prev_metrics")
    creativos = raw.get("creativos", [])
    acciones = raw.get("acciones_hechas", [])
    plan = raw.get("plan_proximo", [])
    cliente_display = a.cliente_display or raw.get("cliente_display", "")
    periodo = a.periodo or raw.get("periodo", "")
    insight = a.insight or raw.get("insight", "")

    data = build_data(
        metrics=metrics, prev_metrics=prev,
        cliente_display=cliente_display, periodo=periodo,
        insight=insight, creativos=creativos,
        acciones_hechas=acciones, plan_proximo=plan,
    )
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    render_reporte_semanal(data, out)
    print(json.dumps({"status": "ok", "pdf": str(out)}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
