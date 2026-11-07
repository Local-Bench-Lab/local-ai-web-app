/**
 * Shared Bench Board API contract.
 *
 * This single file is the one source of truth for the JSON that flows between
 * the Fastify server and the React frontend. Both import the same names, so a
 * type can never drift between a client and its server:
 *
 *   server  →  import { LeaderboardSchema, type Leaderboard } from '../contract/api'
 *   frontend → import { LeaderboardSchema, type Leaderboard } from '../../contract/api'
 *
 * The TypeBox *schemas* (e.g. `LeaderboardSchema`) power runtime validation in
 * Fastify, while the *static types* (e.g. `type Leaderboard`) are used in
 * components and fetch helpers.
 *
 * The shape covers exactly what the three pages consume — see contract/README.md
 * for the route list.
 */

// NOTE: the shared directory sits next to `server/`, but TypeBox is only
// installed under `server/node_modules`. A symlink at
// `node_modules/@sinclair/typebox` → `server/node_modules/@sinclair/typebox`
// lets Node resolve the bare import from here (and the frontend will too),
// so both sides use the *same* package the server runs against.
import { Type, type Static } from '@sinclair/typebox'

// ---------------------------------------------------------------------------
// Route paths and HTTP methods
// ---------------------------------------------------------------------------
//
// Keeping the paths as one-time `as const` values (rather than string literals
// sprinkled through handlers) means a single typo breaks both sides at once.

export const Routes = {
  latest: '/api/latest',
  leaderboard: '/api/leaderboard',
  testRequests: '/api/test-requests',
} as const

export type RoutePath = (typeof Routes)[keyof typeof Routes]

export const Methods = {
  get: 'GET',
  post: 'POST',
} as const

export type HttpMethod = (typeof Methods)[keyof typeof Methods]

// ---------------------------------------------------------------------------
// Common shapes
// ---------------------------------------------------------------------------

/**
 * Canonical error body, always a JSON object.
 * `code` is a stable machine-identifiable string (e.g. `validation_failed`,
 * `not_found`, `internal`) so the client can branch on it without parsing
 * English messages. `message` is safe to show to end users.
 * `fields` maps a request field name to the first error message for it —
 * the "Request a test" form uses this to mark Name / Email inline.
 */
export const ApiErrorSchema = Type.Object(
  {
    code: Type.String({ description: 'Stable machine code, e.g. validation_failed' }),
    message: Type.String({ description: 'Human-readable message, safe to show' }),
    fields: Type.Optional(
      Type.Record(Type.String(), Type.String(), {
        description: 'Per-field error messages (only set for field-level problems)',
      }),
    ),
  },
  { description: 'Standard error response body for this API' },
)
export type ApiError = Static<typeof ApiErrorSchema>

// ---------------------------------------------------------------------------
// Model colour tokens
// ---------------------------------------------------------------------------
//
// The design brief pins five model colours (design/brief.md "Colours"). Rather
// than free-form hex values, the API exposes a token name that the frontend
// maps to a CSS custom property (`--color-model-*`). This keeps the contract
// stable when the design tokens change.

/** Token names for the model colour slots (see `src/styles/tokens.css`). */
export const ModelColorSchema = Type.Union([
  Type.Literal('lfm'),
  Type.Literal('gptoss'),
  Type.Literal('nemotron'),
  Type.Literal('gemma'),
  Type.Literal('qwen'),
], { description: 'Colour token name for a leaderboard model (mapped to a CSS custom property)', })
export type ModelColor = Static<typeof ModelColorSchema>

// ---------------------------------------------------------------------------
// GET /api/latest  — Home "Latest tests" strip
// ---------------------------------------------------------------------------

/**
 * One "Latest test" card on the Home page: a model chip, a title, a big result
 * value ("121 tok/s" or "10/10"), an optional score badge ("11/12" or "Qwen 3.8"),
 * a human-readable date, and the chip colour token.
 */
