#!/bin/bash
# Claude Reconstruction install verification

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

CLAUDE_DIR="$HOME/.claude"
ERRORS=0

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         Claude Reconstruction v5.0 - Verify                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

verify_file() {
    local file_path="$1"
    local description="$2"

    if [ -f "$file_path" ]; then
        echo -e "${GREEN}✓${NC} $description"
        return 0
    else
        echo -e "${RED}✗${NC} $description (missing: $file_path)"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

verify_dir() {
    local dir_path="$1"
    local description="$2"

    if [ -d "$dir_path" ]; then
        echo -e "${GREEN}✓${NC} $description"
        return 0
    else
        echo -e "${RED}✗${NC} $description (missing: $dir_path)"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

echo -e "${YELLOW}[1/4] Core config files...${NC}"
verify_file "$CLAUDE_DIR/CLAUDE.md" "CLAUDE.md (entry point)"
verify_file "$CLAUDE_DIR/CONTEXT_MANAGER.md" "CONTEXT_MANAGER.md (smart loading)"
echo ""

echo -e "${YELLOW}[2/4] Rules engine...${NC}"
verify_dir "$CLAUDE_DIR/rules" "rules/"
verify_dir "$CLAUDE_DIR/rules/core" "rules/core/"
verify_dir "$CLAUDE_DIR/rules/domain" "rules/domain/"
verify_dir "$CLAUDE_DIR/rules/delegator" "rules/delegator/"
verify_file "$CLAUDE_DIR/rules/core/work-mode.md" "core/work-mode.md"
verify_file "$CLAUDE_DIR/rules/core/blocking-rules.md" "core/blocking-rules.md"
verify_file "$CLAUDE_DIR/rules/coding-style.md" "coding-style.md"
verify_file "$CLAUDE_DIR/rules/security.md" "security.md"
echo ""

echo -e "${YELLOW}[3/4] Index & capabilities...${NC}"
verify_dir "$CLAUDE_DIR/index" "index/"
verify_file "$CLAUDE_DIR/index/task-router.md" "task-router.md"
verify_dir "$CLAUDE_DIR/capabilities" "capabilities/"
verify_file "$CLAUDE_DIR/capabilities/mcp-servers.md" "mcp-servers.md"
verify_file "$CLAUDE_DIR/capabilities/skills-guide.md" "skills-guide.md"
echo ""

echo -e "${YELLOW}[4/4] Error library...${NC}"
verify_dir "$CLAUDE_DIR/errors" "errors/"
verify_file "$CLAUDE_DIR/errors/ERROR_CATALOG.md" "ERROR_CATALOG.md"
verify_file "$CLAUDE_DIR/errors/top-5-errors.md" "top-5-errors.md"
echo ""

# Results
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo -e "${YELLOW}Config location:${NC} $CLAUDE_DIR"
    echo -e "${YELLOW}Version:${NC} 5.0 (Context Engineering)"
    exit 0
else
    echo -e "${RED}✗ $ERRORS check(s) failed.${NC}"
    echo ""
    echo "Run: ./scripts/install.sh"
    exit 1
fi
