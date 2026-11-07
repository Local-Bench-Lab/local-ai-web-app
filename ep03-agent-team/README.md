# Ep 3: A team of 12 local AI agents

Video: https://youtu.be/L1yxuCVJEho

- `.opencode/agent/`: the 12 agents, one file each (model, tools, and the job in plain words): planner, developer, design reader, visual checker, React reviewer, CSS reviewer, accessibility/performance auditor, test engineer, API designer, schema reviewer, security reviewer, contract checker. Copy the folder into your project's `.opencode/`.
- `AGENTS.md`: the project rule book every agent reads.
- `.opencode/skills/`: skills from [agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani (MIT, licence included).
- `decision-gate/`: who decides which agent runs next. `next-agent "<what just happened>"` asks a Qwen judge (9 of 10 right in the test); `clm_gate.py` also tries CLM-8B (3 of 10). The test cases and results are in `routing_cases.json` and `results.json`.
