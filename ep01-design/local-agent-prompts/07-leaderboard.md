Task 7 of 11 for "Bench Board": the Leaderboard page, its ranked state and the details card. Use list_layers to get component ids (Nav, Logo, Button, Card, Race). Pages go in a row at y 1900; each desktop page is a frame 1440×1024 with fill bg, vertical auto layout, clip on. Put a Nav instance (sizingH fill) at the top of each page and pick its variant with instance.setProperties {Page: ...}.

1. "Leaderboard" at x 3280 (Nav Page=Leaderboard): a vertical frame "header" (padding 64 80 32 80, gap 16, no fill) with text "Leaderboard" (H1), text "Generation speed on the GB10, 4-bit models, Ollama, 16 Oct 2026." (Body, muted) and a horizontal frame "tabs" (gap 8) with two pills (padding 8 16, radius 99): "Speed (tok/s)" (fill accent, text bg) and "Vision" (fill surface, text muted). Then a vertical frame "board" (padding 16 80 0 80, gap 24, no fill) holding a Race instance with State=Start and a text "Tap a model for details" (Small, muted).
2. "Leaderboard – ranked": duplicate Leaderboard to x 3280, y 3044, rename it, and set its Race instance to State=Ranked.
3. "LFM details" at x 3280, y 4188: a frame 440 wide, vertical auto layout, padding 28, gap 12, radius 16, fill surface, 1 px stroke line, height hugs, with texts "LFM2.5 24B-A2B" (H2), "121.2 tok/s · 11/12 · 16.5 GB" (Body bold, accent) and "Fastest of five. Missed one maths question." (Body, muted).

## Checks
- exists: Leaderboard, Leaderboard – ranked, LFM details
- in Leaderboard: header, tabs, board
- in Leaderboard – ranked: header, board
