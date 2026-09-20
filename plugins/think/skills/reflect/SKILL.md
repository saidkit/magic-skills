---
name: reflect
description: Distil the operator's working method from the CURRENT dialogue's corrections into a reusable instruction, then propose reconciling it with the project's knowledge base. Activates ONLY on the explicit "reflect!!" invocation, or an explicit request to "reflect on / distil the working method (rules, lessons) from this conversation" AND NOTHING ELSE. 
---

# reflect - distil the dialogue's working method

`reflect!!` captures *how the operator wanted the work done* - the corrections, reversals, and wording
they approved this session - as a reusable instruction, and files it where the project already keeps
its rules. Two constraints make it trustworthy: never invent a method the dialogue did not show, and
never overwrite what the project already decided.

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

The point of the seven fields is coverage: they force you past a bland summary into the operative
detail a future run can actually follow.

## Step 2 - Turn it into a numbered playbook

Rewrite the fields as a **numbered playbook for the next task of this kind** - a list of distinct,
deduplicated, imperative rules, **one rule per line**, ordered **highest-value first**. Lead with the
correction the operator pressed hardest or repeated - that is what they most cared about, and a future
run should meet it first. Ground each rule in something the operator actually did or said this session;
keep it general enough to apply beyond this one dialogue, specific enough to change behaviour, in the
operator's own approved wording where you have it. Decompose to the ATOMIC actionable level - one move per rule; a correction-dense session commonly
yields fifteen to thirty distinct rules, a thin one far fewer. Never pad to hit a count, and never
merge two real rules to shorten. Do not restate a playbook rule as its own negative anywhere else - in the Mistakes field list ONLY a
caution the playbook does not already carry, otherwise write "none beyond the playbook". The playbook
is the single home for the actionable rules. This numbered playbook is the deliverable; the
seven fields are how you got there. (A single dense paragraph is the failure mode - it hides the
distinct moves a future run needs to follow.)

## Step 3 - Find the right home (two kinds)

Working-method lessons and project rules live in different homes; find each. **Project-scoped
rules / decisions** (how this codebase or project is built) belong in the project's rule / decision /
convention docs. **Working-method lessons** (how the operator wants work done, across tasks) belong in
the operator's method store - wherever they keep durable how-to-work notes across sessions. A
working-method lesson usually belongs with method notes, not with a project's code-style rules - route
each conclusion to its fitting home. Discover both generically from what is in front of you; there is
no fixed path, and this skill takes no dependency on any other plugin or tool to do it. If the
operator's setup provides a precedent-sweep helper, it is wired in from their macro, not named here.

If a home does not exist, skip reconciliation for that kind and present the standalone playbook from
Step 2. Do not create a store that did not exist.

## Step 4 - Reconcile with what is already there

For a project that does keep a knowledge base, reconcile rather than dump:

- **Merge** the new conclusions into the closest existing rule where one already covers the area.
- **De-duplicate** - if the project already states this, do not add a second copy; strengthen the
  existing entry instead.
- **Surface contradictions** - when a new conclusion conflicts with an existing rule, do not silently
  overwrite it. Name the conflict and propose the change as "superseded - because <reason>", so the
  reversal is visible and the operator can judge it.

## Step 5 - Propose, then write only on confirmation

Never write to the knowledge base unprompted. **Propose first**, then **write nothing until the
operator confirms**. Present:

- the distilled reusable instruction (Step 2),
- the candidate target file(s) you would update or add (ranked, with why each fits),
- a concrete diff of the proposed change.

On confirmation, apply exactly the confirmed change. On decline, leave the project untouched - the
operator still has the instruction to file however they like.

## Output format

Emit the proposal as a **console-safe, flush-left** markdown block: one `###` heading per field, each
value on its own line, tags inline. Do not use fixed-width columns, padded labels, or right-floated
tags - they deform on terminal word-wrap. Keep it scannable.

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

### Knowledge-base proposal
Working-method home: <the method/notes store file(s), ranked; or "none - present standalone above">
Change: <merge / add / supersede - because ...>
Diff: <the proposed diff>
Project-rules home: <the project rule/decision doc(s), for project-scoped conclusions only; or "none">
Change: <merge / add / supersede - because ...>
Diff: <the proposed diff>

Awaiting your confirmation before writing anything.
```
