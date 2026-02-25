# ⚠️ ERROR_CATALOG - 错误知识库总览

> **Version**: 2.2
> **Last Updated**: 2026-02-02
> **Status**: Active
> **用途**: 错误统计仪表板和快速索引
> **新增**: ML Production Errors (E016-E018)

---

## 📊 错误统计仪表板

### 高频错误 Top 13（⭐ 每次编码前必查）

| ID       | 错误类型                      | 频率   | 严重度 | 最后修复       | 自检问题                          |
| -------- | ----------------------------- | ------ | ------ | -------------- | --------------------------------- |
| E001     | 异步未并行处理                | 高     | 🔴     | 2026-01-10     | 是否使用 `Promise.all()`?         |
| E002     | 轮询无超时限制                | 高     | 🔴     | 2026-01-10     | 是否设置 `maxAttempts`?           |
| E003     | 错误未重新抛出                | 中     | 🔴     | 2026-01-10     | `catch` 是否 `throw error`?       |
| E004     | SQL 未使用 CTE                | 中     | 🟡     | 2026-01-09     | 是否预过滤数据?                   |
| E005     | 状态 ID 重复生成              | 中     | 🟡     | 2026-01-09     | ID 是否只生成一次?                |
| E006     | API 参数顺序错误              | 中     | 🟡     | 2026-01-09     | 是否核对文档?                     |
| E007     | 忘记资源清理                  | 低     | 🔴     | 2026-01-09     | 超时/失败是否清理?                |
| E008     | Chart 配置不完整              | 低     | 🟢     | 2026-01-09     | 是否包含 tooltip?                 |
| E009     | 依赖未安装就使用              | 低     | 🟡     | 2026-01-09     | 是否 `npm install`?               |
| E010     | 硬编码魔法值                  | 低     | 🟢     | 2026-01-09     | 是否使用常量?                     |
| **E011** | **Git Bash npm install 失败** | **高** | **🟡** | **2026-01-23** | **是否在 PowerShell/CMD 中运行?** |
| **E012** | **Pre-commit Hook 权限**      | **中** | **🟡** | **2026-01-23** | **Hook 是否可执行 (`chmod +x`)?** |
| **E013** | **知识库每次请求加载**        | **中** | **🔴** | **2026-01-23** | **是否在启动时预加载到内存?**     |
| **E016** | **🆕 Train/Serve Skew**       | **高** | **🔴** | **2026-02-02** | **训练服务是否用同一代码路径?**   |
| **E017** | **🆕 ML 部署无监控**          | **高** | **🔴** | **2026-02-02** | **是否有 5 个核心监控?**          |
| **E018** | **🆕 静默模型漂移**           | **中** | **🔴** | **2026-02-02** | **是否监控输入分布?**             |

### 错误趋势分析

```
高频错误趋势（过去 30 天）:
E001: ████████░░ 80% → 60%  📉 下降
E002: ██████████ 100% → 40% 📉 显著改善
E003: ████████░░ 80% → 70%  📉 轻微改善
E004: ██████░░░░ 60% → 50%  📉 持续改善
E005: ████░░░░░░ 40% → 30%  📉 改善中
```

### 严重度分布

| 严重度  | 数量 | 占比 | 状态                         |
| ------- | ---- | ---- | ---------------------------- |
| 🔴 严重 | 7    | 44%  | 需要优先处理（新增 ML 错误） |
| 🟡 中等 | 4    | 25%  | 持续监控                     |
| 🟢 轻微 | 2    | 12%  | 定期审查                     |

---

## 📂 错误分类索引

### 系统级错误（影响思维逻辑和代码质量）

系统级错误会影响整体思考方式和编码模式，需要特别注意。

