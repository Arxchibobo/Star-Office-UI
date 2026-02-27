#!/bin/bash
# Telegram WebApp 公网访问配置脚本
# 用于重启cloudflare tunnel并更新bot配置

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 配置 Telegram WebApp 公网访问"
echo "════════════════════════════════════════════"
echo ""

# 停止旧的tunnel
echo "🛑 停止旧的tunnel..."
pkill -f cloudflared 2>/dev/null
sleep 2

# 启动新的tunnel
echo "🌐 启动新的cloudflare tunnel..."
nohup cloudflared tunnel --url http://localhost:18793 > /tmp/cloudflared.log 2>&1 &
TUNNEL_PID=$!
echo "   ✓ Tunnel已启动 (PID: $TUNNEL_PID)"
echo ""

# 等待tunnel就绪
echo "⏳ 等待tunnel就绪..."
sleep 8

# 获取公网URL
TUNNEL_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cloudflared.log | head -1)

if [ -z "$TUNNEL_URL" ]; then
    echo "❌ 错误：无法获取tunnel URL"
    echo "请查看日志：tail -f /tmp/cloudflared.log"
    exit 1
fi

echo "✅ Tunnel URL: $TUNNEL_URL"
echo ""

# 更新配置文件
echo "📝 更新配置文件..."
sed -i "s|WEBAPP_URL = \"https://[^\"]*\"|WEBAPP_URL = \"$TUNNEL_URL\"|" setup_telegram_webapp.py
sed -i "s|\"url\": \"https://[^\"]*\"|\"url\": \"$TUNNEL_URL\"|" office-config.json
echo "   ✓ setup_telegram_webapp.py"
echo "   ✓ office-config.json"
echo ""

# 配置Bot
echo "🤖 配置Telegram Bot..."
source venv/bin/activate
python setup_telegram_webapp.py
echo ""

echo "════════════════════════════════════════════"
echo "✅ 配置完成！"
echo "════════════════════════════════════════════"
echo ""
echo "📱 使用方法："
echo "  1. 打开Telegram bot对话"
echo "  2. 点击菜单按钮（☰）→ 🏢 查看办公室"
echo "  3. 或点击我发送的消息中的按钮"
echo ""
echo "🔗 公网URL: $TUNNEL_URL"
echo "📊 Tunnel PID: $TUNNEL_PID"
echo "📝 日志: tail -f /tmp/cloudflared.log"
echo ""
echo "🛑 停止tunnel: kill $TUNNEL_PID"
echo "════════════════════════════════════════════"
