# Telegram Agent Swarm 集成指南

将 Agent Swarm 系统与 Telegram 深度集成，实现实时交互和管理。

## 🎯 核心概念

### 双 Bot 架构

```
主控制 Bot (@openclaw_control_bot)
    ├─ 创建和管理所有 agents
    ├─ 查看状态和日志
    └─ 发送全局命令

Agent Bots（每个任务一个）
    ├─ @agent_feat_auth_bot
    ├─ @agent_test_api_bot
    └─ @agent_fix_bug_bot
        ├─ 实时报告进度
        ├─ 接受 steering 指令
        └─ 等待 Plan 确认
```

### 工作流程

```
你 → 主控制 Bot: "/spawn feat-auth security 实现JWT认证"
    ↓
主控制 Bot: "✅ 创建 Agent Bot: @agent_feat_auth_bot"
    ↓
Agent Bot 自动加入你的对话列表
    ↓
Agent Bot: "📋 [Plan] 我的实现计划：
           1. 创建 JWT utilities
           2. 添加 auth middleware
           3. 实现 login/logout 路由
           确认？"
    ↓
你 → Agent Bot: "确认"
    ↓
Agent Bot: "⚙️ [Execute] 正在实现...
           ✓ 创建 src/auth/jwt.ts
           ✓ 添加测试
           ✓ 运行测试（覆盖率 92%）"
    ↓
Agent Bot: "✅ [Done] 
           PR #123 已创建并通过所有检查
           https://github.com/your/repo/pull/123"
    ↓
你审查并合并 PR
```

## 🚀 快速开始

### 1. 创建主控制 Bot

1. **与 @BotFather 对话**
   ```
   /newbot
   名称: OpenClaw Control
   用户名: openclaw_control_bot（或你的自定义名称）
   ```

2. **复制 Token**
   ```
   Your bot token: 123456:ABC-DEF...
   ```

3. **配置到系统**
   ```bash
   cd ~/.openclaw/workspace/.clawdbot/scripts
   ./telegram-agent-manager.sh init
   
   # 编辑配置
   nano ../config/telegram-agents.json
   ```

4. **填入 Token**
   ```json
   {
     "mainBot": {
       "enabled": true,
       "token": "YOUR_BOT_TOKEN_HERE",
       "chatId": "",
       "description": "Main control bot"
     },
     ...
   }
   ```

5. **获取你的 Chat ID**
   ```bash
   # 启动 bot
   python3 telegram-main-bot.py
   
   # 在 Telegram 中向 bot 发送 /start
   # 控制台会显示你的 chat_id
   # 复制并填入配置中的 chatId
   ```

### 2. 启动主控制 Bot

```bash
cd ~/.openclaw/workspace/.clawdbot/scripts

# 前台运行（测试）
python3 telegram-main-bot.py

# 后台运行（生产）
nohup python3 telegram-main-bot.py > ../logs/main-bot.log 2>&1 &

# 查看日志
tail -f ../logs/main-bot.log
```

### 3. 创建第一个 Agent

在 Telegram 中向主控制 Bot 发送：

```
/spawn feat-hello api 创建Hello World API endpoint
```

主控制 Bot 会引导你：
1. 创建 Agent Bot（通过 @BotFather）
2. 配置 Token
3. 启动 Agent Bot 监听器
4. 开始任务

## 📱 主控制 Bot 命令

### 任务管理

```bash
# 创建普通 agent
/spawn <task-id> <agent-type> <description>
# 示例：/spawn feat-auth codex "实现用户认证"

# 创建工程化 agent（推荐）
/spawn-eng <task-id> <task-type> <description>
# 示例：/spawn-eng feat-auth security "实现JWT认证"

# 查看所有任务状态
/status

# 列出运行中的任务
/list

# 查看任务日志
/logs <task-id>
# 示例：/logs feat-auth

# 杀死任务
/kill <task-id>

# 清理完成的任务
/cleanup
```

### Agent 类型

| 类型 | 适用场景 | 特点 |
|------|---------|------|
| `codex` | 后端逻辑、复杂 bug | 推理能力强，适合复杂任务 |
| `claude` | 前端开发、快速迭代 | 速度快，适合迭代 |
| `gemini` | UI 设计、文档 | 擅长设计，免费 |

### 任务类型（工程化）

