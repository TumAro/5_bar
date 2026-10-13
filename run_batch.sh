
#!/usr/bin/env bash
set -e
sed -i 's/^LOOPS = .*/LOOPS = 10/' src/sim2real.py

for i in 1 2 3; do
  echo "run $i $(date +%H:%M)"
  uv run python -m test.aruco_calibrate
  uv run python -m src.sim2real > /dev/null
  sleep 60   # servo cool-down
done
echo done
