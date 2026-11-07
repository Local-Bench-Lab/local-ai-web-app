#!/bin/bash
# V4 run B: confirm the visual-checker's list, unit tests, accessibility, then performance before and after one fix.
step() { printf '\n\033[1;33m== %s ==\033[0m\n' "$1"; }
CHECK="Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173."

step "developer (Qwen 3.8): check Gemma's list"
time opencode run --agent developer "The visual-checker (Gemma 4) compared the leaderboard race, the details card, the mobile menu and the request error state with design/ and reported: tabs too tight, a cut-off suffix and a wrong active-tab shade on the leaderboard, uneven spacing in the details card, the Request a test link overlapping a divider in the mobile menu, and the error text indented on the request form. Gemma is a fast first look and can be wrong: check each one yourself in Chrome against the design image, say which are real, and fix only the real ones. $CHECK"

step "test-engineer (Qwen 3.8): tests and coverage"
time opencode run --agent test-engineer "Run npm test -- --coverage. Add tests for what is not covered in the race animation (reduced motion shows the end state at once), the details card (opens and closes with the keyboard) and the drawer (Escape closes it). Report pass/fail and the coverage numbers."

step "a11y-perf-auditor (gpt-oss 120B): accessibility"
time opencode run --agent a11y-perf-auditor "Run a Lighthouse accessibility audit with the chrome tools on http://localhost:5173/, /?view=leaderboard and /?view=request at 390 px wide. Report each score and the top 3 problems with the element they are on."

step "developer (Qwen 3.8): accessibility fix"
time opencode run --agent developer "Fix the top accessibility problems from the audit: run a Lighthouse accessibility audit on /, /?view=leaderboard and /?view=request at 390 px yourself first, fix what it flags (contrast on the dark theme, labels, focus), and run it again. Report the scores before and after. $CHECK"

step "a11y-perf-auditor (gpt-oss 120B): performance, before"
time opencode run --agent a11y-perf-auditor "Record a performance trace with the chrome tools of http://localhost:5173/?view=leaderboard loading and the race playing, with 4x CPU slowdown and Slow 4G. Report LCP, CLS and any long tasks or layout shifts, and the top 3 fixes."

step "developer (Qwen 3.8): performance fix, then trace again"
time opencode run --agent developer "Record a performance trace of http://localhost:5173/?view=leaderboard loading with the race playing (4x CPU slowdown, Slow 4G) with the chrome tools. Fix the biggest problem it shows (for example layout shifts from the bars or count-up, a font that blocks render, work in long tasks), then trace again with the same settings. Report LCP and CLS before and after. $CHECK"

step "the automatic checks"
docker exec -u 1000:1000 -e HOME=/config -w /config/bench-board-app recorder sh -c 'npm run typecheck && npm run lint && npm test'
echo "V4B-RUN-""FINISHED"
