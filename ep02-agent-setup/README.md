# Ep 2: OpenCode + Ollama agents

Video: https://youtu.be/7I02-5ohqOo

- `modelfiles/`: Ollama Modelfiles that make 128k-context copies of the models (the default context is too small for agents). Example:

```
ollama create qwen3.8-128k -f modelfiles/qwen3.8-128k.Modelfile
```

- `opencode.json`: the OpenCode config. Note the `modalities` lines: without `"input": ["text", "image"]` OpenCode won't send screenshots to the model. It also adds two MCP servers: FigCraft (reads the design) and Chrome DevTools (opens and checks the page).
- `opencode-wrapper.sh`: how I run OpenCode inside a Docker container, so model-written code never touches my home folder.
