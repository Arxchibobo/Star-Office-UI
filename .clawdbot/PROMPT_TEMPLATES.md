# Prompt Template for Agent Tasks

## 基础模板

```
CONTEXT:
[业务背景、为什么需要这个功能、客户是谁]

TASK:
[具体要实现什么功能]

FILES TO MODIFY:
- src/api/[filename].ts
- src/components/[component].tsx
- tests/[test-file].test.ts

CONSTRAINTS:
- Don't modify [某些文件]
- Keep the existing API structure
- Follow the coding style in [reference-file]

DEFINITION OF DONE:
- Feature implemented and working
- Tests added and passing
- TypeScript types correct
- PR created with screenshot (if UI changes)

TECHNICAL DETAILS:
[任何技术细节、API 规范、数据结构等]
```

## 示例 1: 后端功能

```
CONTEXT:
Customer (Agency X) needs to save and reuse email templates. Currently they have to recreate configurations every time.

TASK:
Add a template system that lets users save their current email configuration as a template, and load templates later.

FILES TO MODIFY:
- src/api/templates.ts (create new)
- src/types/template.ts (create new)
- src/routes/api.ts (add new routes)
- tests/templates.test.ts (create new)

CONSTRAINTS:
- Don't change the existing email sending logic
- Templates should be per-user (not global)
- Use the existing database schema pattern

DEFINITION OF DONE:
- POST /api/templates - save template
- GET /api/templates - list user's templates
- GET /api/templates/:id - get specific template
- DELETE /api/templates/:id - delete template
- All endpoints tested
- TypeScript types defined
- Database migration included

TECHNICAL DETAILS:
Template schema:
{
  id: string
  userId: string
  name: string
  config: EmailConfig  // existing type
  createdAt: Date
  updatedAt: Date
}
```

## 示例 2: 前端 UI

```
CONTEXT:
Users are confused by the current dashboard layout. They want to see their key metrics at a glance.

TASK:
Redesign the dashboard to show:
1. Total emails sent (this month)
2. Open rate
3. Click rate
4. Recent campaigns (list)

FILES TO MODIFY:
- src/pages/Dashboard.tsx
- src/components/MetricCard.tsx (create new)
- src/hooks/useDashboardStats.ts (create new)
- src/styles/dashboard.css

CONSTRAINTS:
- Keep the existing sidebar navigation
- Use the existing design system (colors, spacing)
- Must be mobile-responsive

DEFINITION OF DONE:
- Dashboard shows 3 metric cards at top
- Campaign list below with infinite scroll
- Loading states handled
- Error states handled
- Screenshot included in PR
- Works on mobile (< 768px width)

TECHNICAL DETAILS:
API endpoint already exists: GET /api/stats/dashboard
Returns: { emailsSent: number, openRate: number, clickRate: number, recentCampaigns: Campaign[] }
```

## 示例 3: Bug Fix

```
CONTEXT:
Customers are reporting that webhook retries aren't working. When a webhook fails, we should retry up to 3 times with exponential backoff, but it's only trying once.

TASK:
Fix the webhook retry logic.

FILES TO INVESTIGATE:
- src/services/webhook.ts
- src/workers/webhook-retry.ts
- tests/webhook.test.ts

CONSTRAINTS:
- Don't change the webhook payload format
- Maintain backward compatibility

DEFINITION OF DONE:
- Retries work (3 attempts with backoff: 1s, 5s, 15s)
- Existing tests still pass
- New test added for retry logic
- No breaking changes

TECHNICAL DETAILS:
Current code is in src/services/webhook.ts:sendWebhook()
Should use the retry utility in src/utils/retry.ts
Check git blame to see when this broke.
```

## 示例 4: Refactoring

```
CONTEXT:
The billing code has grown messy. Multiple files duplicate logic for calculating costs.

TASK:
Refactor billing calculation into a single, testable module.

FILES TO MODIFY:
- src/billing/calculator.ts (create new - centralized logic)
- src/api/checkout.ts (use new calculator)
- src/api/invoices.ts (use new calculator)
- src/workers/billing-sync.ts (use new calculator)
- tests/billing-calculator.test.ts (create comprehensive tests)

CONSTRAINTS:
- Don't change any API responses or database schemas
- Behavior must remain identical (no logic changes)
- This is pure refactoring

DEFINITION OF DONE:
- All billing calculation in one place
- All call sites use the new module
- 100% test coverage on calculator
- All existing tests still pass
- No behavior changes

TECHNICAL DETAILS:
Current logic duplicated in:
- checkout.ts:calculateTotal()
- invoices.ts:calculateInvoiceAmount()
- billing-sync.ts:syncAmount()

New calculator should expose:
- calculateSubtotal(items)
- calculateTax(subtotal, region)
- calculateDiscount(subtotal, coupon)
- calculateTotal(items, region, coupon)
```

## Tips for Writing Good Prompts

### ✅ DO:
- **Be specific** about files to modify
- **Include context** (why this matters, who needs it)
- **Define "done"** clearly
- **Mention constraints** (what NOT to do)
- **Provide technical details** (schemas, types, APIs)
- **Reference existing code** when possible

### ❌ DON'T:
- "Fix the bug" (too vague)
- "Make it better" (subjective)
- "Add a feature" (what feature?)
- Give contradictory instructions
- Assume agent knows your codebase structure

### 🎯 Pro Tips:

1. **Include file paths**: Agent needs to know where to start
2. **Show examples**: "Like how we did X in file Y"
3. **Break down big tasks**: "First do A, then B, finally C"
4. **Specify tests**: "Add test that covers [edge case]"
5. **UI changes**: "Like the design in [figma link / screenshot]"

## Advanced: Multi-Step Prompts

For complex tasks, break into phases:

```
PHASE 1: Database Schema
1. Add migration for `templates` table
2. Update Prisma schema
3. Run migration

PHASE 2: API Layer
1. Create types in src/types/template.ts
2. Implement CRUD in src/api/templates.ts
3. Add routes

PHASE 3: Tests
1. Unit tests for each endpoint
2. Integration test for full flow
3. Edge case tests (empty name, invalid userId, etc.)

PHASE 4: Documentation
1. Update API docs
2. Add JSDoc comments
3. Update CHANGELOG.md

IMPORTANT: Complete each phase fully before moving to next.
```

---

**Remember**: The better your prompt, the better the result. Invest time in writing clear, detailed prompts!
