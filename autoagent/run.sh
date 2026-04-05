#!/usr/bin/env bash
# AutoAgent Runner — Kicks off the self-improving loop via Claude Code CLI
# Usage: bash autoagent/run.sh [--max-iterations N] [--dry-run]
#
# This script launches Claude Code with program.md as the directive,
# instructing it to run the eval → diagnose → edit → re-eval loop.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

MAX_ITERATIONS=50
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --max-iterations) MAX_ITERATIONS="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Ensure we're in the project root
cd "$ROOT_DIR"

# Initialize results.tsv if not present
RESULTS_FILE="$SCRIPT_DIR/results.tsv"
if [[ ! -f "$RESULTS_FILE" ]]; then
  echo -e "timestamp\texperiment\tscore_before\tscore_after\tverdict\tnotes" > "$RESULTS_FILE"
fi

# Run baseline eval
echo "╔══════════════════════════════════════════════╗"
echo "║  AutoAgent Runner — Dagelan Game Studio      ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "Running baseline evaluation..."
bash "$SCRIPT_DIR/eval.sh"
echo ""

if $DRY_RUN; then
  echo "[DRY RUN] Would launch Claude Code with program.md directive."
  echo "[DRY RUN] Max iterations: $MAX_ITERATIONS"
  exit 0
fi

# Launch Claude Code with the program.md directive
# The meta-agent reads program.md and enters the autonomous improvement loop.
PROMPT="Read autoagent/program.md in full. This is your directive. \
Follow the Setup Checklist, then enter the Experiment Loop. \
Run up to $MAX_ITERATIONS iterations. \
After each iteration, log results to autoagent/results.tsv. \
If you plateau for 5 iterations, switch focus areas as described in the program. \
Begin now."

echo "Launching meta-agent..."
echo "Max iterations: $MAX_ITERATIONS"
echo ""

# Use claude CLI if available, otherwise print instructions
if command -v claude &> /dev/null; then
  claude --print "$PROMPT"
else
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Claude Code CLI not found in PATH."
  echo ""
  echo "To run the meta-agent manually:"
  echo "  1. Open Claude Code in this directory"
  echo "  2. Paste this prompt:"
  echo ""
  echo "  $PROMPT"
  echo ""
  echo "Or invoke from CLI:"
  echo "  claude \"$PROMPT\""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi
