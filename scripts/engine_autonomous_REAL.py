#!/usr/bin/env python3
"""
Quran Engine V5 DEEP - Structural Grammar Deep Analysis
Production Grade - Real Execution Only - English Only
DEEP LAYERS:
  M14: Entropy per Surah
  M16: Top 100 Roots + Real Zipf (log-log regression) + Co-occurrence
  M17: Root Morphology - triliteral/quadriliteral, weak, hamzated, geminated
  M18: Surah Similarity Matrix - TF-IDF cosine 114x114, top similar/dissimilar pairs
  M19: Network Centrality - degree, weighted degree, PageRank on root graph
  M20: PMI - Pointwise Mutual Information for root pairs
  M21: KL Divergence - each Surah vs Global distribution + Meccan vs Medinan entropy gap
"""
from __future__ import annotations
import json, math, time, logging, subprocess, datetime, itertools, re
from pathlib import Path
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict
from typing import List, Tuple, Dict, Set
from statistics import mean, stdev

# Meccan vs Medinan classification - standard 86 Meccan, 28 Medinan
MEDINAN_SURAHS = {2,3,4,5,8,9,13,22,24,33,47,48,49,55,57,58,59,60,61,62,63,64,65,66,76,98,99,110}
MECCAN_SURAHS = set(range(1,115)) - MEDINAN_SURAHS

@dataclass(frozen=True)
class Config:
    root: Path
    gold: Path
    reports: Path
    log: Path
    sleep: int = 300
    @classmethod
    def default(cls):
        r = Path.home() / "structural-grammar"
        return cls(r, r/"gold"/"gold_WORD_77430.jsonl", r/"reports", r/"reports"/"engine.log")

@dataclass
class SurahMetrics:
    surah: int; words: int; unique: int; hapax: int
    entropy: float; hapax_density: float; info_density: float; complexity: float

@dataclass
class RootFreq:
    rank: int; root: str; freq: int; percent: float; cumulative_percent: float

@dataclass
class ZipfPoint:
    rank: int; root: str; freq: int; log_rank: float; log_freq: float; expected_freq: float; zipf_product: int

@dataclass
class CooccurPair:
    root1: str; root2: str; count: int; strength: float

@dataclass
class MorphologyStats:
    total_unique: int; triliteral: int; quadriliteral: int; quinqueliteral: int
    weak_waw: int; weak_ya: int; hamzated: int; geminated: int
    avg_length: float; triliteral_percent: float

@dataclass
class SimilarityPair:
    surah1: int; surah2: int; cosine: float; shared_roots: int; type: str

@dataclass
class CentralityNode:
    root: str; degree: int; weighted_degree: int; pagerank: float; rank: int

@dataclass
class PMIPair:
    root1: str; root2: str; cooccur: int; pmi: float; p1: float; p2: float; p_pair: float

@dataclass
class KLDivergence:
    surah: int; kl_global: float; words: int; entropy: float; group: str

def setup_log(p: Path, name="V5-DEEP"):
    p.parent.mkdir(parents=True, exist_ok=True)
    lg = logging.getLogger(name)
    lg.setLevel(logging.INFO)
    lg.handlers.clear()
    fmt = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    sh = logging.StreamHandler(); sh.setFormatter(fmt); lg.addHandler(sh)
    fh = logging.FileHandler(p, encoding="utf-8"); fh.setFormatter(fmt); lg.addHandler(fh)
    return lg

