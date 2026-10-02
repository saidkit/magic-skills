#!/usr/bin/env python3
"""Rulings lists: print them, check them, and find the operator's words in a session transcript.

  rulings.py list <list|folder>        print every entry line of one list, with file and line
  rulings.py pending [<list|folder>]   print every `pending` line, with file and line
  rulings.py check [<list|folder>]     check entry lines, links and arrows; ends with one result line
  rulings.py home <home>               exit 0 when a home opens, 1 when it does not
  rulings.py find ...                  read a session transcript (see `find --help`)

Options for every command: --root <dir>. Paths written in a list resolve from the root, else from the list's
own folder. The root defaults to the git root of the current folder, else the current folder; no git is needed.
With no target, `pending` and `check` read the lists under the current folder. Symbolic links are not followed
while walking; a named target is read wherever it points. A folder holding `.rulings-ignore` is skipped, with
everything under it, and each skipped folder is printed; a path named on the command line is still read.

A list is a file named `rulings.md` whose first line starting with `- ` is an entry; a title and a format line
may come before it. One entry per line:

  - WR-<unix-seconds>[-n] - <who>, <status>: <ruling> [<evidence>]

and, once marked, ` -> <home>[, <home>]` on `landed` or ` -> <WR-id>` on `superseded`. A bracket that ends the
ruling is its evidence: every item is a path (an optional `:12`, `:12-18` or `:12 to :18`, an optional `#anchor`;
a backticked path may carry a label) and every path must open. A bracket inside the text is text. An entry the
grammar does not read (a broken id, no status, an arrow not written ` -> `, an evidence item that is not a path,
or a bulleted line that starts like an entry) is MALFORMED and fails the check.
"""
import argparse
import json
import os
import subprocess
import tempfile
import sys

LIST_NAME = "rulings.md"
IGNORE_MARK = ".rulings-ignore"
STATUSES = ("pending", "landed", "rejected", "superseded")
TEXT_LIMIT = 160
TITLE_LIMIT = 50
POINT_LIMIT = 100
SECTION_WORDS = (("If it turns out wrong", 12), ("Not settled", 10))
QUESTION_WORDS = 12
DOC_PARTS = ("The question", "The operator's ask", "The operator's message", "The ruling", "Evidence",
             "If it turns out wrong", "Not settled")
ROLE_WORDS = ("operator", "pm", "assistant", "user")  # <who> names a person; these name a role
DOC_TAG = "-ruling-"


class Malformed(Exception):
    pass


# --- root and discovery ---------------------------------------------------------------------------------

def root_dir(explicit):
    if explicit:
        return os.path.realpath(explicit)
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            return os.path.realpath(r.stdout.strip())
    except OSError:
        pass
    return os.path.realpath(os.getcwd())


def read_lines(path):
    try:
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            return [ln[:-1] if ln.endswith("\r") else ln for ln in f.read().split("\n")]
    except OSError:
        return None


def entry_like(line):
    """A bulleted line that reads as an attempted entry: `-` then, after spaces, `WR` in any case."""
    if not line.startswith("-"):
        return False
    rest = line[1:].lstrip(" \t")
    return rest[:2].upper() == "WR"


def is_list(path):
    if os.path.basename(path) != LIST_NAME:
        return False
    lines = read_lines(path)
    if not lines:
        return False
    for ln in lines:
        if ln.startswith("-"):
            return entry_like(ln)
    return False


def walk(top, honour_top_marker):
    """Lists under top and the folders skipped by a marker. Symbolic links are not followed."""
    lists, skipped = [], []
    for d, dirs, files in os.walk(top):
        dirs[:] = sorted(x for x in dirs if x != ".git")
        if IGNORE_MARK in files and (honour_top_marker or d != top):
            skipped.append(d)
            dirs[:] = []
            continue
        if LIST_NAME in files:
            p = os.path.join(d, LIST_NAME)
            if not os.path.islink(p) and is_list(p):
                lists.append(p)
    return lists, skipped


def select(target):
    """(lists, skipped) for a named target or, with none, the current folder's tree."""
    if target is None:
        return walk(os.getcwd(), True)
    if os.path.isdir(target):
        return walk(target, False)
    if os.path.isfile(target):
        return ([target] if is_list(target) else []), []
    return [], []


def shown(path):
    """A path as printed: relative to the current folder when below it."""
    cwd = os.path.realpath(os.getcwd())
    real = os.path.realpath(path) if os.path.exists(path) else path
    for base, p in ((cwd, real), (os.path.abspath(os.getcwd()), os.path.abspath(path))):
        if p == base:
            return "."
        if p.startswith(base + os.sep):
            return p[len(base) + 1:]
    return path


# --- the line grammar -----------------------------------------------------------------------------------

def parse_id(s):
    """`WR-<10 digits>[-<digits>]` at the start of s -> (id, rest), else None."""
    if not s.startswith("WR-") or len(s) < 13 or not (s[3:13].isascii() and s[3:13].isdigit()):
        return None
    j = 13
    if s[j:j + 1] == "-" and s[j + 1:j + 2].isdigit() and s[j + 1:j + 2].isascii():
        k = j + 1
        while k < len(s) and s[k].isascii() and s[k].isdigit():
            k += 1
        j = k
    if j < len(s) and s[j] not in " \t":
        return None
    return s[:j], s[j:]


def strip_lines(item):
    """Drop a line suffix: `:12`, `:12-18`, `:12 to :18`."""
    for sep in (" to :", " to "):
        k = item.find(sep)
        if k >= 0 and item[k + len(sep):].strip().isdigit():
            item = item[:k]
            break
    i = item.rfind(":")
    if i > 0:
        tail = item[i + 1:]
        parts = tail.split("-", 1)
        if all(p.isdigit() for p in parts):
            item = item[:i]
    return item.strip()


