# 🤖 Agent Swarm + Claude Reconstruction 系统总结

完整的 AI Agent 编排系统，结合工程化配置，实现专业级代码生产。

## 🏗️ 完整架构

```
┌─────────────────────────────────────────────────────────┐
│  你/OpenClaw (最高编排层)                                │
│  • 读取业务上下文 (MEMORY.md, meetings, etc.)           │
│  • 决定任务优先级和分配                                  │
│  • 监督整体进度                                          │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼ 生成 agents
┌─────────────────────────────────────────────────────────┐
│  Agent Swarm (编排层)                                    │
│  • 生成 agents (spawn/spawn-eng)                        │
│  • 监控进度 (Ralph Loop V2)                             │
│  • 自动重试 (失败分析 + prompt 改进)                     │
│  • Mid-task steering (中途干预)                         │
└──────────────┬──────────────────────────────────────────┘
               │ 使用工程化配置
               ▼
┌─────────────────────────────────────────────────────────┐
│  Claude Reconstruction (工程化配置层)                    │
│                                                          │
│  Layer 5: Context Manager                               │
│    • 智能加载文档 (只加载需要的)                         │
│    • 上下文使用率: 12-20% (vs 60%+)                     │
│                                                          │
│  Layer 4: Workflow Engine                               │
│    • Plan → Confirm → Execute → Deliver                │
│    • 强制流程，不跳步                                    │
│                                                          │
│  Layer 3: Rules Engine                                  │
│    • 编码规范 (coding.md)                               │
│    • 测试规范 (testing.md)                              │
│    • 安全规范 (security.md)                             │
│    • Git 规范 (git.md)                                  │
│                                                          │
│  Layer 2: Hook Layer                                    │
│    • PreToolUse: 验证参数                               │
│    • PostToolUse: 验证结果                              │
│    • Stop Conditions: 知道何时寻求帮助                   │
│                                                          │
│  Layer 1: Delegation Layer                              │
│    • Architect: 架构设计                                │
│    • Security: 安全审查                                 │
│    • Reviewer: 代码审查                                 │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼ 遵循规则和流程
┌─────────────────────────────────────────────────────────┐
│  Claude Code Agents (执行层)                            │
│  • 独立 worktree + tmux 会话                            │
│  • 遵循工程化规则                                        │
│  • 智能上下文管理                                        │
│  • 自动测试和 PR                                         │
│  • 高质量代码产出                                        │
└─────────────────────────────────────────────────────────┘
```

## 📁 完整目录结构

```
~/.openclaw/workspace/
│
├── swarm                                # 主 CLI 入口
│
├── .clawdbot/                          # Agent Swarm 系统
│   ├── README.md                       # 完整文档
│   ├── QUICK_START.md                  # 快速开始（基础）
│   ├── QUICK_START_ENGINEERING.md      # 快速开始（工程化）
│   ├── INTEGRATION.md                  # 集成文档
│   ├── PROMPT_TEMPLATES.md             # Prompt 模板库
│   │
│   ├── active-tasks.json               # 任务注册表
│   │
│   ├── config/
│   │   ├── swarm-config.json           # Swarm 配置
│   │   └── integration.json            # 集成配置
│   │
│   ├── scripts/
│   │   ├── spawn-agent.sh              # 基础 agent 生成
│   │   ├── spawn-with-config.sh        # 工程化 agent 生成
│   │   ├── check-agents.sh             # 监控系统 (Ralph Loop V2)
│   │   ├── run-code-review.sh          # 自动化代码审查
│   │   └── task-manager.sh             # 任务管理
│   │
│   ├── templates/
│   │   ├── engineering.md              # 工程化 prompt 模板
│   │   ├── standard.md                 # 标准 prompt 模板
│   │   └── ...                         # 其他模板
│   │
│   ├── logs/
│   │   ├── <task-id>.log               # 每个任务的日志
│   │   ├── monitor.log                 # 监控日志
│   │   └── cron.log                    # Cron 日志
│   │
│   └── setup.sh                        # 安装验证脚本
│
├── claude-Reconstruction/               # 工程化配置系统
│   ├── CLAUDE.md                       # 主配置
│   ├── CONTEXT_MANAGER.md              # 上下文管理器
│   ├── KNOWLEDGE_MAP.md                # 知识图谱
│   │
│   ├── rules/
│   │   ├── core/                       # 核心规则
│   │   │   ├── work-mode.md            # 工作模式
│   │   │   ├── blocking-rules.md       # 阻塞规则
│   │   │   └── immutability.md         # 不可变性
│   │   │
│   │   ├── domain/                     # 领域规则
│   │   │   ├── coding.md               # 编码规范
│   │   │   ├── testing.md              # 测试规范
│   │   │   ├── security.md             # 安全规范
│   │   │   └── git.md                  # Git 规范
│   │   │
│   │   ├── delegator/                  # 委托专家
│   │   │   ├── architect.md            # 架构师
│   │   │   ├── security.md             # 安全专家
│   │   │   └── reviewer.md             # 代码审查
│   │   │
│   │   └── hooks.md                    # Hook 层
│   │
│   ├── capabilities/                    # 能力定义
│   │   ├── browser-automation/         # 浏览器自动化
│   │   ├── api-design/                 # API 设计
│   │   └── frontend-frameworks/        # 前端框架
│   │
│   └── index/                          # 索引和路由
│       └── task-router.md              # 任务路由
│
└── worktrees/                          # Agent 工作区
    ├── feat-task-1/                    # Task 1 的独立工作区
    ├── feat-task-2/                    # Task 2 的独立工作区
    └── ...
```

