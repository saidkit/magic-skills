# Changelog

## 0.3.8 — 2026-08-11

**Changed — `critic` invocation surface finalized (explicit-token trigger).** The frontmatter now
activates the skill ONLY on an explicit `/magic:critic` or `critic!` invocation (never on a bare
"review"/"critique"/"write acceptance criteria" request), so it never hijacks a casual review — a
deliberate precision-over-recall choice for a power-tool. `critic!` is the skill's own frontmatter
alias, not an operator macro (the macro was redundant once the frontmatter owns the trigger). No
behavior change to the phases; description-only. (A description-triggering optimization pass was run
but is not a meaningful signal for a token-triggered skill — an installed skill shadows the throwaway
test copies — so the lean explicit-only description was kept, which the pass also returned as best.)

## 0.3.7 — 2026-08-11

**Changed — `critic` now authors objective/repair-loop contracts, not just blind-comparative ones.**
`critic` previously framed itself as comparative-only and hard-blocked whenever no external reference
existed — yet its library already shipped non-perceptual **T** bars (software feature · API · refactor ·
data) that were unreachable through that gate. A new **Phase 0 — Classify** routes the target to **C**
(subjective/perceptual → blind A/B vs a reference), **T** (objective/spec → adversarial review to
*0 open P0/P1 and nothing new*, attacker stance for money/data/security, or the executed form), or
**C+T** (composed). **Phase 1 branches:** the C branch still pins an external anchor and hard-blocks
without one; the T branch pins the *internal* standard (spec/tests/source-of-truth) and does **not**
hard-block — a repair loop's reference is the code itself. The pin still survives autonomy in both
branches. Lets an operator get the full repair-loop `Done-when` from an interview instead of hand-writing
it. `think-deep` untouched; the comparative path is unchanged. (Version 0.3.6 was skipped.)

**Added — output modes: a gate, a review-vs-repair default, and a human-prompt render.** `critic` now
does more than emit a `Done-when` and stop. Phase 3 gained a **gate**: standalone, it renders the
contract **terse** (a floor pointer + the bar + the stop — the enumerated form is `as full prompt`, in
the new `references/prompt-forms.md`) and **waits**; under `auror!`/`expelliarmus` (or composed in a
loop) the gate auto-passes — the pin never drops in either case. Three exits: **contract** (`as prompt`
— render-only export for future human composition, or the feeder hand-off inside a loop), **review**
(the default drive — adversarial per target, verified, writes a ranked `…-review.md`; **reports
findings, edits nothing**; stops when a pass finds nothing new), and **repair** (`+fix` — review then
fix to *0 open P0/P1 + nothing new*, the only exit that edits). The review-not-repair default means
"criticize what X generated" never silently rewrites the thing under review. The skill now self-triggers
on `/magic:critic` **or** the bare `critic!` alias (frontmatter), and an **Invocation & parameters** table
documents the mode parameter (`+fix` · `as prompt` / `as full prompt` · `park`; default = review). No
operator macro is needed — classify/gate/exits are all self-enforced, so the trigger lives in the skill,
not the always-loaded block.

## 0.3.5 — 2026-08-10

**Changed — terser Phase-1 backend tag.** think-deep now announces the bound tracker as a bare
`(task tracking: native)` / `(task tracking: file protocol)` tag on the Phase-1 heading — no rationale
("tools loaded", "no hint") and no "registering the plan…" preamble. Output hygiene only; no behavior
change.

## 0.3.4 — 2026-08-10

**Fixed — deferred native task tools now bind native instead of falling back to file.** The 0.3.3
tracker-composition rule was ambiguous for the *present-but-deferred* case: an agent could read a
lazy-loaded `TaskCreate/TaskUpdate` as "not positively confirmed" and default to the file protocol —
so no native task panel appeared even though the tracker was one `ToolSearch` away. Tier 2/3 of "Bind
the step tracker" are now decisive: **being named anywhere in the manifest (eager OR deferred) is
positive confirmation ⇒ load the schema and bind native**; the file backend is used **only when the
tracker is absent entirely** (or an explicit `task-tracker: file` hint). "I'd have to load it first"
and "another log already tracks this" are explicitly not reasons to fall back.

## 0.3.3 — 2026-08-10

**Changed — `think-deep` composes with the environment's native task tracker instead of emulating
one.** Its protocol bundled two concerns: *step tracking* (the `## Steps` checklist, refocus prints,
checkbox integrity) and *verification* (`Done-when` + acceptance gate + `Gate log` + converge/escalate
loop). The tracking half duplicated — and underperformed — a harness's native todo/Task tools
(structured states, automatic next-item refocus, dependencies, tool-enforced completion), against the
skill's own *compose, don't emulate* directive.

think-deep now **binds a step-tracker backend once at Phase 1**: an explicit `task-tracker:
native|file` hint (operator or `CLAUDE.md`) wins; else a **deferred-aware, positive-confirmation** read
of the actual tool manifest binds the native tracker (`TaskCreate/TaskUpdate`, or `TodoWrite`) when
present — writing **no `## Steps` markdown**; else the file protocol, unchanged, as a portability
fallback. The **verification layer stays think-deep's own in every mode** — a tracker item marked
`completed` never closes the run; only the Phase-3 gate does. A harness with no native tracker behaves
exactly as before.

## 0.3.2 — 2026-08-10

**Added — `magic:critic`.** A blind-comparative acceptance-contract author: turns a subjective/quality
target ("as good as X", "world-class", "on-brand") into a pinned **K-of-N** `Done-when` that the
`think-deep` acceptance loop converges on. It authors the contract and hands off — never runs the loop
itself. MagicKit is now five skills: `revelio`, `pensieve`, `session`, `think-deep`, `critic`.

