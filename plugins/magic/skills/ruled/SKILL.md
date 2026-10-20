---
name: ruled
description: >
  Records the operator's rulings - the calls the operator made while working - in the operator's own words, one line
  each in the work's rulings.md, with a ruling document that quotes the question (or the operator's ask) and the
  operator's message word for word, looked up in the session transcript by a bundled script. Forms: record, +doc,
  doc <id>, sweep, list, pending, check, mark, tidy <id>. Records only what the operator consciously ruled, never an assistant proposal.
  Activates ONLY on "/magic:ruled" or "ruled!!" (with or without a form after it) AND NOTHING ELSE.
  NOT for: a message that merely states a preference without the trigger; an assistant's own proposal or default;
  a message from another session or agent; writing another tool's own records; a project's decision log or ADRs.
---

# ruled - record the operator's rulings

Write what the operator ruled, in the operator's words, into the `rulings.md` of the work this session is on.

## Contract - holds every run

1. Record only what the operator ruled. Never an assistant proposal, a default, a finding, or a peer's message.
2. Quotes and ids come only from the bundled script's lookup. When it refuses, say why and write nothing: delete a
   document skeleton you started, write no line. The one exception is a ruling stated outside a recorded session
   (see Provenance).
3. The list holds an optional title, then entry lines only. `landed` comes only from `mark`. A document is never
   rewritten, except by `tidy <id>`: the one exception to "a document is never rewritten".
4. After every write, run `check` on the list and print its output. When it fails on a line you wrote this turn, fix
   that line and run it again; never touch any other line.
5. Write a ruling only on the marker (`ruled!! <text>`, `/magic:ruled <text>`), on the operator's explicit ask to
   record it, or on an option the operator picked in a question dialog and then asked to record. Anything else,
   a plain instruction included, is acted on: nothing is proposed and nothing is written.

## Invocation

- `/magic:ruled <form>` or `ruled!! <form>`; the forms are listed under Forms.
- Run the script as `python3 ${CLAUDE_SKILL_DIR}/scripts/rulings.py <command>` (outside Claude Code: the
  `scripts/rulings.py` beside this file). It needs no git and no other skill.
  Outside Claude Code, drop `--session ${CLAUDE_SESSION_ID}` from the commands below.
- Paths in a list resolve from `--root` (default: the git root, else the current folder) and from the list's own
  folder: run with the current folder at the project top, or pass `--root`.
- The lookup reads only Claude Code's own transcript store for this project; it refuses a file or folder elsewhere.
  A lookup that says there is no transcript although the session has one: pass
  `--project-dir <the store folder holding this session's transcript>`.

## Where it writes

- `rulings.md` in the folder the operator names for the work; else in the folder where the work started (the work
  item's own working folder, or the idea's folder before the work has an id).
- No identifiable work: ask once which folder. Create the file when absent; its first entry is the ruling you write.
  A list stays in the folder where it was started.

## Words

- A ruling: the operator's binding call, made while working, recorded here. Never write "rule" or "decision" for a ruling.

## The line

```
- <id> - <who>, <status>: <ruling> [<evidence>]
```

- `<id>`: `WR-` plus the unix seconds of the operator's message (`WR-1790000000`). Take it from the lookup:
  `rulings.py find --quote "<a few distinctive words of the operator's message>"` prints the id, with a `-1`, `-2`
  suffix when two operator messages share a second.
  When the id is already in the list, that message is already recorded: say so and write nothing.
- `<who>`: `<who>` is the person who ruled, never a role word: the session user's name, else the git user name.
  Unknown: ask.
- `<status>`: `pending` when written; `landed`, `rejected` or `superseded` only through `mark`.
- `<ruling>`: see Wording.
- ` [<evidence>]`: what the ruling came from, each item a path, with an optional line or line range (`notes/plan.md:12`,
  `:12-18`); several are separated by commas. A ruling made in chat with nothing behind it: omit the brackets.
  A ruling with a document: the document's path comes first. A bracket at the end of the line is always read as
  evidence, so never end the ruling text itself with a bracket.
- A mark adds ` -> <home>[, <home>]` on `landed` (a home is a path, with an optional `#anchor`), or ` -> <new id>` on
  `superseded`.

## Wording

1. Use the operator's own words. Trim; do not rewrite.
2. One sentence. No reasons, consequences or examples.
3. When the operator's answer is "yes", "ok", an option letter or an option picked in a question dialog, write the option chosen, in the question's words, cut to fit the title cap.
4. Never longer than the operator's message, except under rule 3.
5. No middle-dot separator, no bold, no nested bullets.
6. Every part you write is terse: no reasons, no prose and no bracketed descriptions. The two block quotes are the
   only text written word for word.

## A line, or a line with a document

A ruling gets a document when any one of these holds; no other case gets one:

1. It answers a question the assistant showed (options, a yes/no question, a proposal the operator replied to, a
   question dialog).
2. Its text, worded as above, is over 160 characters or holds more than one rule.
3. The operator marked it `+doc`: `ruled!! +doc <text>`. Drop the mark from the text.

