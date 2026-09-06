---
name: 00-telegram-ux-guardian
description: حارس تجربة مستخدم بوتات التليجرام (Telegram UX & Notification Guardian) — يضمن نظافة الرسائل، إخفاء الإشعارات المزعجة، تقطيع الردود الطويلة، وعزل الثريدات.
---

# 🤖 مهارة حارس تجربة مستخدم التليجرام (00-telegram-ux-guardian)

> **Description:**  
> حارس تجربة مستخدم بوتات التليجرام التفاعلية — يضمن نظافة الرسائل، كتم الإشعارات التقنية المزعجة وسياسات الأرشيفات، التقطيع الذكي للردود الطويلة قبل حد الـ 4096 حرف، عزل عمليات التوليد في ثريدات مستقلة لمنع تجميد حلقة الـ Polling، والتصريح الإلزامي بالمهارات المستخدمة في النقد الذاتي.

---

## 🎯 مبادئ المهارة الأساسية (Core Principles):

### 1. 🔇 مبدأ كتم الإشعارات الزائدة (Zero-Noise Policy):
* أي تفاصيل تقنية داخلية (مثل مسارات الملفات المحلية، سياسات الأرشيفات D-002، أو أخطاء التراجع المؤقتة) **لا يجب** أن تُرسل كرسالة مستقلة للمستخدم على التليجرام.
* يتم تسجيلها فقط في الـ `log_event` بالـ Terminal أو ملف اللوج المحلي `bridge_bot.log`.

### 2. ✂️ التقطيع الذكي للرسائل (Smart Chunking):
* حد رسائل التيليجرام هو **4096 حرف**.
* إذا تجاوز الرد الحد المسموح، يجب تقطيعه بناءً على الفواصل المنطقية (مثل الفقرات `\n\n` أو فواصل الأكواد ```) وليس في منتصف الكلمة.

### 3. 🧵 عزل المعالجة التزامنية (Asynchronous Thread Isolation):
* حلقة الـ Long-Polling (`getUpdates`) يجب ألا تُحظر أبداً بأي عملية توليد طويلة.
* يتم تمرير كل تحديث إلى `ThreadPoolExecutor` مستقل فوراً وحفظ الـ `update_id` لمنع تكرار معالجة الرسائل.

### 4. 🎛️ الأزرار التفاعلية الديناميكية (Dynamic Keyboards):
* يجب توليد أزرار الموديلات والإعدادات ديناميكياً من مصفوفات البيانات (`AVAILABLE_MODELS`) لضمان عدم الحاجة لتعديل يدوي في الـ UI عند إضافة ميزات جديدة.

### 5. 🔍 التوثيق والنقد الذاتي للمهارات (Mandatory Skills Self-Critique):
* **إلزامي:** في نهاية أي رد يحتوي على كود أو فحص، يجب على الـ AI أن يذكر صراحة قائمة المهارات الهندسية التي استخدمها (لا تقل عن 6 إلى 8 مهارات) ويوضح كيف ساهمت كل مهارة في إنجاز المهمة وخلوها من الأخطاء.

### 6. 🔒 حوكمة ترحيل الردود (Governance Relay — Round 11):
* **إلزامي:** Delivery/relay of a governance turn requires: `attest verify --live` exit 0 AND `claim_check` exit 0 on the exact text being delivered. Relaying a turn strips code fences; `attest.py` handles unfenced footers (R78), but the ATTEST lines themselves must survive the relay byte-for-byte.
* **إلزامي (Round 12):** Round 12 (R81/R83/R84 — Rules 27-29): (a) `intent_gate.py detect` → **CONFIRM-FIRST** ⇒ the turn is ONE ```mirror block (UNDERSTOOD: verbatim quotes · QUESTION: · WAITING FOR: تمام), zero tool calls/edits/plans. (b) No "the bug is / السبب / الخطأ في" about a file without a live `attest run -- read_proof.py index <file>` block in the same turn; `read_proof.py check <turn>` exit 0. (c) Never type a checker verdict line — `claim_check` C7 fails the turn; verdicts are pasted from `attest run`, footer included.

---

## 📋 Checklist الفحص الإلزامي:
- [ ] هل تم فحص دالة `describe_archive_delivery` للتأكد من عدم إرسال إشعارات مسارات محلية؟
- [ ] هل يتم حفظ الـ `offset` فور استلام الرسالة؟
- [ ] هل توكن البوت محمي في ملف خارجي أو متغير بيئة؟
- [ ] هل تم فحص الـ Syntax بـ `python -m py_compile`؟
- [ ] هل تعمل الأزرار التفاعلية بنظام الـ Callback Data الآمن؟
- [ ] هل تم تضمين كتلة النقد الذاتي للمهارات المستخدمة في نهاية الرد؟
- [ ] هل اجتاز النص المرحل فحوصات `attest verify --live` و `claim_check`؟
