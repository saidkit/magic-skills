# Changelog — think plugin

## 0.4.1 — 2026-09-20

**Changed — `reflect!!` output sharpened.** The distilled instruction is now an **atomic numbered
playbook** — distinct, deduplicated, imperative rules, one per line, highest-value first (a
correction-dense session yields roughly fifteen to thirty) — replacing the earlier single-paragraph
form that hid the distinct moves a future run needs. Knowledge-base reconciliation now routes **by
kind**: working-method lessons to the operator's method / notes store, project-scoped rules to the
project's rule / decision docs — both discovered generically, no hardcoded path, self-contained. The
change was grounded by a two-arm experiment and reverses the earlier "personal memory excluded"
premise (a working-method lesson belongs with method notes, not code-style rules). Guards: harness
`G16` (atomic playbook) + `G17` (two-kind routing), negative-control-proven; `G3` (explicit sibling
negative-routing) retired — routing is carried by the description's positive-exclusion. No trigger or
behavioural-contract change; description unchanged.

## 0.4.0 — 2026-09-20

**Added — `reflect!!` skill.** A new `think` skill that distils the operator's *working method* from the
current dialogue's corrections into a reusable instruction, then proposes reconciling it with the
project's knowledge base. It mines seven fields (original task, what was corrected, what dissatisfied,
why the vector changed, decisions made, formulations approved, mistakes-never-repeat), grounds every
line in the dialogue (invents nothing — says "none observed" when a field has no signal), discovers the
project's rule/convention docs generically (no hardcoded path, no cross-plugin dependency), reconciles
by merge / de-duplicate / "superseded — because", and **proposes-then-writes-nothing until the operator
confirms** (standalone instruction when the project keeps no KB). Runs in the main agent on the live
dialogue; description-triggered, no macro (like `refresh!!` / `session!!`). Console-safe flush-left
output. Authored via `skill-creator` → `skill-doctor`; the lane owns the eval (Tier-0 exit-coded harness
15/15, negative-control-proven + Tier-1 non-comparative blind panel, both PASS). Retrieval-sweep
composition (for KB discovery) is operator-composed at the prompt, never shipped in the skill body.

## 0.3.0 — 2026-09-03

**Changed — macro references migrated to the `!!` ontology.** `smart` and `ideate` reference the magic
plugin's operator macros as downstream targets; those references now use the `!!` names —
`think!`→`think!!`, `auror!`→`run!!`, `gauntlet!`→`gauntlet!!` — across `description` triggers, bodies,
`references/output-format.md`, and the plugin manifest. Each skill's **own** trigger also migrates for full
`!!` uniformity: `smart!`→`smart!!`, `ideate!`→`ideate!!` (behavior unchanged). Guard: `smart`'s `S12`
compose-check rebased onto the new names.

## 0.2.2 — 2026-08-28

**Fix (`ideate`) — console-safe output format (backport of smart's 0.2.1 fix).** `ideate`'s Phase-2 output
block used the same fixed-width aligned-column layout (`Problem:  …   Rubric:`) that deformed for `smart` —
long real-world values broke on console word-wrap and couldn't be copied without reflow. Reshaped to
**flush-left `###`-per-field markdown** (Problem · Rubric · Field · Top-N · Usage); exact template in
`references/output-format.md`. Harness guard `S16` (no aligned columns) + `S15` extended to the reference.
Both `think` skills now emit console-safe output. (THINK-01-03.)

## 0.2.1 — 2026-08-13

**Fix (`smart`) — console-safe output format.** The Phase-2 sharpened-goal block used a fixed-width
aligned-column layout (padded `Field:` labels, right-floated `[Measurable ✓]` tags, `•` hanging indents)
that **deformed on console word-wrap** — long real-world values couldn't be copied from terminal output
without manual reflow. Reshaped to **flush-left markdown**: one `###` heading per field, values on their own
lines, tags inline as a lead-in, sub-points as flush-left `-` bullets. Exact template moved to
`references/output-format.md` (keeps `SKILL.md` ≤60). Harness guard `S16` locks the format (no aligned
columns); `S15` extended to cover the reference.

## 0.2.0 — 2026-08-12

**New skill: `smart` — front-door goal-shaper (the kit's IFR builder).** Turns a vague goal into a
think-deep-ready statement carrying the two properties a run needs — **Measurable** (a success signal a gate
can evaluate) and **Convergent** (a reachable stop, not "as good as possible") — with light Specific/Relevant
(anti-drift) + Achievable (feasibility) checks, and **Time-bound reinterpreted as convergence, never a clock**.
It **names** the measure and **defers** operationalization: authors **no** executable `Done-when`
(think-deep's) and **no** acceptance/quality bar (critic's). Emits the sharpened-goal block and **STOPs**
(feeder — runs inline, never spawns); standalone (no cross-kit dependency). Reframes goal-shaping as
**IFR-building** — a sharpened goal (objective + measurable signal + convergent stop) *is* a checkable Ideal
Final Result. Frontmatter-owned trigger (`smart!` / `/think:smart`), no macro. README in
`docs/specs/think/smart/`; static + behavioral eval (`G1`–`G8`, negative-control-proven; ≤60 line budget).
The general (any-goal) front door — sibling to `critic` (the specialized quality-bar case).

## 0.1.0 — 2026-08-12

**New plugin: `think` — divergent front-doors.** Ships its first skill, **`ideate`** — the divergent
front-end of the kit. For a problem it generates 5–15 genuinely diverse candidate ideas (each forced from
a **distinct lens**), adversarially reviews them against a **pinned merit rubric** (composing the `magic`
plugin's `critic` as the judge — never a bespoke inline scorer), and selects **comparatively**
(refute-each-then-rank ≤8 ideas · pairwise tournament larger) to return the **top N** (default 3, `N=1` on
request) with the rationale each survived on + its main risk — then **STOPS**, feeding the winners to
`think!` / `auror!` / `gauntlet!` / `smart!`.

- The **mirror twin of `gauntlet`**: `ideate` diverges (many ideas → select the best against a rubric);
  `gauntlet` converges (one target → build it to a blind-vs-reference bar). Distinct on four axes:
  ideas-not-builds · rubric-not-external-reference · diverge-not-converge · run-not-print.
- **Depth-safe runner-feeder** — fans out at depth-0, STOPs at top-N; degrades to inline generation +
  judging when itself a subagent (never nest-spawns).
- **Frontmatter-owned trigger** (`ideate!` / `/think:ideate`), explicit-only — no operator macro.
- **Standalone** — no cross-kit dependency; the only skill it composes is `magic:critic`. Carries a small
  generic lens catalog (`references/lens-catalog.md`).
- Static + behavioral eval package (deterministic harness, negative-control-proven; golden set `I1`–`I7`).
