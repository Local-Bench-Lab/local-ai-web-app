Task 3 of 11 for "Bench Board". Use list_layers to find existing components (Logo, Button, Card). Build in the area x 0–2000, y 800–1300, nothing overlapping.

1. Nav: component "Page=Home", 1440×72, horizontal auto layout, padding 0 80, gap 12, centred vertically, fill bg, with only a bottom border (stroke style line, then set strokeTopWeight 0, strokeRightWeight 0, strokeLeftWeight 0, strokeBottomWeight 1). Children in order: an instance of Logo; text "brand" = "Bench Board" (Body bold, size 20, colour text); a frame "spacer" with sizingH fill, height 1, no fill; a horizontal frame "links" (gap 32, hug, no fill) holding three vertical frames named "link/Home", "link/Leaderboard", "link/Request a test" (gap 6, hug, centred, no fill), each with a text "label" (Body, colour muted) and a rectangle "underline" 24×2 radius 1 fill accent, hidden (visible false); and a vertical frame "hamburger" (22×16, gap 5, no fill, hidden) with three 22×2 rectangles fill text.
2. Combine as variants, name the set "Nav", and add variants Page=Leaderboard, Page=Request, Page=Mobile. In Page=Home / Leaderboard / Request, make that page's link label colour text and its underline visible. In Page=Mobile: width 390, padding 0 16, hide "links", show "hamburger". Keep the variants stacked vertically 24 px apart.
3. Drawer: component "Drawer" 300×844, vertical auto layout, padding 24, gap 28, fill surface. A horizontal row "top" (fills the width) with text "Menu" (Small, muted), a fill-width spacer, and text "close" = "×" (H2, colour text). Then three texts named "drawer/Home", "drawer/Leaderboard", "drawer/Request a test" with those words (H2 at size 24, colour text). Place it at x 1600, y 800.

## Checks
- exists: Nav, Drawer
- in Nav: Page=Home, Page=Leaderboard, Page=Request, Page=Mobile, links, link/Home, link/Leaderboard, link/Request a test, underline, hamburger
- in Drawer: top, close, drawer/Home, drawer/Leaderboard, drawer/Request a test
- set Nav: Page=Home, Page=Leaderboard, Page=Request, Page=Mobile
