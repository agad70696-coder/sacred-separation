#!/usr/bin/env python3
import random, json, os
random.seed(42)
m19=[("Alh",89),("qwl",53),("kwn",48),("rbb",31),("Amn",27),("Elm",17),("qwm",16),("$yA",14),("byn",15),("Aty",14),("ArD",11),("rsl",12),("kfr",11),("smw",10),("kll",9)]
m20=[("Eml","SlH",93,9.29),("ArD","smw",224,9.12),("gfr","rHm",91,8.97)]
m16_co=[("Alh","qwl",514),("Alh","kwn",441),("Alh","Elm",408)]
hub_89=[r[0] for r in m19]+["ns","jEl","Ebd","nfs","qbl","bEd","kwn2","sbl","dwn","qbl2","Hd","khr","dkhl","rHm","gfr","SlH","Eml","smw","ArD2","ywm2","l","mn","ma","An","fy","Ala","Ala2","Ayn","Aww","Akh","Ab","Am","Hm","Hn","Hwa","Hya","Hdh","Dlk","Tlkm","Ala3","qdr","Hkm","kwn3","kwn4","smy","bSr","smi","Elq","ktb","qrA","dkr","Hmd","sjd","rkE","swm","Hjj","zkat","jhd","qtl","Hrb","slm","Amn2","kfr2","nfq","mnn","Edl","qst","Hqq","bTl","xlf","wld","zwj","Ahl","qwm2"]
quad_40=["zlzl","wsws","zHzH","dmdm","kbkb","SrSr","HsHs","rfRf","EsEs","kfKf","dkdk","zqzq","jlJl","lmlm","tmtm","hmhm","qsqs","trjm","bETr","dHrj","brhn","frdq","srhq","zrqm","frEwn","qrn","Anjyl","Twrat","Ababyl","salsbyl","qrn2","brzq","qstas","sndr","Astbrq","frdws","jhnm","sjyl","zngbyl","kawTr"]
print(f"RULES hub={len(hub_89)} quad={len(quad_40)} total={len(hub_89)+len(quad_40)}")
for i in range(5):
    ayah=[ "Alh" if random.random()<0.45 else random.choice(hub_89) for _ in range(3)]
    print(f"Ayah {i+1}: {' + '.join(ayah)}")
print("BUILT V7 OK")
