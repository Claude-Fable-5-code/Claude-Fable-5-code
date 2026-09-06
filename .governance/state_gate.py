#!/usr/bin/env python3
"""
state_gate.py — the agent restores state at the START of a turn and advances it at the END, or the turn
is not sendable (R90, Round 14, Rule 35).

Usage:
    python .governance/state_gate.py open  [--ack-drift]
    python .governance/state_gate.py close [--write] [--next "…"] [--last "…"] [--tag "…"] [--mode "…"]
    python .governance/state_gate.py check <turn.md>
    python .governance/state_gate.py verify [--staged]
    python .governance/state_gate.py --self-test

Why this exists (Round 14). USER_COMPLETE_OPERATING_GUIDE §9 promised a "compulsory silent pre-flight": the
agent reads Root/ai_state.json + Root/PROGRESS.md before writing a word and updates them after. Audit:
`grep ai_state .governance/*.py` found only a regex in claim_check; no hook, no precheck step, no CI step
read the file. ai_state.json sat 10 commits behind HEAD. A promise with no tool is prose.

  open    reads Root/ai_state.json + Root/PROGRESS.md, prints a `state_gate open` block (head, state commit,
          drift, turn, next_action) and writes .governance/.state_open.json (the open marker).
          exit 1 when drift>0 and --ack-drift is absent — the agent must SEE the gap before it works.
  close   requires the open marker. --write rewrites ai_state.json (turn_count+1, git_commit=HEAD,
          last_updated=now, optional next/last/tag/mode). Then verifies: turn_count advanced by exactly 1,
          git_commit==HEAD, last_updated > open utc, next_action non-empty. exit 1 otherwise. Removes marker.
  check   the turn's FIRST tool block is `state_gate open`, ONE `state_gate close` block exists with exit=0 and
          a ✅ verdict, and every tool block after close is a turn-closing one (precheck/self_review/attest/
          state_gate). Anything else after close = work done after the state was sealed → exit 1.
  verify  repo-level (hook + CI): ai_state.json parses, git_commit ∈ allowed(HEAD), next_action non-empty,
          Root/PROGRESS.md exists and is non-empty. allowed(HEAD) = {HEAD, HEAD~1} for an ordinary commit; for a
          MERGE commit (2+ parents — GitHub's "Merge pull request") it also includes every parent and each
          non-first parent's own parent, because the PR head's ai_state.json legally points at HEAD~1 *of the
          branch*, not of main (R95, Round 15: main went red after PR #14 for exactly this reason).
  Both open and close print `remaining=N` = number of `- [ ]` lines in Root/PROGRESS.md — the tool-stamped
  answer to "فاضل حاجة ولا خلاص؟" (Round 15). N=0 → nothing remains.
  Every write uses newline="\n" so a Windows Python cannot turn the state file into CRLF (R97). --staged reads ai_state.json from the index and demands
          it be staged whenever any other file is staged ("state moves with code").
"""
import datetime, json, pathlib, re, subprocess, sys, tempfile

GOV = pathlib.Path(__file__).resolve().parent
ROOT = GOV.parent
sys.path.insert(0, str(GOV))
STATE = "Root/ai_state.json"
PROGRESS = "Root/PROGRESS.md"
MARK = ".governance/.state_open.json"
CLOSERS = {"precheck", "self_review", "attest", "state_gate"}


def git(root, *a) -> str:
    p = subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=root)
    return (p.stdout or "").strip()


def utcnow() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(s: str):
    try:
        d = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)
    except Exception:
        return None


def remaining(root) -> int:
    """Count of open `- [ ]` checklist lines in Root/PROGRESS.md (0 when the file is missing)."""
    prog = root / PROGRESS
    if not prog.exists():
        return 0
    return sum(1 for l in prog.read_text(encoding="utf-8", errors="replace").splitlines() if l.lstrip().startswith("- [ ]"))


def allowed_state_commits(root) -> list:
    """Short SHAs a committed ai_state.json may legally point at for the current HEAD (R95)."""
    parents = git(root, "rev-list", "--parents", "-n1", "HEAD").split()
    head, ps = parents[0] if parents else "", parents[1:] if parents else []
    out = [head[:7]] if head else []
    for i, p in enumerate(ps):
        out.append(p[:7])
        if i > 0:                                   # non-first parent = the PR head; its own HEAD~1 is legal too
            pp = git(root, "rev-parse", "--short=7", f"{p}~1")
            if pp:
                out.append(pp)
    return [x for x in out if x]


def load_state(root, staged=False):
    raw = git(root, "show", f":{STATE}") if staged else (root / STATE).read_text(encoding="utf-8") if (root / STATE).exists() else ""
    try:
        return json.loads(raw), None
    except Exception as e:
        return None, f"{STATE} unreadable: {e}"


