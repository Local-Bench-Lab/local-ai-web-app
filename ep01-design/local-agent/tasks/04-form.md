Task 4 of 11 for "Bench Board". Use list_layers to see what exists. Build in the area x 2200–3600, y 0–1100, nothing overlapping.

1. Field: component "State=Default", 560 wide, vertical auto layout, gap 8, no fill, height hugs. Children: text "label" = "Email" (Small, muted); a horizontal frame "input" (height 48, padding 0 16, centred vertically, radius 10, fills the width, fill surface, 1 px stroke line) holding text "value" = "you@example.com" (Body, muted); text "help" = "Enter a valid email" (Small, colour bad), hidden. Combine as variants, name the set "Field", add State=Focus (input stroke accent), State=Error (input stroke bad, help visible), State=Filled (value colour text). Stack the variants vertically 24 px apart.
2. Select: component "Select" like the field (label "Hardware", input with text "value" = "Choose…" filling the width and a text "caret" = "▾", both muted). No variants.
3. TextArea: component "TextArea": label "What should I test?", input frame vertical, height 120, padding 14 16, with value "e.g. Does Llama 5 8B beat Gemma 4 at coding?" (Body, muted).
4. DropZone: component "DropZone" 560×120, vertical auto layout centred both ways, gap 6, radius 10, fill bg, 1.5 px stroke line dashed [6, 4], with text "label" = "Drop a screenshot or click to choose" (Body, muted) and "hint" = "PNG or JPG, up to 5 MB" (Small, muted).

## Checks
- exists: Field, Select, TextArea, DropZone
- in Field: State=Default, State=Focus, State=Error, State=Filled, label, input, value, help
- in Select: label, input, value, caret
- in DropZone: label, hint
- set Field: State=Default, State=Focus, State=Error, State=Filled
