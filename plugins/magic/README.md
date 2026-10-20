# `magic` — plain-language guide to the operator skills

Eleven small, stack-agnostic skills for staying on top of a long working session: refresh your context, audit your progress, explain things simply, hand off cleanly, run a multi-step job carefully, manage its run files, hold work to a quality bar, generate a build prompt, record your rulings, and keep a work log in a note. You invoke each by typing a short word - no setup, no config. Part of [MagicKit](https://github.com/saidkit/magic-skills).

Every skill below has its full instructions in `skills/<name>/SKILL.md`. This page is the tour, with a couple of real "you type -> you get" samples each.

## At a glance

| Skill | What it does | You type |
|---|---|---|
| **refresh** | Quick "where were we?" recap of a long chat | `refresh!!` |
| **audit** | Full start-to-finish status audit (a table) | `audit!!` |
| **explain** | Explains what's going on in plain English | `explain!!` |
| **session** | Saves a handoff so a new chat picks up warm | `session!!` |
| **think-deep** | Runs a multi-step job and verifies the result | `/magic:think-deep` · `think!!` · `run!!` |
| **think** | Manages think-deep's run files — list, resume, clean up, move | `think!! list` · `/magic:think` |
| **critic** | Turns "make it good" into a finish line, then reviews | `critic!!` / `criticize!!` |
| **gauntlet** | Prints a ready-to-paste "build-to-a-bar" prompt | `gauntlet!!` |
| **prompt** | Writes a new prompt in your own voice from your saved prompt library | `prompt!!` |
| **ruled** | Records your rulings in your own words, quotes looked up in the session transcript | `ruled!!` / `/magic:ruled` |
| **worklog** | Keeps a work log in a note: one step per request, your request quoted with a short result | `/magic:worklog on <note>` |

The first three **just report and stop** — they show you where things stand and hand the decision back. The rest **do work.**

---

## refresh — a quick "where were we?"
Sweeps back through a long conversation and hands you a short recap: recent activity, where the work stands, constraints you set earlier, and 3–5 next actions. Then stops.

- **You type:** `refresh!!`
  **You get:** *"Recent: refactored the checkout page, fixed two failing tests. State: payment step works; the confirmation email is still stubbed. Constraints you set: keep it TypeScript, no new dependencies. Next: (1) wire up the real email, (2) test the empty-cart case, (3) update the changelog."*
- **You type:** `refresh!!` *(early in a short chat)* → a brief note that there isn't much to refresh yet — it's all still on screen.

*Full guide: `skills/refresh/README.md`*

## audit — the full status check-up
Reconstructs the whole task end-to-end and lays it out as a **status ledger** — every step marked Done / In progress / Blocked / Not started / Superseded, with evidence and a next action — then the blockers and the remaining path. Then stops.

- **You type:** `audit!!`
  **You get:** a one-line task restatement, then a table like:

  ```
  | # | Step          | Status      | Evidence / notes        | Next action      |
  |---|---------------|-------------|-------------------------|------------------|
  | 1 | Sign-up form  | Done        | PROJ-01 shipped, tested | —                |
  | 2 | Welcome email | In progress | draft written           | wire up the send |
  | 3 | Error copy    | Blocked     | waiting on the writer   | ping them        |
  ```
- **You type:** `audit!!` *(before a handoff)* → the same audit, so nothing quietly falls through the cracks.

*Full guide: `skills/audit/README.md`*

## explain — explain it in plain English
A jargon-free explanation of where things stand or what something means — the gist, the current state, and the practical "so what." No code, no status tables.

- **You type:** `explain!! what this change actually does`
  **You get:** a couple of plain sentences — what it's for, what's different now, and why it matters, without walking through the code.
- **You type:** `explain!! give me something I can send to a non-technical teammate` → one clear, shareable sentence you can paste into a message.

*Full guide: `skills/explain/README.md`*

## session — save your place for a new chat
Writes a handoff file so tomorrow's session (or a teammate's) starts warm: what's done, in progress, and blocked, the decisions and why, and pointers to the files that matter. It confirms the details with you first.

- **You type:** `session!!`
  **You get:** *"Before I save — this is the billing feature, id `PROJ-01`, session 2. Sound right?"* Once you confirm, it writes `working/PROJ-01/session-2.md` and tells you it's saved. Next chat: *"read `working/PROJ-01/session-2.md` and let's keep going."*
- **You type:** `session!!` *(handing off to a teammate)* → the same quick confirm, then a file their chat can open to get the full picture — no long write-up needed from you.

*Full guide: `skills/session/README.md`*

## think-deep — a careful worker for multi-step jobs
Breaks a task into a short plan, does each step with a self-check, then verifies the whole result against your "done when…" criteria — looping to fix whatever failed. Three ways to call it, by how hands-on you want to be.

- **You type:** `run!! add pagination to the results table and make sure the tests pass`
  **You get:** a plan, each step done with a self-check, a final run against "tests pass," and a short report — fully hands-off.
- **You type:** `think!! migrate the CSV import feature to the new config format` → the task restated with a plan for your **approval**, then it works through each step with checks.

*Full guide: `skills/think-deep/README.md`*

## critic — turn a fuzzy goal into a finish line
Pins a vague standard ("make it good", "as good as that page") into a concrete, finishable **done-when**, then reviews your target against it — so a quality loop can actually stop.

- **You type:** `critic!! review the pricing page against ref/hero.png`
  **You get:** a blind side-by-side bar from your example image, a ranked list of what's off (spacing, color, alignment), and **zero edits** to your files.
- **You type:** `critic!! get the checkout flow to production quality +fix` → a done-when of "zero serious issues and tests green," then the fixes applied until it clears the bar. *(Default is review, which never edits; add `+fix` only when you want changes.)*

