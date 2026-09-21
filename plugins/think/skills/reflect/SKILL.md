---
name: reflect
description: Distil the operator's working method from the CURRENT dialogue's corrections into a reusable instruction, then propose reconciling it with the project's knowledge base. Activates ONLY on the explicit "reflect!!" invocation, or an explicit request to "reflect on / distil the working method (rules, lessons) from this conversation" AND NOTHING ELSE. 
---

# reflect - distil the dialogue's working method

`reflect!!` captures *how the operator wanted the work done* - the corrections, reversals, and wording
they approved this session - as a reusable instruction, and files it where the project already keeps
its rules. Two hard constraints: never invent a method the dialogue did not show; never overwrite what
the project already decided.

## Where this runs (read first)

Run in the **main agent**, on the **current dialogue** only. You are the only context that holds the
conversation - a subagent cannot see it, so **never delegate the mining to a subagent**. If you are
invoked without a real dialogue to mine (a fresh session, nothing corrected yet), say so and stop;
there is nothing to distil.

## Step 1 - Mine the corrections, distil the seven fields

Read back over the conversation and extract the *method*, not the topic. The signal lives in the
operator's corrections: where they redirected you, rejected an approach, or approved a phrasing.
Distil these seven fields - name each one explicitly, and ground every line in something the operator
actually said or did (cite the turn where useful). If a field has no signal in this dialogue, write
"none observed" - do not manufacture one.

1. **Original task** - what the operator set out to do.
2. **What was corrected** - the concrete edits and redirections they made.
3. **What dissatisfied** - what specifically did not meet their bar, in their terms.
4. **Why the vector changed** - what made the direction shift mid-session.
5. **Decisions made** - the choices that got settled (and, briefly, why).
6. **Formulations approved** - the exact wording / framing the operator accepted.
7. **Mistakes never to repeat** - what must not happen again next time.


## Step 2 - Turn it into a numbered playbook

Rewrite the fields as a **numbered playbook for the next task of this kind** - a list of distinct,
deduplicated, imperative rules, **one rule per line**, ordered **highest-value first**. Lead with the
correction the operator pressed hardest or repeated. Ground each rule in something the operator actually did or said this session;
keep it general enough to apply beyond this one dialogue, specific enough to change behaviour, in the
operator's own approved wording where you have it. Decompose to the ATOMIC actionable level - one move per rule; a correction-dense session commonly
yields fifteen to thirty distinct rules, a thin one far fewer. Never pad to hit a count, and never
merge two real rules to shorten. Do not restate a playbook rule as its own negative anywhere else - in the Mistakes field list ONLY a
caution the playbook does not already carry, otherwise write "none beyond the playbook". The playbook
is the single home for the actionable rules. The numbered playbook is the deliverable; the seven fields are its source notes.

## Step 3 - Emit the playbook, then offer the next step

Present the numbered playbook + the seven fields. Then STOP; do NOT discover homes, render diffs, or write anything yet. Offer a short
menu and do only what the operator picks:

- **(a) Integrate now** - find the right home(s) for each conclusion and propose the exact changes (Step 4).
- **(b) Just point me where** - name the candidate home(s) and which existing entries this would touch, no diffs; the operator files it.
- **(c) Make it reusable** - turn the method into a reusable **instruction/rule**, a saved **prompt**, or a new **skill** (a skill-creator brief). Ask which.
- **(or nothing)** - keep the playbook as-is.

Wait for the choice. The heavy knowledge-base work (homes + diffs) is opt-in - it renders ONLY under (a).

## Step 4 - (a) Integrate: home, reconcile, propose (opt-in)

Only when the operator picks (a). Route by kind: **working-method lessons** to the operator's method
store (their durable how-to-work notes); **project-scoped rules / decisions** to the project's rule /
decision / convention docs. Discover both generically from what is in front of you - no fixed path, no
dependency on another plugin or tool. If the project keeps no knowledge base (no home for a kind), say so and keep the standalone playbook;
do not create a store that did not exist.

Reconcile rather than dump: **merge** into the closest existing rule; **de-duplicate** (strengthen the
existing entry, never add a second copy); **surface contradictions** as "superseded - because <reason>",
never a silent overwrite. Then **propose** the ranked home(s) + a concrete diff and **write nothing
until the operator confirms**; on confirmation apply exactly the confirmed change, on decline leave it
untouched.

## Step 5 - (b) point, or (c) make reusable

- **(b)** Name the candidate home(s), ranked, and the existing entries each conclusion would touch. No
  diffs, no writes - the operator files it.
- **(c)** Turn the method into the form the operator picks: an **instruction/rule** block ready to drop
  into a rules file; a reusable **prompt**; or a **skill-creator brief** (intent + contract) to author a
  new skill. Emit that one artifact; write nothing to a shipped location without confirmation.

## Output format

Emit everything as a **console-safe, flush-left** markdown block: one `###` heading per field, values on
their own lines, tags inline. Do not use fixed-width columns, padded labels, or right-floated tags -
they deform on terminal word-wrap. The DEFAULT emission is the playbook + fields + the menu; the
homes/diffs block appears only under (a).

```
### Distilled instruction (numbered playbook)
1. <highest-value rule - what the operator pressed hardest>
2. <next rule>
3. <... one distinct, actionable rule per line, at the granularity the dialogue supports>

### Method (seven fields)
Original task: <...>
Corrected: <...>
Dissatisfied: <...>
Vector change: <...>
Decisions: <...>
Formulations approved: <...>
Mistakes to avoid: <only a caution NOT already a playbook rule above; else "none beyond the playbook">

### Next step (pick one)
(a) Integrate now - I find the homes and propose the diffs.
(b) Just point me where - candidate home(s) + touched entries, no diffs.
(c) Make it reusable - an instruction/rule, a saved prompt, or a new skill (skill-creator brief). Which?
(or nothing - keep the playbook.)

--- if you pick (a), I then add, routed by kind ---
Working-method home: <method/notes store file(s), ranked; or "none">
Change: <merge / add / supersede - because ...>
Diff: <the proposed diff>
Project-rules home: <project rule/decision doc(s), project-scoped only; or "none">
Change: <merge / add / supersede - because ...>
Diff: <the proposed diff>

Awaiting your confirmation before writing anything.
```
