# Ep 1: Design

Video: https://youtu.be/xFcJaLkPAKo

- `design-brief.md`: the brief for Bench Board (colours, type, grid, components, the three pages). I designed it by hand in FigCraft from this.
- `local-agent/`: a small agent where a local model (Ollama) drives FigCraft through its MCP server. `tasks/` holds one prompt per design step; `run_all.sh` runs them in order:

```
sh run_all.sh gpt-oss:120b /config/designs/bench-board-local.figcraft
```

  Honest result: local models could do simple steps, but not the full design. That's why the episode's design was made by hand.
- `opencode.json`: the first OpenCode config pointing at Ollama.