**Changed — operator macros.** `said!` / `flow!` reworked to the 3-slot **Invoke · Compose · Drive**
shape over their skills' `goal:` control lines; `auror locomotor!` now drives the critic/gauntlet.

## 0.3.0 — 2026-08-09

**Removed — `magic:lumos`.** Precedent/decision-record search moved to the SAID plugin as
`said:retrieval` — it is decision-investigation inside the SAID setup, not a context-hygiene macro,
and was already built against SAID's artifact layout. The `lumos!` operator macro is retained but now
targets `/said:retrieval`. MagicKit is now four skills: `revelio`, `pensieve`, `session`,
`think-deep`.

## 0.2.3 — 2026-08-08

`magic:think-deep` closes the loop. It verified each step against the *plan* but never the whole
deliverable against the *goal* — so a perfectly-executed wrong plan reported done, and the terminal
review self-graded, leaving the operator to verify by hand.

**Added — `Done-when` contract (Phase 0).** The task's acceptance criteria are captured up front as
checkable predicates (executable where possible, else tagged *judgment*). They seed the per-step
self-checks and are the oracle the gate tests against. No `Done-when`, no gate.

**Added — acceptance gate (Phase 3), independent and depth-safe.** The deliverable is verified
against every `Done-when` by *evidence*, not self-assessment: executable criteria are re-run (tool
output is the verdict), judgment criteria get a fresh-pass review. Spawning a reviewer subagent is
optional and top-level-only — a skill running as a subagent must not spawn (nested-spawn errors) or
invoke a verification skill that itself spawns; it verifies inline. This keeps think-deep safe when
it runs nested inside another skill's agent.

**Added — converge or escalate (Phase 4).** All-pass closes; any fail re-enters Phase 1 as a repair
iteration scoped to the failed criteria (cap 3, or stop on no-progress); a reached cap escalates
with the residual gap rather than self-certifying or silently quitting.

**Changed — body tightened** to imperative directives (199 → 127 lines); the prime-directive
example no longer names a sibling plugin (`said`) — think-deep carries no cross-plugin dependency.

**Changed — protocol file defaults to the session scratchpad** (was: project working dir preferred).
The execution protocol is a transient single-run scaffold; keeping it out of the repo avoids litter,
accidental commits, and stale files. Promote it to a project working dir only on operator request.

**`guides/operator-macros.md`** — `auror!` / `think!` / `auror locomotor!` now name the acceptance
loop think-deep carries (Phase-3 gate on `Done-when` → Phase-4 converge/escalate) instead of leaving
it implicit; the loop stays in the skill only, never duplicated into the macros. `auror locomotor!` is reframed as a **goal-run** — the requested scope + quality gates become the `Done-when` and Phase-4 drives to satisfaction (the prompt-level equivalent of a `/goal` run).

## 0.2.0 — 2026-08-03

`magic:think-deep` gains two rules, both from a live post-mortem in which a plan silently
dropped a verification stage and then reported the work complete.

**Added — loop-shaped `via:` bindings (Phase 1).** When a `via:` names a skill whose contract
is a re-entrant loop, the step must read *"drive X to its stop condition via repeated
invocation"*, not *"invoke X"*, and the plan must carry a final step that re-invokes it and
records its stop-condition output verbatim. Invoking a loop once demotes it to a subroutine:
every rule it would have enforced on later passes becomes unreachable, the plan's own steps
become the only enforcement, and a step that quietly fails to run leaves none.

**Added — checkbox integrity (Phase 2 self-check).** A step may not be marked `[x]` while its
Results entry reads pending / blocked / not started. The observed failure was exactly this —
all steps ticked, Results reading *"pending steps 5–6"*, and nothing detecting the
contradiction for two sessions.

**`guides/operator-macros.md`** — two `flow!` changes. It now instructs **driving `said:flow` to
its stop condition** rather than invoking it once. And its opening line no longer names one
project's directories (`FE / BE / shared engine`) — those were *mounts*, not lanes. It states
the test instead: **spans two or more task logs; a lane is not a repo or a mount**, and one
feature may touch several mounts and stay single-lane. The enforcement clause also now names
`Skill(said:flow)` rather than the retired pre-plugin skill id. Pairs with `said` 0.2.0.

## 0.1.0 — 2026-07-27

Initial release. Five skills migrated from personal `~/.claude/skills/` into the `magic` plugin under the `magickit` marketplace.

- `magic:revelio` — context refresh (was `magic-revelio`)
- `magic:pensieve` — scope / status audit (was `magic-pensieve`)
- `magic:lumos` — precedent / decision-record search (was `magic-lumos`)
- `magic:session` — new-session handoff (was `magic-session`)
- `magic:think-deep` — structured task orchestrator (was `think-deep`)

Migration notes:

- Skills are now namespaced by the plugin: `/magic-revelio` → `/magic:revelio`, `/think-deep` → `/magic:think-deep`, and so on. Update any `CLAUDE.md` macros that referenced the old names.
- `guides/operator-macros.md` ships the `CLAUDE.md` macro block (`revelio!`, `pensieve!`, `lumos!`, `session!`, `think!`, `auror!`, `expelliarmus`, `locomotor!`) that the skills were designed against — previously personal-config-only, now part of the distribution.
- `think-deep` wrote its execution protocol to a hardcoded `/home/claude/think-deep-protocol.md`. That path only exists in a Linux sandbox; the ported skill resolves a `<protocol-dir>` at runtime (project working dir, else session scratch) and reports the resolved path in chat.
