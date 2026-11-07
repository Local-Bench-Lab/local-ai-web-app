#!/bin/sh
# OpenCode in the recorder container (no access to home files), with the database URL from secrets/ (never printed).
exec docker exec -u 1000:1000 -e HOME=/config --env-file $HOME/localbenchlab/secrets/bench-server.env -w /config/bench-board-app recorder /config/apps/opencode/opencode "$@"
