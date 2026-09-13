#!/usr/bin/env python3
import json, pathlib
def main():
    print("L2 Engine V8 REAL - Core")
    mp = pathlib.Path(__file__).parent.parent / "L0_quran_source" / "manifest.json"
    data = json.loads(mp.read_text(encoding="utf-8"))
    assert not data["integrity"]["is_executable"]
    print("OK V8 REAL")
if __name__ == "__main__":
    main()
