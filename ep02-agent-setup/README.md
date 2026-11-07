# Ep 2: OpenCode + Ollama agents

📺 Video: https://youtu.be/7I02-5ohqOo

We set up a free, local coding agent: **OpenCode** (the harness) talking to models in **Ollama**. It gets two sets of tools: **FigCraft** (reads the design) and **Chrome DevTools** (opens the page, takes screenshots). Then we test whether each model is really agent-ready.

## What you need

- **Ollama:** https://ollama.com
- **OpenCode:** https://opencode.ai
- **Node 22** (for the Chrome DevTools MCP server) and **Google Chrome**.
- **Enough memory for the models.** On the GB10 I use Qwen 3.8 27B, gpt-oss 120B and Gemma 4 8B. On a smaller machine, pick models that fit; my llmfit video shows how: https://youtube.com/shorts/aOTe8goXE1c

I run OpenCode inside a Docker container, so code written by a model can't touch my home folder. I recommend you do the same.

## 1. Ollama: install, pull, list

```bash
ollama --version
ollama pull qwen3.8:27b
ollama pull gpt-oss:120b
ollama pull gemma4
ollama list
curl -s localhost:11434/v1/models     # the OpenAI-compatible address OpenCode uses
```

## 2. Give the models a big enough context window

Ollama's default context is too small for an agent. With 8k, after three screenshots my agent forgot it even had a Chrome tool. Each Modelfile here is two lines: the model, then `num_ctx 131072`.

```bash
ollama create qwen3.8-128k -f modelfiles/qwen3.8-128k.Modelfile
ollama create gpt-oss-128k -f modelfiles/gpt-oss-128k.Modelfile
ollama create gemma4-128k -f modelfiles/gemma4-128k.Modelfile
```

(Or set `OLLAMA_CONTEXT_LENGTH` for the whole machine.)

## 3. The OpenCode config

Copy [`opencode.json`](opencode.json) into your project folder. It has:
- **provider:** Ollama at `http://localhost:11434/v1`, with the three 128k models.
- **modalities:** `"input": ["text", "image"]` on the vision models. ⚠️ Without this, OpenCode never sends images: Qwen answered "NO IMAGE" to an attached picture.
- **mcp:** FigCraft (`figcraft-cli mcp --attach 47801`, with FigCraft started with its control port) and Chrome DevTools (`npx chrome-devtools-mcp`).

Check it:

```bash
opencode models ollama
opencode mcp list
```

## 4. Is the model agent-ready? Three checks

**Check 1: capability flags.** Look for `tools` (and `vision` for screenshot work):

```bash
ollama show qwen3.8-128k
```

**Check 2: the image setting.** Use any image from [`../app-starter/design`](../app-starter/design):

```bash
opencode run -m ollama/qwen3.8-128k "Describe this image in one sentence. If you cannot see an image, say NO IMAGE." -f design/home.png
```

**Check 3: a real 5-step task.** Put [`test/shapes.html`](test/shapes.html) in your project's `playground/test/`, and the design brief at `design/brief.md`:

```bash
opencode run -m ollama/qwen3.8-128k "Do these 5 steps in order. 1) Read design/brief.md and find the accent colour hex. 2) Use a figcraft tool to get the name of the open FigCraft document. 3) Use the chrome tools to open file://$PWD/playground/test/shapes.html and find the word written on the page. 4) Write playground/report.txt with three lines: accent=<hex>, document=<name>, word=<word>. 5) Reply DONE followed by the three values."
cat playground/report.txt
```

**Browser vision.** Run this for each vision model:

```bash
opencode run -m ollama/gemma4-128k "Use the chrome tools: open file://$PWD/playground/test/shapes.html, take one screenshot, then tell me in two sentences which shapes you see (with colours, left to right) and what word is written on the page."
```

**My results:** all four models finished the 5-step task with 0 bad tool calls. gpt-oss 120B took 1:15, Qwen 3.8 1:21, Gemma 4 8B 1:41 and Gemma 4 31B 2:25. In the vision test, all three were correct.

## Next

[Ep 3: a team of 12 agents](../ep03-agent-team)
