"""
render_editorial.py — Ensambla y renderiza un carrusel editorial cinematografico.

Uso:
    python scripts/render_editorial.py <copy.json> [--prefix slide]

El copy.json especifica:
    {
      "pieza": "carrusel_captacion_belgrano",
      "cliente": "toribio_achaval",
      "fecha": "2026-05-05",
      "output_subdir": "carrusel_captacion_02_belgrano",
      "fotos": {"hook": "fachada_x.jpg", "narrative": "interior_y.jpg", "cta": "casa.jpg"},
      "slides": [
        {"tipo": "hook_foto", "label": "...", "headline_html": "...", "sub_text": "...", "sub_meta": "...", "footer_meta": "...", "pn": "01 / 07"},
        {"tipo": "contexto_lead", "tag": "...", "pn": "02 / 07", "kicker": "...", "title_html": "...", "lead": "...", "vars": [{"n":"01","h":"...","p":"..."},...]},
        {"tipo": "compare_arrow_foto", "tag":"...", "pn":"...", "kicker":"...", "title_html":"...", "left_h5":"...","left_v_html":"...","left_p":"...", "right_h5":"...","right_v_html":"...","right_p":"..."},
        {"tipo": "dato_grande", "tag":"...","pn":"...","kicker":"...","title_html":"...","num_html":"...","num_anno_html":"...","cols":[{"h":"...","v_html":"...","p":"..."},...]},
        {"tipo": "stat_duo_chips", "tag":"...","pn":"...","kicker":"...","title_html":"...","stats":[{"label":"...","num_html":"...","sub":"..."},...],"chips_h5":"...","chips":[{"t":"...","hl":true},...]},
        {"tipo": "duo_indicador", "tag":"...","pn":"...","kicker":"...","title_html":"...","cols":[{"h5":"...","arrow":"→","word_html":"Estable","p":"..."},...],"insight_html":"..."},
        {"tipo": "problema_3puntos_foto", "tag":"...","pn":"...","kicker":"...","title_html":"...","puntos":[{"n":"01","txt_html":"..."},...]},
        {"tipo": "cta_foto", "tag":"...","pn":"...","kicker":"...","cta_html":"...","invite":"...","meta_html":"..."}
      ]
    }
"""
import argparse
import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRANDS = ROOT.parent.parent.parent / "shared" / "brands"
TEMPLATES = ROOT / "templates"
OUTPUT_BASE = ROOT / "output"


def load_brand(brand_id: str) -> dict:
    return json.loads((BRANDS / f"{brand_id}.json").read_text(encoding="utf-8"))


def load_logo_b64(brand: dict) -> str:
    logo_rel = brand["logo"]["main_file"]
    logo_path = BRANDS / logo_rel
    return base64.b64encode(logo_path.read_bytes()).decode("ascii")


def copy_photo_assets(brand_id: str, fotos: dict, out_dir: Path) -> dict:
    """Copia las fotos especificadas a out_dir. Retorna dict {role: nombre_archivo}.
    Las fotos pueden estar en shared/brands/assets/<brand>/ o ya en out_dir."""
    brand_assets = BRANDS / "assets" / brand_id
    out_paths = {}
    for role, fname in fotos.items():
        if not fname:
            continue
        src_options = [out_dir / fname, brand_assets / fname]
        src = next((p for p in src_options if p.exists()), None)
        if src is None:
            print(f"WARN: foto '{fname}' (rol {role}) no encontrada en out_dir ni en {brand_assets}", file=sys.stderr)
            continue
        dst = out_dir / fname
        if src != dst:
            shutil.copy(src, dst)
        out_paths[role] = fname
    return out_paths


# ============================================================================
# BLOCK BUILDERS
# ============================================================================

def head(slide: dict) -> str:
    return f'''<div class="top">
      <div class="l"><span class="dot"></span>{slide.get("tag","")}</div>
      <div class="pn">{slide.get("pn","")}</div>
    </div>'''