| 类型 | 自动加载规则 | 适用场景 |
|------|-------------|---------|
| `api` | coding + api-design | REST API, GraphQL |
| `frontend` | coding + frontend-frameworks | React/Vue 组件 |
| `testing` | testing + browser-automation | 单元测试、E2E |
| `security` | security + coding | 认证、授权 |
| `database` | coding + data-modeling | 迁移、查询 |

## 🤖 Agent Bot 交互

### 自动功能

Agent Bot 会自动：

1. **报告进度**
   ```
   📋 [Plan] 我的实现计划是...
   ⚙️ [Execute] 正在实现...
   ✓ 创建文件 src/auth/jwt.ts
   ✓ 运行测试（92% 覆盖率）
   ✅ [Done] PR #123 已创建
   ```

2. **等待确认**
   ```
   Plan 阶段会等待你确认：
   "确认方案？回复 '确认' 或 'yes'"
   ```

3. **接受 Steering**
   ```
   你可以随时发送指导消息：
   "先实现 API 层，UI 稍后做"
   ```

### 手动命令

```bash
# 查看任务状态
/status

# 发送 steering 指令
/steer <message>
# 或直接发送文本（自动作为 steering）

# 确认 Plan
"确认" / "confirm" / "yes" / "OK"
```

## ⚙️ 配置

### 配置文件

`.clawdbot/config/telegram-agents.json`:

```json
{
  "mainBot": {
    "enabled": true,
    "token": "YOUR_MAIN_BOT_TOKEN",
    "chatId": "YOUR_CHAT_ID",
    "description": "Main control bot for managing all agents"
  },
  "agentBots": {
    "feat-auth": {
      "taskId": "feat-auth",
      "token": "AGENT_BOT_TOKEN",
      "username": "agent_feat_auth_bot",
      "description": "User authentication feature",
      "createdAt": 1234567890,
      "status": "active",
      "pid": 12345
    }
  },
  "autoCreateBots": false,
  "useTopics": true
}
```

### 环境变量（可选）

```bash
# 添加到 ~/.bashrc
export OPENCLAW_TG_MAIN_BOT="YOUR_MAIN_BOT_TOKEN"
export OPENCLAW_TG_CHAT_ID="YOUR_CHAT_ID"
```

## 🔧 高级功能

### 1. Topics 模式（推荐）

使用 Telegram Topics 功能，一个 bot 管理多个任务：

```json
{
  "useTopics": true
}
```

优点：
- 只需要一个 agent bot
- 每个任务一个 topic
- 清晰的任务隔离

缺点：
- 需要超级群组
- 需要手动创建 topics

### 2. 自动创建 Bots（实验性）

```json
{
  "autoCreateBots": true,
  "botFatherToken": "SPECIAL_TOKEN"
}
```

注意：需要特殊的 BotFather API 访问权限（一般用户无法使用）。

### 3. 通知钩子

Agent 完成时自动发送富文本通知：

```python
# 在 agent 完成时调用
def notify_completion(task_id, pr_number):
    bot.send_message(
        chat_id,
        f"✅ **任务完成**\n\n"
        f"Task: `{task_id}`\n"
        f"PR: #{pr_number}\n"
        f"Status: All checks passed ✓\n\n"
        f"[View PR](https://github.com/your/repo/pull/{pr_number})",
        parse_mode="Markdown"
    )
```

### 4. 群组管理

将 Agent Bots 加入团队群组：

1. 创建 Telegram 群组
2. 将主控制 Bot 加入群组
3. 将 Agent Bots 加入群组
4. 团队成员可以查看所有 agent 进度

## 🔄 集成到现有 Swarm

### 修改 spawn-agent.sh

在 `spawn-agent.sh` 末尾添加：

```bash
# 6. 创建 Telegram Agent Bot（可选）
echo "Step 6: Creating Telegram bot..."
if [ -f "$SCRIPT_DIR/telegram-agent-manager.sh" ]; then
    "$SCRIPT_DIR/telegram-agent-manager.sh" create "$TASK_ID" "$DESCRIPTION" || {
        echo "Telegram bot creation skipped"
    }
    
    "$SCRIPT_DIR/telegram-agent-manager.sh" start "$TASK_ID" || {
        echo "Telegram bot listener not started"
    }
fi
```

### 修改 check-agents.sh

在监控脚本中添加 Telegram 通知：

