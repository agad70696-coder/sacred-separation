import json, os, re
from pathlib import Path
from collections import defaultdict

QAC = Path(os.path.expanduser("~/apex44-zero/PHASE2_CLEAN/source/quranic-corpus-morphology-0.4.txt"))
OUT_DERIVED = Path("gold/gold_01_85_DERIVED_from_QAC.jsonl")
OUT_GOLD = Path("gold/gold_01_85.jsonl")

ayah_map = defaultdict(list)
lines=0
data_lines=0

with open(QAC, encoding='utf-8', errors='ignore') as f:
    for raw in f:
        lines+=1
        line=raw.strip()
        if not line or line.startswith('#'):
            continue
        data_lines+=1
        sura=aya=None
        form=""

        # Format 1: Tanzil pipe 1|1|بسم...
        if '|' in line:
            parts=line.split('|')
            if len(parts)>=3 and parts[0].strip().isdigit() and parts[1].strip().isdigit():
                sura=parts[0].strip()
                aya=parts[1].strip()
                text=parts[2].strip()
                form=text.split()[0] if text else ""

        # Format 2: QAC (1:1:1:1) or 1:1:1
        if not sura:
            m=re.search(r'\(?(\d+):(\d+):(\d+)', line)
            if m:
                sura=m.group(1)
                aya=m.group(2)
                # try to get form
                if '\t' in line:
                    form=line.split('\t')[1] if len(line.split('\t'))>1 else ""
                else:
                    sp=line.split()
                    form=sp[1] if len(sp)>1 else ""

        if sura and aya:
            ayah_key=f"{sura}:{aya}"
            ayah_map[ayah_key].append(form if form else "FORM")

print(f"Total lines {lines}, data {data_lines}, unique ayat {len(ayah_map)}")

sorted_ayahs = sorted(ayah_map.keys(), key=lambda k: tuple(map(int, k.split(':'))))[:85]
print(f"Using {len(sorted_ayahs)} ayat")

OUT_DERIVED.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_DERIVED,'w',encoding='utf-8') as out:
    for i, ayah in enumerate(sorted_ayahs, 1):
        toks=ayah_map[ayah]
        rec={
            "construction_id": f"c{i:03d}",
            "ayah": ayah,
            "domain": "DERIVED_QAC",
            "entry": toks[0] if toks else "",
            "family": "DERIVED_FAMILY",
            "parent_id": None,
            "slot": 0,
            "span": f"{ayah}:1-{len(toks)}"
        }
        out.write(json.dumps(rec, ensure_ascii=False)+"\n")

import shutil
shutil.copyfile(OUT_DERIVED, OUT_GOLD)
print(f"Wrote {OUT_DERIVED} and {OUT_GOLD} - {len(sorted_ayahs)} records")
