# Ep 5: Animations, tests, accessibility, speed

The agent team makes the frontend interactive (the leaderboard race, form states, the mobile menu), then tests it, checks accessibility with Lighthouse, and makes it load faster. Every prompt from the video is below, in order, including the failed attempts.

## What you need

- The app from [Ep 4](../ep04-frontend-1), with the dev server running (`npm run dev`).
- Chrome DevTools MCP from [Ep 2](../ep02-agent-setup): Lighthouse audits and performance traces run through it.

After every step, run the checks yourself:

```bash
npm run typecheck && npm run lint && npm test
```

## 1. Form states and the mobile menu
```bash
opencode run --agent developer "On the Request page (/?view=request) add the form states from design/request_error.png, request_sending.png and request_done.png: submit while empty shows the errors, a bad email shows its error, a valid form shows Sending, then success with \"Thanks, it's on the list\" (no backend yet: fake a 1 second wait). On mobile, the hamburger opens the drawer from design/menu_open.png, sliding in from the right; a link closes it and navigates. Also the Home hero text and cards fade and slide up on load, staggered. Add tests for each form state and the drawer. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173: check your work in Chrome at 390 and 1440 px wide and compare it with design/."
```

## 2. The leaderboard race, in small steps

First try, one big prompt (**failed attempt**):
```bash
opencode run --agent developer "Add the race animation to the Leaderboard at /?view=leaderboard, as in design/brief.md and design/race-start.png, race-grown.png, race-ranked.png: bars start at 0, grow to their values while the numbers count up, then reorder fastest first. Animate transform, not width. Respect prefers-reduced-motion (show the end state at once). Clicking a bar expands its details card as in design/details.png. Add tests for the end order and the details card. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173: check your work in Chrome at 390 and 1440 px wide and compare it with design/."
```

Second try, three small prompts that each say "keep your thinking short":
```bash
opencode run --agent developer "On the Leaderboard (/?view=leaderboard) make the bars grow from 0 to their values when the page opens, about 1.2 seconds, while each number counts up from 0. Animate transform: scaleX, not width. With prefers-reduced-motion, show the end state at once. Add a test for the reduced-motion case. Keep your thinking short: write the code first, then check it. Change only the files you need. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173."
```

```bash
opencode run --agent developer "On the Leaderboard, after the bars have grown, reorder them fastest first with a short slide (FLIP: measure, then animate translateY), as in design/race-grown.png then design/race-ranked.png. Add a test that the final order is fastest first. Keep your thinking short: write the code first, then check it. Change only the files you need. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173."
```

```bash
opencode run --agent developer "On the Leaderboard, clicking a bar (or Enter on it) expands a details card under it, as in design/details.png, with the model's real numbers from data/results.json; clicking again or Escape closes it. Add tests for open and close. Keep your thinking short: write the code first, then check it. Change only the files you need. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173."
```

## 3. The visual check of the motion
```bash
opencode run --agent visual-checker "Open http://localhost:5173/?view=leaderboard at 1440 px wide. Take a screenshot right away and another after 3 seconds, and compare them with design/race-start.png and design/race-ranked.png. Click the first bar and compare with design/details.png. Then at 390 px open the menu and compare with design/menu_open.png. On /?view=request press Send with the form empty and compare with design/request_error.png. List concrete problems, or say PASS."
```

Don't trust the list blindly: have the developer check each point first. Replace the list in this prompt with what your visual checker reported.
```bash
opencode run --agent developer "The visual-checker (Gemma 4) compared the leaderboard race, the details card, the mobile menu and the request error state with design/ and reported: tabs too tight, a cut-off suffix and a wrong active-tab shade on the leaderboard, uneven spacing in the details card, the Request a test link overlapping a divider in the mobile menu, and the error text indented on the request form. Gemma is a fast first look and can be wrong: check each one yourself in Chrome against the design image, say which are real, and fix only the real ones. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173."
```

## 4. Tests
```bash
opencode run --agent test-engineer "Run npm test -- --coverage. Add tests for what is not covered in the race animation (reduced motion shows the end state at once), the details card (opens and closes with the keyboard) and the drawer (Escape closes it). Report pass/fail and the coverage numbers."
```

## 5. Accessibility
```bash
opencode run --agent a11y-perf-auditor "Run a Lighthouse accessibility audit with the chrome tools on http://localhost:5173/, /?view=leaderboard and /?view=request at 390 px wide. Report each score and the top 3 problems with the element they are on."
```

```bash
opencode run --agent developer "Fix the top accessibility problems from the audit: run a Lighthouse accessibility audit on /, /?view=leaderboard and /?view=request at 390 px yourself first, fix what it flags (contrast on the dark theme, labels, focus), and run it again. Report the scores before and after. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173."
```

## 6. Speed: trace, fix, trace again
```bash
opencode run --agent a11y-perf-auditor "Record a performance trace with the chrome tools of http://localhost:5173/?view=leaderboard loading and the race playing, with 4x CPU slowdown and Slow 4G. Report LCP, CLS and any long tasks or layout shifts, and the top 3 fixes."
```

```bash
opencode run --agent developer "Record a performance trace of http://localhost:5173/?view=leaderboard loading with the race playing (4x CPU slowdown, Slow 4G) with the chrome tools. Fix the biggest problem it shows (for example layout shifts from the bars or count-up, a font that blocks render, work in long tasks), then trace again with the same settings. Report LCP and CLS before and after. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173."
```

## 7. The checks
```bash
npm run typecheck && npm run lint && npm test
```

## Results in the video

- **The race, first try:** 93 minutes and no code. Qwen's last answer hit the 32,000-token limit for one reply before it wrote anything.
- **The race, second try (three small prompts):** the bars grow in 76 minutes (Qwen wrote the file after 17 minutes, 49/49 tests). The reorder took 132 minutes: it still thought for about 93,000 tokens before its first edit, but no single answer hit the limit, so it got to the code; it fixed two type errors and a failing test (52/52). The details card took 53 minutes (60/60). Reduced motion shows the end state at once. A reboot cut the first try at part 2, so part 2 was run again.
- **Form states, mobile drawer, home fade-in:** done in 66 minutes, with 39/39 tests.
- **Visual check:** Gemma 4 listed problems, and Qwen measured each one in Chrome. None of the 6 problems it checked was real, so always check the checker.
- **Tests:** no new tests, because the features it was asked to test hadn't been built yet. It also installed a coverage tool without asking.
- **Accessibility:** every page already scored 100. The real fix was making the leaderboard tabs work with the arrow keys, plus 8 tests (47/47).
- **Speed:** splitting the code per page (React.lazy) cut the leaderboard's LCP from 5.1 s to 3.9 s. CLS was 0.00 before and after.

## Next

[Ep 6: the backend, part 1](../ep06-backend-1)
