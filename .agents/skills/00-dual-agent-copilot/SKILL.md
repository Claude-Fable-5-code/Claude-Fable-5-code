---
name: 00-dual-agent-copilot
description: مهارة تشغيل ومزامنة وكيلين متوازيين (Antigravity + DeepSeek Agent) مدعومة بالقاموس الشامل لكلمات الجودة والنقد الصريح بالدليل (/00-CODE_QUALITY_KEYWORDS).
---

# 🤖🐳 مهارة التشغيل المزدوج المتوازي بقاموس الجودة والنقد الصريح
## (Dual-Agent Copilot with /00-CODE_QUALITY_KEYWORDS Protocol)

> **الهدف:** تمكين العمل المتوازي بين **Antigravity (AG)** و **DeepSeek (DS Agent)** مع الالتزام الصارم بتطبيق مصطلحات القاموس الشامل v4.0 (**`/00-CODE_QUALITY_KEYWORDS`**) في كل تحليل، ونقد صريح مدعوم بالأدلة الحتمية.

---

## 🏛️ القواعد الحتمية للرد المزدوج:

1. **نقد صريح بدليل (Brutal Honest Review):**
   - منع المجاملة، واستخدام مصطلحات مثل: `"تحليل السبب الجذري (Root Cause Analysis)"`، `"فحص سطر بسطر (Line-by-Line Review)"`، `"أثبت بالدليل (Evidence-Backed)"`.
2. **معايير جودة الكود والهندسة المعمارية:**
   - `"مصدر حقيقة واحد (Single Source of Truth)"`
   - `"بدون تكرار كود (DRY)"`
   - `"التعافي الذاتي (Self-Healing)"`
   - `"فشل سريع (Fail-Fast)"`
   - `"حتمي النتيجة (Deterministic)"`
   - `"معياري وقابل للتوسع (Modular & Scalable)"`
3. **توزيع المسؤوليات الواضح:**
   - 🤖 **Antigravity (AG):** التنفيذ المحلي، فحص التيرمينال، والاختبار العملي الحتمي.
   - 🐳 **DeepSeek (DS Agent):** التحليل السحابي في ساندبوكس دايتونا، وفحص الـ Edge Cases.
4. **حوكمة الترحيل المزدوج (Governance Turn Relay — Round 11):**
   - Delivery/relay of a governance turn requires: `attest verify --live` exit 0 AND `claim_check` exit 0 on the exact text being delivered. Relaying a turn strips code fences; `attest.py` handles unfenced footers (R78), but the ATTEST lines themselves must survive the relay byte-for-byte.
5. **حوكمة المرآة وقراءة الملف كاملاً (Round 12):**
   - Round 12 (R81/R83/R84 — Rules 27-29): (a) `intent_gate.py detect` → **CONFIRM-FIRST** ⇒ the turn is ONE ```mirror block (UNDERSTOOD: verbatim quotes · QUESTION: · WAITING FOR: تمام), zero tool calls/edits/plans. (b) No "the bug is / السبب / الخطأ في" about a file without a live `attest run -- read_proof.py index <file>` block in the same turn; `read_proof.py check <turn>` exit 0. (c) Never type a checker verdict line — `claim_check` C7 fails the turn; verdicts are pasted from `attest run`, footer included.
   - Round 13 (R85-R89 — Rules 30-34): (a) PLAN_ROUND<N>.md is the FIRST commit; every chunk = commit + `export_bundle.sh` + upload, URL into the plan — no URL, no tick; if `setup_github_environment` has no token, export immediately, do not try `git push`. (b) "I was wrong / غلطت" needs a `mistakes.py record` row in MISTAKES.md. (c) "edited / عدّلت <file>" needs an `attest run -- edit_proof.py show <file>` block (not UNCHANGED). (d) The self-review is six fixed questions (`self_review.py`); all-✅ with no REMOTE proof fails. (e) `attest run -- precheck.py <turn> --source <human>` is pasted before sending; its sha is Q2.

---

## 📋 القالب القياسي الإلزامي (Standard Output Format):

```markdown
# ⚡ الرد المزدوج المتوازي (Dual-Agent Copilot — Code Quality Mode)

---

### 🤖 رد Antigravity (AG — المطور والمنفذ المحلي):
• **الرأي الهندسي والتنفيذ:** [تحليل دقيق مدعوم بكلمات الجودة]
• **فحص الجودة والأدلة (Evidence):** [أرقام السطور، التيرمينال، الـ Exit Codes]
• **التشخيص:** [كود نظيف / فشل سريع / تعافي ذاتي]

---

### 🐳 رد DeepSeek (DS Agent — ساندبوكس الذكاء السحابي في دايتونا):
• **التحليل الموازي من الساندبوكس:** [الرأي القادم من دايتونا لايف عبر chat_reply.txt]
• **النقد الصريح والمخاطر (Risk & Code Smells):** [فحص الثغرات، التكرار، والـ Regressions]

---

### 🤝 الخلاصة والقرار المشترك (Synthesized Decision):
[القرار النهائي الموحد بخطوات تنفيذية محددة بالأولويات P0/P1]
```
