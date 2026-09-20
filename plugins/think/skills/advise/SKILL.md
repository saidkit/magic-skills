---
name: advise
description: >
  Grounded-decision front door: turn ONE owed decision you cannot answer — "I have no idea", "I don't know the
  consequences", or a bare lean you are about to record ("I'll just go with X, moving on") — into a recommendation
  grounded in a real EXPERIMENT, then brief the owner and STOP. Frame measurable criteria, sweep precedent and
  facts only far enough to avoid re-deciding a settled thing, generate candidates, run a battery of real +
  adversarial cases with a negative control against the REAL engine, verify the conclusion, and hand the owner
  the call. It is for the moment a decision is owed and the honest answer is "I'm guessing" — the bare lean about
  to be recorded, the precedent about to be defaulted to, the premise about to be escalated after a couple of failures.
  Activates ONLY on an explicit `/think:advise <question>` or `advise!! <question>` invocation AND NOTHING ELSE —
  NOT `ideate` (diverges options, no decision owed), NOT `smart` (shapes a goal), NOT `critic` (authors a quality
  bar), NOT a walk of many questions (drive that yourself, calling advise per question). It grounds and recommends ONE
  decision, then STOPS: it never implements the decision and never settles a load-bearing or reserved choice for
  the owner.
---

# Advise — ground one owed decision by experiment, then brief the owner

One question in; one grounded recommendation and one legible stop state out. When you don't know and it matters,
you **run a small experiment** — you do not argue, guess, default to a stale precedent, or escalate a premise you
could have tested. The owner keeps the call; you hand it over with the evidence attached.

## Invocation & parameters
`/think:advise <question>` or `advise!! <question>`. Optional inputs:

| Input | Effect |
|---|---|
| a pointer to where the decision lives (a file + an id) | opened in the sweep before the question is treated as open |
| `Handed-in precedent:` findings from a caller | accepted, but the record it cites is opened before it is relied on |

## Contract — holds every run
- **Experiment before you conclude — but size it first.** When a question is *genuinely empirical* — the real
  engine's behaviour is what separates the options — and **no single check (G1) would settle it**, a battery is
  the default and skipping it is the exception the brief must justify; reasoning your way to such a decision when a
  cheap experiment was available is the failure this skill prevents. *Empirical* is the gate: a question that turns
  on a rule, a fact, or a preference never gets a battery — it settles on the **SPEND ladder** (below, G0/G1/G2).
  Proportionality sizes the experiment; it never cancels a needed one — guessing on an empirical decision is the
  same failure as a battery on a fact.
- **Never escalate a premise you have not tested.** A criterion failing twice is a signal to state measurable
  criteria and run the battery, then choose the path from data — not to stop and ask the owner "is this even
  possible?". Escalate only after the experiment, and only with its evidence attached.
- **Compose, never reimplement.** Every mode but the experiment has an owner (routing in `references/modes.md`);
  invoke it. The experiment is the only mode this skill owns natively. An owner that is not installed degrades to
  a bounded, *declared* inline equivalent — the skill still works in a `think`-only install.
- **Real engine, mechanical capture.** An experiment runs the project's actual code or artifact, never a toy
  reimplementation and never hand-typed results; captures mechanically; and writes its record into the feature's
  working directory — or, where the project has none, a `probe-<topic>.md` beside the code — so the brief cites a path.
- **Read-only until the decision is recorded.** You may ADD an evidence record under the feature's working
  directory (or the fallback beside the code); you change no existing project file. Recording the owner's decision
  is the one write, and only after they rule.
- **The owner keeps what is theirs.** A load-bearing choice, or anything the project reserves for the owner (an
  open conflict or question, a forcing function, a manual acceptance item), is *recommended*, never self-decided —
  attended or under an autonomy grant. A standing "make a defaulted decision" covers reversible leaves only;
  reversibility alone is no licence.
- **One decision, then STOP.** Ground the decision named and brief it; never implement it, never walk to the next
  question.

## The cycle
Steps 1–2 are a fast filter — spend little there. Step 4 is where the work is.

### 1. Frame
State the decision as a task with **measurable success criteria** — what a good answer must satisfy — before you
try anything, so the experiment has a scorable target rather than a vibe. A decision with no statable criterion is
usually the owner's judgment call; say so and route it to them.

### 2. Sweep — only to avoid wasted work
Its whole job is to keep you from experimenting on a settled question and to size the spend; this is the one place
"cheapest first, stop when answered" applies.
- **Precedent AND its outcome** — route to a decision-record search (`precedent!!`) if installed, else sweep the
  project's records inline. Ask two things: *was this decided?* and ***how did it turn out*** — held, superseded,
  never ratified. A precedent whose outcome was bad is evidence *against* defaulting to it. Count a claim as
  precedent only if its record is reachable and is the record that *made* the decision — not a restatement or a
  derived doc. A held record that squarely answers it → stop at `already-decided`, cite it.
- **Facts** — route to a read-only investigation, else read the real code. Answer fact-shaped questions by
  citation (`path:line`) and set the spend tier. A plain fact that answers it → stop at `decided`, cite it.

**Set** the two axes now (below), provisionally: the **spend ladder** sizes step 4 (G0 cite / G1 one check / G2
battery) — G1's check *runs* once candidates are named (step 3); the **ownership flag** sets the stop state.
Reserved does not mean battery.

### 3. Candidates
Name at least **two** genuinely distinct options — cheap, and always: G1's settling check needs candidates to test
against. **Prototypes are G2 only** — where no option exists yet, build throwaways only once the ladder reaches G2.
Route to `ideate`. Each option carries its main consequence; a question settling at G0/G1 skips to **step 5**.

