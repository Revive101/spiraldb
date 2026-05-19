#!/usr/bin/env python3
"""
Recursively walk a directory tree, load every .json file,
strip the top-level '@metadata' key, and write back with
consistent formatting (2-space indent, trailing newline).
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def process_file(path: str) -> bool:
    """Remove '@metadata' from a JSON file. Returns True if modified."""
    with open(path, "r", encoding="utf-8") as fh:
        try:
            data = json.load(fh)
        except json.JSONDecodeError as exc:
            print(f"  SKIP: invalid JSON — {exc}")
            return False

    if not isinstance(data, dict):
        return False

    if "@metadata" not in data:
        return False

    del data["@metadata"]

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    return True


def main():
    modified = 0
    skipped = 0

    for dirpath, _, filenames in os.walk(ROOT):
        for name in filenames:
            if not name.lower().endswith(".json"):
                continue

            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, ROOT)
            try:
                if process_file(full):
                    modified += 1
                    print(f"  OK  {rel}")
                else:
                    skipped += 1
            except OSError as exc:
                print(f"  ERR {rel}: {exc}")

    print(f"\nDone. {modified} file(s) modified, {skipped} skipped (no @metadata or non-dict).")


if __name__ == "__main__":
    main()