## 🚀 完整命令参考

### 基础命令

```bash
# 查看帮助
./swarm help

# 查看状态
./swarm status

# 生成普通 agent
./swarm spawn

# 生成工程化 agent ⭐ (推荐)
./swarm spawn-eng
```

### 集成相关

```bash
# 检查集成状态
./swarm integration-status

# 设置集成（如果 Claude Reconstruction 未安装）
./swarm setup-integration

# 查看配置
./swarm config
cat .clawdbot/config/integration.json
```

### 任务管理

```bash
# 查看任务列表
./swarm status

# 查看任务日志
./swarm logs <task-id>

# 实时查看（连接 tmux）
./swarm attach <task-id>

# 中途干预 (steering)
./swarm steer <task-id> "Your message"

# 杀死任务
./swarm kill <task-id>

# 清理完成的任务
./swarm cleanup
```

### 监控和自动化

```bash
# 手动触发检查
./swarm check

# 安装 cron 自动监控（每10分钟）
./swarm install-cron

# 卸载 cron
./swarm uninstall-cron

# 查看 cron 日志
tail -f .clawdbot/logs/cron.log
```

## 🎯 使用场景

### 场景 1: 快速原型（普通 agent）

```bash
./swarm spawn

# 适合：
- 快速测试想法
- 简单的一次性任务
- 不需要严格规范的代码
```

### 场景 2: 生产级代码（工程化 agent）⭐

```bash
./swarm spawn-eng

# 适合：
- 生产环境的功能开发
- 需要遵循编码规范
- 需要高测试覆盖率
- 需要代码审查
- 团队协作项目
```

### 场景 3: 批量任务

```bash
# 从任务列表批量生成
for task in auth billing dashboard; do
  ./swarm spawn-eng <<EOF
feat-$task
api
Implement $task feature
EOF
done
```

### 场景 4: 紧急 Bug 修复

```bash
./swarm spawn-eng

# Task ID: hotfix-login-bug
# Task Type: security
# Description: Fix authentication bypass vulnerability
# 
# 工程化 agent 会：
# 1. 快速分析问题
# 2. 提出修复方案并确认
# 3. 实现修复 + 测试
# 4. 创建 PR 并触发安全审查
```

## 📊 性能对比

| 指标 | 普通 Agent | 工程化 Agent | 改进 |
|------|-----------|-------------|------|
| 上下文使用率 | 60%+ | 12-20% | **3x-5x** |
| 代码质量 | 不稳定 | 高且一致 | **显著提升** |
| 测试覆盖率 | 可能缺失 | 强制 >80% | **有保障** |
| 重试成功率 | 低（相同prompt） | 高（改进prompt） | **Ralph Loop V2** |
| 人工介入 | 频繁询问 | 最小化 | **Plan-Confirm** |
| PR 质量 | 需要大量审查 | 高质量检查清单 | **自动审查** |

