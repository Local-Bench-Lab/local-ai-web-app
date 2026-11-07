# Ep 1: Design

📺 Video: https://youtu.be/xFcJaLkPAKo

Before any code, we design **Bench Board**: a three page web app that shows real benchmark results.
- **Home** with an entrance animation.
- **Leaderboard** where the models race, using real speed numbers.
- **Request a test** form with error, sending and done states.
- A mobile menu.

## What you need

- **FigCraft** (design, like Figma) and **PhotoCraft** (image editor, like Photoshop). Both are free and run locally: https://getartcraft.com/apps. On a Mac, Windows or a normal Linux PC, use the installer. On ARM Linux (like the GB10), I run them in the linuxserver `craft-apps` Docker container.
- For the local model test at the end: Ollama and OpenCode, set up as in [Ep 2](../ep02-agent-setup).

## Option A: use my design (fastest)

Open [`../app-starter/bench-board.figcraft`](../app-starter/bench-board.figcraft) in FigCraft. The page images the agents use later are in [`../app-starter/design`](../app-starter/design).

## Option B: design it yourself

Follow [`app-starter/design/brief.md`](../app-starter/design/brief.md). It has the colours, type, grid, every component and the three pages. In order:

1. **Styles:** the 7 colours plus 5 model colours, and the text styles (Inter for UI, Liberation Mono for numbers).
2. **Components**, built once and reused everywhere: Nav bar (desktop and mobile), mobile drawer, Button (primary and secondary, with hover, pressed and disabled states), test card, race bar, input field, select field, text area and file drop zone. Use auto layout, so the code export stays clean.
3. **Pages**, at desktop (1440) and mobile (390) width.
4. **Prototype:** link the frames (trigger, action, animation) and make the race with three RaceBar variants and smart animate.
5. **Logo** in PhotoCraft, placed once in the Logo component so it shows everywhere.

Save often. The design file is what the agents read in Ep 4.

## Try a local model on the design

FigCraft has an MCP server, so an agent can design with it. Start FigCraft with its control port on, add it to OpenCode (see [Ep 2](../ep02-agent-setup)), put [`brief.md`](../app-starter/design/brief.md) in the folder, then:

```bash
opencode -m ollama/qwen3.8-128k
```

and give it this prompt:

```
Read brief.md. Using the figcraft MCP, create the colour styles and text styles from the brief, then a Button component with primary and secondary variants that uses those styles. Lay it out neatly on the canvas.
```

**My results:**
- **Qwen 3.8 27B:** 14 min 20 s. It made all 12 colour styles, 6 text styles and a Button with both variants, plus a small demo board. Its heading came out black on a dark background.
- **gpt-oss 120B (failed attempt):** stopped after 2 min 20 s. It made 11 colour and 4 text styles, but its button used none of them and had no variants.

## Next

[Ep 2: set up the local agents](../ep02-agent-setup)
