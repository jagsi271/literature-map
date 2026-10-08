#!/bin/sh
# Regenerate every record-dependent Stage 3 output from cached data (no new searches; the
# emerging-terms check may make a few 1-credit list calls), then commit and push.
# Usage: sh scripts/stage3_build.sh "commit message"
set -e
cd "$(dirname "$0")/.."
python3 scripts/build_records.py
python3 scripts/emerging_terms.py | tail -3
OPENALEX_OFFLINE=1 python3 scripts/growth_counts.py table > /dev/null
python3 scripts/population_counts.py table
python3 scripts/stage3_analysis.py
python3 scripts/build_xlsx.py
python3 scripts/export_bib.py
sh scripts/commit_theme.sh "$1"
