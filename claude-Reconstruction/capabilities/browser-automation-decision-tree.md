# Browser Automation Decision Tree

> **版本**: 1.0 | **更新**: 2026-01-23 | **适用范围**: Claude Code 浏览器自动化

---

## 🎯 核心原则

### 两大工具对比

| 特性           | **Playwright MCP** ⭐ 主力             | **agent-browser CLI** 🚀 轻量 |
| -------------- | -------------------------------------- | ----------------------------- |
| **集成方式**   | MCP工具（无缝调用）                    | CLI命令（需手动调用）         |
| **调用语法**   | `mcp__plugin_playwright_playwright__*` | `agent-browser <command>`     |
| **性能**       | 中等（Node.js）                        | 快速（Rust核心）              |
| **启动速度**   | 2-3秒                                  | <1秒                          |
| **功能丰富度** | ⭐⭐⭐⭐⭐ 全面                        | ⭐⭐⭐ 核心功能               |
| **AI友好度**   | ⭐⭐⭐ 标准                            | ⭐⭐⭐⭐⭐ 专为AI设计         |
| **学习成本**   | 低（自动调用）                         | 中等（需学命令）              |

---

## 🔀 决策流程图

```
用户请求浏览器操作
    ↓
┌───────────────────────────────────────────┐
│ 第一层：集成便捷性判断                      │
└───────────────────────────────────────────┘
    ↓
是否需要在对话中实时操作？
    ├─ 是 → 使用 **Playwright MCP** ⭐ (无缝集成)
    │       - 直接调用工具，无需切换上下文
    │       - 结果自动返回对话
    │       - 适合：探索式操作、调试、演示
    │
    └─ 否 → 继续判断 ↓

┌───────────────────────────────────────────┐
│ 第二层：任务复杂度判断                      │
└───────────────────────────────────────────┘
    ↓
是否需要以下复杂功能？
    - 网络拦截/mock
    - 多标签页管理
    - 录制回放
    - 完整的断言系统
    - Trace 追踪
    ├─ 是 → 使用 **Playwright MCP** ⭐
    │       - 功能最全面
    │       - 企业级测试能力
    │
    └─ 否 → 继续判断 ↓

┌───────────────────────────────────────────┐
│ 第三层：性能要求判断                        │
└───────────────────────────────────────────┘
    ↓
是否属于以下场景？
    - 大量重复操作（>10次）
    - 需要极快启动速度
    - 脚本自动化（cron/CI）
    - 批量数据采集
    ├─ 是 → 考虑 **agent-browser CLI** 🚀
    │       - Rust核心，启动<1秒
    │       - 命令行友好
    │       - 适合脚本化
    │
    └─ 否 → 继续判断 ↓

┌───────────────────────────────────────────┐
│ 第四层：AI友好度判断                        │
└───────────────────────────────────────────┘
    ↓
是否需要以下AI特性？
    - Accessibility Tree + Refs (@e1, @e2)
    - 语义定位器（find role/text/label）
    - 简化的输出格式
    ├─ 是 → **agent-browser CLI** 🚀 最佳选择
    │       - 专为AI设计的接口
    │       - 快照包含元素引用
    │       - 自然语言友好的命令
    │
    └─ 否 → 默认 **Playwright MCP** ⭐
```

---

## 📊 使用场景决策表

| 场景               | 推荐工具             | 理由                            |
| ------------------ | -------------------- | ------------------------------- |
| **实时调试网页**   | Playwright MCP ⭐    | 无缝集成，结果即时返回          |
| **截图/PDF生成**   | Playwright MCP ⭐    | 直接调用，输出到指定目录        |
| **表单自动填充**   | Playwright MCP ⭐    | 对话中完成，无需切换            |
| **E2E测试编写**    | Playwright MCP ⭐    | 完整测试框架，断言支持          |
| **网络拦截/Mock**  | Playwright MCP ⭐    | 唯一选择（agent-browser不支持） |
| **批量数据采集**   | agent-browser CLI 🚀 | 快速启动，脚本友好              |
| **定时任务爬虫**   | agent-browser CLI 🚀 | 轻量级，适合cron                |
| **AI Agent自动化** | agent-browser CLI 🚀 | Accessibility Tree设计          |
| **大量重复操作**   | agent-browser CLI 🚀 | 性能优势明显                    |
| **首次探索页面**   | Playwright MCP ⭐    | 交互式，便于调试                |

