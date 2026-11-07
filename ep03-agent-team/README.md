# Ep 3: A team of 12 local AI agents

Video: https://youtu.be/L1yxuCVJEho

- `.opencode/agent/`: the 12 agents, one file each (model, tools, and the job in plain words): planner, developer, design reader, visual checker, React reviewer, CSS reviewer, accessibility/performance auditor, test engineer, API designer, schema reviewer, security reviewer, contract checker. Copy the folder into your project's `.opencode/`.
- `AGENTS.md`: the project rule book every agent reads.
- `.opencode/skills/`: skills from [agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani (MIT, licence included).
- `decision-gate/`: who decides which agent runs next. `judge-prompt.md` is the prompt the Qwen judge gets (9 of 10 right in the test; CLM-8B got 3 of 10), and `routing_cases.json` the agent menu and test states.
