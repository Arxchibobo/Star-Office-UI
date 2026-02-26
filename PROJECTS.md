# 📂 Projects Overview

OpenClaw 工作空间中的所有项目和子项目概览。

---

## 🚀 Active Projects

### 1. Agent Swarm System (`.clawdbot/`)

**状态**: ✅ 生产就绪  
**大小**: 189M  
**描述**: 基于 Elvis Sun 架构的完整 AI Agent 编排系统

**核心功能**:
- 双层 AI 架构（编排层 + 执行层）
- Ralph Loop V2 智能重试
- Worktree 隔离和 tmux 会话管理
- 自动代码审查（Gemini + Codex）
- Telegram 集成和通知

**技术栈**: Bash, Python, Codex, Claude, Gemini, GitHub CLI, tmux

**文档**:
- [README.md](.clawdbot/README.md)
- [SYSTEM_OVERVIEW.md](.clawdbot/SYSTEM_OVERVIEW.md)
- [QUICK_START.md](.clawdbot/QUICK_START.md)

**入口**: `~/.openclaw/workspace/.clawdbot/scripts/swarm`

---

### 2. AgentHub (agenthub/)

**状态**: 🔨 开发中（后端就绪）  
**大小**: 80M  
**描述**: AI Agent 社交平台 - GitHub 风格的 Agent 任务市场

**核心功能**:
- Agent Profile 和技能展示
- 任务发布和分配系统
- 实时 Feed 动态流
- WebSocket 实时通信
- 积分和声誉系统
- 与 Agent Swarm 深度集成

**技术栈**:
- 后端: FastAPI, PostgreSQL, SQLAlchemy, Redis, Celery
- 前端: React 18, TypeScript, Vite, TailwindCSS
- DevOps: Docker, Kubernetes, GitHub Actions

**文档**:
- [README.md](agenthub/README.md)
- [BACKEND_READY.md](agenthub/BACKEND_READY.md)
- [架构文档](agenthub/docs/project-arch/ARCHITECTURE.md)
- [API 规范](agenthub/docs/project-arch/API_SPEC.md)
- [数据库设计](agenthub/docs/project-arch/DB_SCHEMA.md)

**入口**: `agenthub/run.sh`

---

### 3. ClawProduct Hunt (projects/clawproduct-hunt/)

**状态**: ✅ 前端就绪  
**大小**: 14M  
**描述**: Product Hunt 克隆 - AI Agent 产品发现平台

**核心功能**:
- 产品展示和投票
- 分类浏览
- 搜索和过滤
- 用户评论和互动

**技术栈**:
- 后端: FastAPI, SQLite
- 前端: React, Vite

**文档**:
- [README.md](projects/clawproduct-hunt/README.md)
- [FRONTEND_READY.md](projects/clawproduct-hunt/FRONTEND_READY.md)
- [QUICKSTART.md](projects/clawproduct-hunt/QUICKSTART.md)

**入口**: `projects/clawproduct-hunt/start.sh`

**仓库**: 独立 Git 仓库（有 .git/）

---

### 4. Telegram Subagent Hooks (projects/telegram-subagent-hooks/)

**状态**: 🔨 开发中  
**大小**: 436K  
**描述**: Telegram 子 Agent 系统 - 自动响应和任务派发

**核心功能**:
- Telegram bot 集成
- 子 Agent 自动生成
- 任务队列管理
- 状态监控和通知

**技术栈**: TypeScript, Node.js, Telegram Bot API

**文档**:
- [README.md](projects/telegram-subagent-hooks/README.md)
- [DEPLOYMENT.md](projects/telegram-subagent-hooks/DEPLOYMENT.md)
- [DEV_PLAN.md](projects/telegram-subagent-hooks/DEV_PLAN.md)

**入口**: `npm start`

**仓库**: 独立 Git 仓库（有 .git/）

---

### 5. Claude Reconstruction (claude-Reconstruction/)

**状态**: ✅ 生产就绪  
**大小**: 616K  
**描述**: Claude 工程化重构系统 - 规则化编码框架

**核心功能**:
- 上下文优化（60% → 12-20%）
- 规则化 Prompt 系统
- 代码质量保证
- 知识图谱管理

**技术栈**: Markdown, YAML, TypeScript

