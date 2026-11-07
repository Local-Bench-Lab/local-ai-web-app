# Ep 3: A team of 12 local AI agents

Video: https://youtu.be/L1yxuCVJEho

Copy `AGENTS.md` and the `.opencode/` folder into your app folder.

- `.opencode/agent/`: the 12 agents, one file each (model, tools, and the job in plain words): planner, developer, design reader, visual checker, React reviewer, CSS reviewer, accessibility/performance auditor, test engineer, API designer, schema reviewer, security reviewer, contract checker.
- `AGENTS.md`: the project rule book every agent reads.
- `.opencode/skills/`: skills from [agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani (MIT, licence included).
- `decision-gate/judge-prompt.md`: the prompt the Qwen judge gets to pick the next agent.
