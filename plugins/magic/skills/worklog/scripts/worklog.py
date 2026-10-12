#!/usr/bin/env python3
"""Hook script of the worklog skill: the switch, the request queue, the step head and the end-of-turn hold.

It reads one hook JSON object on stdin (event UserPromptSubmit or Stop), acts on it, and always exits 0.
State is kept per session in <root>/<session_id>/state.json, where <root> is $WORKLOG_HOME or ~/.claude/worklog.
At the end of a turn the script itself adds the step head to the note (the heading, its underline and every queued
request as a quote), then holds the turn once with one line that names the step; the assistant writes the body.
The script only ever inserts text into the note; it reads no reply of the assistant. While the log is off it
creates nothing.
"""
import json
import os
import shutil
import sys
import time

LIMIT = 2                      # holds in one turn; the CLI itself ends a turn after more than 8
RETENTION_SECONDS = 7 * 86400
COMMANDS = ("/magic:worklog", "/worklog")
OUR_FILES = {"state.json"}
NOT_OPERATOR = ("<task-notification>", "<cross-session-message ", "[Cross-session ")   # matched at the start only
HEADING = "# Step "
UNDERLINE = "=" * 39
PASTE_OPEN, PASTE_CLOSE = "<pasted_content", "</pasted_content"
HOLD = "worklog: fill the body of Step %d in %s"
UNWRITABLE = "worklog: the note could not be written (%s); %d request(s) kept for the next step"
UNKNOWN = "worklog: unknown form - use on <note>, off or status"
NO_NOTE = "worklog: no note named - type /magic:worklog on <note>"


def root_dir():
    return os.environ.get("WORKLOG_HOME") or os.path.join(os.path.expanduser("~"), ".claude", "worklog")


def safe_id(value):
    """A session id becomes a folder name, so it may hold nothing that could leave the root."""
    if not isinstance(value, str) or not value or value[0] == ".":
        return False
    return all(c.isascii() and (c.isalnum() or c in "._-") for c in value)


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def emit(obj):
    sys.stdout.write(json.dumps(obj) + "\n")