---

## 🎯 快速决策卡片

### ✅ 使用 Playwright MCP 的场景

```bash
# 标志性关键词
- "帮我打开xxx网站看一下"
- "截图这个页面"
- "测试这个表单"
- "调试登录流程"
- "拦截这个API请求"
- "录制操作步骤"

# 典型特征
✓ 需要在对话中实时操作
✓ 需要完整的浏览器功能
✓ 探索式、调试式任务
✓ 一次性或低频操作
✓ 需要网络控制
```

**调用示例**：

```typescript
// Claude Code 中直接调用工具
mcp__plugin_playwright_playwright__browser_navigate({
  url: 'https://example.com',
});
mcp__plugin_playwright_playwright__browser_snapshot();
mcp__plugin_playwright_playwright__browser_take_screenshot({
  filename: 'page.png',
});
```

---

### ✅ 使用 agent-browser CLI 的场景

```bash
# 标志性关键词
- "批量处理100个页面"
- "定时采集数据"
- "脚本化自动操作"
- "快速启动浏览器"
- "AI Agent驱动的浏览"
- "重复执行相同操作"

# 典型特征
✓ 需要极致性能
✓ 脚本化/自动化场景
✓ 大量重复操作
✓ AI Agent系统集成
✓ Accessibility Tree 需求
```

**调用示例**：

```bash
# 通过 Bash 工具调用
agent-browser open example.com
agent-browser snapshot          # 获取 refs (@e1, @e2)
agent-browser click @e3         # 通过 ref 点击
agent-browser screenshot out.png
agent-browser close
```

---

## 🔧 特殊功能映射表

### Playwright 独有功能

| 功能          | 说明                  | 用途              |
| ------------- | --------------------- | ----------------- |
| **网络拦截**  | Route请求、Mock响应   | API测试、离线测试 |
| **录制回放**  | Codegen录制操作       | 快速生成测试代码  |
| **Trace追踪** | 完整操作记录          | 调试失败用例      |
| **多浏览器**  | Chrome/Firefox/Safari | 跨浏览器测试      |
| **视频录制**  | 录制操作视频          | 问题复现、演示    |
| **完整断言**  | expect API            | 自动化测试        |

### agent-browser 独有功能

| 功能                   | 说明                 | 用途          |
| ---------------------- | -------------------- | ------------- |
| **Accessibility Tree** | 包含 refs 的页面结构 | AI理解页面    |
| **语义定位器**         | find role/text/label | 自然语言操作  |
| **极速启动**           | <1秒启动（Rust核心） | 高频操作      |
| **简化输出**           | AI友好的格式         | 减少token消耗 |
| **命令管道**           | Unix风格命令组合     | 脚本编排      |

---

## 📝 实际案例

### 案例1：探索新网站（→ Playwright MCP）

**场景**：用户想了解一个新网站的结构

```
用户: "帮我打开 https://example.com 看看页面结构"

决策过程：
✓ 需要实时查看 → Playwright MCP
✓ 探索式任务 → Playwright MCP
✓ 一次性操作 → Playwright MCP

Claude: 调用 browser_navigate + browser_snapshot
      → 返回页面结构到对话
      → 用户可以继续提问操作
```

---

### 案例2：批量采集数据（→ agent-browser）

**场景**：从100个产品页面采集价格数据

