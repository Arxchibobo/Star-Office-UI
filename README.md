# 🤖 OpenClaw Arxchibo Workspace

<div align="center">

**AI Agent 工作空间 • 完整的编排系统 • 工程化AI开发**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/Arxchibobo/openclaw-arxchibo?style=social)](https://github.com/Arxchibobo/openclaw-arxchibo)
[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)]()
[![Status](https://img.shields.io/badge/workspace-production-brightgreen.svg)]()

[系统概览](#-系统概览) •
[项目列表](#-项目列表) •
[Agent Swarm](#-agent-swarm-系统) •
[快速开始](#-快速开始) •
[文档](#-文档)

</div>

---

## 📖 简介

这是 **Arxchibobo** 的 OpenClaw 工作空间，包含 AI Agent 编排系统、实时可视化UI和完整的工程化配置。

### ✨ 工作空间特点

- 🏗️ **清晰的目录结构** - 逻辑分层，易于维护
- 🤖 **Agent Swarm 系统** - 智能AI代理编排
- 🎨 **Star Office UI** - 实时可视化工作状态
- 📱 **Telegram 集成** - 移动端远程控制
- 🔧 **完整工具链** - Claude Reconstruction + 自定义脚本
- 📚 **丰富文档** - 每个系统都有完整文档

---

## 📊 系统概览

### 工作空间结构 (v2.1)

```
~/.openclaw/workspace/
├── 📁 projects/               # 子项目集合 ⭐
│   ├── Star-Office-UI/        # 像素办公室可视化
│   └── telegram-subagent-hooks/ # Telegram集成钩子
├── 📁 .clawdbot/              # Agent Swarm 核心系统 ⭐
│   ├── config/                # 配置文件
│   ├── scripts/               # 编排脚本（18个）
│   ├── logs/                  # 运行日志
│   └── active-tasks.json      # 任务注册表
├── 📁 claude-Reconstruction/  # 工程化AI配置
├── 📁 skills/                 # OpenClaw 技能库
├── 📁 memory/                 # 记忆系统（YYYY-MM-DD.md）
├── 📁 assets/                 # 资源文件
├── 📁 docs/                   # 文档归档
├── 📄 MEMORY.md               # 长期记忆
├── 📄 AGENTS.md               # Agent 行为规范
├── 📄 SOUL.md                 # 核心价值观
├── 📄 TOOLS.md                # 工具配置
├── 📄 PROJECTS.md             # 项目总览 ⭐
└── 📄 swarm                   # Agent Swarm CLI ⭐
```

---

## 🚀 项目列表

### 1. Agent Swarm System ⭐⭐⭐

**核心编排引擎**

- 双层 AI 架构（编排层 + 执行层）
- Ralph Loop V2 智能重试
- Worktree 隔离和 tmux 会话管理
- Telegram 远程控制
- 自动代码审查

**快速开始**:
```bash
cd ~/.openclaw/workspace
./swarm spawn            # 创建 agent
./swarm status           # 查看状态
./swarm logs <task-id>   # 查看日志
```

**文档**: [.clawdbot/README.md](.clawdbot/README.md)

---

### 2. Star Office UI ⭐⭐

**实时可视化工作状态**

- Telegram WebApp 集成
- 像素风格动画（Phaser 3）
- 实时状态同步
- Agent 工作状态展示

**访问**: https://showtimes-lyric-titanium-sale.trycloudflare.com/debug

**启动**:
```bash
cd projects/Star-Office-UI
./start.sh
```

**文档**: [projects/Star-Office-UI/STAR_OFFICE_INTEGRATION.md](projects/Star-Office-UI/STAR_OFFICE_INTEGRATION.md)

---

### 3. Telegram Integration

**移动端控制中心**

两个 Bot 已配置：
- **ArxchiboSwarm_bot** - Agent Swarm 主控制
- **boboclawbot** - OpenClaw 集成

**可用命令**:
```
/spawn <id> <type> <desc>  - 创建 agent
/status                     - 查看状态
/logs <id>                  - 查看日志
/kill <id>                  - 终止任务
/cleanup                    - 清理完成任务
```

**文档**: [.clawdbot/TELEGRAM_INTEGRATION.md](.clawdbot/TELEGRAM_INTEGRATION.md)

---

### 4. Claude Reconstruction

**工程化 AI 开发框架**

- 上下文优化（60% → 12-20%）
- 规则化 Prompt 系统
- 4 步工作流程
- 自动能力进化

**启动**:
```bash
cd ~/.openclaw/workspace
./start-claude-code.sh api  # 指定任务类型
```

**文档**: [claude-Reconstruction/README.md](claude-Reconstruction/README.md)

---

## 🎯 Agent Swarm 系统

### 核心概念

```
┌─────────────────────────────┐
│  我 / OpenClaw (最高编排层)  │
│  - 业务决策                  │
│  - 优先级管理                │
└───────────┬─────────────────┘
            │
            ▼
┌─────────────────────────────┐
│  Agent Swarm (编排层)        │
│  - 生成 agents               │
│  - 监控进度                  │
│  - Ralph Loop V2 重试        │
└───────────┬─────────────────┘
            │
            ▼
┌─────────────────────────────┐
│  Claude Reconstruction       │
│  (5层工程化配置)              │
│  - Context Manager           │
│  - Workflow Engine           │
│  - Rules Engine              │
└───────────┬─────────────────┘
            │
            ▼
┌─────────────────────────────┐
│  Execution Layer             │
│  - Claude Code / Codex       │
│  - 高质量代码产出             │
└─────────────────────────────┘
```

### 工作流程

1. **创建 Agent**
   ```bash
   ./swarm spawn-eng
   ```
   
2. **监控进度**
   ```bash
   ./swarm status
   # 或在 Telegram 中使用 /status
   ```

3. **查看日志**
   ```bash
   ./swarm logs <task-id>
   # 或使用 /logs <task-id>
   ```

4. **中途干预**
   ```bash
   ./swarm steer <task-id>
   ```

5. **完成清理**
   ```bash
   ./swarm cleanup
   ```

---

## 🚦 快速开始

### 前提条件

- OpenClaw Gateway 运行中
- Claude CLI 已安装
- tmux 已安装
- (可选) Telegram Bot Token

### 1. 启动 Agent Swarm

```bash
cd ~/.openclaw/workspace

# 创建工程化 agent
./swarm spawn-eng

# 按提示输入：
# - Task ID: my-api-task
# - Agent Type: codex (或 claude/gemini)
# - Task Type: api (或 frontend/testing/security/coding)
# - Description: Build REST API with FastAPI
```

### 2. 启动可视化 UI

```bash
cd projects/Star-Office-UI
./deploy.sh          # 首次运行
./start.sh           # 启动服务
./start_sync.sh      # 启动状态同步
```

### 3. 配置 Telegram (可选)

```bash
cd ~/.openclaw/workspace/.clawdbot/scripts
python telegram-main-bot.py
```

打开 Telegram，搜索 `@ArxchiboSwarm_bot`，发送 `/help`

---

## 📚 文档

### 核心文档

- [PROJECTS.md](PROJECTS.md) - 项目总览
- [AGENTS.md](AGENTS.md) - Agent 行为规范
- [MEMORY.md](MEMORY.md) - 系统知识图谱
- [TOOLS.md](TOOLS.md) - 工具配置

### Agent Swarm 文档

- [系统概览](.clawdbot/SYSTEM_OVERVIEW.md)
- [快速开始](.clawdbot/QUICK_START_ENGINEERING.md)
- [集成指南](.clawdbot/INTEGRATION.md)
- [Telegram 集成](.clawdbot/TELEGRAM_INTEGRATION.md)
- [Prompt 模板](.clawdbot/PROMPT_TEMPLATES.md)

### Claude Reconstruction 文档

- [主文档](claude-Reconstruction/README.md)
- [Context Manager](claude-Reconstruction/CONTEXT_MANAGER.md)
- [快速开始](claude-Reconstruction/QUICK_START.md)

---

## 🛠️ 常用命令

### Agent 管理

```bash
# 创建 agent
./swarm spawn              # 普通 agent
./swarm spawn-eng          # 工程化 agent

# 监控
./swarm status             # 查看所有任务
./swarm logs <id>          # 查看日志
./swarm attach <id>        # 连接 tmux

# 控制
./swarm steer <id>         # 中途干预
./swarm kill <id>          # 终止任务
./swarm cleanup            # 清理完成任务
```

### Telegram 命令

```
/spawn <id> <type> <desc>  - 创建 agent
/status                     - 查看状态
/logs <id>                  - 查看日志
/kill <id>                  - 终止任务
/cleanup                    - 清理
/help                       - 帮助
```

### 可视化 UI

```bash
# 启动服务
cd projects/Star-Office-UI
./start.sh

# 启动状态同步
./start_sync.sh

# 访问 WebApp
# https://showtimes-lyric-titanium-sale.trycloudflare.com/debug
```

---

## 📈 系统状态

### 完成度

- **Agent Swarm**: 100% ✅
- **Telegram 集成**: 100% ✅
- **Star Office UI**: 100% ✅
- **Claude Reconstruction**: 100% ✅
- **文档**: 100% ✅

### 测试状态

- ✅ Agent spawn/status/logs/kill
- ✅ Telegram Bot 所有命令
- ✅ WebApp 访问和实时更新
- ✅ Claude Reconstruction 集成

---

## 🔒 安全

### 敏感信息保护

- `.github-token` - GitHub Personal Access Token (gitignored)
- `.clawdbot/config/*.json` - Bot tokens (gitignored)
- `state.json` - 运行时状态 (gitignored)

### 权限系统

Telegram Bot 授权：
- **用户ID**: 7744442092, 8573919212
- **群组ID**: 7744442092 (私聊), -1003731869348

---

## 📞 联系方式

- **GitHub**: [@Arxchibobo](https://github.com/Arxchibobo)
- **项目**: [openclaw-arxchibo](https://github.com/Arxchibobo/openclaw-arxchibo)
- **Telegram**: @ArxchiboSwarm_bot

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - 核心框架
- [Claude](https://claude.ai) - AI 助手
- Elvis Sun - Agent Swarm 架构灵感

---

**最后更新**: 2026-02-26  
**版本**: v2.1.0  
**状态**: Production Ready  
**完成度**: 100%
