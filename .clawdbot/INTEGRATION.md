# Agent Swarm + Claude Reconstruction Integration

将 Agent Swarm 系统与 Claude Reconstruction 工程化配置集成。

## 集成架构

```
┌──────────────────────────────────────────┐
│  Agent Swarm (编排层)                     │
│  • 生成 agents                            │
│  • 监控进度                               │
│  • Ralph Loop V2                         │
└──────────┬───────────────────────────────┘
           │ 使用工程化配置
           ▼
┌──────────────────────────────────────────┐
│  Claude Reconstruction (配置层)          │
│  • 5层工程化系统                          │
│  • Context Manager (智能加载)            │
│  • Workflow Engine (工作流程)            │
│  • Rules Engine (编码规则)               │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  Claude Code Agents (执行层)            │
│  • 遵循工程化规则                         │
│  • 智能上下文管理                         │
│  • 高质量代码产出                         │
└──────────────────────────────────────────┘
```

## 核心优势

### 1. 智能上下文管理

**Before (普通 Agent):**
```
Context usage: 60%+
120KB config loaded
Limited space for actual code
```

**After (With Claude Reconstruction):**
```
Context usage: 12-20%
Only load relevant rules
80%+ space for actual work
```

### 2. 工程化行为

**普通 Agent：**
- 像 chatbot 一样行为
- 频繁询问
- 代码质量不稳定

**工程化 Agent：**
- 像 senior engineer 行为
- Plan → Confirm → Execute → Deliver
- 遵循编码规范和最佳实践

### 3. 5层质量保证

```
Layer 5: Context Manager   → 只加载需要的文档
Layer 4: Workflow Engine   → Plan-Confirm-Execute
Layer 3: Rules Engine      → 编码规范、测试规范
Layer 2: Hook Layer        → 工具调用前后的质量检查
Layer 1: Delegation Layer  → 路由到专业 sub-agents
```

## 使用方法

### 方法 1: 启动时指定工程化配置

```bash
# 在 spawn-agent.sh 中会自动检测并使用 claude-Reconstruction 配置
./swarm spawn

# 输入：
# Task ID: feat-user-auth
# Agent type: claude
# Description: Implement user authentication with JWT
# Prompt: (使用工程化模板)
```

### 方法 2: 使用集成脚本

```bash
# 使用预配置的工程化 agent
./swarm spawn-with-config

# 自动：
# - 检测 claude-Reconstruction 是否安装
# - 使用 Context Manager 智能加载
# - 应用工程化工作流程
# - 遵循编码规范
```

### 方法 3: 手动指定配置路径

```bash
# 为特定项目指定配置
CLAUDE_CONFIG=~/.openclaw/workspace/claude-Reconstruction \
./swarm spawn
```

## Prompt 模板（工程化版本）

### 标准工程化 Prompt

```markdown
CONTEXT:
You are working in a project that uses the Claude Reconstruction engineering system.
- Follow the Plan-Confirm-Execute-Deliver workflow
- Load context intelligently (only what's needed)
- Follow coding rules in rules/domain/coding.md
- Follow git workflow in rules/domain/git.md

TASK:
[具体任务描述]

FILES TO MODIFY:
[文件列表]

WORKFLOW:
1. **Plan**: Analyze the task, identify files, plan approach
2. **Confirm**: Present plan to orchestrator (via comments in code or commit message)
3. **Execute**: Implement following rules
4. **Deliver**: Create PR with clear description

RULES TO FOLLOW:
- Immutability: Avoid mutating existing data structures
- File Organization: Keep files under 400 lines
- Testing: Add tests for all new features
- Git: Atomic commits with clear messages

DEFINITION OF DONE:
- Feature implemented and working
- Tests added and passing
- Code follows project rules
- PR created with clear description
- No warnings or errors
```

### 示例：实现用户认证

```markdown
CONTEXT:
Using Claude Reconstruction engineering system v5.2.0

TASK:
Implement JWT-based user authentication

FILES TO CREATE:
- src/auth/jwt.ts (JWT utilities)
- src/auth/middleware.ts (Auth middleware)
- src/routes/auth.ts (Auth routes)
- tests/auth/jwt.test.ts (Unit tests)

FILES TO MODIFY:
- src/app.ts (Register auth routes)
- src/types/user.ts (Add auth types)

WORKFLOW:
1. **Plan**:
   - Design JWT token structure
   - Plan middleware flow
   - Identify dependencies (jsonwebtoken, bcrypt)
2. **Confirm**: Present plan in commit message
3. **Execute**: Implement with tests
4. **Deliver**: PR with security review checklist

RULES:
- Follow rules/domain/security.md (Never log tokens)
- Follow rules/domain/coding.md (Error handling)
- Follow rules/domain/testing.md (Coverage > 80%)

DEFINITION OF DONE:
- Login/logout endpoints work
- JWT generation and validation
- Middleware protects routes
- 90%+ test coverage
- Security checklist completed
```

