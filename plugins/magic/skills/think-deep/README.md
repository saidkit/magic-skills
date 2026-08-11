# think-deep — a careful worker for jobs with several steps

**What it is.** think-deep takes a multi-step task, breaks it into a short plan, does each step with a self-check before moving on, and then checks the whole result against your "done when…" criteria — looping to fix anything that failed. Think of it as the difference between "just do it" and "do it, then prove it's right."

**When to reach for it.**
- "This has a few moving parts and I don't want a step skipped."
- "Get it done, but actually verify it works — don't just tell me it's done."
- "There's a clear finish line (tests pass, the page loads, the numbers match) — hold the work to it."
- "I'd rather it check its own work as it goes than hand me something half-right."

**How to call it.** Three ways, pick by how hands-on you want to be:
- `/magic:think-deep <task>` — call the skill straight.
- `think!` — the **interactive** form: it plans, checks the plan with you, then works. Good when you want a say before it runs.
- `auror!` — the **autonomous** form: it plans and runs the whole thing on its own, then hands you a final report. Good when you want to walk away.

**What you get back.** A restated task with a clear "done when…" list, a short plan, the work itself done step by step, and a final pass/fail check against those criteria. If something fails, it fixes and re-checks. If it truly can't finish, it stops and tells you why instead of pretending it's done.

## Examples

**You type:** `auror! add pagination to the results table and make sure the tests pass`
**You get back:** A plan (add the control, wire it up, cover it with tests), each step done with a self-check, a final run against "tests pass," and a short report — hands-off from start to finish.

**You type:** `think! how to migrate the CSV import feature to the new config format`
**You get back:** The task restated with a plan for your review; once you confirm, it works through each step with checks and verifies the migration steps is complete before calling it done.

**You type:** `/magic:think-deep refactor the billing module in a few passes, then confirm nothing broke`
**You get back:** The refactor split into clear passes, each checked as it goes, and a final acceptance check against "nothing broke" before it reports finished.

## Where it really shines

The examples above are the everyday shape. Here's what makes think-deep more than a to-do runner — each is a pattern pulled from live sessions:

**1. "Autonomous" that earns the word — it proves it's done, it doesn't just claim it.**
`auror! add the feature and don't stop until the tests pass and a review finds nothing left` → it writes the "done when…" up front, works step by step with self-checks, then runs an **acceptance gate that re-runs each criterion as a real check** (a test run, a validator's exit code, a count) and prints a PASS table with the actual output. The final report is earned by evidence, not asserted.

**2. It refuses to fake success — and escalates honestly.**
`auror! make it satisfy <two requirements that secretly can't both hold>` → it plans, builds, the gate fails one check, it makes one scoped repair attempt, sees no progress at the cap, then **stops and reports the exact gap** — no false "done," no silent quit. Treating "I can't get there" as a real, reportable outcome is the one pause even full autonomy can't skip.

**3. "Use tool X" means it actually invokes tool X.**
`auror! this helper is too thin — use the trimming skill to tighten it, then the testing skill to validate it` → its golden rule is *compose, don't emulate*: it binds each named skill as a real step and **calls it** (so you get the tool's true behavior), instead of paraphrasing equivalent work by hand.

**4. It's a disciplined investigator, not just a builder.**
`think! figure out why the background job shows no progress panel` → the same plan → self-check → gate machinery becomes a diagnosis: it gathers concrete evidence, runs a **differential table** that rules out each candidate cause against that evidence, and the gate passes only when the root cause is *cited*, not guessed. A follow-up `auror! fix it` then ships the fix with a before/after that proves the change was the cause.

**5. Anchored quality goal-runs (`auror locomotor!`).**
`auror locomotor! make our landing hero as polished as ref/hero.png` → it pins the reference and writes a *blind, comparative* "done when…" **before** burning a long run, then loops build → judge → fix-the-weakest → re-judge until it clears the bar or escalates — and it's smart enough to switch to a tests-green bar instead if you point it at something with no look-and-feel to compare.

## Good to know

- It's at its best when there's a real finish line. If you have a clear "done when…" in mind, say it — that's exactly what it checks against at the end.
- Pair it with `auror!` when you want it fully hands-off, or `think!` when you want to approve the plan first.
- It's overkill for a quick one-liner. Reach for it when correctness matters and you want the work verified, not just done.
- "Compose, don't emulate" is its golden rule: if your task mentions another tool, it uses that real tool instead of faking the work by hand.
