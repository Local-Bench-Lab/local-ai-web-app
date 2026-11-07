# Ep 2: OpenCode + Ollama agents

Video: https://youtu.be/7I02-5ohqOo

1. Pull the models and make 128k-context copies (the default context is too small for agents):

```bash
ollama pull qwen3.8:27b && ollama pull gpt-oss:120b && ollama pull gemma4
ollama create qwen3.8-128k -f modelfiles/qwen3.8-128k.Modelfile
ollama create gpt-oss-128k -f modelfiles/gpt-oss-128k.Modelfile
ollama create gemma4-128k -f modelfiles/gemma4-128k.Modelfile
```

2. Copy `opencode.json` into your app folder. The `modalities` lines matter: without `"input": ["text", "image"]` OpenCode won't send screenshots to the model. It adds two MCP servers: FigCraft (reads the design) and Chrome DevTools (opens and checks the page).

I run OpenCode inside a Docker container so model-written code can't touch my home folder. Do the same if you can.
