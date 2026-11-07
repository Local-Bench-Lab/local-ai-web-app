# Building a Web App with Local AI Models & Apps

The prompts, agents and scripts from my YouTube series, where local AI models build a full web app (Bench Board) on an NVIDIA DGX Spark GB10. Everything runs on the machine: Ollama, OpenCode, Pi, FigCraft, Postgres, and Floci for the cloud episodes. No cloud AI.

Channel: https://www.youtube.com/channel/UCR1YydvrN6VTtWUGHH2mTSg (playlist "Building a Web App with Local AI Models & Apps")

| Folder | Episode | What's inside |
|---|---|---|
| [ep01-design](ep01-design) | [Ep 1: Design](https://youtu.be/xFcJaLkPAKo) | The design brief, and a small local agent that drives FigCraft over MCP, with its task prompts |
| [ep02-agent-setup](ep02-agent-setup) | [Ep 2: OpenCode + Ollama agents](https://youtu.be/7I02-5ohqOo) | Ollama Modelfiles (128k context), the OpenCode config (models, image input, MCP servers) |
| [ep03-agent-team](ep03-agent-team) | [Ep 3: A team of 12 local AI agents](https://youtu.be/L1yxuCVJEho) | The 12 agent files, AGENTS.md, the skills, and the decision gate (Qwen judge vs CLM-8B) |
| [ep04-frontend-1](ep04-frontend-1) | [Ep 4: Local AI builds the frontend](https://youtu.be/ygrqkF7pN4g) | Every prompt as a run script, the app design brief, the design-token checker |
| [ep05-frontend-2](ep05-frontend-2) | Ep 5: Animations, tests, accessibility, speed | Run scripts for the race animation, form states, tests, accessibility and performance |
| [ep06-backend-1](ep06-backend-1) | Ep 6: Backend part 1, Postgres + a database | Postgres and npm installs, the API design and contract prompts, the contract the model wrote |

More folders are added as the episodes come out.

## How the run scripts work

Each `runs/*.sh` file is one recorded session: a list of `opencode run --agent <name> "<prompt>"` steps, with `time` in front so you see how long each model took. The prompts in these files are exactly what the models got on camera.

My setup, if you want to follow along:
- Ollama with 128k-context copies of `qwen3.8:27b`, `gpt-oss:120b` and `gemma4` (see `ep02-agent-setup/modelfiles`).
- OpenCode runs inside a Docker container with no access to my home files. The `opencode-wrapper.sh` files show how: they call `docker exec` into that container. Without Docker, put `opencode` on your PATH and run the scripts from the app folder.
- Secrets (the database password) live in an env file that is never committed or printed.

Results are real and include the failures. The numbers in each episode's description come from these runs.