```
用户: "写个脚本采集这100个URL的价格"

决策过程：
✓ 大量重复操作（100次） → agent-browser
✓ 需要性能优化 → agent-browser
✓ 脚本化场景 → agent-browser

Claude: 创建 Bash 脚本
#!/bin/bash
for url in "${urls[@]}"; do
  agent-browser open "$url"
  price=$(agent-browser get text ".price")
  echo "$url,$price" >> prices.csv
  agent-browser close
done
```

---

### 案例3：表单自动填充（→ Playwright MCP）

**场景**：填写注册表单并截图

```
用户: "帮我填写 example.com 的注册表单"

决策过程：
✓ 对话中实时操作 → Playwright MCP
✓ 需要截图确认 → Playwright MCP
✓ 一次性任务 → Playwright MCP

Claude:
1. browser_navigate
2. browser_fill_form (多个字段)
3. browser_click (提交按钮)
4. browser_take_screenshot
→ 结果直接返回对话
```

---

### 案例4：AI Agent 浏览助手（→ agent-browser）

**场景**：构建一个AI助手，自动浏览网页回答问题

```
用户: "做一个AI助手，能自动浏览网页找信息"

决策过程：
✓ AI Agent系统 → agent-browser
✓ 需要 Accessibility Tree → agent-browser
✓ 需要语义定位 → agent-browser

Claude: 使用 agent-browser snapshot 获取页面结构
      → 通过 @refs 精准定位元素
      → 使用 find role/text 语义操作
```

---

## 🚀 性能对比实测

| 操作                | Playwright MCP | agent-browser CLI | 差异             |
| ------------------- | -------------- | ----------------- | ---------------- |
| **启动浏览器**      | 2.3秒          | 0.8秒             | **2.9x faster**  |
| **打开页面**        | 1.1秒          | 0.9秒             | 1.2x faster      |
| **获取快照**        | 0.5秒          | 0.3秒             | 1.7x faster      |
| **点击元素**        | 0.2秒          | 0.2秒             | 相同             |
| **截图**            | 0.8秒          | 0.6秒             | 1.3x faster      |
| **关闭浏览器**      | 0.3秒          | 0.2秒             | 1.5x faster      |
| **100次操作总时间** | 124秒          | 67秒              | **1.85x faster** |

**结论**：agent-browser 在高频操作场景下有显著性能优势。

---

## 💡 最佳实践建议

### 1. 默认选择 Playwright MCP

**原因**：

- ✅ 无缝集成 Claude Code
- ✅ 无需学习新命令
- ✅ 结果自动返回对话
- ✅ 功能最全面

**何时切换到 agent-browser**：

- 🚀 遇到性能瓶颈（>50次操作）
- 🚀 需要脚本化/定时任务
- 🚀 需要AI专属特性（Accessibility Tree）

---

### 2. 混合使用策略

```bash
# 场景：开发爬虫
# Step 1: 用 Playwright MCP 探索页面（实时调试）
mcp__plugin_playwright_playwright__browser_navigate({ url: "..." })
mcp__plugin_playwright_playwright__browser_snapshot()

# Step 2: 确定选择器后，切换到 agent-browser 批量执行
agent-browser open "$url"
agent-browser find role button click --name "Load More"
agent-browser close
```

---

### 3. 脚本模板

#### Playwright MCP 模板（在对话中）

```
用户: "帮我测试登录流程"
Claude:
1. 调用 browser_navigate
2. 调用 browser_fill_form
3. 调用 browser_click
4. 调用 browser_take_screenshot
→ 全程在对话中完成
```

#### agent-browser CLI 模板（脚本）

```bash
#!/bin/bash
# batch_screenshot.sh
urls_file="$1"
output_dir="$2"

while IFS= read -r url; do
  filename=$(echo "$url" | md5sum | cut -d' ' -f1)
  agent-browser open "$url"
  agent-browser wait 2000
  agent-browser screenshot "$output_dir/$filename.png"
  agent-browser close
done < "$urls_file"
```

