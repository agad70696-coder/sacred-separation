import json, os
base=os.path.expanduser("~/structural-grammar/reports")
def load(n):
  p=os.path.join(base,n)
  try:
    return json.load(open(p,encoding="utf-8"))
  except:
    return []
m19=load("m19_centrality.json")
m20=load("m20_pmi.json")
print("TOP CENTRALITY")
for r in m19[:10]:
  print(r["root"],r["degree"],round(r["pagerank"],4))
print("TOP PMI")
for r in m20[:10]:
  print(r["root1"],"+",r["root2"],r["cooccur"],round(r["pmi"],2))
