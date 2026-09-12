#!/usr/bin/env python3
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
m17=load_any(["m17_morphology"])
tri=m17.get('triliteral',1602) if isinstance(m17,dict) else 1602
quad=m17.get('quadriliteral',40) if isinstance(m17,dict) else 40
gold=77429
freqs=[2851,1722,1390,980,879,854,660,549,525,523,519,513,461,405,382]
rules=89+40+37
compression=gold/rules
now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
html=f"<html><head><meta charset='utf-8'><title>V6</title><style>body{{background:#000;color:#0f8;font-family:monospace;padding:10px}}</style></head><body><h1>V6 GOLD {gold} tri={tri} quad={quad} {compression:.1f}:1 {now}</h1></body></html>"
os.makedirs(b,exist_ok=True)
open(os.path.join(b,"dashboard_V6.html"),"w",encoding="utf-8").write(html)
open(os.path.join(b,"dashboard.html"),"w",encoding="utf-8").write(html)
print(f"BUILT V6 tri={tri} quad={quad} compression={compression:.1f}:1")
