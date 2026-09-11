import json, pathlib
gold_path = pathlib.Path("gold/gold_01_85.jsonl")
gold = [json.loads(l) for l in open(gold_path, encoding='utf-8')]
import glob
results=[]
for mf in glob.glob("models/M*.json"):
    mid = pathlib.Path(mf).stem
    if mid=="M11": continue
    model=json.load(open(mf))
    cand_path=pathlib.Path(f"evaluations/{mid}_candidate.jsonl")
    if not cand_path.exists(): continue
    cand=[json.loads(l) for l in open(cand_path, encoding='utf-8')][:85]
    exact=sum(1 for g,c in zip(gold,cand) if g["domain"]==c["domain"] and g["family"].split("|")[0]==c["family"].split("|")[0])
    res_dom=sum(1 for g,c in zip(gold,cand) if g["domain"]!=c["domain"])
    res_fam=sum(1 for g,c in zip(gold,cand) if g["family"].split("|")[0]!=c["family"].split("|")[0])
    mc=model.get("model_cost_bits",0)
    dc=res_dom*5+res_fam*6
    ec=(res_dom+res_fam)*4
    results.append({"model_id":mid,"gold_records":85,"exact_records":exact,"exact_rate":exact/85,"model_cost_bits":mc,"data_cost_bits":dc,"exception_cost_bits":ec,"total_description_length_bits":mc+dc+ec,"residual_counts":{"domain":res_dom,"family":res_fam}})

results=sorted(results, key=lambda x: x["total_description_length_bits"])
open("reports/mdl_gold_01_85.json","w",encoding="utf-8").write(json.dumps({"results":results},ensure_ascii=False,indent=2))
for r in results:
    print(f"{r['model_id']}: TOTAL={r['total_description_length_bits']} exact={r['exact_records']}/85 rate={r['exact_rate']} model={r['model_cost_bits']}")
print(f"WINNER 85 = {results[0]['model_id']}")
