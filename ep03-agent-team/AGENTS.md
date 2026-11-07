# Bench Board

A three-page responsive web app that shows Local Bench Lab's real benchmark results: Home, Leaderboard (with a race
animation), and a "Request a test" form, plus a mobile menu.

## Source of truth for the design
- The FigCraft file `bench-board.figcraft` (read it with the `figcraft` tools; never change it).
- `design/brief.md` for colours, type, spacing and components.
- `design/*.png` are the reference frames. Compare screenshots against them.

## Stack
- Frontend: React + Vite + TypeScript, CSS Modules, design tokens in `src/styles/tokens.css`.
- Backend: Fastify + TypeScript, Postgres (Drizzle). The shared API contract lives in `contract/`.
- Tests: Vitest + React Testing Library; Fastify `inject` for the API.

## Rules
- Mobile first. Check every page at 390, 768 and 1440 px wide with the `chrome` tools before calling it done.
- No raw colours or sizes in components; use the tokens.
- One component per folder: `Button/Button.tsx`, `Button.module.css`, `Button.test.tsx`.
- Small steps: plan first, then build one step, check it, then the next.
- Real data only: copy numbers from `data/results.json`, never invent them.

## Commands
- `npm run dev`: dev server on port 5173
- `npm run lint` · `npm run typecheck` · `npm test`

## Definition of done
Lint, typecheck and tests pass, and the screenshots at 3 widths match the design with no overlaps or cut-off text.

## Limits
- Work only inside this folder. No network installs without asking.
- Reviewers never edit code. The test-engineer edits only `*.test.*` files.
