# Evidence modes — the sweep's routing table (step 2), not the unit's spine

The experiment (mode 4) is the skill's native core; the others exist only to keep you from experimenting on a
question already answered, and to size the stakes. Route each to its owner when installed; degrade to a bounded,
**declared** inline equivalent otherwise — the skill ships in a `think`-only install and must still work. Say
"routed to X" or "X not installed — bounded inline sweep of Y" so the brief is honest about what ran.

| # | Mode | Owner (compose) | Bounded inline fallback (declared) |
|---|---|---|---|
| 1 | **Precedent + outcome** | a decision-record search (`precedent!!`) | sweep the project's records — CLAUDE.md, memory, ADRs, prior working dirs, debriefs, and every record the question's own context cites; ask *decided? how did it turn out?* |
| 2 | **Facts** | a read-only investigation | search + read the real code; answer by `path:line`; set the spend tier |
| 3 | **Candidates** | `ideate` | list ≥2 distinct options with their main consequence; prototype where none exist — prototypes only at G2 |
| 4 | **Experiment** | *native — no owner* | — (never delegated; see the SKILL body step 4) |
| 5 | **Independent break** | `critic` (reviewer ≠ builder) | a fresh no-context reviewer pass, briefed to make the load-bearing model FAIL; re-run its counter-cases yourself |
| 6 | **Outside the project** | name the person / absent source; `interview!!` for an expert, web search for a fact | never invent the answer; options listed are marked ungrounded |

## Rules the routing must respect
- **Cheapest first applies HERE ONLY** (modes 1–2). It is never a reason to skip the experiment on a genuinely
  empirical question.
- **A held record that answers the question ends the run** at `already-decided`; a plain fact that answers it ends
  it at `decided`. Neither runs modes 3–4; a cited record is still classified at step 5. A question settled by a
  single G1 check runs no battery (mode 4) either.
- **Outcome-aware precedent** — a superseded or costly precedent is reported as such and is *not* defaulted to.
- **Handed-in precedent** is accepted from a caller, but the record it cites is opened before it is relied on; a
  citation that cannot be opened is reported as dangling, not as grounding.
- **Verify a conclusion, not just a finding** — an earlier probe/record is classified `sound` / `insufficient`
  (true but does not cover what the conclusion needs) / `contradicted` (a re-run disagrees) before use.