### 4. The experiment — the core, GATED
Build a battery ONLY when the spend ladder reaches **G2** — genuinely empirical *and* no single G1 check settled
it (the ladder decides this, not this step). Build one anyway and the brief must name the single check you
rejected and why. **A battery on a fact, a rule, a
cheap-check, or a preference is the same failure as guessing on an empirical one.** When it is genuinely G2, run
**every candidate arm on every case**:
- **Cases = real + adversarial + a negative control** — a case built so a broken or over-permissive arm PASSES
  when it should FAIL; without it the battery cannot tell "sound" from "lucky".
- **Real engine**, run on each case; captured **mechanically** (redirect the real output), never by hand.
- **Isolate the arms** — a subagent per arm where they are independent, so one arm's state cannot leak into
  another's; where a subagent is unavailable, separate mechanical invocations, and say so.
- **Write it down** — the battery, the per-arm/per-case table and the negative-control row go under the feature's
  working directory (fallback as above); the brief cites this file. Record format in `references/probe-record.md`.

### 5. Verify the conclusion — not just the finding
A probe can report a **true fact and draw the wrong inference**. Re-read the results against step 1's criteria and
ask what they actually license; classify any earlier evidence record `sound` / `insufficient` / `contradicted`
before relying on it. For a **load-bearing model** (a claim others will build on), get an independent
adversarial break — route to `critic` with reviewer ≠ builder, briefed to make the model FAIL. This is **one
step**, not the skill's purpose.

### 6. Brief the owner, then STOP
Emit the brief (below) and hand the decision over. Record the decision only after the owner rules (a reversible
leaf may report-and-proceed under an autonomy grant; a load-bearing or reserved one never may). Then STOP.

## Two questions, kept separate — how much to spend vs who decides
*How much evidence* and *who makes the call* are different axes; answer them separately, or every reserved question
drags in an experiment it does not need.

### How much evidence — the SPEND ladder (first match wins — except G1, which falls through when its check does not settle)
- **G0** — a reachable record or fact **settles** it → cite it; nothing heavier runs.
- **G1 — the settling test (a hard gate before any battery).** Name the **single measurement or citation** that
  would settle this and **run it**. If it separates every candidate against the step-1 criteria, stop there — one
  cheap check, no battery; most fact / rule / "who-decides" / "nothing-consumes-it" questions end here. If it runs
  and does **not** separate them, G1 did not settle it → fall through to G2.
- **G2 — battery** — reached ONLY when the decision is genuinely **empirical** AND no single G1 check settled it.
  The **empirical test**: name the observation the real engine could emit that would change your answer, and the
  command that emits it — can't name one the code can actually produce, it is **not** empirical (turns on a rule, a
  policy, a cost, or a preference) → no battery. If nothing cheaper settles it either, it is a **judgment call** —
  take it to the ownership flag and brief it (`recommend`, or `decided` if not reserved); never loop naming checks.

### Who decides — the OWNERSHIP flag (orthogonal; it sets the STOP STATE, never the spend)
- **Reserved** — the project reserves it (open conflict/question, forcing function, manual acceptance) OR it is
  load-bearing → **recommend**; the owner rules, never self-decided, attended or not; reversibility is no licence.
- **Not reserved** — a reversible leaf you may settle and report (`decided`).

Reserved-ness raises the bar for **deciding**, never for **experimenting** — spend on the ladder, ownership on the flag.

## The brief — console-safe, one `###` per field, values on their own line
The brief is the **last thing you print** — these fields, each on its own `### ` line, never narrated in prose
(print the fields, not the code fence). Flush-left, **stop state first** (never padded columns or right-floated
tags — they deform on wrap). A field the run never reached prints `n/a` — never invent one to fill it.

```
### advise
already-decided | decided | recommend | escalated | blocked

### question
<the one decision, one line>

### criteria
<the measurable bar from step 1>

### stakes
spend <G0|G1|G2> · owner <reserved|not-reserved> — <the single check that settles it, or why it is genuinely empirical (G2)>

### precedent
none | <path> (held | superseded-by <path> | unattributed)

### experiment
none (<why safe to skip>) | one-check: <path or command> — <result> | <path to the battery record> — <arms × cases, negative control named>

### finding
<what the battery showed, mechanically>

### conclusion
<what that licenses — checked against the criteria, not just restated>

### recommendation
<one line: the option you recommend and why it won on the evidence>

### drawbacks
<the recommended option's main cost / what it gives up>

### consequences
<what changes downstream if this is adopted>

### owner-decides
<the choice that is the owner's> | n/a (reversible, proceeding)
```

## Stop states — a driver reads this line to know whether to advance
- **already-decided** — a held record answers it. *(advance)*
- **decided** — a fact answers it, or a not-reserved question you settled after its G0/G1 check. *(advance)*
- **recommend** — briefed; the decision is the owner's; nothing recorded. *(hold)*
- **escalated** — the evidence that ran (a battery or the G1 check) shows no candidate meets the criteria; evidence attached. *(hold)*
- **blocked** — it cannot be grounded from this project; name who or what can. *(hold)*

## When NOT to use
The decision is already made and you want it built → `think!!` / `run!!`. Options with no decision owed →
`ideate!!`. A goal to shape → `smart!!`. A quality bar to author → `critic!!`. A *list* of questions → walk it
yourself, calling `advise!!` per question. Expert knowledge to extract → `interview!!`.
