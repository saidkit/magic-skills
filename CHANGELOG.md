# Changelog

> **Marketplace note — 2026-09-20:** the **`think`** plugin ships **v0.4.0** — a third skill,
> **`reflect!!`** (distil the working method from the current dialogue into a reusable instruction;
> propose reconciling it with the project's knowledge base, propose-then-confirm). See
> `plugins/think/CHANGELOG.md`. The `magic` plugin is unchanged by this release.
>
> **Marketplace note — 2026-08-12:** the `magickit` marketplace now ships a second plugin, **`think`**
> (v0.1.0) — divergent-thinking front-doors, first skill **`ideate`** (diverge → adversarially judge →
> select top-N; composes `magic:critic`). Its history lives in `plugins/think/CHANGELOG.md`. Entries below
> are the `magic` plugin.

## 0.10.0 — 2026-09-22

**Changed — the grant-reading fuse carries an explicit counter-framing (defense-in-depth).** The
always-loaded invariant now states, in one added line, that an owed operator decision is **not an
"ambiguous answer" a blanket grant may default**: a blanket grant does not reach it, however the grant is
worded — only naming the specific reserved class pre-decides it. This closes the residual failure where an
autonomous run, standing on a blanket "default ambiguous answers" grant, reclassifies a reserved decision as
just such an answer and self-defaults it. Behavior-preserving for how-to-build autonomy; the only new outcome
is that a reserved decision held even under a grant that names "ambiguous answers" as a class to default.
Guard: `docs/evaluation/macros/decision-fuse/harness.sh` grows to **12 checks** (new `D11`, RED-first — proven
failing on the shipped block before the edit).

## 0.9.0 — 2026-09-22

**Changed — the owed-operator-decision fuse is explicit in the operator-macro layer.** A blanket autonomy
grant (`proceed!!` / `run!!`) now covers *how-to-build choices only — never a decision reserved for the
operator*: an owed decision is announced once, then held (the same whether you are watching or away); to
pre-decide a reserved class, name it in the directive. The phase-boundary-skip clause is tightened so
autonomy never sweeps up an owed-decision boundary, and the `said!!` Compose line no longer implies an
unconfirmed omission is the *sole* undroppable wait. Behavior-preserving for how-to-build autonomy — the new
outcome is that a reserved decision **holds** under a grant instead of being silently defaulted. Also: a
consumer-permission note in the plugin README (the plugin ships no tool-level fuse — outward-operation
consent stays your own tool-permission configuration), and a stale `finish!!` reference removed from the
install page + README. Guard: `docs/evaluation/macros/decision-fuse/harness.sh` (11 checks, RED-first +
mutation-tested).

## 0.8.0 — 2026-09-03

**Changed — `think-deep` enforces the rising-severity escape (Phase 4).** The repair loop now records a per-iteration severity signal (weighted by how bad the open findings are when the gate ranks them, else the open-criterion count) and, when it fails to decrease across two consecutive iterations, **stops and escalates "premise suspect — re-examine the premise, not another repair pass"** — a new trigger alongside the existing cap / same-criterion-twice ones. Turns the authored `critic` escape clause into a mechanical engine stop; behavior-preserving for the normal (decreasing) case. Guard: harness `S25` + two golden fixtures (the trigger + a decreasing-severity behavior-preservation control).

## 0.7.0 — 2026-09-03

**Changed — `critic` hardens the acceptance bar against a stale-source premise.** The authored contract now
(1) verifies the pinned source is the current/canonical revision and records the discriminator — a bar on a
superseded source is *void*; (2) briefs one reviewer per run to attack the *contract* ("is this source
current? does the bar measure the right thing?"), distinct from the artifact-attacker; (3) treats *rising*
severity across repair passes as a signal to re-examine the premise, not to keep fixing. Behavior-preserving
— a sound-premise run is unchanged; the only new outcome is "stale source ⇒ void". Guards: three new
`harness.sh` static checks (source-currency spans both branches) + golden fixtures.

## 0.6.0 — 2026-09-03

**Added — `prompt!!` skill.** A new `magic` skill that generates a prompt from the project's curated
prompt library (the `MAGIC.prompts` key in CLAUDE.md → default `docs/prompts.md`) in the operator's own
terse voice, and `prompt!! add` curates good prompts back into it (least-verbose, append-only). Two verbs,
`add` operand-guarded; the corpus is a hand-maintainable human↔AI bridge — one shot per `## <case> — <when>`
block. Ships `references/prompts.template.md` and seeds `docs/prompts.md` on first `add`. Composes nothing
heavy — no critic loop, no embeddings. Guards: exit-coded `harness.sh` (14 checks, negative-control-proven)
+ behavioral goldens.

## 0.5.0 — 2026-09-03

**Changed — operator macros migrated to the `!!` command ontology.** Every operator macro is now named
from intent and marked by a double bang — the sole macro marker; single-`!` and bare-word forms are
retired. `auror!`→`run!!` · `auror locomotor!`→`drive!!` · `expelliarmus!`→`proceed!!` ·
`silencio!`→`task-comments!!` · `locomotor!`→`resume!!` · `lumos!`→`precedent!!` · `think!`→`think!!` ·
`said!`→`said!!` · `flow!`→`flow!!` · `gauntlet!`→`gauntlet!!` · `web!`→`web!!`. **Full uniformity** —
every operator-invoked skill trigger migrates too: `critic!`→`critic!!` · `criticize!`→`criticize!!` ·
`smart!`→`smart!!` · `ideate!`→`ideate!!` · `session!`→`session!!`. Three skills whose operator identity
*is* the ontology were renamed end-to-end: **`revelio`→`refresh`** (`refresh!!`), **`pensieve`→`audit`**
(`audit!!`), and **`muggle`→`explain`** (`explain!!`) — dir, frontmatter `name`, `description` trigger,
and guide. (`explain!!` coexists with the pre-existing personal `explain!!` macro.)
**Hard rename, no aliases** — the old names are retired. Behavior is frozen: skills, gates, stop
conditions, and composition semantics are unchanged; only names/notation and the macro block's
cross-references moved. `guides/operator-macros.md` rewritten to the `!!`-only ontology.

## 0.4.0 — 2026-08-28

**Added — `magic:think` run manager.** A new skill managing the `think-<id>.md` protocol files think-deep
writes to the session scratchpad — the manager to think-deep's executor. Six verbs: `list` (outline the
unfinished runs) · `status` (the current run's tree) · `clear` (sweep terminal runs, never a live leaf
without confirm) · `resume` (re-enter a run) · `export` / `continue` (the opt-in cross-session bridge). It
**composes** think-deep — reads its live-leaf / `Parent:` / `Closed:` / marker model, hands
`resume`/`continue` to `Skill(magic:think-deep)`, and never forks its reconstruct logic. The `think!` macro
gains an **operand-guarded** front-dispatch: a verb routes to the manager only as the operative token (bare,
or + a lone `all`/id/path), so a task phrase like `think! clear up the spec` still runs the executor.
Guards: a new eval package (`harness.sh` SUT-by-role, negative-control-proven, live-leaf fixture oracle;
behavioral goldens G1–G7); self-containment + line-budget checks.

**Changed — run-id rule extracted to a single shared source.** think-deep's id derivation + minting (the
task-slug / nested `-<k>` / suffix-until-free rule) moved out of its SKILL.md into `references/run-id.md`,
the one source the whole `think-*` family reuses; think-deep now points at it. Behavior-preserving —
think-deep's own harness stays green (S17 rebased onto the extract). Independent critic (reviewer ≠ builder)
accepted; 0 open P0/P1.

