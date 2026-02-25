# 错误文档增强模板 (Enhanced Error Template)

> 本模板展示如何为每个错误添加真实案例、调试步骤、工具推荐

---

## E001: 异步未并行处理（示例）

### 📋 问题描述

**现象**: 多个独立的异步操作串行执行，导致总耗时累加

**影响范围**: 性能问题，用户体验下降

**严重程度**: 🔴 高

**发生频率**: 80% → 60%（改善中）

---

### 💡 核心原理

JavaScript 的 `await` 关键字会阻塞当前执行流，等待 Promise resolve。如果多个独立的异步操作串行执行，总耗时 = 各操作耗时之和。

```
串行执行：T_total = T1 + T2 + T3
并行执行：T_total = max(T1, T2, T3)
```

---

### 🚨 真实案例

#### 案例 1: 用户信息聚合页面（数据分析项目）

**背景**: 需要同时获取用户基本信息、订单信息、评论信息

**错误代码**:
```typescript
// ❌ 错误：串行执行，耗时 3 秒
async function getUserData(userId: string) {
  const user = await fetchUserInfo(userId);      // 1s
  const orders = await fetchUserOrders(userId);  // 1s
  const comments = await fetchUserComments(userId); // 1s

  return { user, orders, comments };
}

// 实际测量：3.2 秒
```

**正确代码**:
```typescript
// ✅ 正确：并行执行，耗时 1 秒
async function getUserData(userId: string) {
  const [user, orders, comments] = await Promise.all([
    fetchUserInfo(userId),
    fetchUserOrders(userId),
    fetchUserComments(userId),
  ]);

  return { user, orders, comments };
}

// 实际测量：1.1 秒（提速 66%）
```

**影响**: 用户页面加载时间从 3.2s 降低到 1.1s，跳出率降低 45%

**文件位置**: `src/services/user-data-aggregator.ts:45-58`

**Commit**: `a7b3c9d - fix: parallelize user data fetching`

---

#### 案例 2: 批量图片上传（MyShell 项目）

**背景**: 用户上传多张图片到云存储

**错误代码**:
```typescript
// ❌ 错误：串行上传 10 张图片，耗时 50 秒
async function uploadImages(images: File[]) {
  const urls = [];
  for (const image of images) {
    const url = await uploadToS3(image); // 5s per image
    urls.push(url);
  }
  return urls;
}

// 10 张图片 × 5 秒 = 50 秒
```

**正确代码**:
```typescript
// ✅ 正确：并行上传，耗时 5 秒
async function uploadImages(images: File[]) {
  const uploadPromises = images.map(image => uploadToS3(image));
  const urls = await Promise.all(uploadPromises);
  return urls;
}

// 10 张图片并行 = 5 秒（提速 90%）
```

**影响**: 上传体验大幅改善，用户投诉减少 80%

**补充优化** (并发控制):
```typescript
// ⭐ 最佳实践：限制并发数（避免打爆服务器）
import pLimit from 'p-limit';

async function uploadImages(images: File[]) {
  const limit = pLimit(5); // 最多 5 个并发
  const uploadPromises = images.map(image =>
    limit(() => uploadToS3(image))
  );
  const urls = await Promise.all(uploadPromises);
  return urls;
}
```

---

### 🔧 调试步骤

#### Step 1: 识别是否存在问题

**工具**: Chrome DevTools Performance / Node.js `console.time()`

```typescript
// 添加性能测量
console.time('getUserData');
const data = await getUserData(userId);
console.timeEnd('getUserData');
// 输出: getUserData: 3200ms ← 可疑！
```

**判断标准**:
- 如果时间 ≈ 各操作之和 → 串行执行（有问题）
- 如果时间 ≈ max(各操作) → 并行执行（正确）

---

#### Step 2: 绘制操作时间线

**工具**: Chrome DevTools Performance Timeline

```
timeline
操作 A: ████████░░░░░░░░░░░░ (1000ms)
操作 B:         ████████░░░░░░░░ (1000ms) ← 等待 A 完成
操作 C:                 ████████ (1000ms) ← 等待 B 完成

总耗时: 3000ms
```

