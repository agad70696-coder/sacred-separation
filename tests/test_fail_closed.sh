#!/data/data/com.termux/files/usr/bin/bash
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GOLD="$ROOT/gold/gold_01_85.jsonl"
backup=""
if [ -f "$GOLD" ]; then
  backup="$GOLD.bak_test"
  mv "$GOLD" "$backup"
fi
set +e
OUT="$TMPDIR/mdl_test.out"
ERR="$TMPDIR/mdl_test.err"
rm -f "$OUT" "$ERR"
python "$ROOT/scripts/mdl_evaluator.py" > "$OUT" 2>"$ERR"
status=$?
set -e
if [ -n "$backup" ]; then
  mv "$backup" "$GOLD"
fi
if [ "$status" -eq 2 ] && grep -q "BLOCKED" "$ERR"; then
  echo "PASS: evaluator fails closed when Gold is missing"
  exit 0
fi
echo "FAIL: evaluator did not fail closed"
cat "$ERR"
exit 1
