# 知识图谱 (Knowledge Map)

> 文档之间的关系可视化，帮助你快速找到需要的信息

---

## 🗺️ 核心文档关系图

```mermaid
graph TD
    A[CLAUDE.md<br/>核心入口] --> B[CONTEXT_MANAGER.md<br/>智能加载]
    A --> C[rules/core/<br/>核心规则]
    A --> D[rules/domain/<br/>领域规则]
    A --> E[capabilities/<br/>能力库]
    A --> F[errors/<br/>错误库]

    C --> C1[work-mode.md<br/>工作模式]
    C --> C2[blocking-rules.md<br/>阻塞规则]
    C --> C3[capability-evolution.md<br/>能力进化]

    D --> D1[coding.md<br/>编码规范]
    D --> D2[testing.md<br/>测试要求]
    D --> D3[security.md<br/>安全规范]
    D --> D4[git.md<br/>Git工作流]
    D --> D5[engineering-workflows.md<br/>工程化流程]

    E --> E1[browser-automation/<br/>浏览器自动化]
    E --> E2[skills-guide.md<br/>Skills指南]
    E --> E3[plugins-auto.md<br/>Plugins指南]
    E --> E4[mcp-servers.md<br/>MCP服务器]

    F --> F1[top-5-errors.md<br/>Top 5错误]
    F --> F2[ERROR_CATALOG.md<br/>完整错误目录]

    style A fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style B fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style C fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style D fill:#9C27B0,stroke:#6A1B9A,stroke-width:2px,color:#fff
    style E fill:#00BCD4,stroke:#006064,stroke-width:2px,color:#fff
    style F fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
```

---

## 📚 文档层次结构

```mermaid
graph LR
    subgraph "Layer 0: 入口"
        L0A[CLAUDE.md]
        L0B[README.md]
        L0C[QUICK_START.md]
    end

    subgraph "Layer 1: 索引"
        L1A[index/task-router.md]
        L1B[index/capabilities-index.md]
        L1C[index/tools-index.md]
    end

    subgraph "Layer 2: 规则"
        L2A[rules/core/*]
        L2B[rules/domain/*]
        L2C[rules/agents.md]
        L2D[rules/hooks.md]
    end

    subgraph "Layer 3: 能力"
        L3A[capabilities/*]
        L3B[design/*]
        L3C[vibe-marketing/*]
    end

    subgraph "Layer 4: 参考"
        L4A[errors/*]
        L4B[examples/*]
    end

    L0A --> L1A
    L0A --> L2A
    L1A --> L3A
    L2A --> L3A
    L3A --> L4A

    style L0A fill:#4CAF50,color:#fff
    style L1A fill:#2196F3,color:#fff
    style L2A fill:#FF9800,color:#fff
    style L3A fill:#9C27B0,color:#fff
    style L4A fill:#F44336,color:#fff
```

---

## 🔍 任务路由流程图

```mermaid
flowchart TD
    START([用户输入任务]) --> DETECT{识别任务类型}

    DETECT -->|浏览器、自动化| BROWSER[capabilities/browser-automation/]
    DETECT -->|视频、Remotion| VIDEO[capabilities/video-creation/]
    DETECT -->|数据、分析、SQL| DATA[capabilities/data-analysis/]
    DETECT -->|设计、UI| DESIGN[design/DESIGN_MASTER_PERSONA.md]
    DETECT -->|营销、文案| MARKETING[vibe-marketing/]
    DETECT -->|开发、代码| CODING[rules/domain/coding.md]
    DETECT -->|测试、TDD| TESTING[rules/domain/testing.md]
    DETECT -->|安全、漏洞| SECURITY[rules/domain/security.md]
    DETECT -->|Git、提交| GIT[rules/domain/git.md]
    DETECT -->|错误、调试| ERROR[errors/ERROR_CATALOG.md]

    BROWSER --> LOAD[加载相关文档<br/>~15KB]
    VIDEO --> LOAD
    DATA --> LOAD
    DESIGN --> LOAD
    MARKETING --> LOAD
    CODING --> LOAD
    TESTING --> LOAD
    SECURITY --> LOAD
    GIT --> LOAD
    ERROR --> LOAD

    LOAD --> EXECUTE[执行任务<br/>85% context可用]

    style START fill:#4CAF50,color:#fff
    style DETECT fill:#2196F3,color:#fff
    style LOAD fill:#FF9800,color:#fff
    style EXECUTE fill:#9C27B0,color:#fff
```