def path_of(item):
    """The path an evidence item or home names (line suffix and `#anchor` dropped), or None when the item is broken:
    empty, an unclosed backtick, or only dots and slashes."""
    item = item.strip()
    if item.startswith("`"):
        k = item.find("`", 1)
        if k <= 1:
            return None
        item = item[1:k]
    elif "`" in item:
        return None
    p = strip_lines(item).split("#", 1)[0].strip()
    if not p or not p.strip("./") or p.startswith("-"):
        return None
    return p


def final_bracket(text):
    """(text without it, [paths]) when the text ends in a bracket; (text, []) when it does not.
    The final bracket is the evidence: every item must be a path, else the entry is MALFORMED."""
    t = text.rstrip()
    if not t.endswith("]"):
        return text, []
    depth, k = 0, len(t) - 1
    while k >= 0:
        if t[k] == "]":
            depth += 1
        elif t[k] == "[":
            depth -= 1
            if depth == 0:
                break
        k -= 1
    if k < 0:
        raise Malformed("the final ']' has no '['")
    inner = t[k + 1:-1]
    if "[" in inner or "]" in inner:
        raise Malformed("a bracket inside the evidence bracket")
    items = inner.replace(";", ",").split(",")
    paths = []
    for x in items:
        p = path_of(x)
        if p is None:
            raise Malformed("the evidence item '%s' is not a path" % x.strip())
        paths.append(p)
    return t[:k].rstrip(), paths


def home_path(home):
    """The file a home names: a path with an optional `#anchor` or a section mark (U+00A7) and a section."""
    h = home.strip()
    k = h.find(" \u00a7")
    if k >= 0:
        h = h[:k]
    return path_of(h)


def parse_entry(line):
    """A list line -> dict for an entry, None for a non-entry line; raise Malformed for a broken entry."""
    if not line.startswith("- WR-"):
        if entry_like(line):
            raise Malformed("an entry starts with '- WR-'")
        return None
    body = line[2:].rstrip()
    p = parse_id(body)
    if not p:
        raise Malformed("the id is not WR-<10 digits>[-n]")
    rid, rest = p
    if not rest.startswith(" - "):
        raise Malformed("no ' - ' after the id")
    rest = rest[3:]
    cut = None
    for st in STATUSES:
        k = rest.find(", " + st + ": ")
        if k > 0 and (cut is None or k < cut[0]):
            cut = (k, st)
    if cut is None:
        raise Malformed("no ', <status>: ' with a status of " + ", ".join(STATUSES))
    who = rest[:cut[0]].strip()
    status = cut[1]
    text = rest[cut[0] + len(status) + 4:]
    if not who:
        raise Malformed("no who")
    arrow = None
    if status in ("landed", "superseded"):
        k = text.rfind(" -> ")
        if k >= 0:
            arrow, text = text[k + 4:].strip(), text[:k]
        elif any(a in text for a in ("->", "=>", "\u2192")):
            raise Malformed("a mark's arrow is written ' -> '")
    text, links = final_bracket(text)
    if not text.strip():
        raise Malformed("no ruling text")
    return {"id": rid, "who": who, "status": status, "text": text.strip(), "arrow": arrow, "links": links}


def rows(lists):
    """(list, n, line, entry | None | Malformed) for every entry-shaped or bulleted line after the first entry."""
    out = []
    for p in lists:
        started = False
        for n, ln in enumerate(read_lines(p) or [], 1):
            if not started:
                if not ln.startswith("-"):
                    continue
                started = True
            if not ln.strip():
                continue
            try:
                out.append((p, n, ln, parse_entry(ln)))
            except Malformed as e:
                out.append((p, n, ln, e))
    return out


def bases(root, list_path):
    """Where a path written in a list resolves from: the root, then the list's own folder. Nothing above."""
    return [root, os.path.dirname(os.path.abspath(list_path))]


def inside(root, full):
    """True when a path, normalised without following symlinks, lies under the root."""
    r, f = os.path.normpath(os.path.abspath(root)), os.path.normpath(os.path.abspath(full))
    return f == r or f.startswith(r.rstrip(os.sep) + os.sep)


def resolve(root, list_path, path):
    """The normalised path a written path opens, from the root or the list's folder, else None. Confinement and
    existence are judged on the same normalised path; an absolute path, or one that leaves the root, never opens."""
    if os.path.isabs(path):
        return None
    own = os.path.dirname(os.path.abspath(list_path))
    for b in bases(root, list_path):
        n = os.path.normpath(os.path.abspath(os.path.join(b, path)))
        if (inside(root, n) or inside(own, n)) and os.path.exists(n):
            return n
    return None


def opens(root, list_path, path):
    return resolve(root, list_path, path) is not None


def in_folder(root, list_path, link):
    folder = os.path.realpath(os.path.dirname(list_path))
    for base in bases(root, list_path):
        full = os.path.join(base, link)
        if os.path.exists(full):
            return os.path.dirname(os.path.realpath(full)) == folder
    return False


UNASKED = "Stated by the operator, unasked."
ASK_PART = "The operator's ask"  # the operator asked, the assistant proposed, the operator ruled
ATTRIBUTION_PARTS = ("The question", ASK_PART, "The operator's message")
# Rulings recorded before 2026-10-02 (UTC) predate the rule that a document's two attribution parts hold only quotes;
# their documents are never rewritten, so text outside those quotes only warns. Later rulings FAIL on it.
ATTRIBUTION_FROM = 1790899200


def heading2(ln):
    """The text of a level-2 heading as markdown renders it (up to three leading spaces, closing hashes), else None."""
    s = ln[len(ln) - len(ln.lstrip(" ")):] if len(ln) - len(ln.lstrip(" ")) <= 3 else None
    if s is None or not s.startswith("##") or s.startswith("###") or s[2:3] not in (" ", "\t"):
        return None
    return s[3:].strip().rstrip("#").strip()


