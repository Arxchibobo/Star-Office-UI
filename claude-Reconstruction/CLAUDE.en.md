# CLAUDE.md v5.2

> **Core Principles**: Plan → Confirm → Execute → Deliver
> **Smart Loading**: Load only essential documents, keep context clean
> **Capability Evolution**: Make future similar tasks easier (auto-activated each conversation)

---

## 🧬 Capability Evolution Mode (Auto-Activated)

**At the start of every conversation**, capability evolution mode is automatically activated:

- Identify reusable patterns → Abstract into capability profiles → Internalize into decision layer
- Prove evolution effectiveness through **faster, more stable, fewer steps**
- Let results speak, not process reports

**Detailed Documentation**: `rules/core/capability-evolution.md`

---

## 🎯 Workflow (4 Steps)

```
1️⃣ Receive Task → Create TodoList
2️⃣ Present Plan → User Confirms
3️⃣ Execute to Completion (No Questions) → Self-Decide
4️⃣ Summarize & Deliver → Hand Over Results
```

**Detailed Documentation**: `rules/core/work-mode.md`

---

## 🚨 Only 4 Situations to Ask Questions

1. ❗ **Missing Critical Credentials** - Database passwords, API keys
2. ❗ **Multiple Conflicting Solutions** - Cannot determine from codebase
3. ❗ **Contradictory Requirements** - User requirements conflict
4. ❗ **Irreversible High Risk** - Deleting production data, force push

**Self-decide all other cases**: File naming, code style, dependency versions, UI details, etc.

**Detailed Documentation**: `rules/core/blocking-rules.md`

---

## 🤖 Smart Context Loading

### System Automatically Identifies Task Type and Loads Documents on Demand

**You don't need to worry about what's loaded** - the system automatically selects based on your needs.

| Task Keywords               | Auto-Loaded Documents           | Est. Size |
| --------------------------- | ------------------------------- | --------- |
| Browser, automation, scrape | Browser automation guide        | ~15KB     |
| Video, Remotion, animation  | Video creation guide            | ~25KB     |
| Data, analysis, SQL         | Data analysis guide             | ~20KB     |
| Design, UI, interface       | Design guide                    | ~30KB     |
| Marketing, copywriting, SEO | Marketing guide                 | ~35KB     |
| Development, code, feature  | Coding rules + Eng workflows    | ~20KB     |
| Migration, TDD, component   | Engineering workflows (advanced)| ~8KB      |
| Error, bug, debugging       | Error catalog                   | ~12KB     |
| Security, vulnerability     | Security rules                  | ~15KB     |

**System Documentation**: `CONTEXT_MANAGER.md`

---

## 🚀 Quick Start (I Want to...)

### Don't Know Which Tool to Use?

👉 **Check Quick Decision Tree**: `index/task-router.md`

- Find what you need in 30 seconds
- Categorized by task type
- Includes quick links to all capabilities

### Common Capabilities Quick Jump

| Capability           | Quick Link                                         |
| -------------------- | -------------------------------------------------- |
| 🌐 Browser Automation| `capabilities/browser-automation/decision-tree.md` |
| 🎬 Video Creation    | Project-level `.claude/rules/remotion-auto-production.md` |
| 📊 Data Analysis     | `capabilities/data-analysis-guide.md`              |
| 🎨 UI Design         | `design/DESIGN_MASTER_PERSONA.md`                  |
| 📝 Marketing Content | `vibe-marketing/VIBE_MARKETING_GUIDE.md`           |
| 🐛 Error Debugging   | `errors/top-5-errors.md`                           |
| 🤖 Agent Orchestration| `rules/agents.md`                                 |

---

## ⚠️ Top 5 Common Errors (Quick Reference)

| Error    | Core Issue           | Quick Check                                   |
| -------- | -------------------- | --------------------------------------------- |
| **E001** | Async not parallel   | Are multiple async ops using `Promise.all()`? |
| **E002** | Polling no timeout   | Does polling have `maxAttempts` set?          |
| **E003** | Error not re-thrown  | Does `catch` block `throw error`?             |
| **E004** | SQL without CTE      | JOIN then filter → Use CTE to pre-filter      |
| **E007** | Resource leak        | Do all exit paths clean up resources?         |

**Complete Error Catalog**: `errors/ERROR_CATALOG.md` (E001-E015)

---

## 🧠 Core Methodology (Long Tasks)

### Three-File Pattern

```
task_plan.md     - Task planning and progress tracking
notes.md         - Research notes and discoveries
[deliverable].md - Final output
```

**Key**: Re-read `task_plan.md` before each major decision point

### Phase Gate Control

```
Phase 1: Requirements Understanding → [User confirms "ready"]
Phase 2: Design Solution → [Confirm]
Phase 3: Implement Code
```

**Principle**: Never proceed to next phase until user explicitly confirms

---

## 🔧 Capability Library (Load on Demand)

### MCP Servers (External Data)

| Task         | MCP        | Documentation                      |
| ------------ | ---------- | ---------------------------------- |
| SQL Queries  | bytebase   | `capabilities/mcp-servers.md`      |
| Browser      | playwright | `capabilities/browser-automation/` |
| Monitoring   | honeycomb  | `capabilities/mcp-servers.md`      |

### Skills (Automated Tasks)

| Category     | Examples            | Documentation                            |
| ------------ | ------------------- | ---------------------------------------- |
| Git Workflow | /commit, /create-pr | `capabilities/skills-guide.md`           |
| Test Gen     | /write-tests        | Same as above                            |
| UI Design    | ui-ux-pro-max       | Same as above                            |
| Marketing    | 24 Pro Skills       | `capabilities/MARKETING_SKILLS_GUIDE.md` |

