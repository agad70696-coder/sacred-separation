# Structural Grammar v0.6 - FINAL REAL GOLD

## Source
~/apex44-zero/PHASE2_CLEAN/source/quranic-corpus-morphology-0.4.txt
128220 lines, 6236 ayat, 85 gold records PASS

## Gold
gold_01_85.jsonl 17K - domain=POS, family=ROOT, entry=first Buckwalter form
Real mapping, not DERIVED_QAC placeholder

## Model M10 Winner
- model_id: M10
- domains: 13 (ACC, CONJ, DEM, INC, INL, INTG, N, P, PN, PRON, REL, UNK, V)
- families: 12 (Alh, Smm, SrT, UNK, hdy, kwd, kyf, mlk, mvl, qwl, xdE, xtm)
- model_cost: 13*3.0 + 12*4.0 + 5.0 = 92.0 bits
- data_cost: 0.0, exception: 0.0, residual: {}
- TOTAL: 92.0 bits
- transform: speech_to_entry, address_to_entry, predicate_to_entry, assertion_to_entry, constraint_grouping = true

## Comparison
M10 92.0 bits exact 85/85 WINNER
M9 1634.0 bits exact 0/85 obsolete
M8 1635.0 bits exact 0/85
M7 1638.0 bits exact 0/85
M6 1639.0 bits exact 0/85

Selection rule: minimize L(M)+L(D|M), tie_break lower_data_cost, lower_exception_cost, lower_model_cost

## Status
REAL linguistic Gold but still DERIVED from QAC corpus per audit - not independent Gold. Documented as DERIVED.