def attribution_errors(path):
    """Text written outside the block quotes of the two attribution parts (the unasked line excepted), or a part
    missing."""
    out, cur, seen, quoted = [], None, set(), set()
    for ln in read_lines(path) or []:
        h = heading2(ln)
        if h is not None:
            cur = h
            seen.add(h)
            continue
        s = ln.strip()
        if cur in ATTRIBUTION_PARTS and ln.lstrip(" \t").startswith(">"):
            quoted.add(cur)
            continue
        if not s or cur not in ATTRIBUTION_PARTS:
            continue
        if cur == "The question" and s == UNASKED:
            quoted.add(cur)
            continue
        out.append("%s holds text outside a quote: %s" % (cur, s[:60]))
    if "The operator's message" not in seen:
        out.append("The operator's message is missing")
    if "The question" not in seen and ASK_PART not in seen:
        out.append("The question (or The operator's ask) is missing")
    for part in sorted(seen & set(ATTRIBUTION_PARTS) - quoted):
        out.append("%s has no quote" % part)
    return out


def id_seconds(rid):
    """The unix seconds of a ruling id (WR-<seconds>[-n])."""
    return int(rid[3:].split("-", 1)[0])


def unfilled(path):
    """The first fill placeholder left outside the block quotes of a document, else None."""
    for ln in read_lines(path) or []:
        if ln.lstrip().startswith(">"):
            continue
        for ph in PLACEHOLDERS:
            if ph in ln:
                return ph
    return None


def sections(lines):
    """{heading text: [lines]} for the `## ` sections of a ruling document."""
    out, cur = {}, None
    for ln in lines:
        if ln.startswith("## "):
            cur = ln[3:].strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(ln)
    return out


def outside_code(text):
    """text with its `code spans` removed."""
    parts = text.split("`")
    return "".join(parts[0::2])


def is_path_token(tok):
    tok = tok.strip().strip("`").strip()
    return bool(tok) and not any(c.isspace() for c in tok)


def terse_warnings(path):
    """Warnings for the parts of a ruling document the assistant writes: title, points, Evidence, the last two parts."""
    lines = read_lines(path) or []
    out = []
    for ln in lines:
        if ln.startswith("# Ruling ") and ": " in ln:
            title = ln.split(": ", 1)[1].strip()
            if len(title) > TITLE_LIMIT:
                out.append("the title is %d characters, over %d" % (len(title), TITLE_LIMIT))
            break
    secs = sections(lines)
    for name in secs:
        if name not in DOC_PARTS:
            out.append("a section outside the document shape: %s" % name[:40])
    for ln in lines:
        if ln.startswith("## "):
            break
        low = ln.lower()
        if ln.startswith("- ") and ("this session" in low or "in session" in low.split(":", 1)[-1] and not ln.startswith("- Ruled by:")):
            out.append("the header names the session: %s" % ln[:60])
        if ln.startswith("- Question:") and len(ln.split()) - 2 > QUESTION_WORDS:
            out.append("the Question bullet is %d words, over %d" % (len(ln.split()) - 2, QUESTION_WORDS))
    for ln in secs.get("The ruling", []):
        head, dot, rest = ln.partition(". ")
        if not dot or not head.isdigit() or not head.isascii():
            if ln.strip():
                out.append("The ruling holds a line that is not a numbered point: %s" % ln.strip()[:50])
            continue
        if len(rest.strip()) > POINT_LIMIT:
            out.append("ruling point %s is %d characters, over %d" % (head, len(rest.strip()), POINT_LIMIT))
        bare = outside_code(rest)
        k = bare.find("(")
        if k >= 0 and bare.find(")", k) > k:
            out.append("ruling point %s holds a parenthetical" % head)
    for ln in secs.get("Evidence", []):
        s = ln.strip()
        if not s or s.startswith(">"):
            continue
        if s.startswith("- "):
            s = s[2:]
        toks = []
        for chunk in s.split(","):
            toks.extend(chunk.split(" and "))
        if not all(is_path_token(x) for x in toks):
            out.append("an Evidence line is not paths only: %s" % s[:60])
    for name, cap in SECTION_WORDS:
        body = [x for x in secs.get(name, []) if x.strip()]
        if len(body) > 1:
            out.append("'%s' is more than one line" % name)
        n = sum(len(x.split()) for x in body)
        if n > cap:
            out.append("'%s' is %d words, over %d" % (name, n, cap))
    return out


# --- the transcript lookup ------------------------------------------------------------------------------

OPERATOR_SOURCES = ("typed", "queued")
QUESTION_TOOL = "AskUserQuestion"


class Refused(Exception):
    pass


def project_key(path):
    return "".join(c if c.isalnum() or c == "-" else "-" for c in path)


def real_home():
    """The running user's home folder from the system user database; the environment cannot move it."""
    import pwd
    return pwd.getpwuid(os.getuid()).pw_dir


def store_root():
    """Claude Code's transcript store: <home>/.claude/projects. CLAUDE_CONFIG_DIR and HOME are ignored, so a
    relocated config folder is not supported and the environment cannot point the lookup at another store."""
    return os.path.join(real_home(), ".claude", "projects")


def in_store(path):
    """True when a path, symlinks resolved, lies inside Claude Code's transcript store."""
    s, p = os.path.realpath(store_root()), os.path.realpath(path)
    return p.startswith(s.rstrip(os.sep) + os.sep)


def project_dir(explicit, root, session=None):
    """The store folder of this project: the one named (it must lie in the store), else the nearest folder for the
    working folder, the root or one of their parents; with a session id, the nearest such folder holding it."""
    base, tried = store_root(), []
    for start in (os.path.abspath(os.getcwd()), os.path.realpath(os.getcwd()), root):
        p = start
        while p and p not in tried:
            tried.append(p)
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
    never = {os.path.realpath(real_home()), os.path.realpath(os.sep)}  # too wide to be one project
    never_keys = {project_key(p) for p in never} | {project_key(real_home()), project_key(os.sep)}
    if explicit:
        if os.path.isdir(explicit) and os.path.basename(os.path.realpath(explicit)) in never_keys:
            raise Refused("%s is the home folder's or the root's store folder, not a project's" % explicit)
        if not in_store(explicit):
            raise Refused("%s is outside Claude Code's transcript store (%s); only the store is read"
                          % (explicit, store_root()))
        if os.path.isdir(explicit) and os.path.basename(os.path.realpath(explicit)) not in {project_key(p) for p in tried}:
            raise Refused("%s is not this project's folder in Claude Code's store" % explicit)
        return explicit
    tried = [p for p in tried if os.path.realpath(p) not in never]
    found = [os.path.join(base, project_key(p)) for p in tried if os.path.isdir(os.path.join(base, project_key(p)))]
    if session:
        held = [d for d in found if os.path.isfile(os.path.join(d, session + ".jsonl"))]
        if held:
            return held[0]
    if found:
        return found[0]
    if os.path.realpath(os.getcwd()) in never:
        raise Refused("the home folder or the root is not a project; run from the project's folder")
    return os.path.join(base, project_key(os.path.abspath(os.getcwd())))