def foot(slide: dict, light: bool = False) -> str:
    l = slide.get("foot_l","TORIBIO ACHAVAL — REAL ESTATE")
    r = slide.get("foot_r","MERCADO · MAYO 2026")
    return f'<div class="foot-row"><div>{l}</div><div>{r}</div></div>'


def b_hook_foto(slide, photo_url):
    return f'''<div class="slide bg-photo b-hook">
  <div class="photo" style="background-image:url('{photo_url}');"></div>
  <div class="ovl-hook"></div>
  <div class="grain"></div>
  <div class="content">
    {head(slide)}
    <div class="body">
      <div class="label">{slide.get("label","EL DATO")}</div>
      <div class="headline">{slide["headline_html"]}</div>
      <div class="sub">
        <div class="col"><p>{slide.get("sub_text","")}</p></div>
        <div class="col"><p class="meta">{slide.get("sub_meta","")}</p></div>
      </div>
      <div class="footer">
        <div class="meta">{slide.get("footer_meta","LECTURA DE CICLO · MERCADO PREMIUM")}</div>
        <div class="pn">{slide.get("pn","")}</div>
      </div>
    </div>
  </div>
</div>'''


def b_contexto_lead(slide, bg="bg-paper"):
    vars_html = "".join(
        f'<div class="var-card"><div class="num">{v["n"]}</div><h4>{v["h"]}</h4><p>{v["p"]}</p></div>'
        for v in slide.get("vars",[])
    )
    return f'''<div class="slide {bg} b-contexto">
  {head(slide)}
  <div class="body">
    <div class="kicker">{slide.get("kicker","")}</div>
    <div class="title">{slide["title_html"]}</div>
    {f'<div class="lead">{slide["lead"]}</div>' if slide.get("lead") else ""}
    {f'<div class="three-vars">{vars_html}</div>' if vars_html else ""}
  </div>
  {foot(slide)}
</div>'''


def b_compare_arrow_foto(slide, photo_url):
    return f'''<div class="slide bg-photo b-compare">
  <div class="photo" style="background-image:url('{photo_url}');background-position:center 30%;"></div>
  <div class="ovl-narrative"></div>
  <div class="grain"></div>
  <div class="content">
    {head(slide)}
    <div class="body">
      <div class="kicker">{slide.get("kicker","")}</div>
      <div class="title">{slide["title_html"]}</div>
      <div class="compare">
        <div class="col"><h5>{slide["left_h5"]}</h5><div class="v">{slide["left_v_html"]}</div><p>{slide["left_p"]}</p></div>
        <div class="arrow">→</div>
        <div class="col"><h5>{slide["right_h5"]}</h5><div class="v">{slide["right_v_html"]}</div><p>{slide["right_p"]}</p></div>
      </div>
    </div>
    {foot(slide)}
  </div>
</div>'''


def b_dato_grande(slide, bg="bg-paper"):
    cols_html = "".join(
        f'<div class="col"><h4>{c["h"]}</h4><div class="v">{c["v_html"]}</div><p>{c.get("p","")}</p></div>'
        for c in slide.get("cols",[])
    )
    return f'''<div class="slide {bg} b-dato">
  {head(slide)}
  <div class="body">
    <div class="kicker">{slide.get("kicker","")}</div>
    <div class="title">{slide["title_html"]}</div>
    <div class="num-row">
      <div class="num">{slide["num_html"]}</div>
      <div class="num-anno"><p>{slide["num_anno_html"]}</p></div>
    </div>
    {f'<div class="columns">{cols_html}</div>' if cols_html else ""}
  </div>
  {foot(slide)}
</div>'''