**文档**:
- [README.md](claude-Reconstruction/README.md)
- [QUICK_START.md](claude-Reconstruction/QUICK_START.md)
- [CONTEXT_MANAGER.md](claude-Reconstruction/CONTEXT_MANAGER.md)

**仓库**: 独立 Git 仓库（有 .git/）

---

## 🗄️ Archived Projects

### 1. Demo Video (projects/archived/demo-video/)

**状态**: 📦 归档  
**大小**: 406M  
**描述**: Remotion 视频生成演示项目

**原因**: 演示完成，暂不维护  
**优化**: 可删除 node_modules/ 和 out/ 节省 ~380M

---

### 2. Temporary Files (projects/archived/tmp/)

**状态**: 📦 归档  
**大小**: 8K  
**描述**: 临时文件和测试输出

---

## 🧩 Skills (skills/)

**描述**: Agent 技能包 - 可复用的功能模块

**大小**: 228K

| Skill | 功能 | 状态 |
|-------|------|------|
| ai-conversation-summary | 对话摘要生成 | ✅ |
| nano-banana-pro | Gemini 图片生成 | ✅ |
| remotion-video-toolkit | Remotion 视频工具 | ✅ |

---

## 📊 项目统计

### 规模分布

| 类型 | 数量 | 总大小 | 占比 |
|------|------|--------|------|
| 活跃项目 | 5 | ~280M | 31.9% |
| 归档项目 | 2 | ~414M | 47.1% |
| Skills | 3 | 228K | 0.03% |
| 文档/资源 | - | ~184M | 21.0% |
| **总计** | **10** | **~878M** | **100%** |

### 技术栈分布

| 语言/框架 | 项目数 |
|-----------|--------|
| Python | 5 |
| TypeScript/JavaScript | 4 |
| Bash | 3 |
| React | 3 |
| FastAPI | 2 |

---

## 🎯 项目优先级

### 高优先级（核心功能）

1. **Agent Swarm System** - 基础设施，所有项目依赖
2. **AgentHub** - 主要产品，开发中

### 中优先级（实验性）

3. **ClawProduct Hunt** - 独立产品，前端已完成
4. **Telegram Subagent Hooks** - 集成功能，开发中

### 低优先级（支持性）

5. **Claude Reconstruction** - 工程化工具，稳定维护
6. **Skills** - 按需开发

---

## 🚀 启动所有项目

### 一键启动脚本（TODO）

```bash
# scripts/start-all.sh
#!/bin/bash

# Agent Swarm
tmux new-session -d -s swarm "cd ~/.openclaw/workspace && ./.clawdbot/scripts/swarm monitor"

# AgentHub
tmux new-window -t swarm -n agenthub "cd agenthub && ./run.sh"

# Telegram Hooks
tmux new-window -t swarm -n telegram "cd projects/telegram-subagent-hooks && npm start"

echo "All services started in tmux session 'swarm'"
tmux attach -t swarm
```

---

## 📝 项目依赖关系

```
┌─────────────────────────┐
│   AgentHub Platform     │  ← 主产品
│   (User Interface)      │
└───────────┬─────────────┘
            │ 调用
            ▼
┌─────────────────────────┐
│   Agent Swarm System    │  ← 核心引擎
│   (Orchestration)       │
└───────────┬─────────────┘
            │ 使用
            ▼
┌─────────────────────────┐
│  Claude Reconstruction  │  ← 工程化规则
│  (Prompt Engineering)   │
└─────────────────────────┘

并行独立项目：
- ClawProduct Hunt
- Telegram Subagent Hooks
- Skills (可插拔模块)
```

---

## 🔗 相关链接

- **主仓库**: https://github.com/Arxchibobo/openclaw-arxchibo
- **AgentHub**: (待发布)
- **ClawProduct Hunt**: (待发布)
- **Claude Reconstruction**: https://github.com/Arxchibobo/claude-Reconstruction

---

## 📞 维护者

- **Arxchibobo** - 所有项目
- **OpenClaw Agent** - 自动化维护和监控

---

**最后更新**: 2026-02-26  
**总项目数**: 10 (5 活跃 + 2 归档 + 3 skills)  
**工作空间大小**: ~878M
