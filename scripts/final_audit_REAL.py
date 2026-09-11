import json
from collections import Counter
gold="gold/gold_WORD_77430.jsonl"
recs=[json.loads(l) for l in open(gold, encoding='utf-8')]
rc=Counter([r["root"] for r in recs if r.get("root")])
print(f"AUDIT REAL:")
print(f"Words: {len(recs)}")
print(f"Unique roots: {len(rc)}")
print(f"Hapax: {sum(1 for v in rc.values() if v==1)}")
print(f"Top root: {rc.most_common(1)}")
# Verify 90% claim
sorted_roots=rc.most_common()
cum=sum(f for _,f in sorted_roots[:441])
total=sum(rc.values())
print(f"441 roots cover {cum/total*100:.2f}% - claim 90.01% - diff {cum/total*100-90.01:.2f}%")
