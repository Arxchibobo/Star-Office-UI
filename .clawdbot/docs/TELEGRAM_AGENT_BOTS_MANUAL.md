# Telegram Agent Bots 手动配置指南

## 📖 概述

本指南介绍如何手动创建和配置独立的 Telegram Agent Bots，用于与特定任务一对一交互。

### 为什么需要独立 Agent Bots？

**主控 Bot (@ArxchiboSwarm_bot)** 适合：
- 快速查看所有任务状态
- 批量管理多个 agents
- 简单命令操作

**独立 Agent Bots** 适合：
- 实时接收特定任务的进度更新
- 在移动端直接与 agent 对话
- 需要确认或steering时立即收到通知
- 大团队场景下隔离不同任务

---

## 🚀 快速开始

### 前提条件

- ✅ 已安装 Agent Swarm 系统
- ✅ Telegram 账号
- ✅ 可以访问 @BotFather

### 创建流程（5分钟）

1. **创建新Bot** → BotFather
2. **配置Bot** → telegram-agents.json
3. **启动监听** → telegram-agent-manager.sh
4. **测试交互** → 发送消息

---

## 📱 Step 1: 使用 BotFather 创建Bot

### 1.1 打开 Telegram，搜索 `@BotFather`

### 1.2 发送 `/newbot` 命令

```
You: /newbot

BotFather: Alright, a new bot. How are we going to call it? 
           Please choose a name for your bot.
```

### 1.3 输入Bot名称

```
You: MyTask Agent

BotFather: Good. Now let's choose a username for your bot. 
           It must end in `bot`. Like this, for example: 
           TetrisBot or tetris_bot.
```

### 1.4 输入Bot用户名（必须以bot结尾）

```
You: mytask_agent_bot

BotFather: Done! Congratulations on your new bot. 
           You will find it at t.me/mytask_agent_bot.
           
           Use this token to access the HTTP API:
           123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 1.5 **保存Token** 📝

**重要：** 复制并保存这个 token，稍后需要用到！

---

## ⚙️ Step 2: 配置 Agent Bot

### 2.1 打开配置文件

```bash
cd ~/.openclaw/workspace/.clawdbot/config
nano telegram-agents.json
```

### 2.2 添加Bot配置

找到 `"agentBots"` 部分，添加新Bot：

```json
{
  "mainBot": {
    "enabled": true,
    "token": "8222373172:AAHOIrA6ujqZiCN5Pv25vOaJIKIRzaA5ifY",
    "chatId": "7744442092",
    "authorizedChatIds": ["7744442092", "-1003731869348"],
    "authorizedUserIds": ["7744442092", "8573919212"],
    "description": "Main control bot for managing all agents"
  },
  "agentBots": {
    "my-task": {
      "enabled": true,
      "token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
      "username": "mytask_agent_bot",
      "taskId": "my-task",
      "chatId": "7744442092",
      "description": "Agent bot for my-task"
    }
  },
  "botFatherToken": "",
  "autoCreateBots": false,
  "useTopics": true
}
```

**字段说明：**
- `token` - BotFather 给你的 Token
- `username` - Bot 用户名
- `taskId` - 对应的任务ID（必须与 swarm spawn 时使用的ID一致）
- `chatId` - 你的 Telegram 用户ID
- `description` - Bot描述（可选）

### 2.3 保存并退出

按 `Ctrl+X`, 然后 `Y`, 然后 `Enter`

---

## 🎬 Step 3: 启动Agent Bot监听器

### 3.1 使用 telegram-agent-manager.sh

```bash
cd ~/.openclaw/workspace/.clawdbot/scripts

# 启动单个 agent bot
./telegram-agent-manager.sh start my-task

# 或者查看帮助
./telegram-agent-manager.sh help
```

### 3.2 验证启动成功

```bash
# 查看运行中的监听器
ps aux | grep "telegram-agent-bot"

