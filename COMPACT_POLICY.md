# Context Compact Policy (Auto-Compact)

**Goal**: Keep conversations clear and efficient as context grows, without losing critical constraints or decisions.

## When I Auto-Compact
I will proactively compact when any of these are true:
- The conversation becomes long/fragmented and the working memory is at risk of drifting.
- There are multiple parallel tasks, decisions, or constraints that need consolidation.
- You explicitly ask for a compact/summary.

## What I Produce
A short, high-signal summary that includes:
1. **Primary goal** (what we are trying to achieve)
2. **Key decisions & constraints** (non‑negotiables, policies, preferences)
3. **Current status** (what’s done vs. pending)
4. **Next actions** (the immediate plan)
5. **Open questions** (only if needed)

## What I Will NOT Include
- Internal chain‑of‑thought or hidden reasoning
- Unnecessary repetition or verbose logs
- Sensitive data beyond what you already provided

## Persistence Rules
- The compact summary becomes the new working context for the next steps.
- I will carry forward your fixed constraints and preferences by default.
- If anything seems ambiguous, I’ll ask once and then proceed.

## Your Control
- You can say **“compact now”** to force an immediate summary.
- You can say **“don’t compact yet”** to defer.
- You can say **“compact less/more”** to adjust summary detail.
