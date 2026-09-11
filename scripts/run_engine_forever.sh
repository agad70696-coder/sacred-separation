#!/data/data/com.termux/files/usr/bin/bash
cd ~/structural-grammar
mkdir -p reports
while true; do
  echo "[$(date)] ENGINE START"
  python scripts/engine_autonomous_REAL.py >> reports/engine.log 2>&1
  echo "[$(date)] ENGINE DIED - RESTART IN 10s"
  sleep 10
done
