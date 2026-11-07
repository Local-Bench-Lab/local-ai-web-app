#!/bin/bash
# Ep 4: the scaffold, recorded for real in a throwaway folder (/config/scaffold-demo) inside the recorder container.
# Each command is typed on screen, then really run. The folder is deleted after the recording.
P=$'\e[1;32mLocalBenchLabs@gb10\e[0m:\e[1;34m%s\e[0m$ '
run() {
  printf "$P" "$(basename "$PWD")"
  for ((i = 0; i < ${#1}; i++)); do printf '%s' "${1:i:1}"; sleep 0.03; done
  sleep 1.5; echo
  eval "$1"
  echo; sleep 2.5
}
cd /config
clear
run "node --version && npm --version"
run "npm create vite@latest scaffold-demo -- --template react-ts --no-interactive"
run "cd scaffold-demo"
run "ls"
run "npm install"
run "npm install --save-dev vitest jsdom @testing-library/react @testing-library/dom @testing-library/jest-dom"
run "npm pkg set scripts.test='vitest run --passWithNoTests' scripts.typecheck='tsc -b --noEmit'"
run "npm pkg get scripts"
run "npm run lint && npm run typecheck && npm test"
run "npm run dev -- --host 127.0.0.1 --port 5199 --strictPort > /tmp/scaffold-dev.log 2>&1 &"
run "sleep 3; cat /tmp/scaffold-dev.log"
run "node -e \"fetch('http://127.0.0.1:5199/').then(r => console.log('HTTP', r.status, r.statusText))\""
run "pkill -f \"vite --host 127.0.0.1 --port 5199\""
echo "SCAFFOLD-RUN-""FINISHED"
sleep 3
