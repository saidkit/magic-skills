# pensieve — the full status check-up for whatever you're working on

**What it is.** A single command that stops and takes stock of your current task from start to finish. It lays out everything — what was planned, what's finished, what's underway, what's stuck, and what's left — in one clear table, then hands the wheel back to you.

**When to reach for it.**
- "Wait — where are we on this whole thing?"
- "I've been heads-down a while and lost the thread."
- "Before I pick what to do next, show me the full picture."
- "I'm about to hand this off — what's still open?"

**How to call it.** Type `pensieve` (or `pensieve!`) on its own. That's all it needs.

**What you get back.** A short restatement of the task, then a **status ledger** — a table with one row per step, each marked Done, In progress, Blocked, Not started, or Superseded, with a note on how it got that mark and the next action. Below the table you get the current blockers and the remaining path, in order. Then it stops. It won't keep working unless you tell it to.

## Examples

**You type:** `pensieve`
**You get back:** A full readout of the feature you've been building — a paragraph naming the task, a ledger of every step with its status and evidence, a short list of what's blocking you right now, and a numbered path through what's left.

**You type:** `pensieve!` (halfway through a long project, before deciding what to tackle next)
**You get back:** The same end-to-end audit, including the little steps that only came up along the way, so nothing quietly falls through the cracks. It looks like this:

```
# Scope
Building the onboarding feature — new-user sign-up plus the welcome email.

## Status ledger

| # | Step              | Status       | Evidence / notes        | Next action        |
|---|-------------------|--------------|-------------------------|--------------------|
| 1 | Sign-up form      | Done         | PROJ-01 shipped, tested | —                  |
| 2 | Welcome email     | In progress  | draft written           | wire up the send   |
| 3 | Error messages    | Blocked      | waiting on copy         | ping the writer    |
| 4 | Analytics hook    | Not started  | —                       | scope it           |

## Current blockers
- Error-message copy hasn't landed yet.

## Remaining path
1. Finish wiring the welcome email.
2. Unblock and add the error messages.
3. Add the analytics hook.
```

**You type:** `pensieve` (right before handing the work to a teammate)
**You get back:** A tidy snapshot of everything still open, so the next person can pick it up without guesswork.

## Good to know
- **It stops when it's done reporting.** If you want it to keep going straight into the work, pair it with a "keep going" command — `pensieve locomotor!`.
- **It's the thorough cousin of `revelio`.** `revelio` is a quick refresh that skips your most recent turns; pensieve reviews the entire task, recent turns and all.
- **It reads, it doesn't change anything.** Running it is always safe — it just looks and reports.
