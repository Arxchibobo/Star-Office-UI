#!/bin/bash
# 启动配置好claude-Reconstruction的Claude Code

WORKSPACE=~/.openclaw/workspace
TASK_TYPE=${1:-coding}

echo "🚀 启动 Claude Code (集成 claude-Reconstruction v5.2)"
echo ""
echo "任务类型: $TASK_TYPE"
echo "工作目录: $WORKSPACE"
echo ""

cd $WORKSPACE

# 根据任务类型设置上下文
case $TASK_TYPE in
  api)
    echo "📡 加载 API 开发规则..."
    CONTEXT="API开发任务，加载规则: api设计、安全、测试"
    ;;
  frontend)
    echo "🎨 加载前端开发规则..."
    CONTEXT="前端开发任务，加载规则: UI规范、性能、响应式"
    ;;
  testing)
    echo "🧪 加载测试开发规则..."
    CONTEXT="测试开发任务，加载规则: 测试策略、覆盖率、E2E"
    ;;
  security)
    echo "🔒 加载安全开发规则..."
    CONTEXT="安全功能任务，加载规则: 安全审查、加密、认证"
    ;;
  *)
    echo "💻 加载通用编码规则..."
    CONTEXT="通用编码任务，加载规则: 代码规范、Git、重构"
    ;;
esac

echo ""
echo "提示: Claude Code将按照claude-Reconstruction的4步工作模式运行："
echo "  1️⃣ 规划 → 2️⃣ 确认 → 3️⃣ 执行到底 → 4️⃣ 验收"
echo ""
echo "════════════════════════════════════════════════════"
echo ""

# 启动Claude Code，传递配置和上下文
claude --config .claude/config.json --message "$CONTEXT"