def drift(root, state_commit: str) -> int:
    if not state_commit or not re.fullmatch(r"[0-9a-f]{7,40}", state_commit) or git(root, "cat-file", "-t", state_commit) != "commit":
        return -1
    n = git(root, "rev-list", "--count", f"{state_commit}..HEAD")
    return int(n) if n.isdigit() else -1


def cmd_open(root, ack: bool) -> int:
    st, err = load_state(root)
    head = git(root, "rev-parse", "--short=7", "HEAD") or "0000000"
    if err:
        print(f"state_gate open: head={head} state=??????? drift=? turn=?"); print(f"⛔ state_gate: open — {err}"); return 1
    sc = str(st.get("git_commit", ""))[:7] or "???????"
    d = drift(root, st.get("git_commit", ""))
    turn = st.get("turn_count", 0)
    prog = root / PROGRESS
    plines = len(prog.read_text(encoding="utf-8", errors="replace").splitlines()) if prog.exists() else 0
    print(f"state_gate open: head={head} state={sc} drift={d if d >= 0 else '?'} turn={turn}")
    print(f"  tag={st.get('current_tag', '-')}  mode={st.get('mode', '-')}")
    print(f"  next={str(st.get('next_action', ''))[:120]}")
    print(f"  progress={'ok' if plines else 'MISSING'} ({plines} lines)  remaining={remaining(root)}")
    (root / MARK).write_text(json.dumps({"utc": utcnow(), "head": head, "turn_count": turn}), encoding="utf-8", newline="\n")
    if d == 0:
        print("✅ state_gate: open — state matches HEAD"); return 0
    if ack:
        print(f"🟡 state_gate: open — drift {d} commit(s) acknowledged; close --write must bring state to {head}"); return 0
    print(f"⛔ state_gate: open — state is {d if d >= 0 else 'unknown'} commit(s) behind HEAD ({sc}); re-run with --ack-drift, then close --write this turn"); return 1


def cmd_close(root, write: bool, opts: dict) -> int:
    head = git(root, "rev-parse", "--short=7", "HEAD") or "0000000"
    mark = root / MARK
    if not mark.exists():
        print(f"state_gate close: head={head} state=??????? turn=?→? written=no"); print("⛔ state_gate: close — no open marker; this turn never ran `state_gate open`"); return 1
    op = json.loads(mark.read_text(encoding="utf-8"))
    st, err = load_state(root)
    if err:
        print(f"state_gate close: head={head} state=??????? turn=?→? written=no"); print(f"⛔ state_gate: close — {err}"); return 1
    if write:
        st["turn_count"] = int(op["turn_count"]) + 1
        st["git_commit"] = head
        st["last_updated"] = utcnow()
        for k, key in (("next", "next_action"), ("last", "last_action"), ("tag", "current_tag"), ("mode", "mode")):
            if opts.get(k):
                st[key] = opts[k]
        (root / STATE).write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    bad = []
    if int(st.get("turn_count", -1)) != int(op["turn_count"]) + 1:
        bad.append(f"turn_count {st.get('turn_count')} != open {op['turn_count']}+1")
    if str(st.get("git_commit", ""))[:7] != head:
        bad.append(f"git_commit {str(st.get('git_commit', ''))[:7]} != HEAD {head}")
    lu, ou = parse_ts(str(st.get("last_updated", ""))), parse_ts(op["utc"])
    if not lu or not ou or lu < ou:
        bad.append(f"last_updated {st.get('last_updated')} not after open {op['utc']}")
    if not str(st.get("next_action", "")).strip():
        bad.append("next_action empty")
    print(f"state_gate close: head={head} state={str(st.get('git_commit', ''))[:7] or '???????'} turn={op['turn_count']}→{st.get('turn_count')} written={'yes' if write else 'no'}")
    print(f"  next={str(st.get('next_action', ''))[:120]}")
    print(f"  remaining={remaining(root)}")
    for b in bad:
        print(f"🔴 {b}")
    if bad:
        print(f"⛔ state_gate: close — {len(bad)} problem(s); state not advanced (use --write --next \"…\")"); return 1
    mark.unlink()
    print("✅ state_gate: close — state advanced to HEAD"); return 0


