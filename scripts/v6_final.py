import json, os
b=os.path.expanduser("~/structural-grammar/reports")
def load(n):
  p=os.path.join(b,n)
  if not os.path.exists(p): return None
  with open(p,"r",encoding="utf-8") as f:
    return json.load(f)

hap=load("hapax_by_surah.json")
m17=load("m17_morphology.json")
m19=load("m19_centrality.json")
m20=load("m20_pmi.json")
m21=load("m21_kl_divergence.json")

print("M17:",m17)
if hap:
  cnt={int(k):len(v) for k,v in hap.items()}
  top=sorted(cnt.items(),key=lambda x:x[1],reverse=True)[:15]
  print("TOP HAPAX:")
  for s,c in top:
    print(s,c)
  print("TOTAL HAPAX:",sum(cnt.values()))

if m19:
  print("M19 SAMPLE:",str(m19)[:500])
if m20:
  print("M20 SAMPLE:",str(m20)[:500])
if m21:
  print("M21 SAMPLE:",str(m21)[:500])