## 🌟 核心优势

### 1. 智能上下文管理

**Before:**
```
120KB config 全部加载 → 60% context
只剩 40% 用于实际代码
```

**After:**
```
只加载需要的 23KB → 12% context
剩余 88% 用于实际代码
```

### 2. Ralph Loop V2 - 智能重试

**传统方式:**
```
失败 → 重复相同 prompt → 再次失败 → 放弃
```

**Ralph Loop V2:**
```
失败 → 分析原因 → 重写 prompt → 成功
- 上下文太多？ → 缩小范围
- 方向错误？ → 重新对齐
- 缺少信息？ → 补充上下文
```

### 3. 4步工作流程 - 专业行为

```
Plan     → 先思考再行动
Confirm  → 确认方案再实现
Execute  → 遵循规则实现
Deliver  → 高质量交付
```

不是 chatbot 的"边做边想"，而是 senior engineer 的"计划执行"。

### 4. 5层质量保证

```
Layer 5: Context Manager   → 只加载需要的
Layer 4: Workflow Engine   → 强制流程
Layer 3: Rules Engine      → 编码规范
Layer 2: Hook Layer        → 质量门控
Layer 1: Delegation Layer  → 专家系统
```

每一层都在保证代码质量。

## 🔄 典型工作流程示例

### 完整案例：实现用户认证功能

#### 1. 生成工程化 Agent

```bash
./swarm spawn-eng
```

```
Task ID: feat-user-auth
Task Type: security
Description: Implement JWT-based authentication with refresh tokens

Files to create:
src/auth/jwt.ts, src/auth/middleware.ts, src/routes/auth.ts, tests/auth/jwt.test.ts

Files to modify:
src/app.ts, src/types/user.ts

Constraints:
- Use bcrypt for passwords
- JWT secret from env
- Refresh token in HTTP-only cookie
```

#### 2. Agent 执行 Plan 阶段

```
[10:00] Agent 开始分析...
[10:01] [PLAN] Implement JWT authentication

Approach:
1. Create JWT utilities (sign/verify)
2. Add bcrypt password hashing
3. Create auth middleware
4. Add login/logout/refresh routes
5. Add comprehensive tests

Dependencies: jsonwebtoken, bcrypt
Tech decisions:
- JWT expiry: 15min (access), 7d (refresh)
- Token storage: localStorage (access), HTTP-only cookie (refresh)

Risks:
- Need to handle token rotation carefully
- Cookie security settings critical
```

#### 3. Agent 执行 Confirm 阶段

```
[10:02] Commit: [PLAN] ...
[10:02] Agent 等待确认...
```

**你查看并确认：**
```bash
./swarm logs feat-user-auth

# 如果需要调整：
./swarm steer feat-user-auth "Looks good, but use 30min expiry for access tokens"
```

#### 4. Agent 执行 Execute 阶段

```
[10:05] Creating src/auth/jwt.ts...
[10:06] Commit: feat(auth): Add JWT utilities
[10:08] Creating tests/auth/jwt.test.ts...
[10:10] Commit: test(auth): Add JWT tests (coverage: 95%)
[10:12] Creating src/auth/middleware.ts...
[10:14] Commit: feat(auth): Add auth middleware
[10:16] All tests passing ✓
```

#### 5. Agent 执行 Deliver 阶段

```
[10:18] Creating PR #342...

Title: feat: Implement JWT-based authentication

Description:
Implements JWT authentication with refresh tokens.

Changes:
- JWT sign/verify utilities
- Bcrypt password hashing
- Auth middleware for protected routes
- Login/logout/refresh endpoints
- Comprehensive test suite

Tests:
- Unit tests: 95% coverage
- Integration tests: All passing
- Security checklist: ✓

Ready for review!
```

#### 6. 自动化流程

```
[10:20] CI 开始运行...
[10:22] Lint: ✓
[10:23] TypeScript: ✓
[10:25] Tests: ✓ (95% coverage)
[10:27] Code review (Gemini): ✓ No critical issues
[10:30] Code review (Codex): ✓ LGTM
```

#### 7. 通知你

```
[10:30] Telegram: ✅ Task completed: feat-user-auth
        PR #342 is ready for review!
        All checks passed.
```

