# Building a Web App with Local AI Models & Apps

A follow-along course from my YouTube series. Local AI models build a full web app, **Bench Board**, from design to backend to cloud. Everything runs on one machine (my NVIDIA DGX Spark GB10): Ollama, OpenCode, FigCraft, Postgres, and Floci for the cloud episodes. No cloud AI and no API keys.

📺 Channel: https://www.youtube.com/channel/UCR1YydvrN6VTtWUGHH2mTSg (playlist "Building a Web App with Local AI Models & Apps")

## The course

Do the episodes in order. Each folder's README is a full guide: what you need, every command and prompt in order, and what happened in the video, failed attempts included.

| # | Episode | What you do |
|---|---|---|
| 1 | [Design](ep01-design) · [video](https://youtu.be/xFcJaLkPAKo) | Design the three pages in FigCraft (or use mine) |
| 2 | [Agent setup](ep02-agent-setup) · [video](https://youtu.be/7I02-5ohqOo) | Install Ollama and OpenCode, give the models eyes and enough memory |
| 3 | [Agent team](ep03-agent-team) · [video](https://youtu.be/L1yxuCVJEho) | Add 12 agents, the rule book and the skills; run one full loop |
| 4 | [Frontend, part 1](ep04-frontend-1) · [video](https://youtu.be/ygrqkF7pN4g) | The agents build the three pages |
| 5 | [Frontend, part 2](ep05-frontend-2) | Animations, tests, accessibility, speed |
| 6 | [Backend, part 1](ep06-backend-1) | Postgres, the API contract, the database |

More episodes are added as they come out.

## What you need overall

- A machine that can run local models. The GB10 runs Qwen 3.8 27B, gpt-oss 120B and Gemma 4 8B. On smaller hardware, pick models that fit and swap the names in the configs.
- Ollama, OpenCode, Node 22, Google Chrome, Docker, and FigCraft (free, from getartcraft.com/apps).
- Patience: local models are slower than the cloud, and some steps take an hour or more.

## Starter files

[`app-starter/`](app-starter) has everything the prompts refer to:
- `bench-board.figcraft`: the finished Ep 1 design.
- `design/`: the page images and `brief.md`.
- `data/results.json`: the real benchmark numbers the app shows.

Copy `design/` and `data/` into your app folder in Ep 4.

## Good to know

- The prompts are exactly what the models got on camera.
- Keep secrets (like the database password) in env files, never in a prompt or in git.
- I run OpenCode inside a Docker container, so code written by a model can't touch my home folder.
