# Claude-Reconstruction 使用手册（小波比执行版）

> 适用目标：你需要我在工程/设计/营销任务中“像高级工程师一样”交付。

---

## A. 开始前
- 先读：CLAUDE.md / CONTEXT_MANAGER.md / rules/core/work-mode.md
- 如果任务复杂：先规划，再确认，再执行
- 默认不提问，除非触发四类阻塞

---

## B. 任务类型 → 文档加载（默认路径）
- 开发/功能：rules/domain/coding.md + testing.md + git.md
- 设计/UI：design/DESIGN_MASTER_PERSONA.md + UI_DESIGN_STYLES_REFERENCE.md
- 营销/文案：vibe-marketing/VIBE_MARKETING_GUIDE.md + MARKETING_SKILLS_GUIDE.md
- 浏览器自动化：browser-automation-decision-tree.md
- 错误调试：errors/top-5-errors.md → ERROR_CATALOG.md

---

## C. 标准交付格式
每个任务交付包含：
1. 完成摘要（做了什么）
2. 关键决策（为何这么做）
3. 风险提示（如有）
4. 后续建议（如有）

---

## D. 高风险提醒（必须先问）
- 删除数据 / 强推分支 / 覆盖历史 / 不可逆操作

---

## E. 质量硬标准
- 代码：不可变、函数短、文件小、无 console.log
- 测试：TDD + 80%覆盖
- 安全：无硬编码密钥 + 输入校验
- UI：必须本地验证闭环（npm run dev → 视觉确认）

---

## F. 常用工作流模板

### 开发任务
1) 规划 TodoList
2) 展示计划 → 等确认
3) 实现 + 测试 + 自检
4) 交付总结

### 调试任务
1) 先查 Top 5 错误
2) 对照 ERROR_CATALOG 定位
3) 修复 + 补测试
4) 交付总结

### 设计任务
1) 需求深挖（真实意图）
2) 给 3 方案（安全/激进/理想）
3) 输出完整可运行实现

### PPT 任务
1) Nano Banana Pro → 页面图
2) Processing → 转场动画
3) PPT 组装 + 双格式导出

---

## G. 小波比执行偏好（可扩展）
- 默认输出中文
- 不改动现有文件，只写新文件
- 重大动作先请你确认

---

如需我把这些规则“固化成固定指令模板”，或做成“任务清单式”，告诉我。
