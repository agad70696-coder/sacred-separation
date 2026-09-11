import json
from collections import Counter, defaultdict
path="gold/gold_WORD_77430.jsonl"
records=[json.loads(l) for l in open(path, encoding='utf-8')]
rc=Counter([r["root"] for r in records if r["root"]])
hapax={k for k,v in rc.items() if v==1}
by_surah=defaultdict(list)
for r in records:
    if r["root"] in hapax:
        by_surah[r["surah"]].append(r)

print(f"REAL: {len(hapax)} hapax roots across {len(by_surah)} surahs")
for surah in sorted(by_surah, key=lambda s: len(by_surah[s]), reverse=True)[:15]:
    roots=[x["root"] for x in by_surah[surah]]
    print(f"Surah {surah:3d}: {len(roots):3d} hapax - {roots[:8]}")

# Save report
import pathlib
pathlib.Path("reports").mkdir(exist_ok=True)
with open("reports/hapax_by_surah.json","w",encoding='utf-8') as out:
    json.dump({str(k):[r["root"] for r in v] for k,v in by_surah.items()}, out, ensure_ascii=False, indent=2)
print("Saved to reports/hapax_by_surah.json")
