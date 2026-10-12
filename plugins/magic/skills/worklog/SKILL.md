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

The operator switches the log on for a session; this skill's hooks queue every request and, at the end of a turn, ask
you to write one step into the note.

## Contract

- **The hook has already applied the switch.** For `on`, `off` and `status` print its result line and do nothing
  else: no shell command, no file edit, no state of your own.
- **Write a step only when the hook's message asks for it.** It starts
  `worklog: N request(s) from the operator are not in the work log yet. Note: <path>` and carries the requests. No
  such message, no step; a request that is not in that message gets no step.
- **The quote comes only from the hook's message.** Copy it; never type it from memory; never retell, trim or
  correct it.
- **Change nothing outside the new step.** The operator's own sections and every existing step stay byte for byte,
  except the one link line of step 7.
- **End every reply to that message with exactly one closing line**, spelled as in "The closing line"; the hook
  matches it. An ordinary reply never ends with a closing line, and neither does the reply to the switch command.
- **Never read, edit or delete anything under `~/.claude/worklog/`**; it is the hook's own state. Never run a shell
  command for the queue.

## Invocation

- `/magic:worklog on <note>` - switch the log on for this session and name its note.
- `/magic:worklog off` - switch it off.
- `/magic:worklog status` - report the state.

For each form:

1. Print the `worklog:` result line the hook added to your context, word for word and flush-left. For `status`
   while on the result is four lines (one per line, no table, no padding);
   while off it is the one line `worklog: off`. Print exactly what the hook gave, nothing more.
2. If no `worklog:` line was added to your context, say that the switch could not be confirmed and ask the operator
   to type `/magic:worklog status`.
3. After a successful `on` (the result starts `worklog: on - note`), tell the operator once: the first edit of the
   note asks for permission (answering "always allow" covers the session), and after `/clear` the command has to be
   typed again. A refused `on` gets its result line only.

## Writing a step

When the hook's message arrives:

1. Take the note's path from the message's first line (`Note: <path>`) and the requests from its body: each request
   sits between its delimiter lines, exactly as sent; one marked `carried` was sent in an earlier turn.
2. Re-read the note before every write; never assume it ends with the last step.
3. A short reply that earns no step (a "no", a one-word clarification, a thanks) is carried: when every request in
   the message is one, write nothing and close with `worklog: carried`. Its quote opens the next step.
4. Otherwise write ONE step for ALL requests in the message, short replies included; never drop one. A request that is
   already quoted in an existing step is not quoted again; when every request is, write nothing and close with
   `worklog: written`. The shape:

```
# Step N
=======================================
> the operator's request, exactly as sent

what changed, with the numbers; what was checked and how; what stays unchecked
```

   - `N` is one more than the highest step number in the note; 1 when the note has no step.
   - The underline is that line of 39 equals signs.
   - Copy each request from the hook's message, every line prefixed `> `, an empty line as `>`. Several requests are
     separate quote blocks split by a blank line, in the message's order (carried ones come first). Keep typos,
     spacing and every word; no cap on length. The delimiter lines are not part of a request.
   - The body is a compressed result, never a copy of your chat reply: what changed, the numbers, what was checked
     and how, what stays unchecked.
   - Write the step in the note's language.
5. Put the step before the note's closing data section: the top-level section after the steps that lists links to
   data files (`# Data` is the usual name). When the note has no such section, put it at the end of the file. A note
   that does not exist yet is created with the step as its content.
6. Insert the step with an edit that adds text; never rewrite the whole note.
7. A data file produced in this turn gets one link line in the closing data section, when the note has one.

## The closing line

Only in a reply to the hook's message; the last line of that reply, on its own:

- `worklog: written` - every request of the message is quoted in the note: the step was just written and the edit
  succeeded, or all of them were already there.
- `worklog: carried` - every request was a short reply; nothing was written.
- `worklog: failed - <why>` - the note could not be written (a denied edit, a missing folder).
