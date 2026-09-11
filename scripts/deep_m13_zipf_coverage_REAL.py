import json
from collections import Counter

gold = "gold/gold_WORD_77430.jsonl"
records = [json.loads(l) for l in open(gold, encoding='utf-8')]
roots = [r["root"] for r in records if r.get("root")]
rc = Counter(roots)
total_roots_tokens = len(roots)
unique_roots = len(rc)

# Zipf ranking
sorted_roots = rc.most_common()
cumulative = 0
coverage_points = []

print(f"TOTAL TOKENS: {total_roots_tokens} root tokens")
print(f"UNIQUE ROOTS: {unique_roots}")
print(f"\nZIPF ANALYSIS - Top roots:")

for rank, (root, freq) in enumerate(sorted_roots[:20], 1):
    cumulative += freq
    coverage = cumulative / total_roots_tokens * 100
    print(f"Rank {rank:3d}: {root:6s} freq {freq:4d} cum {cumulative:5d} coverage {coverage:5.2f}%")
    coverage_points.append((rank, coverage))

# Find minimal set for 80, 90, 95, 99%
targets = [80, 90, 95, 99, 100]
cumulative = 0
results = {}
for rank, (root, freq) in enumerate(sorted_roots, 1):
    cumulative += freq
    cov = cumulative / total_roots_tokens * 100
    for t in targets:
        if t not in results and cov >= t:
            results[t] = (rank, root, cov)

print(f"\nM13 MINIMAL ROOT SET:")
for t in targets:
    if t in results:
        rank, root, cov = results[t]
        print(f"{t}% coverage needs {rank} roots - last root {root} - actual {cov:.2f}%")

# Hapax analysis
hapax = [r for r,f in rc.items() if f==1]
print(f"\nHAPAX: {len(hapax)} roots = {len(hapax)/unique_roots*100:.1f}% of vocabulary but only {len(hapax)/total_roots_tokens*100:.2f}% of tokens")
print(f"CORE vs HAPAX: {unique_roots-len(hapax)} common roots carry {100-len(hapax)/total_roots_tokens*100:.2f}% of meaning")

# Save
import pathlib
pathlib.Path("reports").mkdir(exist_ok=True)
with open("reports/m13_zipf_coverage.json", "w", encoding="utf-8") as f:
    json.dump({
        "total_tokens": total_roots_tokens,
        "unique_roots": unique_roots,
        "coverage_targets": {str(k): {"roots_needed": v[0], "coverage": v[2]} for k,v in results.items()},
        "top_20": [{"rank": i+1, "root": r, "freq": f} for i,(r,f) in enumerate(sorted_roots[:20])],
        "hapax_percent_vocab": len(hapax)/unique_roots*100,
        "hapax_percent_tokens": len(hapax)/total_roots_tokens*100
    }, f, ensure_ascii=False, indent=2)

print("\nSaved to reports/m13_zipf_coverage.json")
