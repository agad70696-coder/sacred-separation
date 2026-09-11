#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "gold" / "gold_01_85.jsonl"

REQUIRED = {
    "construction_id",
    "ayah",
    "parent_id",
    "family",
    "domain",
    "entry",
    "slot",
    "span"
}


def main() -> int:
    if not PATH.exists():
        print(f"BLOCKED: missing {PATH}")
        return 2

    count = 0
    ids = set()

    with PATH.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue

            try:
                obj = json.loads(line)
            except Exception as exc:
                print(
                    f"BLOCKED: invalid JSON at line {line_no}: {exc}"
                )
                return 2

            missing = REQUIRED - set(obj)

            if missing:
                print(
                    f"BLOCKED: line {line_no} missing {sorted(missing)}"
                )
                return 2

            cid = obj["construction_id"]

            if cid in ids:
                print(
                    f"BLOCKED: duplicate construction_id: {cid}"
                )
                return 2

            ids.add(cid)
            count += 1

    if count == 0:
        print("BLOCKED: Gold dataset is empty")
        return 2

    print(f"PASS: Gold records={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
