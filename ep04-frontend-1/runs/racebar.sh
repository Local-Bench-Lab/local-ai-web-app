#!/bin/bash
# V3: continue the RaceBar step (the components run hit its 3-hour recording cap mid-step), then the checks.
step() { printf '\n\033[1;33m== %s ==\033[0m\n' "$1"; }
CHECK="Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173: check your work in Chrome at 390 and 1440 px wide and compare it with design/."

step "developer (Qwen 3.8): finish RaceBar"
time opencode run -c --agent developer "Continue where you stopped: finish RaceBar using the real numbers in data/results.json, with a test file, and add it to the gallery. $CHECK"

step "the automatic checks"
docker exec -u 1000:1000 -e HOME=/config -w /config/bench-board-app recorder sh -c 'npm run typecheck && npm run lint && npm test'
echo "RACEBAR-RUN-""FINISHED"
