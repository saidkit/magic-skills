# session — save your place so a new chat can pick up right where you left off

**What it is.** When you need to stop but the work isn't finished, `session` writes down everything a fresh chat would need to carry on — so tomorrow's session, or a teammate's, starts warm instead of guessing. It saves that summary as a file you can point the next session at.

**When to reach for it.**
- It's the end of the day and you want to pick this up tomorrow in a new chat.
- This conversation has gotten long or full, and you'd like a clean restart without losing the thread.
- You're handing the work off to a teammate who'll continue in their own chat.
- You just want a safety net — a written record of where things stand before you step away.

**How to call it.** Just type `session!`. It'll check a couple of details with you first (see below), then save the file.

**What you get back.** A handoff file saved at `working/<feature>/session-<number>.md`. It captures the things a cold chat can't reconstruct on its own: what's done, what's still in progress, what's blocked, the decisions you made and *why*, any limits or rules you set, and pointers to the files that matter. To resume later, you just open a new chat and have it read that file.

## Examples

**You type:** `session!`
**You get back:** "Before I save — this is the billing feature, id `PROJ-01`, and this looks like session 2. Sound right?" Once you confirm, it writes `working/PROJ-01/session-2.md` with a summary of where things stand, and tells you it's saved.

**You type:** `session!`  (wrapping up for the day)
**You get back:** A quick confirm on the feature and session number, then a saved handoff noting what's finished, what's half-built, the decisions behind them, and which files to look at first tomorrow. Next chat: just say "read `working/PROJ-01/session-3.md` and let's keep going."

**You type:** `session!`  (handing off to a teammate)
**You get back:** The same confirm, then a file your teammate's chat can open to get the full picture — no need for you to write up a long explanation by hand.

## Good to know
- It always confirms the feature id and the session number with you *before* writing, so the file lands in the right place with the right name.
- It saves a file — nothing is lost when this chat ends. Resuming is as simple as having the next session read it.
- Pick a feature id you'll recognize later (like `PROJ-01`); that's the folder your handoffs are grouped under, so they're easy to find.
