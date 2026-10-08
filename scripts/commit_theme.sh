#!/bin/sh
# Rebuild records and PROGRESS tables, check that no staged file contains the API key,
# then commit and push.  Usage: sh scripts/commit_theme.sh "commit message"
set -e
cd "$(dirname "$0")/.."
python3 scripts/build_records.py
python3 scripts/stage2_log.py
git add -A
if [ -n "$OPENALEX_API_KEY" ]; then
  n=$(git diff --cached --name-only --diff-filter=AM | while read -r f; do
        case "$f" in *.gz) zcat "$f";; *.xlsx) unzip -p "$f";; *) cat "$f";; esac; done | grep -c -F "$OPENALEX_API_KEY" || true)
  if [ "$n" != "0" ]; then echo "API key found in staged files; aborting"; exit 1; fi
fi
git commit -q -m "$1" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HeNfts6HcQmptxhQJFcL2N"
for d in 2 4 8 16 0; do
  git push -q -u origin claude/trusting-mccarthy-9n38o9 && break
  [ "$d" = 0 ] && exit 1; sleep $d
done
git log --oneline -1
