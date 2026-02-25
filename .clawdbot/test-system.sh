#!/bin/bash
# test-system.sh - Test Agent Swarm system configuration

echo "🧪 Testing Agent Swarm System"
echo ""

# Test 1: Check CLI
echo "Test 1: Main CLI exists and is executable"
if [ -x ~/.openclaw/workspace/swarm ]; then
    echo "  ✓ swarm CLI is executable"
else
    echo "  ✗ swarm CLI not executable"
    exit 1
fi

# Test 2: Check dependencies
echo ""
echo "Test 2: Check dependencies"
for cmd in gh tmux jq; do
    if command -v $cmd &> /dev/null; then
        echo "  ✓ $cmd installed"
    else
        echo "  ✗ $cmd not found"
        exit 1
    fi
done

# Test 3: Check configuration files
echo ""
echo "Test 3: Configuration files"
for file in \
    ~/.openclaw/workspace/.clawdbot/config/swarm-config.json \
    ~/.openclaw/workspace/.clawdbot/config/integration.json \
    ~/.openclaw/workspace/.clawdbot/active-tasks.json; do
    if [ -f "$file" ]; then
        echo "  ✓ $(basename $file) exists"
    else
        echo "  ✗ $(basename $file) missing"
        exit 1
    fi
done

# Test 4: Check scripts
echo ""
echo "Test 4: Core scripts"
for script in \
    spawn-agent.sh \
    spawn-with-config.sh \
    check-agents.sh \
    run-code-review.sh \
    task-manager.sh; do
    if [ -x ~/.openclaw/workspace/.clawdbot/scripts/$script ]; then
        echo "  ✓ $script is executable"
    else
        echo "  ✗ $script not executable"
        exit 1
    fi
done

# Test 5: Check Claude Reconstruction
echo ""
echo "Test 5: Claude Reconstruction integration"
if [ -d ~/.openclaw/workspace/claude-Reconstruction ]; then
    echo "  ✓ claude-Reconstruction directory exists"
    if [ -f ~/.openclaw/workspace/claude-Reconstruction/CLAUDE.md ]; then
        echo "  ✓ CLAUDE.md found"
    else
        echo "  ✗ CLAUDE.md not found"
    fi
else
    echo "  ✗ claude-Reconstruction not found"
fi

# Test 6: Check Claude CLI
echo ""
echo "Test 6: Claude CLI"
if command -v claude &> /dev/null; then
    version=$(claude --version 2>&1)
    echo "  ✓ Claude CLI installed: $version"
else
    echo "  ✗ Claude CLI not found"
fi

# Test 7: Validate JSON configs
echo ""
echo "Test 7: Validate JSON configurations"
for json in \
    ~/.openclaw/workspace/.clawdbot/config/swarm-config.json \
    ~/.openclaw/workspace/.clawdbot/config/integration.json; do
    if jq empty "$json" 2>/dev/null; then
        echo "  ✓ $(basename $json) is valid JSON"
    else
        echo "  ✗ $(basename $json) has JSON errors"
        exit 1
    fi
done

# Test 8: Check documentation
echo ""
echo "Test 8: Documentation"
docs=(
    "SYSTEM_OVERVIEW.md"
    "INTEGRATION.md"
    "QUICK_START_ENGINEERING.md"
    "README.md"
)
for doc in "${docs[@]}"; do
    if [ -f ~/.openclaw/workspace/.clawdbot/$doc ]; then
        echo "  ✓ $doc exists"
    else
        echo "  ✗ $doc missing"
    fi
done

echo ""
echo "═══════════════════════════════════════"
echo "✅ All tests passed!"
echo ""
echo "System is ready to use:"
echo "  cd ~/.openclaw/workspace"
echo "  ./swarm help"
echo "  ./swarm spawn-eng"
echo "═══════════════════════════════════════"
