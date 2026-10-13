---
name: worklog
description: >
  Keeps the work log of a task in a note: after each request of the operator that the assistant acted on, one step is
  added to the note with the request quoted and a compressed result. Forms: on <note>, off, status. The log is
  switched on per session by the typed command and kept by the assistant itself.
  Activates ONLY on "/magic:worklog" (with a form after it) AND NOTHING ELSE.
  NOT for: a request to "keep a log" or "write this down" typed without the command; a call the assistant makes on
  its own; recording decisions or rulings (that is /magic:ruled); meeting notes, changelogs, commit messages;
  editing or summarising an existing note.
---

# worklog - a work log kept in a note

## Contract

- **The switch lives in this conversation.** `on <note>` binds the note until `off`; nothing is stored on disk.
- **While the log is on, every turn that acted on an operator request ends with one new step in the note**, written
  before your reply. Nothing reminds you; the step is yours to remember.
- **The quote is your copy of the operator's message as it stands in your context.** Copy it whole;
  never retell, trim, translate or correct it. Quote only a message you can see word for word;
  never rebuild one from a summary.
- **Change nothing outside the new step.** The operator's own sections and every existing step stay byte for byte,
  except the one link line of rule 7.
- **Say nothing about the log in chat.** Beyond the switch's own one-line answer, no reply mentions the step or the
  note. The one exception is rule 8.
- **These limits bind your own logging.** When the operator asks you to change the note, or asks about the log,
  do as asked.
- **Touch the note only with the file tools** (read, edit; write for a note that does not exist yet).
  Run no shell command for the log; keep no other file for it.
- **When the command is gone from your context, the log is off.** After `/clear`, or when you know of the log only
  from a summary, write no step until the operator types the command again.

## Invocation

- `/magic:worklog on <note>` - switch the log on for this session and name its note.
- `/magic:worklog off` - switch it off.
- `/magic:worklog status` - report the state.

Answer each form with one line, flush-left, and nothing else:

- `on <note>` -> `worklog: on - note <path>`, the path as resolved. A relative path is taken from the working
  directory; a second `on` replaces the note. No note named -> `worklog: no note named - type /magic:worklog on <note>`.
- `off` -> `worklog: off`.
- `status` -> `worklog: on - note <path>`, or `worklog: off`.
- Anything else -> `worklog: unknown form - use on <note>, off or status`.

The command itself is never a request and never gets a step.

## Writing a step

A turn acted on a request when it did work or answered a question; a failed attempt is a result too.
At the end of such a turn:

1. Re-read the note before every write; never assume it ends with the last step. A note that does not exist yet is
   created with the step as its content.
2. Write ONE step for the turn, in this shape:

```
# Step N
=======================================
> the operator's request, exactly as sent

what changed, with the numbers; what was checked and how; what stays unchecked
```

   - `N` is one more than the highest step number among the note's `# Step N` headings; 1 when there is none.
   - The underline is that line of 39 equals signs.
   - The quote: every line of the request prefixed `> `, an empty line as `>`. Keep typos, spacing and every word;
     no cap on length.
   - A request typed as a slash command is quoted as the typed line with its arguments,
     never the text it expanded to.
   - A block the operator pasted arrives between two `<pasted_content ...>` tag lines: quote its lines one level
     deeper (`> > `, an empty line as `> >`) and drop the two tag lines. Nothing else the operator typed is dropped.
   - Several requests under one step (carried ones, and every message the operator sent during the turn)
     are separate quote blocks split by an empty line, oldest first.
   - One empty line, then the body: a compressed result, never a copy of your chat reply. What changed, the
     numbers, what was checked and how, what stays unchecked; `##` sections and tables when the result needs them.
     For a turn that only answered a question, say what was answered; do not restate the answer.
   - Write the step in the note's language; in a new note, in the operator's.
3. Put the step before the note's closing data section: the top-level section that lists links to data files
   (`# Data` is the usual name), whatever follows it. No such section: at the end of the file.
4. Insert the step with an edit that adds text, one empty line before the heading and one after the body;
   never rewrite the whole note.
5. A short reply earns no step when it starts no work (a "no", a one-word clarification, a thanks), and neither
   does a turn that has no result yet (you asked back, the operator interrupted). Write nothing; that message's
   quote opens the next step, above the next request's own quote.
6. Never quoted and never a step, because the operator did not type it: a message from another session,
   a task notification, any text a tool or the harness added to the conversation,
   also inside the operator's message.
7. A data file produced in this turn gets one link line in the closing data section, when the note has one.
8. If the note cannot be written (the edit was denied, the folder is missing), say why in one line, once, and go
   on with your reply; the request's quote opens the next step that can be written.
