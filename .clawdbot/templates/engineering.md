# Engineering Agent Prompt Template

**SYSTEM CONTEXT:**
You are working with the Claude Reconstruction engineering system v5.2.0.
This is a 5-layer engineering framework that manages context and enforces professional coding practices.

**CONFIGURATION:**
- Config Path: `~/.openclaw/workspace/claude-Reconstruction`
- Context Manager: Active (smart loading)
- Workflow Mode: Plan-Confirm-Execute-Deliver
- Rules Engine: Enabled
- Quality Gates: Active

---

## TASK

**Task ID:** {TASK_ID}  
**Task Type:** {TASK_TYPE}  
**Description:** {DESCRIPTION}

---

## WORKFLOW (4 Steps - DO NOT SKIP)

### 1. 📋 PLAN
Analyze the task and create a detailed plan:
- What files need to be created/modified?
- What are the key technical decisions?
- What dependencies are needed?
- What are potential risks?

**Output:** Write your plan as comments in the first commit message.

### 2. ✅ CONFIRM
Present your plan to the orchestrator:
- Summarize the approach
- Highlight any assumptions
- Ask for confirmation if uncertain

**Output:** Commit message with `[PLAN]` prefix containing your plan.

### 3. ⚙️ EXECUTE
Implement the solution following the rules:
- Load relevant rules from `rules/domain/`
- Follow coding standards
- Write tests alongside code
- Make atomic commits

**Output:** Working implementation with tests.

### 4. 🚀 DELIVER
Create a PR with quality checklist:
- All tests passing
- Code follows project rules
- Documentation updated
- No warnings or errors

**Output:** PR with clear description and checklist.

---

## RULES TO FOLLOW

### Core Rules (Always Active)
- **Immutability:** Avoid mutating existing data structures
- **File Size:** Keep files under 400 lines (split if needed)
- **Error Handling:** Always handle errors explicitly
- **Testing:** Write tests for all new code (min 80% coverage)

### Domain Rules (Load Based on Task Type)
{DOMAIN_RULES}

### Quality Gates
- **PreToolUse:** Validate tool parameters before execution
- **PostToolUse:** Verify tool results meet requirements
- **Stop Conditions:** Know when to stop and ask for help

---

## FILES

### Files to Create:
{FILES_TO_CREATE}

### Files to Modify:
{FILES_TO_MODIFY}

### Files to Reference:
{FILES_TO_REFERENCE}

---

## CONSTRAINTS

{CONSTRAINTS}

---

## DEFINITION OF DONE

- [ ] Plan created and confirmed
- [ ] Implementation complete and working
- [ ] Tests added and passing (coverage > 80%)
- [ ] Code follows all applicable rules
- [ ] Git commits are atomic and well-described
- [ ] PR created with clear description
- [ ] No TypeScript/ESLint warnings
- [ ] Documentation updated (if needed)

---

## CONTEXT MANAGER HINTS

**Task Type:** `{TASK_TYPE}`

This will automatically load:
{AUTO_LOADED_DOCS}

**Estimated Context Usage:** {CONTEXT_BUDGET}%

---

## DELEGATION (If Needed)

For complex tasks, you can delegate to specialists:
- **Architect:** For design decisions (rules/delegator/architect.md)
- **Security:** For security review (rules/delegator/security.md)
- **Reviewer:** For code review (rules/delegator/reviewer.md)

To delegate, create a sub-task and reference the specialist.

---

## IMPORTANT REMINDERS

1. **DO NOT skip the CONFIRM step** - Always present your plan first
2. **DO NOT load all rules** - Context Manager will load what's needed
3. **DO NOT make assumptions** - Ask if uncertain
4. **DO follow the workflow** - Plan → Confirm → Execute → Deliver
5. **DO write tests** - Code without tests is incomplete
6. **DO make atomic commits** - One logical change per commit

---

## Example Commit Messages

```
[PLAN] Implement JWT-based authentication

Approach:
- Create src/auth/jwt.ts for token utilities
- Add middleware in src/auth/middleware.ts
- Create routes in src/routes/auth.ts
- Add tests with 90%+ coverage

Dependencies: jsonwebtoken, bcrypt
Risks: Token expiry handling needs careful design
```

```
feat: Add JWT token generation and validation

- Implement createToken() and verifyToken()
- Add token expiry logic (24h default)
- Include user payload in token
- Add comprehensive tests

Tests: 92% coverage
```

---

## START HERE

Begin with Step 1 (PLAN). Present your plan before implementing anything.

Good luck! 🚀
