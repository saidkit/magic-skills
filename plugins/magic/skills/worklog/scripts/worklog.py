#!/usr/bin/env python3
"""Hook script of the worklog skill: the switch, the request queue and the end-of-turn reminder.

It reads one hook JSON object on stdin (event UserPromptSubmit or Stop), acts on it, and always exits 0.
State is kept per session in <root>/<session_id>/, where <root> is $WORKLOG_HOME or ~/.claude/worklog:
  state.json    the script's own record
  requests.txt  the queued requests, exactly as sent, for the assistant to read
The script never opens the note. While the log is off it creates nothing.
"""
import json
import os
import shutil
import sys
import time

LIMIT = 2                      # holds in one turn; the CLI itself ends a turn after more than 8
RETENTION_SECONDS = 7 * 86400
COMMANDS = ("/magic:worklog", "/worklog")
OUR_FILES = {"state.json", "requests.txt"}
WORDS = ("written", "carried", "failed")
RULE = "-----8<-----"
REASON = ("worklog: %d request(s) from the operator are not in the work log yet. Read %s (it names the note "
          "and holds each request exactly as sent), then follow the worklog skill's step rules: write the step into "
          "that note, copying each quote from the file. End your reply with one of these lines on its own: "
          "`worklog: written` once the step is in the note; `worklog: carried` if every request is a short reply "
          "that earns no step yet; `worklog: failed - <why>` if the note could not be written.")
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
                and isinstance(r.get("at"), str) and isinstance(r.get("carried"), bool)):
            return None
    state["seq"] = state["seq"] if isinstance(state.get("seq"), int) else max([r["n"] for r in requests] or [0])
    state["holds"] = state["holds"] if isinstance(state.get("holds"), int) else 0
    state["awaiting"] = state.get("awaiting") is True
    state["quiet"] = state.get("quiet") is True
    state["since"] = state["since"] if isinstance(state.get("since"), str) else now()
    return state


def requests_text(state):
    parts = ["worklog requests\nnote: %s\ncount: %d\n" % (state["note"], len(state["requests"]))]
    for r in state["requests"]:
        mark = ", carried" if r["carried"] else ""
        parts.append("\n%s request %d (%s%s) %s\n%s\n%s end of request %d %s\n"
                     % (RULE, r["n"], r["at"], mark, RULE, r["text"], RULE, r["n"], RULE))
    return "".join(parts)


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
        listing = os.path.join(folder, "requests.txt")
        if state["requests"]:
            write_private(listing, requests_text(state).encode("utf-8", "replace"))
        elif os.path.exists(listing):
            os.unlink(listing)
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
        carried = sum(1 for r in state["requests"] if r["carried"])
        return say("worklog: on\nnote: %s\nqueued: %d (%d carried)\nsince: %s"
                   % (state["note"], len(state["requests"]), carried, state["since"]))
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
    state = load(folder) or {"version": 1, "since": now(), "seq": 0, "holds": 0, "awaiting": False,
                             "quiet": False, "requests": []}
    state["note"] = note
    if not save(folder, state):
        return say("worklog: the state could not be saved under %s" % os.path.dirname(folder))
    prune(os.path.dirname(folder), os.path.basename(folder))
    missing = "" if os.path.exists(note) else " (the note does not exist yet; the first step creates it)"
    return say("worklog: on - note %s%s" % (note, missing))


def on_prompt(folder, data):
    prompt = data.get("prompt")
    if not isinstance(prompt, str):
        return
    args = command_args(prompt)
    if args is not None:          # the skill's own command is the switch and is never a request
        return switch(folder, data, args)
    state = load(folder)
    if state is None:
        return
    # not the operator's: a prompt raised inside a subagent, and the notice a finished background task sends
    if "agent_id" in data or prompt.startswith("<task-notification>") or not prompt:
        return
    prompt_id = data.get("prompt_id")
    if isinstance(prompt_id, str) and prompt_id and state.get("last_id") == prompt_id:
        return                    # the same prompt delivered a second time
    state["last_id"] = prompt_id if isinstance(prompt_id, str) else None
    state["seq"] += 1
    state["requests"].append({"n": state["seq"], "at": now(), "text": prompt, "carried": False})
    state["holds"], state["awaiting"], state["quiet"] = 0, False, False   # a new request starts a new turn
    if not save(folder, state):
        say("worklog: the state could not be saved under %s" % os.path.dirname(folder))


# -- Stop: the reminder ------------------------------------------------------------------------------------------------

def closing_word(message):
    """The word of the assistant's closing line (`worklog: written` and so on), or None."""
    if not isinstance(message, str):
        return None
    for line in reversed(message.splitlines()):
        text = line.strip(" \t`*").lower()
        if not text.startswith("worklog:"):
            continue
        rest = text[len("worklog:"):].lstrip(" \t")
        for word in WORDS:
            if rest.startswith(word) and (rest[len(word):] == "" or rest[len(word)] in " \t.,:!-"):
                return word
    return None


def running(data):
    """True while a background task of this session is still at work."""
    background = data.get("background_tasks")
    return isinstance(background, list) and bool(background)


def hold(folder, state):
    state["holds"] += 1
    state["awaiting"] = True
    if save(folder, state):       # an unsaved hold could repeat forever, so it is never printed
        emit({"decision": "block",
              "reason": REASON % (len(state["requests"]), os.path.join(folder, "requests.txt"))})


def on_stop(folder, data):
    state = load(folder)
    if state is None or "agent_id" in data:
        return
    if state["awaiting"]:
        word = closing_word(data.get("last_assistant_message"))
        if word == "written":
            state["requests"] = []
        elif word == "carried":
            for r in state["requests"]:
                r["carried"] = True
        elif word is None and running(data):
            return                # still waiting for the closing line; no reminder while a task runs
        elif word is None and state["holds"] < LIMIT:
            return hold(folder, state)
        state["awaiting"] = False
        if word in ("written", "carried"):
            state["holds"] = 0
        else:                     # failed, or the limit was reached: release, keep the requests, stay quiet
            state["quiet"] = True
        saved = save(folder, state)
        if word is None and saved:
            emit({"systemMessage": "worklog: the step was not written after %d reminders; %d request(s) kept "
                                   "for the next step" % (LIMIT, len(state["requests"]))})
        return
    if state["quiet"] or all(r["carried"] for r in state["requests"]):
        return
    if running(data):             # the result is not in yet; the requests wait for it
        return
    if data.get("stop_hook_active") is True:          # another hook already forced this turn to continue
        state["holds"] = max(state["holds"], 1)
    if state["holds"] >= LIMIT:
        return
    hold(folder, state)


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
