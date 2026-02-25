# 工具索引 - Tools Index

> **用途**: 快速查找所有可用工具及其使用场景

---

## 🗂️ 工具分类

### 1️⃣ MCP Servers（外部数据访问）

### 2️⃣ Skills（自动化任务）

### 3️⃣ Plugins（自动激活）

### 4️⃣ CLI 工具

### 5️⃣ 内置工具

---

## 1️⃣ MCP Servers

> **用途**: 访问外部服务和数据源

### 浏览器自动化

| MCP               | 功能                       | 使用场景           | 文档                  |
| ----------------- | -------------------------- | ------------------ | --------------------- |
| **playwright** ⭐ | 浏览器操作、截图、网络拦截 | 对话中实时操作网页 | `browser-automation/` |

**命令示例**:

```typescript
// 导航到网页
mcp__plugin_playwright_playwright__browser_navigate({
  url: 'https://google.com',
});

// 截图
mcp__plugin_playwright_playwright__browser_take_screenshot({
  filename: 'screenshot.png',
});

// 快照（accessibility tree）
mcp__plugin_playwright_playwright__browser_snapshot();
```

---

### 数据库

| MCP          | 功能                 | 使用场景             | 文档             |
| ------------ | -------------------- | -------------------- | ---------------- |
| **bytebase** | MySQL 查询、对象搜索 | SQL 查询、数据库管理 | `mcp-servers.md` |

**命令示例**:

```typescript
// 执行 SQL
mcp__mcphub__bytebase - execute_sql({ sql: 'SELECT * FROM users LIMIT 10' });

// 搜索数据库对象
mcp__mcphub__bytebase -
  search_objects({
    object_type: 'table',
    pattern: 'user%',
  });
```

---

### 监控日志

| MCP           | 功能                 | 使用场景             | 文档             |
| ------------- | -------------------- | -------------------- | ---------------- |
| **honeycomb** | 时序查询、分布式追踪 | APM 监控、性能分析   | `mcp-servers.md` |
| **guance**    | 观测云 DQL 查询      | 日志、指标、链路分析 | `mcp-servers.md` |

**命令示例**:

```typescript
// Honeycomb 查询
mcp__mcphub__honeycomb -
  run_query({
    environment_slug: 'production',
    dataset_slug: 'api',
    query_spec: {
      calculations: [{ op: 'COUNT' }],
      time_range: '24h',
    },
  });

// 观测云查询
mcp__mcphub__guance -
  query_metric_data({
    dql: 'M::cpu:(avg(`load5s`))',
    time_delta: 300000,
  });
```

---

### 图表生成

| MCP       | 功能         | 使用场景   | 文档             |
| --------- | ------------ | ---------- | ---------------- |
| **chart** | 生成图表图片 | 数据可视化 | `mcp-servers.md` |

---

### Google 服务

| MCP          | 功能                   | 使用场景              | 文档     |
| ------------ | ---------------------- | --------------------- | -------- |
| **stitch**   | 项目/屏幕管理、AI 生成 | Google Stitch UI 设计 | MCP 文档 |
| **firebase** | Firebase 项目管理      | Firebase 开发         | MCP 文档 |

**完整 MCP 列表**: `capabilities/mcp-servers.md`

---

## 2️⃣ Skills（自动化任务）

> **用途**: 使用 `/skill-name` 或 `Skill` tool 调用

### Git & 代码工作流

| Skill            | 触发方式       | 功能              | 文档              |
| ---------------- | -------------- | ----------------- | ----------------- |
| **/commit**      | `/commit`      | 生成 Git 提交     | `skills-guide.md` |
| **/create-pr**   | `/create-pr`   | 创建 Pull Request | 同上              |
| **/code-review** | `/code-review` | 代码审查          | 同上              |
| **/write-tests** | `/write-tests` | 生成测试          | 同上              |
| **/refactor**    | `/refactor`    | 重构代码          | 同上              |
| **/debug**       | `/debug`       | 调试问题          | 同上              |

**使用示例**:

