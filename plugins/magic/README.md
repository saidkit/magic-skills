# `magic` — plain-language guide to the operator skills

Seven small, stack-agnostic skills for staying on top of a long working session: refresh your context, audit your progress, explain things simply, hand off cleanly, run a multi-step job carefully, hold work to a quality bar, and generate a build prompt. You invoke each by typing a short word — no setup, no config. Part of [MagicKit](https://github.com/saidkit/magic-skills).

Every skill below has its own fuller guide at `skills/<name>/README.md`. This page is the tour, with a couple of real "you type → you get" samples each.

## The seven at a glance

| Skill | What it does | You type |
|---|---|---|
| **revelio** | Quick "where were we?" recap of a long chat | `revelio` / `revelio!` |
| **pensieve** | Full start-to-finish status audit (a table) | `pensieve` / `pensieve!` |
| **muggle** | Explains what's going on in plain English | `muggle!` |
| **session** | Saves a handoff so a new chat picks up warm | `session!` |
| **think-deep** | Runs a multi-step job and verifies the result | `/magic:think-deep` · `think!` · `auror!` |
| **critic** | Turns "make it good" into a finish line, then reviews | `critic!` / `criticize!` |
| **gauntlet** | Prints a ready-to-paste "build-to-a-bar" prompt | `gauntlet!` |

The first three **just report and stop** — they show you where things stand and hand the decision back. The rest **do work.**

---

## revelio — a quick "where were we?"
Sweeps back through a long conversation and hands you a short recap: recent activity, where the work stands, constraints you set earlier, and 3–5 next actions. Then stops.

- **You type:** `revelio`
  **You get:** *"Recent: refactored the checkout page, fixed two failing tests. State: payment step works; the confirmation email is still stubbed. Constraints you set: keep it TypeScript, no new dependencies. Next: (1) wire up the real email, (2) test the empty-cart case, (3) update the changelog."*
- **You type:** `revelio!` *(early in a short chat)* → a brief note that there isn't much to refresh yet — it's all still on screen.

*Full guide: `skills/revelio/README.md`*

## pensieve — the full status check-up
Reconstructs the whole task end-to-end and lays it out as a **status ledger** — every step marked Done / In progress / Blocked / Not started / Superseded, with evidence and a next action — then the blockers and the remaining path. Then stops.

- **You type:** `pensieve`
  **You get:** a one-line task restatement, then a table like:

  ```
  | # | Step          | Status      | Evidence / notes        | Next action      |
  |---|---------------|-------------|-------------------------|------------------|
  | 1 | Sign-up form  | Done        | PROJ-01 shipped, tested | —                |
  | 2 | Welcome email | In progress | draft written           | wire up the send |
  | 3 | Error copy    | Blocked     | waiting on the writer   | ping them        |
  ```
- **You type:** `pensieve!` *(before a handoff)* → the same audit, so nothing quietly falls through the cracks.

*Full guide: `skills/pensieve/README.md`*

## muggle — explain it in plain English
A jargon-free explanation of where things stand or what something means — the gist, the current state, and the practical "so what." No code, no status tables.

- **You type:** `muggle! explain what this change actually does`
  **You get:** a couple of plain sentences — what it's for, what's different now, and why it matters, without walking through the code.
- **You type:** `muggle! give me something I can send to a non-technical teammate` → one clear, shareable sentence you can paste into a message.

*Full guide: `skills/muggle/README.md`*

## session — save your place for a new chat
Writes a handoff file so tomorrow's session (or a teammate's) starts warm: what's done, in progress, and blocked, the decisions and why, and pointers to the files that matter. It confirms the details with you first.

- **You type:** `session!`
  **You get:** *"Before I save — this is the billing feature, id `PROJ-01`, session 2. Sound right?"* Once you confirm, it writes `working/PROJ-01/session-2.md` and tells you it's saved. Next chat: *"read `working/PROJ-01/session-2.md` and let's keep going."*
- **You type:** `session!` *(handing off to a teammate)* → the same quick confirm, then a file their chat can open to get the full picture — no long write-up needed from you.

*Full guide: `skills/session/README.md`*

## think-deep — a careful worker for multi-step jobs
Breaks a task into a short plan, does each step with a self-check, then verifies the whole result against your "done when…" criteria — looping to fix whatever failed. Three ways to call it, by how hands-on you want to be.

- **You type:** `auror! add pagination to the results table and make sure the tests pass`
  **You get:** a plan, each step done with a self-check, a final run against "tests pass," and a short report — fully hands-off.
- **You type:** `think! migrate the CSV import feature to the new config format` → the task restated with a plan for your **approval**, then it works through each step with checks.

*Full guide: `skills/think-deep/README.md`*

## critic — turn a fuzzy goal into a finish line
Pins a vague standard ("make it good", "as good as that page") into a concrete, finishable **done-when**, then reviews your target against it — so a quality loop can actually stop.

- **You type:** `critic! review the pricing page against ref/hero.png`
  **You get:** a blind side-by-side bar from your example image, a ranked list of what's off (spacing, color, alignment), and **zero edits** to your files.
- **You type:** `critic! get the checkout flow to production quality +fix` → a done-when of "zero serious issues and tests green," then the fixes applied until it clears the bar. *(Default is review, which never edits; add `+fix` only when you want changes.)*

*Full guide: `skills/critic/README.md`*

## gauntlet — a ready-to-paste build prompt
Writes (does **not** run) a strong copy-paste prompt that tells an AI to split the work into parts, put a builder and a harsh critic on each, and loop until every part matches or beats an example you name — judged blind.

- **You type:** `gauntlet! a landing page as polished as ref/hero.png`
  **You get:** a copy-paste prompt that splits the page into parts (hero, pricing, footer…), loops each against `ref/hero.png`, and won't stop until each wins a blind side-by-side. You paste it and run it wherever you like.
- **You type:** `gauntlet! a polished dashboard` *(no reference)* → it pauses and asks what to compare against, rather than inventing a bar.

*Full guide: `skills/gauntlet/README.md`*

---

## How they fit together
- **Lost the thread?** `revelio` (quick recap) · `pensieve` (full audit) · `muggle` (plain-English explainer). All three report and stop.
- **Stepping away?** `session!` saves a handoff for a fresh chat.
- **Real work to do?** `think-deep` (via `think!` or `auror!`) plans, does, and **verifies** a multi-step job. `critic!` pins a quality bar and reviews or fixes against it. `gauntlet!` hands you a build-to-a-bar prompt to run elsewhere.

## Good to know
- **The diagnostics stop by contract.** `revelio` / `pensieve` / `muggle` report and hand the decision back to you. To refresh *and then* keep going, use the `locomotor!` / `pensieve locomotor!` macros (see [operator-macros.md](../../guides/operator-macros.md)).
- **Nothing carries across calls.** Each invocation is a fresh sweep scoped to the message that triggered it — call again whenever you need another look.
- **No project files, no config.** These skills read whatever layout your project already has and adapt (`docs/adr/` vs `decision-log/`, `docs/working/` vs `notes/`, and so on).