def epoch(ts):
    import datetime
    try:
        d = datetime.datetime.strptime((ts or "")[:19], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None
    return int(d.replace(tzinfo=datetime.timezone.utc).timestamp())


def iso_of(seconds):
    import datetime
    return datetime.datetime.fromtimestamp(seconds, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path):
    out = []
    for ln in read_lines(path) or []:
        try:
            r = json.loads(ln)
        except ValueError:
            continue
        if isinstance(r, dict):
            out.append(r)
    return out


def strip_pasted(text):
    """Text with every pasted block replaced by `[pasted text]` (pasted text is not the operator's typing). A block
    closes only at the closing tag carrying its own id; a block with no such tag runs to the end of the text."""
    out, i = [], 0
    while True:
        k = text.find("<pasted_content", i)
        if k < 0:
            out.append(text[i:])
            return "".join(out)
        g = text.find(">", k)
        head = text[k:g + 1] if g >= 0 else ""
        q = head.find('id="')
        pid = head[q + 4:head.find('"', q + 4)] if q >= 0 and head.find('"', q + 4) > 0 else None
        out.append(text[i:k] + "[pasted text]")
        close = '</pasted_content id="%s">' % pid if pid else None
        e = text.find(close, g + 1) if (close and g >= 0) else -1
        if e < 0:
            return "".join(out)
        i = e + len(close)


def message_text(row):
    """The text of a row's message, or None when it holds a tool result or no text."""
    c = (row.get("message") or {}).get("content")
    if isinstance(c, str):
        return c
    if not isinstance(c, list):
        return None
    parts = []
    for x in c:
        if not isinstance(x, dict):
            continue
        if x.get("type") == "tool_result":
            return None
        if x.get("type") == "text":
            parts.append(x.get("text") or "")
    return "\n".join(parts) if parts else None


SKILL_COMMANDS = ("/magic:ruled", "/ruled")  # this skill's own slash commands


def own_command_args(text):
    """The arguments of this skill's own slash command row, else None (any other command row is refused)."""
    open_, close = "<command-name>", "</command-name>"
    i = text.find(open_)
    j = text.find(close, i + len(open_)) if i >= 0 else -1
    if j < 0 or text.count(open_) != 1 or text[i + len(open_):j].strip() not in SKILL_COMMANDS:
        return None
    a, b = "<command-args>", "</command-args>"
    k = text.find(a)
    m = text.find(b, k + len(a)) if k >= 0 else -1
    return text[k + len(a):m].strip() if m >= 0 and text.count(a) == 1 else None


def operator_text(row):
    """The operator's own typed text in a row, else None. A typed slash command counts only when it is this skill's
    own; its arguments are the message."""
    if row.get("type") != "user" or row.get("isMeta") or row.get("isSidechain"):
        return None
    origin = row.get("origin")
    if not isinstance(origin, dict) or origin.get("kind") != "human":
        return None
    t = message_text(row)
    if t is None:
        return None
    if "<command-name>" in t:
        if "pasted_content" in t or not t.lstrip().startswith(("<command-message>", "<command-name>")):
            return None  # command tags inside a paste or after other text are not the row's own command
        if row.get("promptSource") not in OPERATOR_SOURCES + (None,):
            return None
        t = own_command_args(t)
        if not t:
            return None
    elif row.get("promptSource") not in OPERATOR_SOURCES:
        return None
    t = strip_pasted(t)
    return None if "pasted_content" in t else t


def dialog_answer(row, by_uuid):
    """(question block, picked) for an answer to the question tool, else None."""
    res = row.get("toolUseResult")
    if row.get("type") != "user" or row.get("isSidechain") or not isinstance(res, dict):
        return None
    qs, ans = res.get("questions"), res.get("answers")
    if not isinstance(qs, list) or not isinstance(ans, dict) or not qs:
        return None
    src = by_uuid.get(str(row.get("sourceToolAssistantUUID")))
    content = ((src or {}).get("message") or {}).get("content") or []
    asks = {x.get("id") for x in content if isinstance(x, dict) and x.get("type") == "tool_use" and x.get("name") == QUESTION_TOOL}
    answered = [x.get("tool_use_id") for x in ((row.get("message") or {}).get("content") or [])
                if isinstance(x, dict) and x.get("type") == "tool_result"]
    if not asks or not answered or not any(a in asks for a in answered):
        return None
    qlines, picks = [], []
    for q in qs:
        if not isinstance(q, dict):
            continue
        text = q.get("question") or ""
        qlines.append(text)
        for o in q.get("options") or []:
            if isinstance(o, dict):
                qlines.append("- " + (o.get("label") or "") + ((": " + o["description"]) if o.get("description") else ""))
        if text in ans:
            picks.append(str(ans[text]))
    if not picks:
        return None
    return "\n".join(qlines), "\n".join(picks)


def question_before(rows_, idx):
    """The last assistant message before idx: its text parts, joined once per message id."""
    mid = None
    main = [r for r in rows_[:idx] if not r.get("isSidechain") and not r.get("isMeta")]
    for r in reversed(main):
        if r.get("type") == "assistant" and message_text(r):
            mid = (r.get("message") or {}).get("id")
            break
    if mid is None:
        return ""
    parts = []
    for r in main:
        if r.get("type") == "assistant" and (r.get("message") or {}).get("id") == mid:
            t = message_text(r)
            if t and t not in parts:
                parts.append(t)
    return "\n".join(parts)


def ask_row(rows_, idx, by_uuid):
    """The row of the typed operator message before the assistant's last text before idx, when that text asks no
    question; None otherwise (a question, no text, or a dialog answer in that place)."""
    main = [(i, r) for i, r in enumerate(rows_[:idx]) if not r.get("isSidechain") and not r.get("isMeta")]
    mid = None
    for _, r in reversed(main):
        if r.get("type") == "assistant" and message_text(r):
            mid = (r.get("message") or {}).get("id")
            break
    if mid is None:
        return None
    first = next(i for i, r in main if r.get("type") == "assistant" and (r.get("message") or {}).get("id") == mid)
    text = "\n".join(message_text(r) or "" for _, r in main
                     if r.get("type") == "assistant" and (r.get("message") or {}).get("id") == mid)
    if "?" in text:
        return None
    for i, r in reversed([(i, r) for i, r in main if i < first]):
        if safe(operator_text, r) is not None:
            return i
        if safe(dialog_answer, r, by_uuid):
            return None
    return None


def candidates(path):
    rows_ = load(path)
    stem = os.path.basename(path)[:-len(".jsonl")]
    if any(isinstance(r.get("sessionId"), str) and r.get("sessionId") != stem for r in rows_):
        raise Refused("%s holds rows of another session; this transcript is not trusted" % os.path.basename(path))
    prompts = [r for r in rows_ if r.get("type") == "user" and safe(message_text, r) is not None]
    if prompts and not any("promptSource" in r for r in prompts):
        raise Refused("%s has no typed-prompt labels; this transcript format cannot be read" % os.path.basename(path))
    by_uuid = {str(r.get("uuid")): r for r in rows_ if r.get("uuid")}
    out = []
    for i, r in enumerate(rows_):
        s = epoch(r.get("timestamp")) if isinstance(r.get("timestamp"), str) else None
        if s is None:
            continue
        base = {"seconds": s, "session": stem, "time": r.get("timestamp"), "transcript": path, "row": i,
                "uuid": r.get("uuid") if isinstance(r.get("uuid"), str) else None}
        t = safe(operator_text, r)
        if t is not None:
            out.append(dict(base, provenance="typed", message=t, question=safe(question_before, rows_, i) or "",
                            ask_row=safe(ask_row, rows_, i, by_uuid)))
            continue
        d = safe(dialog_answer, r, by_uuid)
        if d:
            out.append(dict(base, provenance="dialog", message=d[1], question=d[0]))
    start = min((c["time"] for c in out), key=time_key, default="")  # when this transcript's operator rows begin
    for c in out:
        c["start"] = start
    return out


def safe(fn, *args):
    """fn(*args), or None for a row whose shape the harness does not write."""
    try:
        return fn(*args)
    except (AttributeError, TypeError, KeyError, ValueError):
        return None


def one_per_message(cands, prefer=None):
    """A row Claude Code copied into a forked or resumed session (same row id, time, provenance and text) is one
    message, credited to the named session when it holds a copy, else to the transcript whose operator rows begin
    first. Rows that differ in anything stay apart, so a planted look-alike makes the lookup refuse as ambiguous."""
    best = {}
    for c in cands:
        if not c.get("uuid"):
            best[id(c)] = c
            continue
        k = (c["uuid"], c["time"], c["provenance"], c["message"])
        rank = lambda x: (x["session"] != prefer, time_key(x.get("start", "")), x["session"])
        if k not in best or rank(c) < rank(best[k]):
            best[k] = c
    keep = {id(c) for c in best.values()}
    return [c for c in cands if id(c) in keep]


def number(cands):
    """Give same-second operator messages their `-n` suffix, ordered by recorded time, then session, then row."""
    by = {}
    for c in cands:
        by.setdefault(c["seconds"], []).append(c)
    for group in by.values():
        group.sort(key=lambda c: (time_key(c["time"]), c["session"], c.get("row", 0)))
        for n, c in enumerate(group, 1):
            c["id"] = "WR-%d" % c["seconds"] if len(group) == 1 else "WR-%d-%d" % (c["seconds"], n)
    return cands


def session_files(pdir, session, newest_only, since=None):
    if session and "${" in session:  # an unsubstituted session variable: no session named
        session = None
    if session:
        p = session if os.path.isfile(session) else os.path.join(pdir, session + ".jsonl")
        if not os.path.isfile(p):
            raise Refused("no transcript: %s" % session)
        if not in_store(p) or os.path.realpath(os.path.dirname(p)) != os.path.realpath(pdir):
            raise Refused("%s is not a transcript of this project in Claude Code's store" % session)
        return [p]
    if not os.path.isdir(pdir):
        raise Refused("no transcript: %s does not exist" % pdir)
    if not in_store(pdir):
        raise Refused("%s is outside Claude Code's transcript store; only the store is read" % pdir)
    files = []
    for f in os.listdir(pdir):
        p = os.path.join(pdir, f)
        try:
            if f.endswith(".jsonl") and os.path.isfile(p) and in_store(p) \
                    and os.path.realpath(os.path.dirname(os.path.realpath(p))) == os.path.realpath(pdir):
                files.append((os.path.getmtime(p), p))
        except OSError:
            continue
    files = [p for _, p in sorted(files)]
    if not files:
        raise Refused("no transcript in %s" % pdir)
    if newest_only:
        return files[-1:]
    if since is not None:
        return [p for p in files if os.path.getmtime(p) >= since]
    return files


def parse_when(value):
    """(seconds, suffix | None) from a WR-id, unix seconds or YYYY-MM-DD (UTC midnight)."""
    v = value.strip()
    if v.startswith("WR-"):
        p = parse_id(v)
        if not p or p[1]:
            raise Refused("not a ruling id: %s" % value)
        sec, _, suf = p[0][3:].partition("-")
        return int(sec), (int(suf) if suf else None)
    if v.isascii() and v.isdigit() and len(v) == 10:
        return int(v), None
    s = epoch(v + "T00:00:00") if len(v) == 10 else None
    if s is None:
        raise Refused("not a time, id or date: %s" % value)
    return s, None


def quote(text):
    return "\n".join("> " + ln if ln else ">" for ln in text.splitlines()) or ">"


def show(c, ask=None):
    print("id: %s" % c.get("id", "WR-%d" % c["seconds"]))
    print("session: %s" % c["session"])
    print("time: %s" % c["time"])
    print("provenance: %s" % c["provenance"])
    print("transcript: %s" % c["transcript"])
    if ask:
        print("ask: %s" % ask)
    print("### question")
    print(quote(c["question"]) if c["question"] else "(none)")
    print("### message")
    print(quote(c["message"]))


PLACEHOLDERS = ("{{question}}", "{{message}}", "{{ask}}", "{{session}}", "{{provenance}}", "{{time}}")


def fill(doc, c, ask=None):
    try:
        with open(doc, encoding="utf-8") as f:
            body = f.read()
    except (OSError, UnicodeDecodeError) as e:
        raise Refused("cannot read %s: %s" % (doc, e))
    if "{{message}}" not in body:
        raise Refused("%s has no {{message}} placeholder" % doc)
    if ("{{ask}}" in body) != (ask is not None):
        raise Refused("%s: an {{ask}} placeholder needs --ask <id of the ask>, and --ask needs the placeholder" % doc)
    values = {"{{question}}": quote(c["question"]) if c["question"] else "> (no question shown)",
              "{{message}}": quote(c["message"]), "{{ask}}": quote(ask["message"]) if ask else "",
              "{{session}}": c["session"],
              "{{provenance}}": c["provenance"], "{{time}}": c["time"]}
    out, i = [], 0
    while i < len(body):  # one pass: text put in is never scanned again
        hit = next((p for p in PLACEHOLDERS if body.startswith(p, i)), None)
        if hit:
            out.append(values[hit])
            i += len(hit)
        else:
            out.append(body[i])
            i += 1
    try:
        with open(doc, "w", encoding="utf-8") as f:
            f.write("".join(out))
    except OSError as e:
        raise Refused("cannot write %s: %s" % (doc, e))
    print("filled: %s" % doc)


def time_key(ts):
    """A recorded time as (second, fraction digits padded to 9): a time with no fraction is .0, whatever its suffix."""
    head, _, rest = (ts or "").partition(".")
    digits = ""
    for ch in rest:
        if ch not in "0123456789":
            break
        digits += ch
    return head[:19], digits.ljust(9, "0")[:9]


def session_stem(session):
    """The session id a --session value names (an id or a transcript path), or None for none or an unsubstituted variable."""
    if not session or "${" in session:
        return None
    b = os.path.basename(session)
    return b[:-len(".jsonl")] if b.endswith(".jsonl") else b


def cmd_find(root, args):
    try:
        stem = session_stem(args.session)
        pdir = project_dir(args.project_dir, root, stem)
        named = session_files(pdir, args.session, False) if stem else []
        try:
            files = session_files(pdir, None, False)  # every transcript: ids are numbered across the whole project
        except Refused:
            if not named:
                raise
            files = []
        real = {os.path.realpath(p) for p in files}
        files += [p for p in named if os.path.realpath(p) not in real]
        named = [next((f for f in files if os.path.realpath(f) == os.path.realpath(p)), p) for p in named]
        found, unread = [], 0
        for p in files:
            try:
                found.extend(candidates(p))
            except Refused:
                if stem and p in named:
                    raise
                unread += 1  # an unlabelled or untrusted transcript is never read, and never guessed from
        found = one_per_message(found, stem)
        number(found)
        if args.since is not None:
            if args.since == "session":
                start = None
                shown_session = stem
                if not stem:
                    newest = session_files(pdir, None, True)[0]
                    shown_session = os.path.basename(newest)[:-len(".jsonl")]
                window = [c for c in found if c["session"] == shown_session]
            else:
                start = parse_when(args.since)[0]
                window = [c for c in found if c["seconds"] >= start and (stem is None or c["session"] == stem)]
            for c in window:
                show(c)
                print("")
            print("window: from %s; transcripts read: %d%s; operator messages: %d"
                  % (iso_of(start) if start is not None else "the start of the session", len(files) - unread,
                     " (%d without labels not read)" % unread if unread else "", len(window)))
            return 0
        if args.at is not None:
            s, suf = parse_when(args.at)
            group = [c for c in found if c["seconds"] == s]
            if suf is None:
                hits = group
            else:
                hits = [c for c in group if c["id"] == "WR-%d-%d" % (s, suf)]
                if not hits and len(group) == 1 and stem and group[0]["session"] == stem:
                    hits = group  # a suffix on a second with one message numbers a ruling within that message
            if stem:
                hits = [c for c in hits if c["session"] == stem]
            what = "at %s" % args.at
        else:
            hits = [c for c in found if args.quote in c["message"] and (stem is None or c["session"] == stem)]
            what = "holding the quote" + (" in session %s" % stem if stem else "")
        if not hits:
            raise Refused("no operator message %s (only typed or queued prompts and question-dialog answers count)%s"
                          % (what, "; %d transcript(s) not read (no labels, or another session's rows)" % unread if unread else ""))
        if len(hits) > 1:
            raise Refused("%d operator messages %s: %s; name one" % (len(hits), what, ", ".join(c["id"] for c in hits)))
        ask = None
        if args.ask is not None:
            if args.at is None:
                raise Refused("--ask needs --at")
            s2, suf2 = parse_when(args.ask)
            asks = [c for c in found if c["seconds"] == s2 and c["session"] == hits[0]["session"]
                    and (suf2 is None or c["id"] == "WR-%d-%d" % (s2, suf2))]
            if len(asks) != 1:
                raise Refused("%d operator messages at %s in the ruling's session; the ask must be one" % (len(asks), args.ask))
            ask = asks[0]
            if ask["provenance"] == "dialog":
                raise Refused("the ask %s is a dialog answer, not a message that asked for a proposal" % ask["id"])
            if time_key(ask["time"]) >= time_key(hits[0]["time"]):
                raise Refused("the ask %s is not before the ruling %s" % (ask["id"], hits[0]["id"]))
        if args.fill:
            fill(args.fill, hits[0], ask)
        elif ask is not None:
            raise Refused("--ask fills a document: pass --fill")
        h = hits[0]
        named_ask = next((c["id"] for c in found if h.get("ask_row") is not None and c["transcript"] == h["transcript"]
                          and c["row"] == h["ask_row"] and c["provenance"] == "typed"), None)
        show(h, named_ask)
        return 0
    except Refused as e:
        print("refused: %s" % e)
        return 3


# --- commands -------------------------------------------------------------------------------------------

def cmd_list(target):
    lists, _ = select(target)
    if not lists:
        print("warn: no rulings list for %s" % target, file=sys.stderr)
    for p, n, ln, _ in rows(lists):
        print("%s:%d  %s" % (shown(p), n, ln[2:]))
    return 0


def cmd_pending(target):
    lists, skipped = select(target)
    for s in skipped:
        print("skip: %s (%s)" % (shown(s), IGNORE_MARK), file=sys.stderr)
    for p, n, ln, m in rows(lists):
        if isinstance(m, dict) and m["status"] == "pending":
            print("%s:%d  %s" % (shown(p), n, ln[2:]))
    return 0


def cmd_check(root, target):
    lists, skipped = select(target)
    errors, warns = [], []
    if target is not None and not lists:
        if os.path.isdir(target):
            warns.append("no rulings list for %s" % target)
        else:
            errors.append("%s is not a rulings list" % target)
    all_rows = rows(lists)
    seen = {}
    for p, n, ln, m in all_rows:
        if isinstance(m, dict):
            seen.setdefault(m["id"], []).append("%s:%d" % (shown(p), n))
    for rid, where in sorted(seen.items()):
        if len(where) > 1:
            errors.append("%s appears on more than one line: %s" % (rid, ", ".join(where)))
    for p, n, ln, m in all_rows:
        where = "%s:%d" % (shown(p), n)
        if isinstance(m, Malformed):
            errors.append("%s: MALFORMED entry (%s): %s" % (where, m, ln))
            continue
        if m is None:
            warns.append("%s: not a ruling line: %s" % (where, ln))
            continue
        folder = os.path.dirname(p)
        for link in m["links"]:
            if not opens(root, p, link):
                errors.append("%s: links %s, which does not exist" % (where, link))
                continue
            full = resolve(root, p, link)
            if DOC_TAG in os.path.basename(link) and os.path.dirname(os.path.realpath(full)) == os.path.realpath(folder):
                for tw in terse_warnings(full):
                    warns.append("%s: %s: %s" % (where, link, tw))
                aes = attribution_errors(full)
                legacy = id_seconds(m["id"]) < ATTRIBUTION_FROM  # the ruling's own time, not the file or git, says how old
                for ae in aes:  # a document committed before the rule only warns: it is never rewritten
                    (warns if legacy else errors).append("%s: %s: %s" % (where, link, ae))
                left = unfilled(full)
                if left:
                    errors.append("%s: %s still holds %s (a document that was never filled)" % (where, link, left))
        has_doc = any(DOC_TAG in os.path.basename(x) and in_folder(root, p, x) for x in m["links"])
        if has_doc and len(m["text"]) > TITLE_LIMIT:
            warns.append("%s: the line title is %d characters, over %d" % (where, len(m["text"]), TITLE_LIMIT))
        if len(m["text"]) > TEXT_LIMIT and not has_doc:
            warns.append("%s: ruling text is %d characters and links no document" % (where, len(m["text"])))
        if m["who"].lower() in ROLE_WORDS:
            warns.append("%s: who '%s' is a role word, not a person" % (where, m["who"]))
        if m["status"] in ("pending", "rejected") and " -> " in m["text"] + " ":  # also an arrow at the end or before the evidence
            warns.append("%s: an arrow ' -> ' belongs only on a landed or superseded line" % where)
        if m["status"] == "landed":
            if not m["arrow"]:
                warns.append("%s: landed without an arrow" % where)
            else:
                for home in m["arrow"].split(","):
                    hp = home_path(home)
                    if hp is None or not opens(root, p, hp):
                        errors.append("%s: arrow to %s, which does not open" % (where, home.strip()))
        elif m["status"] == "superseded":
            if not m["arrow"]:
                warns.append("%s: superseded without an arrow" % where)
            elif m["arrow"] == m["id"]:
                errors.append("%s: superseded by itself" % where)
            elif m["arrow"] not in seen:
                errors.append("%s: superseded by %s, which is in no list read" % (where, m["arrow"]))
    nxt = {m["id"]: m["arrow"] for _, _, _, m in all_rows
           if isinstance(m, dict) and m["status"] == "superseded" and m["arrow"] and m["arrow"] != m["id"]}
    looped = set()
    for start in sorted(nxt):
        path, cur = [], start
        while cur in nxt and cur not in path:
            path.append(cur)
            cur = nxt[cur]
        if cur in path and not looped & set(path[path.index(cur):]):
            loop = path[path.index(cur):]
            looped |= set(loop)
            errors.append("superseded in a loop: %s" % " -> ".join(loop + [cur]))
    for e in errors:
        print("FAIL: " + e)
    for w in warns:
        print("warn: " + w)
    for s in skipped:
        print("skip: %s (%s)" % (shown(s), IGNORE_MARK))
    nl, nr, ns = len(lists), len(all_rows), len(skipped)
    print(f"rulings: {nl} list{'' if nl == 1 else 's'}, {nr} line{'' if nr == 1 else 's'}, "
          f"{len(errors)} FAIL, {len(warns)} warn" + (f", {ns} skipped" if ns else ""))
    return 1 if errors else 0


def cmd_home(root, home):
    hp = home_path(home)
    n = os.path.normpath(os.path.abspath(os.path.join(root, hp))) if hp is not None and not os.path.isabs(hp) else None
    if n is not None and inside(root, n) and os.path.exists(n):
        print("opens: %s" % hp)
        return 0
    print("does not open: %s" % home)
    return 1


def kept_parts(text):
    """What a tidy may not change: every line of an attribution part, every quote-looking line anywhere, and the
    Ruled by / Provenance / Replaces / Standing bullets. Lines are compared exactly, end of line included."""
    out, cur = [], None
    for ln in text.split("\n"):
        h = heading2(ln)
        if h is not None:
            cur = h
            if h in ATTRIBUTION_PARTS:
                out.append(("heading", ln))
            continue
        if cur in ATTRIBUTION_PARTS or ln.lstrip().startswith(">"):
            out.append((cur, ln))
        elif ln.startswith(("- Ruled by:", "- Provenance:", "- Replaces:", "- Standing:")):
            out.append(("header", ln))
    while out and out[-1][1].strip() == "" and out[-1][0] != "heading":  # trailing blank lines of the last part
        out.pop()
    return [(c, l) for c, l in out if l.strip() or c in ATTRIBUTION_PARTS]


def listed_in_folder(root, doc):
    """True when an entry line of the rulings.md in the document's own folder links it (its parsed links, not text)."""
    lst = os.path.join(os.path.dirname(os.path.abspath(doc)), LIST_NAME)
    want = os.path.realpath(doc)
    for ln in read_lines(lst) or []:
        try:
            m = parse_entry(ln)
        except Malformed:
            continue
        for link in (m or {}).get("links", []):
            full = resolve(root, lst, link)
            if full and os.path.realpath(full) == want:
                return True
    return False


def cmd_tidy(root, doc, draft):
    """Replace a ruling document with a form-only rewrite: refused unless its quotes and attribution are unchanged."""
    def refuse(why, code=1):
        print("tidy: refused -- %s; the document is unchanged" % why)
        return code
    if os.path.normpath(draft) != os.path.normpath(doc) + ".tidy":
        return refuse("the draft must be named %s.tidy" % shown(doc))
    if DOC_TAG not in os.path.basename(doc):
        return refuse("%s is not a ruling document" % shown(doc))
    if os.path.islink(doc) or os.path.islink(draft) or not os.path.isfile(doc) or not os.path.isfile(draft):
        return refuse("the document and its draft must be plain files, not links")
    if not listed_in_folder(root, doc):
        return refuse("no rulings.md in the document's folder links %s" % shown(doc))
    try:
        with open(doc, "rb") as f:
            old = f.read().decode("utf-8")
        with open(draft, "rb") as f:
            new = f.read().decode("utf-8")
    except (OSError, UnicodeDecodeError) as err:
        return refuse("a file does not read as UTF-8 (%s)" % type(err).__name__)
    a, b = kept_parts(old), kept_parts(new)
    if a != b:
        i = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        line = (a[i] if i < len(a) else b[i])[1]
        return refuse("a quote or the attribution changed or moved (%d kept lines before, %d after; first at: %s)"
                      % (len(a), len(b), line.strip()[:60]))
    folder = os.path.dirname(os.path.abspath(doc))
    fd, tmp = tempfile.mkstemp(prefix=".tidy-", dir=folder)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(new.encode("utf-8"))
        os.chmod(tmp, os.stat(doc).st_mode & 0o7777)  # the document keeps its mode
        os.replace(tmp, doc)
    except OSError as err:
        if os.path.exists(tmp):
            os.remove(tmp)
        return refuse("cannot write (%s)" % err, 2)
    os.remove(draft)
    print("tidy: %s rewritten; %d quote and attribution lines unchanged" % (shown(doc), len(a)))
    return 0


def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=argparse.SUPPRESS, help="folder that paths in a list resolve from")
    ap = argparse.ArgumentParser(prog="rulings.py", description="rulings lists", parents=[common])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", parents=[common]).add_argument("target")
    sub.add_parser("pending", parents=[common]).add_argument("target", nargs="?")
    sub.add_parser("check", parents=[common]).add_argument("target", nargs="?")
    sub.add_parser("home", parents=[common]).add_argument("home")
    tp = sub.add_parser("tidy", parents=[common], help="replace a ruling document with a form-only rewrite")
    tp.add_argument("document")
    tp.add_argument("draft")
    fp = sub.add_parser("find", parents=[common], help="the operator's message and the question before it")
    g = fp.add_mutually_exclusive_group(required=True)
    g.add_argument("--at", help="WR-id, unix seconds: the operator message at that second")
    g.add_argument("--quote", help="text the operator message holds")
    g.add_argument("--since", help="`session` (the newest transcript), or a WR-id, unix seconds or YYYY-MM-DD (UTC):"
                                   " every operator message from then, in every transcript written since (a sweep)")
    fp.add_argument("--session", help="a transcript file or session id to read instead")
    fp.add_argument("--project-dir", help="the folder holding the transcripts")
    fp.add_argument("--fill", help="a ruling document whose placeholders take the quotes")
    fp.add_argument("--ask", help="WR-id of the operator's earlier ask, quoted into {{ask}} (with --at and --fill)")
    args = ap.parse_args(argv)
    root = root_dir(getattr(args, "root", None))
    if args.cmd == "list":
        return cmd_list(args.target)
    if args.cmd == "pending":
        return cmd_pending(args.target)
    if args.cmd == "home":
        return cmd_home(root, args.home)
    if args.cmd == "find":
        return cmd_find(root, args)
    if args.cmd == "tidy":
        return cmd_tidy(root, args.document, args.draft)
    return cmd_check(root, args.target)


if __name__ == "__main__":
    sys.exit(main())
