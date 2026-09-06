---
name: 0- نظام التخطيط
description: أدوات التخطيط الاحترافي — templates + tracker
---



# === PLANNING_TEMPLATES.md ===

## 🛡️ INTENT GATE (Binding Planning Rule — Round 11)

```
Run intent_gate.py detect on the saved message before any search, fetch, edit or plan expansion.
PLAN-ONLY: output ONLY (a) UNDERSTOOD: <verbatim quote of each sentence> (b) PLAN: numbered steps
(c) "Waiting for go." No tool calls beyond the gate itself. No "while waiting I also…".
Triggers (from code, not memory): "قبل ما تنفذ قولي", "ها تعمل اي", "شوف كده نرفع اي", "اعرف هل هو فاهم",
and the full list in intent_gate.py TRIGGERS. META means the human is quoting the rule, not invoking it.
CONFIRM-FIRST (Round 12, Rule 27): "قبل ما تبحث … تتاكد انك فاهم … مش تخمن" or ≥2 ambiguity admissions →
Round 13 (R85-R89 — Rules 30-34): (a) PLAN_ROUND<N>.md is the FIRST commit; every chunk = commit + `export_bundle.sh` + upload, URL into the plan — no URL, no tick; if `setup_github_environment` has no token, export immediately, do not try `git push`. (b) "I was wrong / غلطت" needs a `mistakes.py record` row in MISTAKES.md. (c) "edited / عدّلت <file>" needs an `attest run -- edit_proof.py show <file>` block (not UNCHANGED). (d) The self-review is six fixed questions (`self_review.py`); all-✅ with no REMOTE proof fails. (e) `attest run -- precheck.py <turn> --source <human>` is pasted before sending; its sha is Q2. Round 14 (R90-R94 — Rules 35-37): (f) FIRST attested block of every turn is `state_gate.py open`, LAST is `state_gate.py close --write` (ai_state.json rewritten by the tool; precheck step 0; pre-commit refuses code without state). (g) A rule broken twice needs a `<n>-ESC` row (`mistakes.py recurrence`). (h) Edits with a line range are proven by `edit_proof.py show <file> --scope A-B` (OUT-OF-SCOPE ⇒ exit 1). (i) `mock_scan.py --staged` blocks TODO / stub / placeholder / constant-return code in pre-commit and CI. (j) No auto-merge script exists; owner pushes `-f` from the export and merges manually after CI + 300 s floor.
output ONLY a ```mirror block (UNDERSTOOD: verbatim quotes → your reading / QUESTION: / WAITING FOR: تمام).
No plan, no tasks, no search. META framing does NOT neutralise CONFIRM-FIRST triggers.
```

---

# 📋 Project Type Templates — قوالب جاهزة

> **اختار القالب المناسب، انسخه، وابعته مع البرومبت الرئيسي.**
> القوالب دي بتوفر عليك وقت كتير في أول كل مشروع.

---

## 1️⃣ بوت / سكريبت تلقائي

```
📌 النوع: بوت / سكريبت Python
📌 الهدف: [مثلاً: تسجيل حسابات / مراقبة / automation]
📌 التقنية: Python + [curl_cffi / SeleniumBase / requests]
📌 الموارد:
  - RAM: [...] MB
  - Storage: [...] GB
  - Can it run 24/7? [Yes/No]
