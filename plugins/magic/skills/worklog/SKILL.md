---
name: worklog
description: >
  Keeps the work log of a task in a note: after each significant request of the operator, one step is added to the
  note with the request quoted word for word and a compressed result. Forms: on <note>, off, status. The log is
  switched on per session; the skill's own hooks queue the requests and remind at the end of a turn.
  Activates ONLY on "/magic:worklog" (with a form after it) AND NOTHING ELSE.
  NOT for: a request to "keep a log" or "write this down" typed without the command; a call the assistant makes on
  its own; recording decisions or rulings (that is /magic:ruled); meeting notes, changelogs, commit messages;
  editing or summarising an existing note.
hooks:
  UserPromptSubmit:
    - hooks:
        - type: command
          command: python3 "${CLAUDE_PLUGIN_ROOT}/skills/worklog/scripts/worklog.py"
  Stop:
    - hooks:
        - type: command
          command: python3 "${CLAUDE_PLUGIN_ROOT}/skills/worklog/scripts/worklog.py"
---

# worklog - a work log kept in a note

The operator switches the log on for a session with `/magic:worklog on <note>`. From then on every request is queued
by this skill's hook, and at the end of a turn the hook asks you to write one step into the note.

## Contract

- **The hook has already applied the switch.** For `on`, `off` and `status` you print its result line and do nothing
  else: no command, no file edit, no state of your own.
- **Write a step only when the hook's message asks for it.** The message starts
  `worklog: N request(s) from the operator are not in the work log yet. Read <path>`. No such message, no step.
- **The quote comes only from the requests file.** Copy it; never type it from memory, never retell it.
- **Change nothing outside the new step.** The note is the operator's; they edit it while you work.
- **End every reply to that message with exactly one closing line** (see "The closing line"). The hook reads it.
- **Never edit `state.json` or `requests.txt`.** They belong to the hook.

## The switch

`/magic:worklog on <note>` switches the log on and names its note; `off` switches it off; `status` reports.

1. Print the `worklog:` result line the hook added to your context, word for word and flush-left. For `status` the
   result is four lines; print all four, one per line, no table, no padding.
2. If no `worklog:` line was added to your context, read `~/.claude/worklog/${CLAUDE_SESSION_ID}/state.json` and
   report from it (a missing file means the log is off). Say that the switch could not be confirmed.
3. After `on`, tell the operator once: the first edit of the note asks for permission (answering "always allow" covers
   the session), and after `/clear` the command has to be typed again.

## Writing a step

When the hook's message arrives:

1. Read the requests file it names. The file names the note and holds each request between delimiter lines.
2. Re-read the note before every write. The operator may have added sections or moved text; never assume the note
   ends with the last step.
3. A short reply that earns no step (a "no", a one-word clarification, a thanks) is carried: when every request in
   the file is one, write nothing and close with `worklog: carried`. Its quote opens the next step.
4. Otherwise write ONE step for all requests in the file, in this shape:

```
# Step N
=======================================
> the operator's request, exactly as sent

what changed, with the numbers; what was checked and how; what stays unchecked
```

   - `N` is one more than the highest step number in the note; 1 when the note has no step.
   - The underline is that line of 39 equals signs.
   - Copy each request from the requests file, every line prefixed `> `, an empty line as `>`. Several requests are
     separate quote blocks split by a blank line, in the file's order (carried ones come first). Keep typos, spacing
     and every word; no cap on length.
   - The body is a compressed result, never a copy of your chat reply: what changed, the numbers, what was checked
     and how, what stays unchecked.
   - Write the step in the note's language.
5. Put the step before the note's closing data section: the top-level section after the steps that lists links to
   data files (`# Data` is the usual name). When the note has no such section, put it at the end of the file. A note
   that does not exist yet is created with the step as its content.
6. Change nothing outside the new step. The operator's own sections and every existing step stay byte for byte: use
   an edit that inserts, never a rewrite of the whole note.
7. A data file produced in this turn gets one link line in the closing data section, when the note has one.

## The closing line

The last line of your reply, on its own:

- `worklog: written` - the step is in the note.
- `worklog: carried` - every request was a short reply; nothing was written.
- `worklog: failed - <why>` - the note could not be written (a denied edit, a missing folder).

Without a closing line the hook reminds once more and then releases the turn; the requests are kept and join the
next step. Say `worklog: written` only after the edit succeeded.

## Never

- Retell, trim or correct a quote.
- Write a step that the hook's message did not ask for, or for a request that is not in the requests file.
- Touch the operator's sections or an existing step.
- Run a shell command for the switch or the queue.
- Clear, edit or delete anything under `~/.claude/worklog/`.
- Claim `worklog: written` when the edit did not happen.