| 文件                                                              | 错误类别     | 错误数量 | 优先级 |
| ----------------------------------------------------------------- | ------------ | -------- | ------ |
| [async-parallel.md](./errors/system-errors/async-parallel.md)     | 异步并行处理 | 3        | 🔴 高  |
| [timeout-polling.md](./errors/system-errors/timeout-polling.md)   | 超时与轮询   | 2        | 🔴 高  |
| [error-handling.md](./errors/system-errors/error-handling.md)     | 错误处理     | 4        | 🔴 高  |
| [sql-optimization.md](./errors/system-errors/sql-optimization.md) | SQL 优化     | 2        | 🟡 中  |
| [state-management.md](./errors/system-errors/state-management.md) | 状态管理     | 3        | 🟡 中  |
| [api-integration.md](./errors/system-errors/api-integration.md)   | API 集成     | 3        | 🟡 中  |

### 🆕 ML 生产错误（Machine Learning in Production）

| 文件                                                                        | 错误类别           | 错误数量 | 优先级 |
| --------------------------------------------------------------------------- | ------------------ | -------- | ------ |
| [E016-train-serve-skew.md](./errors/ml-errors/E016-train-serve-skew.md)     | Train/Serve 不一致 | 4        | 🔴 高  |
| [E017-ml-no-monitoring.md](./errors/ml-errors/E017-ml-no-monitoring.md)     | 部署无监控         | 1        | 🔴 高  |
| [E018-silent-model-drift.md](./errors/ml-errors/E018-silent-model-drift.md) | 静默模型漂移       | 1        | 🔴 高  |

**总计**: 6 个分类，17 个错误模式 + 🆕 3 个 ML 错误（6 个案例）

### 项目级错误（特定项目场景）

项目级错误针对特定项目的技术栈和业务场景。

| 项目                     | 文件                                                                  | 错误数量 | 最后更新   |
| ------------------------ | --------------------------------------------------------------------- | -------- | ---------- |
| claude-plugin-manager    | [claude-plugin-manager.md](./project-errors/claude-plugin-manager.md) | 8        | 2026-01-14 |
| data-analysis-automation | [data-analysis.md](./project-errors/data-analysis.md)                 | 5        | 2026-01-14 |
| firebase-mcp-integration | [firebase-mcp.md](./project-errors/firebase-mcp.md)                   | 3        | 2026-01-14 |

**总计**: 3 个项目，16 个错误案例

---

## 🔍 快速查找

### 按关键词搜索

| 关键词             | 相关错误              | 文档位置                                                                   |
| ------------------ | --------------------- | -------------------------------------------------------------------------- |
| `Promise.all`      | E001 异步并行         | [async-parallel.md](./errors/system-errors/async-parallel.md)              |
| `setTimeout`       | E002 超时轮询         | [timeout-polling.md](./errors/system-errors/timeout-polling.md)            |
| `try-catch`        | E003 错误处理         | [error-handling.md](./errors/system-errors/error-handling.md)              |
| `WITH CTE`         | E004 SQL 优化         | [sql-optimization.md](./errors/system-errors/sql-optimization.md)          |
| `useState`         | E005 状态管理         | [state-management.md](./errors/system-errors/state-management.md)          |
| `API call`         | E006 API 参数         | [api-integration.md](./errors/system-errors/api-integration.md)            |
| `cleanup`          | E007 资源清理         | [error-handling.md](./errors/system-errors/error-handling.md)              |
| `chart config`     | E008 图表配置         | [api-integration.md](./errors/system-errors/api-integration.md)            |
| `npm install`      | E009 依赖安装         | project-errors/ (待创建)                                                   |
| `magic number`     | E010 硬编码           | [state-management.md](./errors/system-errors/state-management.md)          |
| `Feature Store`    | E016 Train/Serve Skew | [E016-train-serve-skew.md](./errors/ml-errors/E016-train-serve-skew.md)    |
| `model monitoring` | E017 ML 无监控        | [ML_MONITORING_CHECKLIST.md](../best-practices/ML_MONITORING_CHECKLIST.md) |
| `feature drift`    | E018 模型漂移         | [E016-train-serve-skew.md](./errors/ml-errors/E016-train-serve-skew.md)    |

### 按场景搜索