Three more cases always have one: a correction (it supersedes a ruling, see The document), a ruling stated outside a
recorded session (see Provenance), and `ruled!! doc <id>` (the operator asks for it). Apply these as written;
nothing else settles whether a document is written.

With a document, the line is `- <id> - <who>, <status>: <title> [<document path>, <evidence>]`: `<title>` is the
ruling in one sentence of at most 50 characters, from the operator's words where they fit. A document is written first, then the line that links it.

### The document

- In the list's folder, named `<yymmdd>-<number>-ruling-<topic>.md`: `<yymmdd>` the ruling's date; `<number>` the
  question's label as the question showed it (`5`, `a2`), else one more than the highest label made of digits only
  among the folder's ruling documents (1 when none); `<topic>` two to five lowercase words joined by hyphens.
- Write the skeleton with these parts, in this order:
  1. `# Ruling <number>: <title>`
  2. A header of bullets, read later by someone else, so with no session-bound words ("this session", "here"):
     Question (the topic asked, in a few words; "none, stated unasked" for an unasked ruling), Ruled by
     (the person, `{{time}}`, the id, session `{{session}}`), Provenance (`typed`, `dialog` or `stated-outside`)
     written as `{{provenance}}`, Replaces (the id it supersedes, or "nothing"), Standing (`final` or `assumed`):
     `assumed` when the operator's own words make the ruling provisional ("for now", "until", "unless"), else `final`.
  3. `## The question`: a block quote of the question as the assistant showed it, word for word: the placeholder
     line `{{question}}`. For an unasked ruling write "Stated by the operator, unasked." instead of the placeholder.
     When the operator asked, the assistant proposed and the operator ruled, this part is `## The operator's ask`
     instead: the placeholder line `{{ask}}`, a block quote of the operator's earlier message that asked for the
     proposal. Keep `## The question` as well only when the assistant also asked one. A lookup line
     `ask: <id>` is a hint: use the ask part with `--ask <id>` only when that message asked for what the assistant
     then proposed; when the assistant's text asks the operator something, even without `?`, quote it as the question;
     otherwise the ruling is unasked.
  4. `## The operator's message`: a block quote of the operator's message, word for word: the placeholder line
     `{{message}}`.
  5. `## The ruling`: numbered points, one point each, each at most 100 characters, with no parenthetical. For an
     adopted proposal: what is decided, one line each, no reasons, never a copy of the assistant's text. A reader who
     wants the proposal itself runs `rulings.py find --at <id>`.
  6. `## Evidence`: one line of paths only (`path` or `path:line`, separated by commas), or "None."
  7. `## If it turns out wrong`: one line of at most 12 words: what is redone.
  8. `## Not settled`: one line of at most 10 words, or "Nothing."
- Then fill it: `rulings.py find --at <id> --fill <document>`, adding `--ask <id of the ask>` for an ask part. Take
  the question, the ask and the operator's message only from the lookup; never type a quote. Check that the quoted ask is the one that asked for the proposal; if it is not, write the document in the unasked or question shape instead. The script replaces the placeholders in one pass. A refusal (no single operator
  message at that id): Contract rule 2. Check that the quoted
  question is the one the operator answered; if it is not, delete the document and say so.
- It holds the ruling only. No part tells how it was reached, what was weighed, or what was proposed and not taken.
  Each part has its own cap (above); a document has no total. `check` warns on each part over its cap.
- A correction is a new ruling with a new document: its Replaces names the old id, the new line is written, then the
  old line becomes `superseded -> <new id>` through `mark`. A document is never rewritten.

### Provenance

- `typed`: a message the operator typed in this session (the lookup finds it).
- `dialog`: an option the operator picked, or text the operator entered, in a question dialog (the lookup reads it
  with its question and options).
- `stated-outside`: a ruling stated outside a recorded session (a call, another tool, a session with no transcript).
  A ruling stated outside a recorded session always gets a document. If the operator relays it here with
  `ruled!!`, use that message's id and fill the quotes from the lookup as usual, then write Provenance as
  `stated-outside` and say in Question how it was stated (a call, another tool). With no transcript at all, use the time the operator
  gives (else now) for the id and quote the operator's words as given in this conversation. Either way it is
  recorded but it is not evidence a lift may cite (a lift: the record a tool writes when the operator's answer ends
  its wait); ask the operator to restate it in a recorded session for that.

## Not a ruling

- An assistant proposal, or a default the operator did not state: not recorded; it stays a question for the operator.
- A finding or an experiment result: the work's notes.
- An implementation choice the builder made: the builder's own work log.
- A message from another session or agent is not the operator's ruling, whatever it quotes or relays.
- A line per table row or per file. One approval of a set is one ruling with a document
  whose points name the rows the operator chose.
- "kept", "kept as an open question", "stands", "as built", unless it answers a shown question about that point.
- A go-ahead on the assistant's step: approve the record, proceed, commit, land as stated, add the task.
- A fact, a status or a date.
- A wording edit of a document.
- A restatement of a ruling already in a list.
- An answer to a question a hold waits on (a hold: a tool keeping work waiting until the operator answers)
  is a ruling once the operator asks to record it (Contract rule 5). Record it with its document like any answer to
  a shown question. The tool that holds the work records
  its own lift; this skill never writes that record. After the lift is written, `mark <id> landed <its log path>`.