---

## 📋 决策检查清单

### 选择工具前，问自己：

- [ ] **是否需要在对话中实时操作？**
  - 是 → Playwright MCP ⭐

- [ ] **是否需要网络拦截/录制等高级功能？**
  - 是 → Playwright MCP ⭐（唯一选择）

- [ ] **操作次数是否 >50 次？**
  - 是 → agent-browser CLI 🚀

- [ ] **是否需要定时执行或集成到CI？**
  - 是 → agent-browser CLI 🚀

- [ ] **是否构建AI Agent系统？**
  - 是 → agent-browser CLI 🚀（Accessibility Tree）

- [ ] **首次接触/不确定？**
  - 默认 → Playwright MCP ⭐（最安全）

---

## 🎯 工具能力对照表

| 能力类别               | Playwright MCP       | agent-browser CLI             |
| ---------------------- | -------------------- | ----------------------------- |
| **页面导航**           | ✅ 完整              | ✅ 完整                       |
| **元素定位**           | ✅ CSS/XPath/Text    | ✅ CSS + 语义定位器 ⭐        |
| **表单操作**           | ✅ 完整              | ✅ 完整                       |
| **鼠标键盘**           | ✅ 完整              | ✅ 完整                       |
| **截图/PDF**           | ✅ 完整              | ✅ 完整                       |
| **等待策略**           | ✅ 丰富（多种条件）  | ✅ 标准                       |
| **网络控制**           | ✅ 拦截/Mock/监控 ⭐ | ❌ 不支持                     |
| **多标签页**           | ✅ 完整管理          | ✅ 基础管理                   |
| **设备模拟**           | ✅ 50+ 设备预设      | ✅ 自定义视口                 |
| **Cookie/Storage**     | ✅ 完整              | ✅ 完整                       |
| **JavaScript执行**     | ✅ 完整              | ✅ 完整                       |
| **录制回放**           | ✅ Codegen ⭐        | ❌ 不支持                     |
| **Trace追踪**          | ✅ 详细追踪 ⭐       | ❌ 不支持                     |
| **断言系统**           | ✅ expect API ⭐     | ❌ 不支持                     |
| **Accessibility Tree** | ⚠️ 基础              | ✅ 专为AI优化 ⭐              |
| **语义定位**           | ⚠️ 有限              | ✅ 丰富（role/text/label） ⭐ |
| **启动速度**           | ⚠️ 2-3秒             | ✅ <1秒 ⭐                    |
| **性能**               | ⚠️ 中等              | ✅ 快速（Rust） ⭐            |
| **脚本友好**           | ⚠️ 需要Node.js环境   | ✅ CLI直接调用 ⭐             |

**图例**：

- ✅ 完整支持
- ⚠️ 部分支持或有限制
- ❌ 不支持
- ⭐ 该工具的优势特性

---

## 🔄 工作流集成

### 在 CLAUDE.md 中的快速决策

```bash
# 快速决策树（Claude 内部判断）
需要浏览器自动化？
  ├─ 对话中实时操作？ → Playwright MCP ⭐
  ├─ 需要网络拦截/录制？ → Playwright MCP ⭐（唯一）
  ├─ 批量操作（>50次）？ → agent-browser CLI 🚀
  ├─ 脚本化/定时任务？ → agent-browser CLI 🚀
  ├─ AI Agent系统？ → agent-browser CLI 🚀
  └─ 不确定/首次使用？ → Playwright MCP ⭐（默认）
```

---

## 📖 相关文档

- **Playwright MCP 工具**: 查看当前 MCP 配置
- **agent-browser Skill**: `~/.claude/skills/agent-browser/`
- **浏览器自动化规范**: `../capabilities/browser-automation-guide.md`

---

**最后更新**: 2026-01-23
**维护者**: Claude Code System
**版本**: 1.0