export const LatestTestSchema = Type.Object(
  {
    id: Type.String({ description: 'Stable id for this card, used as a React key' }),
    chip: Type.String({ description: 'Model pill label, e.g. "LFM2.5"' }),
    title: Type.String({ description: 'Card title, e.g. "LFM2.5 24B vs four reference models"' }),
    value: Type.String({ description: 'Primary result, shown in the number style, e.g. "121 tok/s" or "10/10"' }),
    score: Type.Optional(Type.String({ description: 'Result badge, e.g. "11/12" or "Qwen 3.8" (may be omitted)' })),
    date: Type.String({ description: 'Human-readable date, e.g. "16 Oct 2026"' }),
    color: Type.Optional(ModelColorSchema, true),
  },
  { description: 'A single "Latest tests" card' },
)
export type LatestTest = Static<typeof LatestTestSchema>

/** The "Latest tests" strip. Ordered newest-first; expect three cards. */
export const LatestTestsSchema = Type.Array(LatestTestSchema, {
  description: 'The Latest tests strip, ordered newest first',
})
export type LatestTests = Static<typeof LatestTestsSchema>

// ---------------------------------------------------------------------------
// GET /api/leaderboard?metric=speed|vision
// ---------------------------------------------------------------------------

/** Metric tabs, in display order. */
export const LeaderboardMetricSchema = Type.Union([
  Type.Literal('speed'),
  Type.Literal('vision'),
], { description: 'Leaderboard metric to fetch: `speed` (tok/s) or `vision` (coming soon)' })
export type LeaderboardMetric = Static<typeof LeaderboardMetricSchema>

/**
 * One benchmark task for a model (e.g. a math question, a code prompt).
 * `category` is the stable slug ("math", "logic", "code", …); `ok` is the
 * pass/fail result; `answer` is the model's raw answer text (may be empty).
 */
export const TaskResultSchema = Type.Object(
  {
    category: Type.String({ description: 'Task category slug, e.g. "math" or "code"' }),
    ok: Type.Boolean({ description: 'Whether the model answered correctly' }),
    answer: Type.String({ description: 'The model\'s raw answer (may be empty when it failed)' }),
  },
  { description: 'A single benchmark task result for a model' },
)
export type TaskResult = Static<typeof TaskResultSchema>

/**
 * One row in the leaderboard Speed tab, ranked fastest first. The numeric
 * fields mirror the real rows in `data/results.json`; the strings and colour
 * token exist for the UI.
 */
export const LeaderboardRowSchema = Type.Object(
  {
    rank: Type.Integer({ minimum: 1, description: 'Position after sorting fastest first (1 = fastest)' }),
    model: Type.String({ description: 'Model name, e.g. "LFM2.5 24B"' }),
    load_s: Type.Number({ description: 'Time to load the model, in seconds' }),
    mem_gb: Type.Number({ description: 'Memory used at runtime, in GB' }),
    gen_tps: Type.Number({ description: 'Generation speed, tokens per second (the raced value)' }),
    prompt_tps: Type.Number({ description: 'Prompt (prompt-processing) speed, tokens per second' }),
    score: Type.Integer({ description: 'Count of benchmark tasks the model passed' }),
    of: Type.Integer({ description: 'Total number of benchmark tasks in the suite' }),
    /** The bar width as a percentage of the fastest model (0–100). */
    width: Type.Number({ minimum: 0, maximum: 100, description: 'Bar width as a % of the fastest model' }),
    color: ModelColorSchema,
    tasks: Type.Array(TaskResultSchema, { description: 'Per-task results (for the click-a-bar detail card)' }),
  },
  { description: 'One leaderboard Speed row, fastest first' },
)
export type LeaderboardRow = Static<typeof LeaderboardRowSchema>

/**
 * Full leaderboard response. The `available` flag tells the UI when a metric
 * has no data yet (the Vision tab is `available: false` today — `rows` and
 * `unit` are absent in that case, `message` explains why).
 */
