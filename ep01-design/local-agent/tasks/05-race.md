Task 5 of 11 for "Bench Board": the leaderboard race, the app's main animation. Build it at x 2200, y 1300 (nothing else is there).

Real results from 16 Oct 2026 (generation speed, tok/s): Gemma 4 63.6 (colour style m/gemma), gpt-oss 20B 61.9 (m/gptoss), LFM2.5 24B 121.2 (m/lfm), Nemotron 3 Nano 30B 79.0 (m/nemotron), Qwen 3.8 27B 23.6 (m/qwen).

1. Component "State=Start", 1100 × 304, no fill, NO auto layout. Five rows in this alphabetical order, frames named exactly "row/Gemma 4", "row/gpt-oss 20B", "row/LFM2.5 24B", "row/Nemotron 3 Nano 30B", "row/Qwen 3.8 27B", 1100×48, no fill, at x 0, y = row index × 64. In each row: text "name" (the model name, Body bold, colour text) at x 0, y 12; rectangle "track" at x 240, y 10, 720×28, radius 6, fill surface; rectangle "bar" at x 240, y 10, width 4, height 28, radius 6, fill the model's colour; text "value" = "0" (Number, colour text) at x 984, y 8.
2. Combine as variants and name the set "Race". Add variant State=Grown: every bar's width = round(tok/s ÷ 121.2 × 720) and every value text = the tok/s with one decimal (e.g. "63.6"). Rows stay in the same order.
3. Add variant State=Ranked: same as Grown, but move the rows (change only their y) so they are ordered fastest first: LFM2.5 y 0, Nemotron y 64, Gemma 4 y 128, gpt-oss y 192, Qwen 3.8 y 256.
Keep the three variants stacked vertically, 40 px apart. Check each variant's bars and values with get_node.

## Checks
- exists: Race
- in Race: State=Start, State=Grown, State=Ranked, row/Gemma 4, row/gpt-oss 20B, row/LFM2.5 24B, row/Nemotron 3 Nano 30B, row/Qwen 3.8 27B, track, bar, value
- set Race: State=Start, State=Grown, State=Ranked