📌 المواقع المستهدفة: [...]
📌 Authentication: [API Key / Cookie / Browser]
📌 Anti-Bot Protection: [Cloudflare / reCAPTCHA / None / Unknown]
📌 Email Provider: [emailnator / tempmail / mailtm / own emails]
📌 الكمية: [X حساب / يوم | X request / ساعة]
📌 أهم حاجة: [سرعة / موثوقية / سهولة صيانة]
```

---

## 2️⃣ موقع ويب / Web App

```
📌 النوع: موقع ويب
📌 الهدف: [مثلاً: e-commerce / portfolio / dashboard / SaaS]
📌 المستخدمين المتوقعين: [X/شهر]
📌 التقنية: [غير متأكد / React / Next.js / Vue / Plain HTML]
📌 Backend: [Python/FastAPI / Node.js / PHP / لا يوجد]
📌 Database: [PostgreSQL / MongoDB / MySQL / SQLite / لا يوجد]
📌 Auth: [Email/Pass / Google / GitHub / لا يوجد]
📌 Hosting: [VPS / Shared / Serverless / Vercel / Fly.io]
📌 Budget: [مجاناً / $5-20/شهر / أكتر]
📌 Mobile-friendly: [ضروري / مش مهم]
📌 أهم حاجة: [جمال التصميم / سرعة / SEO / سهولة التطوير]
```

---

## 3️⃣ API / Backend Service

```
📌 النوع: API / Microservice
📌 الهدف: [مثلاً: REST API / Webhook / Integration]
📌 التقنية: [FastAPI / Flask / Express / Spring]
📌 Clients: [Frontend فقط / Mobile / Other services]
📌 Auth: [API Key / JWT / OAuth2 / Session]
📌 Database: [...]
📌 Rate Limiting: [مطلوب؟]
📌 Performance: [X requests/sec]
📌 Deployment: [Docker / Serverless / VPS]
📌 Documentation: [Swagger / Postman / لا يوجد]
📌 Testing: [Unit Tests / Integration / لا]
```

---

## 4️⃣ AI Provider Integration (AI_PROVIDERS)

```
📌 النوع: AI Provider جديد
📌 اسم الـ Provider: [...]
📌 الموقع: [...]
📌 Auth Type: [API Key / Cookie-based / Browser]
📌 Anti-Bot: [Cloudflare / CAPTCHA / None]
📌 الـ Endpoint: [معروف / محتاج Reverse Engineering]
📌 المميزات: [Chat / Image / Code / Voice]
📌 Free Tier: [كم طلب / يوم؟]
📌 Email للتسجيل: [Gmail / Temp / Any]
📌 تشابه مع: [provider شبيه عندنا = ...]
📌 الهدف من الإضافة: [استخدام مباشر / Registration فقط / Rotation]
```

---

## 5️⃣ نظام متكامل (Full Stack)

```
📌 النوع: نظام كامل (Full Stack)
📌 المشكلة اللي بيحلها: [...]
📌 المستخدمين: [من هم؟ كمية؟]
📌 الـ Core Features:
  1. [Feature 1]
  2. [Feature 2]
  3. [Feature 3]
📌 الـ Nice-to-have:
  - [Feature X]
📌 Database: [...]
📌 Frontend: [...]
📌 Backend: [...]
📌 Infrastructure: [...]
📌 Budget/Resources: [...]
📌 Timeline: [...]
📌 Team Size: [وحدك / X أشخاص]
📌 Experience Level: [مبتدئ / متوسط / متقدم]
```


# === PLANNING_TRACKER.md ===

# 📊 PLANNING TRACKER — V4
# ADR + Pre-mortem + RICE + Google Metrics + Amazon PR/FAQ

> **انسخ لكل مشروع. حدّثه بعد كل محادثة. الصقه في أي AI للاستمرار.**

---

## 📰 Amazon Working Backwards — PR/FAQ

```
العنوان: [...]
الفئة المستهدفة: [...]
المشكلة: [...]
الحل: [...]
النتيجة: [...]
اقتباس افتراضي: "[...]"

FAQ:
Q1: [أصعب سؤال تقني؟] → A: [...]
Q2: [التكلفة/الوقت؟] → A: [...]
Q3: [المخاطرة الأكبر؟] → A: [...]
```

---

## 🎯 Scope Definition

```
✅ Goals:
• G1: [...]
• G2: [...]

