# 🤖 Agent Swarm System

OpenClaw + Codex/Claude Code Agent Orchestration System

基于 [Elvis Sun 的文章](https://x.com/elvissun/status/2025920521871716562) 实现的完整 Agent Swarm 原型。

## 🎯 核心特性

### ✅ 已实现

- **双层 AI 架构** - 编排层（你/OpenClaw）+ 执行层（Codex/Claude agents）
- **Ralph Loop V2** - 失败时分析原因并重写 prompt，而非简单重试
- **Worktree 隔离** - 每个任务独立分支和工作区
- **Tmux 会话管理** - 可中途干预（mid-task redirection）
- **自动监控** - 每10分钟检查 tmux、PR、CI 状态
- **自动重试** - 失败最多重试3次，每次改进 prompt
- **任务注册系统** - JSON 格式跟踪所有任务状态
- **Code Review** - Gemini（免费）+ Codex 自动审查
- **Telegram 通知** - 任务完成/失败时通知
- **CLI 工具** - 完整的命令行界面

## 📁 目录结构

```
~/.openclaw/workspace/
├── swarm                          # 主入口脚本
├── .clawdbot/
│   ├── active-tasks.json          # 任务注册表
│   ├── config/
│   │   └── swarm-config.json      # 系统配置
│   ├── scripts/
│   │   ├── spawn-agent.sh         # 生成新 agent
│   │   ├── check-agents.sh        # 监控脚本（Ralph Loop V2）
│   │   ├── run-code-review.sh     # 自动化代码审查
│   │   └── task-manager.sh        # 任务管理工具
│   └── logs/
│       ├── <task-id>.log          # 每个任务的日志
│       ├── monitor.log            # 监控日志
│       └── code-review.log        # 审查日志
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# GitHub CLI（必需）
# Ubuntu/Debian
sudo apt install gh

# 或从官网安装: https://cli.github.com/

# jq（JSON 处理，必需）
sudo apt install jq

# tmux（必需）
sudo apt install tmux

# Codex/Claude Code（根据需要安装）
npm install -g @openai/codex-cli
npm install -g @anthropic/claude-cli
```

### 2. 配置 GitHub CLI

```bash
gh auth login
```

### 3. 安装监控 cron job

```bash
cd ~/.openclaw/workspace
./swarm install-cron
```

这会每10分钟自动检查所有 agent 的状态。

### 4. 生成第一个 Agent

```bash
./swarm spawn
```

按提示输入：
- Task ID: `feat-billing`
- Agent type: `codex`
- Description: `Add billing feature for customers`
- Prompt: （按 Ctrl+D 结束输入）

## 📖 使用指南

### 基础命令

```bash
# 查看所有任务
./swarm status

# 查看任务日志
./swarm logs feat-billing

# 连接到 agent 的 tmux 会话（观察实时进度）
./swarm attach feat-billing

# 中途干预（mid-task redirection）
./swarm steer feat-billing "Stop. Focus on API layer first, not UI."

# 手动触发监控检查
./swarm check

# 杀死任务
./swarm kill feat-billing

# 清理已完成的任务
./swarm cleanup
```

### 高级用法

#### Mid-Task Steering（中途干预）

Agent 走错方向？不要杀掉它，重定向：

```bash
# Agent 看的文件太多
./swarm steer feat-billing "Focus only on src/api/billing.ts and its test"

# Agent 理解错需求
./swarm steer feat-billing "Customer wants X, not Y. Re-read the requirements."

# Agent 需要更多上下文
./swarm steer feat-billing "The schema is in src/types/billing.ts. Use that."
```

#### 批量生成 Agents

```bash
# 从文件批量生成
for task in $(cat tasks.txt); do
    ./swarm spawn <<EOF
$task
codex
Implement feature: $task
<详细 prompt>
EOF
done
```

## ⚙️ 配置

编辑 `.clawdbot/config/swarm-config.json`：

```json
{
  "system": {
    "maxConcurrentAgents": 3,     // 最多并行 agent 数
    "maxRetries": 3,               // 失败最大重试次数
    "checkIntervalMinutes": 10     // 监控间隔
  },
  "agents": {
    "codex": {
      "model": "gpt-5.1-codex",
      "reasoning": "high",
      "useCases": ["backend", "complex_bug"]
    }
  },
  "definitionOfDone": {
    "prCreated": true,
    "ciPassed": true,
    "codeReviewPassed": true
  }
}
```

## 🔄 工作流程

### 1. 生成 Agent

```bash
./swarm spawn
```

系统会：
- 创建独立的 git worktree
- 启动 tmux 会话
- 运行 Codex/Claude agent
- 注册任务到 `active-tasks.json`

### 2. 自动监控（每10分钟）

Cron job 运行 `check-agents.sh`，检查：

```
✓ Tmux 会话存活？
✓ PR 是否创建？
✓ CI 是否通过？
✓ Code review 是否通过？
```

### 3. 失败自动重试（Ralph Loop V2）

如果 agent 失败：

1. **分析失败原因**
   - CI 失败？
   - 上下文太多？
   - 方向错误？

2. **生成改进的 prompt**
   - 根据失败原因添加具体指导
   - 包含错误日志分析
   - 缩小范围或提供更多上下文

3. **重启 agent**（最多3次）

### 4. Code Review

CI 通过后，自动运行：

- **Gemini Code Assist**（免费！）- 发现安全问题、可扩展性问题
- **Codex Reviewer** - 逻辑错误、边界情况

### 5. 完成通知

所有检查通过后，Telegram 通知：

```
✅ Task completed: Add billing feature
PR #341 is ready for review!
```

## 🎓 核心概念

### 双层架构

```
┌────────────────────────────────────┐
│  编排层 (Orchestrator)            │
│  • 业务上下文                      │
│  • 生成 prompt                    │
│  • 监控进度                        │
│  • 主动发现任务                    │
└──────────┬─────────────────────────┘
           │ 精准 prompt
           ▼
┌────────────────────────────────────┐
│  执行层 (Agents)                  │
│  • 只关注代码                      │
│  • 独立环境                        │
│  • 自动测试和 PR                   │
└────────────────────────────────────┘
```

### Ralph Loop V2

传统方式：失败 → 重复相同 prompt
**V2 方式**：失败 → 分析原因 → **重写 prompt**

### Definition of Done

PR 创建 ≠ 完成

真正的"完成"：
- ✅ PR created
- ✅ Branch synced
- ✅ CI passed
- ✅ Code review passed
- ✅ Screenshots included (if UI)

## 🧪 测试示例

### 简单测试

```bash
# 1. 生成一个简单的 agent
./swarm spawn <<EOF
test-hello
codex
Test agent
Create a hello.js file that prints "Hello, Agent Swarm!"
EOF

# 2. 查看状态
./swarm status

# 3. 查看日志
./swarm logs test-hello

# 4. 连接观察
./swarm attach test-hello
# (按 Ctrl+B 然后 D 退出)
```

### 测试 Mid-Task Steering

```bash
# 1. 生成 agent
./swarm spawn
# Task ID: test-steering
# Agent: codex
# Description: Test steering
# Prompt: Create multiple files

# 2. 等几秒后干预
./swarm steer test-steering "Stop. Only create one file: test.js"

# 3. 查看日志，应该能看到 agent 收到消息并调整
./swarm logs test-steering
```

## 🐛 故障排查

### Agent 没有启动

```bash
# 检查 tmux 会话
tmux ls

# 查看日志
./swarm logs <task-id>

# 手动连接
./swarm attach <task-id>
```

### Cron 没有运行

```bash
# 检查 cron 是否安装
crontab -l | grep check-agents

# 查看 cron 日志
tail -f ~/.openclaw/workspace/.clawdbot/logs/cron.log

# 手动运行测试
./swarm check
```

### PR 检查失败

```bash
# 确保 gh CLI 已认证
gh auth status

# 测试 gh 命令
gh pr list
```

## 📊 监控和观察

### 实时监控

```bash
# 方法 1: 连接到 agent 的 tmux 会话
./swarm attach <task-id>

# 方法 2: tail 日志
tail -f ~/.openclaw/workspace/.clawdbot/logs/<task-id>.log

# 方法 3: 监控所有日志
tail -f ~/.openclaw/workspace/.clawdbot/logs/*.log
```

### 任务状态

```bash
# 查看所有任务
./swarm status

# 查看特定任务详情
~/.openclaw/workspace/.clawdbot/scripts/task-manager.sh view <task-id>
```

## 🚀 下一步

### Phase 1（已完成）
- ✅ 基础架构
- ✅ 监控系统
- ✅ 自动重试
- ✅ Code review

### Phase 2（下一步）
- [ ] OpenClaw 集成（通过 OpenClaw API 生成 agents）
- [ ] 主动任务发现（扫描 Sentry、会议笔记）
- [ ] 更智能的 prompt 改进（使用 LLM 分析失败）
- [ ] UI Dashboard（Web 界面）

### Phase 3（未来）
- [ ] 多仓库支持
- [ ] 分布式 agents（云端运行）
- [ ] 自动 merge（高信心 PR）
- [ ] 学习系统（记忆成功模式）

## 💡 最佳实践

### 1. 好的 Prompt 结构

```
CONTEXT:
[业务背景、客户需求]

TASK:
[具体要做什么]

FILES:
[需要修改的文件路径]

CONSTRAINTS:
[不要做什么]

DEFINITION OF DONE:
[什么算完成]
```

### 2. Agent 选择策略

- **Codex**: 后端逻辑、复杂 bug、多文件重构
- **Claude Code**: 前端、快速迭代、git 操作
- **Gemini**: UI 设计（然后 Claude 实现）

### 3. 何时干预

- Agent 看太多文件 → "Focus on these 3 files only"
- Agent 方向错误 → "Stop. Customer wants X, not Y"
- Agent 卡住 → 提供具体的文件路径或代码示例

### 4. 监控技巧

```bash
# 一次性查看所有运行中的 agent
watch -n 5 './swarm status'

# 实时监控日志
tmux new-session -d -s monitor 'tail -f ~/.openclaw/workspace/.clawdbot/logs/*.log'
tmux attach -t monitor
```

## 📚 资源

- 原文: https://x.com/elvissun/status/2025920521871716562
- OpenClaw Docs: https://docs.openclaw.ai
- GitHub CLI: https://cli.github.com/

## 🤝 贡献

这是一个原型系统，欢迎改进！

常见改进方向：
- 更好的错误处理
- 更智能的 prompt 生成
- 支持更多 agent 类型
- 更丰富的监控指标

---

**Made with 🦁 by OpenClaw + 小波比**
