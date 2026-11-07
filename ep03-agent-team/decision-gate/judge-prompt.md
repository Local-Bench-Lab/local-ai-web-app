# The judge prompt (Qwen 3.8 picks which agent runs next)

Sent to the local model through Ollama with temperature 0 and structured output (`choice` must be one of the agent names, plus a short `reason`):

```
Which agent should run next?

State: <what just happened, e.g. "The CSS reviewer found 6 problems: raw colours and hard-coded spacing.">

Agents:
- <agent name>: <what it does>
- ...

Answer with the single best agent.
```

`routing_cases.json` has the agent menu and the 10 test states I used (written before any model ran). Qwen 3.8 picked right 9 of 10 times, in about 4 seconds each.
