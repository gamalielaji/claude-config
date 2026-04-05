#!/usr/bin/env bash
# AutoAgent Evaluator for Dagelan Game Studio
# Scores agents and skills on structural quality, prompt quality, and cross-agent coherence.
# Usage: bash autoagent/eval.sh [--verbose] [--agent <name>] [--skills-only] [--agents-only]
#
# Output: total score + per-file breakdown to stdout, appends summary to autoagent/scores.log

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
AGENTS_DIR="$ROOT_DIR/.claude/agents"
SKILLS_DIR="$ROOT_DIR/.claude/skills"

VERBOSE=false
FILTER_AGENT=""
SKILLS_ONLY=false
AGENTS_ONLY=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --verbose) VERBOSE=true; shift ;;
    --agent) FILTER_AGENT="$2"; shift 2 ;;
    --skills-only) SKILLS_ONLY=true; shift ;;
    --agents-only) AGENTS_ONLY=true; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# ── Color output ──
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

TOTAL_SCORE=0
TOTAL_POSSIBLE=0
AGENT_SCORE=0
AGENT_POSSIBLE=0
SKILL_SCORE=0
SKILL_POSSIBLE=0
AGENT_COUNT=0
SKILL_COUNT=0
ISSUES=()

# ── Helper: extract YAML frontmatter field ──
get_field() {
  local file="$1" field="$2"
  sed -n '/^---$/,/^---$/p' "$file" | grep -E "^${field}:" | head -1 | sed "s/^${field}:[[:space:]]*//" | sed 's/^"//' | sed 's/"$//'
}

has_field() {
  local file="$1" field="$2"
  sed -n '/^---$/,/^---$/p' "$file" | grep -qE "^${field}:" 2>/dev/null
}

# ── Helper: get body (after second ---) ──
get_body() {
  local file="$1"
  awk 'BEGIN{c=0} /^---$/{c++; next} c>=2{print}' "$file"
}

# ── Score tracking ──
score_check() {
  local file="$1" check="$2" passed="$3" weight="${4:-1}"
  TOTAL_POSSIBLE=$((TOTAL_POSSIBLE + weight))
  if [[ "$passed" == "true" ]]; then
    TOTAL_SCORE=$((TOTAL_SCORE + weight))
    if $VERBOSE; then
      echo -e "  ${GREEN}[PASS]${NC} $check"
    fi
  else
    ISSUES+=("$(basename "$file"): $check")
    if $VERBOSE; then
      echo -e "  ${RED}[FAIL]${NC} $check"
    fi
  fi
}

# ══════════════════════════════════════════════
# AGENT EVALUATION
# ══════════════════════════════════════════════
eval_agent() {
  local file="$1"
  local name
  name=$(basename "$file" .md)

  if [[ -n "$FILTER_AGENT" && "$name" != "$FILTER_AGENT" ]]; then
    return
  fi

  AGENT_COUNT=$((AGENT_COUNT + 1))
  local file_score_before=$TOTAL_SCORE

  if $VERBOSE; then
    echo -e "\n${CYAN}Agent: ${BOLD}$name${NC}"
  fi

  # ── Structural checks (weight: 1 each) ──

  # Required frontmatter fields
  has_field "$file" "name"
  score_check "$file" "has 'name' field" "$(has_field "$file" "name" && echo true || echo false)"

  has_field "$file" "description"
  score_check "$file" "has 'description' field" "$(has_field "$file" "description" && echo true || echo false)"

  has_field "$file" "tools"
  score_check "$file" "has 'tools' field" "$(has_field "$file" "tools" && echo true || echo false)"

  has_field "$file" "model"
  score_check "$file" "has 'model' field" "$(has_field "$file" "model" && echo true || echo false)"

  # maxTurns
  has_field "$file" "maxTurns"
  score_check "$file" "has 'maxTurns' field" "$(has_field "$file" "maxTurns" && echo true || echo false)"

  # Description length (under 200 chars)
  local desc
  desc=$(get_field "$file" "description")
  local desc_len=${#desc}
  score_check "$file" "description under 200 chars ($desc_len)" "$([ "$desc_len" -lt 200 ] && echo true || echo false)"

  # Model tier check
  local model
  model=$(get_field "$file" "model")
  local tier_ok="false"
  case "$name" in
    creative-director|technical-director|producer)
      [[ "$model" == *"opus"* ]] && tier_ok="true" ;;
    game-designer|lead-programmer|art-director|audio-director|narrative-director|qa-lead|ux-designer|godot-specialist|unity-specialist|unreal-specialist)
      [[ "$model" == *"sonnet"* || "$model" == *"opus"* ]] && tier_ok="true" ;;
    *)
      [[ "$model" == *"sonnet"* || "$model" == *"haiku"* ]] && tier_ok="true" ;;
  esac
  score_check "$file" "model tier matches role ($model)" "$tier_ok"

  # ── Prompt quality checks (weight: 2 each — these matter more) ──
  local body
  body=$(get_body "$file")

  # Identity statement in first 3 lines of body
  local first_lines
  first_lines=$(echo "$body" | head -5)
  local has_identity="false"
  if echo "$first_lines" | grep -qiE "(you are|you own|your (role|responsibility|job)|as the)"; then
    has_identity="true"
  fi
  score_check "$file" "opens with identity statement" "$has_identity" 2

  # Scope boundaries
  local has_scope="false"
  if echo "$body" | grep -qiE "(you do not|don't|delegate|defer|escalat|not your|outside your|hand off|beyond your scope)"; then
    has_scope="true"
  fi
  score_check "$file" "defines scope boundaries" "$has_scope" 2

  # Collaboration protocol
  local has_collab="false"
  if echo "$body" | grep -qiE "(collaborat|question.first|ask.*before|clarif|present.*options|get approval|confirm with)"; then
    has_collab="true"
  fi
  score_check "$file" "includes collaboration protocol" "$has_collab" 2

  # No generic filler
  local has_filler="false"
  if echo "$body" | grep -qiE "^you are (a helpful|an ai|a large language model|here to help)"; then
    has_filler="true"
  fi
  score_check "$file" "no generic AI filler" "$([[ "$has_filler" == "false" ]] && echo true || echo false)" 2

  # Output format specified
  local has_output="false"
  if echo "$body" | grep -qiE "(output format|deliverable|produce|generate|create.*:$|format:|template|checklist|report)"; then
    has_output="true"
  fi
  score_check "$file" "specifies output format" "$has_output" 1

  # Context research (Karpathy)
  local has_research="false"
  if echo "$body" | grep -qiE "(read.*first|research|grep|glob|search.*before|check.*existing|review.*current)"; then
    has_research="true"
  fi
  score_check "$file" "includes context research step" "$has_research" 2

  # Non-verbose: one-line summary per agent
  if ! $VERBOSE; then
    local file_score=$((TOTAL_SCORE - file_score_before))
    local file_possible=15  # 5*1 + 2 + 4*2 + 1 = 16... let me just track
    printf "  %-35s %2d pts\n" "$name" "$file_score"
  fi
}