# 查看日志
tail -f ~/.openclaw/workspace/.clawdbot/logs/telegram-agent-my-task.log
```

### 3.3 预期输出

```
✅ Agent Bot 'my-task' started (PID: 12345)
📱 Bot username: @mytask_agent_bot
🔗 Open Telegram and search for @mytask_agent_bot
```

---

## 💬 Step 4: 测试Agent Bot

### 4.1 打开 Telegram

搜索你的Bot用户名（例如 `@mytask_agent_bot`）

### 4.2 发送 `/start`

```
You: /start

Bot: 👋 Hello! I'm the agent for task 'my-task'.
     
     📊 Current status: idle
     📝 Task description: [task description]
     ⏱️ Started: 2026-02-27 10:00:00
```

### 4.3 实时接收更新

当Agent工作时，Bot会自动推送消息：

```
Bot: 📝 Status update:
     State: writing
     Progress: 45%
     Detail: Writing API endpoints...
```

### 4.4 与Agent交互

```
You: Show me the current files

Bot: 📂 Current files:
     - src/api/routes.py
     - src/models/user.py
     - tests/test_api.py
```

---

## 🔧 高级配置

### 批量启动所有Agent Bots

```bash
cd ~/.openclaw/workspace/.clawdbot/scripts

# 启动所有配置的 agent bots
for task_id in $(jq -r '.agentBots | keys[]' ../config/telegram-agents.json); do
  ./telegram-agent-manager.sh start "$task_id"
done
```

### 自动重启脚本

创建 `start-all-agent-bots.sh`:

```bash
#!/bin/bash

CONFIG_FILE="$HOME/.openclaw/workspace/.clawdbot/config/telegram-agents.json"
MANAGER_SCRIPT="$HOME/.openclaw/workspace/.clawdbot/scripts/telegram-agent-manager.sh"

echo "🚀 Starting all Agent Bots..."

jq -r '.agentBots | keys[]' "$CONFIG_FILE" | while read task_id; do
  echo "Starting bot for task: $task_id"
  "$MANAGER_SCRIPT" start "$task_id"
done

echo "✅ All Agent Bots started!"
```

使用：

```bash
chmod +x start-all-agent-bots.sh
./start-all-agent-bots.sh
```

### systemd 服务（Linux）

创建 `/etc/systemd/system/telegram-agent-bots.service`:

```ini
[Unit]
Description=Telegram Agent Bots
After=network.target

[Service]
Type=forking
User=arxchibo
WorkingDirectory=/home/arxchibo/.openclaw/workspace
ExecStart=/home/arxchibo/.openclaw/workspace/.clawdbot/scripts/start-all-agent-bots.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-agent-bots
sudo systemctl start telegram-agent-bots
```

---

## 🐛 故障排查

### 问题1: Bot不回复消息

**症状**: 发送消息后没有任何响应

**解决方案**:

1. 检查Bot监听器是否运行：
   ```bash
   ps aux | grep "telegram-agent-bot.*my-task"
   ```

2. 检查日志：
   ```bash
   tail -100 ~/.openclaw/workspace/.clawdbot/logs/telegram-agent-my-task.log
   ```

3. 验证Token：
   ```bash
   curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"
   ```

### 问题2: "Unauthorized" 错误

**原因**: Token错误或已失效

**解决方案**:

1. 在BotFather重新生成Token：
   ```
   /mybots → 选择你的bot → API Token
   ```

2. 更新 `telegram-agents.json` 中的token

3. 重启监听器：
   ```bash
   ./telegram-agent-manager.sh restart my-task
   ```

### 问题3: 收不到实时更新

**原因**: 状态同步脚本未运行

**解决方案**:

1. 检查Agent是否正在运行：
   ```bash
   ./swarm status
   ```

2. 确保任务ID匹配：
   - Bot配置中的 `taskId` 必须与 Agent 的任务ID完全一致

3. 检查Agent日志：
   ```bash
   ./swarm logs my-task
   ```

### 问题4: 多个Bot冲突

**症状**: 消息发送到错误的Bot

**解决方案**:

1. 确保每个Bot的 `taskId` 唯一

2. 停止所有Bot：
   ```bash
   pkill -f "telegram-agent-bot"
   ```

3. 逐个启动并测试：
   ```bash
   ./telegram-agent-manager.sh start task-1
   # 测试 task-1 bot
   ./telegram-agent-manager.sh start task-2
   # 测试 task-2 bot
   ```

---

## 📋 完整工作流示例

### 场景: 创建一个API开发任务的专属Bot

#### 1. 创建Agent任务

```bash
cd ~/.openclaw/workspace
./swarm spawn-eng

