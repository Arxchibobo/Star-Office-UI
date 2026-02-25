#!/bin/bash
# start-image-bot.sh - 启动图片生成Bot

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAWDBOT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🎨 Starting Image Generation Bot..."
echo ""

# 检查配置
if [ ! -f "$CLAWDBOT_ROOT/config/image-bot.json" ]; then
    echo "❌ Config not found!"
    exit 1
fi

# 检查token
TOKEN=$(jq -r '.token' "$CLAWDBOT_ROOT/config/image-bot.json")
if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ] || [ "$TOKEN" = "YOUR_BOT_TOKEN_HERE" ]; then
    echo "❌ Bot token not configured!"
    echo ""
    echo "Steps:"
    echo "1. Create bot via @BotFather"
    echo "2. Edit config: nano $CLAWDBOT_ROOT/config/image-bot.json"
    echo "3. Add token"
    exit 1
fi

cd "$SCRIPT_DIR"

# 检查是否已运行
if pgrep -f "image-bot.py" > /dev/null; then
    echo "⚠️  Bot already running"
    read -p "Restart? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill -f image-bot.py
        sleep 2
    else
        exit 0
    fi
fi

# 启动
if ! pgrep -f "image-bot.py" > /dev/null; then
    nohup bash -c "source ~/.bashrc && \"$CLAWDBOT_ROOT/venv/bin/python\" -u \"$SCRIPT_DIR/image-bot.py\"" > "$CLAWDBOT_ROOT/logs/image-bot.log" 2>&1 &
    PID=$!
    echo "✓ Image Bot started (PID: $PID)"
else
    PID=$(pgrep -f image-bot.py)
    echo "✓ Image Bot running (PID: $PID)"
fi

echo ""
echo "═══════════════════════════════════════"
echo "✅ Image Generation Bot Started!"
echo ""
echo "Log: tail -f $CLAWDBOT_ROOT/logs/image-bot.log"
echo "Stop: $SCRIPT_DIR/stop-image-bot.sh"
echo "═══════════════════════════════════════"
