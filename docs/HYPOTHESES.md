# Hypotheses

H1: Physical filesystem separation is sufficient to enforce L0 ∩ L2 = ∅
Test: CI check for forbidden imports

H2: Hash-only reference prevents transitive corruption
Test: L2 bug does not change L0 hash

H3: Falsifiable L1 improves auditability vs hardcoded verses
Test: Compare BAD vs GOOD in israf_experiment.py

Falsification Condition: 
If any L2 module can import L0 content without CI failure, H1 is falsified and pattern is invalid.
