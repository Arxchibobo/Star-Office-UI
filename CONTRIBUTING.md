# 贡献指南

感谢你考虑为 OpenClaw Agent Swarm 做出贡献！

## 如何贡献

### 报告 Bug

在提交 bug 报告前，请：
1. 检查是否已有相同的 issue
2. 运行系统测试：`./.clawdbot/test-system.sh`
3. 收集相关日志：`./swarm logs <task-id>`

**Bug 报告应包含：**
- 系统环境（OS, Shell, 版本）
- 重现步骤
- 期望行为
- 实际行为
- 相关日志

### 提议功能

欢迎提议新功能！请：
1. 先开一个 issue 讨论
2. 说明使用场景
3. 描述期望的行为

### 提交 Pull Request

#### 1. Fork 仓库

```bash
# Fork 后克隆你的 fork
git clone https://github.com/YOUR-USERNAME/openclaw-arxchibo.git
cd openclaw-arxchibo
```

#### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

#### 3. 进行更改

- 遵循现有代码风格
- 添加必要的测试
- 更新相关文档

#### 4. 测试

```bash
# 运行系统测试
./.clawdbot/test-system.sh

# 手动测试你的更改
./swarm <your-changes>
```

#### 5. 提交

```bash
git add .
git commit -m "feat: add awesome feature"

# 提交信息格式：
# feat: 新功能
# fix: Bug 修复
# docs: 文档更新
# refactor: 代码重构
# test: 测试相关
# chore: 构建/工具相关
```

#### 6. 推送并创建 PR

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

## 开发指南

### 项目结构

```
.clawdbot/
├── scripts/        # Bash 脚本
├── config/         # JSON 配置
├── templates/      # Prompt 模板
└── *.md           # 文档
```

### 脚本规范

- 使用 `set -e` 错误时退出
- 添加详细注释
- 提供使用示例
- 处理错误情况

### 文档规范

- 使用清晰的标题结构
- 提供代码示例
- 包含实际用例
- 保持简洁明了

## 常见贡献方向

### 🎯 高优先级

- [ ] 改进 Gemini code review 集成
- [ ] 更智能的 prompt 改进算法
- [ ] Web Dashboard UI
- [ ] 更多任务类型支持

### 📚 文档

- [ ] 更多 prompt 模板
- [ ] 视频教程
- [ ] 常见问题解答
- [ ] 翻译（英文、中文等）

### 🔧 工具

- [ ] VS Code 扩展
- [ ] GitHub Actions 集成
- [ ] Docker 支持
- [ ] CI/CD 模板

## 代码审查标准

PR 会被审查以下方面：

- ✅ 功能正确性
- ✅ 代码质量
- ✅ 测试覆盖
- ✅ 文档完整性
- ✅ 向后兼容性

## 获取帮助

- 💬 [Discussions](https://github.com/Arxchibobo/openclaw-arxchibo/discussions)
- 🐛 [Issues](https://github.com/Arxchibobo/openclaw-arxchibo/issues)
- 📧 直接联系维护者

## 行为准则

- 尊重他人
- 保持专业
- 接受建设性批评
- 关注最佳结果

---

**感谢你的贡献！** 🎉
