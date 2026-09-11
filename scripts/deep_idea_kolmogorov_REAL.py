import json
from collections import Counter, defaultdict

gold="gold/gold_WORD_77430.jsonl"
records=[json.loads(l) for l in open(gold, encoding='utf-8')]
rc=Counter([r["root"] for r in records if r["root"]])
hapax={k for k,v in rc.items() if v==1}

# Deep idea: which surahs have ZERO hapax = fully compressible core
by_surah=defaultdict(list)
for r in records:
    by_surah[r["surah"]].append(r)

core=[]; innovative=[]
for surah in range(1,115):
    recs=by_surah[surah]
    h_count=sum(1 for r in recs if r["root"] in hapax)
    if h_count==0:
        core.append(surah)
    else:
        innovative.append((surah, h_count))

print(f"REAL DEEP IDEA:")
print(f"Core fully compressible (0 hapax): {len(core)} surahs")
print(f"Core list: {core}")
print(f"Innovative (has hapax): {len(innovative)} surahs")
print(f"\nTop innovative:")
for s,c in sorted(innovative, key=lambda x: x[1], reverse=True)[:10]:
    print(f"Surah {s:3d}: {c} hapax - incompressible information")

# This is M12 theory: TOTAL = L(common) + L(hapax) where L(hapax) is incompressible
print(f"\nM12 Theory: Quran = {len(records)-len(hapax)} compressible words + {len(hapax)} incompressible unique roots")
print(f"Compression ratio core vs innovative: {len(core)}/114 = {len(core)/114*100:.1f}% core")