## 配置文件位置

```
~/.openclaw/workspace/
├── claude-Reconstruction/           # 工程化配置
│   ├── CLAUDE.md                   # 主配置
│   ├── CONTEXT_MANAGER.md          # 上下文管理
│   ├── rules/                      # 规则引擎
│   │   ├── core/                   # 核心规则
│   │   └── domain/                 # 领域规则
│   ├── capabilities/               # 能力定义
│   └── index/                      # 索引和路由
│
└── .clawdbot/                      # Agent Swarm 系统
    ├── config/
    │   ├── swarm-config.json       # Swarm 配置
    │   └── integration.json        # 集成配置 (新)
    └── scripts/
        ├── spawn-agent.sh          # Agent 生成
        └── spawn-with-config.sh    # 工程化 Agent (新)
```

## 集成配置

`.clawdbot/config/integration.json`:

```json
{
  "claudeReconstruction": {
    "enabled": true,
    "path": "~/.openclaw/workspace/claude-Reconstruction",
    "autoDetect": true,
    "features": {
      "contextManager": true,
      "workflowEngine": true,
      "rulesEngine": true,
      "hookLayer": true,
      "delegation": true
    }
  },
  "agentDefaults": {
    "useEngineering": true,
    "contextBudget": "20%",
    "workflowMode": "plan-confirm-execute",
    "qualityGates": true
  },
  "promptTemplates": {
    "engineering": ".clawdbot/templates/engineering.md",
    "standard": ".clawdbot/templates/standard.md"
  }
}
```

## 验证集成

```bash
# 1. 检查 Claude Reconstruction 是否存在
ls -la ~/.openclaw/workspace/claude-Reconstruction/

# 2. 验证 Claude CLI
claude --version

# 3. 测试集成
cd ~/.openclaw/workspace
./swarm spawn-with-config

# 4. 检查 agent 是否使用工程化配置
./swarm logs <task-id> | grep "Claude Reconstruction"
```

## 最佳实践

### 1. 使用 Context Manager

让 Claude 智能加载文档，而不是全部加载：

```bash
# Agent 会根据任务类型自动加载相关文档
Task: "Write Playwright test"
  → Loads: rules/core/ + capabilities/browser-automation
  → Context: 12%

Task: "Implement REST API"
  → Loads: rules/core/ + rules/domain/coding.md + capabilities/api-design
  → Context: 18%
```

### 2. 遵循 4步工作流程

```
Plan → Confirm → Execute → Deliver
```

不要跳过 Confirm 步骤，让编排层确认方案。

### 3. 使用专业 Sub-agents

```
Complex task → Delegate to Architect
Security review → Delegate to Security Specialist
Code review → Delegate to Code Reviewer
```

### 4. 质量门控

每个工具调用前后都有检查：
- PreToolUse: 检查参数是否合理
- PostToolUse: 检查结果是否符合规范
- Stop conditions: 检查是否应该停止

## 故障排查

### Claude Reconstruction 未生效

```bash
# 检查路径
echo $CLAUDE_CONFIG

# 手动指定
export CLAUDE_CONFIG=~/.openclaw/workspace/claude-Reconstruction
```

### Context 仍然过高

```bash
# 检查是否正确使用 Context Manager
cat ~/.openclaw/workspace/claude-Reconstruction/CONTEXT_MANAGER.md

# 确保 agent 使用了 context keywords
# 在 prompt 中明确指定任务类型
```

### Agent 不遵循规则

```bash
# 检查 rules 是否被加载
./swarm logs <task-id> | grep "rules"

# 在 prompt 中明确引用规则
# "Follow rules/domain/coding.md for code style"
```

## 更多资源

- Claude Reconstruction Docs: ~/.openclaw/workspace/claude-Reconstruction/README.md
- Agent Swarm Docs: ~/.openclaw/workspace/.clawdbot/README.md
- Prompt Templates: ~/.openclaw/workspace/.clawdbot/PROMPT_TEMPLATES.md
- Quick Start: ~/.openclaw/workspace/.clawdbot/QUICK_START.md

---

**🎉 集成完成！** 现在你的 Agent Swarm 系统可以利用 Claude Reconstruction 的工程化配置，生成更智能、更专业的 coding agents！