# 输入:
# Task ID: api-dev-2027
# Agent Type: codex
# Task Type: api
# Description: Build user authentication API with JWT
```

#### 2. 通过BotFather创建Bot

```
/newbot
Name: API Dev 2027 Agent
Username: api_dev_2027_bot
Token: 987654321:XYZabcDEFghiJKLmnoPQRstu
```

#### 3. 配置Bot

编辑 `telegram-agents.json`:

```json
"agentBots": {
  "api-dev-2027": {
    "enabled": true,
    "token": "987654321:XYZabcDEFghiJKLmnoPQRstu",
    "username": "api_dev_2027_bot",
    "taskId": "api-dev-2027",
    "chatId": "7744442092",
    "description": "API development agent"
  }
}
```

#### 4. 启动Bot监听

```bash
./telegram-agent-manager.sh start api-dev-2027
```

#### 5. 在Telegram中交互

```
You: /start
Bot: 👋 Hello! Monitoring task 'api-dev-2027'

[5分钟后]
Bot: 📝 Update: Planning authentication flow...
Bot: 📝 Update: Writing JWT middleware...
Bot: 📝 Update: Adding password hashing...

[30分钟后]
Bot: ✅ Task completed!
     Files created:
     - src/auth/jwt.py
     - src/auth/password.py
     - tests/test_auth.py
```

---

## 🎯 最佳实践

### 1. 命名规范

- **任务ID**: 使用短横线分隔，全小写
  - ✅ `api-auth`, `frontend-ui`, `bug-fix-123`
  - ❌ `API_Auth`, `Frontend UI`, `bug fix 123`

- **Bot Username**: 对应任务ID，添加`_bot`后缀
  - ✅ `api_auth_bot`, `frontend_ui_bot`
  - ❌ `my_cool_bot`, `agent_1`

### 2. 任务隔离

- 每个重要任务创建独立Bot
- 简单任务可以共用主控Bot
- 大型项目建议为每个模块创建独立Bot

### 3. 权限管理

只授权必要的用户：

```json
"chatId": "你的用户ID",
"authorizedUserIds": ["你的用户ID", "团队成员ID"]
```

### 4. 日志管理

定期清理旧日志：

```bash
# 清理30天前的日志
find ~/.openclaw/workspace/.clawdbot/logs -name "telegram-agent-*.log" -mtime +30 -delete
```

### 5. 安全建议

- ❌ **不要** 将Bot Token提交到Git
- ✅ 将 `telegram-agents.json` 添加到 `.gitignore`
- ✅ 定期轮换Token（每3-6个月）
- ✅ 只在私人对话中使用Agent Bots

---

## 🔗 相关文档

- [Agent Swarm 系统总览](../SYSTEM_OVERVIEW.md)
- [Telegram 集成指南](../TELEGRAM_INTEGRATION.md)
- [快速开始](../QUICK_START_ENGINEERING.md)

---

## 💡 需要帮助？

- **文档问题**: 查看 `.clawdbot/README.md`
- **技术问题**: 查看日志 `.clawdbot/logs/`
- **配置示例**: 参考 `telegram-agents.json`

---

**最后更新**: 2026-02-27  
**维护者**: Arxchibobo  
**状态**: 架构完成，可用于生产
