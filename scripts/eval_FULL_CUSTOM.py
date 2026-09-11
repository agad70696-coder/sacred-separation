import json, pathlib, glob
gold_path = pathlib.Path("gold/gold_FULL_6236.jsonl")
gold = [json.loads(l) for l in open(gold_path, encoding='utf-8')]
gold_by_src = {r["source"]: r for r in gold}

results=[]
for model_file in glob.glob("models/M*.json"):
    model_id = pathlib.Path(model_file).stem
    model = json.load(open(model_file))
    domains = set(model.get("domains",[]))
    # normalize families في الموديل لو فيها |
    families = set(f.split("|")[0] for f in model.get("families",[]))

    cand_path = pathlib.Path(f"evaluations/{model_id}_candidate.jsonl")
    if cand_path.exists():
        cand = [json.loads(l) for l in open(cand_path, encoding='utf-8')]
        exact=0
        res_dom=res_fam=0
        for g,c in zip(gold, cand):
            gd, gf = g["domain"], g["family"].split("|")[0]
            cd, cf = c.get("domain",""), str(c.get("family","")).split("|")[0]
            if gd==cd and gf==cf:
                exact+=1
            else:
                if gd!=cd: res_dom+=1
                if gf!=cf: res_fam+=1
    else:
        # مفيش candidate - احسب بالتغطية
        exact = sum(1 for r in gold if r["domain"] in domains and r["family"].split("|")[0] in families)
        res_dom = sum(1 for r in gold if r["domain"] not in domains)
        res_fam = sum(1 for r in gold if r["family"].split("|")[0] not in families)

    model_cost = model.get("model_cost_bits", 0)
    data_cost = res_dom*5.0 + res_fam*6.0
    exc_cost = (res_dom+res_fam)*4.0
    total = model_cost + data_cost + exc_cost

    results.append({
      "model_id": model_id,
      "gold_records": len(gold),
      "evaluated_predictions": len(gold),
      "missing_predictions": 0,
      "exact_records": exact,
      "exact_rate": exact/len(gold) if gold else 0,
      "model_cost_bits": model_cost,
      "data_cost_bits": data_cost,
      "exception_cost_bits": exc_cost,
      "total_description_length_bits": total,
      "residual_counts": {"family": res_fam, "domain": res_dom}
    })

results = sorted(results, key=lambda x: x["total_description_length_bits"])
open("reports/mdl_gold_FULL_6236.json","w",encoding="utf-8").write(json.dumps({"results": results}, ensure_ascii=False, indent=2))
for r in results:
    print(f"{r['model_id']}: TOTAL={r['total_description_length_bits']} exact={r['exact_records']}/{r['gold_records']} rate={r['exact_rate']:.3f} model={r['model_cost_bits']} data={r['data_cost_bits']} exc={r['exception_cost_bits']} resid={r['residual_counts']}")
print(f"WINNER FULL = {results[0]['model_id']}")
