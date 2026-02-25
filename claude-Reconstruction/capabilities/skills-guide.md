# Skills 使用指南

> **Skills**: 预定义的自动化任务和专业能力
> **版本**: v2.0 (2026-02-10 更新)
> **Skills 总数**: 41 (15 用户调用 + 26 自动激活)

---

## 概览

Skills 是 Claude Code 的扩展能力，提供：

1. **用户调用的 Skills** - 通过 `/command` 显式调用
2. **自动激活的 Skills** - 根据任务上下文自动激活

---

## 核心 Skills（用户调用 - 15个）

### Git 操作类

| Skill           | 命令           | 用途                                |
| --------------- | -------------- | ----------------------------------- |
| **commit**      | `/commit`      | 分析变更、生成 commit message、提交 |
| **create-pr**   | `/create-pr`   | 分析变更、生成 PR 描述、创建 PR     |
| **code-review** | `/code-review` | 多角度代码审查                      |
| **review-code** | `/review-code` | 代码审查（别名）                    |

#### `/commit` 使用示例

```
/commit

# 自动执行：
# 1. git status 查看变更
# 2. git diff 分析变更内容
# 3. 生成语义化 commit message
# 4. 等待用户确认
# 5. git commit
```

#### `/create-pr` 使用示例

```
/create-pr

# 自动执行：
# 1. 分析当前分支与 main 的差异
# 2. 查看所有 commits
# 3. 生成 PR 标题和描述
# 4. 创建 PR（使用 gh 命令）
```

### 代码质量类

| Skill                      | 命令                      | 用途               |
| -------------------------- | ------------------------- | ------------------ |
| **write-tests**            | `/write-tests`            | 自动生成测试用例   |
| **refactor**               | `/refactor`               | 代码重构建议和执行 |
| **add-comments**           | `/add-comments`           | 添加代码注释       |
| **explain-code**           | `/explain-code`           | 解释代码逻辑       |
| **add-feature**            | `/add-feature`            | 添加新功能         |
| **convert-to-typescript**  | `/convert-to-typescript`  | JS→TS 转换         |
| **optimize-performance**   | `/optimize-performance`   | 性能优化           |
| **generate-documentation** | `/generate-documentation` | 生成文档           |

### 调试类

| Skill             | 命令             | 用途             |
| ----------------- | ---------------- | ---------------- |
| **debug**         | `/debug`         | 调试当前问题     |
| **debug-issue**   | `/debug-issue`   | 定位问题（详细） |
| **fix-bug**       | `/fix-bug`       | 定位并修复 Bug   |
| **explain-issue** | `/explain-issue` | 解释错误根因     |

---

## 自动激活 Skills（26个）

这些 Skills 根据任务上下文自动激活，无需显式调用。

### UI/UX 设计

| Skill                        | 触发条件             | 能力                                    |
| ---------------------------- | -------------------- | --------------------------------------- |
| **ui-ux-pro-max**            | UI 设计、界面、样式  | 50 种设计风格、21 种配色、50 种字体搭配 |
| **frontend-design-official** | 前端组件、页面       | React/Vue/Svelte 代码生成               |
| **canvas-design**            | Canvas 图形、绘画    | Canvas API 图形设计                     |
| **theme-factory**            | 主题、配色、暗色模式 | 主题系统生成                            |
| **image-editor**             | 图片编辑、裁剪、滤镜 | 图片处理操作                            |
| **image-enhancer**           | 图片增强、优化       | 图片质量提升                            |

### 开发专家

| Skill                     | 触发条件           | 能力           |
| ------------------------- | ------------------ | -------------- |
| **backend-expert**        | 后端开发、API 设计 | 后端架构与实现 |
| **frontend-expert**       | 前端开发、组件设计 | 前端架构与实现 |
| **security-expert**       | 安全加固、漏洞修复 | 安全实现       |
| **security-audit-expert** | 安全审计、合规检查 | 安全审计报告   |
| **testing-expert**        | 测试策略、测试框架 | 测试方案设计   |
| **refactoring-expert**    | 大规模重构         | 重构策略与执行 |
| **documentation-expert**  | 技术文档编写       | 文档生成与维护 |
| **code-review-expert**    | 深度代码审查       | 多维度审查     |

### 浏览器自动化

| Skill              | 触发条件     | 能力                |
| ------------------ | ------------ | ------------------- |
| **webapp-testing** | Web 应用测试 | Playwright E2E 测试 |

### 内容创作

| Skill                       | 触发条件         | 能力                   |
| --------------------------- | ---------------- | ---------------------- |
| **content-research-writer** | 写作、内容创作   | 研究、写作、引用       |
| **nano-banana-pro**         | AI 图片生成      | 高质量图片生成指令     |
| **notebooklm**              | 笔记、知识管理   | 结构化笔记生成         |
| **artifacts-builder**       | 交互组件、可视化 | Artifacts 风格组件生成 |

### 专业工具

| Skill              | 触发条件            | 能力             |
| ------------------ | ------------------- | ---------------- |
| **mcp-builder**    | 创建 MCP Server     | MCP 开发指导     |
| **skill-creator**  | 创建 Skill          | Skill 开发指导   |
| **skill-share**    | 分享 Skill 到 Slack | Skill 分发与协作 |
| **file-organizer** | 文件整理、项目结构  | 目录结构优化     |
| **template-skill** | 模板创建            | 快速模板生成     |

### 分析类

| Skill                         | 触发条件       | 能力                   |
| ----------------------------- | -------------- | ---------------------- |
| **meeting-insights-analyzer** | 会议记录分析   | 行为模式分析、沟通洞察 |
| **developer-growth-analysis** | 开发者成长分析 | 技能评估与建议         |

---

## Skill 使用模式

### 模式 1: 直接调用

```
用户: /commit
Claude: [执行 commit skill]
```

### 模式 2: 自然语言触发

```
用户: 帮我设计一个登录页面
Claude: [自动激活 ui-ux-pro-max skill]
```

### 模式 3: 组合使用

```
用户: 实现用户认证功能，写测试，然后提交
Claude:
1. [实现功能代码]
2. [调用 /write-tests 生成测试]
3. [调用 /commit 提交代码]
```

---

## 常见 Skill 组合

### 功能开发流程

```
1. /add-feature 实现功能
   ↓
2. /write-tests 生成测试
   ↓
3. /code-review 审查代码
   ↓
4. /commit 提交代码
   ↓
5. /create-pr 创建 PR
```

### 调试流程

```
1. /explain-issue 理解错误
   ↓
2. /debug 定位问题
   ↓
3. /fix-bug 修复问题
   ↓
4. /write-tests 添加测试防止回归
```

### 代码质量流程

```
1. /code-review 审查现有代码
   ↓
2. /refactor 重构改进
   ↓
3. /optimize-performance 性能优化
   ↓
4. /add-comments 补充注释
```

---

## Skill 配置

Skills 存储在 `~/.claude/commands/` 和 `~/.claude/settings.json` 中：

```
~/.claude/commands/       # 用户自定义 commands
~/.claude/settings.json   # managed skills 配置
```

### 两种 Skill 来源

1. **Managed Skills** - 通过 Claude Code marketplace 安装，存储在 settings.json
2. **Custom Commands** - 手动创建的 .md 文件，放在 commands/ 目录

---

## 最佳实践

1. **优先使用内置 Skill** - 经过充分测试
2. **组合使用** - 利用 Skill 链完成复杂任务
3. **自定义扩展** - 根据项目需求创建专用 Skill
4. **注意上下文** - 自动激活的 Skill 会占用 context，复杂任务时注意控制
