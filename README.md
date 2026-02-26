# 🤖 OpenClaw Arxchibo Workspace

<div align="center">

**AI Agent 工作空间 • 完整的编排系统 • 工程化AI开发**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/Arxchibobo/openclaw-arxchibo?style=social)](https://github.com/Arxchibobo/openclaw-arxchibo)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)]()
[![Status](https://img.shields.io/badge/workspace-organized-brightgreen.svg)]()

[系统概览](#-系统概览) •
[项目列表](#-项目列表) •
[Agent Swarm](#-agent-swarm-系统) •
[快速开始](#-快速开始) •
[文档](#-文档)

</div>

---

## 📖 简介

这是 **Arxchibobo** 的 OpenClaw 工作空间，包含 AI Agent 编排系统、多个活跃项目和完整的工程化配置。

### ✨ 工作空间特点

- 🏗️ **清晰的目录结构** - 逻辑分层，易于维护
- 🤖 **Agent Swarm 系统** - 智能AI代理编排
- 📁 **多项目管理** - 统一管理多个子项目
- 🔧 **完整工具链** - Claude Reconstruction + 自定义脚本
- 📚 **丰富文档** - 每个系统都有完整文档
- 🔒 **安全配置** - 完善的 .gitignore 和密钥保护

---

## 📊 系统概览

### 工作空间结构 (v2.0)

```
~/.openclaw/workspace/
├── 📁 projects/               # 子项目集合 ⭐
│   ├── clawproduct-hunt/      # AgentHub - AI社交平台
│   └── telegram-subagent-hooks/ # Telegram集成钩子
├── 📁 .clawdbot/              # Agent Swarm 核心系统 ⭐
│   ├── config/                # 配置文件
│   ├── scripts/               # 编排脚本（17个）
│   ├── logs/                  # 运行日志
│   └── active-tasks.json      # 任务注册表
├── 📁 agenthub/               # AgentHub 后端独立部署
├── 📁 claude-Reconstruction/  # 工程化AI配置
├── 📁 skills/                 # OpenClaw 技能库
├── 📁 memory/                 # 记忆系统（YYYY-MM-DD.md）
├── 📁 assets/                 # 资源文件 ⭐
│   ├── images/                # 图片归档
│   └── temp/                  # 临时文件
├── 📁 docs/                   # 文档归档 ⭐
│   └── archived/              # 历史文档
├── 📄 MEMORY.md               # 长期记忆
├── 📄 AGENTS.md               # Agent 行为规范
├── 📄 SOUL.md                 # 核心价值观
├── 📄 TOOLS.md                # 工具配置
├── 📄 PROJECTS.md             # 项目总览 ⭐
└── 📄 WORKSPACE_REPORT.md     # 工作空间整理报告 ⭐
```

### 关键改进 (v2.0.0)

| 改进项 | 优化前 | 优化后 | 提升 |
|-------|--------|--------|------|
| 根目录文件数 | 27 | 17 | ⬇️ **37%** |
| .gitignore规则 | 37行 | 95行 | ⬆️ **157%** |
| 目录组织 | 分散 | 分层 | ✅ **清晰** |
| 资源管理 | 零散 | 归档 | ✅ **集中** |
| 文档完整度 | 中等 | 完善 | ✅ **提升** |

---

## 🚀 项目列表

### 活跃项目

#### 1. **clawproduct-hunt** (AgentHub) ⭐
**位置**: `projects/clawproduct-hunt/`  
**描述**: AI Agent 社交平台与技能市场  
**状态**: ✅ Production Ready (v1.2.0)  
**技术栈**: FastAPI, SQLAlchemy, WebSocket, Vanilla JS, Tailwind CSS  
**大小**: ~80 MB

**特性**:
- 多Agent协作和社交网络
- 实时Feed动态
- 任务发布与分配
- 暗黑模式、搜索筛选
- 19个自动化测试
- 完整安全防护

**启动**:
```bash
cd projects/clawproduct-hunt
./setup.sh dev
# 访问 http://localhost:8000
```

#### 2. **telegram-subagent-hooks**
**位置**: `projects/telegram-subagent-hooks/`  
**描述**: Telegram Bot 与 Agent Swarm 集成钩子  
**状态**: 🔄 开发中  
**技术栈**: Python, pyTelegramBotAPI  
**大小**: ~100 KB

#### 3. **agenthub** (独立部署)
**位置**: `agenthub/`  
**描述**: AgentHub 后端独立实例  
**状态**: ✅ 就绪  
**大小**: ~80 MB

### 归档项目

#### demo-video
**位置**: `projects/archived/demo-video/`  
**描述**: 视频演示项目  
**状态**: 📦 已归档  
**大小**: ~406 MB (可优化至 26MB)

---

## 🤖 Agent Swarm 系统

### 核心理念

Agent Swarm 是一个基于 [Elvis Sun 的架构](https://x.com/elvissun/status/2025920521871716562) 和 [Claude Reconstruction](https://github.com/Arxchibobo/claude-Reconstruction) 的 AI Agent 编排系统。

### 三层架构

```
Layer 1: 编排层 (Orchestrator)
  ↓ 读取业务上下文，决策任务优先级
Layer 2: Agent Swarm (编排层)
  ↓ 生成、监控、重试 agents
Layer 3: Claude Reconstruction (5层工程化配置)
  ↓ 智能上下文、工作流程、规则引擎
Execution: Claude Code/Codex Agents
  ↓ 高质量代码产出
```

### 关键特性

1. **Ralph Loop V2** - 智能重试
   - 失败 → 分析原因 → 重写 prompt → 重试
   - 不是无脑重复相同 prompt

2. **Context Manager** - 智能加载
   - 只加载需要的文档（12-20% vs 60%+）
   - 根据任务类型自动选择

3. **4步工作流程** - 专业行为
   - Plan → Confirm → Execute → Deliver
   - 强制流程，不跳步

4. **5层质量保证**
   - Layer 5: Context Manager (智能加载)
   - Layer 4: Workflow Engine (强制流程)
   - Layer 3: Rules Engine (编码规范)
   - Layer 2: Hook Layer (质量门控)
   - Layer 1: Delegation Layer (专家系统)

### 快速使用

#### 创建普通 Agent
```bash
cd ~/.openclaw/workspace
./swarm spawn
```

#### 创建工程化 Agent（推荐）
```bash
./swarm spawn-eng
# 选择任务类型: api, frontend, testing, security, coding
```

#### 管理任务
```bash
./swarm status      # 查看状态
./swarm logs <id>   # 查看日志
./swarm steer <id> "新指令"  # 引导方向
./swarm kill <id>   # 杀死任务
./swarm cleanup     # 清理完成的任务
```

### 脚本工具

| 脚本 | 功能 | 位置 |
|------|------|------|
| `swarm` | 主控制脚本 | `.clawdbot/scripts/swarm` |
| `agent-control.sh` | 小波比专用控制 | `.clawdbot/scripts/agent-control.sh` |
| `spawn-for-bobi.sh` | 非交互式spawn | `.clawdbot/scripts/spawn-for-bobi.sh` |
| `telegram-main-bot.py` | Telegram Bot | `.clawdbot/scripts/telegram-main-bot.py` |

---

## 🔧 Claude Reconstruction 集成

### 什么是 Claude Reconstruction？

一个5层工程化配置系统，让 Claude（或任何 AI coding assistant）像 senior engineer 一样工作。

### 核心配置

**位置**: `claude-Reconstruction/`

**包含**:
- **CLAUDE.md** - 主配置文件
- **CONTEXT_MANAGER.md** - 智能上下文管理
- **rules/core/** - 核心规则（编码、Git、测试）
- **rules/domain/** - 领域规则（API、前端、安全）
- **capabilities/** - 能力定义

### 任务类型

| 类型 | 自动加载规则 | 适用场景 |
|------|-------------|---------|
| `api` | API设计、安全、RESTful | 后端API开发 |
| `frontend` | UI规范、性能、响应式 | 前端开发 |
| `testing` | 测试策略、覆盖率 | 测试开发 |
| `security` | 安全审查、加密 | 安全功能 |
| `coding` | 代码规范、Git、重构 | 通用编码 |

---

## 📚 文档

### 工作空间文档

- **[WORKSPACE_REPORT.md](WORKSPACE_REPORT.md)** - 工作空间整理详细报告
- **[PROJECTS.md](PROJECTS.md)** - 所有项目概览和统计
- **[MEMORY.md](MEMORY.md)** - 长期记忆和决策记录
- **[AGENTS.md](AGENTS.md)** - Agent 行为规范
- **[SOUL.md](SOUL.md)** - 核心价值观和原则
- **[TOOLS.md](TOOLS.md)** - 工具配置（API keys 等）

### Agent Swarm 文档

- **[.clawdbot/README.md](.clawdbot/README.md)** - Agent Swarm 完整指南
- **[.clawdbot/INTEGRATION.md](.clawdbot/INTEGRATION.md)** - 集成指南
- **[.clawdbot/QUICK_START_ENGINEERING.md](.clawdbot/QUICK_START_ENGINEERING.md)** - 工程化快速开始
- **[.clawdbot/SYSTEM_OVERVIEW.md](.clawdbot/SYSTEM_OVERVIEW.md)** - 系统架构总览
- **[.clawdbot/TELEGRAM_INTEGRATION.md](.clawdbot/TELEGRAM_INTEGRATION.md)** - Telegram Bot 集成

### 项目文档

- **[projects/clawproduct-hunt/README.md](projects/clawproduct-hunt/README.md)** - AgentHub 项目文档
- **[projects/clawproduct-hunt/DEPLOYMENT.md](projects/clawproduct-hunt/DEPLOYMENT.md)** - 部署指南
- **[projects/clawproduct-hunt/FRONTEND_ENHANCEMENT.md](projects/clawproduct-hunt/FRONTEND_ENHANCEMENT.md)** - 前端增强报告
- **[projects/clawproduct-hunt/OPTIMIZATION_REPORT.md](projects/clawproduct-hunt/OPTIMIZATION_REPORT.md)** - 架构优化报告

---

## 🚀 快速开始

### 1. 启动 Agent Swarm

```bash
# 查看帮助
cd ~/.openclaw/workspace
./swarm help

# 创建工程化 Agent
./swarm spawn-eng
```

### 2. 启动 AgentHub

```bash
cd projects/clawproduct-hunt
./setup.sh dev
# 访问 http://localhost:8000
```

### 3. 启动 Telegram Bot

```bash
cd .clawdbot/scripts
./start-telegram-swarm.sh
```

---

## 🔒 安全

### .gitignore 保护（95行，6大类）

1. **Python 环境** - venv/, *.pyc, __pycache__/
2. **Node.js** - node_modules/, package-lock.json
3. **IDE/编辑器** - .vscode/, .idea/, *.swp
4. **操作系统** - .DS_Store, Thumbs.db
5. **敏感信息** - *.env, .env.*, *.key, *_token.json
6. **资源文件** - *.mp4, *.mov, *.zip

### 密钥管理

- ✅ GitHub Token 保存在 `.github-token` (不提交)
- ✅ Telegram Bot Token 在 `.clawdbot/config/` (不提交)
- ✅ API Keys 在 `~/.bashrc` 或环境变量
- ✅ 所有密钥路径已加入 .gitignore

---

## 📊 工作空间统计

### 总览

- **总大小**: ~878 MB
- **子项目数**: 4 个（2活跃 + 2归档）
- **文档数**: 20+ 份
- **脚本数**: 30+ 个
- **Agent Swarm 配置**: 完整

### 技术栈分布

| 技术栈 | 项目数 | 主要项目 |
|--------|--------|---------|
| Python + FastAPI | 2 | clawproduct-hunt, agenthub |
| JavaScript/Node.js | 2 | clawproduct-hunt前端, demo-video |
| Bash Scripts | 多个 | Agent Swarm, 部署脚本 |
| Markdown 文档 | 20+ | 各类文档 |

---

## 🎯 最佳实践

### 新建项目时

1. **评估是否需要 Agent** - 检查决策树
2. **选择正确的 Agent 类型**:
   - 后端/复杂逻辑 → codex
   - 前端/快速迭代 → claude
   - UI设计/创意 → gemini
3. **使用工程化模式**: `./swarm spawn-eng`
4. **写详细的 prompt**: 文件列表、约束、测试要求
5. **定期清理**: `./swarm cleanup`

### 管理工作空间

1. **定期整理**: 使用提供的脚本
2. **文档先行**: 每个项目都有 README
3. **Git 提交规范**: 使用语义化提交信息
4. **安全第一**: 不提交密钥和大文件

---

## 🤝 贡献

欢迎 PR 和 Issue！

### 贡献指南

1. Fork 本仓库
2. 创建功能分支
3. 提交更改（遵循提交规范）
4. 推送到分支
5. 打开 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 📞 联系方式

- **作者**: Arxchibobo
- **GitHub**: [openclaw-arxchibo](https://github.com/Arxchibobo/openclaw-arxchibo)
- **项目主页**: [OpenClaw Agent Swarm](https://github.com/Arxchibobo/openclaw-arxchibo)

---

## 📈 版本历史

### v2.0.0 (2026-02-26) - 工作空间重组 ✅
- 🏗️ 完整的目录结构重组
- 📁 项目集中管理（projects/）
- 📚 文档归档和完善
- 🔒 安全加固（.gitignore 95行）
- 📊 完整的统计和报告
- ✨ Agent Swarm 系统优化

### v1.0.0 (2026-02-25) - 初始发布
- 🎉 Agent Swarm 系统部署
- 🤖 Claude Reconstruction 集成
- 📱 Telegram Bot 集成

---

**工作空间版本**: v2.0.0  
**组织状态**: ✅ **Organized & Optimized**  
**质量评级**: ⭐⭐⭐⭐⭐ (5/5)  
**最后更新**: 2026-02-26

---

⭐ **如果这个工作空间对你有帮助，请给我们一个 Star！** ⭐
