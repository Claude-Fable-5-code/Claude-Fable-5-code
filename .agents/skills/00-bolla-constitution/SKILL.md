---
name: 00-bolla-constitution
description: دستور بولا الهندسي v1.2 — نظام الحوكمة الموحد والتدرج الثلاثي T0/T1/T2 والقوانين العشرة الذهبية والمراجعة المزدوجة لجميع المشاريع.
---

# 🏛️ مهارة دستور بولا الهندسي — 00-bolla-constitution (v1.2)

> **المرجع الحاكم لجميع أنواع الأكواد والأنظمة في بيئة العمل.**  
> يُفعَّل عند أي مهمة برمجية لتحديد مستوى التدخل (T0 / T1 / T2) وحماية الكود من الانحدار.

## 👑 القوانين العشرة الذهبية:
1. **قانون الحصانة (Immunity Law):** أخذ مرساة `.anchor` وحساب SHA-256 قبل لمس أي كود.
2. **قانون المشرط الجراحي (Scalpel Law):** صياغة التعديلات كـ hunks دقيقة واستخراج كتل BEFORE ميكانيكياً؛ تغيير معماري واحد لكل مرساة.
3. **قانون المعمل المسبق (Pre-Lab Law):** مسبار خارجي لقياس الفرضية ومحاكي جاف dryrun بـ mock صارم.
4. **قانون البرهان الكمي (Empirical Proof Law):** معايير PASS/FAIL كمية ومقاسة من جهة المستقبِل.
5. **قانون الصدق التوثيقي (Documentary Truth Law):** توثيق ما لم يُقَس وParity افتراضياً للقيم غير المقاسة.
6. **قانون فصل الأدوار وبوابات المراجعة (Role Separation & Gates):** قرارات GO/HOLD/RETURN ملزمة وفصل كاتب المواصفة عن معتمدها.
7. **قانون سيادة هدف المستخدم (Goal Sovereignty):** هدف المستخدم ثابت وتشخيصه قابل للتحدي بالقياس.
8. **قانون الإسناد المرجعي الصريح بالسطور (Verbatim Ground-Truth Citation Law):** إسناد أي تعديل بدليل مقتبس حرفياً بالسطور من المرجع المعتمد (HAR أو كود المصدر).
9. **قانون الاستئناف وميثاق التسليم الإلزامي (Continuity & Mandatory Handoff Law):** حظر أي تعديل دون وثيقة مواصفات مسبقة و Pre-edit في ANCHORS.md؛ وإلزام وثيقة HANDOFF.md والتقرير الختامي للمرحلة.
10. **قانون العزل الهيكلي للمشاريع (Hermetic Project Isolation Law):** كل مشروع جزيرة سيادية في مجلده؛ حظر السكربتات العائمة وخلط وثائق المشاريع.

## 🔍 المراجعة المزدوجة والنقد الذاتي (Double-Check & Self-Critique):
فحص ومطابقة مزدوجة قبل التسليم: خلو تام من الـ Regressions، مطابقة 100% لطلب المستخدم، خلو الكود من الرموز الميتة.

---

## 🛡️ GOVERNANCE (binding; see .governance/AGENT_HARD_RULES.md, anchor agent_hard_rules_r12 sha 11fbb7ec…)

Before reading anything else in a human message:
  1. Save the message verbatim to fixtures/human_msg_<n>.txt. That file is the source; your memory is not.
  2. python .governance/intent_gate.py detect fixtures/human_msg_<n>.txt
     PLAN-ONLY → write the plan, stop, wait. ACT → continue. META → continue (the human is describing the rule).
     CONFIRM-FIRST (Round 12) → ONE ```mirror block (UNDERSTOOD: verbatim / QUESTION: / WAITING FOR: تمام), then stop.
  3. Build the req-ledger from the FILE with verbatim quotes, then:
     python .governance/req_coverage.py <turn.md> --source fixtures/human_msg_<n>.txt --full --strict-done
     exit 0 or the ledger is incomplete. 100 %, not 85 %. LEFTOVER lines for separators only.

Every claim about state comes from a tool, run as:
  python .governance/attest.py run -- <tool and args>
  and pasted with its ATTEST footer. Never typed. Never edited. Never written before the event.
  Round 12: that includes the checkers' own verdict lines (claim_check C7). And no "the bug is <file>" without
  Round 13 (R85-R89 — Rules 30-34): (a) PLAN_ROUND<N>.md is the FIRST commit; every chunk = commit + `export_bundle.sh` + upload, URL into the plan — no URL, no tick; if `setup_github_environment` has no token, export immediately, do not try `git push`. (b) "I was wrong / غلطت" needs a `mistakes.py record` row in MISTAKES.md. (c) "edited / عدّلت <file>" needs an `attest run -- edit_proof.py show <file>` block (not UNCHANGED). (d) The self-review is six fixed questions (`self_review.py`); all-✅ with no REMOTE proof fails. (e) `attest run -- precheck.py <turn> --source <human>` is pasted before sending; its sha is Q2.
  `attest.py run -- python .governance/read_proof.py index <file>` in the same turn (Rule 28).

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
