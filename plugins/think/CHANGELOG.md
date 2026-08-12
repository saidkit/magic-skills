# Changelog — think plugin

## 0.1.0 — 2026-08-12

**New plugin: `think` — divergent front-doors.** Ships its first skill, **`ideate`** — the divergent
front-end of the kit. For a problem it generates 5–15 genuinely diverse candidate ideas (each forced from
a **distinct lens**), adversarially reviews them against a **pinned merit rubric** (composing the `magic`
plugin's `critic` as the judge — never a bespoke inline scorer), and selects **comparatively**
(refute-each-then-rank ≤8 ideas · pairwise tournament larger) to return the **top N** (default 3, `N=1` on
request) with the rationale each survived on + its main risk — then **STOPS**, feeding the winners to
`think!` / `auror!` / `gauntlet!` (and `smart!` once it ships).

- The **mirror twin of `gauntlet`**: `ideate` diverges (many ideas → select the best against a rubric);
  `gauntlet` converges (one target → build it to a blind-vs-reference bar). Distinct on four axes:
  ideas-not-builds · rubric-not-external-reference · diverge-not-converge · run-not-print.
- **Depth-safe runner-feeder** — fans out at depth-0, STOPs at top-N; degrades to inline generation +
  judging when itself a subagent (never nest-spawns).
- **Frontmatter-owned trigger** (`ideate!` / `/think:ideate`), explicit-only — no operator macro.
- **Standalone** — no cross-kit dependency; the only skill it composes is `magic:critic`. Carries a small
  generic lens catalog (`references/lens-catalog.md`).
- Static + behavioral eval package (deterministic harness, negative-control-proven; golden set `I1`–`I7`).
