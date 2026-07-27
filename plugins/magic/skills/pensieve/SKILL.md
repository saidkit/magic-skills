---
name: pensieve
description: |
  Do full scope/status audit, then stop. Use when user called `pensieve` or `pensieve!` directly
---

Refocus by reconstructing the full task scope from the current invocation. Review what was planned, what has been completed, what is in progress, what is blocked, and what remains. Emit a structured status ledger covering all planned steps, including any discovered or implied steps that became necessary during execution. Unlike `revelio`, this is not a context refresh and does not skip recent turns. It reviews the whole active scope end-to-end. Then STOP. Do NOT continue execution unless paired with `locomotor`, `expelliarmus`, or an explicit operator instruction. Does NOT carry across invocations.

Suggested output shape:
```
# Scope
<one-paragraph restatement of the active task>

## Status ledger

| # | Step | Status | Evidence / notes | Next action |
|---|------|--------|------------------|-------------|
| 1 | ... | Done / In progress / Blocked / Not started / Superseded | ... | ... |

## Current blockers
- ...

## Remaining path
1. ...
2. ...
3. ...
```