def b_stat_duo_chips(slide, bg="bg-light"):
    stats_html = "".join(
        f'<div class="stat"><div class="label">{s["label"]}</div><div class="num">{s["num_html"]}</div><p class="sub">{s["sub"]}</p></div>'
        for s in slide.get("stats",[])
    )
    chips_html = "".join(
        f'<span class="chip{" hl" if c.get("hl") else ""}">{c["t"]}</span>'
        for c in slide.get("chips",[])
    )
    return f'''<div class="slide {bg} b-statduo">
  {head(slide)}
  <div class="body">
    <div class="kicker">{slide.get("kicker","")}</div>
    <div class="title">{slide["title_html"]}</div>
    <div class="stat-row">{stats_html}</div>
    {f'<div class="chips"><h5>{slide.get("chips_h5","")}</h5>{chips_html}</div>' if chips_html else ""}
  </div>
  {foot(slide)}
</div>'''


def b_duo_indicador(slide, bg="bg-dark"):
    cols_html = "".join(
        f'<div class="col"><h5>{c["h5"]}</h5><div class="indicator"><span class="arrow">{c.get("arrow","→")}</span><span class="word">{c["word_html"]}</span></div><p>{c["p"]}</p></div>'
        for c in slide.get("cols",[])
    )
    return f'''<div class="slide {bg} b-duo">
  {head(slide)}
  <div class="body">
    <div class="kicker">{slide.get("kicker","")}</div>
    <div class="title">{slide["title_html"]}</div>
    <div class="duo">{cols_html}</div>
    {f'<div class="insight">{slide["insight_html"]}</div>' if slide.get("insight_html") else ""}
  </div>
  {foot(slide)}
</div>'''


def b_problema_3puntos_foto(slide, photo_url):
    puntos_html = "".join(
        f'<div class="punto"><div class="n">{p["n"]}</div><div class="txt">{p["txt_html"]}</div></div>'
        for p in slide.get("puntos",[])
    )
    return f'''<div class="slide bg-photo b-problema">
  <div class="photo" style="background-image:url('{photo_url}');background-position:center 30%;"></div>
  <div class="ovl-narrative"></div>
  <div class="grain"></div>
  <div class="content">
    {head(slide)}
    <div class="body">
      <div class="kicker">{slide.get("kicker","")}</div>
      <div class="title">{slide["title_html"]}</div>
      <div class="puntos">{puntos_html}</div>
    </div>
    {foot(slide)}
  </div>
</div>'''


def b_cta_foto(slide, photo_url, logo_data_uri):
    return f'''<div class="slide bg-photo b-cta">
  <div class="photo" style="background-image:url('{photo_url}');"></div>
  <div class="ovl-cta"></div>
  <div class="grain"></div>
  <div class="content">
    {head(slide)}
    <div class="body">
      <div class="kicker">{slide.get("kicker","CONTACTO")}</div>
      <div class="cta">{slide["cta_html"]}</div>
      <div class="invite">{slide.get("invite","")}</div>
    </div>
    <div class="footer">
      <div class="logo"><img src="{logo_data_uri}" alt="Toribio Achaval"></div>
      <div class="meta">{slide.get("meta_html","TORIBIO ACHAVAL<br><strong>REAL ESTATE</strong>")}</div>
    </div>
  </div>
</div>'''


def b_showcase_foto(slide, photo_url):
    micro_html = "".join(
        f'<div class="cell"><div class="lbl">{m["lbl"]}</div><div class="val">{m["val_html"]}</div></div>'
        for m in slide.get("micro",[])
    )
    pos = slide.get("photo_pos","center")
    ovl = slide.get("ovl","ovl-soft")
    return f'''<div class="slide bg-photo b-showcase">
  <div class="photo" style="background-image:url('{photo_url}');background-position:{pos};"></div>
  <div class="{ovl}"></div>
  <div class="grain"></div>
  <div class="content">
    <div class="chapter-row">
      <div class="chapter">{slide.get("chapter_label","CAPÍTULO")}<span class="num">{slide.get("chapter_num","01")}</span></div>
      <div class="room-tag">{slide.get("room_tag","")}</div>
    </div>
    <div class="body">
      <div class="headline">{slide["headline_html"]}</div>
      {f'<div class="sub">{slide["sub"]}</div>' if slide.get("sub") else ""}
      {f'<div class="micro-row">{micro_html}</div>' if micro_html else ""}
    </div>
  </div>
</div>'''


