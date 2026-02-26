# Claude-Reconstruction 中文精炼速查（5分钟）

## 一句话定位
这是一个让 Claude Code **只加载必需文档 + 按工程化流程执行** 的系统，目标：更快、更稳、更少废话。

---

## 四步工作模式（必遵守）
1. 规划（TodoList）
2. 展示计划 → 等确认
3. 执行到底（不多问）
4. 总结验收

仅允许提问的4种情况：
- 缺关键凭证
- 多个对立方案
- 需求矛盾
- 不可逆高风险

---

## 5层架构
1. Delegation（专家代理）
2. Hooks（工具调用前后质量门）
3. Rules（编码/测试/安全/Git）
4. Workflow（计划-确认-执行-验收）
5. Context Manager（按需加载文档）

---

## 核心规则（必须记住）
- 编码：不可变、函数小于50行、文件<800行
- 测试：TDD + 80%覆盖
- 安全：无硬编码密钥、输入校验、无敏感泄露
- UI修改：必须本地验证闭环
- 数据库：事务 + 回滚 + 一致性验证

---

## 高频错误 Top 5
- E001 异步未并行（Promise.all）
- E002 轮询无超时
- E003 错误未抛出
- E004 SQL 未用 CTE
- E007 资源清理遗漏

---

## 快速路由
- 浏览器自动化 → capabilities/browser-automation-decision-tree.md
- 视频/Remotion → capabilities/REMOTION_TEMPLATES_LIBRARY.md
- 设计/UI → design/DESIGN_MASTER_PERSONA.md
- 营销/文案 → vibe-marketing/VIBE_MARKETING_GUIDE.md
- 错误调试 → errors/top-5-errors.md

---

## 快捷命令
- /commit /create-pr /write-tests /code-review
- pnpm install:config / pnpm verify / pnpm verify:hooks

---

若需要，我可以输出：
- 你的“日常任务路线图”版本
- 工程/设计/营销三线分支速查版
