# 错误模式索引 - Error Patterns Index

> **用途**: 快速诊断和解决常见错误

---

## 🎯 快速诊断流程

```
遇到错误
  ↓
查看 Top 5 高频错误 (本文档)
  ↓
找到匹配？
  ├─ 是 → 应用快速修复
  └─ 否 → 查看完整错误目录 (ERROR_CATALOG.md)
```

---

## ⚡ Top 5 高频错误（必看）

### E001: 异步未并行 | 🔴 严重 | 高频

**症状**: 多个异步操作慢得离谱

**快速检查**:

```javascript
// ❌ 错误模式
for (const item of items) {
  await doSomething(item); // 顺序执行
}

// ✅ 正确模式
await Promise.all(items.map((item) => doSomething(item)));
```

**影响**: 性能慢 N 倍（N = 操作数量）

**详细文档**: `errors/top-5-errors.md` (E001)

---

### E002: 轮询无超时 | 🔴 严重 | 高频

**症状**: 轮询永远不停止

**快速检查**:

```javascript
// ❌ 错误模式
setInterval(async () => {
  const data = await checkStatus();
  // 没有退出条件和超时
}, 2000);

// ✅ 正确模式
function poll(maxAttempts = 30) {
  let attempts = 0;
  const interval = setInterval(async () => {
    attempts++;
    if (attempts > maxAttempts) {
      clearInterval(interval);
      // 处理超时
    }
    // 检查状态...
  }, 2000);
}
```

**影响**: 资源泄漏、浏览器卡死

**详细文档**: `errors/top-5-errors.md` (E002)

---

### E003: 错误未重新抛出 | 🔴 严重 | 中频

**症状**: 错误被"吞掉"，调用者不知道失败

**快速检查**:

```javascript
// ❌ 错误模式
async function fetchData() {
  try {
    return await api.get('/data');
  } catch (error) {
    console.error(error); // 只记录，没有抛出
  }
}

// ✅ 正确模式
async function fetchData() {
  try {
    return await api.get('/data');
  } catch (error) {
    console.error(error);
    throw new Error(`Failed to fetch: ${error.message}`);
  }
}
```

**影响**: 静默失败、数据不一致

**详细文档**: `errors/top-5-errors.md` (E003)

---

### E004: SQL 未用 CTE | 🟡 中等 | 中频

**症状**: SQL 查询慢

**快速检查**:

```sql
-- ❌ 错误模式（先 JOIN 再过滤）
SELECT b.*, u.energy_change
FROM large_table b
JOIN another_table u ON b.id = u.id
WHERE b.date = '2024-01-15';  -- 过滤在 JOIN 后

-- ✅ 正确模式（先过滤再 JOIN）
WITH filtered AS (
  SELECT * FROM large_table
  WHERE date = '2024-01-15'  -- 先过滤
)
SELECT b.*, u.energy_change
FROM filtered b
JOIN another_table u ON b.id = u.id;
```

**影响**: 性能慢 10-100 倍

**详细文档**: `errors/top-5-errors.md` (E004)

---

### E007: 资源泄漏 | 🔴 严重 | 中频

**症状**: UI 卡住、内存持续增长

**快速检查**:

```javascript
// ❌ 错误模式（只在成功时清理）
async function process() {
  startLoading();
  try {
    await doWork();
    stopLoading(); // 只在成功时清理
  } catch (error) {
    showError(error); // 失败时忘记 stopLoading()
  }
}

// ✅ 正确模式（所有路径都清理）
async function process() {
  startLoading();
  try {
    await doWork();
  } catch (error) {
    showError(error);
  } finally {
    stopLoading(); // 所有路径都清理
  }
}
```

**影响**: 资源泄漏、UI 异常

**详细文档**: `errors/top-5-errors.md` (E007)

---

## 📋 编码前检查清单

在写代码前，快速过一遍：

```
[ ] 多个异步操作 → 用 Promise.all() 并行
[ ] 轮询 → 设置 maxAttempts 超时
[ ] catch 块 → throw error 重新抛出
[ ] SQL JOIN → 先 CTE 过滤再 JOIN
[ ] 资源清理 → 用 finally 确保所有路径清理
```

