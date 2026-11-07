# Ep 4: Local AI builds the frontend

📺 Video: https://youtu.be/ygrqkF7pN4g

The agent team writes the Bench Board frontend: from the FigCraft design to three real pages (Home, Leaderboard, Request), in React, Vite and TypeScript. Every prompt from the video is below, in order, including the failed attempts.

## What you need

- [Ep 2](../ep02-agent-setup): the models and `opencode.json`.
- [Ep 3](../ep03-agent-team): the agents and `AGENTS.md`.
- The Ep 1 design open in FigCraft ([`../app-starter/bench-board.figcraft`](../app-starter/bench-board.figcraft)).
- Node 22 and npm.
- Time. Local models are slow: this episode took about 13 hours of agent time on the GB10. Every step runs on its own, so you can stop and come back.

**How the prompts work:** each step is `opencode run --agent <name> "<prompt>"`. `-c` continues the last session, so the agent remembers what came before. After every step, run the three checks yourself:

```bash
npm run typecheck && npm run lint && npm test
```

## 0. The starter app (by hand)

```bash
node --version && npm --version
npm create vite@latest bench-board-app -- --template react-ts --no-interactive
cd bench-board-app
npm install
npm install --save-dev vitest jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom
npm pkg set scripts.test='vitest run --passWithNoTests' scripts.typecheck='tsc -b --noEmit'
npm run lint && npm run typecheck && npm test
npm run dev
```

