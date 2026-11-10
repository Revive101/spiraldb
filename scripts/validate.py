#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema>=4.23,<5"]
# ///
"""Validate every data file against its JSON Schema. Usage: scripts/validate.py [paths...]"""
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
# directory -> schema (matched by longest prefix, so subdirs can override)
MAP = {
    "BadgeDefinitions": "badge-definition",
    "CreatureSpellbook": "creature-spellbook",
    "CrownShop": "crown-shop-tab",
    "DropTables": "drop-table",
    "GlobalRegistry": "global-registry",
    "NpcBank": "npc-bank",
    "NpcDropTable": "npc-drop-table",
    "NpcInventory": "npc-inventory",
    "NpcSeamstress": "npc-seamstress",
    "NpcSpellInventory": "npc-spell-inventory",
    "PlayerStatues": "player-statue",
    "QuestTemplates": "quest-template",
    "QuestTemplates/droptables": "drop-table",
    "TreasureCardInventory": "treasure-card-inventory",
    "ZoneTransfer": "zone-transfer",
}
validators = {}
def validator(name):
    if name not in validators:
        schema = json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text())
        Draft202012Validator.check_schema(schema)
        validators[name] = Draft202012Validator(schema)
    return validators[name]

def schema_for(rel):
    best = max((d for d in MAP if rel.startswith(d + "/")), key=len, default=None)
    return MAP[best] if best else None

def main(args):
    files = [Path(a).resolve() for a in args] if args else sorted(
        p for d in MAP for p in (ROOT / d).rglob("*.json"))
    files = sorted(set(files))
    failures = checked = 0
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        name = schema_for(rel)
        if not name:
            continue
        checked += 1
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError) as e:
            print(f"::error file={rel}::invalid JSON: {e}"); failures += 1; continue
        for err in sorted(validator(name).iter_errors(data), key=lambda e: list(e.absolute_path)):
            loc = "/".join(map(str, err.absolute_path)) or "(root)"
            print(f"::error file={rel}::{loc}: {err.message[:200]}"); failures += 1
    print(f"checked {checked} files, {failures} problem(s)")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
