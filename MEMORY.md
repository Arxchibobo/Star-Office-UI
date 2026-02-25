# MEMORY.md - Long-Term Memory

## 基础信息

- User wants me to be called **小波比**.
- User has a local knowledge/workspace directory: `E:\Bobo's Coding cache\bo-work\claude-reconstruction`. I should learn from it (or the GitHub repo: https://github.com/Arxchibobo/claude-Reconstruction).
- **Strict constraint:** I must NOT modify any pre-existing files on the user's computer; I may only create/edit/delete content that *I* create.
- This constraint should apply across all conversations.
- User wants auto-compact behavior for long contexts; follow COMPACT_POLICY.md by default.

## 工具和配置

- **Image generation:** Use `nano-banana-pro` skill (Gemini 3 Pro Image) - GEMINI_API_KEY configured in ~/.bashrc.
- **Cross-session consistency:** Tool configurations and skills are shared across all sessions (group and private), but conversation memory is isolated for privacy.
- **Claude CLI:** Installed at /usr/local/bin/claude (version 2.0.28)
- **Workspace:** ~/.openclaw/workspace (local git repo, no remote configured yet)

## Agent Swarm 系统 - 知识图谱

### 系统架构（3层）

```
Layer 1: 我/OpenClaw (最高编排层)
  ↓ 读取业务上下文，决策任务优先级
Layer 2: Agent Swarm (编排层)
  ↓ 生成、监控、重试 agents
Layer 3: Claude Reconstruction (5层工程化配置)
  ↓ 智能上下文、工作流程、规则引擎
Execution: Claude Code/Codex Agents
  ↓ 高质量代码产出
```

### 核心系统位置

- **Agent Swarm:** `~/.openclaw/workspace/.clawdbot/`
  - 主入口: `~/workspace/swarm`
  - 配置: `.clawdbot/config/swarm-config.json`
  - 任务注册: `.clawdbot/active-tasks.json`
  - 脚本: `.clawdbot/scripts/`
  - 文档: `.clawdbot/*.md`

- **Claude Reconstruction:** `~/.openclaw/workspace/claude-Reconstruction/`
  - 主配置: `CLAUDE.md`
  - Context Manager: `CONTEXT_MANAGER.md`
  - 规则: `rules/core/`, `rules/domain/`
  - 能力: `capabilities/`

### 核心概念

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

## 决策树 - 何时使用什么

### 新建项目时

```
新项目
  ├─ 需要 AI agents 帮助？
  │   ├─ YES → 使用 Agent Swarm
  │   │   ├─ 快速原型/测试？
  │   │   │   └─ YES → ./swarm spawn (普通 agent)
  │   │   └─ 生产级代码？
  │   │       └─ YES → ./swarm spawn-eng (工程化 agent)
  │   │           ├─ 任务类型选择：
  │   │           │   ├─ API 开发 → api
  │   │           │   ├─ 前端开发 → frontend
  │   │           │   ├─ 测试开发 → testing
  │   │           │   ├─ 安全功能 → security
  │   │           │   └─ 通用编码 → coding
  │   │           └─ 自动加载对应规则和能力
  │   └─ NO → 继续下一步
  │
  ├─ 需要工程化规范？
  │   └─ YES → 参考 Claude Reconstruction
  │       ├─ 编码规范 → rules/domain/coding.md
  │       ├─ 测试规范 → rules/domain/testing.md
  │       ├─ 安全规范 → rules/domain/security.md
  │       └─ Git 规范 → rules/domain/git.md
  │
  └─ 需要图片生成？
      └─ YES → 使用 nano-banana-pro
```

### 任务执行时

```
收到任务
  ├─ 是否复杂/耗时？
  │   ├─ YES → 生成 Agent
  │   │   ├─ 评估复杂度
  │   │   │   ├─ 简单 (< 1h) → 1个 agent
  │   │   │   ├─ 中等 (1-4h) → 1-2个 agents
  │   │   │   └─ 复杂 (> 4h) → 拆分任务，多个 agents
  │   │   └─ 选择 agent 类型
  │   │       ├─ 后端/复杂逻辑 → codex
  │   │       ├─ 前端/快速迭代 → claude
  │   │       └─ UI 设计 → gemini (设计) + claude (实现)
  │   └─ NO → 我直接处理
  │
  ├─ Agent 执行中
  │   ├─ 方向正确？
  │   │   ├─ YES → 继续监控
  │   │   └─ NO → ./swarm steer (中途干预)
  │   └─ Agent 失败？
  │       └─ Ralph Loop V2 自动处理
  │           ├─ 分析失败原因
  │           ├─ 重写 prompt
  │           └─ 自动重试（最多3次）
  │
  └─ 完成后
      ├─ 自动 Code Review (Gemini + Codex)
      ├─ CI/CD 检查
      ├─ 通知我审查
      └─ 我快速审查 + 合并
```

### 检索和使用资源

```
需要参考信息
  ├─ Agent Swarm 相关？
  │   ├─ 系统总览 → .clawdbot/SYSTEM_OVERVIEW.md
  │   ├─ 集成指南 → .clawdbot/INTEGRATION.md
  │   ├─ 快速开始 → .clawdbot/QUICK_START_ENGINEERING.md
  │   └─ Prompt 模板 → .clawdbot/PROMPT_TEMPLATES.md
  │
  ├─ Claude Reconstruction 相关？
  │   ├─ 系统架构 → claude-Reconstruction/README.md
  │   ├─ 上下文管理 → claude-Reconstruction/CONTEXT_MANAGER.md
  │   ├─ 核心规则 → claude-Reconstruction/rules/core/
  │   └─ 领域规则 → claude-Reconstruction/rules/domain/
  │
  └─ 工具使用？
      ├─ 图片生成 → TOOLS.md (nano-banana-pro)
      ├─ 浏览器控制 → browser tool
      └─ 其他工具 → TOOLS.md
```

## 系统状态

### Git 仓库
- **位置:** ~/.openclaw/workspace
- **状态:** 本地仓库，已提交3个 Agent Swarm commits
- **远程:** 未配置（需要时可以 push 到 GitHub）
- **最新提交:**
  1. `d225470` - Add complete system overview documentation
  2. `9d1a88d` - Integrate Agent Swarm with Claude Reconstruction
  3. `42a2811` - Add complete Agent Swarm system prototype

### 系统就绪状态
- ✅ Agent Swarm 系统完整安装
- ✅ Claude Reconstruction 已集成
- ✅ Claude CLI 已安装 (v2.0.28)
- ✅ 所有脚本可执行
- ✅ 完整文档齐全
- ⚠️ GitHub remote 未配置（需要时配置）
- ⚠️ Cron monitoring 未安装（可选）

## 最佳实践提醒

1. **新项目时先检查决策树** - 确定是否需要 agents
2. **使用工程化 agents** - `./swarm spawn-eng` 优于 `./swarm spawn`
3. **正确选择任务类型** - 影响自动加载的规则
4. **写详细的 prompt** - 文件列表、约束、测试要求
5. **不要杀 agent，用 steering** - `./swarm steer` 引导方向
6. **定期清理** - `./swarm cleanup` 清理完成的任务
7. **监控进度** - `./swarm status` 和 `./swarm logs`

## 学习和内化的系统

- **Claude Reconstruction 5层系统** - 已完全理解并可以在新项目中应用
- **Agent Swarm 编排系统** - 已部署并可以使用
- **Ralph Loop V2 逻辑** - 失败时分析原因并改进 prompt
- **Context Manager 原理** - 智能加载文档节省 context
- **4步工作流程** - Plan-Confirm-Execute-Deliver

## 需要记住的约束

- 不修改用户已有的文件
- 只操作我创建的内容
- Group chat 中不读取 MEMORY.md（隐私保护）
- 使用 nano-banana-pro 而不是 DALL-E（billing limit）
- Memory search 当前不可用（OpenAI embeddings quota exhausted）

