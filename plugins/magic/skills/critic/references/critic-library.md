# Critic library — comparative acceptance forms

Each entry: **domain trigger** → judgment form · reference type · stop threshold · guardrails.
Pick the nearest; ideate a new entry from the closest template when the domain is absent.
The blind A/B is for *perceptual* targets; non-perceptual domains gate by **execution**, not comparison.

## visual/UI — page · component · 3D scene · brand surface
- **judgment**: blind A/B of the render vs the reference, whole-artifact (composition, hierarchy, type, color, spacing, finish) — not a feature list
- **reference**: exemplar screenshot / brand kit
- **stop**: matches-or-beats the reference in **≥K of N blind looks** (default 4/5), A/B re-randomized each look
- **guardrails** (executable): brand-token conformance (colors/type/spacing ∈ kit); renders at target widths, no console errors

## document — report · spec · long-form copy
- **judgment**: rubric vs exemplar, whole-document read (argument, structure, clarity)
- **reference**: exemplar doc + a MUST rubric
- **stop**: all rubric MUSTs met **and** prefers-ours in **≥K of N** blind looks (default 3/4)
- **guardrails**: required sections present; every claim sourced

## data/analysis — metric · model · report figures
- **judgment**: recompute + spot-check against a source of truth (not aesthetic)
- **reference**: source dataset / known-good result
- **stop**: **0 discrepancies** on the checked set
- **guardrails**: reproducible end-to-end; figures reconcile to source

## code/API — service · endpoint · library (NON-perceptual: no blind A/B)
- **judgment**: execution, not comparison
- **reference**: spec / acceptance test suite
- **stop**: all tests + typecheck + endpoint checks **green**
- **guardrails**: no regressions in the existing suite

---

**Authoring notes**
- K/N is fixed **before** the run and never moved to manufacture a pass; raise N for higher stakes.
- The reference is per-task and comes from the interview — the library holds *forms*, not references.
- If a target spans domains (e.g. a data-viz page), compose: execution guardrails for the data + blind A/B for the surface.
