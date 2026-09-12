import json,os
b=os.path.expanduser("~/structural-grammar/reports")
def load(n):
 try:
  return json.load(open(os.path.join(b,n),encoding="utf-8"))
 except:
  return []
m19=load("m19_centrality.json")
m20=load("m20_pmi.json")
m21=load("m21_kl_divergence.json")
h=[]
h.append("<html><head><meta charset='utf-8'><title>V5 DEEP PRO</title></head>")
h.append("<body style='background:#000;color:#0f0;padding:20px;font-family:monospace'>")
h.append("<h1 style='color:#ff0'>V5 DEEP GOLD 77429 | Unique 1642 | Hapax 395 | Tri 97.56%</h1>")
h.append("<h2>M19 Centrality - مركز الكون</h2>")
h.append("<table border=1 cellpadding=5><tr><th>Root</th><th>Deg</th><th>Wdeg</th><th>PR</th></tr>")
for r in m19[:15]:
 h.append(f"<tr><td>{r['root']}</td><td>{r['degree']}</td><td>{r['weighted_degree']}</td><td>{r['pagerank']}</td></tr>")
h.append("</table>")
h.append("<h2>M20 PMI - الثنائيات المقدسة</h2>")
h.append("<table border=1 cellpadding=5><tr><th>R1</th><th>R2</th><th>Co</th><th>PMI</th></tr>")
for r in m20[:15]:
 h.append(f"<tr><td>{r['root1']}</td><td>{r['root2']}</td><td>{r['cooccur']}</td><td>{r['pmi']}</td></tr>")
h.append("</table>")
h.append("<h2>M21 KL - سور مميزة</h2>")
h.append("<table border=1 cellpadding=5><tr><th>Surah</th><th>KL</th><th>Words</th><th>Group</th></tr>")
for r in m21[:15]:
 h.append(f"<tr><td>{r['surah']}</td><td>{r['kl_global']}</td><td>{r['words']}</td><td>{r['group']}</td></tr>")
h.append("</table></body></html>")
open(os.path.join(b,"dashboard.html"),"w",encoding="utf-8").write("\n".join(h))
print("pro dashboard built")
