# Claude Code Engineering Config

A layered engineering system for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Manages context intelligently so Claude uses 20% of its context window instead of 60%, and behaves like a senior engineer instead of a chatbot.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-5.2.0-blue.svg)](https://github.com/Arxchibobo/claude-Reconstruction)

## Install

Clone the repo, then tell Claude to run the install script:

```bash
git clone https://github.com/Arxchibobo/claude-Reconstruction.git
cd claude-reconstruction
pnpm install
pnpm install:config
```

Or if you are in the monorepo root:

```bash
pnpm --filter @arxchibobo/claude-reconstruction install:config
```

To verify the installation:

```bash
pnpm verify
```

Legacy Bash scripts are also available:

```bash
./scripts/install.sh
```

Claude will handle backup, directory creation, and file copying. On Windows, the Node.js scripts (`pnpm install:config`) are recommended.

---

## Architecture

The system is built as 5 layers that stack on top of each other. Each layer intercepts at a different point in Claude's execution lifecycle.

```
                    ┌─────────────────────────────┐
                    │       User Request           │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
          Layer 5   │      Context Manager         │  What docs to load?
                    │   (CONTEXT_MANAGER.md)        │  Keyword matching → load plan
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
          Layer 4   │      Workflow Engine          │  How to work?
                    │   (rules/core/work-mode.md)   │  Plan → Confirm → Execute → Deliver
                    │   (rules/core/blocking-rules)  │  When to ask vs. decide
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
          Layer 3   │      Rules Engine             │  What rules to follow?
                    │   (rules/domain/*.md)          │  coding, testing, security, git
                    │   (rules/coding-style.md)      │  immutability, file organization
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
          Layer 2   │      Hook Layer               │  Quality gates on every tool call
                    │   (rules/hooks.md)             │  PreToolUse / PostToolUse / Stop
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
          Layer 1   │      Delegation Layer         │  Route to specialists
                    │   (rules/delegator/*.md)       │  Architect / Reviewer / Security
                    │   (rules/agents.md)            │  Sub-agent orchestration
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │       Tool Execution          │
                    └─────────────────────────────┘
```

### Layer 5: Context Manager

**Problem**: Claude loads everything in `~/.claude/` into context. A 120KB config eats 60% of the context window before any work starts.

**Solution**: The Context Manager (`CONTEXT_MANAGER.md`) identifies task type from keywords and only loads relevant docs.

```
User says "write a Playwright test"
  → detected: browser-automation
  → loads: rules/core/ (10KB) + rules/domain/coding.md (5KB) + capabilities/browser-automation (8KB)
  → total: 23KB (12% context)
  → leaves 88% free for actual work
```

| Layer | What                        | When        | Size    |
| ----- | --------------------------- | ----------- | ------- |
| L0    | `CLAUDE.md` + `rules/core/` | Always      | ~15KB   |
| L1    | `index/task-router.md`      | Routing     | ~3KB    |
| L2    | Domain + capability docs    | On match    | 15-30KB |
| L3    | Templates, examples         | Exact match | varies  |

### Layer 4: Workflow Engine

Defines **how Claude works** on any task. Located in `rules/core/`.

**4-step cycle**:

```
1. Plan      → Create TodoList, break down steps
2. Confirm   → Show plan, wait for user "go"
3. Execute   → Autonomous decisions, no questions
4. Deliver   → Summary, verification, handoff
```

**Blocking rules** — Claude only asks questions in 4 cases:

1. Missing credentials (API keys, passwords)
2. Mutually exclusive approaches (can't infer)
3. Contradictory requirements
4. Irreversible high-risk operations

Everything else is decided autonomously: file names, code style, dependency versions, UI details, test strategy.

### Layer 3: Rules Engine

Domain-specific rules that govern code quality. Located in `rules/` and `rules/domain/`.

| Module           | File                              | What It Enforces                                            |
| ---------------- | --------------------------------- | ----------------------------------------------------------- |
| **Coding Style** | `coding-style.md`                 | Immutability-first, small files (<800 lines), no mutation   |
| **Testing**      | `testing.md`                      | TDD (RED→GREEN→REFACTOR), 80% coverage minimum              |
| **Security**     | `security.md`                     | OWASP checks, no hardcoded secrets, input validation        |
| **Git**          | `git-workflow.md`                 | Conventional commits, PR workflow, branch strategy          |
| **Patterns**     | `patterns.md`                     | API response format, repository pattern, custom hooks       |
| **Performance**  | `performance.md`                  | Model selection (Haiku/Sonnet/Opus), context management     |
| **Engineering**  | `domain/engineering-workflows.md` | UI verification loop, TDD full cycle, DB migration protocol |

### Layer 2: Hook Layer

Hooks intercept Claude's tool calls at 3 points. Defined in `rules/hooks.md`, configured in `~/.claude/settings.json`.

```
┌─────────────────────────────────────────────────────┐
│                    Hook Lifecycle                     │
│                                                       │
│  ┌─────────────┐   ┌──────────┐   ┌──────────────┐  │
│  │ PreToolUse   │──▶│ Tool Run │──▶│ PostToolUse  │  │
│  └─────────────┘   └──────────┘   └──────────────┘  │
│        │                                     │        │
│   Validate &                            Auto-fix &    │
│   Gate before                           Check after   │
│                                                       │
│  ┌──────────────────────────────────────────────┐    │
│  │ Stop Hook — runs when session ends            │    │
│  └──────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

**PreToolUse** (before tool executes):

- Long command reminder — suggests tmux for `npm`, `cargo`, `pnpm` etc.
- Git push review gate — opens editor for review before push
- Doc blocker — prevents creating unnecessary .md/.txt files

**PostToolUse** (after tool executes):

- Prettier auto-format — formats JS/TS files after every edit
- TypeScript check — runs `tsc` after editing .ts/.tsx files
- Console.log warning — flags debug statements in edited files
- PR logger — logs PR URL and CI status after PR creation

**Stop** (session end):

- Console.log audit — scans all modified files for leftover `console.log`

### Layer 1: Delegation Layer

Routes complex problems to specialized experts. Located in `rules/delegator/` and `rules/agents.md`.

**Expert delegation** (via GPT/Codex MCP):

| Expert           | Triggers On                                              | Does                                      |
| ---------------- | -------------------------------------------------------- | ----------------------------------------- |
| Architect        | "how should I structure", system design, 2+ failed fixes | Architecture decisions, tradeoff analysis |
| Plan Reviewer    | "review this plan", before significant work              | APPROVE/REJECT with criteria              |
| Code Reviewer    | After implementing features, "review this code"          | Bug detection, quality issues             |
| Security Analyst | Auth changes, "is this secure", new endpoints            | Vulnerability assessment, OWASP           |
| Scope Analyst    | Vague requirements, "what am I missing"                  | Ambiguity detection, risk surface         |

**Sub-agent orchestration**:

| Agent                | Auto-triggers When                    |
| -------------------- | ------------------------------------- |
| planner              | Complex feature request               |
| code-reviewer        | Code just written/modified            |
| tdd-guide            | New feature or bug fix                |
| architect            | Architectural decision needed         |
| build-error-resolver | Build fails                           |
| security-reviewer    | Before commits with sensitive changes |

Agents run in parallel when tasks are independent.

---

## Modules

### Error Library

15 documented error patterns with root cause and fix. Located in `errors/`.

| Code | Pattern                 | Quick Check                             |
| ---- | ----------------------- | --------------------------------------- |
| E001 | Async not parallelized  | Multiple awaits → use `Promise.all()`?  |
| E002 | Polling without timeout | Loop has `maxAttempts`?                 |
| E003 | Errors swallowed        | `catch` block re-throws?                |
| E004 | SQL without CTE         | JOIN then filter → pre-filter with CTE? |
| E007 | Resource leak           | All exit paths clean up?                |

Full catalog: `errors/ERROR_CATALOG.md`

### Capability Docs

On-demand guides loaded by the Context Manager. Located in `capabilities/`.

| Capability         | File                                  | When Loaded                        |
| ------------------ | ------------------------------------- | ---------------------------------- |
| Browser automation | `browser-automation-decision-tree.md` | "playwright", "scrape", "automate" |
| MCP servers        | `mcp-servers.md`                      | "MCP", "bytebase", "honeycomb"     |
| Skills catalog     | `skills-guide.md`                     | "skill", "/commit", "/write-tests" |
| Remotion templates | `REMOTION_TEMPLATES_LIBRARY.md`       | "video", "Remotion", "animation"   |
| Marketing skills   | `MARKETING_SKILLS_GUIDE.md`           | "marketing", "SEO", "content"      |
| UI/UX design       | `design/DESIGN_MASTER_PERSONA.md`     | "design", "UI", "interface"        |

### Index / Router

Fast lookup tables. Located in `index/`.

- `task-router.md` — "I want to do X" → points to the right tool in 30 seconds
- `capabilities-index.md` — all capabilities listed with descriptions
- `tools-index.md` — all tools (MCP, skills, agents) listed
- `error-patterns-index.md` — error pattern taxonomy

---

## How the Layers Work Together

Example: user asks to "add user authentication to the API".

```
Step 1 — Context Manager (Layer 5)
  Keywords: "authentication", "API"
  → Load: rules/core/ + rules/domain/coding.md + rules/domain/security.md
  → Context used: ~25KB (13%)

Step 2 — Workflow Engine (Layer 4)
  → Create TodoList: schema → middleware → routes → tests
  → Show plan → wait for confirmation

Step 3 — Rules Engine (Layer 3)
  → coding-style.md: immutable patterns, small functions
  → security.md: bcrypt for passwords, no hardcoded secrets, input validation
  → testing.md: TDD cycle, 80% coverage

Step 4 — Hook Layer (Layer 2)
  → PreToolUse: validate before each edit
  → PostToolUse: Prettier formats, tsc checks types, console.log flagged
  → Stop: final console.log audit

Step 5 — Delegation Layer (Layer 1)
  → Auto-trigger: code-reviewer agent after implementation
  → Auto-trigger: security-reviewer for auth code
  → If architecture unclear: delegate to Architect expert
```

---

## Customize

**Add a capability**: Create `capabilities/your-guide.md` → add keywords to `CONTEXT_MANAGER.md` → register in `index/capabilities-index.md`

**Modify rules**: Edit files in `rules/` directly. Takes effect next session.

**Add hooks**: Edit hook definitions in `rules/hooks.md`, configure in `~/.claude/settings.json`

**Add error patterns**: Append to `errors/ERROR_CATALOG.md`:

```markdown
### E0XX: Error Name

**Pattern**: What goes wrong
**Fix**: How to fix it
**Check**: Quick diagnostic question
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Fork → branch → change → PR.

## License

MIT — see [LICENSE](LICENSE).

## Links

- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Issues](https://github.com/Arxchibobo/claude-Reconstruction/issues)
- [Changelog](CHANGELOG.md)