def cmd_check(path: str) -> int:
    import attest
    text = sys.stdin.read() if path == "-" else pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    seq = []
    for tool, body in attest.blocks(text):
        first = body[0].strip() if body else ""
        foot = attest.FOOT.match(body[-1].strip()) if body else None
        rc = int(foot.group(5)) if foot else None
        kind = "open" if first.startswith("state_gate open") else "close" if first.startswith("state_gate close") else ""
        ok = kind == "close" and any(l.startswith("✅ state_gate: close") for l in body)
        seq.append((tool, kind, rc, ok))
    print(f"state_gate check {path}: {len(seq)} tool block(s)")
    bad = 0
    if not seq or seq[0][0] != "state_gate" or seq[0][1] != "open":
        print("🔴 first tool block is not `state_gate open` — the turn started without restoring state"); bad += 1
    closes = [i for i, s in enumerate(seq) if s[0] == "state_gate" and s[1] == "close"]
    if len(closes) != 1:
        print(f"🔴 expected exactly one `state_gate close` block, found {len(closes)}"); bad += 1
    else:
        c = seq[closes[0]]
        if c[2] != 0 or not c[3]:
            print(f"🔴 close block exit={c[2]} without ✅ verdict — state was not advanced"); bad += 1
        after = [s[0] for s in seq[closes[0] + 1:] if s[0] not in CLOSERS]
        if after:
            print(f"🔴 work after close: {', '.join(after)} — state was sealed before these ran"); bad += 1
    if bad:
        print(f"⛔ state_gate: check — {bad} problem(s) (Rule 35: open first, close --write last)"); return 1
    print("✅ state_gate: check — open first, close last, state advanced"); return 0


def cmd_verify(root, staged: bool) -> int:
    head = git(root, "rev-parse", "--short=7", "HEAD") or "0000000"
    allowed = allowed_state_commits(root) or [head]
    prev = git(root, "rev-parse", "--short=7", "HEAD~1")
    if prev and prev not in allowed:
        allowed.append(prev)
    bad = []
    if staged:
        files = [f for f in git(root, "diff", "--cached", "--name-only").splitlines() if f]
        if files and STATE not in files:
            bad.append(f"{len(files)} file(s) staged but {STATE} is not — state must move with code")
    st, err = load_state(root, staged=staged and STATE in git(root, "diff", "--cached", "--name-only"))
    sc = str(st.get("git_commit", ""))[:7] if st else "???????"
    if err:
        bad.append(err)
    else:
        if sc not in allowed:
            bad.append(f"git_commit {sc} ∉ {{{', '.join(allowed)}}} (HEAD, HEAD~1, merge parents and PR-head~1)")
        if not str(st.get("next_action", "")).strip():
            bad.append("next_action empty")
        if not parse_ts(str(st.get("last_updated", ""))):
            bad.append(f"last_updated unparseable: {st.get('last_updated')}")
    prog = root / PROGRESS
    if not prog.exists() or not prog.read_text(encoding="utf-8", errors="replace").strip():
        bad.append(f"{PROGRESS} missing or empty")
    print(f"state_gate verify: head={head} state={sc} staged={'yes' if staged else 'no'} merge={'yes' if len(allowed) > 2 else 'no'}")
    for b in bad:
        print(f"🔴 {b}")
    if bad:
        print(f"⛔ state_gate: verify — {len(bad)} problem(s)"); return 1
    print("✅ state_gate: verify — state file current, PROGRESS present"); return 0