Leave the dev server running (http://localhost:5173) and open a second terminal in the app folder for the agents. Then copy into the app folder:
- `design/` and `data/` from [`../app-starter`](../app-starter)
- `opencode.json` from [Ep 2](../ep02-agent-setup)
- `AGENTS.md` and `.opencode/` from [Ep 3](../ep03-agent-team)

## 1. The folder structure: two models check each other

gpt-oss suggests, Qwen checks (`-c` keeps the same session, so it sees the suggestion):

```bash
opencode run --agent planner "Suggest the folder structure for the Bench Board app: React, Vite and TypeScript, following AGENTS.md and design/brief.md. Pages: Home, Leaderboard, Request. Components: Button, Nav, Drawer, Card, Field, RaceBar. Plus design tokens, data and tests. Show it as a tree of at most 30 lines, then one short line on why for each top-level folder. Do not create any files."
opencode run -c --agent developer "Check the folder structure above against AGENTS.md. List anything that breaks a rule or is missing, then give your corrected tree. Do not create any files."
```

Then swap them, and merge the best of both trees yourself:

```bash
opencode run --agent developer "Suggest the folder structure for the Bench Board app: React, Vite and TypeScript, following AGENTS.md and design/brief.md. Pages: Home, Leaderboard, Request. Components: Button, Nav, Drawer, Card, Field, RaceBar. Plus design tokens, data and tests. Show it as a tree of at most 30 lines, then one short line on why for each top-level folder. Do not create any files."
opencode run -c --agent planner "Check the folder structure above against AGENTS.md. List anything that breaks a rule or is missing, then give your corrected tree. Do not create any files."
```

## 2. Design tokens straight from FigCraft

Open `app-starter/bench-board.figcraft` in FigCraft (the Ep 1 design), then:

```bash
opencode run --agent developer "Ask the design-reader agent to read every colour style and every text style from the open FigCraft file. Then write src/styles/tokens.css with one CSS custom property per style: colours as hex, and for each text style its font family, weight, size and line height in px. Use only values that come from FigCraft."
```

## 3. Plan, then the components

The planner (gpt-oss) writes the plan:
```bash
opencode run --agent planner "Plan the Bench Board frontend in at most 7 steps. Components first: Button (Primary and Secondary), Card (a latest-test card), Field (labelled input with an error state), Nav (desktop links, and on mobile a hamburger that opens the Drawer), RaceBar (one static bar: model name, coloured bar, tok/s). Then the pages Home, Leaderboard (static bars, no animation yet) and Request (default form state). Add a component gallery at /?view=components for checking components."
```

The developer (Qwen 3.8) builds it, one part at a time. `-c` continues the same session, so it remembers the plan:
```bash
opencode run -c --agent developer "Do the first part of the plan: import src/styles/tokens.css in src/main.tsx, remove the Vite demo content, add the component gallery at /?view=components, then build Button and Card with a test file each. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173: check your work in Chrome at 390 and 1440 px wide and compare it with design/."
```

```bash
opencode run -c --agent developer "Next part of the plan: build Field, Nav and Drawer, with a test file each, and add them to the gallery. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173: check your work in Chrome at 390 and 1440 px wide and compare it with design/."
```

```bash
opencode run -c --agent developer "Next part of the plan: build RaceBar using the real numbers in data/results.json, with a test file, and add it to the gallery. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173: check your work in Chrome at 390 and 1440 px wide and compare it with design/."
```

If it stops before RaceBar is done, continue it:
```bash
opencode run -c --agent developer "Continue where you stopped: finish RaceBar using the real numbers in data/results.json, with a test file, and add it to the gallery. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. The dev server is already running on http://localhost:5173: check your work in Chrome at 390 and 1440 px wide and compare it with design/."
```

Then the three checks:
```bash
npm run typecheck && npm run lint && npm test
```

## 4. The review loop

Three reviewers look at the component gallery:
```bash
opencode run --agent visual-checker "Open http://localhost:5173/?view=components in Chrome and take a screenshot at 390, 768 and 1440 px wide. Compare the components with design/home.png, design/home_mobile.png and design/request.png. List concrete problems, or say PASS."
```

```bash
opencode run --agent react-reviewer "Review the React code in src/components and src/pages. List concrete problems with file and line, most important first, at most 8. Say PASS if there are none."
```

```bash
opencode run --agent css-reviewer "Review the CSS modules in src/components against src/styles/tokens.css. List concrete problems with file and line, most important first, at most 8. Say PASS if there are none."
```

Ask the judge which agent goes next with the [judge prompt](../ep03-agent-team/decision-gate/judge-prompt.md), giving it the end of each review as the state. If it says `developer`, paste the findings into:

```bash
opencode run --agent developer "Fix these review findings in src/components, most important first: <the reviewers' findings> Then run npm run typecheck, npm run lint and npm test, and check http://localhost:5173/?view=components in Chrome at 390 and 1440 px."
```

Then review again. I capped it at 2 rounds.

## 5. The pages

Home, first try (**failed attempt**):
```bash
opencode run --agent developer "Build the Home page from design/home.png and design/home_mobile.png with the existing components and the real numbers in data/results.json. Make it the default view of the app. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. Check it in Chrome at 390, 768 and 1440 px wide against design/."
```

Home, second try:
```bash
opencode run --agent developer "Build the Home page as src/pages/Home/Home.tsx from design/home.png and design/home_mobile.png. Look at the two images directly (you can see images); do not write scripts to decode them, and use only the tokens in src/styles/tokens.css. Use the existing components and the real numbers in data/results.json. Make it what / shows, replacing the placeholder in App.tsx, and link it from the Nav. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. Check it in Chrome at 390, 768 and 1440 px wide against design/."
```

Leaderboard:
```bash
opencode run -c --agent developer "Build the Leaderboard page from design/leaderboard_ranked.png at /?view=leaderboard, with RaceBar and data/results.json. Static bars, sorted fastest first, no animation yet. Link it from the Nav. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. Check it in Chrome at 390, 768 and 1440 px wide against design/."
```

If the order isn't fastest first:
```bash
opencode run -c --agent developer "The Leaderboard at /?view=leaderboard is not sorted fastest first: LFM2.5 at 121.2 tok/s should be on top and Qwen 3.8 at 23.6 at the bottom. Fix it and add a test that checks the order. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. Check it in Chrome at 390, 768 and 1440 px wide against design/."
```

Request:
```bash
opencode run -c --agent developer "Build the Request page from design/request.png at /?view=request: the form in its default state, using Field and Button. No sending yet. Link it from the Nav. Then run npm run typecheck, npm run lint and npm test, and fix anything that fails. Check it in Chrome at 390, 768 and 1440 px wide against design/."
```

The visual check of all three pages:
```bash
opencode run --agent visual-checker "Open http://localhost:5173/, /?view=leaderboard and /?view=request in Chrome at 390, 768 and 1440 px wide. Compare each with design/home.png, design/home_mobile.png, design/leaderboard_ranked.png and design/request.png. List concrete problems, or say PASS."
```

And the checks:
```bash
npm run typecheck && npm run lint && npm test
```

## What you should have at the end

Three pages that match the design at phone and desktop width, with typecheck, lint and tests all passing (I had 33/33 tests). On a phone, my Leaderboard still cut "Nemotron 3 Nano 30B" short.

## Results in the video

- **Folder structure:** each model caught things the other missed. I merged the two trees.
- **Design tokens:** 25 of 25 values matched the Ep 1 design, in about 10 minutes.
- **Components:** the developer installed a test package without waiting for an answer.
- **Review loop:** 2 h 41 min. The final CSS review said FAIL because "--space-12 does not exist", but it is in tokens.css, a file the reviewer had just read.
- **Pages, first try:** no Home page, and the Leaderboard came out alphabetical. All checks still passed, because nothing tested Home.
- **Pages, second try:** Home built, the Leaderboard sorted fastest first, and 33/33 tests passing.

## Next

[Ep 5: animations, tests, accessibility, speed](../ep05-frontend-2)
