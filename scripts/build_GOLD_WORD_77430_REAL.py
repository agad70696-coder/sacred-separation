#!/usr/bin/env python3
# build_GOLD_WORD_77430_REAL.py - Build real word-level gold 77430 from QAC morphology
# English only - L0 sacred source read only, L1 gold derived
# Input: quranic-corpus-morphology-0.4.txt
# Output: gold/gold_WORD_77430.jsonl with 8 fields per word

import json
import sys
import re
from pathlib import Path
from collections import defaultdict, Counter

def parse_features(feat_str):
    root = ""
    lemma = ""
    pos = ""
    if not feat_str:
        return root, lemma, pos, feat_str
    m = re.search(r'ROOT:([^\|\s]+)', feat_str)
    if m:
        root = m.group(1)
    m = re.search(r'LEM:([^\|\s]+)', feat_str)
    if m:
        lemma = m.group(1)
    m = re.search(r'POS:([^\|\s]+)', feat_str)
    if m:
        pos = m.group(1)
    else:
        parts = feat_str.strip().split()
        if parts and ':' not in parts[0] and '|' not in parts[0]:
            pos = parts[0]
    return root, lemma, pos, feat_str

def load_qac(path):
    groups = defaultdict(list)
    total_lines = 0
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'):
                continue
            total_lines += 1
            parts = line.split('\t')
            if len(parts) < 3:
                parts = line.split()
                if len(parts) >= 4:
                    loc = parts[0]
                    form = parts[1]
                    tag = parts[2]
                    feats = ' '.join(parts[3:])
                else:
                    continue
            else:
                loc = parts[0].strip()
                form = parts[1].strip() if len(parts) > 1 else ""
                tag = parts[2].strip() if len(parts) > 2 else ""
                feats = parts[3].strip() if len(parts) > 3 else ""
                if len(parts) > 4:
                    feats = '\t'.join(parts[3:])
            loc_parts = loc.split(':')
            if len(loc_parts) < 3:
                continue
            try:
                surah = int(loc_parts[0])
                ayah = int(loc_parts[1])
                word_idx = int(loc_parts[2])
            except:
                continue
            key = (surah, ayah, word_idx)
            groups[key].append({
                "form_seg": form,
                "tag_seg": tag,
                "feat_seg": feats,
                "loc": loc
            })
    return groups, total_lines

def build_word_gold(groups):
    records = []
    for (surah, ayah, word_idx) in sorted(groups.keys()):
        segs = groups[(surah, ayah, word_idx)]
        forms = [s["form_seg"] for s in segs if s["form_seg"]]
        full_form = "".join(forms) if forms else ""
        roots = []
        lemmas = []
        pos_tags = []
        all_features = []
        for s in segs:
            r, l, p, feat = parse_features(s["feat_seg"])
            if r:
                roots.append(r)
            if l:
                lemmas.append(l)
            if p:
                pos_tags.append(p)
            elif s["tag_seg"]:
                pos_tags.append(s["tag_seg"])
            all_features.append(s["feat_seg"])
        root = roots[0] if roots else ""
        lemma = lemmas[0] if lemmas else ""
        tag = pos_tags[0] if pos_tags else ""
        features = "|".join([f for f in all_features if f])
        rec = {
            "surah": surah,
            "ayah": ayah,
            "word": word_idx,
            "form": full_form,
            "root": root,
            "lemma": lemma,
            "tag": tag,
            "features": features,
            "segments": len(segs),
            "location": f"{surah}:{ayah}:{word_idx}"
        }
        records.append(rec)
    return records

def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("quranic-corpus-morphology-0.4.txt")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("gold/gold_WORD_77430.jsonl")
    if not input_path.exists():
        for c in [Path("data/quranic-corpus-morphology-0.4.txt"), Path("./quranic-corpus-morphology-0.4.txt")]:
            if c.exists():
                input_path = c
                break
    if not input_path.exists():
        print(f"Input not found: {input_path}")
        sys.exit(1)
    print(f"Loading QAC from {input_path}")
    groups, total_lines = load_qac(input_path)
    print(f"Read {total_lines} segment lines")
    print(f"Grouped into {len(groups)} words")
    records = build_word_gold(groups)
    print(f"Built {len(records)} word records")
    if len(records) == 77430:
        print("Perfect: 77430 words - FULL Quran")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out:
        for r in records:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Saved to {output_path}")
    roots = [r["root"] for r in records if r["root"]]
    lemmas = [r["lemma"] for r in records if r["lemma"]]
    rc = Counter(roots)
    lc = Counter(lemmas)
    hapax_roots = [k for k,v in rc.items() if v==1]
    print(f"\n=== REAL STATS ===")
    print(f"Unique roots: {len(rc)}")
    print(f"Unique lemmas: {len(lc)}")
    print(f"Hapax roots: {len(hapax_roots)}")
    print(f"Sample hapax roots: {hapax_roots[:10]}")

if __name__ == "__main__":
    main()
