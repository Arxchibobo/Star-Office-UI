#!/bin/bash
# setup.sh - Agent Swarm 系统设置和验证

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}"
cat <<'EOF'
╔═══════════════════════════════════════════════════════╗
║           🤖 Agent Swarm Setup & Verification        ║
╚═══════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# 检查函数
check_command() {
    local cmd="$1"
    local name="$2"
    local install_hint="$3"
    
    if command -v "$cmd" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $name installed"
        return 0
    else
        echo -e "${RED}✗${NC} $name NOT installed"
        if [ -n "$install_hint" ]; then
            echo -e "  ${YELLOW}Install:${NC} $install_hint"
        fi
        return 1
    fi
}

echo "=== Checking Dependencies ==="
echo ""

# 必需依赖
DEPS_OK=true

check_command "bash" "Bash" || DEPS_OK=false
check_command "git" "Git" "sudo apt install git" || DEPS_OK=false
check_command "jq" "jq (JSON processor)" "sudo apt install jq" || DEPS_OK=false
check_command "tmux" "tmux" "sudo apt install tmux" || DEPS_OK=false
check_command "gh" "GitHub CLI" "See https://cli.github.com/" || DEPS_OK=false

echo ""
echo "=== Checking Optional Tools ==="
echo ""

# 可选工具
check_command "codex" "Codex CLI" "npm install -g @openai/codex-cli" || echo -e "  ${YELLOW}Note:${NC} Needed if using Codex agents"
check_command "claude" "Claude CLI" "npm install -g @anthropic/claude-cli" || echo -e "  ${YELLOW}Note:${NC} Needed if using Claude agents"

echo ""

if [ "$DEPS_OK" = false ]; then
    echo -e "${RED}✗ Some required dependencies are missing${NC}"
    echo ""
    echo "Please install missing dependencies and run this script again."
    exit 1
fi

echo -e "${GREEN}✓ All required dependencies installed${NC}"
echo ""

# 检查 GitHub CLI 认证
echo "=== Checking GitHub CLI Authentication ==="
if gh auth status &> /dev/null; then
    echo -e "${GREEN}✓${NC} GitHub CLI authenticated"
else
    echo -e "${YELLOW}⚠${NC} GitHub CLI not authenticated"
    echo ""
    read -p "Run 'gh auth login' now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gh auth login
    else
        echo "You'll need to run 'gh auth login' before using the system"
    fi
fi

echo ""

# 检查文件结构
echo "=== Verifying File Structure ==="

FILES=(
    "$SCRIPT_DIR/active-tasks.json"
    "$SCRIPT_DIR/config/swarm-config.json"
    "$SCRIPT_DIR/scripts/spawn-agent.sh"
    "$SCRIPT_DIR/scripts/check-agents.sh"
    "$SCRIPT_DIR/scripts/run-code-review.sh"
    "$SCRIPT_DIR/scripts/task-manager.sh"
    "$SCRIPT_DIR/../swarm"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $(basename $file)"
    else
        echo -e "${RED}✗${NC} $(basename $file) missing"
    fi
done

echo ""

# 检查权限
echo "=== Checking Permissions ==="

SCRIPTS=(
    "$SCRIPT_DIR/scripts/spawn-agent.sh"
    "$SCRIPT_DIR/scripts/check-agents.sh"
    "$SCRIPT_DIR/scripts/run-code-review.sh"
    "$SCRIPT_DIR/scripts/task-manager.sh"
    "$SCRIPT_DIR/../swarm"
)

for script in "${SCRIPTS[@]}"; do
    if [ -x "$script" ]; then
        echo -e "${GREEN}✓${NC} $(basename $script) executable"
    else
        echo -e "${YELLOW}⚠${NC} $(basename $script) not executable, fixing..."
        chmod +x "$script"
        echo -e "  ${GREEN}✓${NC} Fixed"
    fi
done

echo ""

# 创建必要目录
echo "=== Creating Directories ==="

DIRS=(
    "$SCRIPT_DIR/logs"
    "$SCRIPT_DIR/../worktrees"
)

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} $(basename $dir)/ exists"
    else
        mkdir -p "$dir"
        echo -e "${GREEN}✓${NC} Created $(basename $dir)/"
    fi
done

echo ""

# 检查 Gemini API Key
echo "=== Checking API Keys ==="

if [ -n "$GEMINI_API_KEY" ]; then
    echo -e "${GREEN}✓${NC} GEMINI_API_KEY configured"
else
    echo -e "${YELLOW}⚠${NC} GEMINI_API_KEY not set"
    echo "  Gemini Code Assist (free!) won't work without it"
    echo "  Set in ~/.bashrc: export GEMINI_API_KEY=\"your-key\""
fi

echo ""

# 运行快速测试
echo "=== Running Quick Test ==="

echo "Testing JSON operations..."
if echo '[]' | jq '.' > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} JSON operations work"
else
    echo -e "${RED}✗${NC} JSON operations failed"
fi

echo "Testing tmux..."
if tmux new-session -d -s test-swarm-$$ 'echo "test"'; then
    tmux kill-session -t test-swarm-$$ 2>/dev/null
    echo -e "${GREEN}✓${NC} tmux works"
else
    echo -e "${RED}✗${NC} tmux failed"
fi

echo ""

# 总结
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo ""
echo "  1. (Optional) Install cron monitoring:"
echo -e "     ${YELLOW}cd $(dirname $SCRIPT_DIR) && ./swarm install-cron${NC}"
echo ""
echo "  2. Read the documentation:"
echo -e "     ${YELLOW}cat $SCRIPT_DIR/README.md${NC}"
echo ""
echo "  3. Create your first agent:"
echo -e "     ${YELLOW}cd $(dirname $SCRIPT_DIR) && ./swarm spawn${NC}"
echo ""
echo "  4. Check agent status:"
echo -e "     ${YELLOW}./swarm status${NC}"
echo ""
echo "For help:"
echo -e "  ${YELLOW}./swarm help${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