---

## 🗂️ 完整错误目录（E001-E015）

### 高频错误（编码前必查）

| 错误     | 严重程度 | 频率 | 快速诊断               |
| -------- | -------- | ---- | ---------------------- |
| **E001** | 🔴 严重  | 高频 | 多个 await 顺序执行？  |
| **E002** | 🔴 严重  | 高频 | 轮询没有 maxAttempts？ |
| **E003** | 🔴 严重  | 中频 | catch 没有 throw？     |
| **E007** | 🔴 严重  | 中频 | 没用 finally 清理？    |

### 中频错误（注意防范）

| 错误     | 严重程度 | 频率 | 快速诊断           |
| -------- | -------- | ---- | ------------------ |
| **E004** | 🟡 中等  | 中频 | JOIN 后才过滤？    |
| **E008** | 🔴 严重  | 中频 | ID 类型未验证？    |
| **E013** | 🔴 严重  | 中频 | 每次请求加载文件？ |

### 低频但重要

| 错误     | 严重程度 | 频率 | 快速诊断               |
| -------- | -------- | ---- | ---------------------- |
| **E011** | 🟡 中等  | 低频 | Git Bash 中 npm 卡住？ |
| **E012** | 🟡 中等  | 低频 | Hook 没执行权限？      |
| **E014** | 🟡 中等  | 低频 | 路径跨平台失败？       |
| **E015** | 🔴 严重  | 低频 | Hook 只设置环境变量？  |

**完整错误库**: `errors/ERROR_CATALOG.md`

---

## 🔍 按症状查找

### 性能问题

| 症状       | 可能错误 | 检查项              |
| ---------- | -------- | ------------------- |
| 异步操作慢 | E001     | 是否并行执行？      |
| SQL 查询慢 | E004     | 是否用 CTE 预过滤？ |
| 每次请求慢 | E013     | 是否启动时加载？    |

### 资源问题

| 症状       | 可能错误 | 检查项         |
| ---------- | -------- | -------------- |
| 轮询不停止 | E002     | 有超时机制？   |
| UI 卡住    | E007     | finally 清理？ |
| 内存泄漏   | E007     | 所有路径清理？ |

### 逻辑问题

| 症状     | 可能错误 | 检查项             |
| -------- | -------- | ------------------ |
| 静默失败 | E003     | catch 是否 throw？ |
| ID 混淆  | E008     | 验证 ID 含义？     |
| 权限问题 | E012     | chmod +x hook？    |

### 环境问题

| 症状        | 可能错误 | 检查项                    |
| ----------- | -------- | ------------------------- |
| npm 卡住    | E011     | 在 Git Bash？→ PowerShell |
| 路径错误    | E014     | 统一路径转换？            |
| Hook 未生效 | E015     | 验证完整链路？            |

---

## 🎯 按语言/技术栈查找

### JavaScript/TypeScript

| 错误 | 场景                       |
| ---- | -------------------------- |
| E001 | Promise.all() vs for-await |
| E002 | setInterval 超时控制       |
| E003 | async/await 错误处理       |
| E007 | 资源清理（finally）        |

### SQL/数据库

| 错误 | 场景             |
| ---- | ---------------- |
| E004 | CTE vs 直接 JOIN |
| E008 | ID 类型验证      |

### Node.js/后端

| 错误 | 场景           |
| ---- | -------------- |
| E013 | 知识库加载时机 |

### 工具链

| 错误 | 场景            |
| ---- | --------------- |
| E011 | Git Bash + npm  |
| E012 | Husky hook 权限 |
| E014 | 跨平台路径      |
| E015 | Hook 完整验证   |

---

## 📚 详细文档位置

### 快速参考

- `errors/top-5-errors.md` (6KB) - 5个最高频错误
  - 包含：快速检查、错误/正确示例、影响分析

### 完整目录