---

## 🧬 能力进化流程图

```mermaid
flowchart TD
    START([每次对话开始]) --> ACTIVATE[激活能力进化模式]

    ACTIVATE --> IDENTIFY[识别可复用模式]

    IDENTIFY --> CHECK{是否可抽象?}
    CHECK -->|是| ABSTRACT[抽象为能力轮廓]
    CHECK -->|否| CONTINUE[继续执行]

    ABSTRACT --> INTERNALIZE[内生化到决策层]

    INTERNALIZE --> VERIFY{效果验证}
    VERIFY -->|更快/更稳/更少步骤| SUCCESS[能力进化成功]
    VERIFY -->|无改善| REFINE[继续优化]

    SUCCESS --> MERGE{是否可合并?}
    MERGE -->|是| COMBINE[合并为高层能力]
    MERGE -->|否| STORE[存储能力库]

    COMBINE --> STORE
    REFINE --> ABSTRACT

    STORE --> CONTINUE
    CONTINUE --> NEXT([下次对话自动应用])

    style START fill:#4CAF50,color:#fff
    style ACTIVATE fill:#2196F3,color:#fff
    style ABSTRACT fill:#FF9800,color:#fff
    style SUCCESS fill:#9C27B0,color:#fff
    style NEXT fill:#00BCD4,color:#fff
```

---

## 🔧 工程化工作流触发矩阵

```mermaid
flowchart TD
    TASK([收到任务]) --> TYPE{任务类型}

    TYPE -->|UI修改| UI[验证闭环工作流]
    TYPE -->|新功能| FEATURE[结构化规划 + TDD]
    TYPE -->|数据库变更| DB[事务化迁移]
    TYPE -->|核心组件| COMPONENT[自愈合模式]
    TYPE -->|3D可视化| 3D[截图验证 + 布局算法]
    TYPE -->|大规模数据| DATA[分批 + 去重 + 懒加载]
    TYPE -->|多文件重构| REFACTOR[TDD全流程]

    UI --> CHECK1{验证通过?}
    FEATURE --> CHECK2{测试通过?}
    DB --> CHECK3{数据一致?}
    COMPONENT --> CHECK4{回归测试?}
    3D --> CHECK5{视觉正确?}
    DATA --> CHECK6{性能OK?}
    REFACTOR --> CHECK7{覆盖率>80%?}

    CHECK1 -->|是| DONE([完成])
    CHECK1 -->|否| FIX1[修复问题]
    FIX1 --> UI

    CHECK2 -->|是| DONE
    CHECK2 -->|否| FIX2[修复问题]
    FIX2 --> FEATURE

    CHECK3 -->|是| DONE
    CHECK3 -->|否| ROLLBACK[回滚]
    ROLLBACK --> DB

    CHECK4 -->|是| DONE
    CHECK4 -->|否| FIX4[修复问题]
    FIX4 --> COMPONENT

    CHECK5 -->|是| DONE
    CHECK5 -->|否| FIX5[调整布局]
    FIX5 --> 3D

    CHECK6 -->|是| DONE
    CHECK6 -->|否| FIX6[优化查询]
    FIX6 --> DATA

    CHECK7 -->|是| DONE
    CHECK7 -->|否| FIX7[补充测试]
    FIX7 --> REFACTOR

    style TASK fill:#4CAF50,color:#fff
    style DONE fill:#9C27B0,color:#fff
```

---

## 📖 文档依赖关系

### 核心文档依赖

| 文档 | 依赖文档 | 被依赖次数 |
|------|---------|----------|
| **CLAUDE.md** | 所有其他文档 | 0（入口） |
| **CONTEXT_MANAGER.md** | index/task-router.md | 1 |
| **rules/core/work-mode.md** | CLAUDE.md | 5 |
| **rules/core/blocking-rules.md** | work-mode.md | 3 |
| **rules/domain/coding.md** | core/work-mode.md | 8 |
| **errors/ERROR_CATALOG.md** | top-5-errors.md | 15 |

### 能力文档依赖

