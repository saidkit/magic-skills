# `magic` — operator macros

Six stack-agnostic skills for controlling context, scope, orchestration, handoff, and anchored quality mid-session. Part of [MagicKit](https://github.com/saidkit/magic-skills).

## Skills

### `/magic:revelio` — context refresh

Surfaces what has gone stale or buried mid-conversation and is load-bearing for the next step: recent activity, current work state, operator constraints stated in earlier turns, and 3–5 prioritized next actions. Deliberately skips what is already in recent turns — re-emitting that is noise, not refresh. **Stops.**

### `/magic:pensieve` — scope / status audit

Reconstructs the whole active scope end-to-end and emits a status ledger: every planned step plus every step that became necessary during execution, each marked Done / In progress / Blocked / Not started / Superseded with evidence and a next action, followed by current blockers and the remaining path. Unlike `revelio`, it does **not** skip recent turns. **Stops.**

### `/magic:session` — new-session handoff

Writes `working/<feature>/session-<n>.md` so a fresh session picks the work up cold. Confirms feature id and session number with the operator before writing. Carries what a cold session cannot reconstruct — decisions and their reasons, operator constraints, done vs. in flight vs. blocked — with citations rather than restated prose.

### `/magic:think-deep` — structured task orchestrator

Decomposes a complex task into 3–10 steps, each carrying a deliverable, a check criterion, and a **`via:`** binding naming the skill that performs it. Confirms the restatement with the operator, writes a live execution protocol file, then executes step by step — with a mandatory self-check after each that must name specific positives *and* specific criticism before moving on.

Its prime directive is **compose, don't emulate**: when a step is covered by a named skill, macro or pipeline, the step invokes it rather than hand-rolling equivalent work. A plan whose `via:` bindings omit a pipeline the task named is treated as a wrong plan and rebound before execution.

Pairs with the `think!` macro (plain invocation) and `auror!` (invoke, then run the plan through autonomously and deliver a final report).

### `/magic:critic` — anchored acceptance bar

Authors a bounded, blind-comparative acceptance contract for a subjective or quality target: it pins an external anchor (an exemplar to match, a baseline to beat), chooses the judging form, and emits a `Done-when` a loop can actually terminate on — a blind ≥K-of-N comparison rather than an absolute "make it a 9/10" self-score that never converges. For a non-perceptual target it routes to a review-until-clean or tests-green bar instead of inventing a comparison. Authors the bar and **stops** — the acceptance loop is run by whatever drives it (`auror!`, a `/goal`).

### `/magic:gauntlet` — fan-out gauntlet-loop prompt

Assembles and **prints** a gauntlet-loop prompt for a decomposable perceptual target: fan out a builder-and-critic fleet across the parts, `/loop` each with a separate harsh critic judging it *blind* against the anchor, and don't stop until every part matches or beats the reference side by side. It pins the anchor first and **hard-blocks** if there is nothing to compare against, rather than fabricate a bar. Emits the prompt text only — you run it.

## Use cases — anchored-quality loops

`auror locomotor!` extends `auror!` (see `/magic:think-deep` above) with a **pinned quality bar**. Give it a goal plus something to be judged against; it authors a bounded acceptance bar (via `/magic:critic`), prints the contract, then runs a single builder-and-critic loop — build → judge *blind* against the bar → repair the weakest part → re-judge → **stop when it clears the bar, or escalate at the repair cap** (it never self-certifies). The bar is chosen to fit the target, so one verb spans three shapes:

**Match an exemplar** — perceptual targets, judged by blind comparison:
- `auror locomotor! make the pricing hero as polished as ref/hero.png` — each part (headline · CTA · visual · layout) blind against the exemplar until it clears a set pass mark; brand tokens stay in-kit.
- `auror locomotor! a 15-second intro jingle at the level of ref/theme.mp3` — blind *listen* against the reference track; loudness/format held as a floor.
- `auror locomotor! rewrite our tagline to beat the current line` — blind-pick new vs current on a pinned voice, best-of-N.

**Get it correct** — objective targets, reviewed or executed (no blind A/B is invented where none fits):
- `auror locomotor! harden our password-reset flow` — attacker-stance review down to zero open high-severity findings, with the security tests green.
- `auror locomotor! extract the tax logic, no behavior change` — full suite green, outputs identical, diff stays in scope.
- `auror locomotor! make the quarterly figures reconcile to the ledger` — every number recomputed against the source, zero discrepancies, reproducible.

**Both look and correctness** — mixed targets, every sub-bar must pass:
- `auror locomotor! build the revenue dashboard — matches ref/dash.png and every number reconciles` — the charts clear a blind comparison **and** the numbers recompute to zero discrepancies; either one failing fails the whole.

Want **breadth** instead of depth? `ultra locomotor!` fans out several competing builders, has a harsh critic judge them side-by-side blind, and keeps the best — it prints that prompt (via `/magic:gauntlet`) for you to run.

These verbs are operator macros; install the block per [operator-macros.md](../../guides/operator-macros.md).

## Design notes

**`revelio` and `pensieve` stop by contract.** They are diagnostics. The operator reads the output and decides. To chain straight into execution, use the `locomotor!` / `pensieve locomotor!` macros from [operator-macros.md](../../guides/operator-macros.md).

**Nothing carries across invocations.** No skill here makes subsequent turns "automatically refreshed" or "automatically precedent-checked". Each invocation is a fresh sweep scoped to the message that triggered it.

**No project files, no config.** These skills read whatever layout a project already has and adapt — `docs/adr/` vs `decision-log/` vs `architecture/decisions/`, `docs/working/` vs `notes/` vs `planning/`.
