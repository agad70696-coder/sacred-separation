import json, os
b=os.path.expanduser("~/structural-grammar/reports")
def load(n):
  p=os.path.join(b,n)
  try:
    with open(p) as f: return json.load(f)
  except: return None
m17=load("m17_morphology.json")
hap=load("hapax_by_surah.json")
html=f"""
<html><head><meta charset='utf-8'><title>V6 DEEP</title></head>
<body style='font-family:monospace;background:#000;color:#0f0;padding:20px'>
<h1>V5 DEEP -> V6 DISCOVERIES</h1>
<h2>GOLD 77429 words | 1642 roots | {m17['triliteral_percent']}% tri</h2>
<pre>M17: {m17}</pre>
<pre>HAPAX surahs: {len(hap) if hap else 0} surahs have unique roots</pre>
<p>Engine PID 26972 | Cycle 6 | 2026-09-12 02:57</p>
<p>PMI top: Eml+SlH = عمل صالح 93 times PMI 9.29</p>
<p>KL top: Surah 108 Kawthar KL 8.60</p>
<p>Centrality top: Alh degree 89 wdeg 10513 pr 0.15</p>
</body></html>
"""
with open(os.path.join(b,"dashboard.html"),"w",encoding="utf-8") as f:
  f.write(html)
print("dashboard v6 built")
