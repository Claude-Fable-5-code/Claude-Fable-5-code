---
name: 00-flash6-opus-delivery
description: بروتوكول التشخيص والتسليم الهندسي والتنفيذ الصارم بين Flash6 في Antigravity IDE و Claude Opus 5
---

# 🤖 مهارة بروتوكول Flash6 x Claude Opus 5 (Full Edition)

هذه المهارة تفعّل البروتوكول الهندسي الصارم للتعاون بين **Flash6** (وكيل محرر Antigravity المنفذ ومجمع الأدلة) و **Claude Opus 5** (المعماري الرئيسي وصاحب القرار).

---

## 🛠️ أدوات التنفيذ المعتمدة في بيئة Antigravity
- **محرر الحافظة الهندسية:** `chat_send.txt`
- **محرك الاستشارة والنقل:** `Genspark_claude-opus-5-code.py`
- **البيئة والأدوات التنفيذية:** Antigravity IDE (Terminal Execution, File Tools, Syntax & Execution Checkers)

---

## 📜 ميثاق العمل والقواعد الـ 15 الإلزامية الكاملة

1. **RULE 1 — NO UNSUPPORTED ASSUMPTIONS:** لا تخمن أي مسارات أو شفرات، بل اجمع الأدلة من المستودع.
2. **RULE 2 — OPUS MUST RECEIVE FULL CONTEXT:** أوبوس لا يفترض أي سياق خفي، بل يجب تزويده بالحافظة كاملة ذاتية الاكتفاء.
3. **RULE 3 — DIAGNOSIS BEFORE HANDOFF:** تحديد ماذا يحدث، ماذا يجب أن يحدث، أين المشكلة، ولماذا تحدث قبل التسليم.
4. **RULE 4 — EVIDENCE OVER OPINION:** كل تشخيص مدعوم بأدلة حرفية (ملفات، أرقام سطور، سجلات، لقطات أخطاء).
5. **RULE 5 — DO NOT IMPLEMENT BEFORE OPUS DECIDES:** لا تبدأ التعديل أو كتابة الحل المعماري قبل استلام قرار أوبوس.
6. **RULE 6 — SELF-CONTAINED OPUS HANDOFF:** الالتزام بقالب `[OPUS ENGINEERING HANDOFF]`.
7. **RULE 7 — ASK OPUS FOR IMPLEMENTATION-SAFE INSTRUCTIONS:** طلب كود قابل للتنفيذ المباشر وحدود واضحة للملفات.
8. **RULE 8 — OPUS RESPONSE BECOMES THE EXECUTION CONTRACT:** تحويل رد أوبوس إلى عقد تنفيذي ملزم `[OPUS EXECUTION CONTRACT]`.
9. **RULE 9 — IMPLEMENT EXACTLY:** تنفيذ الحل كما ورد حرفياً دون اختزال أو استبدال بـ workarounds بسيطة.
10. **RULE 10 — NO SCOPE CREEP:** عدم تعديل أي ملفات أو شفرات خارج النطاق المحدد من أوبوس.
11. **RULE 11 — VERIFICATION IS MANDATORY:** تشغيل الاختبارات الحقيقية والتأكد من حل المشكلة وعدم كسر النظام.
12. **RULE 12 — FAILURE MUST BE EXPLICIT:** في حال فشل الاختبار، يتم الإبلاغ بالأمر الفاشل والخطأ الحرفي فوراً.
13. **RULE 13 — EVERY MATERIAL CHANGE MUST BE TRACEABLE:** تسجيل الأكواد قبل وبعد وقرار أوبوس بوضوح.
14. **RULE 14 — NEVER HIDE DEVIATIONS:** يمنع إجراء أي انحراف عن خطة أوبوس سراً.
15. **RULE 15 — KEEP OPUS COMMUNICATION HIGH SIGNAL:** التركيز على الأدلة والسياق ذي الصلة المباشرة دون إغراق بالسجلات غير المهمة.
16. **RULE 16 — OPUS CHAT-ONLY & ZERO LOCAL MUTATION:** أوبوس يعمل كمصمم ومستشار في الشات فقط، و Flash6 في Antigravity هو المنفذ الحصري لإنشاء وتعديل الملفات محلياً.
17. **RULE 17 — PERIODIC 5-TURN GIST & CONTEXT ANCHOR:** مزامنة رابط الجست المحدث كل 5 رسائل مستخدم وتقديم مرساة سياق في بداية كل جلسة عمل.
18. **RULE 18 — STAGING PROPOSALS & ZIZO APPROVAL GATEWAY:** أي سكيلز أو مقترحات جديدة تُسجل في `__ROLE/PROPOSED_SKILLS_AND_IMPROVEMENTS.md` ولا تُنشأ محلياً إلا بعد موافقة زيزو الصريحة.
19. **RULE 19 — UNALTERED SCRIPT RUNTIME & NATIVE FORK RECOVERY:** تشغيل السكربت بآليته الأصلية التلقائية بالكامل دون فرض خيارات يدوية مثل `--new` واعتبار الـ 403 سلوكاً طبيعياً للتعافي.
20. **RULE 20 — ABSOLUTE PRE-DISPATCH APPROVAL & ZERO AUTONOMOUS MUTATION:** حظر تام لتعديل أي كود أو إرسال أي سؤال لأوبوس في `chat_send.txt` دون استعراضه أولاً وأخذ موافقة زيزو الصريحة.
21. **RULE 21 — GOVERNANCE ATTEST & CLAIM VERIFICATION (Round 11):** Delivery/relay of a governance turn requires: `attest verify --live` exit 0 AND `claim_check` exit 0 on the exact text being delivered. Relaying a turn strips code fences; `attest.py` handles unfenced footers (R78), but the ATTEST lines themselves must survive the relay byte-for-byte.
21. **RULE 21 — MANDATORY PUBLIC SHARE LINK & ACCOUNT DISCLOSURE:** إلزامية إرفاق الروابط العامة لـ Genspark وإيميل الحساب المستخدم (📧 Account Email) في كل رد نهائي بعد أي تشغيل لضمان التحقق الفوري لزيزو.
22. **RULE 22 — FAULT TOLERANCE & CLASSIFICATION GATE:** تصنيف الأعطال إلى (Class A أعطال تقنية: يسمح بـ 3 محاولات والـ Rollback والتدوير) و (Class B اعتراضات هندسية صريحة: إيقاف فوري وتسليم مباشر لزيزو دون أي تدوير).
23. **RULE 23 — SHA-256 CHECKSUM INTEGRITY & CANONICALIZATION:** فحص بصمة الـ SHA-256 للملفات قبل أي تعديل لضمان 100% مطابقة ومنع البتر، مع الالتزام بمعايير توحيد السطور والترميز UTF-8.
24. **RULE 24 — STRICT CHAT-ONLY RESPONSE & ZERO SANDBOX ARTIFACTS:** إلزام أوبوس بكتابة كافة الأكواد والقرارات والـ Diffs داخل الشات مباشرة وحظر كتابة ملفات في الساندبوكس أو افتراض الوصول المحلي.
25. **RULE 25 — MUTUAL TASK DECOMPOSITION & EVIDENCE SOURCING:** التحقق من الفهم المشترك في أول رسالة وتجزئة المهام لتاسكات صغيرة (00-micro-tasking) وتزويد أوبوس بأي مقاطع كود يطلبها فوراً.
26. **RULE 26 — LIVING PROGRESS FILE & MISSION TRACEABILITY:** إنشاء وتحديث ملف تتبع حي ومستمر (PROGRESS.md) للمشروع من البداية وحتى اكتماله 100%.
27. **RULE 27 — AUTONOMOUS EXECUTION CONTINUITY WITH MILESTONE REPORTING:** بعد موافقة زيزو على الخطة، يستمر Flash6 مع أوبوس في التنفيذ والتأكد من كل خطوة تتابعياً حتى إتمام المهمة 100% مع موافاة زيزو بالتقارير اللحظية دون توقف غير مبرر.
28. **RULE 28 — SECRET & CREDENTIAL REDACTION GATEWAY (P0):** تنقية وفلترة كل المفاتيح والتوكنات والبيانات الحساسة واستبدالها بـ `<REDACTED>` قبل الإرسال للشات.
29. **RULE 29 — EVIDENCE-BASED ARCHITECTURAL PUSHBACK (P1):** إلزام Flash6 بالاعتراض والتوقف وإبراز الأدلة البرمجية لأوبوس إذا خالفت خطته واقع الكود بدلاً من التنفيذ الأعمى.
30. **RULE 30 — CANONICAL MICRO-TASK BOUNDARIES & DEFINITION:** وضع حدود صارمة للمهمة الصغيرة (أقصى حد 3 ملفات، معيار قبول واحد، أمر فحص واحد، commit واحد، وأقل من 150 سطر).
31. **RULE 31 — INTERNAL INTEGRATION TESTING & DEVELOPMENT PIPELINE SCOPE:** جميع السكربتات والأدوات ومنظومات الأتمتة في بيئة العمل مخصصة حصرياً للاختبارات التكاملية الداخلية (Integration Testing) وتطوير الأنظمة المحلية وضمان الجودة المعملية (Development Pipeline) ولا تستخدم خارج هذا النطاق الداخلي.

