#!/bin/bash
# V3: the screenshot and review loop on the component gallery, with the decision gate choosing what runs next (max 2 fix rounds).
# Each reviewer's last lines go to the gate (next-agent, Qwen judge), and the script follows its pick.
step() { printf '\n\033[1;33m== %s ==\033[0m\n' "$1"; }
LOG=/tmp/v3-review; mkdir -p $LOG
URL="http://localhost:5173/?view=components"

review() {   # run the three reviewers, keep their output for the gate
  step "visual-checker (Gemma 4): screenshots at 390, 768 and 1440 px"
  time opencode run --agent visual-checker "Open $URL in Chrome and take a screenshot at 390, 768 and 1440 px wide. Compare the components with design/home.png, design/home_mobile.png and design/request.png. List concrete problems, or say PASS." | tee $LOG/visual.txt
  step "react-reviewer (gpt-oss): src/components"
  time opencode run --agent react-reviewer "Review the React code in src/components and src/pages. List concrete problems with file and line, most important first, at most 8. Say PASS if there are none." | tee $LOG/react.txt
  step "css-reviewer (gpt-oss): the CSS modules"
  time opencode run --agent css-reviewer "Review the CSS modules in src/components against src/styles/tokens.css. List concrete problems with file and line, most important first, at most 8. Say PASS if there are none." | tee $LOG/css.txt
}

review
for round in 1 2; do
  step "decision gate (Qwen judge): round $round"
  summary="Reviewers on the component gallery. Visual: $(tail -c 600 $LOG/visual.txt | tr '\n' ' ') React: $(tail -c 600 $LOG/react.txt | tr '\n' ' ') CSS: $(tail -c 600 $LOG/css.txt | tr '\n' ' ')"
  next-agent "$summary" | tee $LOG/gate-$round.txt
  grep -q "^next: developer" $LOG/gate-$round.txt || break
  step "developer (Qwen 3.8): fix round $round"
  time opencode run --agent developer "Fix these review findings in src/components, most important first: $(cat $LOG/visual.txt $LOG/react.txt $LOG/css.txt | tail -c 4000) Then run npm run typecheck, npm run lint and npm test, and check $URL in Chrome at 390 and 1440 px."
  review
done
echo "REVIEW-RUN-""FINISHED"
