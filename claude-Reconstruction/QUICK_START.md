# 快速开始 (5 分钟)

> 让 Claude Code 从聊天机器人升级成高级工程师 🚀

---

## ⚡ 一键安装

### 方式 1: Node.js (推荐，跨平台)

```bash
git clone https://github.com/Arxchibobo/claude-Reconstruction.git
cd claude-reconstruction
pnpm install
pnpm install:config
```

### 方式 2: Bash 脚本 (Linux/macOS)

```bash
./scripts/install.sh
```

### 方式 3: PowerShell (Windows)

```powershell
.\scripts\install.ps1
```

**安装完成后会自动备份并复制配置到 `~/.claude/` 目录。**

---

## ✅ 验证安装

```bash
pnpm verify
```

**预期输出**：
```
✓ CLAUDE.md (entry point)
✓ CONTEXT_MANAGER.md (smart loading)
✓ rules/core/ directory
✓ rules/domain/ directory
✓ capabilities/ directory
✓ errors/ directory
```

---

## 🎯 第一个任务

安装成功后，在 Claude Code 中尝试：

### 示例 1: 浏览器自动化

```
帮我用 Playwright 写一个脚本，自动打开百度搜索"Claude Code"
```

**系统会自动**：
- 识别任务类型（browser-automation）
- 加载相关文档（~23KB，仅 12% context）
- 执行任务并生成代码

### 示例 2: 创建 Remotion 视频

```
创建一个 30 秒的产品介绍视频，我们的产品是 AI 写作工具
```

**系统会自动**：
- 匹配 Remotion 模板
- 生成完整的视频项目代码
- 提供渲染命令

### 示例 3: Git 工作流

```
/commit
```

**系统会自动**：
- 分析 git 变更
- 生成符合规范的 commit message
- 创建提交

---

## 📚 核心概念（5 个关键点）

### 1️⃣ **智能 Context 加载**

**问题**: 传统配置加载全部文档（~120KB），占用 60% context
**解决**: 智能识别任务类型，只加载需要的文档（~27KB），仅占 15%

```
你说 "写一个 Playwright 测试"
  ↓
系统识别: browser-automation
  ↓
只加载: rules/core/ + capabilities/browser-automation/
  ↓
剩余 85% context 用于实际工作 ✨
```

### 2️⃣ **四步工作模式**

```
1️⃣ 收到任务 → 创建 TodoList 规划
2️⃣ 展示计划 → 等待用户确认
3️⃣ 执行到底 → 自行决策（不频繁提问）
4️⃣ 总结验收 → 交付成果
```

**关键**: 只在 4 种致命阻塞时提问（缺少凭证、对立方案、需求矛盾、不可逆高风险）

### 3️⃣ **五层架构**

```
Layer 5: Context Manager    → 决定加载什么
Layer 4: Workflow Engine     → 如何工作
Layer 3: Rules Engine        → 遵循什么规则
Layer 2: Hook Layer          → 质量门控
Layer 1: Delegation Layer    → 专家路由
```

### 4️⃣ **能力生态**

- **41 个 Skills** - 自动化任务（/commit, /review-pr, ui-ux-pro-max）
- **80 个 Plugins** - 专业工作流
- **15 个 Error 模式** - 常见错误和解决方案
- **7 种工程化工作流** - 真实踩坑经验

### 5️⃣ **能力进化模式** (v5.2 新增)

每次对话自动激活：
- 识别可复用模式 → 抽象为能力轮廓 → 内生化到决策层
- 通过**更快、更稳、更少步骤**证明进化效果
- 用结果说话，不汇报过程

---

## 🗺️ 下一步

### 新手推荐路径

1. **了解核心概念** → 阅读 `CLAUDE.md`（5 分钟）
2. **探索能力库** → 查看 `index/task-router.md`（30 秒找工具）
3. **尝试第一个任务** → 上面的示例任务
4. **遇到问题？** → 查看 `errors/top-5-errors.md`

### 进阶路径

1. **工程化实践** → 阅读 `rules/domain/engineering-workflows.md`
2. **自定义 Hooks** → 配置 `rules/hooks.md`
3. **错误模式库** → 研究 `errors/ERROR_CATALOG.md`（15 种错误）
4. **设计系统** → 探索 `design/DESIGN_MASTER_PERSONA.md`

### 完整文档导航

| 类型 | 文档 | 用途 |
|------|------|------|
| **快速查找** | `index/task-router.md` | 30 秒找到需要的工具 |
| **核心规则** | `rules/core/` | 工作模式、阻塞规则、能力进化 |
| **领域规则** | `rules/domain/` | 编码、测试、安全、Git |
| **能力库** | `capabilities/` | 浏览器自动化、视频创作、营销 |
| **错误库** | `errors/` | 15 种错误模式 + 解决方案 |
| **设计指南** | `design/` | UI 设计风格参考 |

---

## 🆘 常见问题

### Q1: 安装后 Claude 没有变化？

**A**: 需要**重启 Claude Code** 或开始一个新对话，系统会自动加载配置。

### Q2: 如何验证系统是否生效？

**A**: 在新对话中说"帮我写一个 Playwright 测试"，如果 Claude 快速给出结果且没有加载大量文档，说明系统已生效。

### Q3: Context 使用率如何查看？

**A**: 在 Claude Code 中，输入的提示和加载的文档大小会影响 Context。v5.2 系统将全局规则从 120KB 降到 27KB，为实际任务留出 85% 空间。

### Q4: 可以自定义配置吗？

**A**: 可以！配置位于 `~/.claude/` 目录，你可以：
- 修改 `CLAUDE.md` 添加项目特定规则
- 编辑 `rules/domain/*.md` 自定义编码规范
- 配置 `rules/hooks.md` 添加自动化 Hooks

### Q5: 如何升级到新版本？

**A**:
```bash
cd claude-reconstruction
git pull origin main
pnpm install:config  # 会自动备份旧配置
```

### Q6: 遇到错误怎么办？

**A**:
1. 先查看 `errors/top-5-errors.md`（90% 的问题都在这里）
2. 再查看 `errors/ERROR_CATALOG.md`（完整错误库）
3. 仍未解决？提交 GitHub Issue

---

## 🎉 成功标志

系统正确运行的 3 个标志：

✅ **响应更快** - Claude 不再加载大量无关文档
✅ **更少提问** - Claude 自行决策 95% 的问题
✅ **任务完成质量高** - 代码符合最佳实践，自动执行测试

---

## 📞 获取帮助

- 📖 **完整文档**: [README.md](README.md)
- 🐛 **报告问题**: [GitHub Issues](https://github.com/Arxchibobo/claude-Reconstruction/issues)
- 💬 **讨论交流**: [GitHub Discussions](https://github.com/Arxchibobo/claude-Reconstruction/discussions)
- 📝 **贡献指南**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**版本**: v5.2.0
**更新日期**: 2026-02-22
**预计阅读时间**: 5 分钟