BUILDERS = {
    "hook_foto": b_hook_foto,
    "showcase_foto": b_showcase_foto,
    "contexto_lead": b_contexto_lead,
    "compare_arrow_foto": b_compare_arrow_foto,
    "dato_grande": b_dato_grande,
    "stat_duo_chips": b_stat_duo_chips,
    "duo_indicador": b_duo_indicador,
    "problema_3puntos_foto": b_problema_3puntos_foto,
    "cta_foto": b_cta_foto,
}


def build_html(copy: dict, brand: dict, out_dir: Path) -> str:
    css = (TEMPLATES / "carrusel_editorial_cinematografico.css").read_text(encoding="utf-8")
    logo_b64 = load_logo_b64(brand)
    logo_data_uri = f"data:image/png;base64,{logo_b64}"

    # Recolectar fotos: las del bloque "fotos" + las que cada slide especifique en "foto"
    all_fotos = dict(copy.get("fotos",{}))
    for i, s in enumerate(copy["slides"]):
        if s.get("foto"):
            all_fotos[f"_slide_{i}"] = s["foto"]
    fotos = copy_photo_assets(copy["cliente"], all_fotos, out_dir)

    slides_html = []
    for slide in copy["slides"]:
        tipo = slide["tipo"]
        builder = BUILDERS.get(tipo)
        if builder is None:
            raise ValueError(f"Tipo de slide desconocido: {tipo}")
        # Determinar args segun tipo. slide["foto"] override permite foto distinta por slide.
        if tipo == "hook_foto":
            slides_html.append(builder(slide, slide.get("foto") or fotos.get("hook","")))
        elif tipo == "showcase_foto":
            slides_html.append(builder(slide, slide.get("foto") or fotos.get("hook","")))
        elif tipo == "compare_arrow_foto":
            slides_html.append(builder(slide, slide.get("foto") or fotos.get("narrative","")))
        elif tipo == "problema_3puntos_foto":
            slides_html.append(builder(slide, slide.get("foto") or fotos.get("narrative","")))
        elif tipo == "cta_foto":
            slides_html.append(builder(slide, slide.get("foto") or fotos.get("cta",""), logo_data_uri))
        elif tipo in ("contexto_lead","dato_grande","stat_duo_chips","duo_indicador"):
            bg = slide.get("bg","bg-paper")
            slides_html.append(builder(slide, bg))
        else:
            slides_html.append(builder(slide))

    return f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8">
<title>{copy.get("pieza","Carrusel")} — {brand["brand_name"]}</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{css}</style>
</head><body>
{chr(10).join(slides_html)}
</body></html>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("copy_json", help="Path al JSON de copy")
    parser.add_argument("--prefix", default="slide", help="Prefix para los PNGs")
    args = parser.parse_args()

    copy_path = Path(args.copy_json).resolve()
    copy = json.loads(copy_path.read_text(encoding="utf-8"))

    brand = load_brand(copy["cliente"])

    out_dir = OUTPUT_BASE / copy["cliente"] / copy["fecha"] / copy["output_subdir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    html = build_html(copy, brand, out_dir)
    html_path = out_dir / f"{copy['pieza']}.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"OK HTML escrito: {html_path}")

    # Render con scripts/render.py
    render_script = ROOT / "scripts" / "render.py"
    cmd = [sys.executable, str(render_script), "--html", str(html_path), "--out", str(out_dir),
           "--width", "1080", "--height", "1080", "--prefix", args.prefix]
    print(f"Renderizando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
