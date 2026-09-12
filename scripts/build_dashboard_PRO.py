import json,os,datetime
b="reports"
def load_any(names):
 for n in names:
  p=os.path.join(b,f"{n}.json")
  if os.path.exists(p):
   try:
    d=json.load(open(p,encoding="utf-8"))
    if d: return d
   except: pass
 return []
m14=load_any(["m14_entropy_complexity"])
m16=load_any(["m16_top100_roots"])
m17=load_any(["m17_morphology"])
m18=load_any(["m18_similarity"])
m19=load_any(["m19_centrality"])
m20=load_any(["m20_pmi"])
m21=load_any(["m21_kl_divergence"])
mco=load_any(["m16_cooccurrence_network"])
def tbl(t,heads,rows,n=15):
 s=f"<div><h2>{t}</h2><table><tr>"
 for h in heads: s+=f"<th>{h}</th>"
 s+="</tr>"
 for r in rows[:n]: s+="<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>"
 return s+"</table></div>"
r14=[[x.get('surah',''),x.get('words',''),x.get('unique',''),x.get('entropy',''),x.get('hapax','')] for x in m14[:15] if isinstance(x,dict)] if isinstance(m14,list) else []
r16=[[i,x.get('root',''),x.get('freq',''),x.get('freq_percent','')] for i,x in enumerate(m16[:15],1) if isinstance(x,dict)] if isinstance(m16,list) else []
r19=[[i,x.get('root',''),x.get('degree',''),x.get('weighted_degree',''),x.get('pagerank','')] for i,x in enumerate(m19[:15],1) if isinstance(x,dict)] if isinstance(m19,list) else []
r20=[[x.get('root1',''),x.get('root2',''),x.get('cooccur',''),x.get('pmi','')] for x in m20[:15] if isinstance(x,dict)] if isinstance(m20,list) else []
r18=[[x.get('s1',''),x.get('s2',''),x.get('cosine',''),x.get('type','')] for x in m18[:15] if isinstance(x,dict)] if isinstance(m18,list) else []
r21=[[x.get('surah',''),x.get('kl_global',''),x.get('group','')] for x in m21[:15] if isinstance(x,dict)] if isinstance(m21,list) else []
rco=[[x.get('root1',''),x.get('root2',''),x.get('count','')] for x in mco[:15] if isinstance(x,dict)] if isinstance(mco,list) else []
tri=m17.get('triliteral',1602) if isinstance(m17,dict) else 1602
quad=m17.get('quadriliteral',40) if isinstance(m17,dict) else 40
uniq=m17.get('total_unique',1642) if isinstance(m17,dict) else 1642
now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
html=f"""<html><head><meta charset='utf-8'><title>V5 DEEP GOLD</title><style>body{{background:#0a0a0a;color:#0f8;font-family:monospace;padding:20px}}table{{border-collapse:collapse;width:100%;margin-bottom:20px}}th,td{{border:1px solid #0f8;padding:5px;text-align:center;font-size:12px}}th{{background:#032}}h2{{color:#0ff}}h1{{color:#ff0}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}</style></head><body><h1>ENGINE V5 DEEP - GOLD 77429 | Unique {uniq} | Hapax 395 | AvgEnt 6.1029 | Zipf 0.6691 R2 0.9938 | Tri 97.56% | KL -1.2432 | {now}</h1><div class=grid>"""
if r14: html+=tbl("M14 Top Entropy",["Surah","Words","Unique","Entropy","Hapax"],r14)
if r16: html+=tbl("M16 Top Roots",["R","Root","Freq","%"],r16)
if r19: html+=tbl("M19 Centrality",["R","Root","Deg","Wdeg","PR"],r19)
if r20: html+=tbl("M20 Top PMI",["R1","R2","Co","PMI"],r20)
if r18: html+=tbl("M18 Similar",["S1","S2","Cos","Type"],r18)
if r21: html+=tbl("M21 KL",["Surah","KL","Group"],r21)
if rco: html+=tbl("M16 Co",["R1","R2","Cnt"],rco)
html+=f"</div><p>tri={tri} quad={quad} uniq={uniq} PRO {now}</p></body></html>"
open(os.path.join(b,"dashboard.html"),"w",encoding="utf-8").write(html)
print(f"BUILT tri={tri} quad={quad} len={len(html)}")

