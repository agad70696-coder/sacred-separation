#!/usr/bin/env python3
# analyze_domains_REAL.py - Real discovery: domain/family distribution in gold
# English only - L0 sacred source is never modified, only L1 gold is read
# Usage: python analyze_domains_REAL.py gold/gold_FULL_6236.jsonl

import json
import sys
from collections import Counter
from pathlib import Path

def load_jsonl(path):
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except:
                continue
    return records

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_domains_REAL.py gold/gold_FULL_6236.jsonl")
        sys.exit(1)
    gold_path = Path(sys.argv[1])
    if not gold_path.exists():
        print(f"File not found: {gold_path}")
        sys.exit(1)

    records = load_jsonl(gold_path)
    print(f"Loaded {len(records)} records from {gold_path}")

    domain_counter = Counter()
    family_counter = Counter()
    pos_counter = Counter()
    root_counter = Counter()
    lemma_counter = Counter()

    for r in records:
        tag = r.get('tag') or r.get('pos') or r.get('morphology') or ''
        domain = r.get('domain') or r.get('pos_type') or str(tag).split(':')[0] if tag else 'UNKNOWN'
        family = r.get('family') or r.get('pattern') or r.get('form_type') or 'UNKNOWN'
        domain_counter[domain] += 1
        family_counter[family] += 1
        if 'tag' in r:
            pos_counter[r['tag']] += 1
        if 'root' in r and r['root']:
            root_counter[r['root']] += 1
        if 'lemma' in r and r['lemma']:
            lemma_counter[r['lemma']] += 1

    print("\n=== DOMAIN DISTRIBUTION (L1) ===")
    for dom, cnt in domain_counter.most_common(20):
        print(f"{dom}: {cnt}")

    print("\n=== FAMILY/PATTERN DISTRIBUTION (L1) ===")
    for fam, cnt in family_counter.most_common(20):
        print(f"{fam}: {cnt}")

    print("\n=== POS TAG DISTRIBUTION ===")
    for tag, cnt in pos_counter.most_common(30):
        print(f"{tag}: {cnt}")

    print(f"\nUnique roots: {len(root_counter)}")
    print(f"Unique lemmas: {len(lemma_counter)}")

    hapax_roots = [root for root, c in root_counter.items() if c == 1]
    print(f"\nHapax roots (appear once): {len(hapax_roots)}")
    print("Examples:", hapax_roots[:20])

    out = Path("reports/domain_analysis.json")
    out.parent.mkdir(exist_ok=True)
    report = {
        "total_records": len(records),
        "domains": dict(domain_counter),
        "families": dict(family_counter),
        "pos": dict(pos_counter.most_common(100)),
        "unique_roots": len(root_counter),
        "unique_lemmas": len(lemma_counter),
        "hapax_roots_count": len(hapax_roots),
        "hapax_roots_sample": hapax_roots[:100]
    }
    with open(out, 'w', encoding='utf-8') as fw:
        json.dump(report, fw, ensure_ascii=False, indent=2)
    print(f"\nReport saved to {out}")

if __name__ == "__main__":
    main()
