"""
followup_drafts.py — Drafts de primer contacto WA para leads sin trabajar.

Para cada lead en pipeline con prescore_priority IN (1, 2) y sin sentinel
.followup_drafted, escribe un draft markdown a:

    agentes/02_comercial/outputs/digital_view/<fecha>/followup_<id>.md

El draft NO se manda automaticamente. Queda listo para que Valentin lo revise,
ajuste con info especifica, y mande por WA. Pasa por auto_approve para validar
tono DV antes de mostrarlo (sidecar status.json al lado).

NO genera drafts para leads con prescore_knockouts (zona fuera, presupuesto
bajo, etc.) — esos requieren decision humana de Valentin.
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PIPELINE = ROOT / "agentes" / "02_comercial" / "data" / "pipeline.json"
OUTPUTS = ROOT / "agentes" / "02_comercial" / "outputs" / "digital_view"
AUTO_APPROVE = ROOT / ".claude" / "scripts" / "auto_approve.py"

TEMPLATE = """# Followup draft — {nombre_o_empresa}

**Lead ID:** {lead_id}
**Fuente:** {fuente}
**Prioridad:** {priority}
**Generado:** {ts}

---

## Mensaje WA sugerido (revisar y ajustar antes de mandar)

Hola{coma_nombre}, soy Valentin de Digital View.

Te llego tu consulta desde Instagram. Trabajamos con inmobiliarias y top producers de CABA y Zona Norte armandoles un sistema propio de captacion de prospectos: contenido + pauta en Meta + CRM.

Para no hacerte perder tiempo, te tiro las dos preguntas que definen si tiene sentido seguir hablando:

1. ¿Estas operando hoy en CABA o Zona Norte?
2. ¿Tenes capacidad de invertir desde USD 800/mes en pauta (aparte del fee de la agencia)?

Si las dos son si, agendamos 20 minutos esta semana y vemos si tiene fit. Si alguna es no, te lo digo de una y no te robo tiempo.

---

## Notas internas (no van al lead)

- {prescore_source} — entro {fecha_ingreso}
- Red flags detectados: {red_flags}
- Knockouts detectados: {knockouts}

Va para Valentin. Proximo paso: revisar, agregar nombre real si lo conoces, y mandar por WA.
"""


def _ensure_sidecar(draft_path: Path) -> None:
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("auto_approve", AUTO_APPROVE)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cliente = "digital_view"
        fecha = draft_path.parts[-2]
        mod.run(cliente, fecha, False)
    except Exception:
        pass


def _draft_for(p: dict) -> str:
    nombre = (p.get("nombre") or "").strip()
    empresa = (p.get("empresa") or "").strip()
    nombre_o_empresa = nombre if nombre and nombre.lower() != "sin nombre" else (empresa or f"Lead {p.get('id', '?')}")
    coma_nombre = f" {nombre.split()[0]}" if nombre and nombre.lower() != "sin nombre" else ""
    flags = p.get("prescore_red_flags") or []
    kos = p.get("prescore_knockouts") or []
    return TEMPLATE.format(
        nombre_o_empresa=nombre_o_empresa,
        lead_id=p.get("id", "?"),
        fuente=p.get("fuente", "?"),
        priority=p.get("prescore_priority", "?"),
        ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        coma_nombre=coma_nombre,
        prescore_source=p.get("prescore_source", "?"),
        fecha_ingreso=p.get("fecha_ingreso", "?"),
        red_flags=", ".join(flags) or "ninguno",
        knockouts=", ".join(kos) or "ninguno",
    )


def run(dry_run: bool = False) -> dict:
    if not PIPELINE.exists():
        return {"status": "no_pipeline", "drafted": 0}
    data = json.loads(PIPELINE.read_text(encoding="utf-8"))
    fecha = date.today().isoformat()
    out_dir = OUTPUTS / fecha
    drafted = 0
    skipped_done = 0
    skipped_ko = 0
    skipped_low_prio = 0

    for p in data.get("prospectos", []):
        if p.get("etapa") not in ("pre_filtro", "fit_call"):
            continue
        prio = p.get("prescore_priority")
        if prio not in (1, 2):
            skipped_low_prio += 1
            continue
        if p.get("prescore_knockouts"):
            skipped_ko += 1
            continue
        if p.get("followup_drafted_at"):
            skipped_done += 1
            continue

        draft_path = out_dir / f"followup_{p['id']}.md"
        if draft_path.exists():
            skipped_done += 1
            continue

        if dry_run:
            print(f"[DRY] {draft_path.relative_to(ROOT)}")
            drafted += 1
            continue

        out_dir.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(_draft_for(p), encoding="utf-8")
        p["followup_drafted_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        p["followup_draft_path"] = str(draft_path.relative_to(ROOT)).replace("\\", "/")
        drafted += 1
        _ensure_sidecar(draft_path)

    if drafted and not dry_run:
        PIPELINE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "drafted": drafted,
        "skipped_already_drafted": skipped_done,
        "skipped_knockouts": skipped_ko,
        "skipped_low_priority": skipped_low_prio,
        "fecha": fecha,
        "dry_run": dry_run,
    }


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    r = run(dry_run=dry)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