def self_test() -> int:
    import contextlib, io
    ok = True
    d = pathlib.Path(tempfile.mkdtemp()); (d / "Root").mkdir(); (d / ".governance").mkdir()
    git(d, "init", "-q"); git(d, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "base")
    h0 = git(d, "rev-parse", "--short=7", "HEAD")
    (d / STATE).write_text(json.dumps({"turn_count": 5, "git_commit": h0, "next_action": "x", "last_updated": "2026-01-01T00:00:00Z"}), encoding="utf-8")
    (d / PROGRESS).write_text("# progress\n- step\n", encoding="utf-8")

    def cap(fn, *a):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = fn(*a)
        return rc, buf.getvalue()

    rc, out = cap(cmd_open, d, False); ok &= rc == 0 and "drift=0" in out                       # 1 in-sync open
    rc, out = cap(cmd_close, d, False, {}); ok &= rc == 1 and "turn_count" in out                # 2 close w/o write fails
    rc, out = cap(cmd_close, d, True, {"next": "do C2"}); ok &= rc == 0 and "turn=5→6" in out  # 3 close --write ok
    rc, out = cap(cmd_close, d, True, {}); ok &= rc == 1 and "no open marker" in out             # 4 close twice
    git(d, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "c2")
    rc, out = cap(cmd_open, d, False); ok &= rc == 1 and "drift=1" in out                        # 5 drift blocks
    rc, out = cap(cmd_open, d, True); ok &= rc == 0 and "acknowledged" in out                    # 6 --ack-drift
    rc, out = cap(cmd_close, d, True, {}); ok &= rc == 0                                          # 7 write heals drift
    rc, out = cap(cmd_verify, d, False); ok &= rc == 0                                            # 8 verify ok
    (d / PROGRESS).unlink()
    rc, out = cap(cmd_verify, d, False); ok &= rc == 1 and "PROGRESS.md missing" in out          # 9 verify catches
    t = d / "turn.md"
    t.write_text("```text\nstate_gate open: head=abcdef0 state=abcdef0 drift=0 turn=1\n✅ state_gate: open — state matches HEAD\nATTEST tool=state_gate sha256=0000000000000000 utc=x head=abcdef0 exit=0 cmd=x\n```\n"
                 "```text\nstate_gate close: head=abcdef0 state=abcdef0 turn=1→2 written=yes\n✅ state_gate: close — state advanced to HEAD\nATTEST tool=state_gate sha256=0000000000000000 utc=x head=abcdef0 exit=0 cmd=x\n```\n"
                 "```text\nprecheck t.md: 1 step(s), source=-, live=no\n✅ precheck: 1/1 steps exit 0 — turn may be sent\nATTEST tool=precheck sha256=0000000000000000 utc=x head=abcdef0 exit=0 cmd=x\n```\n", encoding="utf-8")
    rc, out = cap(cmd_check, str(t)); ok &= rc == 0                                              # 10 well-formed turn
    t.write_text("```text\nprecheck t.md: 1 step(s), source=-, live=no\n✅ precheck: ok\nATTEST tool=precheck sha256=0 utc=x head=abcdef0 exit=0 cmd=x\n```\n", encoding="utf-8")
    rc, out = cap(cmd_check, str(t)); ok &= rc == 1 and "first tool block" in out                # 11 no open
    # 12 R95: merge commit — state points at PR-head~1, must PASS; a stranger SHA must still FAIL
    (d / PROGRESS).write_text("# progress\n- [ ] a\n- [x] b\n- [ ] c\n", encoding="utf-8", newline="\n")
    G = ("-c", "user.email=t@t", "-c", "user.name=t")
    base = git(d, "rev-parse", "HEAD")
    git(d, "checkout", "-q", "-b", "feat")
    git(d, *G, "commit", "-q", "--allow-empty", "-m", "f1"); f1 = git(d, "rev-parse", "--short=7", "HEAD")
    git(d, *G, "commit", "-q", "--allow-empty", "-m", "f2")
    git(d, "checkout", "-q", "-")
    git(d, *G, "commit", "-q", "--allow-empty", "-m", "main-moves")
    git(d, *G, "merge", "-q", "--no-ff", "-m", "Merge pull request", "feat")
    (d / STATE).write_text(json.dumps({"turn_count": 9, "git_commit": f1, "next_action": "x", "last_updated": "2026-01-01T00:00:00Z"}), encoding="utf-8", newline="\n")
    rc, out = cap(cmd_verify, d, False); ok &= rc == 0 and "merge=yes" in out                    # 12 PR-head~1 accepted on merge
    (d / STATE).write_text(json.dumps({"turn_count": 9, "git_commit": base[:7], "next_action": "x", "last_updated": "2026-01-01T00:00:00Z"}), encoding="utf-8", newline="\n")
    rc, out = cap(cmd_verify, d, False); ok &= rc == 1 and "∉" in out                            # 13 stranger SHA still refused
    # 14 remaining=N counts only open boxes; close --write emits LF only
    rc, out = cap(cmd_open, d, True); ok &= "remaining=2" in out
    rc, out = cap(cmd_close, d, True, {"next": "n"}); ok &= rc == 0 and "remaining=2" in out and b"\r" not in (d / STATE).read_bytes()
    print("✅ state_gate self-test ok (open/close/drift/--write/marker/verify/check/merge-aware/remaining/LF: 14 cases)" if ok else "⛔ state_gate self-test FAILED")
    return 0 if ok else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if not argv or argv[0] not in ("open", "close", "check", "verify"):
        print(__doc__); return 2
    if argv[0] == "open":
        return cmd_open(ROOT, "--ack-drift" in argv)
    if argv[0] == "close":
        opts = {k: argv[argv.index(f"--{k}") + 1] for k in ("next", "last", "tag", "mode") if f"--{k}" in argv and argv.index(f"--{k}") + 1 < len(argv)}
        return cmd_close(ROOT, "--write" in argv, opts)
    if argv[0] == "check":
        if len(argv) < 2:
            print("⛔ state_gate check: need turn file or -"); return 2
        return cmd_check(argv[1])
    return cmd_verify(ROOT, "--staged" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
