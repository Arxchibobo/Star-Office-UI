#!/bin/bash
# spawn-with-config.sh - Spawn agent with Claude Reconstruction engineering config
# Usage: spawn-with-config.sh <task-id> <task-type> <description>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAWDBOT_ROOT="$(dirname "$SCRIPT_DIR")"
INTEGRATION_CONFIG="$CLAWDBOT_ROOT/config/integration.json"
TEMPLATE_DIR="$CLAWDBOT_ROOT/templates"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🦁 Spawn Engineering Agent (with Claude Config)   ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if integration config exists
if [ ! -f "$INTEGRATION_CONFIG" ]; then
    echo -e "${YELLOW}⚠ Integration config not found${NC}"
    echo "Creating default integration config..."
    cp "$CLAWDBOT_ROOT/config/integration.json.example" "$INTEGRATION_CONFIG" 2>/dev/null || {
        echo "Please run setup first: ./swarm setup-integration"
        exit 1
    }
fi

# Read integration config
CLAUDE_RECON_PATH=$(jq -r '.claudeReconstruction.path' "$INTEGRATION_CONFIG")
CLAUDE_RECON_ENABLED=$(jq -r '.claudeReconstruction.enabled' "$INTEGRATION_CONFIG")

# Check if Claude Reconstruction is available
if [ "$CLAUDE_RECON_ENABLED" != "true" ]; then
    echo -e "${YELLOW}⚠ Claude Reconstruction is disabled in config${NC}"
    echo "Enable it in: $INTEGRATION_CONFIG"
    exit 1
fi

if [ ! -d "$CLAUDE_RECON_PATH" ]; then
    echo -e "${YELLOW}⚠ Claude Reconstruction not found at: $CLAUDE_RECON_PATH${NC}"
    echo ""
    echo "Please install it first:"
    echo "  cd ~/.openclaw/workspace"
    echo "  git clone https://github.com/Arxchibobo/claude-Reconstruction.git"
    exit 1
fi

echo -e "${GREEN}✓${NC} Claude Reconstruction found: $CLAUDE_RECON_PATH"
echo ""

# Interactive input
read -p "Task ID (e.g., feat-user-auth): " TASK_ID
read -p "Task Type (coding/testing/security/api/frontend): " TASK_TYPE
read -p "Description: " DESCRIPTION
echo ""

# Detect relevant rules based on task type
DOMAIN_RULES=""
AUTO_LOADED_DOCS=""
CONTEXT_BUDGET="15"

case "$TASK_TYPE" in
    coding|code)
        DOMAIN_RULES="- rules/domain/coding.md (Code style and organization)"
        AUTO_LOADED_DOCS="- rules/core/\n- rules/domain/coding.md"
        CONTEXT_BUDGET="18"
        ;;
    testing|test)
        DOMAIN_RULES="- rules/domain/testing.md (Test standards)\n- rules/domain/coding.md (Code style)"
        AUTO_LOADED_DOCS="- rules/core/\n- rules/domain/testing.md\n- capabilities/browser-automation (if needed)"
        CONTEXT_BUDGET="20"
        ;;
    security|auth)
        DOMAIN_RULES="- rules/domain/security.md (Security best practices)\n- rules/domain/coding.md (Code style)"
        AUTO_LOADED_DOCS="- rules/core/\n- rules/domain/security.md\n- rules/domain/coding.md"
        CONTEXT_BUDGET="22"
        ;;
    api)
        DOMAIN_RULES="- rules/domain/coding.md (API design)\n- rules/domain/testing.md (API testing)"
        AUTO_LOADED_DOCS="- rules/core/\n- rules/domain/coding.md\n- capabilities/api-design"
        CONTEXT_BUDGET="19"
        ;;
    frontend|ui)
        DOMAIN_RULES="- rules/domain/coding.md (Component design)\n- rules/domain/testing.md (Component testing)"
        AUTO_LOADED_DOCS="- rules/core/\n- rules/domain/coding.md\n- capabilities/frontend-frameworks"
        CONTEXT_BUDGET="17"
        ;;
    *)
        DOMAIN_RULES="- rules/domain/coding.md (General coding standards)"
        AUTO_LOADED_DOCS="- rules/core/\n- rules/domain/coding.md"
        CONTEXT_BUDGET="16"
        ;;
esac

# Prompt user for file details
echo "Files to create (comma-separated, or press Enter to skip):"
read FILES_TO_CREATE
echo ""

echo "Files to modify (comma-separated, or press Enter to skip):"
read FILES_TO_MODIFY
echo ""

echo "Constraints (press Enter to skip):"
read CONSTRAINTS
echo ""

# Generate engineering prompt from template
PROMPT_FILE="$CLAWDBOT_ROOT/.prompt-$TASK_ID.md"

# Read template and replace placeholders
sed \
    -e "s|{TASK_ID}|$TASK_ID|g" \
    -e "s|{TASK_TYPE}|$TASK_TYPE|g" \
    -e "s|{DESCRIPTION}|$DESCRIPTION|g" \
    -e "s|{DOMAIN_RULES}|$DOMAIN_RULES|g" \
    -e "s|{AUTO_LOADED_DOCS}|$AUTO_LOADED_DOCS|g" \
    -e "s|{CONTEXT_BUDGET}|$CONTEXT_BUDGET|g" \
    -e "s|{FILES_TO_CREATE}|${FILES_TO_CREATE:-None}|g" \
    -e "s|{FILES_TO_MODIFY}|${FILES_TO_MODIFY:-None}|g" \
    -e "s|{CONSTRAINTS}|${CONSTRAINTS:-None}|g" \
    "$TEMPLATE_DIR/engineering.md" > "$PROMPT_FILE"

echo -e "${GREEN}✓${NC} Engineering prompt generated: $PROMPT_FILE"
echo ""

# Show summary
echo "=== Agent Configuration Summary ==="
echo "Task ID:        $TASK_ID"
echo "Task Type:      $TASK_TYPE"
echo "Agent Type:     claude (with engineering config)"
echo "Config Path:    $CLAUDE_RECON_PATH"
echo "Context Budget: ~${CONTEXT_BUDGET}%"
echo "Workflow:       Plan → Confirm → Execute → Deliver"
echo ""

# Confirm
read -p "Start agent with this configuration? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Set environment variables for Claude
export CLAUDE_CONFIG="$CLAUDE_RECON_PATH"
export CLAUDE_ENGINEERING_MODE="true"

# Call spawn-agent.sh with the generated prompt
echo ""
echo "=== Spawning Engineering Agent ===" 
"$SCRIPT_DIR/spawn-agent.sh" "$TASK_ID" "claude" "$DESCRIPTION" "$PROMPT_FILE"

echo ""
echo -e "${GREEN}✓ Engineering agent spawned!${NC}"
echo ""
echo "Monitor progress:"
echo "  ./swarm status"
echo "  ./swarm logs $TASK_ID"
echo ""
echo "The agent will follow the 4-step workflow:"
echo "  1. Plan (creates implementation plan)"
echo "  2. Confirm (presents plan for approval)"
echo "  3. Execute (implements following rules)"
echo "  4. Deliver (creates PR with checklist)"
echo ""
