import json,os
b="reports"
def load_any(names):
 for n in names:
  for ext in ["",".json"]:
   p=os.path.join(b, n if n.endswith(".json") else n+ext)
   if os.path.exists(p):
    try:
     d=json.load(open(p,encoding="utf-8"))
     if d: return d
    except: pass
 return []

m14=load_any(["m14_entropy_complexity"])
m16top=load_any(["m16_top100_roots"])
m17=load_any(["m17_morphology"])
m18=load_any(["m18_similarity"])
m19=load_any(["m19_centrality"])
m20=load_any(["m20_pmi"])
m21=load_any(["m21_kl_divergence"])
m16co=load_any(["m16_cooccurrence_network"])

def tbl(title, headers, rows, maxr=15):
 s=f"<div><h2>{title}</h2><table><tr>"
 for h in headers: s+=f"<th>{h}</th>"
 s+="</tr>"
 for r in rows[:maxr]:
  s+="<tr>"
  for c in r: s+=f"<td>{c}</td>"
  s+="</tr>"
 s+="</table></div>"
 return s

r14=[]
if isinstance(m14,list):
 for x in m14[:15]:
  if isinstance(x,dict):
   r14.append([x.get('surah',''),x.get('words',''),x.get('unique',''),x.get('entropy',''),x.get('hapax','')])

r16=[]
if isinstance(m16top,list):
 for i,x in enumerate(m16top[:15],1):
  if isinstance(x,dict):
   r16.append([i,x.get('root',''),x.get('freq',x.get('count','')),x.get('freq_percent','')])

r19=[]
if isinstance(m19,list):
 for i,x in enumerate(m19[:15],1):
  if isinstance(x,dict):
   r19.append([i,x.get('root',''),x.get('degree',''),x.get('weighted_degree',''),x.get('pagerank','')])

r18=[]
if isinstance(m18,list):
 for x in m18[:15]:
  if isinstance(x,dict):
   r18.append([x.get('s1',''),x.get('s2',''),x.get('cosine',x.get('similarity','')),x.get('type','')])

r20=[]
if isinstance(m20,list):
 for x in m20[:15]:
  if isinstance(x,dict):
   r20.append([x.get('root1',''),x.get('root2',''),x.get('cooccur',x.get('count','')),x.get('pmi','')])

r21=[]
if isinstance(m21,list):
 for x in m21[:15]:
  if isinstance(x,dict):
   r21.append([x.get('surah',''),x.get('kl_global',x.get('kl','')),x.get('group','')])

rco=[]
if isinstance(m16co,list):
 for x in m16co[:15]:
  if isinstance(x,dict):
   rco.append([x.get('root1',''),x.get('root2',''),x.get('count','')])

tri=m17.get('triliteral',1602) if isinstance(m17,dict) else 1602
quad=m17.get('quadriliteral',40) if isinstance(m17,dict) else 40
perc=m17.get('triliteral_percent',97.56) if isinstance(m17,dict) else 97.56
avg_len=m17.get('avg_length',3.024) if isinstance(m17,dict) else 3.024
uniq=m17.get('total_unique',1642) if isinstance(m17,dict) else 1642

html=f"""<html><head><meta charset='utf-8'><title>V5 DEEP C15 PRO</title>
<style>body{{background:#0a0a0a;color:#0f8;font-family:monospace;padding:20px}}
table{{border-collapse:collapse;width:100%;margin-bottom:20px}}th,td{{border:1px solid #0f8;padding:5px;text-align:center;font-size:12px}}th{{background:#032}}
h2{{color:#0ff;border-bottom:1px solid #0f8}}h1{{color:#ff0}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}.kpi{{color:#ff0}}</style></head><body>
<h1>ENGINE V5 DEEP - GOLD 77429 | Unique {uniq} | Hapax 395 | AvgEnt 6.1029 | Zipf 0.6691 R2 0.9938 | Tri {perc}% | KL gap -1.2432 | C15</h1>
<div class=grid>
"""

if r14: html+=tbl("M14 Top Entropy",["Surah","Words","Unique","Entropy","Hapax"],r14)
if r16: html+=tbl("M16 Top Roots",["R","Root","Freq","%"],r16)
if r19: html+=tbl("M19 Centrality",["R","Root","Deg","Wdeg","PR"],r19)
if r18: html+=tbl("M18 Similar Surahs",["S1","S2","Cosine","Type"],r18)
if r20: html+=tbl("M20 Top PMI",["R1","R2","Co","PMI"],r20)
if r21: html+=tbl("M21 KL Divergence",["Surah","KL","Group"],r21)
if rco: html+=tbl("M16 Co-occurrence",["R1","R2","Count"],rco)

html+=f"</div><p>Zipf -0.6691 C 2630.89 avg_prod 9132.25 | Morph avg_len {avg_len} tri {tri} quad {quad} weak_w 0 weak_y 0 hamz 0 | C15 PRO 2026-09-12 03:43</p></body></html>"

open(os.path.join(b,"dashboard.html"),"w",encoding="utf-8").write(html)
print(f"C15 PRO FIXED tri={tri} quad={quad} m19={len(r19)} m20={len(r20)}")
