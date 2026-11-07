# Ep 3: A team of 12 local AI agents

📺 Video: https://youtu.be/L1yxuCVJEho

One agent doing everything gets lost. Here we give the work to a **team**: each agent has one job, its own model, and only the tools it needs. They share a rule book (`AGENTS.md`) and skills. Then we run one full pass: plan, build, review, and a judge that decides what runs next.

## What you need

- The [Ep 2](../ep02-agent-setup) setup: the 128k models in Ollama, and `opencode.json` with FigCraft and Chrome DevTools.
- A project folder: Ep 4 creates the real app, but for this episode any empty folder works. Put [`../app-starter/design`](../app-starter/design) in it as `design/`.

## 1. Add the team to your project

Copy `AGENTS.md` and the whole `.opencode/` folder from here into your project folder:

```
your-project/
├── AGENTS.md              the rule book every agent reads
├── opencode.json          from Ep 2
├── design/                from app-starter
└── .opencode/
    ├── agent/             12 agents, one file each
    └── skills/            11 skills
```

Check that OpenCode sees them:

```bash
opencode agent list
```

⚠️ An agent can only be run directly with `opencode run --agent <name>` if its file says `mode: primary` or `mode: all`. Sub-agents (`mode: subagent`) can only be called by another agent. That's why most files here use `mode: all`.

## 2. The team

| Agent | Model | Job |
|---|---|---|
| planner | gpt-oss 120B | Breaks the work into small steps |
| developer | Qwen 3.8 27B | Builds one step at a time, checks it in Chrome (can see screenshots) |
| design-reader | Qwen 3.8 27B | Reads exact styles and sizes from the FigCraft file |
| visual-checker | Gemma 4 8B | Screenshots at phone, tablet and desktop width, looks for layout problems |
| react-reviewer | gpt-oss 120B | Reviews the React code |
| css-reviewer | gpt-oss 120B | Checks the CSS uses design tokens, not raw values |
| a11y-perf-auditor | gpt-oss 120B | Lighthouse accessibility and performance audits |
| test-engineer | Qwen 3.8 27B | Writes and runs tests |
| api-designer | gpt-oss 120B | Proposes the REST API (backend) |
| schema-reviewer | gpt-oss 120B | Reviews the database schema (backend) |
| security-reviewer | gpt-oss 120B | Input validation, injection, secrets (backend) |
| contract-checker | Qwen 3.8 27B | Checks that frontend and backend types match |

Open any file in [`.opencode/agent`](.opencode/agent) to see its exact prompt and tools.

The skills in [`.opencode/skills`](.opencode/skills) come from [agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani (MIT, licence included).

## 3. Try it: the design reader

With the Ep 1 design open in FigCraft:

```bash
opencode run --agent design-reader "What is the hex value of the accent colour style in the open FigCraft document? Answer with just the hex."
```

It should answer `#F5B942`. Mine took about two minutes.

## 4. One full pass of the loop, on a throwaway page

Plan it (gpt-oss), then build it (Qwen). `-c` continues the same session, so the developer sees the plan:

```bash
opencode run --agent planner "Plan a tiny throwaway page, playground/hello/index.html: a centred dark card on the bg colour, the heading Hello, Bench Board, and one amber button that says See the leaderboard. It must look right at 390 and 1440 px wide."
opencode run -c --agent developer "Build the plan above, step by step. Then open the page with the chrome tools at 390 and 1440 px wide and check it."
```

Review it:

```bash
opencode run --agent visual-checker "Check playground/hello/index.html at 390 and 1440 px wide."
opencode run --agent css-reviewer "Review the CSS in playground/hello/index.html. Its tokens are in its own :root block."
```

**My results:** the plan had 7 steps and took 1:17. The developer built and checked the page in about 6 minutes. The visual checker said pass, and the CSS reviewer found 6 real problems (raw colours, hard-coded spacing).

## 5. Who decides what runs next?

A judge model reads what just happened and picks the next agent. The exact prompt is in [`decision-gate/judge-prompt.md`](decision-gate/judge-prompt.md). Try it with these states:

- "The css-reviewer found raw colours (#8a93a6 and #0f1115) and hard-coded spacing in playground/hello/index.html." → should be `developer`
- "The developer replaced every raw colour and size in playground/hello/index.html with tokens. Nothing has been re-checked yet." → a reviewer should check again
- "Visual check passed at 390, 768 and 1440, and the css-reviewer has no comments left on playground/hello/index.html." → should be `done`

**My results:** Qwen 3.8 as the judge got 9 of 10 test decisions right, in about 4 seconds each. CLM-8B, a small router model, was much faster (0.08 s) but got only 3 of 10 (**failed attempt**).

## 6. Bonus: Pi instead of OpenCode

[Pi](https://pi.dev) is a leaner agent. Same model, same 5-step task as in Ep 2:

```bash
pi -p --model ollama/qwen3.8-128k "Do these 5 steps in order. 1) Read design/brief.md and find the accent colour hex. 2) Use a figcraft tool to get the name of the open FigCraft document. 3) Use the chrome tools to open file://$PWD/playground/test/shapes.html and find the word written on the page. 4) Write playground/report.txt with three lines: accent=<hex>, document=<name>, word=<word>. 5) Reply DONE followed by the three values."
```

**My results:** Pi took 53 seconds and OpenCode about 1:20, and both were correct. Pi needs extensions for plan mode and for sub-agents with their own models, so the series uses OpenCode.

## Next

[Ep 4: the agents build the frontend](../ep04-frontend-1)