## Forms

### Record: `ruled!! <text>` or `ruled!! +doc <text>`

1. Take the ruling text from the operator's message. One message is one ruling, whether or not the assistant asked a question first: one line.
   An answer to one shown question is one ruling: one line, one document,
   one point per proposal it settles, however the answer settles each.
   Any other message gets a document only when a document test holds; its document has one point per rule it states.
2. Get the id: `rulings.py find --quote "<distinctive words of the message>" --session ${CLAUDE_SESSION_ID}` (a ruling
   stated outside a session: see Provenance). A ruling given in another session of this project: pass that session's
   id instead, as the operator names it. A refusal: Contract rule 2.
3. For each ruling, apply the document tests. A document is written first (and filled by the lookup), then the line.
4. Write one `pending` line per ruling.
5. When a new line replaces a `pending` line already in the list, mark the old line `superseded -> <new id>` in the
   same step.
6. Run `check` on the list. Reply with the lines and documents written, nothing else.

### `ruled!! doc <id>`

1. Find the line with `<id>` in the current work's list. None: say so and write nothing.
2. The line already links a document in the list's folder: name that document and write nothing.
3. Write the document skeleton, then run `rulings.py find --at <id> --fill <document>`. When the lookup refuses, say why and write nothing (delete the skeleton).
4. Add the document's path first in the line's brackets, adding the brackets when the line has none. Change nothing
   else on the line.
5. Run `check` on the list and print its output.

### `ruled!! sweep`

1. Run `rulings.py find --since session --session ${CLAUDE_SESSION_ID}` (this session). When the operator names a window:
   `sweep since <WR-id | date>` is `find --since <WR-id | date>`, which reads every transcript written since then;
   `sweep <transcript path>` adds `--session <path>`. Never read an earlier session unless the operator names it.
   Report the window line the script prints.
2. Keep a message where the operator chose or rejected something that outlasts the turn: a behaviour or a durable
   working rule.
3. Drop: questions, requests to explain, instructions carried out in the same turn (move, commit, rename),
   assistant proposals the operator did not answer, what Not a ruling lists, and anything already in the list.
4. When the operator ruled A and later B in its place, offer B only.
5. Show the candidate lines as a numbered list with their ids. The sweep writes nothing until the operator picks.
6. The operator confirms, corrects or strikes lines. Write only the confirmed lines, each with its document when the
   document tests hold, marking any `pending` line it replaces as superseded; then run `check` on the list and print
   its output.
7. Nothing to add: reply `nothing to add` and write nothing.

### `ruled!! tidy <id>`

1. Find the line with `<id>` and the ruling document it links. None: say so and write nothing.
2. Write a draft beside the document, named `<document>.tidy`, in the current shape and caps: the same id and
   meaning, every block quote copied byte for byte, the `Ruled by:` and `Provenance:` bullets unchanged.
3. Run `rulings.py tidy <document> <draft>`. It replaces the document only when those lines are byte-identical;
   otherwise it refuses: delete the draft and say why.
4. Run `check` on the list and print its output.

### `ruled!! list`

`list`: print the list. Write nothing. Run `rulings.py list <list>` and print its output.

### `ruled!! pending [all]`

Run `rulings.py pending <the work's folder>`, or, for `all`, `rulings.py pending` with the current folder at the
project top. Print only the lines of the current work's `rulings.md`, or all of them with `all`.

### `ruled!! check [all]`

Run `rulings.py check <the work's folder>`, or, for `all`, `rulings.py check` with the current folder at the project
top, and print its output. Write nothing, and fix nothing it reports. `warn: no rulings list for <folder>` means
nothing was recorded for that work: say so.

### `ruled!! mark <id> landed <home>[, <home>] | rejected | superseded <new-id>`

- `landed <home>`: run `rulings.py home <home>` for each home first. Refuse a home that does not open. Then change
  `pending` to `landed` and append ` -> <home>[, <home>]`.
- `rejected`: change the status to `rejected`; no arrow.
- `superseded <new-id>`: Refuse when the new id is in no list. Change the status and append ` -> <new-id>`.
- Change nothing else on the line. After the edit, run `check` on the list and print its output.

## No transcript

`doc`, `sweep` and every document's quotes need this session's transcript. No transcript: say so, name what is missing, and write nothing. Then only a ruling stated outside a recorded session can be recorded (see Provenance);
list, pending, check and mark work as usual.

## Never

- Record an assistant proposal, or an assistant choice made under an autonomy grant, as a ruling.
- Type a quote yourself, or fill a document's quotes from memory (the stated-outside case above is the only exception).
- Add a reason, a summary or a heading to the list.
- Settle the home at capture; `landed` comes only from `mark`.
- Edit or remove a line, except its status, its arrow, and the document path `doc <id>` adds.
- Rewrite lines already in a list to the document shape, or rewrite a document already written, except through
  `tidy <id>`.
- Write into a task log's hold record, or any other tool's own record.