## 0.3.13 — 2026-08-28

**Added — turn-level `[think] <id>` run-marker.** The carried run-id (R12) was echoed only in Phase-1
setup, so the marker printed once at launch then vanished (the per-step Report is per-step, and the
Phase-3 gate / Phase-4 repair tails carried no id — the long tails where a compaction lands). It is now a
**turn-level invariant** beside the `Language` rule: every live-run turn leads with `[think] <id>`,
phase-scoped (`· step N/total` / `· gate` / `· iter K` / `· done` / `· escalated`), nested flips to the
active leaf; the launch line `▶ think-deep <id>` is rescoped to the first turn. Guards: harness S24
(fixed-string — `[think]` is a `grep -E` char class) + S16 tightened; fixtures F13; EVAL B15.

## 0.3.12 — 2026-08-27

**Changed — run-isolation: carried-id fast path + lean disk fallback** (supersedes the 0.3.11 run-stack,
per an independent review that found its `Status`/active-leaf lifecycle heavier than the common case
needs). Each run carries a meaningful id — a task slug + `-<k>` nesting counter (`auth-refactor` →
`auth-refactor-1`), echoed each turn — naming `think-<id>.md`, opened directly. Fallback: an on-disk
`Parent:` + `Closed:` marker recovers the live leaf if a full compaction drops the id. Timestamp id
rejected (opaque → poor compaction-summary survival; the counter, not a clock, disambiguates nesting).
Guards: harness S15–S22; fixtures F9–F12; independent-critic accepted.