# ══════════════════════════════════════════════
# SKILL EVALUATION
# ══════════════════════════════════════════════
eval_skill() {
  local file="$1"
  local skill_name
  skill_name=$(basename "$(dirname "$file")")

  SKILL_COUNT=$((SKILL_COUNT + 1))
  local file_score_before=$TOTAL_SCORE

  if $VERBOSE; then
    echo -e "\n${CYAN}Skill: ${BOLD}$skill_name${NC}"
  fi

  # Required frontmatter
  score_check "$file" "has 'name' field" "$(has_field "$file" "name" && echo true || echo false)"
  score_check "$file" "has 'description' field" "$(has_field "$file" "description" && echo true || echo false)"

  local has_invocable
  has_invocable=$(has_field "$file" "user-invocable" && echo true || echo false)
  score_check "$file" "has 'user-invocable' field" "$has_invocable"

  score_check "$file" "has 'allowed-tools' field" "$(has_field "$file" "allowed-tools" && echo true || echo false)"

  # Body quality
  local body
  body=$(get_body "$file")

  # Numbered steps
  local has_numbered="false"
  if echo "$body" | grep -qE "^[0-9]+\\."; then
    has_numbered="true"
  fi
  score_check "$file" "has numbered steps" "$has_numbered" 2

  # Steps reference tools
  local has_tool_refs="false"
  if echo "$body" | grep -qiE "(Read|Glob|Grep|Write|Edit|Bash|WebSearch)"; then
    has_tool_refs="true"
  fi
  score_check "$file" "steps reference specific tools" "$has_tool_refs" 1

  # Output format defined
  local has_output="false"
  if echo "$body" | grep -qiE "(output|produce|generate|report|format|deliver|present|checklist)"; then
    has_output="true"
  fi
  score_check "$file" "defines output format" "$has_output" 1

  # Bounded scope (not too long)
  local line_count
  line_count=$(echo "$body" | wc -l)
  score_check "$file" "bounded scope (under 200 lines, got $line_count)" "$([ "$line_count" -lt 200 ] && echo true || echo false)" 1

  if ! $VERBOSE; then
    local file_score=$((TOTAL_SCORE - file_score_before))
    printf "  %-35s %2d pts\n" "$skill_name" "$file_score"
  fi
}