❌ Non-Goals (خارج الـ scope — عمداً):
• NG1: [...] — السبب: [...]
• NG2: [...] — السبب: [...]
```

---

## 📊 Key Metrics for Success

| الميتريك | Target | طريقة القياس | الحالة |
|---------|--------|-------------|--------|
| [M1] | [X] | [إزاي] | ⏳ |
| [M2] | [Y] | [إزاي] | ⏳ |
| Counter-metric | لا نتجاوز [Z] | [إزاي] | ⏳ |

---

## ❓ Open Questions

| # | السؤال | المالك | ETA | الحالة |
|---|--------|--------|-----|--------|
| OQ1 | [...] | [...] | [...] | 🔴 مفتوح |
| OQ2 | [...] | [...] | [...] | 🟡 جار |

---

## 📊 RICE Scoring

```
RICE = (Reach × Impact × Confidence%) ÷ Effort

┌──────────────┬───────┬───────┬────────┬────────┬──────────┐
│ ADR/Feature  │Reach  │Impact │Confid. │Effort  │RICE Score│
├──────────────┼───────┼───────┼────────┼────────┼──────────┤
│ ADR-01       │       │       │   %    │        │          │
│ ADR-02       │       │       │   %    │        │          │
└──────────────┴───────┴───────┴────────┴────────┴──────────┘
Priority Order: 1st=[ADR-X] | 2nd=[ADR-Y] | 3rd=[ADR-Z]
```

---

## 📋 ADR Log

### ADR-01: [عنوان]

```
Status: [Proposed/Accepted/Superseded/Deprecated]
RICE: [score]
Context: [...]
Decision: [...]
  MUST: [...] | SHOULD: [...] | MUST NOT: [...]
Rationale: [...]
Consequences: ✅[...] ❌[...] ⚠️[...]
Metric Impact: [M1: +X% / —]
Superseded By: [ADR-X / —]
```

### ADR-02: [عنوان]
[نفس الهيكل]

---

## ⚡ Risk Matrix

```
┌─────────────────┬──────────┬──────────┬───────────┐
│ ADR             │Likelihood│  Impact  │Risk Level │
├─────────────────┼──────────┼──────────┼───────────┤
│ ADR-01          │    L     │    M     │    🟢     │
│ ADR-02          │    M     │    H     │    🔴     │
├─────────────────┼──────────┼──────────┼───────────┤
│ Overall         │          │          │    🟡     │
└─────────────────┴──────────┴──────────┴───────────┘
```

---

## 💀 Pre-mortem

```
"تخيل الفشل بعد 3 شهور"

1. [السبب] | ADR يحميه: [X/—] | الوقاية: [...]
2. [السبب] | ADR يحميه: [Y/—] | الوقاية: [...]
3. [السبب] | ADR يحميه: [Z/—] | الوقاية: [...]

Pre-mortem Score: [X/3]
```

---

## 📁 سجل المحادثات

| # | AI Tool | الموضوع | ADRs | آخر ADR |
|---|---------|---------|------|---------|
| 1 | [...] | [...] | 01-03 | ADR-03 |

---

## ✅ Execution Gates

```
Gate 1: [ ] PR/FAQ مكتوبة وواضحة
Gate 2: [ ] كل ADRs Critical → Accepted
Gate 3: [ ] Pre-mortem Score ≥ 2/3
Gate 4: [ ] Non-Goals محددة
Gate 5: [ ] Overall Risk 🟢 أو 🟡
Gate 6: [ ] موافقة "ابدأ التنفيذ"

Planning Quality: [X/10]
Top RICE: ADR-[X] = [score]
```

---

## 🚀 نسخة لـ AI التالي

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
من PLANNING_TRACKER V4:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
المشروع: [...]
PR/FAQ: "[عنوان] — [الحل المختصر]"
Goals: [...] | Non-Goals: [...]
Key Metrics: M1=[target] M2=[target]
RICE Top: ADR-[X]=[score]

ADR Log:
ADR-01: [عنوان] → Accepted | RICE=[X]
ADR-02: [عنوان] → Superseded → ADR-03

Pre-mortem: [X/3] | Risk: 🟡
آخر سؤال: رقم [X]
الطلب الجديد: [...]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