export const LeaderboardSchema = Type.Object(
  {
    metric: Type.String({ description: 'Echo of the requested metric: "speed" or "vision"' }),
    date: Type.Optional(
      Type.String({
        description: 'ISO date (YYYY-MM-DD) of the run, e.g. "2026-10-16" (only when the metric is available)',
      }),
    ),
    /** When the requested metric was not yet benchmarked. */
    available: Type.Boolean({ description: 'True when this metric has real data to show' }),
    /** Friendly explanation shown when `available` is false. */
    message: Type.Optional(
      Type.String({ description: 'User-facing message when the metric is not yet available' }),
    ),
    /** Unit of the measured value (e.g. "tok/s"); only present when available. */
    unit: Type.Optional(Type.String({ description: 'Display unit for `value` (e.g. "tok/s")' })),
    /** Ranked rows — present only when `available` is true. */
    rows: Type.Optional(
      Type.Array(LeaderboardRowSchema, { description: 'Ranked rows, fastest first' }),
    ),
  },
  { description: 'Leaderboard response' },
)
export type Leaderboard = Static<typeof LeaderboardSchema>

// ---------------------------------------------------------------------------
// POST /api/test-requests  — Request a test
// ---------------------------------------------------------------------------
//
// The form is submitted as `multipart/form-data` (see @fastify/multipart) so
// the screenshot can be attached. Text-part field names match `RequestForm`:
// the client builds an object with these keys, and the server reads them from
// the multipart request. A JSON-only payload would work too, but multipart keeps
// the file upload on the wire format the browser already knows.

/** Text values the form sends. `name` and `email` are required. */
export const RequestFormSchema = Type.Object(
  {
    name: Type.String({
      minLength: 1,
      description: 'Your name',
    }),
    /**
     * A valid email address (RFC-5322 / simple "local@domain.tld" shape).
     * The frontend does its own lightweight regex check; the Fastify server
     * can register a stricter TypeBox format if it wants.
     */
    email: Type.String({ minLength: 1, description: 'Email address to send updates/results' }),
    model: Type.Optional(
      Type.String({ description: 'Which model to test (e.g. "llama5-8b", "lfm2.5")' }),
    ),
    hardware: Type.Optional(
      Type.Union(
        [Type.Literal('gb10'), Type.Literal('ps5')],
        { description: 'Hardware to test on: GB10 (default) or PS5' },
      ),
    ),
    what: Type.Optional(
      Type.String({ description: 'Free-text description of what should be tested' }),
    ),
  },
  { description: 'Fields for the "Request a test" form (multipart form-parts)' },
)
export type RequestForm = Static<typeof RequestFormSchema>

/**
 * Confirmation returned on a successful accept. `requestId` is a server-issued
 * identifier the client can quote in follow-ups; `status` is stable so the
 * UI can branch on the lifecycle without reading English copy.
 */
export const RequestConfirmationSchema = Type.Object(
  {
    requestId: Type.String({ description: 'Server-issued id for this request' }),
    status: Type.Literal('queued', { description: 'Initial lifecycle state for a newly accepted request' }),
    message: Type.String({ description: 'User-facing confirmation, safe to show' }),
  },
  { description: 'Success response for POST /api/test-requests' },
)
export type RequestConfirmation = Static<typeof RequestConfirmationSchema>

// ---------------------------------------------------------------------------
// Convenience map: route → schemas (handy for the server to register)
// ---------------------------------------------------------------------------

/**
 * Maps each route to its method and the TypeBox schema it should validate
 * against. The server is free to ignore the schemas and use fastify's own
 * validation, but having them in one place keeps the contract discoverable.
 */
export const EndpointSchemas = {
  [Routes.latest]: { method: Methods.get, response: LatestTestsSchema },
  [Routes.leaderboard]: { method: Methods.get, response: LeaderboardSchema, param: LeaderboardMetricSchema },
  [Routes.testRequests]: { method: Methods.post, body: RequestFormSchema, response: RequestConfirmationSchema },
} as const

export type EndpointSpec = typeof EndpointSchemas
export type Endpoint = (typeof EndpointSchemas)[keyof typeof EndpointSchemas]
