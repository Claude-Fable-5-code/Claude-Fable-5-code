#!/usr/bin/env python3
"""
mock_scan.py — placeholder / stub / mock code must not reach a commit (R93, Round 14, Rule 37).

Usage:
    python .governance/mock_scan.py --staged            # scan files staged for commit (pre-commit hook)
    python .governance/mock_scan.py <path> [<path>…]    # scan given files
    python .governance/mock_scan.py --self-test

Why this exists. Guide §4 forbids "TODO / mock / placeholder" code, and Round 14's preflight audit
(ROUND14_PREFLIGHT_AUDIT.md, R93) found no tool enforcing it — the agent had shipped `pass  # stub`,
`return {"ok": True}` bodies and Arabic "ضع الكود هنا" comments and called the chunk done.  # mock-scan:allow

What is flagged (code files only: py js ts tsx jsx sh ps1 bat yml yaml toml):
    P1  TODO / FIXME / XXX / HACK markers                         (`# TODO`, `// FIXME:`)  # mock-scan:allow
    P2  "put the code here" comments, Arabic or English            (ضع الكود, اكتب الكود, your code here, implement me)  # mock-scan:allow
    P3  stub bodies:  `pass  # stub|todo|placeholder`, `...  # stub`
    P4  `raise NotImplementedError` outside an abstract method     (no @abstractmethod within the previous 3 lines)
    P5  lorem ipsum / placeholder / dummy / mock literals in strings
    P6  a def whose whole body is `return {"ok": True}` / `return True` / `return None` / `return []` with a
        name that promises work (verify|check|validate|scan|run|deploy|test|sync|push|merge|prove|fetch)

Opt-out for a genuine line (e.g. this file's own patterns or a negative test): append `# mock-scan:allow`.
Test/fixture paths (`fixtures/`, `examples/`, `*_test.py`, `test_*.py`, `*.md`) are skipped.

Output (attest grammar):
    mock_scan <scope>: <n> file(s), <m> finding(s)
    🔴 <path>:<line> P<k> <excerpt>
    ✅ mock_scan: clean | ⛔ mock_scan: <m> placeholder line(s) — finish the code or delete it (Rule 37)
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CODE_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".ps1", ".bat", ".yml", ".yaml", ".toml"}
SKIP = re.compile(r"(^|/)(fixtures|examples|tests?)/|(^|/)test_[^/]*\.py$|_test\.py$|\.md$", re.I)
ALLOW = "mock-scan:allow"

P1 = re.compile(r"(#|//|/\*|<!--|\brem\b)\s*(TODO|FIXME|XXX|HACK)\b", re.I)
P2 = re.compile(r"ضع الكود|اكتب الكود|الكود هنا|your code here|code goes here|implement me\b|implement this\b", re.I)  # mock-scan:allow
P3 = re.compile(r"^\s*(pass|\.\.\.)\s*#\s*(stub|todo|placeholder|later|tbd)\b", re.I)
P4 = re.compile(r"^\s*raise NotImplementedError\b")
P5 = re.compile(r"[\"'](lorem ipsum|placeholder|dummy (value|data|text)|mock (value|data|response))[\"']", re.I)
DEF = re.compile(r"^\s*def (\w+)\(")
WORK = re.compile(r"verify|check|validate|scan|run|deploy|test|sync|push|merge|prove|fetch|record|gate", re.I)
CONST_RET = re.compile(r"^\s*return (\{\s*[\"']ok[\"']\s*:\s*True\s*\}|True|None|\[\]|\{\}|0|\"\"|'')\s*$")


def is_abstract(lines, i) -> bool:
    return any("@abstractmethod" in lines[j] or "ABC" in lines[j] for j in range(max(0, i - 4), i))


def scan_lines(lines):
    """Return [(lineno, code, excerpt)] — pure function, unit-tested."""
    out = []
    for i, ln in enumerate(lines):
        if ALLOW in ln:
            continue
        for code, rx in (("P1", P1), ("P2", P2), ("P3", P3), ("P5", P5)):
            if rx.search(ln):
                out.append((i + 1, code, ln.strip()[:80])); break
        else:
            if P4.search(ln) and not is_abstract(lines, i):
                out.append((i + 1, "P4", ln.strip()[:80]))
    # P6: def <work-name>(…): with a body that is a single constant return (docstring allowed)
    for i, ln in enumerate(lines):
        m = DEF.match(ln)
        if not m or not WORK.search(m.group(1)) or ALLOW in ln:
            continue
        body = []
        for j in range(i + 1, min(len(lines), i + 8)):
            s = lines[j].strip()
            if not s or s.startswith(("#", '"""', "'''")):
                continue
            if lines[j].startswith((" ", "\t")):
                body.append(lines[j])
            else:
                break
        if len(body) == 1 and CONST_RET.match(body[0]) and ALLOW not in body[0]:
            out.append((i + 1, "P6", f"def {m.group(1)}(): constant return — {body[0].strip()}"))
    return out


def staged_files():
    r = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"], capture_output=True, text=True, cwd=ROOT)
    return [p for p in r.stdout.split("\n") if p]


def scan(paths, scope: str) -> int:
    files = [p for p in paths if pathlib.Path(p).suffix.lower() in CODE_EXT and not SKIP.search(p)]
    findings = []
    for p in files:
        fp = ROOT / p
        if not fp.exists():
            continue
        try:
            lines = fp.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        findings += [(p, *f) for f in scan_lines(lines)]
    print(f"mock_scan {scope}: {len(files)} file(s), {len(findings)} finding(s)")
    for p, n, code, ex in findings:
        print(f"🔴 {p}:{n} {code} {ex}")
    if findings:
        print(f"⛔ mock_scan: {len(findings)} placeholder line(s) — finish the code or delete it (Rule 37)"); return 1
    print("✅ mock_scan: clean"); return 0


def self_test() -> int:
    ok = True
    bad = [  # mock-scan:allow
        "x = 1  # TODO later",                       # P1  # mock-scan:allow
        "# ضع الكود هنا",                              # P2  # mock-scan:allow
        "def f():", "    pass  # stub",              # P3
        "def g():", "    raise NotImplementedError",  # P4
        "s = 'lorem ipsum'",                         # P5  # mock-scan:allow
        "def verify_thing(a):", '    """doc"""', '    return {"ok": True}',  # P6
    ]
    codes = [c for _, c, _ in scan_lines(bad)]
    ok &= codes == ["P1", "P2", "P3", "P4", "P5", "P6"]
    good = [
        "class A(ABC):", "    @abstractmethod", "    def run(self):", "        raise NotImplementedError",  # abstract → ok
        "x = 1  # TODO later  # mock-scan:allow",  # opt-out
        "def verify_x(a):", "    if a:", "        return True", "    return False",  # real body
        "def helper():", "    return None",  # name promises no work
        "todo_list = []",  # word without comment marker
    ]
    ok &= scan_lines(good) == []
    ok &= SKIP.search("docs/x/fixtures/human_msg.txt") is not None and SKIP.search(".governance/mock_scan.py") is None
    print("✅ mock_scan self-test ok (6 patterns flagged / abstract+allow+real-body+non-work-name+bare-word pass / skip paths)" if ok
          else f"⛔ mock_scan self-test FAILED codes={codes}")
    return 0 if ok else 1


def main(argv):
    if "--self-test" in argv:
        return self_test()
    if argv == ["--staged"]:
        return scan(staged_files(), "staged")
    if argv and not argv[0].startswith("-"):
        return scan(argv, "paths")
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
