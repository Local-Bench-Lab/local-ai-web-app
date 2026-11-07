#!/bin/bash
# V3: the three pages at rest (Home, Leaderboard with static bars, Request in its default state), then a visual check at 3 widths.
step() { printf '\n\033[1;33m== %s ==\033[0m\n' "$1"; }
CHECK="Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. Check it in Chrome at 390, 768 and 1440 px wide against design/."

step "developer (Qwen 3.8): Home"
time opencode run --agent developer "Build the Home page from design/home.png and design/home_mobile.png with the existing components and the real numbers in data/results.json. Make it the default view of the app. $CHECK"

step "developer (Qwen 3.8): Leaderboard"
time opencode run -c --agent developer "Build the Leaderboard page from design/leaderboard_ranked.png at /?view=leaderboard, with RaceBar and data/results.json. Static bars, sorted fastest first, no animation yet. Link it from the Nav. $CHECK"

step "developer (Qwen 3.8): Request"
time opencode run -c --agent developer "Build the Request page from design/request.png at /?view=request: the form in its default state, using Field and Button. No sending yet. Link it from the Nav. $CHECK"

step "visual-checker (Gemma 4): all three pages"
time opencode run --agent visual-checker "Open http://localhost:5173/, /?view=leaderboard and /?view=request in Chrome at 390, 768 and 1440 px wide. Compare each with design/home.png, design/home_mobile.png, design/leaderboard_ranked.png and design/request.png. List concrete problems, or say PASS."

step "the automatic checks"
docker exec -u 1000:1000 -e HOME=/config -w /config/bench-board-app recorder sh -c 'npm run typecheck && npm run lint && npm test'
echo "PAGES-RUN-""FINISHED"
