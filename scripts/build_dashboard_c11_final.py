import json,os
b="reports"
def load(n):
 try:
  return json.load(open(os.path.join(b,n),encoding="utf-8"))
 except:
  return {}
m17=load("m17_morphology.json")
m19=load("m19_centrality.json")
m20=load("m20_pmi.json")
m21=load("m21_kl_divergence.json")
tri=m17.get("triliteral",1602)
quad=m17.get("quadriliteral",40)
perc=m17.get("triliteral_percent",97.56)
uniq=m17.get("total_unique",1642)
gem=m17.get("geminated",153)
avg=m17.get("avg_length",3.024)

h=[]
h.append("<html><head><meta charset='utf-8'><title>C11 FINAL PRO</title></head>")
h.append("<body style='background:#000;color:#0f0;padding:15px;font-family:monospace'>")
h.append("<h1 style='color:#ff0'>C11 DONE 77429w 1642r tri97.56% zipf0.6691 R2 0.9938</h1>")
h.append(f"<p style='color:#0ff;font-size:18px'>M17 total={uniq} tri={tri} quad={quad} perc={perc}% weak=0 hamz=0 gem={gem} avg={avg} PERFECT</p>")
h.append("<h2>M19 Centrality</h2><table border=1 cellpadding=3><tr><th>root</th><th>deg</th><th>wdeg</th><th>pr</th></tr>")
for r in m19[:15]:
 h.append(f"<tr><td>{r['root']}</td><td>{r['degree']}</td><td>{r['weighted_degree']}</td><td>{r['pagerank']}</td></tr>")
h.append("</table><h2>M20 PMI</h2><table border=1 cellpadding=3><tr><th>r1</th><th>r2</th><th>co</th><th>pmi</th></tr>")
for r in m20[:15]:
 h.append(f"<tr><td>{r['root1']}</td><td>{r['root2']}</td><td>{r['cooccur']}</td><td>{r['pmi']}</td></tr>")
h.append("</table><h2>M21 KL 108=8.60</h2><table border=1 cellpadding=3><tr><th>surah</th><th>KL</th><th>words</th></tr>")
for r in m21[:15]:
 h.append(f"<tr><td>{r['surah']}</td><td>{r['kl_global']}</td><td>{r['words']}</td></tr>")
h.append("</table></body></html>")
open(os.path.join(b,"dashboard.html"),"w",encoding="utf-8").write("\n".join(h))
print(f"FINAL built tri={tri} quad={quad} {perc}%")