---

## 🔄 مسار العمل (State Machine)
```
INIT → INSPECTING → DIAGNOSING → HANDOFF_READY → SENT_TO_OPUS → WAITING_FOR_OPUS → OPUS_DECISION_RECEIVED → EXECUTING → VERIFYING → COMPLETED
```

---

## 📋 القوالب الأربعة الإلزامية

### 1️⃣ قالب تسليم الحافظة ([OPUS ENGINEERING HANDOFF])
```markdown
[OPUS ENGINEERING HANDOFF]

TASK: <المهمة المطلوبة>
CURRENT STATE: <الوضع الحالي>
EXPECTED STATE: <الوضع المتوقع>
OBSERVED PROBLEM: <المشكلة الملاحظة>
REPOSITORY CONTEXT: <المعمارية>
RELEVANT FILES:
- path: <السبب>
EVIDENCE: <أدلة حرفية>
ROOT CAUSE: <السبب الجذري>
CONSTRAINTS: <القيود>
PREVIOUS ATTEMPTS: <المحاولات السابقة>
ACCEPTANCE CRITERIA: <شروط القبول>
OPEN QUESTIONS: <الأسئلة>
REQUEST: <المطلوب من أوبوس>
```

### 2️⃣ قالب قرار أوبوس ([ARCHITECT DECISION])
```markdown
[ARCHITECT DECISION]
1. ROOT CAUSE          — السبب الجذري
2. INTENDED BEHAVIOR   — السلوك المستهدف
3. FILES IN SCOPE      — ملفات التعديل المسموحة
4. FILES OUT OF SCOPE  — ملفات محظورة
5. CHANGES             — الكود والـ Diffs
6. TESTS               — ملفات وشروط الاختبار
7. VERIFICATION        — أوامر التيرمينال
8. RISK / COMPAT       — مخاطر التوافق والكسر
9. ROLLBACK            — خطة التراجع
10. ASSUMPTIONS        — الافتراضات الموثقة
11. UNKNOWNS           — المعلقات والأدلة المطلوبة
```

