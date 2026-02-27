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

### 2. Star Office UI (projects/Star-Office-UI/)

**状态**: ✅ 生产就绪  
**大小**: ~15M  
**描述**: 像素风格办公室可视化 - 实时展示 AI Assistant 工作状态

**核心功能**:
- Telegram WebApp 集成
- 实时状态同步（Agent Swarm）
- 像素风格动画
- 状态映射和可视化
- 截图推送到 Telegram

**技术栈**:
- 后端: Flask, Flask-CORS
- 前端: Phaser 3 (游戏引擎) + Vanilla JS
- 集成: Playwright (截图)

**文档**:
- [STAR_OFFICE_INTEGRATION.md](projects/Star-Office-UI/STAR_OFFICE_INTEGRATION.md)
- [README.md](projects/Star-Office-UI/README.md)

**入口**: `projects/Star-Office-UI/start.sh`

**WebApp URL**: https://showtimes-lyric-titanium-sale.trycloudflare.com/debug

---

### 3. Telegram Subagent Hooks (projects/telegram-subagent-hooks/)

**状态**: 🔨 开发中（架构完成）  
**大小**: 436K  
**描述**: Telegram 子 Agent 系统 - 持久化线程绑定的 Agent Sessions

**核心功能**:
- Telegram Forum Topics 作为线程
- 子 Agent 自动生成和绑定
- 任务状态监控
- 实时消息通知

**技术栈**: TypeScript, Node.js, Telegram Bot API

**文档**:
- [README.md](projects/telegram-subagent-hooks/README.md)
- [DEV_PLAN.md](projects/telegram-subagent-hooks/DEV_PLAN.md)
- [NEXT_STEPS.md](projects/telegram-subagent-hooks/NEXT_STEPS.md)

**入口**: `npm start`

**仓库**: 独立 Git 仓库（有 .git/）

---

### 4. Claude Reconstruction (claude-Reconstruction/)

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
| 活跃项目 | 4 | ~205M | 94.5% |
| Skills | 3 | 228K | 0.1% |
| 文档/配置 | - | ~12M | 5.4% |
| **总计** | **7** | **~217M** | **100%** |

### 技术栈分布

| 语言/框架 | 项目数 |
|-----------|--------|
| Python | 3 |
| TypeScript/JavaScript | 2 |
| Bash | 2 |
| Flask | 1 |
| Phaser 3 | 1 |

---

## 🎯 项目优先级

### 高优先级（核心功能）

1. **Agent Swarm System** - 基础设施，所有项目依赖
2. **Star Office UI** - 实时可视化，已部署

### 中优先级（实验性）

3. **Telegram Subagent Hooks** - 集成功能，开发中

### 低优先级（支持性）

4. **Claude Reconstruction** - 工程化工具，稳定维护
5. **Skills** - 按需开发

---

## 🚀 启动所有项目

### 一键启动脚本

```bash
#!/bin/bash
# scripts/start-all.sh

# Agent Swarm 监控
tmux new-session -d -s workspace "cd ~/.openclaw/workspace && watch -n 10 './swarm status'"

# Star Office UI
tmux new-window -t workspace -n office "cd projects/Star-Office-UI && ./start.sh"

# Telegram Bot（如果需要）
tmux new-window -t workspace -n telegram "cd ~/.openclaw/workspace/.clawdbot/scripts && python telegram-main-bot.py"

echo "✅ All services started in tmux session 'workspace'"
tmux attach -t workspace
```

---

## 📝 项目依赖关系

```
┌──────────────────────────┐
│   Star Office UI         │  ← 可视化界面
│   (Telegram WebApp)      │
└────────────┬─────────────┘
             │ 展示状态
             ▼
┌──────────────────────────┐
│   Agent Swarm System     │  ← 核心引擎
│   (Orchestration)        │
└────────────┬─────────────┘
             │ 使用规则
             ▼
┌──────────────────────────┐
│  Claude Reconstruction   │  ← 工程化规则
│  (Prompt Engineering)    │
└──────────────────────────┘

并行独立项目：
- Telegram Subagent Hooks
- Skills (可插拔模块)
```

---

## 🔗 相关链接

- **主仓库**: https://github.com/Arxchibobo/openclaw-arxchibo
- **Claude Reconstruction**: https://github.com/Arxchibobo/claude-Reconstruction
- **Telegram Subagent Hooks**: 独立仓库（项目内）
- **Star Office UI WebApp**: https://showtimes-lyric-titanium-sale.trycloudflare.com/debug

---

## 📞 维护者

- **Arxchibobo** - 所有项目
- **OpenClaw Agent (小波比)** - 自动化维护和监控

---

**最后更新**: 2026-02-26  
**总项目数**: 7 (4 活跃 + 3 skills)  
**工作空间大小**: ~217M  
**完成度**: 98%
