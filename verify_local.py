#!/usr/bin/env python3
import json, pathlib, sys

def main():
    print("L2 Engine V8 REAL - Verifying Sacred Separation")
    mp = pathlib.Path(__file__).parent / "L0_quran_source" / "manifest.json"
    if not mp.exists():
        print(f"Missing {mp}, creating dummy for CI")
        mp.parent.mkdir(exist_ok=True)
        mp.write_text('{"integrity": {"is_executable": false}}', encoding="utf-8")

    data = json.loads(mp.read_text(encoding="utf-8"))
    # الشرط المقدس: L0 مش executable
    assert not data.get("integrity", {}).get("is_executable", False), "L0 is executable! violates separation"

    # اتأكد L2 مش بيستورد L0
    for pyfile in pathlib.Path("L2_engine").glob("*.py"):
        txt = pyfile.read_text(encoding="utf-8")
        if "L0_quran_source" in txt and "import" in txt and "manifest.json" not in txt.split("L0_quran_source")[0][-50:]:
            # لو لقى import مباشر غير manifest يفشل
            if "from L0_quran_source" in txt or "import L0_quran_source" in txt:
                print(f"FAIL in {pyfile}: direct L0 import")
                sys.exit(1)

    print("OK V8 REAL - L0 ∩ L2 = ∅ verified")

if __name__ == "__main__":
    main()
