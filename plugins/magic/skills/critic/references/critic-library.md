# Critic library — worked acceptance bars

A lookup of hard-won bars. **Find the nearest target, adapt its standard from the interview.** Every bar: never an **absolute self-score** ("8/10" — never terminates), never a **pre-written feature checklist** (reward-hackable). A bar is *comparative* (blind vs a reference), *review-found* (defects until none), or *executed* (runs green).

## Ask the user first (no answers → no bar)
1. **Standard** — what is "good", concretely? the exemplar to match/beat · the spec to pass · the convention to hold. Un-nameable → say there is no bar.
2. **Reference** — what the judge holds it against: screenshot · footage · recording · golden dataset · test suite · exemplar doc · the real product. Get its path/handle.
3. **Stakes → K/N** — low → 3/4 · noisy (feel/taste) or high → 5/7 · 7/10 · binary/exec → pass-fail.
4. **Guardrails** — the executable floor that holds regardless: tokens · tests · budget · a11y.

## Bars  (C = critic's comparative bar · T = route to think-deep, not a comparative bar)

- **C · 3D game / scene** — decompose (textures · lighting · geometry · physics · movement/feel · sound). *Look* parts: blind vs **footage** ≥4/5. *Feel* parts: **paired hands-on A/B** (play build then the real one, order random, "which feels closer") ≥5/7. Guardrail: frame-rate, no crashes.
- **C · UI surface** (hero · component · page) — parts (headline · CTA · visual · layout); each blind vs `ref.png` ≥4/5. Guardrail: brand tokens ∈ kit, renders at widths, no console errors.
- **C · Logo / brand mark** — blind vs a 3–5-option moodboard, whole-mark ≥3/4 across contexts (favicon · header · mono). Guardrail: legible at 16px, works 1-color. (Not "renders at widths" — it's an asset.)
- **C · Marketing copy / tagline** — beat-baseline: blind-pick new vs current on a **pinned voice** ≥5/7 (raise N — copy is noisy). Guardrail: on-message, no false claims.
- **C · Long-form** (post · report · docs) — blind vs an exemplar, whole-read (argument · clarity · flow) ≥4/5. Guardrail: claims sourced, required sections present.
- **C · Audio** (jingle · VO · SFX) — blind **listen** vs the reference track ≥4/5. Guardrail: loudness/format spec, no clipping.
- **C · Video / animation** — blind **watch** vs a reference clip, per-beat ≥4/5; judge timing/pacing, not just frames. Guardrail: duration, resolution, no dropped frames.
- **C · Slide deck / pitch** — each slide blind vs an exemplar deck ≥4/5 **+** the narrative arc survives an editor's review. Guardrail: on-brand, one idea per slide.
- **C · A skill / prompt / tool** — beat-baseline: run **with vs without** on realistic tasks, blind-judged on a pinned criterion ≥K/N; the baseline is already competent → raise N and add an **executable floor** (output passes the convention's linter). Plus an adversarial review of the text.
- **T · Software feature** — adversarial review until **0 open P0/P1 and nothing new**; security/money/data → reviewer takes an **attacker stance**; + tests green, no regressions. (Survives review + tests, not a blind A/B.)
- **T · API / endpoint to a spec** — execution: contract tests · typecheck · every documented status/shape returned; pass/fail. Adversarial surface → add the software-feature review on top.
- **T · Data / model result** — recompute + spot-check vs a source of truth; **0 discrepancies**; reproducible; figures reconcile to source.
- **T · Refactor / cleanup** — no behavior change: full suite green, no regressions, review finds no new smell, diff stays in scope.
- **C+T · Data dashboard** (compose) — **T** every number recomputes vs source **+** **C** the viz blind vs an exemplar ≥4/5. Wrong numbers OR ugly chart = fail.
- **C+T · Landing page** (compose) — **C** visual vs exemplar **+** **C** copy beats the current line **+** **T** brand tokens ∈ kit. Stop when all pass.
- **C+T · Multi-step flow** (checkout · onboarding · wizard) — per step: **C** the screen vs exemplar **+** **T** the feature review (attacker stance if it moves money/data) **+** **T** endpoints to spec; cross-step: state survives back / refresh / abandon. Stop when every step *and* the whole path pass.

Absent target → adapt the nearest. Compose the conjunction; don't stop until every sub-bar passes.