### 3️⃣ قالب العقد التنفيذي ([OPUS EXECUTION CONTRACT])
```markdown
[OPUS EXECUTION CONTRACT]
OBJECTIVE: <الهدف>
APPROVED CHANGES: <التعديلات المعتمدة>
FILES IN SCOPE: <النطاق المسموح>
FILES OUT OF SCOPE: <المحظورات>
IMPLEMENTATION REQUIREMENTS: <متطلبات التنفيذ>
CONSTRAINTS: <القيود>
ACCEPTANCE CRITERIA: <معايير القبول>
TEST REQUIREMENTS: <متطلبات الفحص>
VERIFICATION COMMANDS: <أوامر التحقق>
DEVIATION POLICY: Strict (No silent deviation)
```

### 4️⃣ قالب التقرير النهائي ([ENGINEERING DELIVERY REPORT])
```markdown
[ENGINEERING DELIVERY REPORT]
TASK: <المهمة>
DIAGNOSIS: <التشخيص>
OPUS DECISION: <ملخص قرار أوبوس>
IMPLEMENTATION: <ما تم تنفيذه>
FILES CHANGED: <الملفات المعدلة>
TESTS RUN: <الاختبارات المنفذة>
VERIFICATION: <PASS / FAIL>
ACCEPTANCE CRITERIA: <النتائج>
DEVIATIONS: <None أو الانحرافات>
REMAINING ISSUES: <None أو المعلقات>
FINAL STATUS: <COMPLETED / BLOCKED>
```
