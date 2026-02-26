#!/bin/bash
# Star Office UI 一键部署脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
VENV_DIR="$SCRIPT_DIR/venv"

echo "============================================"
echo "🏢 Star Office UI - 一键部署"
echo "============================================"

# 1. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装"
    exit 1
fi

echo "✅ Python3: $(python3 --version)"

# 2. 创建虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# 3. 安装依赖
echo "📦 安装依赖..."
pip install -q --upgrade pip
pip install -q flask flask-cors requests playwright

# 4. 安装 Playwright 浏览器（用于截图）
echo "🌐 安装 Playwright Chromium..."
playwright install chromium

# 5. 创建 state.json（如果不存在）
STATE_FILE="$SCRIPT_DIR/state.json"
if [ ! -f "$STATE_FILE" ]; then
    echo "📝 创建默认状态文件..."
    cat > "$STATE_FILE" <<EOF
{
  "state": "idle",
  "detail": "等待任务中...",
  "progress": 0,
  "updated_at": "$(date -Iseconds)"
}
EOF
fi

# 6. 创建启动脚本
START_SCRIPT="$SCRIPT_DIR/start.sh"
cat > "$START_SCRIPT" <<'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
cd "$SCRIPT_DIR/backend"
python app_telegram.py
EOF
chmod +x "$START_SCRIPT"

# 7. 创建状态同步启动脚本
SYNC_SCRIPT="$SCRIPT_DIR/start_sync.sh"
cat > "$SYNC_SCRIPT" <<'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
cd "$SCRIPT_DIR"
python sync_agent_state.py --watch 5
EOF
chmod +x "$SYNC_SCRIPT"

# 8. 创建截图脚本
SCREENSHOT_SCRIPT="$SCRIPT_DIR/screenshot.sh"
cat > "$SCREENSHOT_SCRIPT" <<'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
cd "$SCRIPT_DIR"
python screenshot_to_telegram.py
EOF
chmod +x "$SCREENSHOT_SCRIPT"

echo ""
echo "✅ 部署完成！"
echo ""
echo "📋 使用方法："
echo ""
echo "1️⃣ 启动后端服务:"
echo "   $START_SCRIPT"
echo ""
echo "2️⃣ 启动状态同步 (可选):"
echo "   $SYNC_SCRIPT"
echo ""
echo "3️⃣ 手动截图推送 (可选):"
echo "   $SCREENSHOT_SCRIPT"
echo ""
echo "4️⃣ 使用 Cloudflare Tunnel 暴露到公网:"
echo "   cloudflared tunnel --url http://localhost:18791"
echo ""
echo "5️⃣ 配置 Telegram WebApp 按钮 (见 STAR_OFFICE_INTEGRATION.md)"
echo ""
echo "============================================"
