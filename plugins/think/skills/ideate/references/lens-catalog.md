# Ideate lens catalog — forcing a genuinely varied field

Divergence is **forced**, not hoped for. Generate **one idea per lens**, tag it with the lens, and prune near-duplicates — a field of 15 free-form ideas collapses to one idea restated 15 ways, and adversarial review of near-duplicates is theater. Pick the lenses that fit the problem; aim for **5–15 ideas** total. The goal is *distinct corners of the space*, not a fixed count.

## The lenses (each forces a different corner)
- **Cheapest / smallest** — the least-effort thing that could possibly work; strip to the minimum viable move.
- **Most-ambitious** — ignore cost and risk; the 10× version with unlimited resources. Sets the ceiling.
- **Contrarian / invert** — do the opposite of the obvious default; negate an assumption everyone shares.
- **Adjacent-domain** — steal the pattern another field already solved this with (biology · games · logistics · finance).
- **Constraint-removed** — delete the one constraint taken as fixed (no budget cap · no legacy · no deadline); what opens up?
- **Constraint-added / forcing** — impose a hard limit (one week · one file · zero new deps); scarcity breeds a different shape.
- **User-first** — start from the end-user's job-to-be-done, not the system; what would delight them regardless of build.
- **Risk-first** — start from the biggest failure mode and design to neutralize it; the safe-by-construction option.
- **First-principles** — rebuild from the ground truth of the problem, ignoring how it is done today.
- **Buy / borrow / integrate** — don't build; compose an existing tool, service, or library that already does it.

Small and generic on purpose — add a problem-specific lens when one is obvious, drop the lenses that don't fit.

## Merit rubric — the anchor (pin it *before* judging)
Ideas have no external reference, so **the rubric is the anchor** — the standard the review holds ideas to. Pin it before any judging, drawing on `critic`'s pin-the-standard-first discipline; an unpinned rubric drifts. A default axis set, reweighted per problem:
- **Feasibility** — can it actually be built/done with what's on hand?
- **Fit-to-intent** — does it solve the *actual* problem, not an adjacent one?
- **Impact** — how much does it move the needle if it works?
- **Novelty** — does it open something the obvious answer doesn't?
- **Effort / risk** — cost to try × chance it fails.

Weight to the problem: a throwaway prototype weights feasibility/effort; a strategic bet weights impact/novelty.

## Selection method (comparative, never absolute)
- **≤ 8 ideas — refute-each-then-rank.** Take an attacker stance on each idea against the rubric (surface its fatal flaw / worst-fit axis), then rank by what survives. Robust for a small field.
- **larger field — pairwise / tournament.** Blind side-by-side "which better meets the rubric" comparisons, bracket down to the top-N. Comparison ranks more reliably than isolated scores.

In both, the per-idea refutation is **`critic`'s** (review mode against the rubric-standard, or its refute-first library applied inline) — ideate adds only the comparative ranking, **no bespoke scorer**. Emit the top-N with, per winner, the rubric fit it survives on and its main residual risk.
