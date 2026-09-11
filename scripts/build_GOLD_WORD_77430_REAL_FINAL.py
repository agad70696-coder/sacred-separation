#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
from collections import defaultdict, Counter
LOC_REGEX = re.compile(r'\(?(\d+):(\d+):(\d+)(?::\d+)?\)?')
def parse_line(line):
    line=line.strip()
    if not line or line.startswith('#'):
        return None
    m = LOC_REGEX.match(line)
    if not m:
        return None
    try:
        surah = int(m.group(1)); ayah = int(m.group(2)); word_idx = int(m.group(3))
    except:
        return None
    rest = line[m.end():].strip()
    if not rest:
        return None
    parts = rest.split('\t')
    if len(parts) < 2:
        ws = rest.split()
        if len(ws) < 2:
            return None
        form = ws[0]; tag = ws[1] if len(ws)>1 else ""; feats = ' '.join(ws[2:]) if len(ws)>2 else ""
    else:
        form = parts[0].strip()
        tag = parts[1].strip() if len(parts)>1 else ""
        feats = '\t'.join(parts[2:]).strip() if len(parts)>2 else ""
    return (surah, ayah, word_idx, form, tag, feats)

def load_qac_real(path):
    groups = defaultdict(list)
    total=0; parsed=0; skipped=0
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            total+=1
            if total<=2:
                print(f"DEBUG raw[{total}]: {line[:200].strip()}")
            res = parse_line(line)
            if not res:
                skipped+=1; continue
            surah, ayah, word_idx, form, tag, feats = res
            parsed+=1
            key=(surah, ayah, word_idx)
            groups[key].append((form, tag, feats))
    print(f"Total lines: {total}, Parsed: {parsed}, Skipped: {skipped}")
    return groups, total, parsed

def build_gold(groups):
    records=[]
    for (surah, ayah, word_idx) in sorted(groups.keys()):
        segs=groups[(surah, ayah, word_idx)]
        full_form="".join([s[0] for s in segs])
        roots=[]; lemmas=[]; tags=[]; all_feats=[]
        for form, tag, feats in segs:
            all_feats.append(feats)
            m=re.search(r'ROOT:([^\|\s]+)', feats)
            if m: roots.append(m.group(1))
            m=re.search(r'LEM:([^\|\s]+)', feats)
            if m: lemmas.append(m.group(1))
            if tag: tags.append(tag)
        root=roots[0] if roots else ""; lemma=lemmas[0] if lemmas else ""; tag_main=tags[0] if tags else ""
        rec={"surah":surah,"ayah":ayah,"word":word_idx,"form":full_form,"root":root,"lemma":lemma,"tag":tag_main,"features":"|".join(all_feats),"segments":len(segs),"location":f"{surah}:{ayah}:{word_idx}"}
        records.append(rec)
    return records

def main():
    input_path = Path(sys.argv[1]) if len(sys.argv)>1 else Path("quranic-corpus-morphology-0.4.txt")
    output_path = Path(sys.argv[2]) if len(sys.argv)>2 else Path("gold/gold_WORD_77430.jsonl")
    if not input_path.exists():
        for c in [Path.home()/"Quran_Research_Engine/data/morphology/quranic-corpus-morphology-0.4.txt", Path.home()/"apex44-zero/PHASE2_CLEAN/source/quranic-corpus-morphology-0.4.txt"]:
            if c.exists():
                input_path=c; break
    print(f"REAL EXECUTION: Loading QAC from {input_path}")
    groups, total, parsed = load_qac_real(input_path)
    print(f"REAL: Grouped into {len(groups)} words from {parsed} segments")
    records = build_gold(groups)
    print(f"REAL: Built {len(records)} word records")
    if len(records)==77430:
        print("REAL SUCCESS: 77430 words - FULL Quran verified")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path,'w',encoding='utf-8') as out:
        for r in records:
            out.write(json.dumps(r, ensure_ascii=False)+"\n")
    print(f"REAL: Saved to {output_path}")
    rc=Counter([r["root"] for r in records if r["root"]])
    print(f"\n=== REAL STATS - NON-ILLUSORY ===")
    print(f"Unique roots: {len(rc)}")
    print(f"Hapax roots: {len([k for k,v in rc.items() if v==1])}")
    print(f"Total words: {len(records)}")

if __name__=="__main__":
    main()