class Analyzer:
    def __init__(self, gold: Path, log: logging.Logger):
        self.gold=gold; self.log=log; self._rec=None

    def load(self):
        if self._rec is not None:
            return self._rec
        if not self.gold.exists():
            self.log.error(f"GOLD missing {self.gold}"); return []
        recs=[]
        with open(self.gold, encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line: continue
                try: recs.append(json.loads(line))
                except: continue
        self._rec=recs
        self.log.info(f"GOLD loaded {len(recs)} words")
        return recs

    def verify(self)->Tuple[bool,int]:
        c=len(self.load()); ok=c>=77429
        self.log.info(f"GOLD verify {c} - {'PASS' if ok else 'FAIL'}"); return ok,c

    def m14(self)->Tuple[List[SurahMetrics], Dict[int, Counter]]:
        recs=self.load(); by=defaultdict(list); by_counter={}
        for r in recs:
            try: by[int(r.get("surah",0))].append(r)
            except: continue
        res=[]
        for sid in range(1,115):
            sr=by.get(sid,[]); roots=[x.get("root") for x in sr if x.get("root")]
            if not roots: continue
            cnt=Counter(roots); by_counter[sid]=cnt
            total=len(roots); uniq=len(cnt); hap=sum(1 for v in cnt.values() if v==1)
            ent=-sum((c/total)*math.log2(c/total) for c in cnt.values()) if total else 0
            words=len(sr)
            res.append(SurahMetrics(sid,words,uniq,hap,round(ent,4),round(hap/words*100,3) if words else 0,round(ent/words*1000,4) if words else 0,round(uniq/words*100,3) if words else 0))
        rs=sorted(res,key=lambda x:x.entropy,reverse=True)
        if rs: self.log.info(f"M14 {len(rs)} surahs top {rs[0].surah}={rs[0].entropy}")
        return rs, by_counter

    def m16_top100(self)->Tuple[List[RootFreq], Counter, int]:
        recs=self.load()
        roots=[r.get("root") for r in recs if r.get("root") and len(str(r.get("root")).strip())>0]
        total=len(roots); cnt=Counter(roots); most=cnt.most_common(100)
        result=[]; cum=0
        for idx,(root,freq) in enumerate(most, start=1):
            cum+=freq
            result.append(RootFreq(idx,root,freq,round(freq/total*100,4) if total else 0,round(cum/total*100,4) if total else 0))
        self.log.info(f"M16 top {most[0][0]}={most[0][1]} unique={len(cnt)}")
        return result,cnt,total

    def m16_zipf(self, counter:Counter)->Dict:
        most_all=counter.most_common()
        if not most_all: return {}
        top_n=min(100,len(most_all))
        ranks=list(range(1,top_n+1)); freqs=[f for _,f in most_all[:top_n]]
        log_r=[math.log(r) for r in ranks]; log_f=[math.log(f) if f>0 else 0 for f in freqs]
        mean_lr=mean(log_r); mean_lf=mean(log_f)
        num=sum((lr-mean_lr)*(lf-mean_lf) for lr,lf in zip(log_r,log_f))
        den=sum((lr-mean_lr)**2 for lr in log_r)
        slope=num/den if den!=0 else 0; intercept=mean_lf-slope*mean_lr
        ss_tot=sum((lf-mean_lf)**2 for lf in log_f)
        ss_res=sum((lf-(intercept+slope*lr))**2 for lr,lf in zip(log_r,log_f))
        r2=1-ss_res/ss_tot if ss_tot!=0 else 0; C=math.exp(intercept)
        curve=[]
        for rank,(root,freq) in enumerate(most_all[:100], start=1):
            expected=C/(rank**(-slope)) if slope!=0 else C/rank
            curve.append(ZipfPoint(rank,root,freq,round(math.log(rank),4),round(math.log(freq),4) if freq>0 else 0,round(expected,2),rank*freq))
        avg_product=mean([p.zipf_product for p in curve]) if curve else 0
        result={"slope":round(slope,4),"intercept":round(intercept,4),"r2":round(r2,4),"alpha":round(-slope,4),"C":round(C,2),"avg_rank_freq_product":round(avg_product,2),"top_n":top_n,"curve":[asdict(p) for p in curve]}
        self.log.info(f"M16 Zipf slope={result['slope']} alpha={result['alpha']} R2={result['r2']}")
        return result

    def m16_cooccurrence(self, top_roots:Set[str], min_count:int=3)->Tuple[List[CooccurPair], Dict, int]:
        recs=self.load(); groups=defaultdict(list)
        has_ayah=any("ayah" in r or "aya" in r or "verse" in r for r in recs[:100])
        for r in recs:
            root=r.get("root")
            if not root or root not in top_roots: continue
            surah=r.get("surah",0); ayah=r.get("ayah") or r.get("aya") or r.get("verse") or r.get("ayah_num") or 0
            key=(surah,ayah) if has_ayah else (surah,)
            groups[key].append(root)
        pair_counter=Counter()
        for roots in groups.values():
            uniq=list(set(roots))
            if len(uniq)<2: continue
            for a,b in itertools.combinations(sorted(uniq),2):
                pair_counter[(a,b)]+=1
        filtered=[(pair,c) for pair,c in pair_counter.items() if c>=min_count]
        filtered.sort(key=lambda x:x[1],reverse=True)
        top_pairs=filtered[:300]
        max_c=top_pairs[0][1] if top_pairs else 1
        result=[CooccurPair(r1,r2,c,round(c/max_c,4)) for (r1,r2),c in top_pairs]
        self.log.info(f"M16 cooccur groups={len(groups)} pairs={len(pair_counter)} filtered={len(result)}")
        return result, groups, len(pair_counter)

    def m17_morphology(self, counter:Counter)->MorphologyStats:
        # Deep morphology based on Arabic root string patterns
        unique=list(counter.keys())
        total=len(unique)
        if total==0:
            return MorphologyStats(0,0,0,0,0,0,0,0,0,0)
        def is_weak_waw(r): return "و" in r
        def is_weak_ya(r): return "ي" in r or "ى" in r
        def is_hamzated(r): return "ء" in r or "أ" in r or "إ" in r or "ؤ" in r or "ئ" in r
        def is_geminated(r):
            # same letter twice in a row
            for i in range(len(r)-1):
                if r[i]==r[i+1]: return True
            return False
        triliteral=sum(1 for r in unique if len(r)==3)
        quadriliteral=sum(1 for r in unique if len(r)==4)
        quinque=sum(1 for r in unique if len(r)>=5)
        weak_waw=sum(1 for r in unique if is_weak_waw(r))
        weak_ya=sum(1 for r in unique if is_weak_ya(r))
        hamzated=sum(1 for r in unique if is_hamzated(r))
        geminated=sum(1 for r in unique if is_geminated(r))
        avg_len=mean([len(r) for r in unique]) if unique else 0
        stats=MorphologyStats(
            total_unique=total,
            triliteral=triliteral,
            quadriliteral=quadriliteral,
            quinqueliteral=quinque,
            weak_waw=weak_waw,
            weak_ya=weak_ya,
            hamzated=hamzated,
            geminated=geminated,
            avg_length=round(avg_len,3),
            triliteral_percent=round(triliteral/total*100,2) if total else 0
        )
        self.log.info(f"M17 morphology unique={total} tri={triliteral} quad={quadriliteral} weak_w={weak_waw} weak_y={weak_ya} hamz={hamzated}")
        return stats

    def m18_similarity(self, by_counter:Dict[int, Counter])->List[SimilarityPair]:
        # Build TF vectors for each surah, cosine similarity
        surahs=list(by_counter.keys())
        # global vocab
        vocab=set()
        for cnt in by_counter.values(): vocab.update(cnt.keys())
        vocab=list(vocab)
        # For efficiency, use top 500 roots global for vector
        global_cnt=Counter()
        for cnt in by_counter.values(): global_cnt.update(cnt)
        top_vocab=[r for r,_ in global_cnt.most_common(500)]
        # Build normalized vectors
        vectors={}
        for sid,cnt in by_counter.items():
            total=sum(cnt.values())
            vec=[cnt.get(root,0)/total if total else 0 for root in top_vocab]
            # L2 norm
            norm=math.sqrt(sum(x*x for x in vec))
            vectors[sid]=[x/norm if norm else 0 for x in vec]
        pairs=[]
        for i in range(len(surahs)):
            for j in range(i+1,len(surahs)):
                s1=surahs[i]; s2=surahs[j]
                v1=vectors[s1]; v2=vectors[s2]
                cosine=sum(a*b for a,b in zip(v1,v2))
                shared=len(set(by_counter[s1].keys()) & set(by_counter[s2].keys()))
                typ="both_meccan" if s1 in MECCAN_SURAHS and s2 in MECCAN_SURAHS else "both_medinan" if s1 in MEDINAN_SURAHS and s2 in MEDINAN_SURAHS else "mixed"
                pairs.append(SimilarityPair(s1,s2,round(cosine,4),shared,typ))
        pairs.sort(key=lambda x:x.cosine, reverse=True)
        top_similar=pairs[:50]
        bottom=pairs[-20:]
        self.log.info(f"M18 similarity {len(pairs)} pairs top {top_similar[0].surah1}-{top_similar[0].surah2}={top_similar[0].cosine} bottom {bottom[0].surah1}-{bottom[0].surah2}={bottom[0].cosine}")
        return top_similar + bottom

    def m19_centrality(self, cooccur_pairs:List[CooccurPair], top_roots:Set[str])->List[CentralityNode]:
        # Build graph adjacency
        adj=defaultdict(list)
        weighted=defaultdict(int)
        for p in cooccur_pairs:
            adj[p.root1].append(p.root2)
            adj[p.root2].append(p.root1)
            weighted[p.root1]+=p.count
            weighted[p.root2]+=p.count
        # Degree
        nodes=list(top_roots)
        # PageRank simple iterative
        damping=0.85
        pr={node:1/len(nodes) for node in nodes}
        # adjacency for PageRank - need outlinks
        for _ in range(20): # 20 iterations
            new_pr={}
            for node in nodes:
                rank_sum=0
                for other in nodes:
                    if node in adj[other]:
                        out_deg=len(adj[other]) if adj[other] else 1
                        rank_sum+=pr[other]/out_deg
                new_pr[node]=(1-damping)/len(nodes)+damping*rank_sum
            pr=new_pr
        result=[]
        for node in nodes:
            deg=len(set(adj.get(node,[])))
            wdeg=weighted.get(node,0)
            result.append(CentralityNode(node,deg,wdeg,round(pr.get(node,0),6),0))
        result.sort(key=lambda x:(x.weighted_degree, x.degree), reverse=True)
        for idx, n in enumerate(result, start=1):
            n.rank=idx
        self.log.info(f"M19 centrality top {result[0].root} deg={result[0].degree} wdeg={result[0].weighted_degree} pr={result[0].pagerank}")
        return result[:100]

    def m20_pmi(self, counter:Counter, cooccur_pairs:List[CooccurPair], total_words:int, total_groups:int)->List[PMIPair]:
        # PMI = log2(P(x,y) / (P(x)*P(y)))
        # P(x) = freq(x)/total_words, P(x,y)=cooccur/total_groups
        result=[]
        for p in cooccur_pairs[:100]:
            px=counter.get(p.root1,0)/total_words if total_words else 0
            py=counter.get(p.root2,0)/total_words if total_words else 0
            pxy=p.count/total_groups if total_groups else 0
            if px>0 and py>0 and pxy>0:
                pmi=math.log2(pxy/(px*py))
            else:
                pmi=0
            result.append(PMIPair(p.root1,p.root2,p.count,round(pmi,4),round(px,6),round(py,6),round(pxy,6)))
        result.sort(key=lambda x:x.pmi, reverse=True)
        if result:
            self.log.info(f"M20 PMI top {result[0].root1}+{result[0].root2} PMI={result[0].pmi}")
        return result

    def m21_kl(self, by_counter:Dict[int, Counter], global_counter:Counter, total_global:int, surah_metrics:Dict[int, SurahMetrics])->List[KLDivergence]:
        # KL(P_surah || P_global) - how much surah diverges
        global_probs={r:c/total_global for r,c in global_counter.items()}
        result=[]
        for sid,cnt in by_counter.items():
            total=sum(cnt.values())
            if total==0: continue
            kl=0
            for root,freq in cnt.items():
                p_surah=freq/total
                p_global=global_probs.get(root, 1e-9) # smoothing
                kl+=p_surah*math.log2(p_surah/p_global) if p_global>0 else 0
            group="medinan" if sid in MEDINAN_SURAHS else "meccan"
            result.append(KLDivergence(sid, round(kl,4), total, surah_metrics.get(sid, SurahMetrics(sid,0,0,0,0,0,0,0)).entropy if surah_metrics.get(sid) else 0, group))
        result.sort(key=lambda x:x.kl_global, reverse=True)
        if result:
            avg_meccan=mean([r.kl_global for r in result if r.group=="meccan"]) if any(r.group=="meccan" for r in result) else 0
            avg_medinan=mean([r.kl_global for r in result if r.group=="medinan"]) if any(r.group=="medinan" for r in result) else 0
            self.log.info(f"M21 KL top {result[0].surah} KL={result[0].kl_global} avg_meccan={avg_meccan:.4f} avg_medinan={avg_medinan:.4f}")
        return result

class GitMgr:
    def __init__(self, root:Path, log): self.root=root; self.log=log
    def run(self,cmd,timeout=30):
        try:
            r=subprocess.run(cmd,shell=True,cwd=self.root,capture_output=True,text=True,timeout=timeout)
            return r.returncode==0,(r.stdout+r.stderr).strip()
        except Exception as e: return False,str(e)
    def push(self,msg):
        ok,out=self.run("git status --porcelain")
        if not out.strip():
            self.log.info("Git clean"); return True
        self.run("git add reports/*.json reports/*.html")
        self.run(f'git commit -m "{msg}"')
        ok2,out2=self.run("git push")
        self.log.info(f"Git pushed {msg}" if ok2 else f"Git push fail {out2}"); return ok2

class EngineV5:
    def __init__(self):
        self.cfg=Config.default(); self.log=setup_log(self.cfg.log,"V5-DEEP")
        self.analyzer=Analyzer(self.cfg.gold,self.log); self.git=GitMgr(self.cfg.root,self.log); self.cycle=0

    def cycle_run(self):
        self.cycle+=1
        self.log.info(f"===== CYCLE {self.cycle} START V5 DEEP =====")
        ok,count=self.analyzer.verify()
        if not ok: return False
        m14_list, by_counter=self.analyzer.m14()
        if not m14_list: return False
        m14_dict={m.surah:m for m in m14_list}
        top100,counter,total_roots=self.analyzer.m16_top100()
        zipf_data=self.analyzer.m16_zipf(counter)
        top_set=set([r.root for r in top100])
        cooccur, groups, total_pairs=self.analyzer.m16_cooccurrence(top_set, min_count=3)
        morph=self.analyzer.m17_morphology(counter)
        similarity=self.analyzer.m18_similarity(by_counter)
        centrality=self.analyzer.m19_centrality(cooccur, top_set)
        pmi=self.analyzer.m20_pmi(counter, cooccur, total_roots, len(groups))
        kl_list=self.analyzer.m21_kl(by_counter, counter, total_roots, m14_dict)

        # save all reports
        self.cfg.reports.mkdir(parents=True,exist_ok=True)
        with open(self.cfg.reports/"m14_entropy_complexity.json","w",encoding="utf-8") as f:
            json.dump([asdict(x) for x in m14_list],f,ensure_ascii=False,indent=2)
        with open(self.cfg.reports/"m16_top100_roots.json","w",encoding="utf-8") as f:
            json.dump([asdict(x) for x in top100],f,ensure_ascii=False,indent=2)
        with open(self.cfg.reports/"m16_zipf_curve.json","w",encoding="utf-8") as f:
            json.dump(zipf_data,f,ensure_ascii=False,indent=2)
        with open(self.cfg.reports/"m16_cooccurrence_network.json","w",encoding="utf-8") as f:
            json.dump([asdict(x) for x in cooccur],f,ensure_ascii=False,indent=2)
        with open(self.cfg.reports/"m17_morphology.json","w",encoding="utf-8") as f:
            json.dump(asdict(morph),f,ensure_ascii=False,indent=2)
        with open(self.cfg.reports/"m18_similarity_matrix.json","w",encoding="utf-8") as f:
            json.dump([asdict(x) for x in similarity],f,ensure_ascii=False,indent=2)
        with open(self.cfg.reports/"m19_centrality.json","w",encoding="utf-8") as f:
            json.dump([asdict(x) for x in centrality],f,ensure_ascii=False,indent=2)
        with open(self.cfg.reports/"m20_pmi.json","w",encoding="utf-8") as f:
            json.dump([asdict(x) for x in pmi],f,ensure_ascii=False,indent=2)
        with open(self.cfg.reports/"m21_kl_divergence.json","w",encoding="utf-8") as f:
            json.dump([asdict(x) for x in kl_list],f,ensure_ascii=False,indent=2)

        ents=[x.entropy for x in m14_list]; avg=mean(ents) if ents else 0; std=stdev(ents) if len(ents)>1 else 0
        hapax_total=sum(1 for v in counter.values() if v==1)
        avg_kl_meccan=mean([k.kl_global for k in kl_list if k.group=="meccan"]) if kl_list else 0
        avg_kl_medinan=mean([k.kl_global for k in kl_list if k.group=="medinan"]) if kl_list else 0

        global_metrics={
            "engine":"V5 DEEP",
            "total_words":count,
            "total_unique_roots":len(counter),
            "hapax_total":hapax_total,
            "avg_entropy":round(avg,4),
            "std_entropy":round(std,4),
            "top_entropy":asdict(m14_list[0]) if m14_list else {},
            "top_root":asdict(top100[0]) if top100 else {},
            "zipf_slope":zipf_data.get("slope"),
            "zipf_alpha":zipf_data.get("alpha"),
            "zipf_r2":zipf_data.get("r2"),
            "morphology":asdict(morph),
            "most_similar_pair":asdict(similarity[0]) if similarity else {},
            "most_dissimilar_pair":asdict(similarity[-1]) if similarity else {},
            "top_central_root":asdict(centrality[0]) if centrality else {},
            "top_pmi_pair":asdict(pmi[0]) if pmi else {},
            "top_kl_surah":asdict(kl_list[0]) if kl_list else {},
            "avg_kl_meccan":round(avg_kl_meccan,4),
            "avg_kl_medinan":round(avg_kl_medinan,4),
            "kl_gap":round(avg_kl_medinan-avg_kl_meccan,4),
            "cooccurrence_pairs":len(cooccur),
            "timestamp":datetime.datetime.now().isoformat()
        }
        with open(self.cfg.reports/"m15_global_metrics.json","w",encoding="utf-8") as f:
            json.dump(global_metrics,f,ensure_ascii=False,indent=2)

        # dashboard V5 deep
        top_surahs="".join(f"{s.surah}{s.words}{s.unique}{s.entropy}{s.hapax}" for s in m14_list[:10])
        top_roots_html="".join(f"{r.rank}{r.root}{r.freq}{r.percent}%" for r in top100[:12])
        co_html="".join(f"{c.root1}{c.root2}{c.count}" for c in cooccur[:10])
        cent_html="".join(f"{c.rank}{c.root}{c.degree}{c.weighted_degree}{c.pagerank}" for c in centrality[:10])
        pmi_html="".join(f"{p.root1}{p.root2}{p.cooccur}{p.pmi}" for p in pmi[:10])
        sim_html="".join(f"{s.surah1}{s.surah2}{s.cosine}{s.type}" for s in similarity[:10])
        kl_html="".join(f"{k.surah}{k.kl_global}{k.group}" for k in kl_list[:10])

        html=f"""V5 DEEP Dashboard
        body{{background:#0a0a0a;color:#0f8;font-family:monospace;padding:20px}} table{{border-collapse:collapse;width:100%;margin-bottom:20px}} th,td{{border:1px solid #0f8;padding:5px;text-align:center;font-size:12px}} th{{background:#032}} h2{{color:#0ff;border-bottom:1px solid #0f8}} h1{{color:#ff0}}
        .grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
        
        ENGINE V5 DEEP - STRUCTURAL GRAMMAR
        GOLD {count} | Unique {len(counter)} | Hapax {hapax_total} | AvgEnt {avg:.4f} | Zipf α {zipf_data.get('alpha')} R2 {zipf_data.get('r2')} | Tri {morph.triliteral_percent}% | KL gap Meccan/Medinan {round(avg_kl_medinan-avg_kl_meccan,4)}
        M14 Top EntropySurahWordsUniqueEntropyHapax{top_surahs}
        
        M16 Top RootsRRootFreq%{top_roots_html}
        M19 Centrality (PageRank)RRootDegWdegPR{cent_html}
        
        M18 Most Similar Surahs (Cosine TF)S1S2CosineType{sim_html}
        M20 Top PMI (Mutual Information)R1R2CoPMI{pmi_html}
        M21 KL Divergence Top (vs Global)SurahKLGroup{kl_html}
        M16 Co-occurrenceR1R2Count{co_html}
         Zipf slope {zipf_data.get('slope')} C {zipf_data.get('C')} avg_prod {zipf_data.get('avg_rank_freq_product')} | Morph avg_len {morph.avg_length} tri {morph.triliteral} quad {morph.quadriliteral} weak_w {morph.weak_waw} weak_y {morph.weak_ya} hamz {morph.hamzated} | {datetime.datetime.now().isoformat()} C{self.cycle}
        """
        open(self.cfg.reports/"dashboard.html","w",encoding="utf-8").write(html)

        ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.git.push(f"AUTO V5-DEEP {ts} C{self.cycle} {count}w {len(counter)}r tri={morph.triliteral_percent}% zipf={zipf_data.get('alpha')} KLgap={round(avg_kl_medinan-avg_kl_meccan,4)}")
        self.log.info(f"===== CYCLE {self.cycle} DONE V5 DEEP sleep {self.cfg.sleep}s =====")
        return True

    def forever(self):
        self.log.info("=== ENGINE V5 DEEP START ===")
        while True:
            try:
                self.cycle_run(); time.sleep(self.cfg.sleep)
            except KeyboardInterrupt:
                self.log.info("Stopped"); break
            except Exception as e:
                self.log.exception(f"Loop error {e}"); time.sleep(60)

if __name__=="__main__":
    EngineV5().forever()
