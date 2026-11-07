#!/bin/bash
# V5 (backend) run 1, step by step for a newbie: start Postgres, install the server packages, then the agents design
# the API contract and the database. The password lives in secrets/ and is never printed.
step() { printf '\n\033[1;33m== %s ==\033[0m\n' "$1"; }
run() { printf '\033[1;32m$\033[0m %s\n' "$1"; sleep 2; bash -c "$1"; sleep 2; }
# srv: a command inside the app container (the sandbox), in the server/ folder
srv() { printf '\033[1;36m(app container) server$\033[0m %s\n' "$1"; sleep 2; docker exec -u 1000:1000 -e HOME=/config -w /config/bench-board-app/server recorder sh -c "$1"; sleep 2; }
CHECK="Then run npm run typecheck and npm test in server/, and fix anything that fails."

step "1. Get Postgres (the database), in Docker"
run 'docker pull postgres:18'
run 'docker network create benchnet'
run 'docker run -d --name bench-db --network benchnet --env-file ../../../../secrets/bench-db.env -p 127.0.0.1:5432:5432 postgres:18'
run 'docker network connect benchnet recorder'

run 'until docker exec bench-db pg_isready -U bench -d benchboard; do sleep 1; done'

step "2. Install the server packages"
srv 'npm init -y'
srv 'npm pkg set type=module "scripts.dev=tsx watch src/index.ts" "scripts.start=tsx src/index.ts" "scripts.typecheck=tsc --noEmit" "scripts.test=vitest run --passWithNoTests" "scripts.db:generate=drizzle-kit generate" "scripts.db:migrate=drizzle-kit migrate"'
srv 'npm install fastify @fastify/multipart @fastify/cors @sinclair/typebox drizzle-orm pg'
srv 'npm install -D typescript tsx vitest drizzle-kit @types/node @types/pg'
srv 'npx tsc --init --target es2022 --module nodenext --moduleResolution nodenext --strict --skipLibCheck'
srv 'npm ls --depth=0'

step "3. api-designer (gpt-oss 120B): what the frontend needs"
time opencode run --agent api-designer "Read src/pages (Leaderboard, Home, Request), data/results.json and AGENTS.md. Propose the REST API for Bench Board: GET /api/health, GET /api/leaderboard, GET /api/models/:id, POST /api/requests (multipart with an optional screenshot). For each give the request and response JSON schema and the error shape. Keep it small: only what the pages use."

step "4. developer (Qwen 3.8): write the contract"
time opencode run --agent developer "Write the API contract from the api-designer's proposal (in the previous session, or read what the pages need) as TypeBox schemas in contract/api.ts, exporting both the schemas and the TypeScript types, so the server and the frontend import the same file. Add a short contract/README.md listing the routes. Do not build the server yet. Run npx tsc --noEmit -p server to check it compiles (add contract/ to server/tsconfig.json include)."

step "5. contract-checker (Qwen 3.8): contract vs the frontend"
time opencode run --agent contract-checker "Compare contract/api.ts with what the frontend shows: src/pages/Leaderboard, Home and Request, and the fields in data/results.json. List every mismatch (missing field, wrong type, a form field with no place in POST /api/requests)."

step "6. developer (Qwen 3.8): the database"
time opencode run --agent developer "Build the database for the backend in server/: a Drizzle schema in server/src/db/schema.ts with tables models, runs, results and requests (see AGENTS.md and contract/api.ts), drizzle.config.ts reading DATABASE_URL from the environment (never write the password in a file), generate the migration with npm run db:generate, apply it with npm run db:migrate, and a seed script server/src/db/seed.ts that loads the real numbers from ../data/results.json. Run the seed and show the row counts with a query. $CHECK"

step "7. schema-reviewer (gpt-oss 120B): review the schema"
time opencode run --agent schema-reviewer "Review server/src/db/schema.ts and the migration in server/drizzle. Max 5 comments."

step "8. what is in the database now"
run 'docker exec bench-db psql -U bench -d benchboard -c '\''\dt'\'''
run 'docker exec bench-db psql -U bench -d benchboard -c '\''select count(*) as results from results'\'''
echo "BE1-RUN-""FINISHED"