#### 8. 你只需要

```bash
# 查看 PR
gh pr view 342

# 快速审查（大部分工作已完成）
# - 代码质量：✓ (自动审查通过)
# - 测试覆盖率：✓ (95%)
# - 安全检查：✓ (checklist 完成)

# 合并
gh pr merge 342
```

**总耗时：30分钟（从想法到可合并的 PR）**

**你的实际工作量：5分钟（确认方案 + 最终审查）**

## 📚 学习路径

### 第1天：基础了解

```bash
# 1. 阅读文档
cat .clawdbot/README.md
cat .clawdbot/QUICK_START.md

# 2. 检查系统
./swarm integration-status

# 3. 生成第一个简单 agent
./swarm spawn
```

### 第2天：工程化 Agents

```bash
# 1. 阅读集成文档
cat .clawdbot/INTEGRATION.md
cat .clawdbot/QUICK_START_ENGINEERING.md

# 2. 了解 Claude Reconstruction
cat claude-Reconstruction/README.md

# 3. 生成第一个工程化 agent
./swarm spawn-eng
```

### 第3-7天：实践和优化

```bash
# 1. 尝试不同任务类型
./swarm spawn-eng  # api, frontend, testing, security

# 2. 学习 mid-task steering
./swarm steer <task-id> "..."

# 3. 自定义 prompt 模板
nano .clawdbot/templates/engineering.md

# 4. 优化配置
nano .clawdbot/config/integration.json
```

### 第2周+：高级应用

```bash
# 1. 批量任务
# 2. 复杂多步骤任务
# 3. 自定义规则
# 4. 主动任务发现（未来）
```

## 🎓 最佳实践

1. **任务类型很重要** - 正确的类型会自动加载正确的规则
2. **不要跳过 Confirm** - 让 agent 先展示计划
3. **使用 Mid-Task Steering** - 不要杀掉 agent，引导它
4. **详细的 Prompt** - 文件列表、约束、测试要求
5. **定期 Cleanup** - 清理完成的任务和 worktrees

## 🚧 已知限制

1. **WSL2 内存** - 并行 agents 需要大量内存
2. **GitHub CLI 必需** - PR 检查依赖 `gh`
3. **Cron 权限** - 某些系统需要手动设置
4. **Code Review** - Gemini review 脚本需要完善

## 🔮 未来计划

### Phase 2（下一步）
- [ ] 完善 Gemini code review 集成
- [ ] 更智能的 prompt 改进（使用 LLM 分析失败）
- [ ] 主动任务发现（扫描 git log, Sentry, etc.）
- [ ] Web Dashboard（可视化监控）

### Phase 3（未来）
- [ ] 多仓库支持
- [ ] 分布式 agents（云端运行）
- [ ] 自动 merge（高信心 PR）
- [ ] 学习系统（记忆成功模式）

## 📞 获取帮助

### 文档

```bash
# Agent Swarm
cat .clawdbot/README.md
cat .clawdbot/QUICK_START.md

# 工程化集成
cat .clawdbot/INTEGRATION.md
cat .clawdbot/QUICK_START_ENGINEERING.md

# Claude Reconstruction
cat claude-Reconstruction/README.md
cat claude-Reconstruction/CLAUDE.md
```

### 故障排查

```bash
# 1. 检查系统状态
./swarm integration-status

# 2. 查看日志
./swarm logs <task-id>
tail -f .clawdbot/logs/monitor.log

# 3. 验证配置
cat .clawdbot/config/integration.json

# 4. 重新运行设置
./.clawdbot/setup.sh
```

## 🎉 开始使用

```bash
cd ~/.openclaw/workspace

# 基础 agent
./swarm spawn

# 工程化 agent（推荐）
./swarm spawn-eng

# 查看帮助
./swarm help
```

---

**🏆 你现在拥有了：**

1. ✅ 完整的 Agent Swarm 编排系统
2. ✅ Claude Reconstruction 工程化集成
3. ✅ Ralph Loop V2 智能重试
4. ✅ 5层质量保证体系
5. ✅ 完整的文档和示例
6. ✅ 可直接使用的 CLI 工具

**准备好改变你的开发方式了吗？** 🚀

```bash
./swarm spawn-eng
```
