# Ep 6: Backend part 1, step by step

Carries on from the Ep 5 app.

## 1. Postgres in Docker

Make a file `bench-db.env` (keep it out of git):

```
POSTGRES_USER=bench
POSTGRES_DB=benchboard
POSTGRES_PASSWORD=<a long random password>
```

```bash
docker pull postgres:18
docker run -d --name bench-db --env-file bench-db.env -p 127.0.0.1:5432:5432 postgres:18
until docker exec bench-db pg_isready -U bench -d benchboard; do sleep 1; done
```

The server reads `DATABASE_URL=postgres://bench:<password>@localhost:5432/benchboard` from its environment. Never paste it into a prompt.

## 2. The server packages (in `server/`)

```bash
mkdir server && cd server
npm init -y
npm pkg set type=module "scripts.dev=tsx watch src/index.ts" "scripts.start=tsx src/index.ts" "scripts.typecheck=tsc --noEmit" "scripts.test=vitest run --passWithNoTests" "scripts.db:generate=drizzle-kit generate" "scripts.db:migrate=drizzle-kit migrate"
npm install fastify @fastify/multipart @fastify/cors @sinclair/typebox drizzle-orm pg
npm install -D typescript tsx vitest drizzle-kit @types/node @types/pg
npx tsc --init --target es2022 --module nodenext --moduleResolution nodenext --strict --skipLibCheck
npm ls --depth=0
cd ..
```

## 3. What the frontend needs (the API design)
```bash
opencode run --agent api-designer "Read src/pages (Leaderboard, Home, Request), data/results.json and AGENTS.md. Propose the REST API for Bench Board: GET /api/health, GET /api/leaderboard, GET /api/models/:id, POST /api/requests (multipart with an optional screenshot). For each give the request and response JSON schema and the error shape. Keep it small: only what the pages use."
```

## 4. The contract
```bash
opencode run --agent developer "Write the API contract from the api-designer's proposal (in the previous session, or read what the pages need) as TypeBox schemas in contract/api.ts, exporting both the schemas and the TypeScript types, so the server and the frontend import the same file. Add a short contract/README.md listing the routes. Do not build the server yet. Run npx tsc --noEmit -p server to check it compiles (add contract/ to server/tsconfig.json include)."
```

My result is in [`contract/api.ts`](contract/api.ts).

## 5. Check the contract against the frontend
```bash
opencode run --agent contract-checker "Compare contract/api.ts with what the frontend shows: src/pages/Leaderboard, Home and Request, and the fields in data/results.json. List every mismatch (missing field, wrong type, a form field with no place in POST /api/requests)."
```

## 6. The database
```bash
opencode run --agent developer "Build the database for the backend in server/: a Drizzle schema in server/src/db/schema.ts with tables models, runs, results and requests (see AGENTS.md and contract/api.ts), drizzle.config.ts reading DATABASE_URL from the environment (never write the password in a file), generate the migration with npm run db:generate, apply it with npm run db:migrate, and a seed script server/src/db/seed.ts that loads the real numbers from ../data/results.json. Run the seed and show the row counts with a query. Then run npm run typecheck and npm test in server/, and fix anything that fails."
```

## 7. Review the schema
```bash
opencode run --agent schema-reviewer "Review server/src/db/schema.ts and the migration in server/drizzle. Max 5 comments."
```

## 8. What is in the database now

```bash
docker exec bench-db psql -U bench -d benchboard -c '\dt'
docker exec bench-db psql -U bench -d benchboard -c 'select count(*) as results from results'
```
