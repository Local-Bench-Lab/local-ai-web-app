#!/bin/sh
# Run the design tasks with a local model, one after another, on the same FigCraft file.
#   sh run_all.sh <model> <out.figcraft> [first-task-number] [-- extra local_agent.py args]
MODEL=${1:-gpt-oss:120b}; OUT=${2:-/config/designs/bench-board-local.figcraft}; FIRST=${3:-1}
shift 3 2>/dev/null; [ "$1" = "--" ] && shift
for t in tasks/[0-9][0-9]-*.md; do
  n=$(basename "$t" | cut -c1-2); [ "$n" = "00" ] && continue
  [ "${n#0}" -lt "$FIRST" ] && continue
  echo "===== $t"
  if [ "$n" = "01" ] && [ "$FIRST" = "1" ]; then DOC=""; else DOC="--doc $OUT"; fi
  python3 local_agent.py --model "$MODEL" --task "$t" $DOC --save "$OUT" "$@" | tail -4
done
