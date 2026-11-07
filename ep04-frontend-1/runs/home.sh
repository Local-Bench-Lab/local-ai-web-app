#!/bin/bash
# V3: second pass after pages.sh. Home was never built (Qwen went off writing a PNG decoder in /tmp and was stopped
# by the permission guard), and the Leaderboard is not sorted fastest first. Same agents, tighter asks.
step() { printf '\n\033[1;33m== %s ==\033[0m\n' "$1"; }
CHECK="Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. Check it in Chrome at 390, 768 and 1440 px wide against design/."

step "developer (Qwen 3.8): Home, second try"
time opencode run --agent developer "Build the Home page as src/pages/Home/Home.tsx from design/home.png and design/home_mobile.png. Look at the two images directly (you can see images); do not write scripts to decode them, and use only the tokens in src/styles/tokens.css. Use the existing components and the real numbers in data/results.json. Make it what / shows, replacing the placeholder in App.tsx, and link it from the Nav. $CHECK"

step "developer (Qwen 3.8): Leaderboard sort"
time opencode run -c --agent developer "The Leaderboard at /?view=leaderboard is not sorted fastest first: LFM2.5 at 121.2 tok/s should be on top and Qwen 3.8 at 23.6 at the bottom. Fix it and add a test that checks the order. $CHECK"

step "visual-checker (Gemma 4): all three pages"
time opencode run --agent visual-checker "Open http://localhost:5173/, /?view=leaderboard and /?view=request in Chrome at 390, 768 and 1440 px wide. Compare each with design/home.png, design/home_mobile.png, design/leaderboard_ranked.png and design/request.png. List concrete problems, or say PASS."

step "the automatic checks"
docker exec -u 1000:1000 -e HOME=/config -w /config/bench-board-app recorder sh -c 'npm run typecheck && npm run lint && npm test'
echo "HOME-RUN-""FINISHED"
