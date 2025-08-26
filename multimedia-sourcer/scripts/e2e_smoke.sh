#!/usr/bin/env bash
set -euo pipefail
API_BASE="http://localhost:8000"
echo "Waiting for API..."; for i in {1..60}; do curl -sf "$API_BASE/health" >/dev/null && break; sleep 2; done
WEB_ID=$(curl -sS -X POST -H "Content-Type: application/json" -d '{"source_type":"web","url_or_path":"file:///app/samples/sample.html"}' $API_BASE/v1/sources/json | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
PDF_ID=$(curl -sS -F "source_type=pdf" -F "file=@api/samples/sample.pdf" $API_BASE/v1/sources | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
YT_ID=$(curl -sS -X POST -H "Content-Type: application/json" -d '{"source_type":"youtube","url_or_path":"https://youtube.com/watch?v=abc"}' $API_BASE/v1/sources/json | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
JOB_ID=$(curl -sS -X POST -H "Content-Type: application/json" -d "{\"source_ids\":[\"$WEB_ID\",\"$PDF_ID\",\"$YT_ID\"]}" $API_BASE/v1/pipelines/run | python3 -c 'import sys,json; print(json.load(sys.stdin)["job_id"])')
for i in {1..120}; do J=$(curl -sS $API_BASE/v1/jobs/$JOB_ID); S=$(echo "$J" | python3 -c 'import sys,json; print(json.load(sys.stdin)["status"])'); echo "Status: $S"; [ "$S" = "completed" ] && break; [ "$S" = "failed" ] && { echo "$J"; exit 1; }; sleep 2; done
ls -1 data/exports || true