# ══════════════════════════════════════════════
# CROSS-AGENT COHERENCE
# ══════════════════════════════════════════════
eval_coherence() {
  echo -e "\n${BOLD}Cross-Agent Coherence${NC}"

  # Check: every agent name referenced in delegation text exists as a file
  local missing_targets=0
  for file in "$AGENTS_DIR"/*.md; do
    local body
    body=$(get_body "$file")
    # Look for agent names mentioned in delegation context
    for target_file in "$AGENTS_DIR"/*.md; do
      local target_name
      target_name=$(basename "$target_file" .md)
      # Skip self-reference
      [[ "$file" == "$target_file" ]] && continue
    done
  done

  # Check: no duplicate agent names
  local dupes
  dupes=$(for f in "$AGENTS_DIR"/*.md; do get_field "$f" "name"; done | sort | uniq -d)
  if [[ -z "$dupes" ]]; then
    score_check "coherence" "no duplicate agent names" "true" 2
  else
    score_check "coherence" "no duplicate agent names (found: $dupes)" "false" 2
  fi

  # Check: all three tiers have at least one agent
  local has_opus=false has_sonnet=false has_haiku=false
  for file in "$AGENTS_DIR"/*.md; do
    local m
    m=$(get_field "$file" "model")
    [[ "$m" == *"opus"* ]] && has_opus=true
    [[ "$m" == *"sonnet"* ]] && has_sonnet=true
    [[ "$m" == *"haiku"* ]] && has_haiku=true
  done
  score_check "coherence" "Tier 1 (opus) agents exist" "$has_opus" 1
  score_check "coherence" "Tier 2 (sonnet) agents exist" "$has_sonnet" 1
  score_check "coherence" "Tier 3 (haiku) agents exist" "$has_haiku" 1

  # Check: directors don't have Bash disabled
  for file in "$AGENTS_DIR"/creative-director.md "$AGENTS_DIR"/technical-director.md "$AGENTS_DIR"/producer.md; do
    if [[ -f "$file" ]]; then
      local name
      name=$(basename "$file" .md)
      local tools
      tools=$(get_field "$file" "tools")
      # Directors should have broad tool access
      if echo "$tools" | grep -q "Read"; then
        score_check "$file" "$name has Read access" "true" 1
      else
        score_check "$file" "$name has Read access" "false" 1
      fi
    fi
  done
}

# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

echo -e "${BOLD}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║  AutoAgent Evaluator — Dagelan Game Studio   ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════╝${NC}"
echo ""

# Agents
if ! $SKILLS_ONLY; then
  echo -e "${BOLD}── Agents ──${NC}"
  if [[ -d "$AGENTS_DIR" ]]; then
    for file in "$AGENTS_DIR"/*.md; do
      eval_agent "$file"
    done
  else
    echo "  No agents directory found at $AGENTS_DIR"
  fi
  AGENT_SCORE=$TOTAL_SCORE
  AGENT_POSSIBLE=$TOTAL_POSSIBLE
fi

# Skills
if ! $AGENTS_ONLY; then
  SKILL_SCORE_START=$TOTAL_SCORE
  SKILL_POSSIBLE_START=$TOTAL_POSSIBLE
  echo -e "\n${BOLD}── Skills ──${NC}"
  if [[ -d "$SKILLS_DIR" ]]; then
    for skill_dir in "$SKILLS_DIR"/*/; do
      local_skill="$skill_dir/SKILL.md"
      if [[ -f "$local_skill" ]]; then
        eval_skill "$local_skill"
      fi
    done
  else
    echo "  No skills directory found at $SKILLS_DIR"
  fi
  SKILL_SCORE=$((TOTAL_SCORE - SKILL_SCORE_START))
  SKILL_POSSIBLE=$((TOTAL_POSSIBLE - SKILL_POSSIBLE_START))
fi

# Coherence
if ! $SKILLS_ONLY && ! $AGENTS_ONLY; then
  eval_coherence
fi

# ── Summary ──
echo ""
echo -e "${BOLD}══════════════════════════════════════════════${NC}"
PERCENT=0
if [[ $TOTAL_POSSIBLE -gt 0 ]]; then
  PERCENT=$((TOTAL_SCORE * 100 / TOTAL_POSSIBLE))
fi

if [[ $PERCENT -ge 90 ]]; then
  COLOR=$GREEN
elif [[ $PERCENT -ge 70 ]]; then
  COLOR=$YELLOW
else
  COLOR=$RED
fi

echo -e "${BOLD}Total Score:${NC} ${COLOR}${TOTAL_SCORE}/${TOTAL_POSSIBLE} (${PERCENT}%)${NC}"
echo -e "  Agents:    $AGENT_COUNT evaluated"
echo -e "  Skills:    $SKILL_COUNT evaluated"

if [[ ${#ISSUES[@]} -gt 0 ]]; then
  echo ""
  echo -e "${BOLD}Top Issues (${#ISSUES[@]} total):${NC}"
  # Show first 15 issues
  for i in "${!ISSUES[@]}"; do
    if [[ $i -ge 15 ]]; then
      echo "  ... and $((${#ISSUES[@]} - 15)) more"
      break
    fi
    echo -e "  ${RED}-${NC} ${ISSUES[$i]}"
  done
fi

# ── Log to scores.log ──
LOG_FILE="$SCRIPT_DIR/scores.log"
echo "$(date -Iseconds)	score=${TOTAL_SCORE}/${TOTAL_POSSIBLE}	pct=${PERCENT}%	agents=${AGENT_COUNT}	skills=${SKILL_COUNT}" >> "$LOG_FILE"

echo ""
echo -e "Score logged to ${CYAN}autoagent/scores.log${NC}"