```bash
# 在对话中直接输入
/commit

# 或使用 Skill tool
Skill({ skill: "commit" })
```

---

### 浏览器自动化

| Skill              | 触发方式         | 功能                  | 文档                  |
| ------------------ | ---------------- | --------------------- | --------------------- |
| **agent-browser**  | `/agent-browser` | AI 驱动的浏览器自动化 | `browser-automation/` |
| **webapp-testing** | 描述需求         | Web 应用测试          | `skills-guide.md`     |

**使用场景**:

- 批量操作（>50次）
- 脚本化任务
- 定时执行

---

### UI/UX 设计

| Skill                       | 触发方式 | 功能              | 文档                       |
| --------------------------- | -------- | ----------------- | -------------------------- |
| **ui-ux-pro-max**           | 描述需求 | 智能 UI/UX 设计   | `DESIGN_MASTER_PERSONA.md` |
| **frontend-design-offical** | 描述需求 | 前端设计系统      | `skills-guide.md`          |
| **canvas-design**           | 描述需求 | Canvas 可视化设计 | 同上                       |
| **theme-factory**           | 描述需求 | 样式工具包        | 同上                       |

---

### 营销内容（24个）

| 类别     | Skills                                              | 文档                        |
| -------- | --------------------------------------------------- | --------------------------- |
| **文案** | copywriting, email-sequence                         | `MARKETING_SKILLS_GUIDE.md` |
| **SEO**  | seo-audit, schema-markup, seo-content-writer        | 同上                        |
| **CRO**  | page-cro, signup-flow-cro, popup-cro                | 同上                        |
| **策略** | pricing-strategy, launch-strategy, referral-program | 同上                        |
| **广告** | paid-ads, ab-test-setup, analytics-tracking         | 同上                        |

**完整列表**: `capabilities/MARKETING_SKILLS_GUIDE.md`

---

### 数据分析（8个）

| Skill          | 功能                | 位置                             |
| -------------- | ------------------- | -------------------------------- |
| Bot 毛利率分析 | 分析 Bot 收入和成本 | `bo-skill-research/shane-skill/` |
| 成本趋势分析   | 每日成本趋势        | 同上                             |
| 收入分析       | 收入归因分析        | 同上                             |
| 等等...        | 8个数据分析 Skills  | 同上                             |

---

### 创意工具

| Skill                      | 功能                                       | 文档                  |
| -------------------------- | ------------------------------------------ | --------------------- |
| **nano-banana-pro**        | AI 图片生成/编辑                           | `skills-guide.md`     |
| **visual-prompt-engineer** | Prompt 工程（Midjourney/Stable Diffusion） | 同上                  |
| **processing-creative**    | Processing 创意编程                        | `PROCESSING_SKILL.md` |
| **image-editor**           | 图片编辑                                   | `skills-guide.md`     |
| **image-enhancer**         | 图片增强                                   | 同上                  |

---

### 研究与写作

| Skill                       | 功能              | 文档              |
| --------------------------- | ----------------- | ----------------- |
| **deep-research**           | 深度研究（7阶段） | `skills-guide.md` |
| **literature-review**       | 文献综述          | 同上              |
| **citation-validator**      | 引用验证          | 同上              |
| **synthesizer**             | 综合研究发现      | 同上              |
| **content-research-writer** | 研究型写作        | 同上              |

---

### 其他 Skills（40+个）

**完整清单**: `capabilities/skills-guide.md`（81个Skills）

---

## 3️⃣ Plugins（自动激活）

> **用途**: 描述需求时自动激活，无需手动调用

### 开发类

| Plugin                          | 自动激活场景       | 能力                         |
| ------------------------------- | ------------------ | ---------------------------- |
| **backend-development**         | 后端开发、API 设计 | 架构、REST/GraphQL、微服务   |
| **frontend-mobile-development** | 前端/移动开发      | React、Next.js、React Native |
| **code-documentation**          | 文档生成           | API 文档、架构图、教程       |
| **tdd-workflows**               | TDD 工作流         | 测试驱动开发                 |

