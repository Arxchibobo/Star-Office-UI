#!/bin/bash
# 启动完整的办公室系统（后端 + 状态同步）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 启动 Bobo 的办公室系统..."
echo ""

# 激活虚拟环境
source venv/bin/activate

# 停止旧进程
echo "🛑 停止旧进程..."
pkill -f "app_telegram.py" 2>/dev/null
pkill -f "sync_openclaw_state.py" 2>/dev/null
sleep 2

# 启动后端服务
echo "🌐 启动办公室后端服务..."
nohup python backend/app_telegram.py > /tmp/star-office.log 2>&1 &
BACKEND_PID=$!
echo "   ✓ 后端已启动 (PID: $BACKEND_PID)"
echo "   📍 http://localhost:18793/"

# 等待后端启动
sleep 2

# 启动状态同步
echo "🔄 启动实时状态同步..."
nohup python sync_openclaw_state.py > /tmp/office-sync.log 2>&1 &
SYNC_PID=$!
echo "   ✓ 同步已启动 (PID: $SYNC_PID)"

echo ""
echo "════════════════════════════════════════════"
echo "✅ Bobo的办公室已启动！"
echo "════════════════════════════════════════════"
echo "📱 访问方式："
echo "   • 完整版: http://localhost:18793/"
echo "   • Telegram: http://localhost:18793/debug"
echo ""
echo "📊 状态："
echo "   • 后端服务: PID $BACKEND_PID"
echo "   • 状态同步: PID $SYNC_PID"
echo ""
echo "📝 日志："
echo "   • 后端: tail -f /tmp/star-office.log"
echo "   • 同步: tail -f /tmp/office-sync.log"
echo ""
echo "🛑 停止服务："
echo "   pkill -f 'app_telegram.py|sync_openclaw_state.py'"
echo "════════════════════════════════════════════"
