# Design brief: Bench Board

## Look
- **Mood:** a lab bench at night. Dark UI, one bright accent, numbers front and centre. It matches the channel's video style, so viewers recognise it.
- **Colours** (FigCraft colour styles):
  - `bg` #0f1115
  - `surface` #181b22
  - `line` #2a2f3a
  - `text` #e8eaf0
  - `muted` #8a93a6
  - `accent` #f5b942 (amber)
  - `good` #4ade80
  - Model colours for the leaderboard (real 16 Oct speed run): LFM2.5 = accent, gpt-oss #67c6e3, Nemotron #4ade80, Gemma 4 #f472b6, Qwen 3.8 #c084fc.
- **Type** (text styles), using fonts bundled in FigCraft:
  - Inter for UI: H1 56/64 bold, H2 32/40 semibold, body 16/24, small 13/18.
  - Liberation Mono for numbers (tok/s, scores).
- **Grid:** desktop 1440 wide, 12 columns, 80 margin, 24 gutter. Mobile 390 wide, 4 columns, 16 margin.
- **Radius** 12. **Spacing** on a 4/8 scale. Everything uses auto layout, so the code export stays clean.

## Components (built first, reused on every page)
- **Nav bar:** logo slot, links (Home, Leaderboard, Request a test), active-link underline. Variants: desktop / mobile (hamburger).
- **Mobile drawer:** slides in from the right, with links and a close button.
- **Button:** primary / secondary, with states default / hover / pressed / disabled.
- **Test card:** model chip, title, tok/s, score, date.
- **Race bar:** model name, coloured bar, value. Variants: start (width 0) / end (full width).
- **Input field:** label, input, help/error text. States: default / focus / error / filled.
- **Select field, text area, file drop zone.**

## Pages
1. **Home (desktop + mobile)**
   - Hero: logo, H1 "Every local AI model, tested on one desk.", subline about the GB10, "See the leaderboard" button.
   - Strip of 3 test cards ("Latest tests"), drawn from the channel's real runs: LFM2.5, the vision test, PS5 vs GB10.
   - Footer.
   - **Basic animation:** the hero text and cards fade and slide up on load, staggered.
2. **Leaderboard**
   - Tabs: Speed (tok/s) / Vision score.
   - **Complex animation, the race:** bars start at 0, grow to their values, then reorder by rank. Numbers count up in the real site; in the prototype they switch from 0 to the value. Clicking a bar expands a details card with Smart-Animate.
   - Data comes from the real `runs/2026-10-16/results.json` speeds (LFM2.5 121.2, Nemotron 79.0, Gemma 4 63.6, gpt-oss 61.9, Qwen 3.8 23.6 tok/s), so it's honest.
3. **Request a test**
   - Form: name, email, model to test, hardware (select), what to test (text area), screenshot (drop zone), submit.
   - States to prototype: empty, error (bad email), filled, submitting, success ("Thanks, it's on the list").

## Prototype flows
- Nav links between all three pages, with a dissolve.
- Mobile: hamburger, then the drawer slides in, then a link, then navigate.
- Home on load: the after-delay staggered reveal.
- Leaderboard: after delay, start variant to end variant (bars grow), then a reorder frame; click a bar to expand its card.
- Form: submit while empty, then the error state; fix it, then submitting, then success.

## Logo (PhotoCraft)
- A simple mark: a bench/bar-chart glyph (three rising bars on a desk line) in amber on dark, plus the "Bench Board" wordmark.
- Exports: 512 px PNG with transparency, a 32 px favicon, and a light-background version.
