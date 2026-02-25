# Claude Code 配置说明

## 已集成 claude-Reconstruction v5.2

### 配置位置
- **主配置**: `.claude/config.json`
- **规则库**: `claude-Reconstruction/`

### 工作模式（4步）
```
1️⃣ 收到任务 → TodoList 规划
2️⃣ 展示计划 → 用户确认
3️⃣ 执行到底 → 不问问题
4️⃣ 总结验收 → 交付成果
```

### 智能加载系统
- **API开发**: 自动加载 API设计、安全规则
- **前端开发**: 自动加载 UI规范、性能规则
- **测试开发**: 自动加载 测试策略、覆盖率要求
- **Git操作**: 自动加载 Commit规范、分支策略

### 启动Claude Code时加载配置

**方式1: 使用启动脚本**
```bash
~/.openclaw/workspace/start-claude-code.sh <任务类型>
```

**方式2: 手动启动**
```bash
cd ~/.openclaw/workspace
claude --config .claude/config.json
```

### 任务类型
- `api` - API开发
- `frontend` - 前端开发
- `testing` - 测试开发
- `security` - 安全功能
- `coding` - 通用编码

### 核心规则
1. **只在4种情况提问**: 缺凭证、多方案、需求矛盾、高风险
2. **其他自行决策**: 文件命名、代码风格、依赖版本等
3. **能力进化**: 每次对话自动识别可复用模式并内生化

### 更多信息
- 完整文档: `claude-Reconstruction/README.md`
- 快速开始: `claude-Reconstruction/QUICK_START.md`
- 知识图谱: `claude-Reconstruction/KNOWLEDGE_MAP.md`
