#!/usr/bin/env python3
# sort_surahs_by_complexity.py - Real discovery: which surahs break M10 and require M11
# English only - MDL based complexity: L(D|H) per surah
# Usage: python sort_surahs_by_complexity.py reports/mdl_full.json gold/gold_FULL_6236.jsonl

import json
import sys
from collections import defaultdict
from pathlib import Path

def load_jsonl(path):
    recs=[]
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except:
                continue
    return recs

def main():
    if len(sys.argv) < 3:
        print("Usage: python sort_surahs_by_complexity.py reports/mdl_full.json gold/gold_FULL_6236.jsonl")
        sys.exit(1)
    gold_path = Path(sys.argv[2])
    records = load_jsonl(gold_path)
    surah_stats = defaultdict(list)
    for r in records:
        surah = r.get('surah') or r.get('sura') or 0
        try:
            surah = int(surah)
        except:
            continue
        surah_stats[surah].append(r)

    complexity = []
    for surah_id, recs in sorted(surah_stats.items()):
        unique_roots = len(set(x.get('root','') for x in recs if x.get('root')))
        unique_lemmas = len(set(x.get('lemma','') for x in recs if x.get('lemma')))
        total = len(recs)
        score = (unique_roots + unique_lemmas) / max(1, total) * 100
        complexity.append({
            "surah": surah_id,
            "words": total,
            "unique_roots": unique_roots,
            "unique_lemmas": unique_lemmas,
            "complexity_score": round(score, 2)
        })

    complexity_sorted = sorted(complexity, key=lambda x: x["complexity_score"], reverse=True)

    print("\n=== TOP 20 MOST COMPLEX SURAHS (break M10, need M11) ===")
    for c in complexity_sorted[:20]:
        print(f"Surah {c['surah']:3d} | words={c['words']:4d} | roots={c['unique_roots']:4d} | lemmas={c['unique_lemmas']:4d} | score={c['complexity_score']}")

    out = Path("reports/surah_complexity.json")
    out.parent.mkdir(exist_ok=True)
    with open(out, 'w', encoding='utf-8') as fw:
        json.dump({"all": complexity_sorted}, fw, ensure_ascii=False, indent=2)
    print(f"\nReport saved to {out}")

if __name__ == "__main__":
    main()