```bash
# 发送 Telegram 通知
notify_telegram() {
    local message="$1"
    local task_id="$2"
    
    # 通过 agent bot 发送
    python3 "$SCRIPT_DIR/telegram-notify.py" "$task_id" "$message"
}

# 在任务完成时调用
if [ "$status" = "done" ]; then
    notify_telegram "✅ Task completed! PR #$pr_number ready" "$task_id"
fi
```

## 📊 监控和日志

### 查看日志

```bash
# 主控制 bot 日志
tail -f ~/.openclaw/workspace/.clawdbot/logs/main-bot.log

# Agent bot 日志
tail -f ~/.openclaw/workspace/.clawdbot/logs/bot-<task-id>.log

# 所有 bot 日志
tail -f ~/.openclaw/workspace/.clawdbot/logs/bot-*.log
```

### 调试

```bash
# 测试 Telegram API
curl -X POST https://api.telegram.org/bot<TOKEN>/getMe

# 测试发送消息
curl -X POST https://api.telegram.org/bot<TOKEN>/sendMessage \
  -H "Content-Type: application/json" \
  -d '{"chat_id":"YOUR_CHAT_ID","text":"Test"}'

# 检查 bot 配置
cat ~/.openclaw/workspace/.clawdbot/config/telegram-agents.json | jq
```

## 🐛 故障排查

### Bot 不响应

1. **检查 token**
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getMe
   ```

2. **检查日志**
   ```bash
   tail -f ~/.openclaw/workspace/.clawdbot/logs/main-bot.log
   ```

3. **重启 bot**
   ```bash
   pkill -f telegram-main-bot.py
   python3 ~/.openclaw/workspace/.clawdbot/scripts/telegram-main-bot.py &
   ```

### Agent Bot 未创建

1. **检查配置**
   ```bash
   cat ~/.openclaw/workspace/.clawdbot/config/telegram-agents.json
   ```

2. **手动创建**
   ```bash
   cd ~/.openclaw/workspace/.clawdbot/scripts
   ./telegram-agent-manager.sh create <task-id> "description"
   ```

### 消息延迟

1. **检查网络**
   ```bash
   ping api.telegram.org
   ```

2. **减少轮询间隔**
   ```python
   # 在 bot 代码中
   time.sleep(0.5)  # 改为 0.1
   ```

## 🎯 最佳实践

### 1. 命名规范

```
任务 ID: feat-<feature>、fix-<bug>、test-<test>
Bot 用户名: agent_<task-id>_bot
```

### 2. 安全性

- ✅ 不要在公开仓库提交 bot tokens
- ✅ 使用环境变量或加密配置
- ✅ 定期更新 tokens
- ✅ 只与信任的用户分享 bot

### 3. 性能

- ✅ 使用 webhook 而非长轮询（生产环境）
- ✅ 限制并发 agent 数量
- ✅ 定期清理完成的 agent bots

### 4. 用户体验

- ✅ 提供清晰的命令帮助
- ✅ 使用富文本格式（Markdown）
- ✅ 及时反馈操作结果
- ✅ 错误时给出解决建议

## 📚 相关文档

- [Agent Swarm 系统总览](SYSTEM_OVERVIEW.md)
- [快速开始指南](QUICK_START_ENGINEERING.md)
- [Telegram Bot API 文档](https://core.telegram.org/bots/api)

## 🔗 示例和模板

### 完整启动脚本

```bash
#!/bin/bash
# start-telegram-swarm.sh - 启动完整的 Telegram Agent Swarm

cd ~/.openclaw/workspace/.clawdbot/scripts

# 1. 启动主控制 Bot
echo "Starting main control bot..."
nohup python3 telegram-main-bot.py > ../logs/main-bot.log 2>&1 &
MAIN_PID=$!
echo "Main bot started (PID: $MAIN_PID)"

# 2. 启动所有 agent bots
echo "Starting agent bots..."
./telegram-agent-manager.sh list | grep active | while read task_id _; do
    ./telegram-agent-manager.sh start "$task_id"
done

echo "✓ All bots started!"
echo ""
echo "Check logs:"
echo "  tail -f ../logs/main-bot.log"
echo "  tail -f ../logs/bot-*.log"
```

### 停止脚本

```bash
#!/bin/bash
# stop-telegram-swarm.sh - 停止所有 Telegram bots

# 停止主控制 bot
pkill -f telegram-main-bot.py

# 停止所有 agent bots
pkill -f ".bot-.*.py"

echo "✓ All bots stopped"
```

---

**🎉 享受通过 Telegram 控制你的 Agent Swarm！**
