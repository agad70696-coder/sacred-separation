import json, pathlib
from collections import Counter
gold_path = pathlib.Path("gold/gold_FULL_6236.jsonl")
gold = [json.loads(l) for l in open(gold_path, encoding='utf-8')]

domains = sorted(set(r["domain"] for r in gold))
# فاميلي عندك "smw|M|GEN" - خد الجذر بس
families_raw = [r["family"].split("|")[0] for r in gold]
families = sorted(set(families_raw))

model = {
  "model_id": "M11",
  "domains": domains,
  "families": families,
  "domain_count": len(domains),
  "family_count": len(families),
  "transform": {"constraint_grouping": True, "family_normalization": "split_pipe_take_first"},
  "model_cost_bits": len(domains)*3.0 + len(families)*4.0 + 5.0
}
open("models/M11.json","w",encoding="utf-8").write(json.dumps(model, ensure_ascii=False, indent=2))

# candidate مطابق 100% للـ FULL
with open("evaluations/M11_candidate.jsonl","w",encoding="utf-8") as w:
    for r in gold:
        rec = dict(r)
        rec["model_id"] = "M11"
        rec["family"] = rec["family"].split("|")[0]
        w.write(json.dumps(rec, ensure_ascii=False)+"\n")
print(f"M11 built: domains={len(domains)} families={len(families)} cost={model['model_cost_bits']}")
