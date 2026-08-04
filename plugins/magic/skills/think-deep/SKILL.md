---
name: think-deep
description: >
  Structured task orchestrator — breaks complex tasks into steps with self-checking
  after each step. Creates execution protocol, validates results, corrects errors
  iteratively. Triggered ONLY by the explicit command "/magic:think-deep". Do NOT trigger
  on general requests, problem-solving, analysis, or any other phrasing. Only the
  exact command "/magic:think-deep" activates this skill.
---

# Think-Deep: Structured Task Orchestrator

Solve complex tasks by decomposing them into steps, executing each with mandatory 
self-check, and maintaining a live execution protocol. The user sees progress after 
every step — not just the final result.

**Prime directive — compose, don't emulate.** If the task names or implies a skill, 
`/command`, operator macro, or methodology/pipeline, your first job is to *invoke* it — 
not to reproduce its work by hand. Expand a macro to the skill(s) it maps to (per 
`CLAUDE.md`); a named multi-skill pipeline (e.g. "as said!") is invoked stage-by-stage 
in its declared order — never flattened into hand-rolled steps. Doing inline what a 
named capability would do is the primary failure this skill prevents.

**Language rule:** Always respond in the user's language. Detect the language of 
the user's message that invoked /magic:think-deep and use it for ALL output: phase 
confirmations, step results, self-checks, protocol file, final deliverable. 

## Phase 0: Understand

Before any work begins, establish clarity.

1. **Parse the task.** Read the user's request carefully. Identify: what is the deliverable? 
   What are the constraints? What domain knowledge is needed? And — **identify capability 
   signals**: named skills, `/commands`, operator macros, or pipeline references ("as X", 
   "the Y cycle"). Resolve each to the concrete skills it invokes — read the methodology's 
   map or the skills' descriptions for order + gates.

2. **If unclear — ask.** Do NOT guess. Ask the user ONE focused question about the 
   desired outcome. Do not ask multiple questions. Do not proceed until the answer 
   is clear.

3. **Restate and confirm.** Say to the user:
   
   > "Let me confirm I understand correctly: [restatement of task in your own words, 
   > including deliverable format, scope, and constraints]. Correct?"
   
   Wait for user confirmation before proceeding. If user corrects — restate again.
   **If the task names a skill/macro/pipeline, state the skills you will invoke** as 
   part of the restatement.

**Rules for Phase 0:**
- Do NOT start working before confirmation
- Restatement must be specific: not "you want me to analyze X" but "you want a 
  comparison of X and Y across dimensions A, B, C, delivered as a markdown table 
  with recommendations"
- If the task is simple and unambiguous, Phase 0 can be brief: restate in one 
  sentence, ask "Correct?", proceed on confirmation

## Phase 1: Plan

After user confirms understanding:

1. **Decompose** the task into concrete steps. Each step must have:
   - A clear deliverable (what this step produces)
   - A self-check criterion (how to verify this step succeeded)
   - A **`via:`** — the skill/command that performs it, or `inline` when no capability 
     covers it. A named pipeline's skills appear as `via:` bindings **in their declared 
     order** (its gates as their own steps); never substitute inline work for them.

2. **Create execution protocol file:**

Resolve `<protocol-dir>` once: the project's transient working directory if it has 
one (`docs/working/<feature>/`, `notes/`, `planning/`), otherwise the session 
scratchpad / temp directory. Never a hardcoded absolute path.

```
Path: <protocol-dir>/think-deep-protocol.md

Content:
# Execution Protocol: [task name]

## Task
[Confirmed restatement from Phase 0]

## Steps
- [ ] **1** [step description] → via: [skill | inline] → deliverable: [what], check: [criterion]
- [ ] **2** [step description] → via: [skill | inline] → deliverable: [what], check: [criterion]
- [ ] **N** [step description] → via: [skill | inline] → deliverable: [what], check: [criterion]

## Results
(filled during execution)
```

3. **Output to chat:** the full step list. Nothing else. User sees the plan.

**Rules for Phase 1:**
- Steps should be 3-10. Fewer = too coarse. More = over-decomposed.
- Each step must be independently executable and checkable
- Steps are sequential by default. Note dependencies if non-obvious.
- If task requires research/tools — note which tools in step description
- **Plan self-check:** if the task named a pipeline/skill and it is absent from your 
  `via:` bindings, the plan is wrong — rebind before executing.
