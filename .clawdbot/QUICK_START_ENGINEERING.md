# 🚀 Quick Start: Engineering Agents

使用 Claude Reconstruction 工程化配置生成专业的 coding agents。

## 为什么使用工程化配置？

**普通 Agent：**
- ❌ 上下文使用率：60%+
- ❌ 行为像 chatbot，频繁询问
- ❌ 代码质量不稳定

**工程化 Agent：**
- ✅ 上下文使用率：12-20%
- ✅ 行为像 senior engineer
- ✅ 遵循编码规范和最佳实践
- ✅ Plan → Confirm → Execute → Deliver 工作流程

## 5分钟快速开始

### Step 1: 检查集成状态

```bash
cd ~/.openclaw/workspace
./swarm integration-status
```

应该看到：
```
✓ Integration config exists
✓ Claude Reconstruction installed
✓ Claude CLI installed
```

如果有 ✗，运行：
```bash
./swarm setup-integration
```

### Step 2: 生成第一个工程化 Agent

```bash
./swarm spawn-eng
```

**示例输入：**
```
Task ID: feat-hello-api
Task Type: api
Description: Create a simple Hello World API endpoint
```

**Files to create:**
```
src/routes/hello.ts, tests/hello.test.ts
```

**Files to modify:**
```
src/app.ts
```

### Step 3: 观察 4步工作流程

工程化 agent 会遵循严格的工作流程：

#### 1️⃣ PLAN（规划）
Agent 会首先创建一个实现计划：
```
[PLAN] Create Hello World API endpoint

Approach:
- Create src/routes/hello.ts with GET /hello route
- Add handler that returns { message: "Hello, World!" }
- Register route in src/app.ts
- Add tests in tests/hello.test.ts

Dependencies: None (using existing Express)
Risks: None (simple endpoint)
```

#### 2️⃣ CONFIRM（确认）
Agent 会等待你确认计划。查看日志：
```bash
./swarm logs feat-hello-api
```

如果需要修改方向：
```bash
./swarm steer feat-hello-api "Plan looks good, but add input validation for query params"
```

#### 3️⃣ EXECUTE（执行）
Agent 开始实现，遵循工程化规则：
- 代码遵循 rules/domain/coding.md
- 测试遵循 rules/domain/testing.md
- Git commits 遵循 rules/domain/git.md

#### 4️⃣ DELIVER（交付）
Agent 创建 PR，包含：
- 清晰的描述
- 质量检查清单
- 测试覆盖率报告

### Step 4: 监控进度

```bash
# 查看状态
./swarm status

# 实时查看日志
./swarm logs feat-hello-api

# 连接到 agent 的 tmux 会话
./swarm attach feat-hello-api
# 按 Ctrl+B 然后 D 退出
```

### Step 5: 中途干预（如果需要）

如果 agent 走错方向：
```bash
./swarm steer feat-hello-api "Stop. Focus on the happy path first, handle errors later."
```

## 任务类型参考

选择正确的任务类型会自动加载相关规则：

| Task Type | 自动加载的规则 | 适用场景 |
|-----------|---------------|---------|
| `api` | coding.md + api-design | REST API, GraphQL endpoints |
| `frontend` | coding.md + frontend-frameworks | React/Vue components, UI |
| `testing` | testing.md + browser-automation | 单元测试、E2E 测试 |
| `security` | security.md + coding.md | Authentication, Authorization |
| `database` | coding.md + data-modeling | Migrations, queries |
| `coding` | coding.md | 通用编码任务 |

## 高级示例

### 复杂的后端功能

```bash
./swarm spawn-eng
```

```
Task ID: feat-user-auth
Task Type: security
Description: Implement JWT-based user authentication with refresh tokens

Files to create:
src/auth/jwt.ts, src/auth/middleware.ts, src/routes/auth.ts, tests/auth/jwt.test.ts

Files to modify:
src/app.ts, src/types/user.ts

Constraints:
- Must use bcrypt for password hashing
- JWT secret from environment variable
- Refresh token should be stored in HTTP-only cookie
```

### 前端组件开发

```bash
./swarm spawn-eng
```

```
Task ID: feat-dashboard-widget
Task Type: frontend
Description: Create a dashboard metrics widget showing user statistics

Files to create:
src/components/MetricsWidget.tsx, src/components/MetricCard.tsx, tests/MetricsWidget.test.tsx

Files to modify:
src/pages/Dashboard.tsx

Constraints:
- Must be responsive (mobile-first)
- Use existing design system
- Add loading and error states
```

