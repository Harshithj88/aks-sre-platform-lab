#!/bin/bash
# Load test script for demo-api using hey (HTTP load generator)
# Install: go install github.com/rakyll/hey@latest
# Or: brew install hey
#
# Usage:
#   ./load-test.sh                          # defaults (200 requests, 10 concurrent)
#   ./load-test.sh https://api.example.com  # custom target
#   REQUESTS=1000 CONCURRENCY=50 ./load-test.sh

set -euo pipefail

# Configuration
TARGET_URL="${1:-http://localhost:8080/health}"
REQUESTS="${REQUESTS:-200}"
CONCURRENCY="${CONCURRENCY:-10}"
DURATION="${DURATION:-}"  # If set, overrides REQUESTS (e.g., "30s")

echo "========================================"
echo "  Load Test — demo-api"
echo "========================================"
echo "  Target:      $TARGET_URL"
echo "  Requests:    $REQUESTS"
echo "  Concurrency: $CONCURRENCY"
if [ -n "$DURATION" ]; then
  echo "  Duration:    $DURATION"
fi
echo "========================================"
echo ""

# Verify hey is installed
if ! command -v hey &> /dev/null; then
  echo "ERROR: 'hey' is not installed."
  echo "Install with: go install github.com/rakyll/hey@latest"
  echo "Or:           brew install hey"
  exit 1
fi

# Verify target is reachable
echo "Checking connectivity to $TARGET_URL..."
if ! curl -sf -o /dev/null --max-time 5 "$TARGET_URL"; then
  echo "WARNING: Target may be unreachable. Proceeding anyway..."
fi
echo ""

# --- Test 1: Health endpoint (GET) ---
echo ">>> Test 1: GET $TARGET_URL (baseline)"
if [ -n "$DURATION" ]; then
  hey -z "$DURATION" -c "$CONCURRENCY" "$TARGET_URL"
else
  hey -n "$REQUESTS" -c "$CONCURRENCY" "$TARGET_URL"
fi
echo ""

# --- Test 2: Increased concurrency ---
HIGH_CONCURRENCY=$((CONCURRENCY * 5))
echo ">>> Test 2: GET $TARGET_URL (high concurrency: $HIGH_CONCURRENCY)"
if [ -n "$DURATION" ]; then
  hey -z "$DURATION" -c "$HIGH_CONCURRENCY" "$TARGET_URL"
else
  hey -n "$REQUESTS" -c "$HIGH_CONCURRENCY" "$TARGET_URL"
fi
echo ""

# --- Test 3: POST with payload (if applicable) ---
API_URL="${TARGET_URL%/health}/api/demo"
echo ">>> Test 3: POST $API_URL (with JSON payload)"
if [ -n "$DURATION" ]; then
  hey -z "$DURATION" -c "$CONCURRENCY" -m POST \
    -H "Content-Type: application/json" \
    -d '{"name":"load-test","value":"test-data"}' \
    "$API_URL" || echo "  (POST endpoint may not exist — skipped)"
else
  hey -n "$REQUESTS" -c "$CONCURRENCY" -m POST \
    -H "Content-Type: application/json" \
    -d '{"name":"load-test","value":"test-data"}' \
    "$API_URL" || echo "  (POST endpoint may not exist — skipped)"
fi
echo ""

echo "========================================"
echo "  Load test complete"
echo "========================================"
