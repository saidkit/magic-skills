# Changelog — think plugin

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
