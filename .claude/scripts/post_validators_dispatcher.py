"""PostToolUse dispatcher: matches file path against patterns and suggests validators.

Reads Claude Code PostToolUse event JSON from stdin. Emits additionalContext
back to Claude with validator suggestions. For naming-validator on Meta Ads
CSVs, uses exit code 2 to make the suggestion blocking.

Mapping:
    **/guion_*.md, **/guiones/**/*.md   -> guion-validator + tono-brand-validator
    **/hooks_*.md, **/hook_*.md         -> hook-scorer + tono-brand-validator
    **/plan_campana*.md                 -> brief-pauta-validator + naming-validator --meta
    **/outputs/**/*.md (caption/copy)   -> tono-brand-validator
    agentes/04_pauta/**/campaigns_*.csv -> naming-validator --meta (BLOCKING)
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import sys
from pathlib import Path

CACHE_PATH = Path(".claude/state/validator_cache.json")


def load_cache() -> dict:
    if not CACHE_PATH.exists():
        return {}
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def file_hash(path: str) -> str | None:
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()
    except Exception:
        return None


# (glob_pattern, [validators], blocking)
RULES: list[tuple[str, list[str], bool]] = [
    ("**/guion_*.md", ["guion-validator", "tono-brand-validator"], False),
    ("**/guiones/**/*.md", ["guion-validator", "tono-brand-validator"], False),
    ("**/hooks_*.md", ["hook-scorer", "tono-brand-validator"], False),
    ("**/hook_*.md", ["hook-scorer", "tono-brand-validator"], False),
    ("**/plan_campana*.md", ["brief-pauta-validator", "naming-validator --meta"], False),
    ("**/outputs/**/caption*.md", ["tono-brand-validator"], False),
    ("**/outputs/**/copy*.md", ["tono-brand-validator"], False),
    ("agentes/04_pauta/**/campaigns_*.csv", ["naming-validator --meta"], True),
    ("agentes/04_pauta/**/campaigns_*.tsv", ["naming-validator --meta"], True),
]


def matches(path: str, pattern: str) -> bool:
    norm = path.replace("\\", "/")
    return fnmatch.fnmatch(norm, pattern) or fnmatch.fnmatch(norm, f"**/{pattern}")


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = event.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path") or tool_input.get("path") or ""
    if not file_path:
        return 0

    rel = file_path
    try:
        rel = str(Path(file_path).resolve().relative_to(Path.cwd().resolve())).replace("\\", "/")
    except Exception:
        pass

    matched: list[tuple[list[str], bool]] = []
    for pattern, validators, blocking in RULES:
        if matches(rel, pattern):
            matched.append((validators, blocking))

    if not matched:
        return 0

    blocking_any = any(b for _, b in matched)
    all_validators = sorted({v for vs, _ in matched for v in vs})

    # Dedupe nivel 1: si este archivo + set de validators ya se sugirio para este hash, skip.
    h = file_hash(file_path)
    if h:
        cache = load_cache()
        key = rel
        prev = cache.get(key, {})
        sig = f"{h}:{','.join(all_validators)}"
        if prev.get("sig") == sig:
            return 0
        cache[key] = {"sig": sig, "hash": h}
        save_cache(cache)

    msg_lines = [
        f"Validadores sugeridos para `{rel}`:",
        *[f"  - {v}" for v in all_validators],
    ]
    if blocking_any:
        msg_lines.append("")
        msg_lines.append("HARD GATE: corre naming-validator antes de cualquier handoff/push a Meta.")
        print("\n".join(msg_lines), file=sys.stderr)
        return 2

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": "\n".join(msg_lines),
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
