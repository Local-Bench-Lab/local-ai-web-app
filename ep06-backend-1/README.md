# Ep 6: Backend part 1, Postgres + a database

- `runs/be1.sh`: the whole session. Postgres 18 in Docker, `npm init` and every `npm install` on camera, then the API designer, the contract, the contract checker, the database (Drizzle schema, migrations, seed) and the schema reviewer.
- `contract/api.ts`: the API contract (TypeBox) that Qwen 3.8 wrote in that run, unedited.
- `opencode-wrapper.sh`: runs OpenCode in the container with the database URL from an env file. The env file itself is never committed or printed.