| 场景           | 常见错误         | 推荐阅读                                                                                                                                            |
| -------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **异步操作**   | E001, E002, E003 | [async-parallel.md](./errors/system-errors/async-parallel.md), [timeout-polling.md](./errors/system-errors/timeout-polling.md)                      |
| **数据库查询** | E004             | [sql-optimization.md](./errors/system-errors/sql-optimization.md)                                                                                   |
| **API 集成**   | E006, E008       | [api-integration.md](./errors/system-errors/api-integration.md)                                                                                     |
| **状态管理**   | E005, E010       | [state-management.md](./errors/system-errors/state-management.md)                                                                                   |
| **错误处理**   | E003, E007       | [error-handling.md](./errors/system-errors/error-handling.md)                                                                                       |
| **🆕 ML 生产** | E016, E017, E018 | [E016-train-serve-skew.md](./errors/ml-errors/E016-train-serve-skew.md), [ML_MONITORING_CHECKLIST.md](../best-practices/ML_MONITORING_CHECKLIST.md) |

---

## 📋 编码前自检清单

在开始编写代码前，检查以下要点：

### 异步操作（E001, E002）

- [ ] 多个独立异步操作是否并行？使用 `Promise.all()`？
- [ ] 轮询是否设置超时？`maxAttempts` 限制？
- [ ] 是否有取消机制？`clearInterval` / `clearTimeout`？

### 错误处理（E003, E007）

- [ ] `catch` 块是否重新抛出错误？
- [ ] 错误信息是否友好？是否记录日志？
- [ ] 超时/失败后是否清理资源？

### SQL 查询（E004）

- [ ] 是否使用 CTE 预过滤数据？
- [ ] 避免在 `GROUP BY` 中重复计算？
- [ ] JOIN 前是否过滤数据？

### 状态管理（E005, E010）

- [ ] ID 是否只生成一次？
- [ ] 是否使用正确的状态 ID？
- [ ] 是否有硬编码魔法值？

### API 调用（E006, E008）

- [ ] 参数顺序是否正确？
- [ ] 是否处理 Rate Limit？
- [ ] 图表配置是否完整（tooltip、legend 等）？

---

## 📈 改进目标

### 短期目标（1个月）

- ✅ 高频错误（E001-E003）降至中频
- ✅ 所有严重错误添加到自检清单
- ✅ 建立错误自动检测机制

### 中期目标（3个月）

- ✅ 中频错误降至低频
- ✅ 错误发生率降低 50%
- ✅ 平均修复时间缩短 30%

### 长期目标（6个月）

- ✅ 高频错误实现零发生
- ✅ 建立完善的错误预防体系
- ✅ 代码质量评分提升至 A 级

---

## 🔄 持续改进流程

```
编码 → 遇到错误 → 分析根因
              ↓
        记录到错误库（系统级/项目级）
              ↓
        更新自检清单
              ↓
        下次会话自动审查
              ↓
        跟踪改进趋势
```

---

## 📖 相关文档

### 核心文档

- [CLAUDE.md](../CLAUDE.md) - 主配置文档
- [QUICK_START.md](../QUICK_START.md) - 会话启动清单
- [DECISION_TREE.md](../DECISION_TREE.md) - 能力决策树

### 错误文档

- [system-errors/](./system-errors/README.md) - 系统级错误（6 个分类）
- project-errors/ - 项目级错误（按项目，待创建）

### 学习系统

- [learning/skill-evolution.md](../docs/learning/skill-evolution.md) - 技能进化
- [learning/session-insights.md](../docs/learning/session-insights.md) - 会话洞察

---

## ✅ 使用指南

### 每次会话开始时

1. 阅读 Top 10 高频错误
2. 识别当前任务相关的错误类型
3. 回顾对应的错误文档

### 编码过程中

1. 使用自检清单验证代码
2. 遇到问题先查找相关错误
3. 记录新发现的错误模式

### 会话结束时

1. 更新错误统计
2. 记录改进措施
3. 更新趋势分析

---

**📌 提示**:

- 每次编码前必查 Top 10 错误
- 使用自检清单预防错误
- 持续跟踪改进趋势
- 记录新发现的错误模式
