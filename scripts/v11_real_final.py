import json,os
b="reports"
def load(n):
 p=os.path.join(b,n)
 try:
  return json.load(open(p,encoding="utf-8"))
 except:
  return None
m14=load("m14_entropy_complexity.json")
m16top=load("m16_top100_roots.json")
m16zipf=load("m16_zipf_curve.json")
m17=load("m17_morphology.json")
m19=load("m19_centrality.json")
m20=load("m20_pmi.json")
m21=load("m21_kl_divergence.json")
print("M14",str(m14)[:200])
print("M16 TOP",m16top[:3] if m16top else "no")
print("M17",m17)
print("M19 TOP",m19[0] if m19 else "no")
print("M20 TOP",m20[0] if m20 else "no")
print("M21 TOP",m21[0] if m21 else "no")