- `errors/ERROR_CATALOG.md` (30KB) - 所有 15 个错误
  - 包含：完整案例、根因分析、测试用例、修复方案

---

## 🔄 错误预防流程

### 编码前（最重要）

```
1. 查看 Top 5 错误 (2分钟)
   ↓
2. 过一遍检查清单 (1分钟)
   ↓
3. 开始编码
```

### 编码中

```
写代码
  ↓
遇到类似场景
  ↓
快速查本索引 (30秒)
  ↓
应用正确模式
```

### 调试时

```
遇到错误
  ↓
查症状索引 (30秒)
  ↓
找到可能错误
  ↓
查详细文档
  ↓
应用修复方案
```

---

## 💡 学习路径

### 新手（15分钟）

1. **记住 Top 5** (10分钟)
   - E001: 异步并行
   - E002: 轮询超时
   - E003: 错误抛出
   - E004: SQL CTE
   - E007: 资源清理

2. **实践检查清单** (5分钟)
   - 每次编码前过一遍

### 进阶（1小时）

1. **阅读完整 ERROR_CATALOG.md** (40分钟)
   - 理解所有 15 个错误

2. **建立预防意识** (20分钟)
   - 在实际项目中应用

### 专家（持续）

- **主动预防**: 编码前自动过检查清单
- **快速诊断**: 看症状立即知道可能错误
- **传播知识**: 代码审查时指出这些模式

---

## 🎓 错误模式速查卡

### 打印贴在显示器上

```
┌─────────────────────────────────────┐
│    编码前 5 秒检查清单               │
├─────────────────────────────────────┤
│ □ 异步并行？(Promise.all)           │
│ □ 轮询超时？(maxAttempts)           │
│ □ 错误抛出？(throw error)           │
│ □ SQL CTE？(先过滤再JOIN)           │
│ □ 资源清理？(finally)               │
└─────────────────────────────────────┘
```

---

## 🔗 相关工具

### 自动检测

某些错误可以通过工具自动检测：

| 错误 | 工具        | 如何使用                                                    |
| ---- | ----------- | ----------------------------------------------------------- |
| E003 | ESLint      | `no-unused-vars`, `@typescript-eslint/no-floating-promises` |
| E004 | SQL Explain | `EXPLAIN ANALYZE`                                           |
| E007 | ESLint      | `no-unsafe-finally`                                         |

### 代码审查

使用 `/code-review` Skill 时会自动检查这些模式：

```bash
/code-review
```

### GPT 专家

严重错误可以请 GPT Code Reviewer 审查：

```
"请检查代码中是否有 E001-E007 错误模式"
```

---

## 📊 错误统计

基于历史数据（非官方统计）：

```
E001 (异步未并行): ████████████ 60%
E002 (轮询无超时): ████████ 40%
E003 (错误未抛出): ██████ 30%
E007 (资源泄漏): █████ 25%
E004 (SQL未CTE): ████ 20%
其他 10 个错误: ██ 10%
```

**建议**: 重点防范前 5 个错误，可以避免 ~80% 的问题。

---

## 🆘 紧急修复指南

### 生产环境错误

```
1. 识别症状
   ↓
2. 查本索引找匹配错误
   ↓
3. 应用快速修复（不要重构）
   ↓
4. 验证修复
   ↓
5. 部署
   ↓
6. 事后根因分析（查完整文档）
```

### 开发环境错误

```
1. 查本索引
   ↓
2. 如果是 Top 5 → 立即修复
   ↓
3. 如果不是 → 查 ERROR_CATALOG.md
   ↓
4. 应用正确模式
   ↓
5. 添加测试防止回归
```

---

## 📝 贡献新错误模式

发现新的高频错误模式？

1. 记录错误场景
2. 分析根本原因
3. 总结正确模式
4. 添加到 ERROR_CATALOG.md
5. 如果频率高，考虑加入 Top 5

---

**版本**: v1.0
**更新**: 2026-02-05
**错误总数**: 15个（E001-E015）
**Top 5 覆盖率**: ~80% 常见问题