*Full guide: `skills/critic/README.md`*

## gauntlet — a ready-to-paste build prompt
Writes (does **not** run) a strong copy-paste prompt that tells an AI to split the work into parts, put a builder and a harsh critic on each, and loop until every part matches or beats an example you name — judged blind.

- **You type:** `gauntlet!! a landing page as polished as ref/hero.png`
  **You get:** a copy-paste prompt that splits the page into parts (hero, pricing, footer…), loops each against `ref/hero.png`, and won't stop until each wins a blind side-by-side. You paste it and run it wherever you like.
- **You type:** `gauntlet!! a polished dashboard` *(no reference)* → it pauses and asks what to compare against, rather than inventing a bar.

*Full guide: `skills/gauntlet/README.md`*

---

## ruled - record what you ruled

- **You type:** `ruled!! use the short form` -> one line in the work's `rulings.md`, in your words, with an id taken from
  the time of your message.
- **You type:** `ruled!! sweep` -> the calls you made this session, shown as candidates; nothing is written until you confirm.
- Nothing is recorded unasked: without `ruled!!`, your ask to record or a dialog pick you asked to record, a message
  that looks like a ruling is acted on; nothing is proposed and nothing is written. A go-ahead on a step, a fact, a wording edit or a restatement is not a ruling.
- When you asked, the assistant proposed and you ruled, the document quotes your ask and your message; the adopted
  proposal goes in as short points, never as a copy. Caps apply per point. `ruled!! tidy <id>` rewrites an old
  document to the current form and keeps the id and the quotes byte-identical.
- An answer to a question you were shown gets a ruling document that quotes the question and your message word for
  word, filled from the session transcript by the bundled script (`scripts/rulings.py`), never typed by the assistant.
  `ruled!! check` validates the list; it runs with no git and no transcript.
- The script reads only Claude Code's own transcript store for the project (this session by default, another session
  of the project by name) and refuses a file anywhere else. It reads Claude Code's record but is not tamper-proof: a
  process that can write into the store can still plant a transcript there. The store is always
  `~/.claude/projects` of the user running it: a config folder relocated with `CLAUDE_CONFIG_DIR` is not supported. Quotes are checked against the
  transcript when the document is filled; `check` later reads the list and documents, not the store.
  A question-dialog answer is taken as the operator's pick; a host program or hook that answers the dialog itself
  would be read the same way.

## worklog - a work log kept in a note

- **You type:** `/magic:worklog on notes/task-log.md` -> the log is on for this session, kept in that note.
- From then on, every turn that acted on a request of yours ends with a new step in the note, written by the
  assistant after its reply: a `# Step N` heading, your request quoted as you typed it (a block you pasted is quoted
  one level deeper), and under it the result itself: a reply of up to 10 lines word for word, a longer one cut down
  in its own words (what changed, the numbers, what was checked, what was not) with its sections, tables and lists
  kept. A short message of yours such as "no" or "thanks" gets no step; its quote opens the next step.
- The step goes before the note's closing section that lists data files, or at the end when the note has none. Your
  own sections and the existing steps are left as they are; the note is re-read before every write.
- After writing a step the assistant ends the turn with one line, `worklog: step N`; nothing else about the log is said
  in chat. When the note cannot be written, the line reads `worklog: not written - <why>` instead. The line is
  there because the terminal's host asks for visible text when a turn ends on a file edit; it also shows you that
  the log is working. A turn that writes no step has no such line.
- What you do see: your terminal prints every file edit as a block with its diff, and the edit of the note is one.
  The skill cannot hide it; it comes after the reply, above the closing line.
- **You type:** `/magic:worklog status` -> on or off, and the note. `/magic:worklog off` -> the log is off.
- The assistant's first edit of the note asks for permission once; answering "always allow" covers the session. The
  skill grants itself nothing.
- **What it rests on.** The skill is an instruction and nothing else: it runs no script and keeps no file of its
  own. The quote is the assistant's copy of your message, and the step is the assistant's to remember;
  nothing checks either. After `/clear`, or in a long session whose context was compacted, type the command again.
- The log starts only when you type the command; it has no macro form.

## How they fit together
- **Lost the thread?** `refresh!!` (quick recap) · `audit!!` (full audit) · `explain!!` (plain-English explainer). All three report and stop.
- **Stepping away?** `session!!` saves a handoff for a fresh chat.
- **Real work to do?** `think-deep` (via `think!!` or `run!!`) plans, does, and **verifies** a multi-step job. `critic!!` pins a quality bar and reviews or fixes against it. `gauntlet!!` hands you a build-to-a-bar prompt to run elsewhere.

## Good to know
- **The diagnostics stop by contract.** `refresh!!` / `audit!!` / `explain!!` report and hand the decision back to you. To refresh *and then* keep going, use the `resume!!` macro (see [operator-macros.md](../../guides/operator-macros.md)).
- **Autonomy never green-lights an outward action.** A blanket `proceed!!` / `run!!` grant relaxes routine waits — never a decision reserved for you, and never an outward, hard-to-reverse operation (sending, publishing, deleting). These skills ship no tool-level fuse for that; consent for such an operation stays your own tool-permission configuration (allow / deny rules, approval prompts).
- **Nothing carries across calls.** Each invocation is a fresh sweep scoped to the message that triggered it — call again whenever you need another look. `worklog` is the exception: its switch lasts for the session, until `/magic:worklog off`, `/clear`, or a compaction that drops the command from the context.
- **No project files, no config.** These skills read whatever layout your project already has and adapt (`docs/adr/` vs `decision-log/`, `docs/working/` vs `notes/`, and so on).
