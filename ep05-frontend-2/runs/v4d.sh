#!/bin/bash
# V4 run D: second try at the race. In run A, Qwen spent 93 minutes thinking (97,839 tokens, the last answer stopped at the
# 32,000-token limit) and wrote no file. This time: one small piece per step, and write the file first.
step() { printf '\n\033[1;33m== %s ==\033[0m\n' "$1"; }
CHECK="Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173."
SMALL="Keep your thinking short: write the code first, then check it. Change only the files you need."

step "developer (Qwen 3.8): race part 1, the bars grow"
time opencode run --agent developer "On the Leaderboard (/?view=leaderboard) make the bars grow from 0 to their values when the page opens, about 1.2 seconds, while each number counts up from 0. Animate transform: scaleX, not width. With prefers-reduced-motion, show the end state at once. Add a test for the reduced-motion case. $SMALL $CHECK"

step "developer (Qwen 3.8): race part 2, reorder fastest first"
time opencode run --agent developer "On the Leaderboard, after the bars have grown, reorder them fastest first with a short slide (FLIP: measure, then animate translateY), as in design/race-grown.png then design/race-ranked.png. Add a test that the final order is fastest first. $SMALL $CHECK"

step "developer (Qwen 3.8): the details card"
time opencode run --agent developer "On the Leaderboard, clicking a bar (or Enter on it) expands a details card under it, as in design/details.png, with the model's real numbers from data/results.json; clicking again or Escape closes it. Add tests for open and close. $SMALL $CHECK"

step "the automatic checks"
docker exec -u 1000:1000 -e HOME=/config -w /config/bench-board-app recorder sh -c 'npm run typecheck && npm run lint && npm test'
echo "V4D-RUN-""FINISHED"
