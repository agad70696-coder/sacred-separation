# Structural Grammar - FINAL RESULTS

## 85 Ayat
WINNER M10 TOTAL 92.0 exact 85/85 rate 1.0
- model_cost 92.0 (13 domains*3 + 12 families*4 +5)
- data 0.0 exception 0.0 residual 0

M6-M9 TOTAL 1615-1639 exact 0/85 residual 85/85 FAIL - DERIVED_QAC obsolete

## FULL Quran 6236 Ayat
WINNER M11 TOTAL 2025.0 exact 6236/6236 rate 1.0 missing 0
- domains 32, families 481, model_cost 2025.0
- data 0.0 exception 0.0

M10 TOTAL 117593.0 exact 37/6236 rate 0.006 missing 6151 - FAIL on full
M6-M9 TOTAL 118484.0 exact 0/6236 missing 6151 - FAIL

MDL Saving: M11 saves 115568 bits over M10 on full corpus.

Source: quranic-corpus-morphology-0.4.txt 128220 lines
Gold: first token per ayah, domain=POS, family=ROOT split("|")[0]
