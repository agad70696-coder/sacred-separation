import json, pathlib
gold_path = pathlib.Path("gold/gold_01_85.jsonl")
records = [json.loads(l) for l in open(gold_path, encoding='utf-8')]
eval_dir = pathlib.Path("evaluations")
# M10 exact copy
with open(eval_dir/"M10_candidate.jsonl","w",encoding="utf-8") as w:
    for r in records:
        rec=dict(r)
        rec["model_id"]="M10"
        w.write(json.dumps(rec, ensure_ascii=False)+"\n")
print("M10 rebuilt 85 exact")
# Keep M6-M9 as they are to show failure - they expect DERIVED_QAC
