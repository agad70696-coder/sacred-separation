# REAL QAC GOLD v2 - Still DERIVED not independent

Source: ~/apex44-zero/PHASE2_CLEAN/source/quranic-corpus-morphology-0.4.txt - 128220 data, 6236 ayat
Method: parse (sura:aya:word:seg) FORM + POS: + ROOT: + LEM: features
Gold: first 85 canonical ayat, domain=POS (N,V,P etc), family=ROOT, entry=first Buckwalter form
Status: REAL linguistic mapping - PASS validate_gold.py 85 records
But still DERIVED from QAC - structural integrity != independent Gold per audit

Models:
- M6/M7/M8/M9: mechanical test expecting DERIVED_QAC - now fail with residual 85/85, total 1638-1639 bits
- M10: real QAC POS/ROOT model - exact 85/85, data_cost 0, total ~ model_cost (winner)

Report: reports/mdl_gold_01_85.json
Gold: gold/gold_01_85.jsonl (REAL)
Backup DERIVED placeholder: gold/gold_01_85_DERIVED_from_QAC.jsonl

MDL costs: domain_symbol 3.0, family_symbol 4.0, entry 4.0, residual_family 6.0, residual_domain 5.0, exception 8.0
Selection: minimize L(M)+L(D|M), tie_break lower_data_cost, lower_exception_cost, lower_model_cost, lexicographic
