#!/bin/bash
# Fast health check loop for Streamlit startup
# Waits for Streamlit to be ready with minimal delay
#
# Usage: ./fast-health-check.sh [url] [max_attempts] [sleep_interval]
#   url: Streamlit URL (default: http://localhost:8501)
#   max_attempts: Maximum number of attempts (default: 30)
#   sleep_interval: Seconds between attempts (default: 0.3)
#
# Returns: 0 if healthy, 1 if timed out

URL="${1:-http://localhost:8501}"
MAX_ATTEMPTS="${2:-30}"
SLEEP_INTERVAL="${3:-0.3}"

echo "⏳ Waiting for Streamlit at $URL..."

for i in $(seq 1 $MAX_ATTEMPTS); do
    # Check health endpoint (silent, fail quickly)
    if curl -sf --max-time 1 "${URL}/_stcore/health" > /dev/null 2>&1; then
        echo "✅ Streamlit is ready! (attempt $i/${MAX_ATTEMPTS})"
        exit 0
    fi
    
    # Also check main page as fallback
    if curl -sf --max-time 1 "${URL}" > /dev/null 2>&1; then
        echo "✅ Streamlit is ready! (attempt $i/${MAX_ATTEMPTS})"
        exit 0
    fi
    
    # Brief sleep between attempts
    sleep "$SLEEP_INTERVAL"
done

echo "❌ Streamlit did not start within $((MAX_ATTEMPTS * SLEEP_INTERVAL))s"
exit 1