| 能力文档 | 依赖规则 | 依赖工具 |
|---------|---------|---------|
| **capabilities/browser-automation/** | coding.md, testing.md | Playwright MCP |
| **capabilities/skills-guide.md** | - | 41 Skills |
| **capabilities/plugins-auto.md** | - | 80 Plugins |
| **design/DESIGN_MASTER_PERSONA.md** | - | Nano Banana Pro |
| **vibe-marketing/** | - | N8N Workflows |

---

## 🔄 循环引用检查

```mermaid
graph LR
    A[CLAUDE.md] --> B[rules/core/]
    B --> C[rules/domain/]
    C --> D[capabilities/]
    D --> E[errors/]
    E --> C

    style A fill:#4CAF50,color:#fff
    style E fill:#F44336,color:#fff

    %% 注释：E --> C 是合理的循环（错误文档引用编码规则）
```

**检查结果**: ✅ 无不合理的循环依赖

---

## 🎯 快速查找路径

### 场景 1: 我想写一个 Playwright 测试

```
路径 1: QUICK_START.md → 示例任务
路径 2: index/task-router.md → capabilities/browser-automation/
路径 3: CLAUDE.md → "浏览器" 关键词 → 自动加载
```

### 场景 2: 遇到异步未并行错误

```
路径 1: errors/top-5-errors.md → E001
路径 2: errors/ERROR_CATALOG.md → E001（完整版）
路径 3: rules/domain/coding.md → Common Patterns
```

### 场景 3: 配置 Git 工作流

```
路径 1: CLAUDE.md → Skills 章节 → /commit
路径 2: rules/domain/git.md → Git Workflow
路径 3: capabilities/skills-guide.md → Git 工作流
```

### 场景 4: 创建 Remotion 视频

```
路径 1: QUICK_START.md → 示例任务
路径 2: capabilities/REMOTION_TEMPLATES_LIBRARY.md → 15个模板
路径 3: examples/project-rules/remotion-auto-production.md → 完整规则
```

---

## 📊 文档统计

| 类别 | 文档数量 | 总行数 | 平均大小 |
|------|---------|-------|---------|
| **核心文档** | 3 | ~800 | ~5KB |
| **索引文档** | 4 | ~2,000 | ~8KB |
| **规则文档** | 9 | ~1,200 | ~3KB |
| **能力文档** | 9 | ~5,000 | ~15KB |
| **错误文档** | 2 | ~800 | ~12KB |
| **设计文档** | 2 | ~2,000 | ~30KB |
| **营销文档** | 3 | ~1,400 | ~18KB |
| **总计** | **40** | **~13,200** | **~10KB** |

---

## 🗂️ 文档更新频率

| 文档 | 更新频率 | 最后更新 |
|------|---------|---------|
| **CLAUDE.md** | 每个大版本 | v5.2 (2026-02-22) |
| **rules/hooks.md** | 每次 Hook 变更 | v2.0 (2026-02-10) |
| **capabilities/skills-guide.md** | 新增 Skill 时 | v2.0 (2026-02-10) |
| **capabilities/plugins-auto.md** | 新增 Plugin 时 | v2.0 (2026-02-10) |
| **errors/ERROR_CATALOG.md** | 发现新错误模式 | v1.0 (2026-01-28) |
| **CHANGELOG.md** | 每次提交 | 持续更新 |

---

## 🔗 相关文档链接

### 快速开始
- [QUICK_START.md](QUICK_START.md) - 5 分钟快速开始
- [README.md](README.md) - 项目概览和架构

### 核心文档
- [CLAUDE.md](CLAUDE.md) - 核心配置入口
- [CONTEXT_MANAGER.md](CONTEXT_MANAGER.md) - 智能加载系统

### 索引系统
- [index/task-router.md](index/task-router.md) - 任务路由决策树
- [index/capabilities-index.md](index/capabilities-index.md) - 能力索引
- [index/tools-index.md](index/tools-index.md) - 工具索引

### 规则系统
- [rules/core/](rules/core/) - 核心规则
- [rules/domain/](rules/domain/) - 领域规则
- [rules/agents.md](rules/agents.md) - Agent 编排
- [rules/hooks.md](rules/hooks.md) - Hooks 系统

### 能力库
- [capabilities/](capabilities/) - 各种能力文档
- [design/](design/) - UI 设计指南
- [vibe-marketing/](vibe-marketing/) - 营销内容

### 错误库
- [errors/top-5-errors.md](errors/top-5-errors.md) - Top 5 错误
- [errors/ERROR_CATALOG.md](errors/ERROR_CATALOG.md) - 完整错误目录

---

**版本**: v1.0
**创建日期**: 2026-02-22
**维护周期**: 每次文档结构变更时更新
