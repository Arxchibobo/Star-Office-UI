#!/bin/bash
# start-telegram-swarm.sh - 一键启动 Telegram Agent Swarm

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAWDBOT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🤖 Starting Telegram Agent Swarm..."
echo ""

# 1. 检查配置
if [ ! -f "$CLAWDBOT_ROOT/config/telegram-agents.json" ]; then
    echo "❌ Config not found!"
    echo ""
    echo "Initialize first:"
    echo "  $SCRIPT_DIR/telegram-agent-manager.sh init"
    echo "  nano $CLAWDBOT_ROOT/config/telegram-agents.json"
    exit 1
fi

# 2. 检查主 bot token
MAIN_TOKEN=$(jq -r '.mainBot.token' "$CLAWDBOT_ROOT/config/telegram-agents.json")
if [ -z "$MAIN_TOKEN" ] || [ "$MAIN_TOKEN" = "null" ]; then
    echo "❌ Main bot token not configured!"
    echo ""
    echo "Steps:"
    echo "1. Create bot via @BotFather"
    echo "2. Edit config: nano $CLAWDBOT_ROOT/config/telegram-agents.json"
    echo "3. Add token to mainBot.token"
    exit 1
fi

# 3. 启动主控制 Bot
echo "Starting main control bot..."
cd "$SCRIPT_DIR"

# 检查是否已运行
if pgrep -f "telegram-main-bot.py" > /dev/null; then
    echo "⚠️  Main bot already running"
    read -p "Restart? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill -f telegram-main-bot.py
        sleep 2
    else
        echo "Skipped"
    fi
fi

# 启动
if ! pgrep -f "telegram-main-bot.py" > /dev/null; then
    nohup python3 telegram-main-bot.py > "$CLAWDBOT_ROOT/logs/main-bot.log" 2>&1 &
    MAIN_PID=$!
    echo "✓ Main bot started (PID: $MAIN_PID)"
else
    MAIN_PID=$(pgrep -f telegram-main-bot.py)
    echo "✓ Main bot running (PID: $MAIN_PID)"
fi

# 4. 启动 agent bots
echo ""
echo "Checking agent bots..."

ACTIVE_TASKS=$(jq -r '.agentBots | to_entries[] | select(.value.status == "active") | .key' "$CLAWDBOT_ROOT/config/telegram-agents.json")

if [ -z "$ACTIVE_TASKS" ]; then
    echo "No active agent bots to start"
else
    while read -r task_id; do
        if [ -n "$task_id" ]; then
            echo "Starting agent bot: $task_id"
            "$SCRIPT_DIR/telegram-agent-manager.sh" start "$task_id" || echo "  Failed to start"
        fi
    done <<< "$ACTIVE_TASKS"
fi

# 5. 显示状态
echo ""
echo "═══════════════════════════════════════"
echo "✅ Telegram Agent Swarm Started!"
echo ""
echo "Main Bot:"
echo "  PID: $MAIN_PID"
echo "  Log: tail -f $CLAWDBOT_ROOT/logs/main-bot.log"
echo ""
echo "Send /start to your bot to begin"
echo ""
echo "Commands:"
echo "  Stop all: $SCRIPT_DIR/stop-telegram-swarm.sh"
echo "  Status: $SCRIPT_DIR/telegram-agent-manager.sh list"
echo "═══════════════════════════════════════"
