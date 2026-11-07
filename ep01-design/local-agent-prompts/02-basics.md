Task 2 of 11 for "Bench Board". Styles exist already (list_layers shows what is on the canvas). Build these components in the area x 0–1400, y 0–700. Leave at least 60 px between components so nothing overlaps. Apply the paint and text styles by name with style.apply.

1. Logo: a component named "Logo", 40×40, corner radius 10, fill style surface, 1.5 px stroke style line, dashed (dashes [4, 3]). It is a placeholder; the real logo comes later.
2. Button: component "Type=Primary": horizontal auto layout, padding 14 24, radius 12, hug both ways, centred, fill accent, holding a text layer named "label" = "See the leaderboard" (Body bold, colour bg). Combine as variants, name the set "Button", then add variants Type=Secondary (fill surface, 1 px stroke line, label colour text), Type=Hover (fill #f8ca6a), Type=Disabled (opacity 0.4). Place the variants side by side, 24 px apart, not on top of each other.
3. Card: component "Card", 410 wide, vertical auto layout, padding 20, gap 12, radius 12, fill surface, 1 px stroke line, height hugs. Inside: a pill "chip" (horizontal, padding 4 10, radius 99, hug, fill m/lfm) holding text "chip label" = "LFM2.5" (Small, colour bg); text "title" = "LFM2.5 24B vs four reference models" (Body bold, colour text, fills the width); a horizontal row "stats" (gap 16) with text "speed" = "121 tok/s" (Number, colour text) and text "score" = "11/12" (Body bold, colour good); text "date" = "16 Oct 2026" (Small, colour muted).

## Checks
- exists: Logo, Button, Card
- in Button: Type=Primary, Type=Secondary, Type=Hover, Type=Disabled, label
- in Card: chip, chip label, title, stats, speed, score, date
- set Button: Type=Primary, Type=Secondary, Type=Hover, Type=Disabled
