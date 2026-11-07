#!/bin/bash
# V4 run A: the prototype interactions from V1 (design/brief.md "Prototype flows" + the state frames in design/).
step() { printf '\n\033[1;33m== %s ==\033[0m\n' "$1"; }
CHECK="Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173: check your work in Chrome at 390 and 1440 px wide and compare it with design/."

step "developer (Qwen 3.8): the leaderboard race"
time opencode run --agent developer "Add the race animation to the Leaderboard at /?view=leaderboard, as in design/brief.md and design/race-start.png, race-grown.png, race-ranked.png: bars start at 0, grow to their values while the numbers count up, then reorder fastest first. Animate transform, not width. Respect prefers-reduced-motion (show the end state at once). Clicking a bar expands its details card as in design/details.png. Add tests for the end order and the details card. $CHECK"

step "developer (Qwen 3.8): form states and the mobile drawer"
time opencode run --agent developer "On the Request page (/?view=request) add the form states from design/request_error.png, request_sending.png and request_done.png: submit while empty shows the errors, a bad email shows its error, a valid form shows Sending, then success with \"Thanks, it's on the list\" (no backend yet: fake a 1 second wait). On mobile, the hamburger opens the drawer from design/menu_open.png, sliding in from the right; a link closes it and navigates. Also the Home hero text and cards fade and slide up on load, staggered. Add tests for each form state and the drawer. $CHECK"

step "visual-checker (Gemma 4): the motion, before and after"
time opencode run --agent visual-checker "Open http://localhost:5173/?view=leaderboard at 1440 px wide. Take a screenshot right away and another after 3 seconds, and compare them with design/race-start.png and design/race-ranked.png. Click the first bar and compare with design/details.png. Then at 390 px open the menu and compare with design/menu_open.png. On /?view=request press Send with the form empty and compare with design/request_error.png. List concrete problems, or say PASS."

step "the automatic checks"
docker exec -u 1000:1000 -e HOME=/config -w /config/bench-board-app recorder sh -c 'npm run typecheck && npm run lint && npm test'
echo "V4A-RUN-""FINISHED"