## 0.3.11 — 2026-08-27

**Removed — native task-tracker composition; think-deep is file-protocol only again.** Claude Code
dropped the native todo/Task tools (`TodoWrite`, `TaskCreate`/`TaskUpdate`/`TaskList`) from the tool
manifest, so the 0.3.3–0.3.10 native path bound nothing. The 3-tier `Bind the step tracker` block, the
`task-tracker:` hint, and the native ownership machinery are withdrawn; step tracking returns to a single
scratchpad protocol file. The verification layer (`Done-when` · gate · `Gate log` · converge/escalate) is
unchanged — a ticked step never closes the run, only the gate does.

**Added — per-run isolation + compaction-resume.** The old fixed filename clobbered itself under
nested/parallel runs; each run now writes its own task-slug-keyed file, reads/writes only its own, and
re-locates it from disk after a compaction. Guards: harness S11–S19; fixtures F8 recast, F9 added.
*(Reworked in 0.3.12.)*

## 0.3.10 — 2026-08-12

**Re-instated — ownership & isolation on the shared task list (native backend, R11 + O5).** The 0.3.6
R11 experiment was backed out (`revert 0a5c732`, "keep 0.3.5") before it was ever exercised; a live
session then produced the exact failure it targets — **46 native tasks from `auror!`/think-deep AND
`critic!` mixed in one flat, un-namespaced list**, unattributable and unfilterable. So R11 is restored
with that evidence: think-deep names each task `[think-deep] <N>-<step>` with `owner: think-deep/<run-id>`
+ `metadata {ns,run,step}`, reconstructs only its own by filtering `TaskList` on that `owner`, never
mutates a foreign task, and (O5) marks its tasks to their true terminal state on close — `completed` on
converge, kept as-is on escalation as the residual-gap surface, delete only a planning-error task and
never completed work. Bounded by R6 — the gate, not the list, closes the run. Guards: harness S16–S19.

**Changed — `auror locomotor!` acceptance is now an independent `critic!` review (reviewer ≠ builder),
not the builder's self-grade.** The macro authored a critic bar (step 1) but let `auror!`/think-deep
**self-grade** against it — so a self-generated artifact could close *"all pass, no iteration"* while an
independent review found P0s (observed live: a spec corpus minted "clean" with a cross-file money-math
contradiction inside). New **step 4** binds acceptance to an independent critic review that converges only
when it adds *nothing new* (else escalates); a self-graded "all pass" can never close it. Composition-only
— `think-deep`/`critic` untouched; synced across the distributable `guides/CLAUDE.md` + the personal macro
copy. Guards: auror-locomotor harness S15/S16, fixture A7.

## 0.3.9 — 2026-08-11

**Changed — trigger tidy across `think-deep`, `gauntlet`, `muggle`; `auror locomotor` fan-out repoint.**
Applies the same explicit-invocation tightening used for `critic` to the sibling skills: `think-deep`
and `gauntlet` frontmatter now read "explicit … invocation AND NOTHING ELSE", and `muggle`'s trigger
line was trimmed. The `auror locomotor` macro's fan-out breadth now redirects to **`gauntlet!`** (the
surviving invocation) instead of the retired `ultra locomotor!` alias — synced across the distributable
`guides/CLAUDE.md` and the personal macro copy. Description/macro-doc only; no phase behavior change.

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
