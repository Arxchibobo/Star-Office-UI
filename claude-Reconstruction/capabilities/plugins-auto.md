# Plugins 自动激活指南

> **Plugins**: 根据任务上下文自动激活的专业代理
> **版本**: v2.0 (2026-02-10 更新)
> **Plugins 总数**: 80 (来自 4 个来源)

---

## 概览

Plugins 是预配置的专业代理（Agents），根据任务描述自动激活，无需显式调用。

### Plugin 来源

| 来源                        | 数量 | 说明                            |
| --------------------------- | ---- | ------------------------------- |
| **claude-code-workflows**   | 60   | 官方工作流插件集                |
| **claude-plugins-official** | 13   | 官方核心插件                    |
| **everything-claude-code**  | 1    | 全功能增强插件                  |
| **superpowers-marketplace** | 1    | 社区超能力插件                  |
| **其他第三方**              | 5    | delegator, scientific-writer 等 |

### 核心特点

1. **自动激活** - 描述需求即可，无需记住命令
2. **专业领域** - 每个 Plugin 专注特定领域
3. **协同工作** - 多个 Plugins 可以同时激活

---

## 开发类 Plugins

### 后端开发

| Plugin                     | 专长                                | 自动激活关键词               |
| -------------------------- | ----------------------------------- | ---------------------------- |
| **backend-development**    | API 设计、微服务架构、TDD、事件溯源 | 后端、API、架构              |
| **python-development**     | Python/Django/FastAPI 开发          | Python、Django、FastAPI      |
| **javascript-typescript**  | JS/TS 高级开发                      | JavaScript、TypeScript、Node |
| **systems-programming**    | Rust/Go/C/C++ 系统编程              | Rust、Go、C++、系统          |
| **jvm-languages**          | Java/C#/Scala 企业开发              | Java、Kotlin、Scala、C#      |
| **web-scripting**          | PHP/Ruby Web 开发                   | PHP、Ruby、Rails             |
| **functional-programming** | Elixir/Haskell 函数式               | Elixir、Haskell、函数式      |

### 前端开发

| Plugin                          | 专长                              | 自动激活关键词           |
| ------------------------------- | --------------------------------- | ------------------------ |
| **frontend-mobile-development** | React/Vue/Flutter 前端+移动       | React、Vue、Flutter      |
| **multi-platform-apps**         | 跨平台（iOS/Android/Web/Desktop） | 跨平台、SwiftUI、Flutter |

### 数据库

| Plugin                          | 专长                              | 自动激活关键词       |
| ------------------------------- | --------------------------------- | -------------------- |
| **database-design**             | 数据库架构、Schema 设计、SQL 优化 | 数据库设计、Schema   |
| **database-migrations**         | 数据库迁移、DBA、优化             | 迁移、Migration      |
| **database-cloud-optimization** | 云数据库优化                      | 数据库优化、云数据库 |
| **data-engineering**            | 数据管道、ETL、Spark              | 数据管道、ETL        |
| **data-validation-suite**       | 输入验证、API 安全                | 数据验证、输入检查   |

### API 开发

| Plugin                   | 专长                            | 自动激活关键词   |
| ------------------------ | ------------------------------- | ---------------- |
| **api-scaffolding**      | API 脚手架（REST/GraphQL/gRPC） | API 创建、新接口 |
| **backend-api-security** | API 安全、认证授权              | API 安全、OAuth  |

### 特殊领域

| Plugin                          | 专长                      | 自动激活关键词         |
| ------------------------------- | ------------------------- | ---------------------- |
| **game-development**            | Unity/Minecraft 游戏开发  | 游戏、Unity、Minecraft |
| **blockchain-web3**             | 智能合约、DeFi、Web3      | 区块链、Web3、合约     |
| **arm-cortex-microcontrollers** | 嵌入式 ARM 开发           | 嵌入式、ARM、固件      |
| **payment-processing**          | 支付集成（Stripe/PayPal） | 支付、Stripe           |
| **llm-application-dev**         | LLM 应用、RAG、Agent      | LLM、AI 应用、RAG      |
| **machine-learning-ops**        | MLOps、模型训练部署       | ML、机器学习           |

---

## 运维类 Plugins

### 云基础设施

| Plugin                    | 专长                   | 自动激活关键词                 |
| ------------------------- | ---------------------- | ------------------------------ |
| **cloud-infrastructure**  | AWS/Azure/GCP 多云架构 | AWS、Azure、GCP、云            |
| **kubernetes-operations** | K8s 架构、GitOps       | K8s、Kubernetes、容器          |
| **cicd-automation**       | CI/CD 管道、GitOps     | 部署、Pipeline、GitHub Actions |
| **deployment-strategies** | 部署策略、蓝绿/金丝雀  | 部署策略、蓝绿                 |
| **deployment-validation** | 部署验证               | 部署验证                       |

### 监控与调试

| Plugin                       | 专长                 | 自动激活关键词        |
| ---------------------------- | -------------------- | --------------------- |
| **observability-monitoring** | 可观测性、监控、告警 | 监控、Metrics、Traces |
| **application-performance**  | 应用性能优化         | 性能、Core Web Vitals |
| **debugging-toolkit**        | 调试工具箱           | 调试、Debug           |
| **error-debugging**          | 错误调试             | 错误排查              |
| **error-diagnostics**        | 错误诊断             | 错误诊断、Stack Trace |
| **distributed-debugging**    | 分布式系统调试       | 分布式调试            |
| **incident-response**        | 故障响应、SRE        | 故障、Incident、告警  |

---

## 质量类 Plugins

