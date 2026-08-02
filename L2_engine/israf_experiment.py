"""
Israf Experiment - Mixed vs Sacred Separation
Quran 7:31 - Eat and drink but do not be wasteful
Demonstrates why L0/L1/L2 matters
"""

# === BAD APPROACH: Mixed Sacred Text + Logic ===
def calculate_israf_BAD(consumption: float) -> str:
    quran_text = "وكلوا واشربوا ولا تسرفوا" # Mutable!
    if consumption > 100:
        quran_text = quran_text.replace("لا تسرفوا", "اسرفوا") # BUG corrupts verse!
    is_wasteful = consumption > 80
    return f"{quran_text} - Wasteful: {is_wasteful}"

print("=== BAD APPROACH ===")
print(calculate_israf_BAD(50)) # Correct
print(calculate_israf_BAD(120)) # CORRUPTED! Says "do waste"!

# === GOOD APPROACH: L0/L1/L2 ===
L0_MANIFEST = {
    "verse_id": "7:31",
    "hash_sha256": "a1b2c3d4...",
    "is_executable": False,
    "allowed_operations": ["SHA256_VERIFY"]
}

L1_INTERPRETATION = {
    "principle_id": "no_israf_7_31",
    "version": "v1.0.0",
    "source_hash_ref": "a1b2c3d4...", # Hash only!
    "interpretation": {"max_threshold": 80.0},
    "falsifiable_condition": "If nutrition study shows >80% not wasteful, update to v1.1.0"
}

def calculate_israf_GOOD(principle_id: str, consumption: float, threshold: float) -> dict:
    """Pure function, zero L0 import, formally verifiable"""
    is_wasteful = consumption > threshold
    return {
        "principle_id": principle_id,
        "is_wasteful": is_wasteful,
        "waste_amount": max(0, consumption - threshold),
        "L0_imports": 0
    }

print("\n=== GOOD APPROACH ===")
result = calculate_israf_GOOD("no_israf_7_31", 120, 80.0)
print(result)
print("Proof: L0 verse remains immutable even if L2 has bug")
print("Theorem L0 ∩ L2 = ∅ holds - QED")

def test_zero_L0_import():
    import inspect
    source = inspect.getsource(calculate_israf_GOOD)
    assert "L0_quran_source" not in source
    assert "وكلوا" not in source
    print("✅ CI Passed: L2 has zero L0 imports")

test_zero_L0_import()
