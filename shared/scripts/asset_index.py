"""
asset_index.py — Indice cross-agent de outputs de todos los agentes DV.

Indexa:
    agentes/01_contenido/creative_director/outputs/<cliente>/<fecha>/*.md
    agentes/01_contenido/copywritter/outputs/<cliente>/<fecha>/*.md
    agentes/01_contenido/design/output/<cliente>/<fecha>/*.png   (solo metadata)
    agentes/04_pauta/outputs/<cliente>/<fecha>/*.md

Persiste en shared/state/asset_index.sqlite con FTS5 sobre titulo+contenido.

Uso CLI:
    python asset_index.py index                            # rebuild
    python asset_index.py search "captacion zona norte"    # FTS query
    python asset_index.py search --cliente toribio_achaval --tipo guion "balcon"
    python asset_index.py recent --cliente ini_propiedades 10
"""

from __future__ import annotations

import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "shared" / "state" / "asset_index.sqlite"

SOURCES = [
    ("creative_director", ROOT / "agentes" / "01_contenido" / "creative_director" / "outputs", ".md"),
    ("copywritter",       ROOT / "agentes" / "01_contenido" / "copywritter" / "outputs", ".md"),
    ("design",            ROOT / "agentes" / "01_contenido" / "design" / "output", ".png"),
    ("pauta",             ROOT / "agentes" / "04_pauta" / "outputs", ".md"),
]

PATH_RE = re.compile(r"/([^/]+)/(\d{4}-\d{2}-\d{2})/(.+?)$")


def _classify_tipo(filename: str) -> str:
    f = filename.lower()
    for prefix in ("guion", "brief_carrusel", "estrategia", "meta_ad", "caption",
                   "banco_hooks", "estrategia_copy", "plan_campana", "analisis",
                   "reporte_semanal", "reporte_mensual", "brief_creativo",
                   "brief_diseno", "alerta_daily"):
        if f.startswith(prefix):
            return prefix
    return "otro"


def _connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS assets USING fts5(
            agente, cliente, fecha, tipo, filename, path, content,
            tokenize='unicode61 remove_diacritics 1'
        )
    """)
    return con


def index_all() -> dict:
    con = _connect()
    con.execute("DELETE FROM assets")
    n = 0
    by_agente = {}
    for agente, base, ext in SOURCES:
        if not base.exists():
            continue
        for f in base.rglob(f"*{ext}"):
            rel = str(f.relative_to(ROOT)).replace("\\", "/")
            m = PATH_RE.search("/" + rel)
            if not m:
                continue
            cliente, fecha, tail = m.group(1), m.group(2), m.group(3)
            filename = f.name
            tipo = _classify_tipo(filename)
            content = ""
            if ext == ".md":
                try:
                    content = f.read_text(encoding="utf-8")[:8000]
                except Exception:
                    content = ""
            con.execute(
                "INSERT INTO assets(agente, cliente, fecha, tipo, filename, path, content) VALUES(?,?,?,?,?,?,?)",
                (agente, cliente, fecha, tipo, filename, rel, content),
            )
            n += 1
            by_agente[agente] = by_agente.get(agente, 0) + 1
    con.commit()
    con.close()
    return {"total": n, "by_agente": by_agente}


def _build_where(cliente: str | None, tipo: str | None, agente: str | None) -> tuple[str, list]:
    parts, args = [], []
    if cliente:
        parts.append("cliente MATCH ?")
        args.append(cliente)
    if tipo:
        parts.append("tipo MATCH ?")
        args.append(tipo)
    if agente:
        parts.append("agente MATCH ?")
        args.append(agente)
    where = " AND ".join(parts)
    return where, args


def search(query: str, cliente: str | None = None, tipo: str | None = None, agente: str | None = None, limit: int = 15) -> list[dict]:
    con = _connect()
    parts, args = [], []
    if query:
        parts.append("content MATCH ?")
        args.append(query)
    if cliente:
        parts.append("cliente = ?"); args.append(cliente)
    if tipo:
        parts.append("tipo = ?"); args.append(tipo)
    if agente:
        parts.append("agente = ?"); args.append(agente)
    where = " AND ".join(parts) if parts else "1=1"
    sql = f"""
        SELECT agente, cliente, fecha, tipo, filename, path,
               snippet(assets, 6, '[', ']', '...', 12) AS preview
        FROM assets
        WHERE {where}
        ORDER BY fecha DESC
        LIMIT {limit}
    """
    rows = con.execute(sql, args).fetchall()
    con.close()
    return [
        {"agente": r[0], "cliente": r[1], "fecha": r[2], "tipo": r[3],
         "filename": r[4], "path": r[5], "preview": r[6]}
        for r in rows
    ]


def recent(cliente: str | None = None, limit: int = 20) -> list[dict]:
    con = _connect()
    if cliente:
        rows = con.execute(
            "SELECT agente,cliente,fecha,tipo,filename,path FROM assets WHERE cliente=? ORDER BY fecha DESC LIMIT ?",
            (cliente, limit),
        ).fetchall()
    else:
        rows = con.execute(
            "SELECT agente,cliente,fecha,tipo,filename,path FROM assets ORDER BY fecha DESC LIMIT ?",
            (limit,),
        ).fetchall()
    con.close()
    return [
        {"agente": r[0], "cliente": r[1], "fecha": r[2], "tipo": r[3], "filename": r[4], "path": r[5]}
        for r in rows
    ]


def _print_results(rows: list[dict]) -> None:
    if not rows:
        print("(sin resultados)")
        return
    for r in rows:
        print(f"  [{r['fecha']}] {r['cliente']:20s} {r['tipo']:18s} {r['filename']}")
        print(f"      {r['path']}")
        if r.get("preview"):
            print(f"      ...{r['preview'][:200]}...")


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    cmd = argv[0]

    def _flag(name: str) -> str | None:
        if name in argv:
            i = argv.index(name)
            if i + 1 < len(argv):
                return argv[i + 1]
        return None

    if cmd == "index":
        r = index_all()
        print(f"Indexados: {r['total']}")
        for a, c in r["by_agente"].items():
            print(f"  {a}: {c}")
        return 0

    if cmd == "search":
        cliente = _flag("--cliente")
        tipo = _flag("--tipo")
        agente = _flag("--agente")
        # query es lo ultimo no-flag
        query_args = [a for i, a in enumerate(argv[1:], 1) if not a.startswith("--") and argv[i - 1] not in ("--cliente", "--tipo", "--agente")]
        query = " ".join(query_args).strip()
        rows = search(query, cliente=cliente, tipo=tipo, agente=agente)
        _print_results(rows)
        return 0

    if cmd == "recent":
        cliente = _flag("--cliente")
        try:
            limit = int(argv[-1]) if argv[-1].isdigit() else 20
        except Exception:
            limit = 20
        rows = recent(cliente=cliente, limit=limit)
        _print_results(rows)
        return 0

    print(f"Comando desconocido: {cmd}")
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
