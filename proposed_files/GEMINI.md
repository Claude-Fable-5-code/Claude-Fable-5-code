@.agents/rules/00-bolla-constitution.md
@.agents/rules/00-core-authority.md
@.agents/rules/20-governance-security.md
@.agents/rules/30-golden-master.md
@.agents/rules/90-glossary-limits.md

# 🤖 GEMINI.md — قواعد مشروع AI_MDULE (v1.2)

> **📌 اقرأ الملف ده قبل ما تلمس أي سطر في المشروع.**
> بيخليك تفهم المشروع وتشتغل صح من أول لحظة.

---

## 🗣️ اللغة والأسلوب

- **كلمني بالمصري دايماً** — مش فصحى
- **استخدم Emojis** عشان الوضوح
- **مختصر ومباشر** — بلاش حشو
- **كود → code blocks** مع اسم اللغة دايماً

---

## 🏗️ المشروع — AI Orchestration System

### الـ Stack:
| الطبقة | التقنية |
|--------|---------|
| **API** | FastAPI (`api/app.py`) |
| **Providers** | OpenAI, Gemini, Together, Anthropic, Groq + DeepSeek Browser |
| **Vector DB** | Qdrant (`localhost:6333`) |
| **Embedding** | `paraphrase-multilingual-mpnet-base-v2` (local) |
| **Task Queue** | Celery + Redis |
| **Config** | `.env` + `config/settings.py` |
| **Browser Automation** | SeleniumBase (`uc=True`) |

### الـ Flow:
```
Query → classify domain → RAG retrieve → Provider generate → log + feedback
```

---

## ⚙️ Provider Pattern — إلزامي

### كل provider لازم:
1. يورث من `BaseProvider` في `providers/base.py`
2. يرجع `ProviderResponse` (مش string!)
3. ينفذ دوال `ask` و `generate` وبحث اختياري
4. يتسجل في `providers/manager.py`

---

## 🔒 قواعد إلزامية — Non-Negotiable

### ⛔ ممنوع:
- **مسح أي ملف** أو استبداله كامل — تعديل بس
- **Hardcoded Keys** — كلها في بيئة التشغيل المعزولة
- **تعديل الحوكمة والأمان** بدون طلب صريح
- **كسر Provider Interface** — عقد ثابت غير قابل للتغيير
- **تعديل أو لمس أي كود تنفيذي دون وثيقة مواصفات مسبقة مسجلة كـ Pre-edit وموافقة GO صريحة** (قانون 9)
- **وضع سكربتات كود عائمة في الروت العام أو خلط وثائق المشاريع ببعضها** (قانون 10)

### ✅ إلزامي:
- **Git Commit قبل أي تعديل كبير**
- **DRY تماماً** — صفر تكرار
- **كل إعداد جديد في** `config/settings.py` و `.env.example`
- **try/except لكل تفاعل مع الـ DOM**
- **الـ README.md = سجل حي** — أضف بس، لا تمسح
- **تحديث كوبري التسليم والاستئناف HANDOFF.md وإصدار التقرير الختامي عند إغلاق كل مرحلة** (قانون 9)
- **عزل كل مشروع داخل مجلده المستقل وتسكين توثيقه ومواصفاته بداخله** (قانون 10)

### 📜 قانون الإسناد المرجعي الصريح بالسطور (Verbatim Ground-Truth Citation) — إلزامي:
- **لا كلام ولا تعديل بدون دليل حرفي بالسطور من المرجع الأساسي**:
  - **للشبكة والـ APIs:** إرفاق كتلة الـ HAR المرجعية بالسطور المحددة التي تثبت الرابط (URL)، الهيدرز، الـ Payload، وشكل الاستجابة قبل أي تعديل أو إنشاء.
  - **للكود والمنطق في أي مشروع:** إرفاق أسطر الكود المرجعي الأصلي أو التوثيق الرسمي كما هي بالتحديد مع أرقام السطور.
  - **ممنوع التخمين أو الكلام الإنشائي:** أي ادعاء فني أو مقترح تعديل لا يحمل دليله الحرفي من المرجع الأساسي يُعتبر باطلاً ومرفوضاً تماماً.

---

## 📁 خريطة الملفات المهمة

| الملف/المجلد | الوظيفة |
|-------------|---------|
| `api/app.py` | FastAPI entry point |
| `orchestrator/` | منطق التنسيق بين الطبقات |
| `providers/base.py` | ⚠️ الـ BaseProvider — لا تعدله |
| `providers/manager.py` | إدارة الـ providers + fallback |
| `config/settings.py` | كل الإعدادات المركزية |
| `embedding/` | Qdrant + sentence-transformers |
| `ingestion/` | Pipeline للـ PDF/CSV/URL/OCR |
| `tests/` | حزم الاختبارات التوصيفية الثابتة |
| `__ROLE/` | سجلات المتابعة والتقدم وتتبع المهام |

---

## 🚀 تشغيل المشروع

- استخدام الحاويات: `docker-compose up -d`
- التشغيل المحلي: `uvicorn api.app:app --host 0.0.0.0 --port 8000`

---

## 🔍 النقد الذاتي — إلزامي في كل مهمة

```
🔍 نقد ذاتي:
1. ❌/✅ هل في dead code اتسابت؟
2. ❌/✅ هل في selectors/variables معرّفة ومش بتتستخدم؟
3. ❌/✅ هل كان ممكن أوصل للحل بخطوات أقل؟
4. ❌/✅ هل في تكرار (DRY violation)؟
5. ❌/✅ هل نسيت git commit أو تحديث السجل؟
6. ❌/✅ هل قمت باختبار الكود فعلياً (Execution Test) وتأكدت من خلوه من الأخطاء؟
```
