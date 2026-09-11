import json, pathlib
gold_path = pathlib.Path("gold/gold_FULL_6236.jsonl")
model_path = pathlib.Path("models/M10.json")

gold = [json.loads(l) for l in open(gold_path, encoding='utf-8')] if gold_path.exists() else []
print(f"Gold FULL loaded: {len(gold)}")
if len(gold) == 0:
    print("ERROR: gold file empty, check build step")
    exit(1)

model = json.load(open(model_path))
domains = set(model["domains"])
families = set(model["families"])

exact = sum(1 for r in gold if r["domain"] in domains and r["family"] in families)
residual_domain = sum(1 for r in gold if r["domain"] not in domains)
residual_family = sum(1 for r in gold if r["family"] not in families)

model_cost = model["model_cost_bits"]
data_cost = residual_domain*5.0 + residual_family*6.0
exception_cost = (residual_domain + residual_family)*4.0
total = model_cost + data_cost + exception_cost

rate = exact / len(gold) if len(gold) else 0.0
print(f"M10 on FULL {len(gold)}:")
print(f" exact {exact}/{len(gold)} rate {rate:.3f}")
print(f" residual domain {residual_domain} family {residual_family}")
print(f" model {model_cost} data {data_cost} exception {exception_cost} TOTAL {total}")