### 代码审查

| Plugin                   | 专长                                | 自动激活关键词     |
| ------------------------ | ----------------------------------- | ------------------ |
| **code-review-ai**       | AI 辅助代码审查                     | 审查、Review       |
| **comprehensive-review** | 全面审查（架构+安全+代码）          | 全面审查、深度审查 |
| **pr-review-toolkit**    | PR 审查工具箱（类型分析、静默失败） | PR 审查            |
| **git-pr-workflows**     | Git/PR 工作流                       | PR 流程            |

### 测试

| Plugin                         | 专长                            | 自动激活关键词      |
| ------------------------------ | ------------------------------- | ------------------- |
| **unit-testing**               | 单元测试、调试                  | 单元测试、Unit Test |
| **tdd-workflows**              | TDD 编排、代码审查              | TDD、测试驱动       |
| **performance-testing-review** | 性能测试                        | 性能测试、负载测试  |
| **full-stack-orchestration**   | 全栈编排（部署+性能+安全+测试） | 全栈、端到端        |
| **codebase-cleanup**           | 代码清理                        | 清理、Dead Code     |
| **accessibility-compliance**   | 无障碍合规                      | 无障碍、A11y        |

### 安全

| Plugin                | 专长               | 自动激活关键词 |
| --------------------- | ------------------ | -------------- |
| **security-scanning** | 安全扫描、威胁建模 | 安全扫描、威胁 |

### 重构与迁移

| Plugin                    | 专长                     | 自动激活关键词 |
| ------------------------- | ------------------------ | -------------- |
| **code-refactoring**      | 代码重构、遗留系统现代化 | 重构、Refactor |
| **framework-migration**   | 框架迁移                 | 迁移、框架升级 |
| **dependency-management** | 依赖管理、版本更新       | 依赖、升级     |

---

## 文档类 Plugins

| Plugin                       | 专长                           | 自动激活关键词      |
| ---------------------------- | ------------------------------ | ------------------- |
| **code-documentation**       | 代码文档、审查、教程           | 文档、Documentation |
| **documentation-generation** | API 文档、Mermaid 图、参考手册 | 生成文档、API 文档  |

---

## AI/ML 类 Plugins

| Plugin                  | 专长                     | 自动激活关键词  |
| ----------------------- | ------------------------ | --------------- |
| **agent-orchestration** | Context 管理、Agent 编排 | Agent、多代理   |
| **context-management**  | 上下文工程、知识图谱     | Context、上下文 |

---

## 营销/内容类 Plugins

| Plugin                         | 专长                 | 自动激活关键词          |
| ------------------------------ | -------------------- | ----------------------- |
| **seo-content-creation**       | SEO 内容策划+写作    | SEO、内容创作           |
| **seo-technical-optimization** | 技术 SEO 优化        | 技术 SEO、Meta          |
| **seo-analysis-monitoring**    | SEO 分析监控         | SEO 分析                |
| **content-marketing**          | 内容营销策略         | 营销、Content Marketing |
| **customer-sales-automation**  | 客户支持、销售自动化 | 客服、销售              |

---

## 协作类 Plugins

| Plugin                 | 专长           | 自动激活关键词 |
| ---------------------- | -------------- | -------------- |
| **team-collaboration** | 开发者体验优化 | DX、开发体验   |

---

## 官方核心 Plugins

| Plugin                       | 说明                       |
| ---------------------------- | -------------------------- |
| **code-review**              | 官方代码审查               |
| **commit-commands**          | 官方 Git 提交              |
| **feature-dev**              | 功能开发（架构→探索→审查） |
| **frontend-design**          | 前端设计                   |
| **hookify**                  | Hooks 系统管理             |
| **plugin-dev**               | Plugin 开发工具            |
| **firebase**                 | Firebase 集成              |
| **playwright**               | 浏览器自动化               |
| **gitlab**                   | GitLab 集成                |
| **typescript-lsp**           | TypeScript LSP             |
| **pyright-lsp**              | Python LSP                 |
| **explanatory-output-style** | 解释性输出风格             |
| **learning-output-style**    | 学习性输出风格             |

---

## 增强 Plugins

| Plugin                       | 来源                     | 说明                                                   |
| ---------------------------- | ------------------------ | ------------------------------------------------------ |
| **everything-claude-code**   | everything-claude-code   | 全功能增强（planner、architect、TDD、e2e、security等） |
| **superpowers**              | superpowers-marketplace  | 社区超能力代理                                         |
| **claude-delegator**         | jarrodwatts              | 任务委派器                                             |
| **claude-scientific-writer** | claude-scientific-writer | 科学论文写作                                           |

---

## Plugin 协同

多个 Plugins 可以协同工作：

```
用户: 创建一个新的微服务，包含数据库设计和 CI/CD 配置

自动激活:
├─ backend-development (服务架构)
├─ database-design (数据库设计)
└─ cicd-automation (CI/CD 配置)

执行流程:
1. 设计服务架构
2. 设计数据库 Schema
3. 生成 Dockerfile
4. 配置 CI/CD Pipeline
```

---

## Plugin 优先级

当多个 Plugins 可能适用时，按以下优先级激活：

1. **安全类** - 涉及安全的任务优先
2. **专业领域** - 匹配度最高的领域 Plugin
3. **通用类** - 无特定领域时使用

---

## 最佳实践

1. **让系统选择** - 描述需求，让 Plugin 自动激活
2. **明确意图** - 清晰描述任务目标
3. **迭代优化** - 根据结果调整描述
4. **组合使用** - 复杂任务利用多 Plugin 协同
