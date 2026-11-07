#!/bin/sh
# OpenCode lives in the recorder container (no access to home files); this runs it there, in the project folder.
exec docker exec -u 1000:1000 -e HOME=/config -w /config/bench-board-app recorder /config/apps/opencode/opencode "$@"
