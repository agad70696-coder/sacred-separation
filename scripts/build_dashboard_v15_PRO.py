import json,os,glob
b="reports"
def load(n):
 for p in [os.path.join(b,n), os.path.join(b,n+".json")]:
  if os.path.exists(p):
   try:
    return json.load(open(p,encoding="utf-8"))
   except: pass
 return []
# حاول كل الاسماء المحتملة
def load_any(names):
 for n in names:
  d=load(n)
  if d: return d
 return []

m14=load_any(["m14_entropy_complexity","m14_entropy","m14_top"])
m15=load_any(["m15_global_metrics","m15_metrics"])
m16top=load_any(["m16_top100_roots","m16_top_roots","m16_frequency"])
m17=load_any(["m17_morphology"])
m18=load_any(["m18_similarity","m18_most_similar"])
m19=load_any(["m19_centrality"])
m20=load_any(["m20_pmi"])
m21=load_any(["m21_kl_divergence","m21_kl"])
m16co=load_any(["m16_cooccurrence_network","m16_cooccurrence"])

# header ثابت من C15
gold=77429
uniq=1642
hapax=395
avgEnt=6.1029
zipf=0.6691
r2=0.9938
tri_p=97.56
klgap=-1.2432

html=f"""<html><head><meta charset='utf-8'><title>V5 DEEP C15 PRO</title>
<style>
body{{background:#0a0a0a;color:#0f8;font-family:monospace;padding:20px}}
table{{border-collapse:collapse;width:100%;margin-bottom:20px}} th,td{{border:1px solid #0f8;padding:5px;text-align:center;font-size:12px}}
th{{background:#032}} h2{{color:#0ff;border-bottom:1px solid #0f8}} h1{{color:#ff0}} .grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
.kpi{{color:#ff0;font-size:14px}}
</style></head><body>
<h1>ENGINE V5 DEEP - STRUCTURAL GRAMMAR GOLD C15 PRO</h1>
<p class=kpi>{gold} | Unique {uniq} | Hapax {hapax} | AvgEnt {avgEnt} | Zipf α {zipf} R2 {r2} | Tri {tri_p}% | KL gap Meccan/Medinan {klgap} | 2026-09-12 C15</p>
<div class=grid>
"""

def table_html(title, headers, rows, maxr=15):
  s=f"<div><h2>{title}</h2><table><tr>"
  for h in headers: s+=f"<th>{h}</th>"
  s+="</tr>"
  for r in rows[:maxr]:
   s+="<tr>"
   for c in r: s+=f"<td>{c}</td>"
   s+="</tr>"
  s+="</table></div>"
  return s

# M14
rows14=[]
if isinstance(m14,list):
 for x in m14[:15]:
  if isinstance(x,dict):
   rows14.append([x.get('surah',''), x.get('words',''), x.get('unique',''), x.get('entropy',''), x.get('hapax','')])
  elif isinstance(x,list):
   rows14.append(x)
if rows14:
 html+=table_html("M14 Top Entropy","Surah","Words","Unique","Entropy","Hapax",rows14)

# M16 Top Roots
rows16=[]
if isinstance(m16top,list):
 for i,x in enumerate(m16top[:15],1):
  if isinstance(x,dict):
   rows16.append([i, x.get('root',''), x.get('freq',x.get('count','')), f"{x.get('freq_percent',0):.2f}%" if 'freq_percent' in x else ""])
  else: rows16.append([i,str(x)])
if rows16:
 html+=table_html("M16 Top Roots","R","Root","Freq%","",rows16)

# M19 Centrality
rows19=[]
if isinstance(m19,list):
 for i,x in enumerate(m19[:15],1):
  if isinstance(x,dict):
   rows19.append([i, x.get('root',''), x.get('degree',''), x.get('weighted_degree',''), x.get('pagerank','')])
if rows19:
 html+=table_html("M19 Centrality (PageRank)","R","Root","Deg","Wdeg","PR",rows19)

# M18 Similar
rows18=[]
if isinstance(m18,list):
 for x in m18[:15]:
  if isinstance(x,dict):
   rows18.append([x.get('s1',''), x.get('s2',''), x.get('cosine',x.get('similarity','')), x.get('type','')])
if rows18:
 html+=table_html("M18 Most Similar Surahs (Cosine TF)","S1","S2","Cosine","Type",rows18)

# M20 PMI
rows20=[]
if isinstance(m20,list):
 for x in m20[:15]:
  if isinstance(x,dict):
   rows20.append([x.get('root1',''), x.get('root2',''), x.get('cooccur',x.get('count','')), x.get('pmi','')])
if rows20:
 html+=table_html("M20 Top PMI (Mutual Information)","R1","R2","Co","PMI",rows20)

# M21 KL
rows21=[]
if isinstance(m21,list):
 for x in m21[:15]:
  if isinstance(x,dict):
   rows21.append([x.get('surah',''), x.get('kl_global',x.get('kl','')), x.get('group',x.get('type',''))])
if rows21:
 html+=table_html("M21 KL Divergence Top (vs Global)","Surah","KL","Group",rows21)

# M16 Co-occurrence
rowsco=[]
if isinstance(m16co,list):
 for x in m16co[:15]:
  if isinstance(x,dict):
   rowsco.append([x.get('root1',''), x.get('root2',''), x.get('count',x.get('cooccur',''))])
if rowsco:
 html+=table_html("M16 Co-occurrence","R1","R2","Count",rowsco)

# Footer morph + zipf
tri = m17.get('triliteral',1602) if isinstance(m17,dict) else 1602
quad = m17.get('quadriliteral',40) if isinstance(m17,dict) else 40
avg_len = m17.get('avg_length',3.024) if isinstance(m17,dict) else 3.024
html+=f"</div><p>Zipf slope -0.6691 C 2630.89 avg_prod 9132.25 | Morph avg_len {avg_len} tri {tri} quad {quad} weak_w 0 weak_y 0 hamz 0 | 2026-09-12 C15</p></body></html>"

open(os.path.join(b,"dashboard.html"),"w",encoding="utf-8").write(html)
print(f"C15 PRO built tri={tri} quad={quad} rows m19={len(rows19)} m20={len(rows20)}")
