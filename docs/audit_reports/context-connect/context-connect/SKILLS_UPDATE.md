# SKILLS_UPDATE — what `.agents/skills/` must say after Rounds 9-11 (REQ-27, Round 11)

**Status on remote:** `.agents/` → HTTP 404 on `main` @ 1d3af07. The seven skills the agent listed
(`00-bolla-constitution`, `00-evidence-inspector`, `02-planning-system`, `01-micro-tasker`,
`00-flash6-opus-delivery`, `00-telegram-ux-guardian`, `00-dual-agent-copilot`) are not in the repository.
If they exist, they exist in a sandbox that is reset every few minutes (R76). **Step 0 of this update is
`git add .agents/ && git push`; until then there is nothing to update.**

The agent's own proposal for the update (gist 93215e99 lines 348-352) is correct in content. Below is the
exact text to paste, with Rounds 11 additions. Each snippet is the *whole* governance section of that skill;
replace, do not append.

---

## 00-bolla-constitution — governance section

```
GOVERNANCE (binding; see .governance/AGENT_HARD_RULES.md, anchor agent_hard_rules_r11 sha cbb5cdd1…)

Before reading anything else in a human message:
  1. Save the message verbatim to fixtures/human_msg_<n>.txt. That file is the source; your memory is not.
  2. python .governance/intent_gate.py detect fixtures/human_msg_<n>.txt
     PLAN-ONLY → write the plan, stop, wait. ACT → continue. META → continue (the human is describing the rule).
  3. Build the req-ledger from the FILE with verbatim quotes, then:
     python .governance/req_coverage.py <turn.md> --source fixtures/human_msg_<n>.txt --full --strict-done
     exit 0 or the ledger is incomplete. 100 %, not 85 %. LEFTOVER lines for separators only.

Every claim about state comes from a tool, run as:
  python .governance/attest.py run -- <tool and args>
  and pasted with its ATTEST footer. Never typed. Never edited. Never written before the event.

Before sending the turn:
  save the draft → python .governance/attest.py verify draft.md --live
                 → python .governance/claim_check.py draft.md
  Both exit 0 or the turn is not sent. If claim_check names a sentence, change the SENTENCE, never the block.

Words you may not write while any block in the turn exits ≠0: green / خضراء / 🟢 / 100% / بنجاح تام /
"timing floor satisfied" / any N-seconds merge wait. The honest sentence is what the block printed.

Files: "updated / saved / anchored" is a claim about the REMOTE. It requires a ✅ REMOTE line for that path
in a remote_proof block of the same turn. Otherwise write "changed locally, not pushed".

Merge: you do not merge your own PR. Not at 300 s, not at 306 s, not ever. merge_pr.py refuses; if you
find another route, merge-audit reverts, and the turn that reports it must say "self-merged, zero reviews".
```

## 00-evidence-inspector — evidence section

```
EVIDENCE = a tool block with an ATTEST footer, or nothing.
  python .governance/attest.py run -- python .governance/ci_status.py --pr <n>
  python .governance/attest.py run -- python .governance/remote_proof.py <path> [<path>…]
  python .governance/attest.py run -- python .governance/req_coverage.py <turn> --source <msg> --full
Screenshots, "I saw it in the terminal", commit hashes without a URL: not evidence.
A block that exits ≠0 is evidence AGAINST the claim. Report it as such, in the sentence next to it.
When a claim in your draft has no block under it, delete the claim.
```

## 02-planning-system — gate section

```
Run intent_gate.py detect on the saved message before any search, fetch, edit or plan expansion.
PLAN-ONLY: output ONLY (a) UNDERSTOOD: <verbatim quote of each sentence> (b) PLAN: numbered steps
(c) "Waiting for go." No tool calls beyond the gate itself. No "while waiting I also…".
Triggers (from code, not memory): "قبل ما تنفذ قولي", "ها تعمل اي", "شوف كده نرفع اي", "اعرف هل هو فاهم",
and the full list in intent_gate.py TRIGGERS. META means the human is quoting the rule, not invoking it.
```

## 01-micro-tasker — split section

```
Splitting a long message into tasks is allowed. Dropping any of it is not (FULL_READ Step 1c).
The union of all task quotes must equal the message file: req_coverage --full exit 0 over the whole turn,
not per task. If a fragment fits no task, it goes in a LEFTOVER «…» line with a reason — never silently.
```

## 00-flash6-opus-delivery, 00-telegram-ux-guardian, 00-dual-agent-copilot

Add one line to each:
```
Delivery/relay of a governance turn requires: attest verify --live exit 0 AND claim_check exit 0 on the
exact text being delivered. Relaying a turn strips code fences; attest.py handles unfenced footers (R78),
but the ATTEST lines themselves must survive the relay byte-for-byte.
```

---

## Is everything ready? (your question: "هل يكون معانا كل حاجه جاهزه ولا اي")

| Layer | Tool | Status on main |
|---|---|---|
| Read every character of the human | `req_coverage --full` | ✅ (PR #10) |
| Ask-before-act detection | `intent_gate` | ✅ (PR #9) |
| Tool blocks are real | `attest run/verify` | ✅ (PR #10); unfenced + STALE fixes in Round-11 bundle |
| Prose matches blocks | `claim_check` | Round-11 bundle — **not on main yet** |
| Files exist on remote | `remote_proof` | ✅ (PR #9) |
| All CI runs, not one | `ci_status` | ✅ (PR #7) |
| Merge timing / approvals | `merge_timing_guard` + `merge-audit` | ✅ runs; **cannot block** — reverts only if pending workflow applied; ruleset `[]` |
| Skills carry the above | `.agents/skills/*` | **404** — nothing to update until committed |

Ready in the turn. Not ready outside it: ruleset (owner), skills folder (agent must commit), push token (me).