- **Loop-shaped `via:` bindings.** If a `via:` names a skill whose contract is a re-entrant 
  loop — it reconstructs state, acts, then re-enters until its own stop condition — the step 
  reads **"drive X to its stop condition via repeated invocation"**, never "invoke X". 
  Invoking a loop once demotes it to a subroutine and silently discards every rule it would 
  have enforced on later passes; the plan's own steps then become the only enforcement, and a 
  step that quietly fails to run leaves none. Such a plan MUST also carry a **final step** 
  that re-invokes the skill and records its stop-condition output verbatim.

## Phase 2: Execute

For EACH step, in order:

### Step execution

1. **Do the work.** Execute the step. Use tools, write files, search, analyze — 
   whatever the step requires.

2. **Self-check.** Immediately after completing the step, evaluate against the 
   check criterion defined in Phase 1. Write criticism to chat:

   > **Self-check [step N]:**
   > 
   > **What's good:** [specific positives]
   > 
   > **Criticism:** [specific issues found, numbered]
   > 
   > **Verdict:** [PASS / FIX NEEDED]

3. **If FIX NEEDED:** Fix the issues. Do NOT proceed to next step until fixed. 
   After fixing, re-run self-check. Note what was fixed.

4. **Update protocol file:**
   - Mark step as done: `- [x] **N** ...`
   - Write results summary for this step
   - If step list changed (new steps discovered, steps merged) — update list

5. **Output to chat:** brief step result (at most 3 sentences — what the step found, and anything that changed the plan) + updated remaining steps.

### Self-check rules

The self-check is NOT optional. It is NOT decorative. For each step, check:

- **Completeness:** Does the deliverable contain everything specified?
- **Correctness:** Are facts accurate? Are references valid? Are calculations right?
- **Consistency:** Does this step's output contradict previous steps?
- **Traceability:** Can every claim be traced to a source (data, tool output, reasoning)?
- **Bloat check:** Is there unnecessary content? Remove it.
- **Checkbox integrity:** a step may not be marked `[x]` while its Results entry reads 
  pending / blocked / not started / deferred. If the two disagree, the checkbox is wrong — 
  untick it and say so in chat. A plan that lies about its own completion is worse than no 
  plan, because everything downstream trusts it.

If self-check finds nothing wrong — that's suspicious. Look harder. At minimum, 
identify one thing that COULD be improved even if it's acceptable as-is.

## Phase 3: Deliver

After all steps complete:

1. **Final review.** Read the full protocol file. Check: do all step results 
   together form a coherent deliverable? Any gaps between steps?

2. **Assemble output.** Create the final deliverable in the format the user 
   expects (file, chat response, artifact — whatever was agreed in Phase 0).

3. **Present.** Output the deliverable. Add a brief summary of:
   - What was done (2-3 sentences)
   - Key decisions made during execution
   - Known limitations or caveats

Do NOT repeat the entire execution history. User already saw it step by step.

## Anti-patterns (things to avoid)

- **Emulating a named skill/macro/pipeline instead of invoking it** — the #1 failure. 
  If a capability exists for the step, call it; don't hand-roll its output.
- **Letting an autonomous mode (`auror!`/`expelliarmus`) drop a *stage/gate*** — 
  autonomy removes *waits*, not stages. Suppressing a pause never removes the gate it guarded.
- **Skipping self-check** because "this step is simple." Every step gets checked.
- **Rubber-stamp self-check** ("looks good!"). Must identify specific positives 
  and specific concerns.
- **Rewriting the plan silently.** If steps change — say so explicitly in chat.
- **Gold-plating.** Delivering more than asked. Stick to confirmed scope from Phase 0.
- **Apologizing for corrections.** Finding and fixing errors is the SYSTEM WORKING. 
  Not a failure. Do not apologize.

## When NOT to use this skill

- Simple factual questions
- Quick tasks (< 2 minutes of work)
- Creative writing where structure kills flow
- When user explicitly asks for a quick/rough answer

If "think-deep" skill is invoked but the task is trivial, say so: "This task is 
straightforward enough to handle directly. Proceeding without full protocol. 
[answer]"