### 测试开发

```bash
./swarm spawn-eng
```

```
Task ID: test-checkout-flow
Task Type: testing
Description: Add E2E tests for checkout flow using Playwright

Files to create:
tests/e2e/checkout.spec.ts

Constraints:
- Use Page Object Model pattern
- Test happy path and error cases
- Mock payment gateway
```

## 工程化规则说明

### Context Manager（自动加载）

根据任务类型，只加载需要的文档：
```
Task: "Write Playwright test"
  → 加载: rules/core/ + capabilities/browser-automation
  → 上下文: 12%

Task: "Implement REST API"
  → 加载: rules/core/ + rules/domain/coding.md + capabilities/api-design
  → 上下文: 19%
```

### Workflow Engine（强制流程）

```
1. Plan   → Agent 分析任务并创建计划
2. Confirm → Agent 展示计划等待确认
3. Execute → Agent 实现并遵循规则
4. Deliver → Agent 创建 PR 并完成
```

### Rules Engine（质量保证）

核心规则（总是加载）：
- **Immutability**: 避免修改现有数据结构
- **File Size**: 文件保持在 400 行以下
- **Error Handling**: 显式处理所有错误
- **Testing**: 所有新代码必须有测试（覆盖率 > 80%）

领域规则（按需加载）：
- **coding.md**: 代码风格、组织、命名
- **testing.md**: 测试标准、覆盖率
- **security.md**: 安全最佳实践
- **git.md**: Commit 规范、分支策略

### Hook Layer（质量门控）

每个工具调用前后都有检查：
- **PreToolUse**: 验证参数合理性
- **PostToolUse**: 验证结果符合规范
- **Stop Conditions**: 知道何时停止并寻求帮助

### Delegation Layer（专家系统）

复杂任务可以委托给专家：
- **Architect**: 架构设计决策
- **Security**: 安全审查
- **Reviewer**: 代码审查

## Prompt 最佳实践

### ✅ 好的 Prompt

```markdown
Task Type: api
Description: Implement user registration endpoint

FILES:
- src/routes/auth.ts (create)
- src/services/user.ts (create)
- tests/auth.test.ts (create)

REQUIREMENTS:
- Email validation
- Password strength check (min 8 chars, 1 uppercase, 1 number)
- Hash password with bcrypt
- Return JWT token on success

CONSTRAINTS:
- Don't implement login yet (separate task)
- Use existing User model
- Follow rules/domain/security.md

TESTS:
- Happy path (valid registration)
- Invalid email format
- Weak password
- Duplicate email
```

### ❌ 糟糕的 Prompt

```
Task Type: coding
Description: Add auth

(太模糊，没有具体要求)
```

## 故障排查

### Agent 没有遵循工作流程

检查 agent 是否正确加载了工程化配置：
```bash
./swarm logs <task-id> | grep "Claude Reconstruction"
```

如果没有，尝试重新生成：
```bash
./swarm kill <task-id>
./swarm spawn-eng  # 重新生成
```

### Context 仍然很高

确保在 prompt 中明确指定任务类型：
```
Task Type: api  # 这很重要！
```

Context Manager 根据任务类型智能加载。

### Agent 不询问确认

检查 workflow mode 是否正确：
```bash
cat ~/.openclaw/workspace/.clawdbot/config/integration.json | jq '.agentDefaults.workflowMode'
```

应该是：`"plan-confirm-execute-deliver"`

## 下一步

1. **尝试不同的任务类型**
   - api, frontend, testing, security

2. **学习规则系统**
   ```bash
   cat claude-Reconstruction/rules/domain/coding.md
   cat claude-Reconstruction/rules/domain/testing.md
   ```

3. **自定义 Prompt 模板**
   ```bash
   nano .clawdbot/templates/engineering.md
   ```

4. **配置集成**
   ```bash
   nano .clawdbot/config/integration.json
   ```

## 更多资源

- **Agent Swarm 文档**: `cat .clawdbot/README.md`
- **集成文档**: `cat .clawdbot/INTEGRATION.md`
- **Claude Reconstruction 文档**: `cat claude-Reconstruction/README.md`
- **Prompt 模板**: `cat .clawdbot/PROMPT_TEMPLATES.md`

---

**准备好了吗？**

```bash
./swarm spawn-eng
```

开始你的第一个工程化 agent！🚀