### 审查类

| Plugin                   | 自动激活场景 | 能力             |
| ------------------------ | ------------ | ---------------- |
| **code-review-ai**       | 代码审查     | 质量、安全、性能 |
| **security-scanning**    | 安全扫描     | OWASP、漏洞检测  |
| **comprehensive-review** | 全面审查     | 架构+代码+安全   |

### 基础设施类

| Plugin                    | 自动激活场景 | 能力                      |
| ------------------------- | ------------ | ------------------------- |
| **cloud-infrastructure**  | 云基础设施   | AWS/Azure/GCP、Terraform  |
| **kubernetes-operations** | K8s 操作     | GitOps、Helm、安全        |
| **cicd-automation**       | CI/CD 自动化 | GitHub Actions、GitLab CI |

### 数据类

| Plugin                   | 自动激活场景 | 能力                 |
| ------------------------ | ------------ | -------------------- |
| **data-engineering**     | 数据工程     | Spark、dbt、Airflow  |
| **database-design**      | 数据库设计   | 架构、优化、迁移     |
| **machine-learning-ops** | MLOps        | 模型训练、部署、监控 |

**完整列表**: 查看 System Reminder 中的 Plugin 清单

---

## 4️⃣ CLI 工具

> **用途**: 通过 Bash tool 调用的命令行工具

### 浏览器自动化

| CLI                  | 用途                  | 优势             | 文档                  |
| -------------------- | --------------------- | ---------------- | --------------------- |
| **agent-browser** 🚀 | AI 驱动的浏览器自动化 | 批量操作、脚本化 | `browser-automation/` |

**使用示例**:

```bash
# AI Agent 模式
agent-browser "打开 Google 并搜索 Anthropic"

# 脚本模式
agent-browser --script automation.js
```

---

### Git

| CLI    | 用途       | 文档                  |
| ------ | ---------- | --------------------- |
| **gh** | GitHub CLI | `rules/domain/git.md` |

**使用示例**:

```bash
# 查看 PR
gh pr view 123

# 创建 PR
gh pr create --title "Fix bug" --body "..."

# 查看 issue
gh issue view 456
```

---

### Node.js / 包管理

| CLI      | 用途           | 文档                                    |
| -------- | -------------- | --------------------------------------- |
| **npm**  | Node.js 包管理 | -                                       |
| **pnpm** | 快速包管理     | -                                       |
| **yarn** | 包管理         | -                                       |
| **uv**   | Python 包管理  | `python-development/uv-package-manager` |

---

### 数据库

| CLI       | 用途              | 文档 |
| --------- | ----------------- | ---- |
| **psql**  | PostgreSQL 客户端 | -    |
| **mysql** | MySQL 客户端      | -    |

---

## 5️⃣ 内置工具（Claude Code）

> **用途**: Claude Code 提供的核心工具

### 文件操作

| Tool      | 用途     | 使用场景             |
| --------- | -------- | -------------------- |
| **Read**  | 读取文件 | 查看代码、配置、文档 |
| **Write** | 写入文件 | 创建新文件           |
| **Edit**  | 编辑文件 | 修改现有文件         |
| **Glob**  | 文件匹配 | 按模式查找文件       |
| **Grep**  | 内容搜索 | 搜索代码内容         |

### 执行

| Tool     | 用途       | 使用场景             |
| -------- | ---------- | -------------------- |
| **Bash** | 执行命令   | Git、npm、测试等     |
| **Task** | 启动 Agent | 复杂任务、多步骤任务 |

### 任务管理

| Tool           | 用途     | 使用场景 |
| -------------- | -------- | -------- |
| **TaskCreate** | 创建任务 | 规划工作 |
| **TaskUpdate** | 更新任务 | 标记进度 |
| **TaskList**   | 列出任务 | 查看进度 |

### 用户交互

| Tool                | 用途     | 使用场景     |
| ------------------- | -------- | ------------ |
| **AskUserQuestion** | 询问用户 | 需要用户决策 |

