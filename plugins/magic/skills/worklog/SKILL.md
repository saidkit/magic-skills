---
name: worklog
description: >
  Keeps the work log of a task in a note: after each significant request of the operator, one step is added to the
  note with the request quoted word for word and a compressed result. Forms: on <note>, off, status. The log is
  switched on per session; the skill's own hooks quote the requests into the note and ask for the result at the end
  of a turn.
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

## Contract

- **The hook has already applied the switch.** For `on`, `off` and `status` print its result line and do nothing
  else: no shell command, no file edit, no state of your own.
- **The hook writes the step's head; you write its body.** At the end of a turn the hook itself adds the heading, the
  underline and every request as a quote to the note, then asks with one line:
  `worklog: fill the body of Step N in <note>`. Write a body only when that line asks for it.
- **Never edit the heading, the underline or the quotes.** Never add a quote, a heading or a step of your own.
- **Change nothing outside the body of that step.** The operator's own sections and every other step stay byte for
  byte, except the one link line of step 5.
- **Say nothing about the log in chat.** Beyond the switch's own result (Invocation), no reply mentions the step,
  the note or the hook's line; after the edit of a body, end the turn without further text. The one exception is
  step 6.
- **Never read, edit or delete anything under `~/.claude/worklog/`.** Never run a shell command for the log.

## Invocation

- `/magic:worklog on <note>` - switch the log on for this session and name its note.
- `/magic:worklog off` - switch it off.
- `/magic:worklog status` - report the state.

For each form:

1. Print the `worklog:` result line the hook added to your context, word for word and flush-left: for `status`
   while on, four lines (one per line, no table, no padding); while off, the one line `worklog: off`. Nothing more.
2. If no `worklog:` line was added to your context, say that the switch could not be confirmed and ask the operator
   to type `/magic:worklog status`.
3. After a successful `on` (the result starts `worklog: on - note`), tell the operator once: the first edit of the
   note asks for permission (answering "always allow" covers the session), and after `/clear` the command has to be
   typed again. A refused `on` gets its result line only.

## Writing the body

When the hook's line arrives:

1. Take the step's number and the note's path from the line.
2. Re-read the note before every write and find that step. The hook wrote this much of it:

```
# Step N
=======================================
> the operator's request, exactly as sent

```

3. Add the body below the step's last quote, with an edit that adds text; never rewrite the whole note. The hook
   left one empty line after the last quote: the body starts on the line after it and ends with one empty line.
   - The body is a compressed result, never a copy of your chat reply: what changed, the numbers, what was checked
     and how, what stays unchecked. A few lines. For a turn that only answered a question, say what was answered;
     do not restate the answer.
   - One body covers every quote under the step.
   - Write the body in the note's language.
4. When every quote under the step is a short reply that earns no body yet (a "no", a one-word clarification, a
   thanks), leave the body empty and make no edit. The hook puts the next request's quote under the same step, and
   the body is written then.
5. A data file produced in this turn gets one link line in the note's closing data section, when the note has one.
6. If the edit cannot be made (it was denied, the step is not in the note), say why in one line and do not retry.
