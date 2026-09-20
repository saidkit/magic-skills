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

## Step 2 - Turn it into a reusable instruction

Rewrite the fields as a **forward instruction for the next task of this kind** - imperative, general
enough to apply beyond this one dialogue, specific enough to change behaviour. Prefer the operator's
own approved formulations. This instruction is the deliverable; the seven fields are how you got
there.

## Step 3 - Discover the project's knowledge base

Find where the current project keeps its durable working rules - its **knowledge base**: the
convention docs, decision records, rule files, or contributor guides the project maintains
(project records / rules / conventions). Discover this generically from the project in front of you;
there is no fixed path, and this skill takes no dependency on any other plugin or tool to do it. If
the operator's setup provides a precedent-sweep helper, it is wired in from their macro, not named
here.

If the project keeps **no knowledge base**, skip reconciliation: present the standalone instruction
from Step 2 and stop. Do not create a knowledge base the project never had.

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
### Distilled instruction
<the forward instruction for next time>

### Method (seven fields)
Original task: <...>
Corrected: <...>
Dissatisfied: <...>
Vector change: <...>
Decisions: <...>
Formulations approved: <...>
Mistakes to avoid: <...>

### Knowledge-base proposal
Target: <candidate file, or "none - project keeps no knowledge base; standalone instruction above">
Change: <merge / add / supersede - because ...>
Diff:
<the proposed diff>

Awaiting your confirmation before writing anything.
```
