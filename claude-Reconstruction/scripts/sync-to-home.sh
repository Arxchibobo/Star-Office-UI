#!/bin/bash
# sync-to-home.sh
# Sync claude-reconstruction repo to ~/.claude/
#
# Usage:
#   ./scripts/sync-to-home.sh [--dry-run]

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
TARGET_DIR="$HOME/.claude"

DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo -e "${YELLOW}Dry-run mode: showing what would be done${NC}\n"
fi

copy_directory() {
    local src=$1
    local dest=$2
    local label=$3

    if [ ! -d "$src" ]; then
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] cp -r $src/* $dest/"
    else
        mkdir -p "$dest"
        cp -r "$src"/* "$dest/"
        echo -e "${GREEN}✓${NC} $label"
    fi
}

copy_file() {
    local src=$1
    local dest=$2
    local label=$3

    if [ ! -f "$src" ]; then
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        echo "  [DRY-RUN] cp $src $dest"
    else
        cp "$src" "$dest"
        echo -e "${GREEN}✓${NC} $label"
    fi
}

if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}Target $TARGET_DIR does not exist${NC}"
    exit 1
fi

echo -e "${BLUE}Source: $PROJECT_ROOT${NC}"
echo -e "${BLUE}Target: $TARGET_DIR${NC}"
echo ""

# Backup CLAUDE.md
if [ -f "$TARGET_DIR/CLAUDE.md" ] && [ "$DRY_RUN" = false ]; then
    cp "$TARGET_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md.backup.$(date +%Y%m%d-%H%M%S)"
    echo -e "${YELLOW}Backed up existing CLAUDE.md${NC}"
fi

# Sync core files
copy_file "$PROJECT_ROOT/CLAUDE.md" "$TARGET_DIR/CLAUDE.md" "CLAUDE.md"
copy_file "$PROJECT_ROOT/CONTEXT_MANAGER.md" "$TARGET_DIR/CONTEXT_MANAGER.md" "CONTEXT_MANAGER.md"

# Sync directories
copy_directory "$PROJECT_ROOT/rules" "$TARGET_DIR/rules" "rules/"
copy_directory "$PROJECT_ROOT/index" "$TARGET_DIR/index" "index/"
copy_directory "$PROJECT_ROOT/capabilities" "$TARGET_DIR/capabilities" "capabilities/"
copy_directory "$PROJECT_ROOT/errors" "$TARGET_DIR/errors" "errors/"
copy_directory "$PROJECT_ROOT/design" "$TARGET_DIR/design" "design/"
copy_directory "$PROJECT_ROOT/vibe-marketing" "$TARGET_DIR/vibe-marketing" "vibe-marketing/"

echo ""
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}Dry-run complete. Run without --dry-run to sync.${NC}"
else
    echo -e "${GREEN}Sync complete. Restart Claude Code to apply.${NC}"
fi
