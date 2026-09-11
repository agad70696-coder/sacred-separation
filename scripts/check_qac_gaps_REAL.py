#!/usr/bin/env python3
# check_qac_gaps_REAL.py - Real discovery: find gaps/errors in QAC source L0/L1
# English only - Sacred separation: L0 read only, report gaps
# Usage: python check_qac_gaps_REAL.py gold/gold_FULL_6236.jsonl

import json
import sys
from pathlib import Path

def load_jsonl(path):
    recs=[]
    with open(path,'r',encoding='utf-8') as f:
        for i, line in enumerate(f,1):
            line=line.strip()
            if not line:
                continue
            try:
                recs.append((i, json.loads(line)))
            except Exception as e:
                recs.append((i, {"_parse_error": str(e)}))
    return recs

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_qac_gaps_REAL.py gold/gold_FULL_6236.jsonl")
        sys.exit(1)
    gold_path = Path(sys.argv[1])
    records = load_jsonl(gold_path)
    missing_root = []
    missing_lemma = []
    missing_tag = []

    for lineno, r in records:
        if "_parse_error" in r:
            continue
        if not r.get('root'):
            missing_root.append(lineno)
        if not r.get('lemma'):
            missing_lemma.append(lineno)
        if not r.get('tag'):
            missing_tag.append(lineno)

    print(f"Missing root: {len(missing_root)}")
    print(f"Missing lemma: {len(missing_lemma)}")
    print(f"Missing tag: {len(missing_tag)}")

    out = Path("reports/qac_gaps.json")
    out.parent.mkdir(exist_ok=True)
    with open(out,'w',encoding='utf-8') as fw:
        json.dump({
            "missing_root_count": len(missing_root),
            "missing_lemma_count": len(missing_lemma),
            "missing_tag_count": len(missing_tag)
        }, fw, indent=2)
    print(f"Report saved to {out}")

if __name__ == "__main__":
    main()
