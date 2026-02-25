# Top 5 高频错误 - 快速参考

> **用途**: 编码前必查的5个最常见错误模式

---

## E001: 异步未并行 | 🔴 严重 | 高频

### 问题

多个独立的异步操作顺序执行，而不是并行执行。

### 快速检查

❓ **多个独立的异步操作是否用了 `Promise.all()`？**

### 错误示例

```javascript
// ❌ 错误：顺序执行 (13次 × 2秒 = 26秒)
for (const term of searchTerms) {
  const results = await api.search(term); // 等待这个完成才开始下一个
  allResults.push(...results);
}
```

### 正确做法

```javascript
// ✅ 正确：并行执行 (max 2秒)
const searchPromises = searchTerms.map((term) =>
  api
    .search(term)
    .then((results) => ({ term, results, success: true }))
    .catch((error) => ({
      term,
      results: [],
      success: false,
      error: error.message,
    }))
);
const searchResults = await Promise.all(searchPromises);
```

### 影响

- **性能**: 慢 13 倍
- **用户体验**: 长时间等待

---

## E002: 轮询无超时 | 🔴 严重 | 高频

### 问题

轮询状态时没有设置最大尝试次数，可能无限执行。

### 快速检查

❓ **轮询是否设置了 `maxAttempts`？**
❓ **失败/超时是否 `clearInterval`？**

### 错误示例

```javascript
// ❌ 错误：没有超时机制
setInterval(async () => {
  const data = await fetchStatus(scanId);
  if (data.status === 'completed') {
    clearInterval(scanPollInterval); // 只在成功时清理
    updateUI(data);
  }
}, 2000);
```

### 正确做法

```javascript
// ✅ 正确：带超时和错误处理
function pollStatus(scanId, maxAttempts = 30) {
  let attempts = 0;
  scanPollInterval = setInterval(async () => {
    attempts++;
    if (attempts > maxAttempts) {
      clearInterval(scanPollInterval);
      showError('轮询超时');
      return;
    }
    try {
      const data = await fetchStatus(scanId);
      if (data.status === 'completed' || data.status === 'failed') {
        clearInterval(scanPollInterval);
        updateUI(data);
      }
    } catch (error) {
      clearInterval(scanPollInterval);
      showError(error.message);
    }
  }, 2000);
}
```

### 影响

- **资源泄漏**: 无限轮询
- **浏览器卡死**: 内存占用持续增长

---

## E003: 错误未重新抛出 | 🔴 严重 | 中频

### 问题

在 `catch` 块中捕获错误但没有重新抛出，导致调用者不知道失败了。

### 快速检查

❓ **`catch` 块是否 `throw error`？**

### 错误示例

```javascript
// ❌ 错误：吞掉了错误
async function fetchUser(id) {
  try {
    return await fetch(`/api/users/${id}`).then((r) => r.json());
  } catch (error) {
    console.error('获取失败:', error); // 只记录，没有抛出
    // 函数返回 undefined，调用者不知道失败了
  }
}
```

### 正确做法

```javascript
// ✅ 正确：重新抛出错误
async function fetchUser(id) {
  try {
    return await fetch(`/api/users/${id}`).then((r) => r.json());
  } catch (error) {
    console.error('获取失败:', error);
    throw new Error(`无法获取用户 ${id}: ${error.message}`);
  }
}
```

### 影响

- **静默失败**: 调用者不知道出错了
- **数据不一致**: 使用 undefined 继续执行

---

## E004: SQL 未用 CTE | 🟡 中等 | 中频

### 问题

对大表先 JOIN 再过滤，导致全表扫描。

### 快速检查

❓ **是否先用 CTE 过滤大表再 JOIN？**

### 错误示例

```sql
-- ❌ 错误：先 JOIN 再过滤（扫描全表）
SELECT b.*, u.energy_change
FROM daaf_bot_revenue_snapshots b
LEFT JOIN user_energy_bot_usage_logs u
  ON b.bot_id = u.bot_id
  AND b.user_id = u.user_id
WHERE b.snapshot_date = '2024-01-15';  -- 过滤发生在 JOIN 后
```

### 正确做法

```sql
-- ✅ 正确：用 CTE 先过滤再 JOIN
WITH filtered_snapshots AS (
  SELECT *
  FROM daaf_bot_revenue_snapshots
  WHERE snapshot_date = '2024-01-15'  -- 先过滤
)
SELECT b.*, u.energy_change
FROM filtered_snapshots b
LEFT JOIN user_energy_bot_usage_logs u
  ON b.bot_id = u.bot_id
  AND b.user_id = u.user_id;
```

### 影响

- **性能**: 慢 10-100 倍
- **数据库负载**: CPU 和内存占用高

---

## E007: 资源泄漏 | 🔴 严重 | 中频

### 问题

只在成功路径清理资源，失败时忘记清理。

### 快速检查

❓ **所有退出路径都清理资源了吗？**

### 错误示例

```javascript
// ❌ 错误：只在成功时清理
async function processData() {
  startLoading();
  try {
    const data = await fetchData();
    processResults(data);
    stopLoading(); // 只在成功时清理
  } catch (error) {
    showError(error); // 失败时没有 stopLoading()
  }
}
```

### 正确做法

```javascript
// ✅ 正确：所有路径都清理
async function processData() {
  startLoading();
  try {
    const data = await fetchData();
    processResults(data);
  } catch (error) {
    showError(error);
  } finally {
    stopLoading(); // 所有路径都清理
  }
}
```

### 影响

- **UI 卡住**: Loading 动画不消失
- **内存泄漏**: 定时器/监听器没有清理
- **文件句柄泄漏**: 文件没有关闭

---

## 📋 编码前检查清单

在写代码前，快速过一遍：

- [ ] 多个异步操作 → 用 `Promise.all()` 并行
- [ ] 轮询 → 设置 `maxAttempts` 超时
- [ ] `catch` 块 → `throw error` 重新抛出
- [ ] SQL JOIN → 先 CTE 过滤再 JOIN
- [ ] 资源清理 → 用 `finally` 确保所有路径清理

---

## 📚 完整错误库

**所有 15 个错误模式**: `errors/ERROR_CATALOG.md`

包含：

- E001-E015 完整案例
- 根因分析
- 测试用例
- 修复方案
- 预防措施

---

**版本**: v1.0
**来源**: ERROR_CATALOG.md 精选
**更新**: 2026-02-05
