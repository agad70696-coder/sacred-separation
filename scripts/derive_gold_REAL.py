import json, re
from pathlib import Path
from collections import defaultdict

QAC = Path.home() / "apex44-zero/PHASE2_CLEAN/source/quranic-corpus-morphology-0.4.txt"
OUT = Path("gold/gold_01_85.jsonl")
OUT_DERIVED = Path("gold/gold_01_85_DERIVED_from_QAC.jsonl")

# Parse full QAC morphology 0.4: (1:1:1:1) FORM TAG FEATURES
ayah_tokens = defaultdict(list) # ayah -> list of (form, pos, root, lemma)

pattern = re.compile(r'\(?(\d+):(\d+):(\d+):(\d+)\)?')

with open(QAC, encoding='utf-8', errors='ignore') as f:
    for line in f:
        if not line.strip() or line.startswith('#'): continue
        m = pattern.search(line)
        if not m: continue
        sura, aya = m.group(1), m.group(2)
        ayah = f"{sura}:{aya}"

        # Typical line: (1:1:1:1) bi PREFIX|bi+ or (1:1:1:2) somi STEM|POS:N|LEM:...
        parts = line.strip().split('\t')
        if len(parts) < 2:
            parts = line.strip().split()
        form = parts[1] if len(parts) > 1 else ""
        tag_feat = " ".join(parts[2:]) if len(parts) > 2 else ""

        pos = "UNK"
        root = "UNK"
        lem = ""
        if "POS:" in tag_feat:
            pos = re.search(r'POS:([A-Z]+)', tag_feat)
            pos = pos.group(1) if pos else "UNK"
        if "ROOT:" in tag_feat:
            root = re.search(r'ROOT:([^\|\s]+)', tag_feat)
            root = root.group(1) if root else "UNK"
        if "LEM:" in tag_feat:
            lem = re.search(r'LEM:([^\|\s]+)', tag_feat)
            lem = lem.group(1) if lem else ""

        ayah_tokens[ayah].append({"form": form, "pos": pos, "root": root, "lem": lem})

sorted_ayahs = sorted(ayah_tokens.keys(), key=lambda k: tuple(map(int, k.split(':'))))[:85]

with open(OUT, 'w', encoding='utf-8') as out:
    for i, ayah in enumerate(sorted_ayahs, 1):
        toks = ayah_tokens[ayah]
        first = toks[0]
        # REAL mapping: domain = POS, family = ROOT (instead of DERIVED placeholders)
        # entry = Buckwalter first form (speech_to_entry true per M6)
        rec = {
            "construction_id": f"c{i:03d}",
            "ayah": ayah,
            "domain": first["pos"], # REAL: N, V, P, etc not DERIVED_QAC
            "entry": first["form"], # REAL Buckwalter bi, {lo - clausal unification
            "family": first["root"], # REAL: root like smw, etc not DERIVED_FAMILY
            "parent_id": None,
            "slot": 0,
            "span": f"{ayah}:1-{len(toks)}",
            "lemma": first["lem"],
            "qac_features": f"POS:{first['pos']}|ROOT:{first['root']}"
        }
        out.write(json.dumps(rec, ensure_ascii=False)+"\n")

print(f"Wrote REAL gold {OUT} {len(sorted_ayahs)} records")
print(f"Sample domain/family: {ayah_tokens['1:1'][0]}")
