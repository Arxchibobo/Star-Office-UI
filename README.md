# 🤖 OpenClaw Agent Swarm System

<div align="center">

**一个完整的 AI Agent 编排系统，结合工程化配置，实现专业级代码生产**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/Arxchibobo/openclaw-arxchibo?style=social)](https://github.com/Arxchibobo/openclaw-arxchibo)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

[功能特性](#-功能特性) •
[快速开始](#-快速开始) •
[系统架构](#-系统架构) •
[文档](#-文档) •
[使用指南](#-使用指南)

</div>

---

## 📖 简介

**OpenClaw Agent Swarm** 是一个基于 [Elvis Sun 的 Agent Swarm 架构](https://x.com/elvissun/status/2025920521871716562) 和 [Claude Reconstruction 工程化系统](https://github.com/Arxchibobo/claude-Reconstruction) 的完整 AI Agent 编排系统。

### 为什么需要这个系统？

**传统 AI Coding Assistants 的问题：**
- ❌ 上下文使用率：60%+（大量浪费）
- ❌ 行为像 chatbot，频繁询问
- ❌ 代码质量不稳定
- ❌ 失败后无脑重试

**Agent Swarm 系统的优势：**
- ✅ 上下文使用率：12-20%（**3-5倍提升**）
- ✅ 行为像 senior engineer
- ✅ 一致的高质量代码
- ✅ 智能失败分析和 prompt 改进（Ralph Loop V2）
- ✅ 完整的 4 步工作流程（Plan-Confirm-Execute-Deliver）
- ✅ 5 层质量保证体系

---

## 🌟 功能特性

### 🎯 核心功能

#### 1. **双层 AI 架构**
```
编排层 (Orchestrator)
    ↓ 读取业务上下文，生成精准 prompt
执行层 (Agents)
    ↓ 专注代码实现，遵循工程化规则
```

#### 2. **Ralph Loop V2 - 智能重试系统**
```
失败 → 分析原因 → 重写 prompt → 重试
```
不是无脑重复，而是智能改进：
- 上下文太多？→ 缩小范围
- 方向错误？→ 重新对齐
- 缺少信息？→ 补充上下文

#### 3. **Context Manager - 智能上下文管理**
- 根据任务类型自动加载相关文档
- **上下文使用率从 60%+ 降到 12-20%**
- 释放 5 倍工作空间

#### 4. **4 步工作流程**
```
1. Plan     → 先思考再行动
2. Confirm  → 确认方案再实现
3. Execute  → 遵循规则实现
4. Deliver  → 高质量交付
```

#### 5. **5 层质量保证**
```
Layer 5: Context Manager   → 智能加载文档
Layer 4: Workflow Engine   → 强制工作流程
Layer 3: Rules Engine      → 编码规范
Layer 2: Hook Layer        → 质量门控
Layer 1: Delegation Layer  → 专家系统
```

---

### ⚙️ 主要特性

- 🔄 **自动监控** - 每 10 分钟检查 agent 状态
- 🎯 **Mid-Task Steering** - 中途干预引导方向
- 🤖 **多 Agent 并行** - 同时处理多个任务
- 📊 **自动 Code Review** - Gemini（免费）+ Codex
- 📱 **Telegram 集成** - 每个任务独立 bot，实时交互（NEW!）
- 🔔 **实时通知** - Plan 确认、进度更新、完成通知
- 📝 **完整文档** - 包含快速开始指南和最佳实践
- 🛠️ **CLI 工具** - 简单易用的命令行界面

---

## 📱 Telegram 集成（NEW!）

**通过 Telegram 实时控制和交互你的 Agent Swarm！**

### 双 Bot 架构

```
主控制 Bot (@openclaw_control_bot)
    ├─ 创建和管理所有 agents
    └─ 查看状态和日志

Agent Bots（每个任务一个）
    ├─ 实时报告进度
    ├─ 等待 Plan 确认
    └─ 接受 steering 指令
```

### 工作流程示例

```
你 → 主控制 Bot: "/spawn feat-auth security 实现JWT认证"
    ↓
Agent Bot: "📋 [Plan] 我的实现计划是..."
    ↓
你 → Agent Bot: "确认"
    ↓
Agent Bot: "⚙️ [Execute] 正在实现..."
    ↓
Agent Bot: "✅ [Done] PR #123 已创建"
```

**详细文档：** [Telegram 集成指南](.clawdbot/TELEGRAM_INTEGRATION.md)

---

## 🚀 快速开始

### 前置要求

```bash
# 必需
- Git
- Bash
- jq (JSON 处理)
- tmux
- GitHub CLI (gh)
- Claude CLI (v2.0.28+)

# 可选
- Codex CLI (如果使用 Codex agents)
```

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/Arxchibobo/openclaw-arxchibo.git
cd openclaw-arxchibo

# 2. 运行系统测试
./.clawdbot/test-system.sh

# 3. 检查集成状态
./swarm integration-status
```

### 5 分钟上手

```bash
# 查看帮助
./swarm help

# 生成你的第一个工程化 agent
./swarm spawn-eng
```

**输入示例：**
```
Task ID: test-hello-api
Task Type: api
Description: Create a simple Hello World API endpoint

Files to create: src/routes/hello.ts, tests/hello.test.ts
Files to modify: src/app.ts
```

Agent 会自动：
1. 📋 **Plan** - 创建实现计划
2. ✅ **Confirm** - 等待你确认
3. ⚙️ **Execute** - 按工程化规范实现
4. 🚀 **Deliver** - 创建高质量 PR

---

## 🏗️ 系统架构

### 整体架构（3 层）

```
┌─────────────────────────────────────────────────┐
│  你/OpenClaw (最高编排层)                        │
│  • 读取业务上下文                                │
│  • 决定任务优先级                                │
│  • 监督整体进度                                  │
└──────────────┬──────────────────────────────────┘
               │
               ▼ 生成 agents
┌─────────────────────────────────────────────────┐
│  Agent Swarm (编排层)                           │
│  • 生成 agents (worktree + tmux)               │
│  • 监控进度 (Ralph Loop V2)                    │
│  • 自动重试 (失败分析 + prompt 改进)            │
│  • Mid-task steering                           │
└──────────────┬──────────────────────────────────┘
               │ 使用工程化配置
               ▼
┌─────────────────────────────────────────────────┐
│  Claude Reconstruction (5 层工程化)             │
│  • Context Manager (智能加载)                   │
│  • Workflow Engine (强制流程)                   │
│  • Rules Engine (编码规范)                      │
│  • Hook Layer (质量门控)                        │
│  • Delegation Layer (专家系统)                  │
└──────────────┬──────────────────────────────────┘
               │
               ▼ 遵循规则
┌─────────────────────────────────────────────────┐
│  Codex/Claude Code Agents (执行层)              │
│  • 独立 worktree + tmux                         │
│  • 高质量代码产出                                │
└─────────────────────────────────────────────────┘
```

### 目录结构

```
openclaw-arxchibo/
├── swarm                           # 主 CLI 入口
├── .clawdbot/                      # Agent Swarm 系统
│   ├── README.md                   # 完整文档
│   ├── SYSTEM_OVERVIEW.md          # 系统总览
│   ├── INTEGRATION.md              # 集成指南
│   ├── QUICK_START_ENGINEERING.md  # 工程化快速开始
│   ├── PROMPT_TEMPLATES.md         # Prompt 模板库
│   ├── config/
│   │   ├── swarm-config.json       # Swarm 配置
│   │   └── integration.json        # 集成配置
│   ├── scripts/
│   │   ├── spawn-agent.sh          # Agent 生成器
│   │   ├── spawn-with-config.sh    # 工程化 Agent
│   │   ├── check-agents.sh         # 监控系统
│   │   ├── run-code-review.sh      # 代码审查
│   │   └── task-manager.sh         # 任务管理
│   └── templates/
│       └── engineering.md          # 工程化模板
│
├── claude-Reconstruction/          # 工程化配置
│   ├── CLAUDE.md                   # 主配置
│   ├── CONTEXT_MANAGER.md          # 上下文管理
│   ├── rules/                      # 规则引擎
│   ├── capabilities/               # 能力定义
│   └── index/                      # 索引和路由
│
├── MEMORY.md                       # 决策树和知识图谱
└── TOOLS.md                        # 工具配置
```

---

## 📚 文档

### 核心文档

| 文档 | 描述 |
|------|------|
| [SYSTEM_OVERVIEW.md](.clawdbot/SYSTEM_OVERVIEW.md) | 系统完整总览 |
| [INTEGRATION.md](.clawdbot/INTEGRATION.md) | 集成指南 |
| [QUICK_START_ENGINEERING.md](.clawdbot/QUICK_START_ENGINEERING.md) | 工程化快速开始 |
| [PROMPT_TEMPLATES.md](.clawdbot/PROMPT_TEMPLATES.md) | Prompt 模板库 |
| [MEMORY.md](MEMORY.md) | 决策树和知识图谱 |

### Claude Reconstruction 文档

| 文档 | 描述 |
|------|------|
| [README.md](claude-Reconstruction/README.md) | 系统架构 |
| [CONTEXT_MANAGER.md](claude-Reconstruction/CONTEXT_MANAGER.md) | 上下文管理 |
| [QUICK_START.md](claude-Reconstruction/QUICK_START.md) | 快速开始 |

---

## 🎓 使用指南

### 命令参考

```bash
# 核心命令
./swarm spawn               # 生成普通 agent
./swarm spawn-eng           # 生成工程化 agent（推荐）
./swarm status              # 查看所有任务
./swarm check               # 手动触发监控

# 任务管理
./swarm logs <task-id>      # 查看日志
./swarm attach <task-id>    # 连接 tmux 会话
./swarm steer <task-id> <msg>  # 中途干预
./swarm kill <task-id>      # 杀死任务
./swarm cleanup             # 清理完成的任务

# 配置和集成
./swarm config              # 查看配置
./swarm integration-status  # 检查集成状态
./swarm setup-integration   # 设置集成
./swarm install-cron        # 安装自动监控
```

### 任务类型参考

选择正确的任务类型会自动加载相关规则：

| 任务类型 | 自动加载 | 适用场景 |
|---------|---------|---------|
| `api` | coding.md + api-design | REST API, GraphQL |
| `frontend` | coding.md + frontend-frameworks | React/Vue components |
| `testing` | testing.md + browser-automation | 单元测试、E2E 测试 |
| `security` | security.md + coding.md | 认证、授权 |
| `database` | coding.md + data-modeling | 迁移、查询 |
| `coding` | coding.md | 通用编码 |

### 工作流程示例

#### 完整案例：实现用户认证

```bash
# 1. 生成 agent
./swarm spawn-eng
```

```
Task ID: feat-user-auth
Task Type: security
Description: Implement JWT-based authentication

Files to create:
src/auth/jwt.ts, src/auth/middleware.ts, tests/auth/jwt.test.ts

Constraints:
- Use bcrypt for passwords
- JWT secret from env
- Refresh token in HTTP-only cookie
```

```bash
# 2. 监控进度
./swarm status
./swarm logs feat-user-auth

# 3. 必要时干预
./swarm steer feat-user-auth "Focus on API layer first"

# 4. 等待完成
# Agent 会自动：
# - 创建实现计划
# - 等待确认
# - 实现功能
# - 运行测试
# - 创建 PR
# - 触发 code review

# 5. 收到通知后审查 PR
gh pr view 342
gh pr merge 342
```

**总耗时：** 30 分钟（从想法到可合并的 PR）  
**你的工作量：** 5 分钟（确认方案 + 最终审查）

---

## 📊 性能对比

| 指标 | 普通 Agent | 工程化 Agent | 改进 |
|------|-----------|-------------|------|
| 上下文使用率 | 60%+ | 12-20% | **3-5x** |
| 代码质量 | 不稳定 | 高且一致 | **显著提升** |
| 测试覆盖率 | 可能缺失 | 强制 >80% | **有保障** |
| 重试成功率 | 低 | 高 | **Ralph Loop V2** |
| 人工介入 | 频繁 | 最小化 | **效率提升** |
| PR 质量 | 需大量审查 | 自动检查 | **自动审查** |

---

## 🎯 最佳实践

### 1. 使用工程化 Agents

```bash
# ✅ 推荐
./swarm spawn-eng

# ⚠️ 仅用于快速原型
./swarm spawn
```

### 2. 选择正确的任务类型

任务类型决定加载哪些规则：

```bash
# API 开发
Task Type: api

# 前端开发
Task Type: frontend

# 安全功能
Task Type: security
```

### 3. 写详细的 Prompt

```markdown
✅ 好的 prompt：
- 明确的任务描述
- 列出所有文件
- 说明约束条件
- 定义完成标准

❌ 糟糕的 prompt：
- "添加认证功能"
- "修复 bug"
- "改进性能"
```

### 4. 使用 Mid-Task Steering

```bash
# ✅ 引导方向
./swarm steer <task-id> "Focus on API first, then UI"

# ❌ 不要直接杀掉
./swarm kill <task-id>
```

### 5. 定期清理

```bash
# 清理完成的任务
./swarm cleanup
```

---

## 🔧 配置

### Swarm 配置

编辑 `.clawdbot/config/swarm-config.json`：

```json
{
  "system": {
    "maxConcurrentAgents": 3,
    "maxRetries": 3,
    "checkIntervalMinutes": 10
  },
  "agents": {
    "codex": {
      "model": "gpt-5.1-codex",
      "useCases": ["backend", "complex_bug"]
    },
    "claude": {
      "model": "claude-sonnet-4.5",
      "useCases": ["frontend", "quick_fix"]
    }
  }
}
```

### 集成配置

编辑 `.clawdbot/config/integration.json`：

```json
{
  "claudeReconstruction": {
    "enabled": true,
    "autoDetect": true
  },
  "agentDefaults": {
    "useEngineering": true,
    "contextBudget": "20%",
    "workflowMode": "plan-confirm-execute-deliver"
  }
}
```

---

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)。

常见贡献方向：
- 新的 prompt 模板
- 改进的监控逻辑
- 更多的任务类型支持
- 文档改进
- Bug 修复

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- **Elvis Sun** - 原始 Agent Swarm 架构
  - 文章：https://x.com/elvissun/status/2025920521871716562
- **Claude Reconstruction** - 工程化系统
  - 仓库：https://github.com/Arxchibobo/claude-Reconstruction
- **OpenClaw** - AI Agent 基础设施
  - 官网：https://openclaw.ai

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub CLI](https://cli.github.com/)

---

## 📞 支持

遇到问题？

1. 查看 [文档](.clawdbot/)
2. 运行系统测试：`./.clawdbot/test-system.sh`
3. 提交 [Issue](https://github.com/Arxchibobo/openclaw-arxchibo/issues)

---

<div align="center">

**⭐️ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by [Arxchibobo](https://github.com/Arxchibobo)

</div>
