#!/bin/bash
# V3: plan, then build the components with the developer agent (Qwen 3.8), one opencode run per step.
# The dev server already runs in the recorder container on http://localhost:5173.
step() { printf '\n\033[1;33m== %s ==\033[0m\n' "$1"; }
CHECK="Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173: check your work in Chrome at 390 and 1440 px wide and compare it with design/."

step "planner (gpt-oss): plan the frontend"
time opencode run --agent planner "Plan the Bench Board frontend in at most 7 steps. Components first: Button (Primary and Secondary), Card (a latest-test card), Field (labelled input with an error state), Nav (desktop links, and on mobile a hamburger that opens the Drawer), RaceBar (one static bar: model name, coloured bar, tok/s). Then the pages Home, Leaderboard (static bars, no animation yet) and Request (default form state). Add a component gallery at /?view=components for checking components."

step "developer (Qwen 3.8): app shell, gallery, Button, Card"
time opencode run -c --agent developer "Do the first part of the plan: import src/styles/tokens.css in src/main.tsx, remove the Vite demo content, add the component gallery at /?view=components, then build Button and Card with a test file each. $CHECK"

step "developer (Qwen 3.8): Field, Nav and Drawer"
time opencode run -c --agent developer "Next part of the plan: build Field, Nav and Drawer, with a test file each, and add them to the gallery. $CHECK"

step "developer (Qwen 3.8): RaceBar"
time opencode run -c --agent developer "Next part of the plan: build RaceBar using the real numbers in data/results.json, with a test file, and add it to the gallery. $CHECK"

step "the automatic checks"
docker exec -u 1000:1000 -e HOME=/config -w /config/bench-board-app recorder sh -c 'npm run typecheck && npm run lint && npm test'
echo "COMPONENTS-RUN-""FINISHED"
