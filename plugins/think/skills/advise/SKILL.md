---
name: advise
description: >
  Grounded-decision front door: turn ONE owed decision you cannot answer — "I have no idea", "I don't know the
  consequences", or a bare lean about to be recorded ("I'll just go with X, moving on") — into a recommendation
  grounded in a real EXPERIMENT, then brief the owner and STOP. It states the task and measurable success criteria,
  ideates different solutions, builds and runs them against the REAL engine, weighs drawbacks and consequences, only
  then chooses, verifies its conclusions, and hands the owner the call.
  Activates ONLY on an explicit `/think:advise <question>` or `advise!! <question>` invocation AND NOTHING ELSE —
  NOT `ideate` (diverges options, no decision owed), NOT `smart` (shapes a goal), NOT `critic` (authors a quality
  bar), NOT a walk of many questions (drive that yourself, calling advise per question). It grounds and recommends ONE
  decision, then STOPS: it never implements the decision and never settles a load-bearing or reserved choice for
  the owner.
---

# Advise — run the experiment, then brief the owner

The owner invoked this because a decision is owed and the honest answer is "I'm guessing". The invocation IS the
instruction to experiment: do not argue your way to an answer, record the lean, default to a precedent, or hand the
question back untested.

## Do this, in order
1. **State the task and measurable success criteria first** — what a good answer must satisfy — before trying anything.
2. **Quick sweep.** If a decision record already settles this exact question, or one plain, citable fact — never a
   tradeoff or a similar-but-different precedent — answers it, cite it (`path:line`) and stop there
   (`already-decided` / `decided`). Minutes, not the run.
3. **Ideate at least two genuinely different solutions** — the lean as stated, and its real alternative.
4. **Run the experiment on the real engine — cheapest decisive check first.** Name the ONE check that could pick the
   winner among all your candidates — one run of an existing test or harness, or one measurement on a handful of real
   cases (include one a wrong answer would wrongly pass) — and run it. If it picks the winner against the step-1
   criteria, that check IS the experiment: stop running things and go to step 5. If it only rules one candidate out —
   without confirming the survivor clears the criteria — or only reads text where the candidates would have to be run
   to differ, it has not picked a winner: build each remaining candidate minimally and run them all on the same cases
   — real ones, adversarial ones, and a negative control (a case a broken or over-permissive candidate would wrongly
   pass) — independent candidates in separate subagents so one cannot leak into another. When the thing under test is
   itself a skill or a prompt, the engine is a blind subagent executing it on the same specs — run that. Capture
   output mechanically, never from memory.
5. **Estimate each candidate's drawbacks and consequences** from what the runs showed — by reasoning, not extra
   runs, for a candidate the one check never touched.
6. **Only then choose — and verify the conclusions.** Re-read the results against the step-1 criteria and ask what
   they actually license: a true finding can carry a wrong inference. If step 4 went to the full build-and-run
   comparison and others will build on its result, get an independent adversarial pass (a reviewer who did not do
   the work, briefed to make it fail) and re-run its counter-cases yourself.
7. **Brief the owner and STOP.**

## Hold every run
- **Never escalate a premise you have not tested** — "is this even possible?" is answered by step 4, with evidence.
- **Real engine only** — the project's actual code or artifact, never a toy reimplementation or a typed-in result.
- **Read-only.** You may ADD an evidence record (under the feature's working directory, or beside the code where
  there is none); change no existing file; never commit.
- **The owner decides** anything load-bearing or reserved (an open question or conflict, a manual acceptance) — you
  recommend, attended or autonomous. Only a reversible detail may be settled and reported.
- **Compose.** Where a dedicated skill for a step is installed (a decision-record search, `ideate`, `critic`), use
  it; otherwise do the step inline and say so.
- **One decision, then STOP** — never implement it, never walk on to the next question.

## The brief — the last thing you print
Flush-left, Title Case `###` headings, a blank line between fields, each value on its own line, stop state first,
`### Explained` last (print the fields, not the code fence). A field the run never reached prints `n/a` — never
invent one.

```
### Advise
<already-decided | decided | recommend | escalated | blocked>

### Question
<the one decision, one line>

### Criteria
<the measurable bar from step 1>

### Experiment
none (<the record or fact that settled it>) | one-check: <command> — <result> | <path to the evidence record> — <candidates × cases, negative control named>

### Finding
<what the runs showed, mechanically>

### Conclusion
<what that licenses, checked against the criteria>

### Recommendation
<the option you recommend and why it won on the evidence, or n/a if none met the criteria>

### Drawbacks and Consequences
<what the recommended option costs, and what changes downstream>

### Owner Decides
<the choice that is the owner's> | n/a (reversible detail, settled)

### Explained
<the run explained in plain human language to the owner — see below>
```

`### Explained`, for the owner who will not read the fields — about 200 words, in this shape: the answer in one
plain sentence · one bullet per option, named and judged exactly as the fields name and judge it · what the run found, at most three bullets with
their numbers · **Recommend:** the option and its main catch · **You decide:** one bold line per owner decision with
what hangs on it, or that nothing is owed — every `### Owner Decides` item its own line, never merged. Plain language,
no jargon, command or path; say only what the fields say, each verdict and decision at its exact strength — never
"every" into "some", never "one" into "all"; leave details to the fields rather than blur them. Before printing,
reread it against the fields and fix every quantity, verdict and option name that differs.

Stop states: **already-decided** a held record answers it · **decided** a fact answers it, or a reversible detail you
settled · **recommend** briefed, the owner rules, no decision recorded · **escalated** the experiment ran and no
candidate meets the criteria, evidence attached · **blocked** it cannot be grounded from this project — name who or
what can, in `### Conclusion`.
