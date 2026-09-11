import json, pathlib, glob
gold_path = pathlib.Path("gold/gold_FULL_6236.jsonl")
gold = [json.loads(l) for l in open(gold_path, encoding='utf-8')]

results=[]
for mf in glob.glob("models/M*.json"):
    mid = pathlib.Path(mf).stem
    model = json.load(open(mf))
    cand_path = pathlib.Path(f"evaluations/{mid}_candidate.jsonl")
    if not cand_path.exists():
        continue
    cand = [json.loads(l) for l in open(cand_path, encoding='utf-8')]

    exact=0
    res_dom=res_fam=0
    # قارن الموجود
    for g,c in zip(gold, cand):
        gd = g["domain"]
        gf = g["family"].split("|")[0]
        cd = c.get("domain","")
        cf = str(c.get("family","")).split("|")[0]
        if gd==cd and gf==cf:
            exact+=1
        else:
            if gd!=cd: res_dom+=1
            if gf!=cf: res_fam+=1

    # لو الـ candidate أقصر من الـ gold - احسب الباقي كله غرامة
    missing = len(gold) - len(cand)
    if missing > 0:
        res_dom += missing
        res_fam += missing

    mc = model.get("model_cost_bits", 0)
    dc = res_dom*5.0 + res_fam*6.0
    ec = (res_dom + res_fam)*4.0
    total = mc + dc + ec

    results.append({
      "model_id": mid,
      "gold_records": len(gold),
      "evaluated": min(len(gold), len(cand)),
      "missing": missing,
      "exact_records": exact,
      "exact_rate": exact/len(gold),
      "model_cost_bits": mc,
      "data_cost_bits": dc,
      "exception_cost_bits": ec,
      "total_description_length_bits": total,
      "residual_counts": {"domain": res_dom, "family": res_fam}
    })

results = sorted(results, key=lambda x: x["total_description_length_bits"])
open("reports/mdl_gold_FULL_6236.json","w",encoding="utf-8").write(json.dumps({"results": results}, ensure_ascii=False, indent=2))

for r in results:
    print(f"{r['model_id']}: TOTAL={r['total_description_length_bits']:.1f} exact={r['exact_records']}/{r['gold_records']} rate={r['exact_rate']:.3f} missing={r['missing']} model={r['model_cost_bits']} data={r['data_cost_bits']} resid={r['residual_counts']}")

print(f"\nWINNER FULL = {results[0]['model_id']} TOTAL {results[0]['total_description_length_bits']}")
