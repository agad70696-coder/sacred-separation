# Structural Grammar of the Quran via MDL

**Source:** quranic-corpus-morphology-0.4.txt 128220 lines
**Gold:** first token per ayah, domain=POS, family=ROOT split("|")[0]

## Abstract
MDL: TOTAL = L(M)+L(D|M)
- 85 ayat: WINNER M10 TOTAL 92.0 exact 85/85 rate 1.0
- FULL 6236 ayat: WINNER M11 TOTAL 2025.0 exact 6236/6236 rate 1.0
- Saving: M11 saves 115568 bits over M10 on full corpus.

## Results
### 85 Ayat
M10 92.0 exact 85/85 WINNER
M6-M9 1615-1639 exact 0/85 FAIL DERIVED_QAC obsolete

### FULL 6236
M11 2025.0 domains 32 families 481 exact 6236/6236 WINNER missing 0
M10 117593.0 exact 37/6236 missing 6151 FAIL
M6-M9 118484.0 exact 0/6236 missing 6151 FAIL

Figure: figures/mdl_winners.png
