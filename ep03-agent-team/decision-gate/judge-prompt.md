# The judge prompt (Qwen 3.8 picks which agent runs next)

Send this to `qwen3.8-128k` with temperature 0. In the video it answered with JSON: `choice` (one of the agent names) and a short `reason`.

```
Which agent should run next?

State: <what just happened, e.g. "The CSS reviewer found 6 problems: raw colours and hard-coded spacing.">

Agents:
- developer: Fix the problems a reviewer or checker just found, then re-check.
- design-reader: Read exact styles, sizes and prototype links from the FigCraft design file
- visual-checker: Take screenshots of the page at phone, tablet and desktop width and look for layout problems
- react-reviewer: Review React component code: props, hooks, state and file structure
- css-reviewer: Review CSS: design tokens instead of raw values, responsive media queries
- test-engineer: Write or fix unit tests and run them
- a11y-perf-auditor: Run an accessibility and performance audit (Lighthouse, performance trace)
- security-reviewer: Review backend code for input validation, injection and secrets
- contract-checker: Check that frontend types and backend API responses match
- done: Nothing left to check for this step; move on to the next plan step

Answer with the single best agent.
```