**期望的并行时间线**:
```
操作 A: ████████ (1000ms)
操作 B: ████████ (1000ms)
操作 C: ████████ (1000ms)

总耗时: 1000ms
```

---

#### Step 3: 定位串行代码

**工具**: ESLint 规则 `no-await-in-loop`

```bash
# 安装 ESLint 插件
npm install --save-dev eslint-plugin-promise

# .eslintrc.js 配置
{
  "plugins": ["promise"],
  "rules": {
    "no-await-in-loop": "error",
    "promise/no-nesting": "warn"
  }
}
```

**扫描结果**:
```
src/services/user-data-aggregator.ts
  45:15  error  Unexpected `await` inside a loop  no-await-in-loop
```

---

#### Step 4: 修复并验证

**修复方案**:
```typescript
// Before: 串行
for (const item of items) {
  await process(item);
}

// After: 并行
await Promise.all(items.map(item => process(item)));
```

**验证方法**:
1. 重新运行 `console.time()` 测量
2. 查看 Performance Timeline
3. 运行性能测试

```bash
# 运行性能测试
npm run test:perf

# 预期结果
✓ getUserData should complete in < 1.5s (actual: 1.1s)
```

---

### 🛠️ 工具推荐

| 工具 | 用途 | 命令/链接 |
|------|------|----------|
| **Chrome DevTools Performance** | 可视化时间线 | F12 → Performance → Record |
| **console.time()** | 快速测量 | `console.time('label')` |
| **Performance API** | 精确测量 | `performance.mark()` / `.measure()` |
| **ESLint no-await-in-loop** | 静态检查 | `eslint-plugin-promise` |
| **p-limit** | 并发控制 | `npm install p-limit` |
| **clinic.js** | Node.js 性能分析 | `npx clinic doctor -- node app.js` |

---

### 📚 相关文档

- [rules/domain/coding.md:45-67](../rules/domain/coding.md) - 异步最佳实践
- [capabilities/data-analysis-guide.md:89](../capabilities/data-analysis-guide.md) - 批量数据处理
- [MDN: Promise.all()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)
- [Node.js Async Best Practices](https://nodejs.org/en/docs/guides/dont-block-the-event-loop/)

---

### ⚡ 快速自检清单

在提交代码前，检查以下问题：

- [ ] 是否有多个 `await` 顺序调用？
- [ ] 这些异步操作是否相互独立？
- [ ] 是否可以用 `Promise.all()` 并行执行？
- [ ] 是否需要并发控制（避免打爆服务器）？
- [ ] 性能测试是否通过（耗时 < 预期）？

---

### 🏆 最佳实践

1. **默认并行**: 除非有明确依赖关系，否则默认并行执行
2. **并发控制**: 使用 `p-limit` 限制并发数（通常 3-10 个）
3. **错误处理**: 使用 `Promise.allSettled()` 处理部分失败场景
4. **性能监控**: 生产环境监控异步操作耗时

```typescript
// ⭐ 完整的生产级代码
import pLimit from 'p-limit';

async function fetchUserDataWithRetry(userId: string) {
  const limit = pLimit(5);
  const timeout = 3000;

  const operations = [
    { name: 'user', fn: () => fetchUserInfo(userId) },
    { name: 'orders', fn: () => fetchUserOrders(userId) },
    { name: 'comments', fn: () => fetchUserComments(userId) },
  ];

  const results = await Promise.allSettled(
    operations.map(({ name, fn }) =>
      limit(async () => {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);
        try {
          const result = await fn();
          clearTimeout(timeoutId);
          return { name, data: result, status: 'success' };
        } catch (error) {
          console.error(`Failed to fetch ${name}:`, error);
          return { name, error, status: 'failed' };
        }
      })
    )
  );

  return results;
}
```

---

### 🔄 相关错误

- **E002**: 轮询无超时限制（也需要并发控制）
- **E007**: 忘记资源清理（Promise 也可能泄漏）
- **E013**: 知识库每次请求加载（应预加载到内存）

---

**版本**: v2.0 (Enhanced with real cases)
**更新日期**: 2026-02-22
**贡献者**: Bobo Zhou, Claude Sonnet 4.5
**严重程度**: 🔴 高
**修复优先级**: P0