def say(line):
    emit({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": line}})


# -- state ---------------------------------------------------------------------------------------------------------

def load(folder):
    """The state of this session, or None when the log is off. A damaged state means off, never an error."""
    try:
        with open(os.path.join(folder, "state.json"), encoding="utf-8") as fh:
            state = json.load(fh)
    except (OSError, ValueError):
        return None
    if not isinstance(state, dict) or state.get("version") != 1 or not isinstance(state.get("note"), str):
        return None
    requests = state.get("requests")
    if not isinstance(requests, list):
        return None
    for r in requests:
        if not (isinstance(r, dict) and isinstance(r.get("n"), int) and isinstance(r.get("text"), str)
                and isinstance(r.get("at"), str)):
            return None
    state["seq"] = state["seq"] if isinstance(state.get("seq"), int) else max([r["n"] for r in requests] or [0])
    state["holds"] = state["holds"] if isinstance(state.get("holds"), int) else 0
    state["quiet"] = state.get("quiet") is True
    state["open"] = state["open"] if isinstance(state.get("open"), int) else 0
    state["since"] = state["since"] if isinstance(state.get("since"), str) else now()
    return state


def write_private(path, data):
    """Write through a temp file so a reader never sees half a file; mode 0600."""
    tmp = "%s.%d.tmp" % (path, os.getpid())
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def save(folder, state):
    """True when the state is on disk. The caller prints a hold only after a successful save."""
    try:
        root = os.path.dirname(folder)
        if not os.path.isdir(root):
            os.makedirs(root, mode=0o700, exist_ok=True)
            os.chmod(root, 0o700)
        if not os.path.isdir(folder):
            os.mkdir(folder, 0o700)
            os.chmod(folder, 0o700)
        write_private(os.path.join(folder, "state.json"), json.dumps(state, indent=1).encode("ascii"))
        return True
    except OSError:
        return False


def prune(root, keep):
    """Remove session folders left behind by sessions that ended long ago; only folders holding our files alone."""
    try:
        names = os.listdir(root)
    except OSError:
        return
    limit = time.time() - RETENTION_SECONDS
    for name in names:
        path = os.path.join(root, name)
        if name == keep or os.path.islink(path) or not os.path.isdir(path):
            continue
        try:
            if not set(os.listdir(path)) <= OUR_FILES:
                continue
            marker = os.path.join(path, "state.json")
            if os.path.getmtime(marker if os.path.exists(marker) else path) < limit:
                shutil.rmtree(path, ignore_errors=True)
        except OSError:
            continue


# -- UserPromptSubmit: the switch and the queue ----------------------------------------------------------------------

def command_args(prompt):
    """The text after the skill's own command, or None when the prompt is not that command."""
    text = prompt.lstrip()
    for command in COMMANDS:
        if text == command:
            return ""
        if text.startswith(command) and text[len(command)] in " \t\r\n":
            rest = text[len(command):].strip()
            return rest.splitlines()[0].strip() if rest else ""
    return None


def switch(folder, data, args):
    if args == "off":
        if not os.path.isdir(folder):
            return say("worklog: off - it was not on")
        state = load(folder)
        dropped = len(state["requests"]) if state else 0
        shutil.rmtree(folder, ignore_errors=True)
        return say("worklog: off - %d queued request(s) dropped" % dropped)
    if args == "status":
        state = load(folder)
        if state is None:
            return say("worklog: off")
        return say("worklog: on\nnote: %s\nqueued: %d\nsince: %s"
                   % (state["note"], len(state["requests"]), state["since"]))
    if args != "on" and not (args.startswith("on") and args[2] in " \t"):
        return say(UNKNOWN)
    note = args[2:].strip()
    if len(note) >= 2 and note[0] == note[-1] and note[0] in "\"'":
        note = note[1:-1].strip()
    if not note:
        return say(NO_NOTE)
    note = os.path.expanduser(note)
    if not os.path.isabs(note):
        cwd = data.get("cwd")
        note = os.path.join(cwd if isinstance(cwd, str) and os.path.isabs(cwd) else os.getcwd(), note)
    note = os.path.normpath(note)
    if os.path.isdir(note):
        return say("worklog: %s is a folder - name a note file" % note)
    state = load(folder) or {"version": 1, "since": now(), "seq": 0, "holds": 0, "quiet": False, "open": 0,
                             "requests": []}
    if state.get("note") != note:          # a step opened in another note is not this note's open step
        state["open"] = 0
    state["note"], state["quiet"] = note, False
    if not save(folder, state):
        return say("worklog: the state could not be saved under %s" % os.path.dirname(folder))
    prune(os.path.dirname(folder), os.path.basename(folder))
    missing = "" if os.path.exists(note) else " (the note does not exist yet; the first step creates it)"
    return say("worklog: on - note %s%s" % (note, missing))


def on_prompt(folder, data):
    prompt = data.get("prompt")
    if not isinstance(prompt, str) or "agent_id" in data:   # a prompt raised inside a subagent is the model's own
        return
    args = command_args(prompt)
    if args is not None:          # the skill's own command is the switch and is never a request
        return switch(folder, data, args)
    state = load(folder)
    if state is None:
        return
    # not the operator's: the notice a finished background task sends, a message or a notice from another session
    if not prompt or prompt.startswith(NOT_OPERATOR):
        return
    prompt_id = data.get("prompt_id") if isinstance(data.get("prompt_id"), str) else None
    # a message sent while a turn is running arrives with the running turn's prompt id
    same_turn = bool(prompt_id) and state.get("turn_id") == prompt_id
    if same_turn and state.get("last_text") == prompt:
        return                    # the same prompt delivered a second time
    state["turn_id"], state["last_text"] = prompt_id, prompt
    state["seq"] += 1
    state["requests"].append({"n": state["seq"], "at": now(), "text": prompt})
    if not same_turn:             # a new turn has its own holds
        state["holds"] = 0
    if not save(folder, state):
        say("worklog: the state could not be saved under %s" % os.path.dirname(folder))


# -- the note: the step head -------------------------------------------------------------------------------------------

def split_lines(text):
    """The text as a list of (line, line end); the ends are kept, so the pieces add up to the text again."""
    out, start, i = [], 0, 0
    while i < len(text):
        if text[i] in "\r\n":
            end = "\r\n" if text[i:i + 2] == "\r\n" else text[i]
            out.append((text[start:i], end))
            i += len(end)
            start = i
        else:
            i += 1
    if start < len(text):
        out.append((text[start:], ""))
    return out


def paste_tag(line, name):
    """True when the line is one tag of a pasted block and nothing else: the name, then attributes, then `>`."""
    if not (line.startswith(name) and line.endswith(">")):
        return False
    inner = line[len(name):-1]
    return (inner == "" or inner[0] == " ") and "<" not in inner and ">" not in inner


def quote(text):
    """A request as quote lines: `> ` before every line, `>` for an empty one. A pasted block is quoted one level
    deeper and loses its two tag lines; a tag with no partner is quoted as the text it is."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out, i = [], 0
    while i < len(lines):
        end = None
        if paste_tag(lines[i], PASTE_OPEN):
            attrs = lines[i][len(PASTE_OPEN):]
            for j in range(i + 1, len(lines)):
                if lines[j] in (PASTE_CLOSE + attrs, PASTE_CLOSE + ">"):
                    end = j
                    break
        if end is None:
            out.append("> " + lines[i] if lines[i] else ">")
            i += 1
            continue
        out.extend("> > " + line if line else "> >" for line in lines[i + 1:end])
        i = end + 1
    return out


def fence_of(line):
    """(character, length, the rest) when the line opens or closes a fenced code block, else None."""
    text = line.lstrip(" ")
    if len(line) - len(text) > 3 or text[:3] not in ("```", "~~~"):
        return None
    run = len(text) - len(text.lstrip(text[0]))
    return text[0], run, text[run:].strip()


def outline(lines):
    """The top-level headings of a note: a list of (line index, step number or None). A line inside a fenced code
    block or inside the front matter is never a heading."""
    found, fence, i = [], None, 0
    if lines and lines[0] == "---":                    # front matter: up to the next line of three dashes
        closing = [k for k in range(1, len(lines)) if lines[k] in ("---", "...")]
        i = closing[0] + 1 if closing else 0
    for i in range(i, len(lines)):
        line = lines[i]
        mark = fence_of(line)
        if fence:
            if mark and mark[0] == fence[0] and mark[1] >= fence[1] and not mark[2]:
                fence = None
            continue
        if mark:
            fence = mark
            continue
        if not line.startswith("# "):
            continue
        title = line[2:].strip()
        digits = title[len("Step "):] if title.startswith("Step ") else ""
        found.append((i, int(digits) if digits.isascii() and digits.isdigit() and len(digits) <= 9 else None))
    return found


def is_list_of_links(body):
    """True when a section holds at least one line and every line of it is a list item that carries a link."""
    rows = [line.strip() for line in body if line.strip()]
    return bool(rows) and all(r[:2] in ("- ", "* ", "+ ") and ("](" in r or "[[" in r or "://" in r) for r in rows)


def plan(text, requests, opened):
    """Where the quotes go and what is inserted there: (offset in the text, the insertion, the step's number).

    A step this script opened whose body is still empty takes the quotes under its heading. Otherwise a new step is
    numbered after the highest one and placed before the closing data section: the first top-level section after
    the last step, or, in a note without steps, a last top-level section that is titled Data or is a list of links.
    Without one the step goes to the end of the note.
    """
    nl = "\r\n" if "\r\n" in text else "\n"
    pieces = split_lines(text[1:] if text.startswith("\ufeff") else text)
    shift = 1 if text.startswith("\ufeff") else 0
    lines = [line for line, _ in pieces]
    starts, pos = [], shift                 # the offset of every line, and of the end of the text
    for line, end in pieces:
        starts.append(pos)
        pos += len(line) + len(end)
    starts.append(pos)
    heads = outline(lines)
    blocks = (nl + nl).join(nl.join(quote(r["text"])) for r in requests)
    ragged = bool(pieces) and pieces[-1][1] == ""      # the text does not end with a line end

    at = [k for k, (_, number) in enumerate(heads) if opened and number == opened]
    if at:
        first = heads[at[-1]][0] + 1
        last = heads[at[-1] + 1][0] if at[-1] + 1 < len(heads) else len(lines)
        if first < last and lines[first].strip() and not lines[first].strip().strip("="):
            first += 1                      # the underline
        body = lines[first:last]
        if all(not line.strip() or line.startswith(">") for line in body):
            quoted = [k for k, line in enumerate(body) if line.startswith(">")]
            after = first + (quoted[-1] + 1 if quoted else 0)
            lead = (nl if ragged and after == len(lines) else "") + (nl if quoted else "")
            tail = nl if after == len(lines) or lines[after].strip() else ""
            return starts[after], lead + blocks + nl + tail, opened

    steps = [k for k, (_, number) in enumerate(heads) if number is not None]
    number = max([heads[k][1] for k in steps] or [0]) + 1
    target = len(lines)
    if steps and steps[-1] + 1 < len(heads):
        target = heads[steps[-1] + 1][0]
    elif not steps and heads:
        index = heads[-1][0]
        if lines[index][2:].strip().lower() == "data" or is_list_of_links(lines[index + 1:]):
            target = index
    lead = nl if ragged and target == len(lines) else ""
    if target and lines[target - 1].strip():
        lead += nl                          # an empty line between the text above and the heading
    return starts[target], lead + HEADING + str(number) + nl + UNDERLINE + nl + blocks + nl + nl, number


def write_step(state):
    """Insert the step head into the note. Returns (the step's number, None) or (None, why it could not be done)."""
    path = state["note"]
    try:
        exists = os.path.lexists(path)
        if exists and not os.path.isfile(path):
            return None, "it is not a file"
        if not exists and not os.path.isdir(os.path.dirname(path)):
            return None, "its folder does not exist"
        with open(path, "r+b" if exists else "x+b") as fh:
            try:
                text = fh.read().decode("utf-8")
            except UnicodeDecodeError:
                return None, "it is not UTF-8 text"
            where, insertion, number = plan(text, state["requests"], state["open"])
            fh.seek(len(text[:where].encode("utf-8")))
            fh.write((insertion + text[where:]).encode("utf-8"))
        return number, None
    except OSError as err:
        return None, (err.strerror or "it could not be opened").lower()


# -- Stop: the step head and the hold ----------------------------------------------------------------------------------

def running(data):
    """True while a background task of this session is still at work."""
    background = data.get("background_tasks")
    return isinstance(background, list) and bool(background)


def on_stop(folder, data):
    state = load(folder)
    if state is None or "agent_id" in data or not state["requests"]:
        return
    if running(data):             # the result is not in yet; the requests wait for it
        return
    if data.get("stop_hook_active") is True:          # a hold already ran in this turn, ours or another hook's
        state["holds"] = max(state["holds"], 1)
    if not save(folder, state):   # a state that cannot be saved would quote the same requests again
        return
    number, why = write_step(state)
    if number is None:
        said = state["quiet"]
        state["quiet"] = True
        if save(folder, state) and not said:
            emit({"systemMessage": UNWRITABLE % (why, len(state["requests"]))})
        return
    state["requests"], state["open"], state["quiet"] = [], number, False
    hold = state["holds"] < LIMIT
    if hold:
        state["holds"] += 1
    if save(folder, state) and hold:
        emit({"decision": "block", "reason": HOLD % (number, state["note"])})


def main():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return
    if not isinstance(data, dict) or not safe_id(data.get("session_id")):
        return
    folder = os.path.join(root_dir(), data["session_id"])
    if os.path.islink(folder):    # a session folder is always a real folder of ours
        return
    event = data.get("hook_event_name")
    if event == "UserPromptSubmit":
        on_prompt(folder, data)
    elif event == "Stop":
        on_stop(folder, data)


if __name__ == "__main__":
    try:
        main()
    except Exception:             # a hook that crashes must not break the operator's turn
        pass
    sys.exit(0)