---

## 🎯 按任务选择工具

### 浏览器自动化

```
实时操作（对话中）→ Playwright MCP ⭐
批量操作（>50次）→ agent-browser CLI 🚀
脚本化任务 → agent-browser CLI 🚀
```

### 数据查询

```
MySQL → bytebase MCP
PostgreSQL → psql CLI
监控数据 → honeycomb/guance MCP
```

### 代码工作流

```
提交代码 → /commit Skill
创建 PR → /create-pr Skill
代码审查 → /code-review Skill
测试 → /write-tests Skill
```

### 视频创作

```
现成模板 → Remotion Templates
自定义生成 → Remotion + Processing
背景特效 → Processing Creative Skill
```

### UI 设计

```
智能设计 → ui-ux-pro-max Skill
风格选择 → 30种风格库
组件库 → theme-factory Skill
```

---

## 📚 工具决策树

```
我想做 [任务]
  ↓
查看 task-router.md (30秒)
  ↓
找到推荐工具
  ↓
查看工具详细文档
  ↓
开始使用
```

**快速导航**: `index/task-router.md`

---

## 🔍 工具搜索

### 按功能搜索

| 功能       | 推荐工具                       | 类型      |
| ---------- | ------------------------------ | --------- |
| 网页自动化 | Playwright MCP / agent-browser | MCP / CLI |
| SQL 查询   | bytebase MCP                   | MCP       |
| 代码提交   | /commit                        | Skill     |
| UI 设计    | ui-ux-pro-max                  | Skill     |
| 图表生成   | chart MCP                      | MCP       |
| 浏览器测试 | webapp-testing                 | Skill     |

### 按类型搜索

| 类型            | 工具数量 | 文档                           |
| --------------- | -------- | ------------------------------ |
| **MCP Servers** | 12+      | `capabilities/mcp-servers.md`  |
| **Skills**      | 81+      | `capabilities/skills-guide.md` |
| **Plugins**     | 50+      | System Reminder                |
| **CLI 工具**    | 10+      | 本文档                         |

---

## 💡 工具组合（常见场景）

### 数据可视化完整流程

```
1. bytebase MCP → 查询数据
2. chart MCP → 生成图表
3. Remotion → 制作视频
```

### 浏览器自动化 + 数据分析

```
1. agent-browser CLI → 批量抓取数据
2. bytebase MCP → 存入数据库
3. honeycomb MCP → 监控执行
```

### 完整 Web 开发流程

```
1. ui-ux-pro-max → 设计 UI
2. 编写代码 → frontend-development Plugin
3. /write-tests → 测试
4. /code-review → 审查
5. /commit → 提交
6. /create-pr → PR
```

---

## 🆚 工具对比

### Playwright MCP vs agent-browser CLI

| 特性         | Playwright MCP ⭐ | agent-browser CLI 🚀 |
| ------------ | ----------------- | -------------------- |
| **交互性**   | 实时对话中操作    | 批量/脚本化          |
| **适合场景** | 探索、测试、录制  | 大规模自动化         |
| **速度**     | 实时反馈          | 批量处理更快         |
| **复杂度**   | 简单（对话）      | 中等（需脚本）       |

**建议**: 实时操作用 Playwright，批量任务用 agent-browser

---

## 📖 详细文档

### 核心工具文档

- `capabilities/browser-automation/decision-tree.md` - 浏览器自动化
- `capabilities/mcp-servers.md` - MCP Servers 完整列表
- `capabilities/skills-guide.md` - 81个 Skills 详解
- `capabilities/MARKETING_SKILLS_GUIDE.md` - 24个营销 Skills

### 快速索引

- `index/task-router.md` - 任务路由（30秒找工具）
- `index/capabilities-index.md` - 能力索引
- `index/error-patterns-index.md` - 错误模式索引

---

**版本**: v1.0
**更新**: 2026-02-05
**工具总数**: 150+ 工具（12+ MCP, 81+ Skills, 50+ Plugins, 10+ CLI）
