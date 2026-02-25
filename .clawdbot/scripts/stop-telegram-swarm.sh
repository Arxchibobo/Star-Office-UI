#!/bin/bash
# stop-telegram-swarm.sh - 停止所有 Telegram bots

echo "🛑 Stopping Telegram Agent Swarm..."
echo ""

# 1. 停止主控制 bot
if pgrep -f "telegram-main-bot.py" > /dev/null; then
    echo "Stopping main control bot..."
    pkill -f telegram-main-bot.py
    echo "✓ Main bot stopped"
else
    echo "Main bot not running"
fi

# 2. 停止所有 agent bots
echo ""
echo "Stopping agent bots..."
if pgrep -f ".bot-.*.py" > /dev/null; then
    pkill -f ".bot-.*.py"
    echo "✓ Agent bots stopped"
else
    echo "No agent bots running"
fi

echo ""
echo "═══════════════════════════════════════"
echo "✅ All bots stopped"
echo "═══════════════════════════════════════"
