import json, pathlib, re
src_path = pathlib.Path.home() / "apex44-zero/PHASE2_CLEAN/source/quranic-corpus-morphology-0.4.txt"
out_path = pathlib.Path("gold/gold_FULL_6236.jsonl")

# regex بيستحمل اي ترتيب POS / ROOT
line_re = re.compile(r"\((\d+):(\d+):(\d+):(\d+)\)")

first_per_ayah = {} # (sura,aya) -> record with smallest word

for line in open(src_path, encoding='utf-8', errors='ignore'):
    m = line_re.search(line)
    if not m:
        continue
    sura, aya, word, seg = map(int, m.groups())
    # اطلع FORM و POS و ROOT بأي ترتيب
    form_match = re.search(r"\s+(\S+)\s+.*POS:(\S+)", line)
    root_match = re.search(r"ROOT:(\S+)", line)
    pos_match = re.search(r"POS:([A-Z]+)", line)
    if not pos_match:
        continue
    pos = pos_match.group(1)
    root = root_match.group(1) if root_match else "UNK"
    # FORM هو اول توكن بعد القوس
    parts = line.split()
    form = parts[1] if len(parts) > 1 else "UNK"

    key = (sura, aya)
    # خد اول كلمة بس في كل اية
    if key not in first_per_ayah or word < first_per_ayah[key]["word"]:
        first_per_ayah[key] = {
            "sura": sura, "aya": aya, "word": word,
            "domain": pos, "family": root, "entry": form,
            "source": f"{sura}:{aya}:{word}"
        }

records = sorted(first_per_ayah.values(), key=lambda x: (x["sura"], x["aya"]))
print(f"Found {len(records)} ayat, expected 6236")

with open(out_path, "w", encoding="utf-8") as w:
    for r in records:
        w.write(json.dumps(r, ensure_ascii=False)+"\n")

print(f"WROTE {out_path} {len(records)} records")
print(f"Domains {len(set(r['domain'] for r in records))} Families {len(set(r['family'] for r in records))}")
