Task 9 of 11 for "Bench Board": the mobile frames. Use list_layers for ids (Nav, Field, Select, TextArea, DropZone, Button, Logo, Card, Drawer, Home). Desktop pages are 1440×1024 frames, fill bg, vertical auto layout, clip on, with a Nav instance (sizingH fill) on top.

1. "Home – mobile" at x 1640, y 3324: frame 390×844 like the pages, Nav Page=Mobile; a vertical "hero" (padding 40 16 24 16, gap 16, centred, fills width) with a Logo 56×56, the headline (H1 at size 34, line height 40, centred, fills width), "Measured live on an NVIDIA DGX Spark GB10." (Body, muted, centred) and a Button; then a vertical "latest" (padding 8 16 24 16) with one Card instance filling the width.
2. "Menu open" at x 2150, y 3324: duplicate Home – mobile, rename, then add a black rectangle "dim" 390×844 at opacity 0.5 and a Drawer instance at x 90, y 0, both with absolute true (so auto layout ignores them).

## Checks
- exists: Home – mobile, Menu open
- in Home – mobile: hero, latest
- in Menu open: dim