**Complete List**: `capabilities/skills-guide.md` (81 Skills)

---

## 📚 Complete Documentation Navigation

### Index Layer (Quick Find)

- `index/task-router.md` - Task routing decision tree (30s to find tools)
- `index/capabilities-index.md` - Capability index
- `index/tools-index.md` - Tools index
- `index/error-patterns-index.md` - Error patterns index

### Rules Library (Auto-Loaded)

- `rules/core/` - Core rules (always loaded)
  - `capability-evolution.md` - **Capability Evolution Mode (auto-activated each conversation)**
  - `blocking-rules.md`, `work-mode.md`
- `rules/domain/` - Domain rules (load on demand)
  - `coding.md` (includes Common Patterns), `testing.md`, `security.md`, `git.md`, `engineering-workflows.md`
- `rules/agents.md` - Agent orchestration
- `rules/hooks.md` - Hooks system
- `rules/performance.md` - Performance optimization

### Capability Library (Load on Demand)

- `capabilities/browser-automation/` - Browser automation
- `capabilities/video-creation/` - Video creation
- `capabilities/data-analysis/` - Data analysis
- `design/` - UI design
- `vibe-marketing/` - Marketing content

### Error Library (Load on Demand)

- `errors/top-5-errors.md` - Top 5 common errors quick reference
- `errors/ERROR_CATALOG.md` - Complete error catalog (E001-E015)

### Knowledge Base (Reference)

- `KNOWLEDGE_MAP.md` - Knowledge graph (12 Mermaid diagrams)
- `QUICK_REFERENCE.md` - One-page cheat sheet
- `INDEX.md` - Complete index of all documents

---

## 🔧 Development Environment

- **OS**: Windows 10.0.26200 | **Shell**: Git Bash
- **Path Format**: Windows (use forward slashes in Git Bash)
- **Current Project**: Data Analysis and Automation (DAA)
- **Tech Stack**: TypeScript + PostgreSQL (Vercel) + MySQL (my_shell_prod)

---

## 👁️ Visual Verification

After UI modifications (especially 3D visualization or connection lines), must:

1. Start app with `npm run dev`
2. Navigate to affected components
3. Verify visual elements render correctly with no console errors
4. **Only mark task complete after confirming correctness**

---

## 🔷 TypeScript First

This codebase uses TypeScript as the primary language. Ensure all new files use .ts/.tsx extensions and maintain strict type safety.

---

## 🗄️ Database Operations

All database queries and migrations use Bytebase MCP server (`mcp__mcphub__bytebase-execute_sql`). Multi-table changes must execute in a single transaction with rollback logic.

---

## 🔬 Engineering Workflows

| Task Type       | Must Execute                                      |
| --------------- | ------------------------------------------------- |
| UI Changes      | Verification loop (start app → visual confirm)    |
| New Features    | Sequential planning → breakdown → dependency mark |
| Database Changes| Transactional migration → rollback → consistency  |
| Complex Features| Full TDD cycle (RED → GREEN → property tests)     |
| Core Components | Self-healing mode (regression + responsive + a11y)|

**Detailed Documentation**: `rules/domain/engineering-workflows.md`

---

## 📊 Context Usage Optimization

### Before (v4.2)

```
CLAUDE.md: 20KB
+ Multiple rule files: 30KB
+ Partial capability docs: 70KB
= Total: 120KB (60% context)
```

### After (v5.1 - Cleaned Up)

```
CLAUDE.md: 5KB
+ Core rules (core/ + domain/): ~18KB
+ agents + hooks + performance: ~4KB
= Total: ~27KB (global rules, excluding project-level)
```

**Savings**: Deleted ~50KB duplicate/invalid content (16 duplicate files + delegator 22KB + remotion 24KB moved to project-level)

---

## 🎯 Context Engineering Core

### Smart Loading Principles

1. **Layer 0** (always loaded): CLAUDE.md + Core rules (15KB)
2. **Layer 1** (task identification): Task Router (3KB)
3. **Layer 2** (load on demand): Relevant capability docs (15-30KB)
4. **Layer 3** (exact match): Specific cases/templates (on demand)

### What Do You Need to Do?

**Nothing!** Just describe your task, and the system will automatically:

- ✅ Identify task type
- ✅ Load relevant documents
- ✅ Keep context clean
- ✅ Optimize performance

---

## 📝 Quick Reference

### I Want to Do X, Should I...

1. **First check** `index/task-router.md` - 30s to find tools
2. **Then check** specific capability docs - deep dive
3. **Start working** - system has already auto-loaded necessary content

### Encountered an Error?

1. **First check** `errors/top-5-errors.md` - 5 common errors
2. **Then check** `errors/ERROR_CATALOG.md` - complete error library
3. **Still stuck** - Use Debugging Agent

### Need Agent Assistance?

1. **Check available Agents** - See `rules/agents.md`
2. **Choose appropriate Agent** - planner / code-reviewer / tdd-guide / architect
3. **Invoke via Task tool** - system will auto-route

---

## 🚀 Ready to Work

Ready to receive tasks!

**Remember**:

- ✅ Quick plan → present → confirm → execute
- ✅ Self-decide 95% of issues
- ✅ Only ask for 4 critical blocking situations
- ✅ System will auto-load necessary documents

---

**Version**: v5.2 (Capability Evolution Integration)
**Updated**: 2026-02-22
**Size**: ~5.5KB
**Improvements**:
- Integrated Capability Evolution Mode (auto-activated each conversation)
- Added `rules/core/capability-evolution.md`
- Auto-identify reusable patterns and internalize into decision layer

**Upgraded from**: v5.1 (2026-02-09)
