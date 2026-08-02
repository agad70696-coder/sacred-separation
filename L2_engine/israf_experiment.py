"""
Israf Detection Experiment - L2 Implementation
Quantifiable application of L1 principle: no_israf_7_31_v1
Falsifiable experiment with real metrics
"""

from core import SacredSeparationEngine
import time
import json

class IsrafExperiment:
    def __init__(self):
        self.engine = SacredSeparationEngine()
        # Load L1 interpretation (hash-linked)
        with open('L1_interpretations/no_israf_7_31_v1.json') as f:
            self.l1 = json.load(f)
        self.results = []

    def detect_water_waste(self, water_used_liter: float, threshold=0.5) -> dict:
        """Detect wudu water waste > threshold from L1"""
        # L1 rule: 0.5 liter excess
        is_waste = water_used_liter > threshold
        result = {
            "type": "water_waste",
            "input": water_used_liter,
            "threshold": threshold,
            "is_israf": is_waste,
            "L1_ref": self.l1["interpretation_id"],
            "L0_hash_ref": self.l1["linked_L0_hash"][:16] + "..."
        }
        self.results.append(result)
        return result

    def detect_food_waste(self, edible_waste_grams: float) -> dict:
        """Zero edible waste per L1"""
        is_waste = edible_waste_grams > 0
        result = {
            "type": "food_waste",
            "input_grams": edible_waste_grams,
            "is_israf": is_waste,
            "principle": self.l1["principle"]
        }
        self.results.append(result)
        return result

    def run_experiment(self):
        print("=== Israf Experiment - Sacred Separation Pattern ===")
        print(f"L0 Hash verified: {self.engine.verify_l0_integrity()}")
        print(f"L1 Confidence: {self.l1['confidence_score']}")
        print(f"Falsifiable: {self.l1['falsifiable']}")
        
        # Simulated tests
        tests = [0.3, 0.6, 1.2]  # liters
        for t in tests:
            r = self.detect_water_waste(t)
            print(f"Water {t}L -> Israf: {r['is_israf']}")
        
        food_tests = [0, 50, 120]
        for f in food_tests:
            r = self.detect_food_waste(f)
            print(f"Food waste {f}g -> Israf: {r['is_israf']}")
        
        print("✓ Experiment completed - Results are quantifiable and falsifiable")
        return self.results

if __name__ == "__main__":
    exp = IsrafExperiment()
    exp.run_experiment()
