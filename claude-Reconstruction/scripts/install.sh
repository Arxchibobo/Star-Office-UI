#!/bin/bash
# Claude Reconstruction install script (Unix/Linux/macOS/Git Bash)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         Claude Reconstruction v5.0                           ║"
echo "║         Claude Code Engineering Config                       ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    MSYS*)      MACHINE=MSYS;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo -e "${YELLOW}OS: ${MACHINE}${NC}"

# Directories
CLAUDE_DIR="$HOME/.claude"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo ""
echo -e "${YELLOW}Source: ${PROJECT_DIR}${NC}"
echo -e "${YELLOW}Target: ${CLAUDE_DIR}${NC}"
echo ""

# Create directory structure
echo -e "${GREEN}[1/5] Creating directories...${NC}"
mkdir -p "$CLAUDE_DIR/rules/core"
mkdir -p "$CLAUDE_DIR/rules/domain"
mkdir -p "$CLAUDE_DIR/rules/delegator"
mkdir -p "$CLAUDE_DIR/index"
mkdir -p "$CLAUDE_DIR/capabilities"
mkdir -p "$CLAUDE_DIR/errors"
mkdir -p "$CLAUDE_DIR/design"
mkdir -p "$CLAUDE_DIR/vibe-marketing"

# Backup existing config
if [ -f "$CLAUDE_DIR/CLAUDE.md" ]; then
    echo -e "${YELLOW}[Backup] Backing up existing CLAUDE.md...${NC}"
    cp "$CLAUDE_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Install core config
echo -e "${GREEN}[2/5] Installing core config...${NC}"
cp "$PROJECT_DIR/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
cp "$PROJECT_DIR/CONTEXT_MANAGER.md" "$CLAUDE_DIR/CONTEXT_MANAGER.md"

# Install rules
echo -e "${GREEN}[3/5] Installing rules...${NC}"
cp -r "$PROJECT_DIR/rules/"* "$CLAUDE_DIR/rules/"

# Install index & capabilities
echo -e "${GREEN}[4/5] Installing index, capabilities, errors...${NC}"
cp -r "$PROJECT_DIR/index/"* "$CLAUDE_DIR/index/"
cp -r "$PROJECT_DIR/capabilities/"* "$CLAUDE_DIR/capabilities/"
cp -r "$PROJECT_DIR/errors/"* "$CLAUDE_DIR/errors/"

# Install optional resources
echo -e "${GREEN}[5/5] Installing design & marketing docs...${NC}"
[ -d "$PROJECT_DIR/design" ] && cp -r "$PROJECT_DIR/design/"* "$CLAUDE_DIR/design/"
[ -d "$PROJECT_DIR/vibe-marketing" ] && cp -r "$PROJECT_DIR/vibe-marketing/"* "$CLAUDE_DIR/vibe-marketing/"

# Set permissions
chmod -R 644 "$CLAUDE_DIR"/*.md 2>/dev/null || true
find "$CLAUDE_DIR" -type d -exec chmod 755 {} \; 2>/dev/null || true

# Verify
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Install complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Installed:${NC}"
echo "  - $CLAUDE_DIR/CLAUDE.md (entry point)"
echo "  - $CLAUDE_DIR/CONTEXT_MANAGER.md (smart loading)"
echo "  - $CLAUDE_DIR/rules/ (rules engine)"
echo "  - $CLAUDE_DIR/index/ (navigation)"
echo "  - $CLAUDE_DIR/capabilities/ (capability docs)"
echo "  - $CLAUDE_DIR/errors/ (error library)"
echo "  - $CLAUDE_DIR/design/ (design system)"
echo ""
echo -e "${YELLOW}Next:${NC}"
echo "  1. Start Claude Code"
echo "  2. Config loads automatically"
echo "  3. Context usage: ~20% (down from 60%)"
echo ""
