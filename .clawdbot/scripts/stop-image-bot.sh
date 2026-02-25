#!/bin/bash
# stop-image-bot.sh - 停止图片生成Bot

echo "🛑 Stopping Image Generation Bot..."
echo ""

if pgrep -f "image-bot.py" > /dev/null; then
    pkill -f image-bot.py
    echo "✓ Image Bot stopped"
else
    echo "Image Bot not running"
fi

echo ""
echo "═══════════════════════════════════════"
echo "✅ Image Bot stopped"
echo "═══════════════════════════════════════"
