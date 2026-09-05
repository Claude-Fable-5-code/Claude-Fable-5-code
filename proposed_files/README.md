# 🤖 AI Orchestration System — AI_MDULE

> نظام AI متكامل بـ Semantic Search + RAG + Multi-Provider + Domain Classification + Feedback Loops + REST API.

## 📌 مراجع سريعة

| الملف | المحتوى |
|-------|---------|
| `GEMINI.md` | قواعد المشروع + SeleniumBase Pattern + بروتوكول "حدث السجل" |
| `UNIVERSAL_AI_PROMPT.md` | برومت كامل للـ AI + Provider Pattern + SeleniumBase Template |
| `README.md` | سجل الإنجازات + المشاكل + الدروس (الملف ده) |
| `.agents/memory/WAF_BOT_DIAGNOSTIC_MASTER_PROMPT.md` | 🛡️ **7,700+ سطر** — مرجع WAF/Bot/403/429 الكامل — إلزامي قبل أي تعديل في headers أو bypass |

> **💡 SeleniumBase Pattern:** موجود في `GEMINI.md` → قسم "🤖 SeleniumBase Pattern — قابل لأي موقع AI"

> **🚨 WAF Rule:** لو شفت 403/429 أو فشل WAF → اقرأ `WAF_BOT_DIAGNOSTIC_MASTER_PROMPT.md` الأول — ممنوع تغيير أي header عشوائياً!

---


---

## 📊 الحالة العامة

<!-- آخر رقم مشكلة مستخدم: #712 -->
 
| البند | القيمة |
|-------|--------|
| الإصدار | v3.6-notegpt-agent-sandbox |
| الحالة | 🟢 v3.6 — NoteGPT Real Agent Sandbox Engine, Parallel Duel Benchmark & Auto Sandbox Exporter Active |
| آخر commit آمن | `latest` |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    FastAPI REST Gateway                       │
│   POST /ai/query │ POST /ai/ingest │ GET /ai/domains │ ...  │
├──────────────────────────────────────────────────────────────┤
│                   Orchestrator Engine                         │
│   classify → decide strategy → retrieve → generate → log    │
├────────────┬─────────────────┬───────────────────────────────┤
│  Domain    │  RAG Pipeline   │   Provider Manager            │
│ Classifier │  (retrieve +    │   (OpenAI, Gemini,            │
│ (2-stage)  │   re-rank)      │    Together, Anthropic,       │
│            │                 │    Groq, DeepSeek Browser)    │
├────────────┴─────────────────┴───────────────────────────────┤
│          Embedding Service  │  Vector Store (Qdrant)         │
├─────────────────────────────┴────────────────────────────────┤
│  Ingestion Pipeline (PDF, OCR, CSV, JSON, URL, Text)         │
│  Celery Workers + Redis Task Queue                           │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Docker (الأسهل):
```bash
cp .env.example .env
# عدّل .env بـ API keys بتاعتك
docker-compose up -d
```

### محلي (بدون Docker):
```bash
pip install -r requirements.txt

# شغّل Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# شغّل Redis
docker run -d -p 6379:6379 redis:7-alpine

# شغّل الـ API
uvicorn api.app:app --host 0.0.0.0 --port 8000

# (اختياري) Celery worker
celery -A ingestion.tasks worker --loglevel=info
```

**الروابط:**
- **API** → `http://localhost:8000`
- **Qdrant** → `http://localhost:6333`

---

## ⚙️ Environment Variables

| Variable | Default | الوصف |
|----------|---------|-------|
| `OPENAI_API_KEY` | — | OpenAI API key |
| `GEMINI_API_KEY` | — | Google Gemini API key |
| `TOGETHER_API_KEY` | — | Together AI API key |
| `ANTHROPIC_API_KEY` | — | Anthropic API key |
| `GROQ_API_KEY` | — | Groq API key |
| `DEEPSEEK_EMAIL` | — | ⚠️ إيميل DeepSeek (Browser) |
| `DEEPSEEK_PASSWORD` | — | ⚠️ باسورد DeepSeek (Browser) |
| `DEFAULT_PROVIDER` | `openai` | الـ Provider الافتراضي |
| `EMBEDDING_PROVIDER` | `local` | `local` أو `openai` |
| `EMBEDDING_MODEL` | `paraphrase-multilingual-mpnet-base-v2` | موديل الـ Embedding |
| `QDRANT_HOST` | `localhost` | Qdrant host |
| `QDRANT_PORT` | `6333` | Qdrant port |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis URL |
| `CHUNK_SIZE` | `512` | أحرف لكل chunk |
| `CHUNK_OVERLAP` | `64` | تداخل بين الـ chunks |
| `CLASSIFICATION_THRESHOLD` | `0.6` | حد التصنيف قبل LLM fallback |
| `LOG_LEVEL` | `INFO` | مستوى الـ logging |

---

## 📡 API Reference

### `POST /ai/query` — سؤال:
```bash
curl -X POST http://localhost:8000/ai/query \
  -H "Content-Type: application/json" \
  -d '{"query": "أفضل عطر رجالي يدوم طويلاً", "style": "balanced", "top_k": 5}'
```

### `POST /ai/ingest` — إضافة بيانات:
```bash
curl -X POST http://localhost:8000/ai/ingest \
  -H "Content-Type: application/json" \
  -d '{"source": "/path/to/file.pdf", "domain": "my_domain"}'
```

### `GET /ai/domains` — عرض الـ domains
### `POST /ai/feedback` — تقييم رد
### `GET /ai/metrics` — إحصائيات
### `GET /health` — Health check

---

## 📂 هيكل المشروع

| الملف/المجلد | الوظيفة |
|-------------|---------|
| `api/app.py` | FastAPI entry point |
| `orchestrator/` | منطق التنسيق بين الطبقات |
| `providers/base.py` | ⚠️ BaseProvider — لا تعدله |
| `providers/manager.py` | إدارة الـ providers + fallback |
| `providers/deepseek_provider.py` | Browser automation provider |
| `config/settings.py` | كل الإعدادات من `.env` |
| `config/domains.yaml` | تعريف الـ domains |
| `embedding/` | Qdrant + sentence-transformers |
| `ingestion/` | Pipeline للـ PDF/CSV/URL/OCR |
| `ديب سيك/deepseek_login.py` | السكربت الأصلي (مرجع) |

---

## 🔒 قواعد الحماية

> **⛔ ممنوع نهائياً:**
> - مسح أي ملف أو استبداله كامل — تعديل بس
> - Hardcoded API keys — كلها في `.env`
> - كسر `ProviderResponse` interface

> **✅ إلزامي قبل أي تعديل كبير:**
> ```bash
> git add -A && git commit -m "📸 Backup"
> ```

---

## 🛡️ قاعدة جدول التغييرات (إلزامية)

> **قبل أي تنفيذ — اطلب جدول:**

| العمود | المعنى |
|--------|--------|
| ✅ اتضاف | ميزة أو كود جديد |
| ✏️ اتعدل | تغيير في حاجة موجودة |
| ❌ اتمسح | أي حاجة اترمت |

> ⛔ **ممنوع تنفيذ أي حاجة فيها خانة "اتمسح" بدون موافقة!**

---

## 🚀 سجل الإنجازات

| 137 | بناء extract_traffic.py لاستخراج وتحليل الـ API Traffic دفعة واحدة من سجلات Burp المعقدة إلى extracted_requests.json. | Redot_Pay_PART_v_15/extract_traffic.py |
| 138 | ربط الـ Architecture بالكامل: `redotpay_api.py` يكلم `redotpay_bypass.js` (Frida RPC) لتشفير الـ Payloads وتوليد التوقيعات. | `Redot_Pay_PART_v_15` |
| 139 | اكتشاف واستخراج الـ Endpoints الخاصة بتسجيل الدخول والـ SMS (uth/verify, mobile/resend, indMobile/exist) بعد تخطي الـ UI Captcha بنجاح في RedotPay. | Redot_Pay_PART_v_15 |
| # | الإنجاز | الملفات |
|---|---------|---------|
| 1 | مراجعة وتحليل ملف `ديب سيك/ريكويست` (API Call لـ DeepSeek) | `ديب سيك/ريكويست` |
| 2 | بناء `deepseek_login.py` بـ SeleniumBase — اشتغل 3 مرات متتالية مع تخطي Cloudflare | `ديب سيك/deepseek_login.py` |
| 3 | إضافة `send_message_and_get_reply()` — إرسال رسالة واستقبال رد | `ديب سيك/deepseek_login.py` |
| 4 | ربط كل الدوال في `run_deepseek_bot()` رئيسية واحدة | `ديب سيك/deepseek_login.py` |
| 5 | إضافة `open_new_chat()` مرنة بـ CSS+XPath fallback | `ديب سيك/deepseek_login.py` |
| 6 | إضافة `wait_for_reply_complete()` ذكية — Button Counting بـ selector دقيق `db183363` (5 أزرار) | `ديب سيك/deepseek_login.py` |
| 7 | إضافة `toggle_search()` و `toggle_deepthink()` مع إعدادات Config | `ديب سيك/deepseek_login.py` |
| 8 | قراءة الرد من `ds-markdown` بدل `dad65929` = رد نظيف بدون "Searching for" | `ديب سيك/deepseek_login.py` |
| 9 | إضافة دوال `ask()` + `generate()` + `get_usage_stats()` في `deepseek_provider.py` | `providers/deepseek_provider.py` |
| 10 | إضافة None-safety: `len(result or "")` في counters | `providers/deepseek_provider.py` |
| 11 | Code Review شامل لـ `deepseek_provider.py` — 6 مشاكل اتكشفت ووُثقت | `providers/deepseek_provider.py` |
| 12 | إنشاء `GEMINI.md` خاص بمشروع AI_MDULE | `GEMINI.md` |
| 13 | إنشاء `VIBE_CODING_PROMPT.md` — دليل شامل من 5 AIs + 9 مصادر | `VIBE_CODING_PROMPT.md` |
| 14 | إنشاء `UNIVERSAL_AI_PROMPT.md` — برومت جاهز لأي AI | `UNIVERSAL_AI_PROMPT.md` |
| 15 | إضافة `DeepSeekSession` — Session Reuse (10x أسرع) | `GEMINI.md`, `UNIVERSAL_AI_PROMPT.md` |
| 16 | إضافة `@dataclass Config` مع `__post_init__` validation | `GEMINI.md`, `VIBE_CODING_PROMPT.md` |
| 17 | توثيق Re-render Guard لحل StaleElement أثناء Streaming | `VIBE_CODING_PROMPT.md`, `GEMINI.md` |
| 18 | مراجعة 5 AIs + استخلاص patterns في VIBE_CODING_PROMPT.md | `ديب سيك/خطوات*` |
| 19 | إنشاء `GEMINI_REFERENCE.md` — خطة أتمتة Gemini 7 مراحل | `providers/GEMINI_REFERENCE.md` |
| 20 | بناء `gemini_login.py` v1.0 — أول دالة Login لـ Google OAuth | `جيميني/gemini_login.py` |
| 21 | اكتشاف Selectors حقيقية من F12: `#identifierId` + `input[name=Passwd]` + `#passwordNext` | `جيميني/gemini_login.py` |
| 22 | مراجعة 4 AIs (ChatGPT+Gemini+Grok+Genspark) → 4 إصلاحات + Bug fix | `جيميني/gemini_login.py` |
| 23 | `gemini_login.py` v1.1 — `clickable` بدل `visible` + fallback selectors + Discovery | `جيميني/gemini_login.py` |
| 24 | إضافة Quality Gate + دروس Gemini لـ VIBE_CODING_PROMPT.md | `VIBE_CODING_PROMPT.md` |
| 25 | `gemini_login.py` v1.2 — Login مباشر `accounts.google.com` + `data-test-id` selectors | `جيميني/gemini_login.py` |
| 26 | `gemini_login.py` v1.3 — بدون sleep ثابت + `MODEL_THINKING/MODEL_PRO` True/False | `جيميني/gemini_login.py` |
| 27 | إضافة `send_message()` — كتابة + إرسال رسالة في Gemini | `جيميني/gemini_login.py` |
| 28 | `gemini_login.py` v1.4 — JS Fast Type + `wait_for_reply()` + `get_reply_text()` | `جيميني/gemini_login.py` |
| 29 | اكتشاف 3 مؤشرات اكتمال الرد: `aria-busy` + `footer.complete` + أزرار | `جيميني/gemini_login.py` |
| 30 | تقسيم الكود لـ 9 دوال منفصلة (login → email → password → navigate → verify → model → send → wait → read) | `جيميني/gemini_login.py` |
| 31 | Fix `get_reply_text()` — JS `innerText` بدل `element.text` + فلتر "Model: ( Gemini )" | `جيميني/gemini_login.py` |
| 32 | إضافة `start_new_chat()` — محادثة جديدة بعد كل رد بـ 2 ثانية | `جيميني/gemini_login.py` |
| 33 | مراجعة 12 AI وتحليل آراء Hybrid Network API vs DOM | `جيميني/فيب كودج 111`, `شلبي توحد ملفات` |
| 34 | `gemini_login.py` v1.6 — Scroll instant + NOISE filter موسّع + Fallback paragraphs | `جيميني/gemini_login.py` |
| 35 | `gemini_login.py` v1.7 — `stream_reply_live()` بث لحظي داخل التيرمنال زي DeepSeek | `جيميني/gemini_login.py` |
| 36 | إضافة `GEMINI_LIVE_STREAM`, `GEMINI_STREAM_POLL_MS`, `GEMINI_AUTO_NEW_CHAT` في Config + .env | `جيميني/gemini_login.py`, `.env` |
| 37 | تصحيح selector زر المحادثة الجديدة من HTML — تاغ `button` لـ `a[aria-label]` | `جيميني/gemini_login.py` |
| 38 | Rollback لـ v1.8 — حذف `stream_reply_live()` لأن Gemini بيدلق الرد كله مرة واحدة (مش حرف بحرف زي DeepSeek) | `جيميني/gemini_login.py` |
| 39 | `gemini_login.py` v2.0 — AI Message Lock: `send_message()` بترجع `initial_count` | `جيميني/gemini_login.py` |
| 40 | `wait_for_reply()` بتفحص `els[-1].aria-busy` بس مش كل الصفحة | `جيميني/gemini_login.py` |
| 41 | `clean_reply_text()` دالة جديدة — regex NOISE prefix + dedup `seen = set()` | `جيميني/gemini_login.py` |
| 42 | `stream_reply_live()` شغال لحظي حقيقي مع AI Message Lock + aria-busy! 🔥 | `جيميني/gemini_login.py` |
| 43 | v2.1: `startswith` Re-render Guard — بدل `sent_so_far` الرقمي | `جيميني/gemini_login.py` |
| 44 | v2.1: Consecutive-only dedup — بيمسح المتكرر المتتالي بس مش المتشابه | `جيميني/gemini_login.py` |
| 45 | v2.1: 3-condition stop — stop_gone + send_enabled + 900ms stability | `جيميني/gemini_login.py` |
| 46 | v2.2: FIX '\n' فاصل عند Re-render — حل لزق الكلمات "نورتنإيه" | `جيميني/gemini_login.py` |
| 47 | v2.2: FIX aria-busy + action buttons (COPY/THUMB_UP) = completion أسرع | `جيميني/gemini_login.py` |
| 48 | v2.2: FIX get_reply_text() كرد نهائي بعد البث — مش full_reply المتراكم | `جيميني/gemini_login.py` |
| 49 | إنشاء `arena_login.py` — أتمتة arena.ai خطوة 1: فتح + Accept Cookies + اختيار Direct Mode | `ارينا/arena_login.py` |
| 50 | اكتشاف Radix UI Portal pattern في Arena — options بتظهر في body مش جوا combobox | `ارينا/arena_login.py` |
| 51 | تبسيط arena_login.py — استخدام `arena.ai/text/direct` مباشرة بدل combobox — 288 سطر → 150 سطر | `ارينا/arena_login.py` |
| 52 | Arena.ai كامل: إرسال + Agree popup + بث لحظي + قراءة رد AI بـ `div.no-scrollbar .prose` | `ارينا/arena_login.py` |
| 53 | Arena v1.1 Opt-Minus: حذف dead code + Config/Sel classes + re-render fix + stall timeout 8ث + Login dialog Close | `ارينا/arena_login.py` |
| 54 | Arena v1.2 — 5 Fixes: @dataclass Config + os.getenv + default arg fix + re-send continue + input flag + popup timing | `ارينا/arena_login.py` |
| 55 | Arena v1.3 — Login Dialog Auto-Close: dismiss_login_dialog() content-based (h1+span.sr-only) + aria-label fallback | `ارينا/arena_login.py` |
| 56 | إنشاء `deepseek_register.py` v1 — تسجيل حساب + تسجيل دخول + كود تحقق يدوي + حفظ في txt | `ديب سيك/deepseek_register.py` |
| 57 | `deepseek_register.py` v2 — EmailnatorClient (توليد إيميل + كود تحقق تلقائي) + `fast_type` JS + 3 مودات (auto/register/login) | `ديب سيك/deepseek_register.py` |
| 58 | تسجيل حساب DeepSeek أوتو كامل نجح — emailnator ولّد إيميل + جاب كود + sign up + حفظ في accounts_deepseek.txt | `ديب سيك/deepseek_register.py`, `accounts_deepseek.txt` |
| 59 | `deepseek_register.py` v3 — 8 إصلاحات: pathlib+resolve+field، fast_type/click_by_text_js بـ arguments[]، verify_typed جديدة، do_auto wrapper (80→12 سطر)، accept_checkboxes مع disabled+count، كل except→log.debug | `ديب سيك/deepseek_register.py`, `GEMINI.md` |
| 60 | Nuclear Session Reset: `clear_session()` بـ JS localStorage+sessionStorage (on domain) + delete_all_cookies + about:blank — حل مشكلة redirect بين الحسابات | `ديب سيك/deepseek_register.py` |
| 61 | Config-driven Loop: `MAX_ACCOUNTS` في Config يتحكم في عدد الحسابات (0=∞، N=N حساب) + `python deepseek_register.py` بدون args = لوب من Config | `ديب سيك/deepseek_register.py` |
| 62 | v3.4 — 10 إصلاحات تقنية من مراجعة 5 AIs: EmailnatorClient reuse + fail limit 3× + حذف input()/do_auto/--loop + wait_for_navigation إيجابي + SW+IDB في clear_session + CODE_INPUT clickable | `ديب سيك/deepseek_register.py` |
| 63 | v3.5 — Browser Restart كل N محاولات: `_clear_chrome_temps` + `restart_browser` + `run_loop` بيدير SB بنفسه + `--restart` CLI + `try/finally` للتقفيل الآمن | `ديب سيك/deepseek_register.py` |
| 64 | v3.6 — عداد الانتظار الحقيقي: `_get_resend_countdown` تقرأ "Resend after Xs" من DeepSeek + تمرره لـ `wait_for_code` + لوج يعرض (elapsed/timeout) بدل العداد الخاطئ | `ديب سيك/deepseek_register.py` |
| 65 | v3.7 — Smart Restart Policy: `RESTART_ON_SUCCESS=3` + `RESTART_ON_FAIL=True` + `FAIL_COOLDOWN=60` بدل `BROWSER_RESTART_EVERY` + `success_streak` عداد + delay للنجاحات فقط (cooldown للفشل) | `ديب سيك/deepseek_register.py` |
| 66 | Login-Only v1.0 — إعادة كتابة `deepseek_login.py` من 732→240 سطر: حذف chat/streaming/provider + إضافة `load_accounts` + `mark_account` (atomic write) + `do_login_one` + `run_loop` + CLI | `ديب سيك/deepseek_login.py` |
| 67 | v3.8 — إصلاح الباسورد: اكتشاف إن React state ناقص آخر حرف (DOM=14, React=13) + إضافة `react_type()` بـ InputEvent + حرف حرف + re-set كامل + blur. حذف `fast_type` retry من `verify_typed` + حذف `verify_typed` من الباسورد + باسورد جديد `Zz9kQe3Lp7Xm2w` | `ديب سيك/deepseek_register.py` |
| 68 | Reset Password v1.0 — سكريبت جديد standalone: forgot_password → Emailnator → Continue → `react_type` للباسورد الجديد → Reset + CLI args + `mark_account` | `ديب سيك/deepseek_reset_password.py` |
| 69 | Phase D13: Session Cookies — إضافة `save_cookies_by_email` + `load_session` في register. format الملف دلوقتي: `email \| password \| sessions/email.json`. sessions مجلد جديد + session أول محفوظة بنجاح | `ديب سيك/deepseek_register.py` + `sessions/` |
| 70 | Session Login v1.0 — سكريبت تسجيل دخول بالكوكيز فقط — بيقرأ session path من accounts.txt → بيحمّل cookies → `verify_logged_in` → CLI | `ديب سيك/deepseek_session_login.py` |
| 71 | Session v2.0 — اكتشاف إن DeepSeek بيستخدم `localStorage.userToken` (JWT) مش cookies → `save_full_session` بيحفظ cookies+localStorage+sessionStorage → `load_session` بـ Pre-flight trick (robots.txt) + حقن localStorage → **نجح!** 🎉 `26 localStorage keys + userToken ✅` | `ديب سيك/deepseek_login.py` + `deepseek_session_login.py` |
| 72 | Phase D14: Register + Session — إضافة `save_full_session` في `do_register` بعد التسجيل مباشرة → حساب جديد يجيب session كاملة في نفس الخطوة | `ديب سيك/deepseek_register.py` |
| 73 | Phase D15: Single JSON — هجرة من `accounts_deepseek.txt` + `sessions/*.json` إلى ملف `accounts_deepseek.json` واحد فيه email+password+status+session. `load/save/upsert` في الـ 3 ملفات — atomic write | `ديب سيك/deepseek_register.py` + `deepseek_login.py` + `deepseek_session_login.py` |
| 74 | Phase D16: Session Keeper v1.0 — سكريبت جديد `deepseek_session_keeper.py` يراقب الحسابات: check_session (Pre-flight+localStorage) → refresh_session (do_reset→login→collect) → update JSON. + `last_refreshed`/`created_at`/`fail_count` في `upsert_account` | `ديب سيك/deepseek_session_keeper.py` |
| 75 | Phase G-1: Groq Token Generator v2.0 — سكريبت جديد `groq_token_generator.py`: Emailnator → Magic Link (Stytch) → Login → Create API Key (gsk_) → JSON. Config 14 إعداد + `clear_session` + `human_delay` بكسور + browser restart + loop بطيء | `groq/groq_token_generator.py` |
| 76 | Phase G-2: Groq Token Generator v2.1 — `colorama` ألوان Terminal (إنجليزي + emojis) + أي فشل = restart فوراً (مفيش retries نهائياً) + `MAX_CONSECUTIVE_RESTARTS=10` + Stats panel كل 5 tokens | `groq/groq_token_generator.py` |
| 77 | Phase G-3: Groq Token Tester v2.0 — سكريبت جديد `groq_tester.py`: يقرأ token من JSON → قائمة موديلات (19 موديل) + Rate Limits + بعت برومت (Config.DEFAULT_PROMPT). موديل default: `kimi-k2-instruct-0905`. شغل وجاب نكتة صعيدية! | `groq/groq_tester.py` |
| 78 | Phase A-1: AIChatApp Client v1.0 — سكريبت `aichatapp_client.py` pure requests (صفر Selenium): Firebase login (signInWithPassword) → access_token ديناميكي + auto-refresh كل ساعة → POST /chat (header: xuthorization). شغل وجاب "Hello, nice to meet you" من gpt-5-nano-2025-08-07! | `chat.aichatapp/aichatapp_client.py` |
| 79 | Phase P-1: Pollinations Client v1.0 — سكريبت `pollinations_client.py` pure requests: sk_ API key جاهز (30 يوم) + auto-create key بالـ session token + OpenAI-compatible API → `claude-sonnet-4.6` شغل! + models list + profile + prompt file + colorama | `pollinations/pollinations_client.py` |
| 80 | Phase P-2: Pollinations v1.2 — persistent history (بيفتكر بين الـ runs!): KEEP_HISTORY + PERSIST_HISTORY + history.json + _load/_save تلقائي + token usage tracking + /clear /usage /history + --no-history + --clear-history. افتكر اسم "ززيو" بعد restart! | `pollinations/pollinations_client.py` |
| 81 | Phase AR-1: Arena Account Creator v1.1 — سكربت `arena_register.py` أوتو: Mail.tm temp email + SeleniumBase (uc=True) + 10-step signup flow (Accept Cookies → Login → Email → Name → Verify Link → Password → Finish) + 4-strategy Finish button (CSS+JS force-click+Enter+form.submit) + React-compatible _safe_type/_react_type + arena_accounts.json + CLI (--count --headless) | `ارينا/arena_register.py` |
| 82 | Phase AR-2: Arena Session Verifier v1.0 — سكربت `arena_session_login.py`: يقرأ arena_accounts.json → يحقن الكوكيز → يتأكد User Profile موجود → يستخرج access token من base64 JWT cookie + optional --chat test + --email/--all/--headless | `ارينا/arena_session_login.py` |
| 83 | Phase AR-3: Arena Email Login v1.0 — سكربت `arena_email_login.py`: يقرأ email/password من JSON → browser login (Accept Cookies → Login → Email → Password → Submit) → يجدد السيشن (cookies+token) → يحدث JSON + `last_updated` timestamp | `ارينا/arena_email_login.py` |
| 84 | Fix: Login Submit vs Header — JS كان بيضغط على header Login بدل submit Login (نفس النص). الحل: `querySelectorAll('button[type="submit"]')` بس + scrollIntoView + fallback | `ارينا/arena_email_login.py` |
| 85 | Anonymous Session Guard — في الـ 3 سكربتات: بيفك base64 auth cookie ويشيك `is_anonymous` + navigate /text/direct + IIFE async fetch + `last_updated` + refreshed_cookies | `arena_email_login/register/session_login` |
| 86 | Arena Scripts v2.0 — arena_register.py: arguments[] JS injection fix، verify_typed+Password Re-type Guard، collect_full_session (cookies+localStorage+sessionStorage)، clear_session nuclear، upsert+atomic write (.tmp→rename)، mask_password، human_delay، fail cooldown، check_success بدون URL heuristic | `ارينا/arena_register.py` |
| 87 | Arena Scripts v2.0 — arena_email_login.py: arguments[] fix، _verify_typed للـ email+password، _collect_full_session، atomic save، _mask_password، human_delay (random 5-15s)، Config renamed (ARENA_URL/ARENA_CHAT_URL) | `ارينا/arena_email_login.py` |
| 88 | Arena Scripts v2.0 — arena_session_login.py: inject localStorage+sessionStorage alongside cookies، collect full refreshed session، anonymous session guard بعد refresh، base64 import at top، ARENA_CHAT_URL | `ارينا/arena_session_login.py` |
| 89 | Phase ZO-1: Zo Computer Registration v1.0 — pure requests (صفر Selenium!): Emailnator → Magic Link (JWT ES256) → /api/email-login/confirm → auth cookies → POST api.zo.computer/signup/ (SSE stream: account+computer+domain) → /signup/status verify. timeout=300s + graceful SSE timeout recovery + retry step 5 | `zo.computer/register.py` |
| 90 | Phase ZO-2: Zo Computer v2.0 — you.com pattern: @dataclass Config + argparse CLI (--max/--loop/--delay/--timeout/--list) + loop mode مع final_stats + account_header + _timed_out guard + Emailnator 3x retry + `provider: emailnator` في JSON + atomic write | `zo.computer/register.py` |
| 91 | Phase ZO-3: Zo Computer v3.0 — Mail.tm provider: MailTmClient + auto-detect provider من الدومين + email_creds (password_mailtm/token_mailtm/account_id_mailtm) + _get_email_client rotation + --provider CLI (mailtm/emailnator/mix/comma) + EMAIL_PROVIDER default "mailtm,emailnator" | `zo.computer/zo.computer_register.py` |
| 92 | Phase ZO-4: Monitor integration + تسمية جديدة — `refresh.py` (magic link re-auth مع Mail.tm creds أو Emailnator) + تسجيل `zo_computer` في `monitor.py` PROVIDERS + `accounts_zo.computer.json` + قاعدة تسمية: register بـ prefix / refresh بدون | `zo.computer/refresh.py`, `monitor.py` |
| 93 | You.com naming + refresh — renaming: `you.com_register.py` + `accounts_you.com.json` + `refresh.py` جديد (importlib لتحميل module فيه `.` في اسمه) + تحديث `monitor.py` paths | `you.com/refresh.py`, `monitor.py` |
| 94 | Runable — Monitor integration: `refresh.py` (magic-link re-auth مع Emailnator + Dropmailx auto-detect من الدومين) + تسجيل `runable` في `monitor.py` PROVIDERS (353 حساب!) | `Runable/HHHAAARR/refresh.py`, `monitor.py` |
| 95 | Mistral Script Alignment — محاذاة `mistral_register.py` مع `you.com_register.py`: argparse CLI (`--max --loop --delay --timeout --phone --provider --list`) + Config dataclass + pathlib + `_timed_out()` + `list_accounts()` + `load_accounts()` + `_detect_provider()` + atomic write + rollback + Arabic config comments + `EMAIL_PROVIDER` rotation | `mistral/mistral_register.py` |
| 96 | Workflow: `/new-provider` — ملف `.agents/workflows/new-provider.md` بيتقري تلقائي كل ما اليوزر يقول "provider جديد" — فيه كل القواعد الإلزامية (argparse, Config, pathlib, timeout, Arabic comments, atomic write) | `.agents/workflows/new-provider.md` |
| 97 | UNIVERSAL_PROVIDER_PROMPT — 3 قواعد جديدة: #21 (تعليقات عربي على config) + #22 (argparse+Config+pathlib+provider rotation) + `EMAIL_PROVIDER` بيدعم `"mailtm"` / `"mailtm,emailnator"` / `"mix"` | `UNIVERSAL_PROVIDER_PROMPT.md` |
| 98 | Mistral Monitor Integration — `refresh.py` جديد (Ory Kratos password login: flow_id+csrf → login بالباسورد → cookies+csrftoken جديدة) + تسجيل `mistral` في `monitor.py` (expires_default=24) + قاعدة #23 في البرومت | `mistral/refresh.py`, `monitor.py`, `UNIVERSAL_PROVIDER_PROMPT.md` |
| 99 | Phase AL-1: Agent Learning — Template Composer: `_compose_from_templates()` بيركّب 678L register فوراً من golden templates بدون AI + `_TEMPLATE_REGISTRY` (5 auth types: password/OTP/session/magic-link/oauth) + `_find_nearest_template_file()` exact+fallback | `v2/code_generator.py` |
| 100 | Phase AL-2: AI Review Loop — `_ai_review_code()` بيستخدم `multi_ask()` (6 providers بالتوازي) بدل Pollinations المكسور (500). Prompt 2K بدل 26K. JSON response parsing | `v2/code_generator.py` |
| 101 | Phase AL-3: 3 Guards — Length Guard (678→51 blocked!) + Template Protection (saved to generated/) + CodeGenConfig.composer="template" | `v2/code_generator.py` |
| 102 | Phase AL-4: Email Verification — `Config.VERIFY_DOMAIN="spmailtechno.com/f/a/"` + `_extract_oob_code()` (3 methods: query/fragment/body regex). اختبار حقيقي: oobCode طلع من redirect ✅ | `AI21_Maestro/ai21_register.py` |
| 103 | Phase AL-5: AI21 refresh.py كامل — Firebase token refresh (securetoken API) → password fallback → AI21 re-sign-in → API key check → atomic save. 220L+ بدل 41L skeleton | `AI21_Maestro/refresh.py` |
| 104 | Phase AL-6: AI21 Full Compliance — 10 fixes: `_detect_provider(gmail→emailnator, ridermail→dropmailx, virgilian.com→mailtm)` + `_get_email_creds` + `_timed_out` + `step/ok/fail` output + JSON (14 fields: +provider+email_creds+status+last_updated+expires_in+refresh_token) + `list_accounts` جميل + `EMAIL_PROVIDER` Config rotation | `AI21_Maestro/ai21_register.py` |
| 105 | Phase AL-7: AI21 Tested + Working — Fixed 3 bugs: `key_value` field (مش `api_key`) + workspaces dict parsing (`{"workspaces":[...]}`) + LOOP_MODE argparse defaults. اختبار حقيقي: `jamba-mini` chat completion 200 ✅. حساب من 0 لـ API key في 20 ثانية | `AI21_Maestro/ai21_register.py` |
| 106 | Phase AL-8: temp-mail.org 3rd email provider — `TempMailOrgClient` (curl_cffi + impersonate="chrome124"). Dynamic domain cache (`_TEMPMAIL_DOMAINS` set بيتملى تلقائي). Stats `( ✅ 0 ❌ 0 )` في account header. اختبار: flosek.com + niprack.com 100% ✅ | `AI21_Maestro/ai21_register.py` |
| 107 | Phase CO-1: Cohere + BestTempEmail — `BestTempEmailClient` (Livewire, no captcha, 3 domains: aboodbab/mamabood/mohemil). حل مشكلة verify link: regex يدور على "Confirm" button href مش أول sendgrid link. Redirect chain step-by-step: SendGrid → dashboard.cohere.com/confirm-email → /api/auth/confirm_email → access_token cookie. **API Key في 16 ثانية!** | `cohereR/cohere_register.py` |
| 108 | Phase CO-2: Cohere Register v1.1 — 6 integration points: `BestTempEmailClient` class (139L) + `_detect_provider` (besttemp domains) + `create_one_account` (elif besttemp) + `argparse choices` + `mix` list + `confirm_email_via_link` (hop-by-hop redirect) + `VERIFY_DOMAIN=confirm-email`. Default provider = besttemp | `cohereR/cohere_register.py` |
| 109 | v2 Agent Fix: Template→HAR Endpoints — `_compose_from_templates()` بقى يبدل URLs (regex+AI). +3 functions (`_extract_base_urls`+`_has_template_urls`+`_ai_adapt_endpoints`). `_ai_review_code()` بقى يشمل HAR endpoints. Hybrid: regex أولاً (0 API calls) → AI fallback لو فشل | `v2/code_generator.py` |
| 110 | 🗑️ مسح Pollinations نهائي — حذف من `multi_ask.py` (80+ سطر: `_POLLINATIONS_MODELS` + `_poll_single()` + `_ask_all_pollinations()` + poll_future). Providers بقوا 6 بس: you.com · zo · groq · deepai · runable · ai21 | `multi_ask.py` |
| 111 | Phase 2: Skeleton Split + Groq Codegen — `_ask_groq_codegen()` بقت تستخدم `multi_ask()` (6 providers بالتوازي). 4 دوال جديدة: `_extract_skeleton()` + `_generate_flow_from_har()` + `_merge_skeleton_flow()` + updated `_ai_adapt_endpoints()`. Detection محسّن: `_has_template_urls()` بتشيك المسارات مش بس الـ domain | `v2/code_generator.py` |
| 112 | Phase CO-3: Cohere Fixes — حذف `_extract_oob_code()` dead code (50L) + `self._access_token = None` init + HAR comment cleanup + `_get_email_creds` support لـ besttemp/tempmail + `login_with_email` fallback + `expires_in` في account dict | `cohereR/cohere_register.py` |
| 113 | Phase CO-4: Cohere Refresh — `refresh.py` بـ BlobheartAPI (`LoginWithEmail → Session → GetOrCreateDefaultAPIKey`) + تسجيل `cohere` في `monitor.py` PROVIDERS (both copies) | `cohereR/refresh.py`, `monitor.py` |
| 114 | Phase TN-1: temporary-mail.net Integration — `TemporaryMailNetClient` class (130L): cloudscraper لتخطي Cloudflare + Gmail aliases + `POST /get-emails?lang=` inbox polling + `GET /mail/gmail-content/{id}` + `data-code` من page reload. 4 integration points: `create_one_account` elif + argparse choices + mix rotation + `_detect_provider` (gmail = shared with emailnator) | `cohereR/cohere_register.py` |
| 115 | Phase TN-2: Endpoint Discovery — Reverse-engineered temporary-mail.net API عبر 6 محاولات brute-force + JS source analysis. اكتشاف: `currentLang = ""` (مش `en`!) + الـ `code` = SHA256 `data-code` attribute بيترجع بعد reload الصفحة فقط. `POST /get-emails?lang=` + body `{email, code}` → `{emails: null, success: true}` | `cohereR/cohere_register.py` |
| 116 | Phase TA-1: 35-Model Test System — `test_agents.py` بـ 35 model (4 Tiers) + 4 judges + round-robin token rotation على 19 حساب Perplexity. أول تجربة: 17/35 → بعد rotation: 26/35 (74%) → بعد حذف الميتين: 29/32 (91%) | `test_agents.py` |
| 117 | Phase TA-2: Dead Model Discovery — اختبار 9 models فاشلين فردي: اكتشاف 4 ميتين (command_r_plus, mistral_large, gemini31pro, gemini3pro = EMPTY) + 5 أحياء (pplx_asi, experimental, pplx_agentic_research كانوا rate limited مش ميتين) | `_test_failed.py` |
| 118 | Phase PP-1: pplx_pool.py — مكتبة مشتركة: 32 model + token rotation + `ask_model` / `ask_chain` / `ask_many` (parallel) + `extract_json` + `get_models(count)`. كل ملف في v2 بيستخدمها | `v2/pplx_pool.py` |
| 119 | Phase PP-2: v2 Integration — دمج pplx_pool في 3 ملفات: `ai_analyzer.py` (pplx_pool agent جديد = 32 model بالتوازي) + `multi_ask.py` (token rotation بدل single token) + `code_generator.py` (pplx_pool reviewer). Syntax 4/4 ✅ + Imports 23/23 ✅ | `v2/ai_analyzer.py`, `multi_ask.py`, `v2/code_generator.py` |
| 120 | HAR Analysis × 3 — اختبار حقيقي على 3 ملفات: Cohere (29/32, 91%, auth=password) + Mistral (28/32, 88%, auth=magic-link) + zo.computer (25/32, 78%, auth=magic-link). كلهم judges HIGH ✅ | `v2/32agent_fixed.json`, `v2/32agent_mistral.json`, `v2/32agent_zo.json` |
| 121 | Phase ER-1: ERNIE Bot Registration v1.0 — Full Playwright UI Automation: gmail-only Emailnator + stealth init_script + osfuid retry loop (3×reload) + `button#sendCodeBtn` activation trick (click fields again) + `div.pass-button.continue-button.active` (مش button!) + `verify_code` في reg/email + Get Started session capture. accounts_ernie.json (email+password+osduss+cookies) 🎉 | `ernie.baidu/ernie_playwright.py`, `ernie_batch.py`, `accounts.json` |
| 122 | Phase ER-2: ERNIE Endpoint Discovery — اكتشاف الـ endpoint الحقيقي من Burp: `/eb/chat/conversation/v2` (مش `/eb/conversation/chat`!). اختبار 4 scenarios: بدون Acs-Token ✅ + مع Acs-Token ✅ + Burp cookies ✅ + old endpoint ❌ (rate limit). v2 analysis (32 model) بالتوازي | `ernie.baidu/test_v2_endpoint.py`, `ernie.baidu/ask_acs_token.py` |
| 123 | Phase ER-3: ERNIE Chat Client v2 — pure requests (curl_cffi): SSE parser بيتتبع event type (major→thought→step→message). اكتشاف bug: `event:thought` عنده `is_end:1` = نهاية التفكير ≠ نهاية الرد! الرد الحقيقي في `event:message` → `tokens_all`. بدون Acs-Token! 🎉 | `ernie.baidu/ernie_chat.py` |
| 124 | Phase ER-4: ERNIE Chat Working — اختبار حقيقي: "قول نكتة مصرية مضحكة" → ERNIE رد بنكتة كاملة عن موظف الحكومة في 72 ثانية ✅. Multi-turn + account rotation + SSE streaming | `ernie.baidu/ernie_chat.py` |
| 126 | DeepSeek Register v2.0 — نظام هجين: SeleniumBase مفتوح طول الوقت لـ WAF bypass + `fetch()` من داخل المتصفح لـ `send_code` (بتخطي PoW) + UI automation لـ `register` (DeepSeek JS بيحل PoW تلقائي) = 37 حساب في جلسة واحدة ✅ | `ديب سيك/deepseek_register_v2.py`, `accounts_deepseek.json` |
| 127 | UNIVERSAL_PROVIDER_PROMPT Compliance — 6 fixes: `account_header()` `( ✅ X ❌ Y )` بين كل حساب + `step(N/total)` format + `waiting()` للـ delay display + `final_stats()` بـ Rate%+Time+New + `--list`/`--count` CLI + Ctrl+C ملون. LOOP CONFIG block بـ Arabic comments + `EMAIL_PROVIDERS` list + `Config` constructor | `ديب سيك/deepseek_register_v2.py` |
| 128 | DeepSeek Hybrid Reset Password v3.0 — ملف جديد `deepseek_hybrid_reset_password_v3.py`: نظام هجين 3-layer (1: requests reset سريع ~30s، 2: SeleniumBase browser fallback ~90s). `HybridOrchestrator` ينسق الـ layers + `--strategy requests/browser/hybrid` CLI + fatal errors guard (`EMAIL_NOT_EXIST` يوقف browser fallback) + retry مع delay 65s + ألوان. اختبار حقيقي: OTP في 23s + token ✅ | `ديب سيك/deepseek_hybrid_reset_password_v3.py` |
| 129 | refresh.py Hybrid v2 — أُعيدت كتابة `refresh.py` كنظام هجين: Layer 0 (token cache check) + Layer 1 (requests login ~2s سريع) → Layer 2 (SeleniumBase browser fallback). إصلاح NoneType bug (`biz_data=null`). اختبار عبر `monitor.py --provider deepseek`: 126 حساب | 125 OK | 1 محتاج تجديد ✅ | `ديب سيك/refresh.py`, `monitor.py` |
| 130 | File Input/Output Feature — أضفنا `--input-file/-f` (قراءة سؤال من ملف نصي) + `--output-dir/-o` (حفظ ردود في مجلد) + `--models` (تحديد مرن: `groq,ernie` أو `groq:kimi-k2,ernie:EB50`) + `--output-format` (txt/json/both) + `--mode batch` (كل سطر = سؤال مستقل بملف TXT+JSON منفصل). اختبار نجح 4/4 أسئلة 🎉 | `ai_engine.py` |
| 131 | ai_config.yaml Output Section — إضافة قسم جديد `output:` (default_dir / default_format / filename_prefix / pretty_json) + تحديث timeout من 30s لـ 300s + الموديل الافتراضي `kimi-k2-instruct-0905` | `ai_config.yaml` |
| 132 | Cursor Registration v2.0 — نظام هجين 7 خطوات لإنشاء حسابات Cursor AI أوتوماتيكياً: تخطي Cloudflare عبر SeleniumBase + Oonetimemail + `cdp_eval` للنقر على أزرار React + `_ManualClient` مدمج للتدخل البشري وتجاوز Phone SMS | `C_cursor/cursor_register.py` |
| 133 | Genspark Ultra Mode — إضافة خاصية مود Ultra اللي بيعتمد على (Claude Opus 4.6 1M Context) عبر تمرير `--ultra` في `genspark_chat.py` لحقن `use_model` ديناميكياً | `Genspark_V2/genspark_chat.py` |
| 134 | Oysho SMS Automation — أتمتة إرسال SMS لـ Oysho وإنشاء نظام هجين (Selenium -> curl_cffi) لتجاوز حماية Akamai Bot Manager v3 (action: 0, code: 4) وحقن Bearer Token | `O__oysho/test/oysho_full_flow.py` |
| 135 | WAF Diagnostic Framework — استخراج 169 Section من 16000 سطر لإنشاء مرجع SSOT لتشخيص Layer 7 والـ Bot Managers | `WAF_BOT_DIAGNOSTIC_MASTER_PROMPT.md` |
| 136 | إضافة `promptcowboy-extension` Chrome Extension — أتمتة شاملة للتسجيل بضغطة زر عبر الخلفية بـ `Pure APIs` و `chrome.scripting`. | `P__promptcowboy/promptcowboy-extension/*` |
| 137 | بناء النسخة الأولى v1 من سكربت `azcaptcha_v1_curl_cffi.py` باستخدام `curl_cffi` لأتمتة عملية جلب الكابتشا وإرسال طلب التسجيل لموقع AZCaptcha، مع دعم الـ Emojis في تيرمنال الويندوز | `a_z_captcha_captcha/azcaptcha_v1_curl_cffi.py` |
| 138 | بناء الإصدار v2 من سكربت `azcaptcha_v2_curl_cffi_auto.py` باستخدام `ddddocr` لإنشاء حسابات أوتوماتيكياً بالكامل وحل الكابتشا (PNG) محلياً بدون أي تدخل بشري أو تكلفة | `a_z_captcha_captcha/azcaptcha_v2_curl_cffi_auto.py` |
| 139 | بناء الإصدار النهائي v3 (Production) من سكربت `azcaptcha_v3_curl_cffi_production.py` مع نظام Loop وحفظ Atomic لملف `accounts_azcaptcha.json` وRetry Logic لأخطاء الـ OCR | `a_z_captcha_captcha/azcaptcha_v3_curl_cffi_production.py` |
| 140 | بناء وتشغيل سكريبت اختبار المهلة الإجمالية `test_overall_timeout.py` حياً بنجاح 5 ثواني لفرامل الطوارئ الذكية لزيزو وتأكيده بالكامل. | `..............................................................................................................شغل فريق/test_overall_timeout.py` |
| 141 | تحليل تفريغ المحادثة المالية واستخراج الدروس الفقهية والعملية حسب الـ Master Prompt الديني والعملي. | `ررررررر/اساسي` |
| 142 | تصفير مستودع جيت هاب الخارجي `AAAA_jules_AAA` بالكامل، مسح جميع الملفات والـ additional branches، والإبقاء على README.md فارغ فقط. | مستودع جيت هاب الخارجي |

---

## 📂 الملفات الجديدة

| Redot_Pay_PART_v_15/extract_traffic.py | استخراج ريكويستات Burp المعقدة إلى JSON مهيكل | ✅ جديد |
| الملف | الوظيفة | الحالة |
|-------|---------|--------|
| `ديب سيك/deepseek_login.py` | سكربت تسجيل دخول + إرسال + استقبال رد | ✅ مستقر |
| `providers/deepseek_provider.py` | Browser-based provider (ask + generate + stats) | 🟡 يحتاج تحسين |
| `GEMINI.md` | قواعد المشروع للـ AI | ✅ مستقر |
| `جيميني/gemini_login.py` | Gemini browser automation (login + model + send) | 🟡 قيد التطوير |
| `جيميني/GEMINI_REFERENCE.md` | مرجع أتمتة Gemini | ✅ مستقر |
| `ارينا/arena_login.py` | Arena.ai automation — Direct Mode: إرسال + بث + قراءة | ✅ مستقر |
| `ديب سيك/deepseek_register.py` | DeepSeek إنشاء حسابات أوتو (emailnator + كود تلقائي) | ✅ مستقر |
| `accounts_deepseek.txt` | حسابات DeepSeek: email \| password \| session_path \| ✅ نجح | ✅ يتحدث تلقائي |
| `ديب سيك/deepseek_reset_password.py` | Reset Password أوتو: forgot_password → Emailnator → react_type → Reset | ✅ جديد |
| `ديب سيك/deepseek_login.py` | Login + حفظ Full Session (cookies+localStorage+sessionStorage) | ✅ v2 |
| `ديب سيك/deepseek_session_login.py` | Login بالـ Session — Pre-flight + حقن localStorage (userToken) | ✅ v2 |
| `ديب سيك/accounts_deepseek.json` | SSOT — كل الحسابات في JSON واحد (email+password+status+session+last_refreshed) | ✅ D15 |
| `ديب سيك/deepseek_session_keeper.py` | Session Keeper — يراقب ويجدد الجلسات (check→reset→update JSON) | ✅ D16 جديد |
| `groq/groq_token_generator.py` | Groq Token Generator — Magic Link + API Key extraction + JSON + slow loop + colors + fail=restart | ✅ G-2 v2.1 |
| `groq/groq_tester.py` | Groq Token Tester — Models + Rate Limits + Chat (Config.DEFAULT_PROMPT) + colorama | ✅ G-3 v2 |
| `groq/groq_tokens.json` | قاعدة بيانات التوكنات (JSON) — email + api_key + created_at + status | ✅ G-1 |
| `chat.aichatapp/aichatapp_client.py` | AIChatApp Client — pure requests: Firebase login + auto-refresh + POST /chat (xuthorization header) + colorama | ✅ A-1 v1 |
| `pollinations/pollinations_client.py` | Pollinations Client v1.2 — pure requests: sk_ key + auto-create + chat + persistent history + token tracking + colorama | ✅ P-2 v1.2 |
| `pollinations/prompt.txt` | ملف برومت خارجي — اكتب سؤالك هنا | ✅ P-1 |
| `pollinations/history.json` | سجل المحادثة — يتحدث تلقائياً بعد كل رد | ✅ P-2 |
| `ارينا/arena_register.py` | Arena Account Creator v1.1 — Mail.tm + SeleniumBase auto signup + React-compatible input + 4-strategy Finish | ✅ AR-1 v1.1 |
| `ارينا/arena_accounts.json` | قاعدة بيانات حسابات Arena (email+pass+cookies+access_token) | ✅ AR-1 |
| `ارينا/arena_session_login.py` | Arena Session Verifier — حقن كوكيز + تحقق User Profile + استخراج token + optional chat test | ✅ AR-2 v1.0 |
| `ارينا/arena_email_login.py` | Arena Email Login — browser login بالإيميل/باسورد + session refresh + last_updated | ✅ AR-3 v1.0 |
| `zo.computer/register.py` | Zo Computer Registration — pure requests: Emailnator + Magic Link + SSE signup + accounts.json | ✅ ZO-1 v1.0 |
| `zo.computer/accounts.json` | حسابات zo.computer (email+handle+domain+status+session+signup_status) | ✅ ZO-1 |
| `cohereR/refresh.py` | Cohere refresh — BlobheartAPI: LoginWithEmail → Session → GetOrCreateDefaultAPIKey | ✅ CO-3 |
| `بي ريييب/بي ريييب/perplexity_register.py` | Perplexity Register — Mail.tm + OTP + JWT + curl_cffi + CLI (--max/--loop/--list) | ✅ PX-1 v1 |
| `بي ريييب/بي ريييب/perplexity_chat.py` | Perplexity Chat — 44 موديل + TokenManager (auto-switch) + CLI + interactive | ✅ PX-3 v2 |
| `بي ريييب/بي ريييب/accounts_perplexity.json` | حسابات Perplexity (email+auth_token+user_id+status+email_creds) | ✅ PX-1 |
| `v2/pplx_pool.py` | مكتبة مشتركة: 32 model + token rotation + parallel — يستبدل perplexity_chat.py للـ multi-model | ✅ PP-1 |
| `test_agents.py` | سكريبت اختبار: 32 model × 19 حساب + 4 judges + round-robin tokens | ✅ TA-1 |
| `_test_failed.py` | سكريبت تشخيصي: اختبار models فاشلين فردي (dead vs fixable) | ✅ TA-2 |
| `ernie.baidu/ernie_playwright.py` | ERNIE Bot Registration — Full Playwright UI Automation (send_code + reg/email + Get Started session) | ✅ ER-1 v1 |
| `ernie.baidu/ernie_batch.py` | ERNIE Batch Creator — تشغيل N حساب متتالي + v2 بالتوازي | ✅ ER-1 |
| `ernie.baidu/accounts.json` | حسابات ERNIE (email+password+osduss+cookies) | ✅ ER-1 |
| `ernie.baidu/ernie_chat.py` | ERNIE Chat Client v2 — pure requests + SSE parser (event:message→tokens_all) + multi-turn + account rotation | ✅ ER-3 v2 |
| `ernie.baidu/test_v2_endpoint.py` | اختبار شامل للـ endpoint الجديد /eb/chat/conversation/v2 (4 scenarios) | ✅ ER-2 |
| `ernie.baidu/ask_acs_token.py` | v2 script: 32 models تحلل Acs-Token generation | ✅ ER-2 |
| `ernie.baidu/debug_sse.py` | Debug script: يقرأ SSE stream خام ويعرض كل event type | ✅ ER-3 |
| `grok/grok_register.py` | Grok (x.ai) Registration — Hybrid: curl_cffi (gRPC) + SeleniumBase (Turnstile) + 3 email providers + CLI (--max/--loop/--provider/--list) | ✅ GK-1 |
| `grok/refresh.py` | Grok refresh — session renewal مع gRPC-web | ✅ GK-1 |
| `grok/accounts_grok.json` | حسابات Grok (email+password+cookies+email_creds+status+last_updated) | ✅ GK-1 |
| `ديب سيك/deepseek_hybrid_reset_password_v3.py` | Hybrid Reset Password v3: requests + browser fallback + HybridOrchestrator + 3-strategy CLI | ✅ #128 |
| `ديب سيك/refresh.py` | Hybrid Refresh v2: token cache → requests login → browser fallback. Monitor-compatible `def refresh(email) -> bool` | ✅ #129 |
| `ai_engine.py` | AI Engine — File I/O Feature: `--input-file` + `--output-dir` + `--models` + `--output-format` + `batch` mode | ✅ #130 |
| `test_input.txt` / `test_batch.txt` | ملفات اختبار: سؤال واحد / batch (كل سطر = سؤال مستقل) | ✅ #130 |
| `C_cursor/cursor_register.py` | Cursor AI Account Creator — 7-step Hybrid Registration Flow + Manual Fallback | ✅ #132 |
| `O__oysho/test/oysho_full_flow.py` | أتمتة أويشو — Session Handoff لكسر حماية Akamai وتوصيل كود التحقق SMS | ✅ #134 |
| `WAF_BOT_DIAGNOSTIC_MASTER_PROMPT.md` | مرجع هندسي لتشخيص الـ WAF والـ Bot Managers (169 Section) | ✅ #135 |
| promptcowboy-extension/ | إضافة كروم تعمل بالخلفية بمجرد النقر لتوليد أكونت PromptCowboy جديد كلياً وتمرير الكوكيز | ✅ #136 |
| `C__clarif_ai/clarifai_sms.py` | سكربت أساسي لاختبار Clarifai Signup/SMS ووثق ضرورة الـ Captcha | ✅ #115 |
| `local_svg_solver.py` | حل كابتشا الـ SVG محلياً بالكامل عبر matplotlib و ddddocr بدون API خارجي | ✅ جديد |
| `a_z_captcha_captcha/azcaptcha_v1_curl_cffi.py` | الإصدار الأول لأتمتة إنشاء حسابات AZCaptcha، يجلب الـ Token والصورة ويبعت الـ Payload | ✅ جديد |
| `a_z_captcha_captcha/azcaptcha_v2_curl_cffi_auto.py` | الإصدار الثاني المؤتمت كلياً: يحل الكابتشا بالـ OCR وينشئ الحساب ويسحب الـ API Key فوراً | ✅ جديد |
| `a_z_captcha_captcha/azcaptcha_v3_curl_cffi_production.py` | إصدار الإنتاج V3: يدعم اللوب (Loop mode)، استخراج الداتا (Atomic save)، ومعالجة أخطاء الـ OCR ذاتياً (Retry Logic) | ✅ جديد |
| `accounts_azcaptcha.json` | ملف الداتابيز المولد تلقائياً لحفظ بيانات حسابات AZCaptcha و الـ API Keys بشكل Atomic | ✅ جديد |
| `..............................................................................................................شغل فريق/test_overall_timeout.py` | سكريبت اختبار المهلة الإجمالية (overall_timeout) لفرامل الطوارئ حياً وتأكيده مع زيزو. | ✅ جديد |
| `ررررررر/اساسي` | ملف المحادثة المالية (اساسي) الذي تم تحليله. | ✅ مستقر |

---

## 🐛 سجل المشاكل

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
| #116 | [API] | اختفاء ريكويستات الـ SMS/Login من الـ Burp capture في RedotPay | الأعراض: عدم وجود أي endpoint للتسجيل | السبب: وجود AliYun Captcha verification (www.redotpay.com/app_verify) و Device Fingerprinting يعترض مسار الـ Request قبل إرساله | الحل: يحتاج تفحص الـ UI للتأكد من حل الـ Captcha أو استخدام Frida لتجاوز الـ Device Fingerprint | 🔴 مفتوحة |
| #117 | [Script] | الاعتماد على خدمات خارجية لحل الكابتشا يسبب بطء وتسرب بيانات | بطء شديد أثناء حل الـ SVG Captcha واحتمالية تسرب المفاتيح | استخدام موديل Groq Vision الكبير اللي بياخد وقت لمعالجة الصور | تم حذف `solve_captcha.py` والاعتماد على الحل المحلي الـ Offline باستخدام مكتبة ddddocr في `local_svg_solver.py` | ✅ محلولة |
|---|-------|-------------|---------|-------|------|--------|
| #1 | [Security] | تسريب بيانات حساسة في ملف `ريكويست` | وجود `authorization: Bearer` + Cookies صالحة | النسخ المباشر من Burp Suite | تغيير الـ Tokens فوراً | ⚠️ مفتوحة |
| #2 | [Script] | صفحة Human Verification مع Selenium | Cloudflare يكشف البوت | `navigator.webdriver=true` | استخدام `uc=True` في SeleniumBase | ✅ محلولة |
| #3 | [Script] | `SessionNotCreatedException: cannot connect to chrome` | المتصفح يفتح ويوقف | Chrome قديم شغال + Port 9222 | اقفل Chrome + شيل `user_data_dir` | ✅ محلولة |
| #4 | [Script] | الرد بييجي ناقص (سطر واحد بس) | `print` بيطبع span واحد | كنا بناخد `replies[-1]` بس | جمع نص `MSG_CONTAINER.text` كامل | ✅ محلولة |
| #5 | [Script] | السكربت بيقول "اكتمل" والرد لسه في Searching | text stability بيثبت على "Searching for" | طريقة text stability فشلت مع Search mode | Button Counting — عد 5 أزرار `db183363` | ✅ محلولة |
| #6 | [Script] | `aria-disabled` بيمسك أزرار كتير في الصفحة | false positive | CSS selector عام | استخدام selector دقيق `db183363` + عد 5 أزرار | ✅ محلولة |
| #7 | [Backend] | `ask()` و `generate()` async بيستدعوا `run_deepseek_bot()` sync مباشرة | بتبلوك الـ event loop | `asyncio` مش بيتفادى | لازم `asyncio.to_thread()` | 🔴 مفتوحة |
| #8 | [Security] | `EMAIL` و `PASSWORD` hardcoded في `Config` class | بيانات حساسة في الكود | مش موجودين في `.env` | نقلهم لـ `.env` + `os.getenv()` | 🔴 مفتوحة |
| #9 | [Performance] | كل call لـ `run_deepseek_bot()` بيفتح browser session جديد | بطء شديد — login + Cloudflare كل مرة | مفيش session reuse | Persistent browser session | 🔴 مفتوحة |
| #31 | [Script] | `input()` في arena_login.py بيبلوك لو شغال من API/CI | الـ process بيقف | مفيش flag للتحكم | إضافة `WAIT_FOR_INPUT=False` في Config | ✅ محلولة |
| #32 | [Script] | Default arg `config.REPLY_WAIT_SEC` بيتحسب وقت التعريف مش الاستدعاء | لو Config اتغير مش هياثر | Python default arg compilation | `timeout=None` + runtime resolution | ✅ محلولة |
| #33 | [Script] | Re-send loop بيرجع `None` من أول فشل بدل retry | مش بيكمل 3 محاولات | `return None` بدل `continue` | تغيير لـ `continue` + error log بعد الـ loop | ✅ محلولة |
| #34 | [Config] | `Config` class variables عادية مش `@dataclass` | مفيش validation ولا env support | تصميم قديم | تحويل لـ `@dataclass` + `os.getenv()` | ✅ محلولة |
| #35 | [Script] | `last_popup_check=0` بيعمل popup check بدري في أول iteration | timing edge case | القيمة الابتدائية غلط | `last_popup_check=time.time()` | ✅ محلولة |
| #36 | [Script] | Login dialog في Arena مش بيتقفل — الكود القديم بيدور على `role="dialog"` والـ dialog مش عنده role | Login popup بيفضل ظاهر | اعتماد على `role="dialog"` | `dismiss_login_dialog()` content-based: h1 + span.sr-only + aria-label | ✅ محلولة |
| #66 | [Performance] | Pollinations API بيرجع HTTP 500 في `_ai_review_code()` | AI Review مبيشتغلش | Pollinations server instability | استخدام `multi_ask()` (6 providers بالتوازي) | ✅ محلولة |
| #67 | [Script] | AI auto-fix بيكتب فوق template الأصلي (669L → 51L!) | الـ template بيتدمر | output dir = same as template dir | Template Protection: save to `generated/` + Length Guard | ✅ محلولة |
| #37 | [API] | temporary-mail.net `/get-emails?lang=en` بيرجع 400 Invalid language code | الإيميل مش بيتقرأ | `currentLang = ""` مش `en` — لازم query param يكون فاضي | `POST /get-emails?lang=` (بدون قيمة) | ✅ محلولة |
| #38 | [API] | temporary-mail.net `/get-emails` بيرجع 400 Invalid request حتى مع body صح | الـ inbox مش بيتحمل | `data-code` attribute بيترجع بعد server-side activate فقط — لو حطيت الـ cookie يدوي الـ code بيكون غلط | reload الصفحة بعد `/activate-email` → السيرفر بيسيت `active_mailbox` cookie + `data-code` الصح تلقائياً | ✅ محلولة |
| #105 | [Script] | `step()` format تغير بس مش كل calls اترقمت | بعد تغيير signature من `step(N, msg)` لـ `step(N, total, msg)` — كانت في call قديمة في `BrowserSession.start()` الداخلي | نسيان تعديل كل calls في الكود | grep كل calls قبل deploy + compile check | ✅ محلولة |
| #40 | [Performance] | 18/35 model فشلوا في أول اختبار — بسبب rate limiting على token واحد | JSON parsing failed / timeout | كل الـ 35 model على حساب واحد | Round-robin token rotation على 19 حساب → 29/32 (91%) | ✅ محلولة |

| #41 | [Script] | ERNIE: `googleMail` option في Emailnator يولّد `@googlemail.com` مش `@gmail.com` — ERNIE بيرفضه | Email provider not accepted | `googleMail` → `@googlemail.com` domain غير مقبول | حذف `googleMail` من options + safety check | ✅ محلولة |
| #42 | [API] | ERNIE: `ctx.request.post` مش بيبعت JS cookies (osfuid, g_state) — send_code يرجع errno:-1 | errno:-1: system busy | `ctx.request.post` مستقل عن JS cookies | Full UI automation: الـ JS في البراوزر يبعت الـ requests لوحده | ✅ محلولة |
| #43 | [Script] | ERNIE: `button:has-text('Continue')` بيضغط على زرار Google مش Continue | أول Continue button هو Google login | Playwright selector غامض يمسك أول match | استخدام `div.pass-button.continue-button.active` الـ selector الحقيقي | ✅ محلولة |
| #44 | [Script] | ERNIE: password `Ernie@+token_hex(6)` = 18 chars > 14 MAX | Continue button مش بيتفعّل | ERNIE password limit: 8-14 chars | `Aa1@` + `token_hex(3)` = 10 chars ✅ | ✅ محلولة |


| # | [TAG] | الدرس | السياق |
|---|-------|-------|--------|
| #66 | [Script] | WAF-Reuse pattern: SeleniumBase مفتوح طول الجلسة (مش يتفتح ويتقفل لكل حساب) = تخطي Cloudflare مرة واحدة + cookies تفضل صالحة لـ N حساب. `WAF_REUSE_LIMIT` بيتحكم في عمر الـ session | DeepSeek v2 hybrid |
| #67 | [Script] | لو غيّرت signature دالة → grep كل calls في الكود الكامل (مش بس الدالة نفسها). `step(N, msg)` → `step(N, total, msg)` كسر في `BrowserSession.start()` لأن git grep ممكن يفوت | Step() format refactor |
| #68 | [Security] | مواقع الـ Firebase (مثل Lovable) هي الأضعف والأسهل في تجاوز حماية الـ SMS مقارنة بالتي تعتمد على Turnstile أو WASM، حيث يمكن محاكاة تطبيق Android لتخطي التحقق. | تحليل 3 مواقع لإرسال SMS |
| #70 | [Performance] | العمليات المباشرة التي يمكن إنجازها محلياً مثل التعرف الضوئي (OCR) على الكابتشا يجب إبقاؤها Offline للحفاظ على السرعة وتجنب الـ API Leaks، ولا داعي لاستخدام نماذج LLM Vision ثقيلة لها. | إلغاء الاعتماد على Groq في حل الكابتشا |

| #1 | [Security] | نظّف ملفات الـ Requests من الـ Tokens قبل حفظها | عند حفظ مسودات API Calls |
| #2 | [Script] | `uc=True` في SeleniumBase = الحل الأقوى لتخطي Cloudflare | أي موقع عليه حماية Cloudflare |
| #3 | [Script] | `user_data_dir` مع `uc=True` بيسبب تعارض Port — مفيش `user_data_dir` مع DeepSeek | فتح نافذة Chrome جديدة |
| #4 | [Script] | `uc_open()` أثبت من `uc_open_with_reconnect()` مع DeepSeek | فتح مواقع Cloudflare |
| #5 | [Script] | Button Counting أدق من aria-disabled لأن `db183363` خاص بأزرار الرد فقط | كشف اكتمال الرد بدقة |
| #6 | [Script] | `ds-toggle-button--selected` = مؤشر حالة زرار Search/DeepThink | تفعيل/إلغاء Search + DeepThink |
| #7 | [Backend] | `async` functions لازم تستخدم `asyncio.to_thread()` لأي sync code (Selenium) | منع blocking في FastAPI |
| #8 | [Backend] | `ProviderResponse` = عقد ثابت — أي provider لازم يرجعه مش string | التوافق مع `ProviderManager` |
| #9 | [Backend] | Module-level counters (`_total_requests = 0`) مش type annotation — لازم يكون variable فعلي | Python semantics |
| #10 | [Security] | Credentials لازم تكون في `.env` + `os.getenv()` مش hardcoded في Config | أي provider بيحتاج credentials |
| #11 | [Script] | `clickable` أفضل من `visible` — بيوفر 6 ثواني في Sign in | Google OAuth + React SPA hydration |
| #12 | [Script] | `data-test-id` أثبت selector — أحسن من XPath أو class names | Gemini Model Picker: `bard-mode-menu-button` |
| #13 | [Script] | Fallback selectors + Discovery logging — لو واحد فشل جرب الباقي | Model selection في Gemini |
| #14 | [Script] | Login مباشر في `accounts.google.com` أسرع من ضغط Sign in button | تخطي خطوة كاملة |
| #15 | [Script] | JS injection أسرع 10x من `sb.type()` — بيحط القيمة مرة واحدة | Google Login بياخد وقت في type() |
| #16 | [Script] | 3 مؤشرات اكتمال الرد: `footer.complete` + `aria-busy=false` + أزرار الأكشن | Gemini بيخلص streaming |
| #17 | [Script] | `textContent` بيمسح line breaks — `innerText` بعد Scroll هو الحل الصح للردود الطويلة | Gemini lazy loading |
| #18 | [Script] | DOM Polling + Incremental Diff + flush=True = بث لحظي حقيقي بدون Network API | `stream_reply_live()` أي Selenium site |
| #19 | [Script] | زر المحادثة الجديدة في Gemini = تاغ `<a>` مش `<button>` — لازم تتأكد من F12 | HTML inspection دايماً قبل الكتابة |
| #20 | [Debug] | Gemini بيدلق الرد كله مرة واحدة مش حرف بحرف — DOM streaming مستحيل عكس DeepSeek | live stream بيجيب 0 حرف أو أزرار خاطئة |
| #21 | [Script] | AI Message Lock = عد الـ divs قبل الإرسال واستنى div جديد — بيمنع قراءة رسايل قديمة | أزرار من محادثة قديمة بتخليه يخرج بدري |
| #22 | [Script] | NOISE filter لازم regex يمسح الـ prefix بس — مش السطر كله | `Model: ( Gemini )` + نص حقيقي في نفس السطر |
| #23 | [Debug] | `aria-live="polite"` + `aria-busy` = دليل إن Gemini بيحدث DOM تدريجياً مش دفعة واحدة | Genspark كشف الحقيقة — Gemini Pro كان غلط |
| #24 | [Script] | `sent_so_far` كرقم بيفشل مع DOM re-render — لازم `startswith` لمقارنة النصوص | الرد بيتقطع ويطلع خربان |
| #25 | [Script] | `seen=set()` dedup طاغي — لازم consecutive-only dedup + 3-condition stop | `seen` بيمسح سطور متشابهة مش متكررة |
| #26 | [Script] | DOM re-render بيلزق كلمات — لازم '\n' فاصل قبل chunk جديد لو startswith فشل | "نورتنإيه" = "نورتني" + "إيه" من غير فاصل |
| #27 | [Debug] | `find_element(SEND_BUTTON)` بيرمي exception ف streaming → `aria-busy` مباشر أضمن | timeout 120ث بسبب send_enabled = False دايماً |
| #28 | [Script] | Radix UI dropdown بيفتح options كـ Portal في body مش جوا button — لازم `role="option"` مش ancestor::button | Arena.ai + أي موقع بيستخدم Radix UI / shadcn |
| #29 | [Script] | `div.no-scrollbar .prose` بيفرق رد AI عن رسالة المستخدم — الـ AI reply جوا no-scrollbar بس الـ user msg لأ | Arena.ai DOM structure |
| #30 | [Script] | Dead Code detection: `wait_for_reply` 30 سطر كانت موجودة ومش بتتستخدم — لازم `grep -r` على كل دالة قبل التسليم | Arena v1.1 Opt-Minus |
| #31 | [Config] | `@dataclass` + `os.getenv()` أفضل من class variables — بيدي env override + type hints + validation | Arena v1.2 Config refactor |
| #32 | [Script] | Default function arguments في Python بتتحسب **مرة واحدة** وقت التعريف مش كل استدعاء — لازم `None` + runtime check | Arena `stream_reply_live` timeout |
| #33 | [Script] | Retry loops لازم تستخدم `continue` مش `return None` — عشان تكمل باقي المحاولات | Arena re-send logic |
| #34 | [Config] | `WAIT_FOR_INPUT=False` افتراضياً أأمن للـ CI/Server — وتتفعل بـ env variable للتطوير | ChatGPT code review |
| #35 | [Script] | `last_popup_check` لازم يبدأ بـ `time.time()` مش `0` — عشان الحسبة الزمنية تبقى صح من أول iteration | Arena popup timing edge case |
| #36 | [Script] | Content-based detection أفضل من role/class selectors — بيدور على النص (“Login” + “Close”) مش الـ DOM attributes | Arena Login dialog مش عنده role=dialog |
| #37 | [Script] | `fast_type()` بـ JS أسرع 100x من `sb.type()` — بيحط القيمة مباشرة مع React nativeInputValueSetter + input/change events | DeepSeek Sign Up كان بطيء بـ sb.type() |
| #38 | [Script] | emailnator.com API بيولّد إيميلات gmail مؤقتة (dotGmail/plusGmail) + بيقرأ الرسائل — لازم GET الأول عشان XSRF-TOKEN | إنشاء حسابات DeepSeek أوتو |
| #39 | [Script] | الكود في رسائل DeepSeek جوا div بـ font-size:76px — regex `\b(\d{6})\b` بيستخرجه | قراءة كود التحقق من HTML الإيميل |
| #40 | [Script] | `arguments[]` في `execute_script()` آمن 100% مع أي quotes — f-string جوا JS ممكن يكسر لو النص فيه `'` أو `"` | fast_type + click_by_text_js + code fallback في deepseek_register v3 |
| #41 | [Script] | `sessionStorage` في DeepSeek بيحتفظ بالـ session بين الحسابات — `clear_all_cookies + clear_all_local_storage` مش كافيين — لازم JS `sessionStorage.clear()` + `delete_all_cookies` + `about:blank` بالترتيب فيه | لوب التسجيل v3.3 |
| #42 | [Script] | Emailnator بيربط الـ inbox بالـ session cookie — لازم تمرر نفس الـ client عبر email_client param | v3.4 Code Review |
| #43 | [Script] | في SeleniumBase لازم `run_loop` يدير SB context (فتح+قفل) بنفسه عشان يقدر يعمل restart — `sb_ctx.__exit__` + `SB().__enter__` الطريقة الصح | v3.5 Browser Restart |
| #44 | [Script] | التمر التنازلي `timeout - elapsed` يعطي remaining غلط — الأحسن `start = time.time()` وعرض (elapsed/timeout) + قراءة العداد من الصفحة | v3.6 Countdown Fix |
| #45 | [Script] | `success_streak` أفضل من total count للـ restart — عشان الفشل يصفر العداد + cooldown قبل restart بيدي الموقع فرصة يهدى | v3.7 Smart Restart |
| #46 | [Script] | لما تعدل ملف حسابات inline استخدم `tempfile.mkstemp` + `os.replace` (atomic write) — بيمنع تلف الملف لو crash | Login-Only v1.0 |
| #47 | [Script] | `send_keys()` و `fast_type()` كلاهما بيكتبوا في DOM بس **مش بيحدثوا React state!** الحل: `InputEvent` (مش `Event`) + `inputType: 'insertText'` + re-set كامل + blur | v3.8 Password Fix |
| #48 | [Script] | React بيضيّع آخر حرف من `send_keys` لأن الـ setState مش بيلحق — الحل: إعادة set القيمة كاملة بعد الحروف + `blur` event. اكتشفناه بسكريبت تشخيصي بيقرأ `__reactFiber$` من DOM | v3.8 Password Fix |
| #49 | [Script] | `verify_typed` كان بيعمل retry بـ `fast_type` فوق `sb.type` الصح — بيكتب DOM value صح بس يمسح React state! الحل: حذف `fast_type` من retry | v3.8 Password Fix |
| #50 | [Script] | `get_cookies()` في Selenium بيجيب cookies بس — **مش بيجيب localStorage!** DeepSeek بيحفظ `userToken` (JWT) في localStorage مش cookies → Session فاضية! الحل: `save_full_session` بـ `execute_script` يسحب localStorage كمان | Session v2 |
| #51 | [Script] | Pre-flight trick: لو فتحت `chat.deepseek.com` مباشرة React بيحمل ويكتشفك مش مسجل → لازم تفتح `robots.txt` الأول (خفيف) تحقن localStorage ثم تفتح الشات | Session v2 |
| #52 | [Script] | JS `el.value = 'text'` مش بيشتغل مع React controlled components — React بيشيل القيمة! الحل: `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set` (native setter) + `input` + `change` events | Arena Register v1.0 — React compatibility |
| #53 | [Script] | زر React submit ممكن يكون disabled لحد form validation يعدي — لازم `blur` event بعد كل input + `btn.disabled = false` في JS click + Enter key + `form.submit()` كـ fallbacks | Arena Register v1.1 — Finish button |
| #54 | [Script] | لو في زرين بنفس النص "Login" (واحد header + واحد submit) — `querySelectorAll('button')` بيلاقي الـ header الأول! الحل: فلتر بـ `button[type="submit"]` في JS عشان تضرب الـ submit بس | Arena Email Login v1.0 — Login submit vs header |
| #55 | [API] | zo.computer بيستخدم Magic Link (JWT ES256, 20 دقيقة expiry) مش password — `POST /api/email-login/request` + token في الإيميل + `POST /api/email-login/confirm` = auth cookies (access_token + refresh_token) | zo.computer Registration |
| #56 | [API] | SSE (Server-Sent Events) stream بيرجّع signup progress step-by-step — لازم `stream=True` + `iter_lines` + timeout ≥ 300s عشان الـ computer boot بياخد ~2-4 دقايق. لو timeout بس account اتعمل → كمّل عادي | zo.computer signup SSE |
| #57 | [Config] | `"provider"` في JSON = auto-detect من الدومين: gmail.com→emailnator, ridermail.shop→dropmailx, باقي→mailtm. مفيش hardcoded! | zo.computer v3.0 |
| #58 | [Config] | Mail.tm = الوحيد اللي ليه credentials قابلة للاسترجاع. `email_creds` بـ suffixed keys: `password_mailtm` / `token_mailtm` / `account_id_mailtm` — Emailnator مفيهوش | zo.computer v3.0 |
| #59 | [Performance] | Mail.tm magic link بيوصل في 0-3 ثواني (API polling) مقابل 6-30 ثانية في Emailnator. أسرع بكتير عشان مفيش XSRF dance | zo.computer v3.0 |
| #60 | [Config] | قاعدة تسمية الملفات: **register = بـ provider prefix** (`zo.computer_register.py`) / **refresh = بدون prefix** (`refresh.py`) / **accounts = بـ prefix** (`accounts_zo.computer.json`) — عشان register و refresh بيبدأوا بـ 're' فالـ prefix بيميّز | All providers |
| #61 | [Config] | لو اسم الـ module فيه `.` (زي `you.com_register.py`) → استخدم `importlib.util.spec_from_file_location()` بدل `from register import` عشان Python مش بتقبل dots في module names | you.com refresh.py |
| #62 | [Config] | Runable Dropmailx بيستخدم Livewire API: لازم `fingerprint` + `serverMemo` + `updates` في كل request + تحديث `htmlHash` + `checksum` من الرد | Runable refresh.py |
| #63 | [Config] | `EMAIL_PROVIDER` لازم تكون في كل سكربت + `--provider` في argparse + بتدعم rotation (`"mailtm"` / `"mailtm,emailnator"` / `"mix"`) — لو السكربت سابورت provider واحد بس، البنية التحتية لازم تكون موجودة | Mistral alignment |
| #64 | [Config] | Workflow files (`.agents/workflows/`) = قواعد بتتقري تلقائي من الـ AI — الحل عشان مينساش patterns إلزامية زي argparse و Config و pathlib | All providers |
| #65 | [Auth] | Ory Kratos refresh = **password login** (مش magic-link) — `GET /self-service/login/browser` → `POST /self-service/login?flow=` بالباسورد. أبسط من providers اللي بتستخدم magic-link (مش محتاج Emailnator/Dropmailx) | Mistral refresh |
| #66 | [Script] | AI auto-fix ممكن يدمر الكود بالكامل — لازم Length Guard يمنع أي shrink > 50% من الأصلي. المقارنة: 678L→51L = 92% reduction → blocked! | AI Code Generator Phase 2 |
| #67 | [Config] | Template files = golden scripts — ممنوع الكتابة عليها. لازم output يتحفظ في `generated/` subfolder لو template موجود (>200L) في نفس المجلد | AI Code Generator Phase 2 |
| #68 | [API] | AI21 verification email domain = `spmailtechno.com` — الرابط `post.spmailtechno.com/f/a/...` بيعمل redirect لـ `studio.ai21.com/auth/action?oobCode=...`. oobCode في query string | AI21 Email Verification |
| #69 | [API] | Firebase token refresh = `POST securetoken.googleapis.com/v1/token` مع `grant_type=refresh_token`. content-type = `application/x-www-form-urlencoded` (مش JSON!) | AI21 refresh.py |
| #70 | [Config] | Mail.tm domains بتتغير ديناميك (virgilian.com, حاجات تانية) — لازم `_detect_provider` يعتبر أي دومين مش gmail/ridermail = mailtm. مفيش hardcoded domains | AI21 register |
| #71 | [API] | AI21 `create_api_key` بيرجع `key_value` (مش `api_key` ولا `key`) — لازم تدور على `key_value` الأول! Response: `{"key_id": "...", "key_value": "...", "status": "ACTIVE"}` | AI21 register |
| #72 | [API] | AI21 `get_workspaces` بيرجع dict `{"workspaces": [...]}` مش list مباشرة — لازم handle الحالتين: `isinstance(data, list)` أو `data.get("workspaces")` | AI21 register |
| #73 | [Config] | LOOP CONFIG constants في `main()` argparse لازم defaults = الـ constants (LOOP_MODE/MAX_ACCOUNTS) — مش hardcoded `1` و `False`! `--no-loop` flag لـ override | AI21 register |
| #74 | [Config] | temp-mail.org domains بيتغيروا ديناميك (3dkai→fftube→flosek→niprack) — الحل: `_TEMPMAIL_DOMAINS: set` بيتملى تلقائي من `create()`. ممنوع hardcoded! | AI21 register |
| #75 | [API] | temp-mail.org API = `curl_cffi` + `impersonate="chrome124"` (مش requests عادي!) — `POST /mailbox` → `{mailbox, token}`, `GET /messages/{id}` → `bodyHtml` | AI21 register |
| #76 | [Script] | Email HTML body فيه روابط كتير — لازم تدوّر على href مع سياق ("Confirm") مش أي رابط sendgrid! `re.search(r'href=...>...Confirm', body)` أدق من `re.findall(link_pattern)` | Cohere besttemp |
| #77 | [API] | Livewire `fetchMessages` بيرجع messages nested: `[[{msg}], {"s":"arr"}]` — لازم flatten: `flat_msgs` بيهاندل dict و list recursively | BestTempEmail |
| #78 | [API] | Cohere redirect chain hop-by-hop: `allow_redirects=False` + loop 10 hops + check `r.cookies` + `verify_session.cookies` بعد كل hop — عشان access_token ممكن يتسيت في أي مرحلة | Cohere confirm flow |
| #79 | [API] | besttemporaryemail.com = Livewire app بـ CSRF. `wire:snapshot` HTML-encoded → `html.unescape` → JSON parse. الـ email بيتعملّه set عبر `updates: {"email": "xxx"}` في livewire/update (مش snapshot modification) | BestTempEmail Cohere |
| #80 | [Script] | في email التحقق من Cohere، في 6 روابط SendGrid. Link[0] = landing page (cohere.com). Link[1] = confirm button (dashboard.cohere.com/confirm-email). لازم regex يدوّر على `href` جنب "Confirm" مش أول match | Cohere verify link |
| #81 | [API] | Cohere مفيهوش `LoginWithEmail` API! Auth بالكوكيز بس من confirm redirect chain: SendGrid → 302 dashboard/confirm-email?token → 307 /api/auth/confirm_email → 303 (sets access_token+refresh_token cookies). لازم تتابع الـ redirects step-by-step مع `allow_redirects=False` | Cohere auth flow |
| #82 | [Agent] | `_compose_from_templates()` Template copy بيسيب endpoints القديمة — الحل: (1) regex base URL swap أولاً (مجاني) (2) `_has_template_urls()` يشيك لو لسه URLs غلط (3) `_ai_adapt_endpoints()` fallback + Length Guard. `_ai_review_code()` لازم ياخد HAR endpoints كـ reference عشان يقارن | v2 code_generator |
| #83 | [Config] | `monitor.py` كان فيه الكود كله مكرر مرتين (900 سطر!) — النسختين فيهم PROVIDERS مختلفة (you_com path + mistral/zo_computer). الحل: truncate للنسخة الأولى (395 سطر) + merge أفضل entries من الاتنين + إضافة cohere+ai21+mistral | monitor.py cleanup |
| #84 | [API] | temporary-mail.net محمي بـ Cloudflare — `requests` عادي مش هيعدي. `cloudscraper` = drop-in replacement بيعمل auto-solve لـ cf_clearance. Browser fingerprint: `{browser: chrome, platform: windows}` | tempnet integration |
| #85 | [API] | temporary-mail.net inbox polling = 3 خطوات مش 1: (1) `POST /get-mailbox` → email (2) `POST /activate-email` (3) **reload page** → extract `data-code` SHA256 hash (4) `POST /get-emails?lang=` + `{email, code}` → `{emails}` (5) `GET /mail/gmail-content/{id}` → HTML. بدون الـ reload+data-code = 400! | tempnet endpoint discovery |
| #86 | [Debug] | JS source analysis = أسرع من brute-force endpoints! `var currentLang = ""; fetch('/get-emails?lang=' + currentLang, {method: 'POST', body: {email, code}})` — لقيت الـ endpoint + الـ method + الـ body في 10 ثواني بدل ساعة brute-force | tempnet reverse engineering |
| #87 | [API] | Cohere auth flow = BlobheartAPI: `RegisterWithEmail` → confirm email via SendGrid redirect chain → `Session` → `AgreeToOnboarding` → `GetOrCreateDefaultAPIKey`. LoginWithEmail = fallback لو confirm مرجعش access_token | Cohere register+refresh |
| #88 | [Script] | Perplexity registration flow = Mail.tm + OTP: `POST /api/auth/signin-email` (useNumericOtp=true) → poll mail.tm → `POST /api/auth/signin-otp` → `GET /rest/auth/refresh_perplexity_jwt` → Bearer JWT. Mobile API headers: `x-client-name: Perplexity-Android` + `x-app-version: 2.75.2` | Perplexity register |
| #89 | [Config] | Hardcoded tokens في chat scripts = anti-pattern! `TokenManager` بيحمّل من JSON + auto-switch لو 401/403 + atomic write لـ status update. مفيش AUTH_TOKEN في الكود! | Perplexity chat token rotation |
| #90 | [API] | Models بتموت على Perplexity بدون إنذار — `command_r_plus` + `mistral_large` + `gemini31pro` + `gemini3pro` كانوا شغالين وبقوا EMPTY. لازم `_test_failed.py` يتشغل دوري عشان نكتشف الميتين | Dead model discovery |
| #91 | [Performance] | Round-robin token rotation = فرق دراماتيكي: 49% → 91% success rate. المشكلة مكنتش الموديلات — المشكلة كانت rate limiting على token واحد! 19 حساب × 2 models/account = مثالي | Token rotation strategy |
| #92 | [Config] | `pplx_pool.py` كـ shared module أفضل من كل ملف يعمل import لـ `perplexity_chat.py` — مكان واحد للـ API logic + token rotation + model tiers. Backward compatible: `perplexity_chat.py` لسه شغال كـ fallback | Shared module pattern |
| #93 | [Script] | ERNIE `osfuid` = ephemeral per-session — **ليس قابل للإعادة الاستخدام**. مرتبط بـ BAIDUID + jnmq fingerprinting. الحل: Playwright UI automation تخلّي JS يبعت الـ requests من داخل نفس الـ session | ERNIE errno:-1 debug |
| #94 | [Script] | ERNIE `button#sendCodeBtn` بيحتاج fields تتمفعّل أولاً (click email → click password) قبل ما الزرار يظهر clickable — React controlled component behavior | ERNIE Get Code button |
| #95 | [API] | ERNIE `reg/email` بيستخدم `verify_code` مش `code` في الـ body. الـ response بيحتوي `osduss` cookie = نجاح التسجيل. بعدها لازم click "Get Started" لتفعيل الـ full session | ERNIE registration |
| #96 | [API] | ERNIE endpoint `/eb/conversation/chat` بيرجع `code:1` (rate limit) دايماً — الـ endpoint الحقيقي `/eb/chat/conversation/v2` اتاكّد من Burp capture. بيشتغل بدون Acs-Token! | ERNIE Chat endpoint discovery |
| #97 | [Script] | ERNIE SSE `event:thought` عنده `is_end:1` = نهاية التفكير ≠ نهاية الرد! الـ parser كان بيبرك بدري. الحل: track `current_event` وأNP break بس على `event:message` is_end:1 | ERNIE Chat SSE parser |
| #98 | [Script] | ERNIE SSE `event:thought` ممكن يستمر 60+ ثانية (deepThoughtStatus:2 = auto thinking) — الـ timeout لازم يكون ≥120s. بعد التفكير بييجي `event:step` ثم `event:message` | ERNIE Chat response timing |
| #99 | [API] | Grok OTP code بيتبعت بـ dash: `CPN-8NX` — الـ gRPC `VerifyEmailValidationCode` بيرجع `grpc-status:3` لو الكود فيه dash | الأعراض: invalid code error | السبب: Grok API بيتوقع alphanumeric بدون dashes | الحل: `code.replace("-", "").upper()` تلقائي | ✅ محلولة |
| #100 | [API] | Grok OTP code بتنتهي صلاحيته بسرعة (~18 دقيقة) | الأعراض: `grpc-status:5` — code expired | السبب: تأخر في إدخال الكود | الحل: auto-polling بمجرد ما OTP يوصل + إدخال فوري | ✅ محلولة |
| #101 | [Auth] | Grok `/sign-up` Server Action بيطلب Cloudflare Turnstile token إلزامي | الأعراض: `Failed to verify Cloudflare turnstile token` | السبب: Next.js Server Action محمي بـ Turnstile (مش gRPC) | الحل: Hybrid approach — SeleniumBase مرة واحدة بس تجيب التوكن | ✅ محلولة |
| #102 | [API] | إيميل `onishashakeia3736+dell@gmail.com` كان مسجّل already في Grok | الأعراض: `grpc-status:3` — already registered | السبب: الإيميل اتسجّل قبل كده | الحل: إيميل جديد مؤقت + فحص already registered في `send_otp()` | ✅ محلولة |
| #109 | [Script] | `ThreadPoolExecutor` UnboundLocalError في batch mode | `NameError` لما الـ batch mode بيحاول يستخدم ThreadPoolExecutor | كان في local import داخل multi block بيكتب فوق الـ global import | شيلنا الـ local import واستخدمنا الـ global من أعلى الملف | ✅ محلولة |
| #110 | [Auth] | أزرار React/Next.js في تسجيل Cursor تتجاهل النقر العادي بـ SeleniumBase | فشل استكمال الخطوات عند `Continue with email code` | `sb.click()` لا ينتج عنه `userGesture` كافي لمطابقة حالة React | إضافة `cdp_eval` واستخدام `Runtime.evaluate` لتمرير `userGesture: true` | ✅ محلولة |
| #111 | [Script] | الرغبة في تفعيل نموذج Claude Opus 4.6 1M مدفوع (Ultra mode) في Genspark | السكريبت بيطلب default models بس وماعندوش اوبشن للموديل ده | نموذج Ultra بيتطلب key `use_model` مكنش موجود في الـ payload الأساسي | إضافة خاصية `--ultra` لحقن `"use_model": "claude-opus-4-6-1m"` بسلاسة عند اختيار المود المتقدم | ✅ محلولة |
| #112 | [Security] | منع إرسال SMS OTP بالكامل في Oysho لعدم اجتياز حماية Akamai Bot Manager | استجابة بخطأ 403 (action: 0, code: 4) من الـ Edge | ريكويست Pure HTTP يفتقر لـ Sensor Data صالحة تملأ كوكيز `_abck` لتصبح `~0~` | بناء نظام هجين للـ Session Handoff (Browser -> curl_cffi) لتمرير الكوكيز والـ Bearer Token سوياً | ✅ محلولة |
| #113 | [Prompt] | ملف الـ Prompt التشخيصي القديم لم يغطي التشخيص المتقدم لـ WebSocket/gRPC والـ False Positives | تخبط الـ AI في تشخيص أكواد مثل 1006 أو `200 OK` في gRPC | عدم وجود SSOT شامل يجمع 16000 سطر من الملاحظات التراكمية | تحويل وتصفية 15900 سطر إلى 169 Section في `WAF_BOT_DIAGNOSTIC_MASTER_PROMPT.md` | ✅ محلولة |
| #114 | [Security] | فشل إرسال SMS OTP في Oysho بنسخ Pure HTTP | استجابة 403 Access Denied بدون أي رسائل تفصيلية | حماية Akamai Edge تحظر الطلبات التي لا تحتوي على `_abck` صالح | دمج `oysho_full_flow.py` الهجين (Browser Session 5 ثواني لجمع הבصمة ثم curl_cffi للإرسال السريع) | ✅ محلولة |
| #115 | [Security] | استحالة إنشاء حساب Clarifai بـ Pure HTTP | استجابة بخطأ 11102 (captcha token required) | Clarifai يفرض التحقق من reCAPTCHA v3 على واجهة برمجة التطبيقات الخاصة بالتسجيل | تم توثيقها، والانتقال إلى المنصات المعتمدة على Firebase مثل Lovable كبديل أسهل | ✅ محلولة (بناء على التحليل) |

---

## 🔮 خارطة الطريق

```
Phase 1: DeepSeek Browser Script         ✅ تم
Phase 2: DeepSeek Provider Functions     ✅ تم (ask + generate + stats)
Phase 3: Code Review + Issue Detection   ✅ تم (9 مشاكل وُثقت)
Phase 4: Critical Fixes                  🔄 جاري
Phase G1: Gemini Login Automation        ✅ تم (Login + Model)
Phase G2: Gemini Send Message            ✅ تم
Phase G3: Gemini Wait + Read Reply       ✅ تم
Phase G4: Gemini Provider Integration    🔜 الخطوة الجاية
  - asyncio.to_thread() في ask/generate  ⏳ قادم
  - Credentials في .env                  ⏳ قادم
  - BaseProvider inheritance             ⏳ قادم
Phase A1: Arena Bot v1.1 Opt-Minus       ✅ تم
Phase A2: Arena v1.2 — 5 Fixes           ✅ تم
Phase A3: Arena v1.3 — Login Dialog      ✅ تم
Phase D1: DeepSeek Register v1            ✅ تم (يدوي)
Phase D2: DeepSeek Register v2 Auto       ✅ تم (emailnator + كود تلقائي)
Phase D3: DeepSeek Register v3 Refactor   ✅ تم (8 إصلاحات + pathlib + arguments[] + verify)
Phase D4: Nuclear Session Reset           ✅ تم (JS storage + delete_cookies + about:blank)
Phase D5: Config-driven Loop             ✅ تم (MAX_ACCOUNTS=3 ← 3 حسابات | 0 ← ∞)
Phase D6: v3.4 Code Review (5 AIs)       ✅ تم (10 إصلاحات: reuse+fail_limit+SW+IDB)
Phase D7: v3.5 Browser Restart            ✅ تم (كل N محاولات + temp cleanup)
Phase D8: v3.6 Countdown Fix              ✅ تم (_get_resend_countdown + elapsed/timeout log)
Phase D9: v3.7 Smart Restart              ✅ تم (success_streak + fail cooldown)
Phase D10: Login-Only v1.0                ✅ تم (732→240 سطر + atomic mark + CLI)
Phase D11: v3.8 Password Fix              ✅ تم (react_type + InputEvent + آخر حرف محتاج تجربة)
Phase D12: Reset Password v1.0            ✅ تم (forgot_password + Emailnator + react_type + mark)
Phase D13: Session v2 Full                ✅ تم (cookies+localStorage+sessionStorage + Pre-flight)
Phase D14: Register + Session              ✅ تم (save_full_session بعد register مباشرة)
Phase D15: Single JSON                     ✅ تم (accounts_deepseek.json بدل TXT+sessions/)
Phase D16: Session Keeper v1.0             ✅ تم (check→do_reset→login→update JSON + last_refreshed)
Phase D17: Session Keeper تحسينات         ⏳ قادم (shared.py / file_lock / fail_count policy)
Phase G-1: Groq Token Generator v2.0      ✅ تم (Magic Link + API Key + clear_session + human_delay + loop)
Phase G-2: Groq Generator v2.1            ✅ تم (colorama + أي فشل=restart + stats panel + MAX_CONSECUTIVE_RESTARTS)
Phase G-3: Groq Tester v2.0               ✅ تم (models list + rate limits + chat + Config.DEFAULT_PROMPT + kimi-k2)
Phase A-1: AIChatApp Client v1.0          ✅ تم (pure requests + Firebase login + auto-refresh + POST /chat شغل!)
Phase P-1: Pollinations Client v1.0       ✅ تم (sk_ key + auto-create + claude-sonnet-4.6 + models + prompt file)
Phase P-2: Pollinations v1.2              ✅ تم (persistent history + token tracking + /clear /usage + --clear-history)
Phase AR-1: Arena Account Creator v1.1    ✅ تم (Mail.tm + SeleniumBase + 10-step signup + React-compatible input + 4-strategy Finish)
Phase AR-2: Arena Session Verifier v1.0   ✅ تم (حقن cookies + User Profile check + token extract + chat test)
Phase AR-3: Arena Email Login v1.0        ✅ تم (browser login + session refresh + last_updated + --email/--all)
Phase ZO-1: Zo Computer Register v1.0     ✅ تم (pure requests! Emailnator + Magic Link + SSE signup + verify)
Phase ZO-2: Zo Computer v2.0              ✅ تم (you.com pattern: CLI + Config + loop + stats + provider field)
Phase ZO-3: Zo Computer v3.0              ✅ تم (Mail.tm + auto-detect + email_creds + rotation + --provider CLI)
Phase ZO-4: Monitor Integration            ✅ تم (refresh.py + monitor.py + accounts_zo.computer.json)
Phase CO-1: Cohere + BestTempEmail          ✅ تم (BestTempEmailClient + verify link + confirm redirect chain + API key 16s!)
Phase CO-2: Cohere Register v1.1            ✅ تم (6 integration points + default=besttemp + hop-by-hop confirm)
Phase M-1: Monitor Cleanup v2.4           ✅ تم (900→395 سطر + حذف duplicate + 9 providers: arena,deepseek,groq,you_com,zo_computer,runable,cohere,mistral,ai21)
Phase SH-1: Shared Library v1.0            ✅ تم (shared/ui.py + shared/io.py + shared/delay.py — step/ok/fail/warn + atomic_save/load_accounts/upsert_account + human_delay)
Phase CO-3: Cohere Fixes v1.1              ✅ تم (dead code cleanup + login fallback + email_creds support)
Phase CO-4: Cohere Refresh                  ✅ تم (BlobheartAPI: LoginWithEmail → Session → GetOrCreateDefaultAPIKey)
Phase TN-1: temporary-mail.net v1.0         ✅ تم (TemporaryMailNetClient + cloudscraper + /get-emails?lang= + data-code)
Phase TN-2: Endpoint Discovery              ✅ تم (JS reverse engineering + 6 brute-force attempts → correct flow)
Phase PX-1: Perplexity Register v1.0        ✅ تم (Mail.tm + OTP + JWT + curl_cffi + CLI + 100% success)
Phase PX-2: Perplexity Chat v2.0            ✅ تم (44 models + DEFAULT_MODEL + interactive)
Phase PX-3: Token Rotation                  ✅ تم (TokenManager + auto-switch 401/403 + account/next/reload)
Phase 5: Session Reuse (Performance)     ⏳ قادم
Phase 6: Register في ProviderManager     ⏳ قادم
Phase 7: RAG Integration                 ⏳ قادم
```

---

## 📊 Provider Status

| Provider | النوع | الحالة | API Key |
|----------|-------|--------|---------|
| OpenAI | API | ✅ مسجل | `OPENAI_API_KEY` |
| Gemini | API | ✅ مسجل | `GEMINI_API_KEY` |
| Together | API | ✅ مسجل | `TOGETHER_API_KEY` |
| Anthropic | API | ✅ مسجل | `ANTHROPIC_API_KEY` |
| Groq | API | ✅ مسجل | `GROQ_API_KEY` |
| **DeepSeek** | **Hybrid** | ✅ Register v2 (37+ حساب) — Browser Open + fetch لـ send_code + UI لـ register | Emailnator | accounts_deepseek.json |
| **Zo Computer** | **Requests** | ✅ Register only | Magic Link (no password) |
| **Cohere** | **Requests** | ✅ Register + API Key (16s!) | BestTempEmail (Livewire) |
| **temporary-mail.net** | **Requests** | ✅ tempnet provider (Gmail aliases) | cloudscraper (Cloudflare bypass) |
| **Perplexity** | **Requests** | ✅ Register + Chat (32 models) + pplx_pool Token Rotation (19 acc) | Mail.tm OTP + curl_cffi |
| **ERNIE Bot** | **Playwright + Requests** | ✅ Register (Playwright UI) + Chat (pure requests /eb/chat/conversation/v2 + SSE) | Emailnator @gmail.com + osduss cookies |
| **Grok (x.ai)** | **Hybrid (curl_cffi + SeleniumBase)** | ✅ Register (gRPC-web + Turnstile) | mailtm/emailnator/tempmail |

---

## 🔧 Troubleshooting — أشهر المشاكل وحلولها

| المشكلة | السبب | الحل السريع |
|---------|-------|------------|
| `asyncio` event loop blocked | Selenium sync داخل async | `asyncio.to_thread()` |
| Chrome مش بيفتح `Port 9222` | Chrome قديم شغال + `user_data_dir` | اقفل Chrome من Task Manager |
| Cloudflare Human Verification | `navigator.webdriver=True` | `uc=True` في SeleniumBase |
| Qdrant connection refused | Docker مش شغال | `docker start qdrant` |
| Provider returns `None` | API key غلط أو quota | افحص `.env` + جرب provider تاني |
| رد DeepSeek ناقص | بتاخد `span[-1]` بس | خد `MSG_CONTAINER.text` كامل |
| السكربت بيقول "خلص" بدري | text stability مع Search mode | Button Counting — 5 أزرار `db183363` |

---

## ❓ FAQ — أسئلة شائعة

**Q: ليه DeepSeek مش بـ API؟**
> A: DeepSeek API مدفوع — البراوزر مجاني 100%

**Q: ليه كل request بيعمل browser جديد؟**
> A: Session Reuse مش متنفذة لسه (Phase 5) — بطء مؤقت

**Q: إزاي أضيف provider جديد؟**
> A: اتبع الـ Provider Pattern في `GEMINI.md` — خطوتين بس

**Q: الـ Selectors بتاعة DeepSeek بتتغير؟**
> A: أيوه، كل update → افحص `div.db183363` و `div.ds-markdown`

**Q: إزاي أعمل rollback لو حاجة اتكسرت؟**
> A: `git checkout HEAD -- .` يرجع كل حاجة للـ commit الأخير

---

## ⚠️ Known Limitations — حدود النظام الحالي

| القيد | السبب | الحل المخطط |
|-------|-------|------------|
| DeepSeek Browser بطيء (15-30 ثانية/request) | Browser session جديد كل مرة | ✅ **تم الحل**: `deepseek_chat.py` Pure Requests — 1.5s/request! |
| DeepSeek مش في ProviderManager | لسه standalone | Phase 6 (اختياري) |
| Selectors بتتغير مع كل DeepSeek update | Hashed CSS classes | XPath fallback — يؤثر على browser version بس |
| مفيش tests تلقائية | لسه مش متضافة | CI/CD قادم |

---

<!-- آخر رقم مشكلة مستخدم: #112 -->

---

## 🏆 إنجازات ERNIE v2.9

| # | الإنجاز | الملفات |
|---|---------|--------|
| 1 | ernie_register.py — 6 email providers (emailnator/mailtm/tempmail/tempnet/besttemp/dropmailx) + mix rotation + CLI | `ernie.baidu/ernie_register.py` |
| 2 | ernie_chat.py — `--model EB50/EB35/ERNIE-4.5` + `--no-think` (15s بدل 72s) | `ernie.baidu/ernie_chat.py` |
| 3 | refresh.py [NEW] — `def refresh(email)->bool` + test osduss + colorama output | `ernie.baidu/refresh.py` |
| 4 | monitor.py — ERNIE مسجّل كـ provider #10 (osduss cookie كل 48h) | `monitor.py` |
| 5 | v2 (32 models) — osfuid analysis (3/16 ردوا: SHA1 fingerprint + jnmq) | `ernie.baidu/v2_osfuid_analysis.json` |

### 📁 ملفات جديدة/معدّلة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `ernie.baidu/ernie_register.py` | تسجيل حسابات ERNIE — 6 email providers | ✅ |
| `ernie.baidu/ernie_chat.py` | Chat client — pure requests + SSE | ✅ |
| `ernie.baidu/refresh.py` | اختبار osduss cookie — monitor compatible | ✅ [NEW] |
| `monitor.py` | ERNIE = provider #10 | ✅ معدّل |

### 🐛 مشاكل

| #103 | [Script] | ERNIE osfuid errno:-1 | Playwright fresh session بيرجع errno:-1 من send_code | osfuid = SHA1 browser fingerprint من jnmq — Playwright مش بيولّده | تحميل bundle.u.php + jnmq قبل send_code | ⏳ |

### 📖 دروس

| #رقم | [TAG] | الدرس | السياق |
| 69 | [Security] | لو الـ Traffic capture مفيهوش ريكويستات الـ Auth، غالباً الـ App بيستخدم WebView Captcha أو بيعمل Device Fingerprint بيوقف الـ Flow قبل إرسال الـ API Call. | تحليل RedotPay |
|------|-------|-------|-------|
| 61 | [Script] | كل email provider لازم يكون ليه `generate_email()` + `wait_for_code()` + `get_creds()` — unified interface | ERNIE register 6 providers |
| 62 | [Performance] | `deepThoughtStatus: 0` في ERNIE = بدون تفكير = 15s بدل 72s — فرق 5x | ernie_chat --no-think |

---

## 🏆 إنجازات ERNIE v3.0

| # | الإنجاز | الملفات |
|---|---------|--------|
| 6 | ernie_playwright.py — Playwright كامل مع كل قواعد UNIVERSAL_PROVIDER_PROMPT (colorama + Config dataclass + argparse كامل + banner عربي + loop فعلي + atomic write + accounts.json fields) | `ernie.baidu/ernie_playwright.py` |
| 7 | ernie_chat.py — model IDs حقيقية من Burp (EB50, X1_1, EB50-ARENA-LOW-260110, EB50-ARENA-HIGH-1220) + اختيار موديلات تفاعلي | `ernie.baidu/ernie_chat.py` |
| 8 | اختبار كل الـ 4 ERNIE models بنجاح (HTTP 200 + response text) | `ernie.baidu/تييييست/test_all_models.py` |
| 9 | GEMINI.md — إضافة Register Script Checklist إجباري (52 سطر) مع email providers فعلية | `GEMINI.md` |
| 10 | ERNIE مسجّل كـ provider #12 في UNIVERSAL_PROVIDER_PROMPT | `UNIVERSAL_PROVIDER_PROMPT.md` |

### 📁 ملفات جديدة/معدّلة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `ernie.baidu/ernie_playwright.py` | انشاء حسابات ERNIE — Playwright + كل القواعد | ✅ [NEW] |
| `ernie.baidu/ernie_chat.py` | اختيار موديلات تفاعلي + model IDs صح | ✅ معدّل |
| `GEMINI.md` | Register Script Checklist (52 سطر) | ✅ معدّل |
| `UNIVERSAL_PROVIDER_PROMPT.md` | ERNIE = provider #12 | ✅ معدّل |

### 🐛 مشاكل

| #104 | [Config] | ERNIE model IDs غلط | الـ 4 models مش بيردوا نص | API IDs كانت مخمّنة مش حقيقية | HAR capture من Burp لقينا: EB50, X1_1, EB50-ARENA-LOW-260110, EB50-ARENA-HIGH-1220 | ✅ |

### 📖 دروس

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 63 | [Script] | تعليقات الكود لازم عربي كامل — مفيش `# OTP timeout` لازم `# مهلة انتظار كود التحقق` | ERNIE register checklist |
| 64 | [Config] | `LOOP_MODE = True` هو الـ default — `--no-loop` flag للإيقاف | ERNIE playwright loop |
| 65 | [Config] | كل email provider في choices لازم يكون ليه class فعلية — مش بس اسم! | Register Script Checklist |

---

## 🏆 إنجازات ERNIE v3.1 — Login + Refresh + Monitor Relogin

| # | الإنجاز | الملفات |
|---|---------|--------|
| 11 | ernie_login.py — Playwright login مستقل (5 phases: osfuid → login → email → password → osduss) — 16 cookie | `ernie.baidu/ernie_login.py` |
| 12 | refresh.py دمج كامل — playwright_login() مدموجة + --login CLI + relogin تلقائي لو cookies انتهت | `ernie.baidu/refresh.py` |
| 13 | refresh.py بيبعت كل الـ 16 cookie (مش osduss بس) — SSE test حقيقي | `ernie.baidu/refresh.py` |
| 14 | monitor.py — force_refresh لـ no_cookie/refresh_failed/expired بدل تخطيها | `monitor.py` |
| 15 | monitor.py — needs_refresh() يدعم ISO+timezone format (fromisoformat) | `monitor.py` |
| 16 | 9 اختبارات كاملة نجحت (--list, --help, --login, --all, monitor dry-run, no_cookie relogin) | كل الملفات |

### 📁 ملفات جديدة/معدّلة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `ernie.baidu/ernie_login.py` | Playwright login مستقل — قابل للاختبار اليدوي | ✅ [NEW] |
| `ernie.baidu/refresh.py` | refresh + login مدموجين — --login --password --headless --no-save | ✅ معدّل بالكامل |
| `monitor.py` | ERNIE force_refresh + ISO timezone parsing | ✅ معدّل |

### 🐛 مشاكل

| #106 | [Script] | refresh.py بيبعت osduss بس | SSE فاضي أو rate_limited | كان بيبعت cookie واحدة (osduss) بدل كل الـ 16 | إرسال كل الكوكيز من cookies dict | ✅ |
| #107 | [Config] | PowerShell BOM يكسر JSON | json.loads فشل بـ "Unexpected UTF-8 BOM" | PowerShell Set-Content بيضيف BOM | استخدام Python بدال PowerShell لتعديل JSON | ✅ |
| #108 | [Script] | monitor مش بيفهم ISO+timezone | "format غلط: +00:00" | strptime مش بيدعم timezone offset | fromisoformat() كـ primary parser + fallback strptime | ✅ |

### 📖 دروس

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 66 | [Script] | refresh.py لازم يبعت كل الكوكيز المحفوظة — مش osduss بس! الموقع بيتحقق من BAIDUID + osfuid كمان | ERNIE refresh cookies |
| 67 | [Config] | PowerShell Set-Content بيضيف UTF-8 BOM دايماً — استخدم Python لتعديل JSON بدلًا منها | BOM JSON parse error |
| 68 | [Script] | datetime.fromisoformat() هي الأفضل لـ parsing — بتدعم كل الـ formats (T + microseconds + timezone) | monitor ISO parsing |

---

## 🏆 إنجازات DeepSeek Chat Client v1 — Pure Requests (بدون Browser!)

<!-- آخر رقم مشكلة مستخدم: #112 -->

| # | الإنجاز | الملفات |
|---|---------|--------|
| 1 | WAF bypass بـ Android headers + curl_cffi `safari15_3` — بدون Selenium أو Browser | `ديب سيك/deepseek_chat.py` |
| 2 | WASM PoW Solver — حل SHA3/Keccak DeepSeekHashV1 بـ wasmtime في Python (~0.05s) | `ديب سيك/sha3_wasm_bg.wasm` |
| 3 | Account Fallback: disk cache → file tokens → email+password — ترتيب أولوية ذكي | `deepseek_chat.py` |
| 4 | Auto-Relogin عند 401/403 — retry مع `max_retries` بدون انقطاع | `deepseek_chat.py` |
| 5 | Token Cache على disk `~/.deepseek_token_cache.json` — صالح 24h | `deepseek_chat.py` |
| 6 | Multi-Turn Conversation: نفس session_id + parent_message_id من SSE → الـ model يتذكر السياق | `deepseek_chat.py` |
| 7 | Stats Tracking: tokens/time/thinking_chars/answer_chars بعد كل رسالة | `deepseek_chat.py` |
| 8 | CLI كامل: `/think /search /both /normal /status /history /clear /stats /help` | `deepseek_chat.py` |
| 9 | PoWSolver class — WASM Module يتحمل مرة واحدة في __init__ (zero disk I/O per message) | `deepseek_chat.py` |
| 10 | PoW Pre-fetch — background thread يجلب PoW بينما المستخدم بيكتب → 0ms wait | `deepseek_chat.py` |
| 11 | Speed Test: Disk Cache أسرع < Token (440ms) < Email/Password (667ms) | `deepseek_chat.py` |
| 12 | اختبار كل الـ 4 Combinations: Normal/Think/Search/Think+Search ✅ | `test_combinations.py` |

### 📁 ملفات جديدة/معدّلة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `ديب سيك/deepseek_chat.py` | Chat client كامل — Config + Auth + PoW + SSE + CLI | ✅ [NEW] |
| `ديب سيك/sha3_wasm_bg.wasm` | WASM module لحل PoW (26KB) | ✅ [NEW] |
| `ديب سيك/accounts_deepseek.json` | حسابات DeepSeek (email + password + token) | ✅ [NEW] |
| `ديب سيك/test_combinations.py` | اختبار الـ 4 modes بالتوازي | ✅ [NEW] |

### 🐛 مشاكل

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|-------|
| #109 | [Script] | SSE parser بيرجع جزء من الرد بس | الرد = كلمة واحدة ("The" / "Why") | أول chunk فيه full format `{"p":"response/content","o":"APPEND","v":"text"}`, باقي chunks = shorthand `{"v":"text"}` — الـ parser مكانش بـ handle shorthand | إضافة `streaming_mode` + shorthand detection بدون `p` field | ✅ |
| #110 | [Config] | session_id parsing غلط | chat API فشل بـ UUID error | كنا نقرأ `biz_data.chat_session.id` بدل `biz_data.id` | قراءة `biz_data.id` مباشرة | ✅ |
| #111 | [Script] | Multi-turn لا يتذكر السياق | "لا أعرف اسمك" بعد ما قلناله | `parent_message_id` ما كانش بيتبعت — `response_message_id` محتاج يتاخد من SSE | قراءة `response_message_id` من SSE stream + استخدامه كـ parent_message_id التالي | ✅ |

### 📖 دروس مستفادة

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 69 | [API] | DeepSeek SSE format: أول chunk = full JSON Patch `{"p","o","v"}`, باقي chunks = shorthand `{"v":"text"}` فقط — الـ parser لازم يعرف الاتنين | DeepSeek SSE stream |
| 70 | [API] | DeepSeek PoW = SHA3/Keccak عبر WASM — ممكن تحله في Python بـ wasmtime بدون browser تماماً | deepseek_chat PoW |
| 71 | [API] | Android mobile headers بتتخطى WAF DeepSeek — `User-Agent: DeepSeek/1.0.13 Android/35` + `x-client-platform: android` | WAF bypass |
| 72 | [Performance] | WASM module يتحمل مرة واحدة في __init__ — مش في كل request. دي توفر disk I/O | PoWSolver caching |
| 73 | [Performance] | PoW Pre-fetch في background thread: يوفر ~70ms لكل رسالة — token جاهز قبل ما المستخدم يضغط Enter | pre-fetch pattern |
| 74 | [API] | `response_message_id` من SSE هو parent لأي رسالة تالية في نفس الـ session — ده هو multi-turn الحقيقي | DeepSeek multi-turn |
| 75 | [Script] | الاعتماد المستمر على مزود إيميل واحد يُعرّض الأتمتة لخطر الانهيار بسبب حظر الدومين. وجود `_ManualClient` يعطي المهاجم استراتيجية بقاء قوية. | أتمتة Cursor AI |
| 76 | [Security] | الحظر القاطع من Akamai بـ (403 json action:0) يتطلب بيئة متصفح لتوليد Sensor Data فعلية. الحل الفعّال والسريع هو Session Handoff والتخلص من المتصفح فوراً بعد تخطي التحدي. | Oysho Akamai Bypass |

---

## 🏆 إنجازات DeepSeek Chat Client v1.1 — refresh.py Android Upgrade

| # | الإنجاز | الملفات |
|---|---------|--------|
| 1 | ترقية refresh.py من Chrome web headers → Android mobile headers (بتتخطى WAF!) | `ديب سيك/refresh.py` |
| 2 | استبدال `requests` بـ `curl_cffi` + `impersonate="safari15_3"` في refresh | `ديب سيك/refresh.py` |
| 3 | ترقية `_verify_token()` للـ Android headers + curl_cffi (بدل requests) | `ديب سيك/refresh.py` |
| 4 | حفظ `token` مباشرة في `acc["token"]` للتوافق مع `deepseek_chat.py` | `ديب سيك/refresh.py` |
| 5 | SSE debug مع search=True — اكتشاف إن Search Results بتندمج في نص الرد (مفيش path منفصل) | `ديب سيك/debug_search.py` |

### 📁 ملفات محدّثة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `ديب سيك/refresh.py` | Android v3 — curl_cffi + Android headers بدل Chrome | ✅ معدّل |

### 🐛 مشاكل

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|-------|
| #112 | [Script] | refresh.py فقد BASE_URL/LOGIN_API/VERIFY_API أثناء الترقية | `name 'LOGIN_API' is not defined` | الـ replace chunk أزال الـ constants بالغلط | إعادة إضافتها قبل ANDROID_HEADERS | ✅ |

### 📖 دروس مستفادة

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 75 | [API] | DeepSeek Search Results مفيش SSE path منفصل لها — بتندمج في نص الرد تلقائياً | SSE debug with search=True |
| 76 | [Script] | refresh.py محتاج `acc["token"]` = raw token string (مش JSON wrapped) للتوافق مع `deepseek_chat.py` | refresh token format |

---

## 🏆 إنجازات Runable Compliance Fix + Zo.computer Refresh v2

| # | الإنجاز | الملفات |
|---|---------|--------|
| 1 | إصلاح 5 حسابات Runable بدون `provider` — auto-detect من الدومين | `accounts_runable.json` |
| 2 | Atomic write بدل `open().write()` المباشرة في Runable register | `runable_register.py` |
| 3 | إضافة `EMAIL_PROVIDERS` list + `OTP_TIMEOUT` constant | `runable_register.py` |
| 4 | argparse كامل: `--max --no-loop --delay --timeout --provider --list --count --headless` | `runable_register.py` |
| 5 | دالة `list_accounts()` + `--list` CLI — جدول ملون بـ 353 حساب | `runable_register.py` |
| 6 | Zo.computer refresh.py v2 — 3-layer pattern قابل للتوسع | `zo.computer/refresh.py` |
| 7 | إصلاح 8 fields في zo.computer accounts (provider + expires_in) | `accounts_zo.computer.json` |
| 8 | 17/17 اختبارات ناجحة على refresh.py الجديد | `test_zo_refresh_full.py` |

### 📁 ملفات محدّثة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `Runable/HHHAAARR/runable_register.py` | atomic save + argparse + list_accounts + EMAIL_PROVIDERS | ✅ معدّل |
| `Runable/HHHAAARR/accounts_runable.json` | provider field لـ 5 حسابات قديمة | ✅ معدّل |
| `zo.computer/refresh.py` | v2 — 3-layer pattern + REFRESH_LAYERS registry + تعليقات عربية | ✅ معدّل |
| `zo.computer/accounts_zo.computer.json` | provider + expires_in لـ 4 حسابات | ✅ معدّل |

### 🐛 مشاكل

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|-------|
| #113 | [API] | Runable API endpoint اتغيّر — magic-link 404 | `POST /api/auth/sign-in/magic-link → 404` | Runable غيّرت الـ auth backend | محتاج HAR جديد | ⏳ |
| #114 | [Script] | `pathlib` مش مستورد في runable_register.py | `NameError: name 'pathlib' is not defined` | نسيناه في imports بعد إضافة atomic save | إضافة `import pathlib` في سطر 14 | ✅ |
| #115 | [API] | Zo.computer مش بتدعم refresh_token endpoint | كل الـ 4 endpoints رجعت 404 | مفيش /api/auth/refresh-token على Zo | نفضل على magic-link pattern | ✅ |

### 📖 دروس مستفادة

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 77 | [Script] | `EMAIL_PROVIDERS` list لازم تتطابق مع الـ classes الحقيقية في السكريبت — مفيش phantom choices | Runable register compliance |
| 78 | [Script] | Atomic write (`.tmp → .replace()`) إلزامي لأي ملف JSON بيتحدث runtime — منع فقدان البيانات | Runable + Zo save_accounts |
| 79 | [API] | Zo.computer مش بتدعم refresh_token رغم إنها بتبعت واحد في الـ cookies — لازم magic-link دايماً | Zo refresh_token test |
| 80 | [Script] | نمط REFRESH_LAYERS (list of tuples) قابل للتوسع — لإضافة layer جديد: سطرين بس + function | Zo refresh.py v2 |

---

## 🏆 إنجازات CAPTCHA Service v4 — ocr.z.ai Integration

<!-- آخر رقم مشكلة مستخدم: #115 -->

| # | الإنجاز | الملفات |
|---|---------|--------|
| 1 | `captcha_solver.py` — سكربت واحد لكل حاجة: Config + OCR + CAPTCHA Solver (4 طرق: API/Base64/Crop/File) | `z.ai_ocr/captcha_solver.py` |
| 2 | Strategy Pattern — 3 strategies: `ocr` (ocr.z.ai) + `tesseract` (محلي) + `2captcha` (مدفوع) | `z.ai_ocr/captcha_solver.py` |
| 3 | Session Pooling — `requests.Session()` reuse = أسرع 3x للطلبات المتتالية | `z.ai_ocr/captcha_solver.py` |
| 4 | Retry + Backoff — 3 محاولات أوتوماتيك لـ HTTP 429/500/503 مع exponential delay | `z.ai_ocr/captcha_solver.py` |
| 5 | Image Preprocessing — grayscale + contrast 1.5x + threshold (اختياري) = حجم أقل 20% + OCR أدق | `z.ai_ocr/captcha_solver.py` |
| 6 | SHA1 Hash Cache — نفس الصورة مرتين → cached بدون API call | `z.ai_ocr/captcha_solver.py` |
| 7 | `solve_batch()` — حل أكتر من CAPTCHA بالتوازي بـ ThreadPoolExecutor | `z.ai_ocr/captcha_solver.py` |
| 8 | `_TPL_CAPTCHA` template — v2 code_generator بيحقن CAPTCHA solving logic تلقائياً في السكربتات المولّدة | `v2/code_generator.py` |

### 📁 ملفات جديدة/معدّلة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `z.ai_ocr/captcha_solver.py` | سكربت رئيسي: Config + 4 methods + 3 strategies + cache + batch + retry + preprocessing | ✅ v4 |
| `z.ai_ocr/captcha_client.py` | واجهة بسيطة: CaptchaClient facade — يستورد من captcha_solver | ✅ |
| `z.ai_ocr/z_ocr.py` | CLI الرئيسي للـ OCR — يستورد من captcha_solver | ✅ |
| `z.ai_ocr/config.json` | إعدادات (اختياري — override فقط) | ✅ |
| `v2/code_generator.py` | `_TPL_CAPTCHA` template للـ AI code generator | ✅ معدّل |

### 📖 دروس مستفادة

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|--------|
| 81 | [Config] | Config defaults لازم تكون في الكود — ملف JSON اختياري للـ override بس | ملاحظة المستخدم |
| 82 | [Script] | Session pooling (`requests.Session`) بيسرّع 3x لطلبات متتالية — مش محتاج session جديد كل request | Gemini review |
| 83 | [Script] | RateLimiter لازم يكون singleton في الـ Service — مش instance جديد كل request | ChatGPT review |
| 84 | [Script] | Strategy Pattern بيخلي الكود مفتوح للتوسع — solver جديد = function واحدة + entry في STRATEGIES dict | AI review integration |
| 85 | [Script] | SHA1 hash cache بيوفر API calls لنفس الصورة — مفيد في loops (CAPTCHA retry) | Cache optimization |

---

## 🏆 إنجازات Arena Hybrid Login Integration

<!-- آخر رقم مشكلة مستخدم: #115 -->

| # | الإنجاز | الملفات |
|---|---------|--------|
| 1 | Arena Hybrid Login — دمج `arena_hybrid_login.py` في `refresh.py`: pure curl_cffi أولاً → browser fallback (SeleniumBase uc=True, headless=False) | `ارينا/refresh.py` |
| 2 | `arena_hybrid_login.py` — browser_login بـ two-step flow (Email → Continue → Password → Submit) + React `_react_type()` + JS force-click | `ارينا/arena_hybrid_login.py` |
| 3 | تحديث UNIVERSAL_PROVIDER_PROMPT — قاعدة #56 (Arena two-step login) + Arena = Hybrid في جدول المزودين + 10 providers في monitor.py | `UNIVERSAL_PROVIDER_PROMPT.md` |
| 4 | `arena_accounts.json` — حقول كاملة: cookies + localStorage + sessionStorage + access_token + user_info + login_method (pure_curl_cffi) | `ارينا/arena_accounts.json` |

### 📁 ملفات معدّلة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `ارينا/refresh.py` | Hybrid refresh: `hybrid_login()` + atomic save + login_method tracking | ✅ معدّل بالكامل |
| `ارينا/arena_hybrid_login.py` | Two-step browser login + `--browser-only` CLI flag | ✅ معدّل |
| `UNIVERSAL_PROVIDER_PROMPT.md` | قاعدة #56 + Arena Hybrid + 10 providers | ✅ معدّل |
| `monitor.py` | Arena = provider #10 (expires_default: 24) | ✅ |

### 📖 دروس مستفادة

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|--------|
| 86 | [Auth] | Arena two-step login: Main page → Login → Email → Continue → Password → Submit. React `nativeSetter` + `verify_typed()` إلزامي. JS force-click لـ buttons | Arena hybrid login |
| 87 | [Script] | Hybrid login pattern: pure requests أولاً (curl_cffi ~2s) → browser fallback (SeleniumBase ~30s). `login_method` بيتحفظ في JSON عشان تعرف مين اشتغل | Arena refresh.py |


---

## 🏆 إنجازات Arena Register v3 — CDP Runtime.evaluate WINNER

<!-- آخر رقم مشكلة مستخدم: #119 -->

| # | الإنجاز | الملفات |
|---|---------|---------|
| 1 | اكتشاف WINNER: `CDP Runtime.evaluate + userGesture=True` — الوحيد اللي بيوصل لـ fullName في Arena | `ارينا/test_click.py` |
| 2 | `test_click.py` — سكريبت اختبار مستقل: 17 طريقة ضغط بالتسلسل مع انتظار fullName 8 ثواني كل طريقة | `ارينا/test_click.py` |
| 3 | `_cdp_eval()` helper — helper مركزية تشغّل JS في main world (userGesture=True) زي Chrome console | `ارينا/arena_register.py` |
| 4 | تحديث `_mega_click()` — CDP-eval-click(WINNER) كأول استراتيجية قبل كل الناس | `ارينا/arena_register.py` |
| 5 | استبدال كل `execute_script` بـ `_cdp_eval` في 6 استراتيجيات JS | `ارينا/arena_register.py` |
| 6 | إصلاح `_try_js_mouse_event` المكسور + إضافة `_try_full_mouse_seq` جديدة | `ارينا/arena_register.py` |
| 7 | Retry loop في `enter_email` — 3 محاولات مع `[DBG]` logging | `ارينا/arena_register.py` |
| 8 | إصلاح كل `—` (em-dash) و `→` في الكود اللي كانت بتسبب `SyntaxError` | `ارينا/arena_register.py` |
| 9 | تسجيل حساب Arena حقيقي: ✅ 100% Success Rate — 22 total accounts! | `ارينا/arena_accounts.json` |
| 10 | توثيق القاعدة الذهبية في `GEMINI.md`: "قاعدة الضغط الذهبية — لأي موقع React/Next.js" | `GEMINI.md` |

### 📁 ملفات جديدة/معدّلة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `ارينا/test_click.py` | سكريبت اختبار: 17 طريقة ضغط + انتظار fullName + WINNER report | ✅ [NEW] |
| `ارينا/arena_register.py` | `_cdp_eval` + CDP strategies + إصلاح SyntaxErrors + retry loop | ✅ معدّل |
| `GEMINI.md` | قاعدة CDP Runtime.evaluate + userGesture للضغط في React/Next.js | ✅ معدّل |

### 🐛 مشاكل

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|-------|
| #116 | [Script] | `execute_script btn.click()` مش بيشتغل في React | Arena بتتجاهل الضغطة بصمت | `execute_script` بيشتغل في isolated world — React context مش موجود فيه | `CDP Runtime.evaluate + userGesture=True` بيشتغل في main world | ✅ |
| #117 | [Script] | `CDP Input.dispatchMouseEvent` مش كافي رغم إنه trusted | fullName مش بيظهر | React مش بيستمع لـ OS-level events — بيستمع بس للـ trusted JS events | CDP Runtime.evaluate هو الوحيد اللي بيطلع isTrusted في React context | ✅ |
| #118 | [Script] | `SyntaxError: invalid character '—' (U+2014)` في arena_register.py | السكريبت مش بيشتغل خالص | em-dash في docstrings + `→` في comments — Python parser بيرفضها | استبدال كل `→` بـ `->` وكل `—` بـ `-` | ✅ |
| #119 | [Script] | `_try_js_mouse_event` مفتوح بدون إغلاق — f-string غير متكاملة | `SyntaxError: unterminated triple-quoted string` | الـ edit السابق خلط استراتيجيتين في نفس الـ f-string | إعادة كتابة المنطقة كاملة من line 1290 لـ 1361 | ✅ |

### 📖 دروس مستفادة

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 88 | [Script] | `CDP Runtime.evaluate + userGesture=True` هو الوحيد اللي بيشتغل مع React/Next.js! `execute_script` بيشتغل في isolated world — React مش بيشوفه. بـ `userGesture=True`: Chrome بيعامله كـ user gesture حقيقي | Arena Register v3 |
| 89 | [Script] | `stdin` test_click.py pattern: اصنع سكريبت مستقل بـ N طريقة + watch for success element + print WINNER — أسرع طريقة تعرف ايه اللي بيشتغل | Arena click debugging |
| 90 | [Script] | `em-dash (—)` و `→` في Python strings/docstrings يسبّبوا SyntaxError على Python \< 3.12 أو لو الـ file encoding غلط — استخدم فقط ASCII characters في الكود | arena_register SyntaxError |
| 91 | [Script] | لو عدّلت f-string بطريقة partial (مش الـ block كاملة) → السطر اللي قبله ممكن يبقى مفتوح وفيه ambiguity للـ triple-quote parser. الحل: اعمل replace للـ block كاملة في view ثم edit | _try_js_mouse_event corruption |

---


---

## 🏆 إنجازات Genspark Provider — Azure AD B2C + CAPTCHA Multi-Solver

<!-- آخر رقم مشكلة مستخدم: #123 -->

| # | الإنجاز | الملفات |
|---|---------|---------|
| 1 | genspark_register.py (1291 سطر) — Azure AD B2C + PKCE + CAPTCHA Multi-Solver + OTP 6-digit + Mail.tm | `.Genspark/genspark_register.py` |
| 2 | CAPTCHA Multi-Solver: Groq Vision + Pollinations (OpenAI+Claude) + OCR بالتوازي → Consensus vote + Judges | `genspark_register.py` |
| 3 | Groq Llama-4 Scout Vision — أسرع solver (0.7s avg) | `genspark_register.py` |
| 4 | Pollinations Vision — OpenAI Azure + Claude Sonnet — مجاني 100% | `genspark_register.py` |
| 5 | Perplexity Judge x7 models بالتوازي — majority vote لـ tiebreak | `genspark_register.py` |
| 6 | genspark_master.py (660 سطر) — Register→Login→Chat في زر واحد | `.Genspark/genspark_master.py` |
| 7 | Headless Login — Azure B2C 4 خطوات: GET csrf+tx → POST email+pass → GET confirmed → GET /api/auth | `genspark_master.py` |
| 8 | Chat API — POST /api/agent/ask_proxy + SSE parser (3 formats: field_name/OpenAI delta/direct) | `genspark_master.py` |

### 📁 ملفات جديدة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `.Genspark/genspark_register.py` | تسجيل — Azure B2C + CAPTCHA Multi-Solver + PKCE + OTP | ✅ 1291L |
| `.Genspark/genspark_master.py` | Master: Register→Login→Chat في زر واحد | ✅ 660L |
| `.Genspark/genspark_auth.py` | Auth module — B2C flows | ✅ |
| `.Genspark/genspark_chat.py` | Chat client — SSE parser | ✅ |
| `.Genspark/genspark_login_headless.py` | Headless login — بدون browser | ✅ |
| `.Genspark/genspark_session_login.py` | Session login — من cookies | ✅ |
| `.Genspark/genspark_send.py` | Send message module | ✅ |
| `.Genspark/genspark_full_headless.py` | Full headless version | ✅ |
| `.Genspark/accounts_genspark.json` | قاعدة بيانات الحسابات | ✅ |

### 🐛 مشاكل

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|-------|
| #120 | [API] | Azure B2C CAPTCHA = Base64 JPEG مش رابط URL | solve_from_url مش شغال | B2C بيرجع صورة كـ base64 في HTML مش URL | تحويل base64 → data:image/jpeg;base64 URL للـ vision APIs | ✅ |
| #121 | [Script] | Genspark SSE format = field_name/field_value مش OpenAI standard | parser بيرجع نص فاضي | Genspark format مختلف | parser بيتعرف على الـ 3 formats | ✅ |
| #122 | [API] | B2C_1A_SIGNUP_SIGNIN مش متاح مباشرة | التسجيل بيفشل | registration policy مختلف عن login policy | fallback: login كـ existing user | ✅ |
| #123 | [Performance] | Groq Vision rate limit لو token واحد | captcha solver بيرجع empty | rate limit | random.sample من 3 tokens بـ fallback | ✅ |

### 📖 دروس مستفادة

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 92 | [API] | Azure AD B2C: csrf و transId موجودين في HTML كـ JSON inline. استخرجهم بـ regex مش meta tags | Genspark B2C |
| 93 | [API] | Azure B2C PKCE: code_verifier (32 bytes urlsafe) → SHA256 → base64url = code_challenge | Genspark PKCE |
| 94 | [Script] | CAPTCHA Multi-Solver: ThreadPoolExecutor + consensus vote. لو اختلفوا → Judges. Vision APIs بتاكل data:image/jpeg;base64 URLs | Genspark CAPTCHA |
| 95 | [API] | Genspark Chat SSE = 3 formats: field_name/field_value + OpenAI delta + direct content. parser لازم يتعامل مع الـ 3 | Genspark Chat |

---


## 🏆 إنجازات arena_hybrid_login — دمج CDP Pattern

<!-- آخر رقم مشكلة مستخدم: #128 -->

| # | الإنجاز | الملفات |
|---|---------|---------|
| 1 | دمج _cdp_eval في arena_hybrid_login.py | `ارينا/arena_hybrid_login.py` |
| 2 | إضافة _cdp_click_by_text بـ % formatting (مش f-string!) | `ارينا/arena_hybrid_login.py` |
| 3 | تحديث _click_smart يستخدم CDP بدل execute_script | `ارينا/arena_hybrid_login.py` |
| 4 | Login Submit الآن = CDP Strategy 1 (WINNER للـ React) | `ارينا/arena_hybrid_login.py` |
| 5 | استبدال uc_open_with_reconnect بـ uc_open + sleep 8s | `ارينا/arena_hybrid_login.py` |
| 6 | Login button: CDP text search بدل CSS selector هش | `ارينا/arena_hybrid_login.py` |
| 7 | Accept Cookies: dismiss مرتين + sleep بينهم | `ارينا/arena_hybrid_login.py` |
| 8 | debug_login_btn.py — debug script لمعرفة الـ buttons الموجودة | `ارينا/debug_login_btn.py` |
| 9 | Browser Login نجح 100%: 11 cookies + localStorage + session | `ارينا/arena_hybrid_login.py` |

### 🐛 مشاكل

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|-------|
| #124 | [Script] | execute_script مش بيشتغل مع React في arena_hybrid_login | الضغط بيتنفذ بس Arena مش بتستجبش | execute_script بيشتغل في isolated world | CDP Runtime.evaluate + userGesture=True | ✅ |
| #125 | [Script] | uc_open_with_reconnect بيسبب browser exit | المتصفح بيخرج كل شوية | reconnect بيفتح tab جديد | uc_open عادي + sleep(8) | ✅ |
| #126 | [Script] | Login button CSS selector قديم (bg-header-primary) | is_element_visible فشل | Arena غيّرت الـ design | CDP text search بالنص مش بالـ class | ✅ |
| #127 | [Script] | _cdp_click_by_text مش بتلاقي الـ button رغم وجوده | لا clicked ولا error | مزج f-string مع plain string ينتج }} في JS (Syntax Error صامت) | % formatting نظيف بدون f-string | ✅ |
| #128 | [Script] | Accept Cookies popup بيحجب Login button | Login button مش بيتضغط | Cookies popup موجود وقت الـ click | dismiss مرتين + sleep(1) بينهم | ✅ |

### 📖 دروس مستفادة

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 96 | [Script] | مزج f-string مع plain string في JS يعمل syntax error صامت. الـ CDP بيرجع null بدون exception. الحل: % formatting أو string واحدة | arena_hybrid_login CDP bug |
| 97 | [Script] | uc_open_with_reconnect بيسبب browser exit في بعض السيناريوهات. الأأمن: uc_open + sleep(8) | arena_hybrid_login |
| 98 | [Script] | CSS selectors هشة (بتتكسر لو الموقع غيّر الـ design). CDP text search بالنص أقوى وأبقى | arena_hybrid_login Login button |
| 99 | [Debug] | لو CDP مش بيلاقي element → أضف debug يطبع الـ elements الموجودة بـ getBoundingClientRect. لو موجود في debug ومش في click → المشكلة في الـ JS click code نفسه | arena_hybrid_login |
| 100 | [Script] | Accept Cookies popup بيحجب buttons تانية. الحل: dismiss مرتين + sleep(1) بينهم عشان تتأكد إنه اتعمل | arena_hybrid_login |
| 101 | [Script] | اختبر الـ JS code في Chrome console قبل ما تستخدمه في CDP عشان تتأكد من syntax صح مش صامت | CDP debugging |

---


## ?? ??????? refresh.py � ????? ?? arena_hybrid_login

<!-- ??? ??? ????? ??????: #131 -->

| # | ??????? | ??????? |
|---|---------|---------|
| 1 | ??? DRY violation � ??? arena_hybrid_login ??? ????? ???? ?? refresh.py (1346?312 ???) | `?????/refresh.py` |
| 2 | ????? uc_open_with_reconnect ? uc_open + sleep(8) (bug #125 ???????) | `?????/refresh.py` |
| 3 | ????? _fallback_hybrid() � ?? session ?????? ?? ???? ????? ? ????? hybrid_login ????????? | `?????/refresh.py` |
| 4 | ????? _USER_PROFILE selector ?? arena_hybrid_login.py | `?????/refresh.py` |
| 5 | ????? UTF-8 fix ?? ????? refresh.py (PowerShell cp1252 + emoji) | `?????/refresh.py` |
| 6 | ???????? ?????: Syntax OK + monitor dry-run (22 ????) + Pure Login + Cookie Injection + Browser Login | ?? ????? Arena |

### ?? ?????

| # | [TAG] | ??? ??????? | ??????? | ????? | ???? | ?????? |
|---|-------|---------|---------|-------|------|-------|
| #129 | [Script] | DRY violation ?? refresh.py � ??? arena_hybrid_login.py ?????? ????? ??? if __name__ (???? 289-1326) | ????? 1346 ??? ??? 311 | ??? ???? ???? | ??? ????? ?????? ?? Python script (cutoff at parser.print_help) | ? |
| #130 | [Script] | UnicodeEncodeError ?? refresh.py ??? ??????? ?? PowerShell | ???? cp1252 error ??? print emoji ??? ?? | PowerShell default encoding cp1252 ?? ???? emoji | ????? sys.stdout.reconfigure(encoding='utf-8') ?? ????? ????? | ? |
| #131 | [Script] | mycdp KeyError (sameParty/privateNetworkRequestPolicy) ?? ?? ????? SeleniumBase | Traceback ???? ?? ??? output ???? ????? | mycdp ????? ?????? ????? ?? ??????? ?? Chrome 146 ?????? | ??? ????? ??? ??? login � ???????? ??? ???? ??????? | ?? ?????? |

### ?? ???? ???????

| #??? | [TAG] | ????? | ?????? |
|------|-------|-------|-------|
| 102 | [Script] | ??? ???? ??? ???? ?? ??? ???? ? ???? ?????? ?????? ??? ???? ???????. DRY violation ???? ??? ???? ?????? | refresh.py DRY |
| 103 | [Script] | sys.stdout.reconfigure(encoding='utf-8', errors='replace') ???? ????? ?? ????? ?? ?????? ????? emoji ?? PowerShell | UTF-8 fix |
| 104 | [Script] | fallback pattern ??? session renewal: ???? cookie injection ????? ? ?? ??? ???? hybrid_login ?????????. ?? ???? False ?????? | refresh fallback |
| 105 | [Debug] | mycdp KeyError errors ?? SeleniumBase (Chrome 146) ??? ????? ??? ??? login = ???? noise. ???? ?????? ?? '?? ?????' ?? exit code ?? ??? output | mycdp errors |


































































---

## 🏆 إنجازات Uncensored Chat v2.0 — Pure Requests & WebSocket

<!-- آخر رقم مشكلة مستخدم: #134 -->

| # | الإنجاز | الملفات |
|---|---------|--------|
| 1 | `uncensored_chat.py` (v2.0) — سكريبت واحد يدمج كل الخصائص (Auth, Chat, WebSocket, CLI) | `Uuncensored/uncensored_chat.py` |
| 2 | تخطي حماية Clerk (4 خطوات) بـ `curl_cffi` لانتحال بصمة متصفح `chrome120` | `Uuncensored/uncensored_chat.py` |
| 3 | بناء `AccountManager` لإدارة قاعدة حسابات بتنسيق JSON (حفظ/تجديد/تبديل/Account Rotation) | `Uuncensored/uncensored_chat.py` |
| 4 | دعم كامل لـ WebSocket Parsing (معالجة تدفق الرسائل كـ Chunks حية) | `Uuncensored/uncensored_chat.py` |
| 5 | إصلاح كشف الـ Stream End عن طريق رصد `end_of_stream: true` مع `raw_text` الكامل | `Uuncensored/uncensored_chat.py` |
| 6 | إضافة `Config` Dataclass للسيطرة على 7 خصائص (الموديل، نمط الشات، المهلة، حسابات، الخ) | `Uuncensored/uncensored_chat.py` |
| 7 | إضافة 12 أمراً تفاعلياً (`help`, `list`, `model`, `chat`, `code`, `web`, `switch`, الخ) داخل كونسول الدردشة | `Uuncensored/uncensored_chat.py` |
| 8 | دعم الذاكرة السياقية (History Limit) للحفاظ على مسار المحادثة (Multi-turn) | `Uuncensored/uncensored_chat.py` |
| 9 | توسيع الـ CLI Args (`--code`, `--web-search`, `--account`, `--list`, `--count`) | `Uuncensored/uncensored_chat.py` |

### 📁 ملفات جديدة/معدّلة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `Uuncensored/uncensored_chat.py` | السكريبت الشامل (Auth + WebSocket Client + Account Rotation + CLI) | ✅ v2.0 |
| `Uuncensored/uncensored_accounts.json` | قاعدة بيانات الحسابات والجلسات (Token/Session) المعمول لها Upsert آلي | ✅ جديد |

### 🐛 مشاكل

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|-------|
| #132 | [Auth] | فشل التسجيل واستخراج JWT من Clerk Auth | 401 Unauthorized + Cookie Missing | Clerk يستخدم Cloudflare Fingerprinting معقد بـ 4 خطوات (Session ID → JWT) | استخدام `curl_cffi` بـ `impersonate="chrome120"` لتنفيذ الخطوات تتابعيًا وتخطي الحماية | ✅ |
| #133 | [API] | السكريبت يعلق للأبد عند استلام رسائل WebSocket | Infinite Loop في `recv()` | انتظار إشارة `message_type: done` اللي مش بتتبعت من السيرفر أساساً | الاعتماد على Chunk اللي يحتوي `end_of_stream: true` + `raw_text` للخروج من الـ Loop | ✅ |
| #134 | [CLI] | صعوبة التبديل بين الحسابات وأوضاع الشات وتذكر السياق بطريقة سلسة | أوامر متشابكة، عدم استجابة الحسابات | الافتقار لهيكل تنظيمي مرن لـ State | إدخال `Config Dataclass` لـ State و 12 أمراً لـ Interactive Mode و `--code` Flag | ✅ |

### 📖 دروس مستفادة

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 106 | [Auth] | أنظمة زي Clerk Auth بتطلب تتابع دقيق بين GET للـ Token، و POST لـ Session، واستخراج JWT. `curl_cffi` هو الحل الأقوى لعمل Impersonate للمتصفح. | Clerk Token Exchange Flow |
| 107 | [API] | في تحليل WebSockets، إياك تفترض شكل الإغلاق (Disconnect/Done Signal). استخدم `--discover` mode أو سجل Burp حقيقي لاكتشاف إشارة النهاية الحقيقية (مثل `end_of_stream`). | WebSocket End Detection |
| 108 | [Architecture] | في أدوات النقل السريع، دمج الكلاسات (Config, AccountManager, ChatApp) في ملف واحد باستخدام `Dataclasses` يجعلها Portable و Clean. | Uncensored Tool v2.0 Structure |

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# 🧠 AI OS — بي ريييب

نظام ذكاء اصطناعي متكامل يشغّل AI providers بالتوازي.

---

## 🔰 الحالة العامة: v7.0 — مكتمل ✅

---

## 📋 سجل الإنجازات

| # | الإنجاز | الحالة |
|---|---|---|
| 1 | ai_engine.py — 11 providers | ✅ |
| 2 | ai_team.py v1 — 8 commands أساسية | ✅ |
| 3 | ai_team.py v2 — cache + smart routing | ✅ |
| 4 | tools/ — 5 tools (file, http, code, browser, har) | ✅ |
| 5 | ai_agents.py — Meta-Agent (Planner + Steps) | ✅ |
| 6 | ai_team.py v3 — F1+F2+F3 fixes | ✅ |
| 7 | Worker Scoring (accuracy×0.5+speed×0.3+stability×0.2) | ✅ |
| 8 | Multi-Agent Debate (Workers→Critique→Judge) | ✅ |
| 9 | Learning System (learning.jsonl) | ✅ |
| 10 | Rate Limit Guard (0.3s minimum) | ✅ |
| 11 | Task Tree + Anti-Loop (Jaccard 0.70) في ai_agents.py | ✅ |
| 12 | monitor.py — Quarantine + Auto-Revive (15min) | ✅ |
| 13 | agents/ — Agent Registry (4 agents + Auto-Discovery) | ✅ |
| 14 | logs/ — system.log + errors.log | ✅ |
| 15 | stats.py — Stats Dashboard | ✅ |
| 16 | dashboard.py — Web UI Flask (4 pages + 5s cache) | ✅ |
| 17 | scheduler.py — 3 jobs (Daemon + --stop) | ✅ |
| 18 | templates.py — 8 Prompt Templates (.format()) | ✅ |

---

## 📁 الملفات الجديدة
- infra/proxy_manager.py: إدارة البروكسيات بنظام Cooldown.
- infra/persistence.py: كتابة ملفات آمنة (Atomic Writes).
- clarifai_parallel_v3.py: مشغل Clarifai المتوازي الأساسي.

| الملف | الوظيفة |
|---|---|
| `ai_engine.py` | 11 providers engine |
| `ai_team.py` | 15 commands + Debate + Scoring |
| `ai_agents.py` | Meta-Agent + Task Tree |
| `monitor.py` | صحة providers + Quarantine |
| `stats.py` | stats dashboard |
| `dashboard.py` | Web UI (Flask) |
| `scheduler.py` | Background scheduled jobs |
| `templates.py` | 8 Prompt Templates |
| `agents/` | Agent Registry (debug, code, analyze, har) |
| `tools/` | 5 execution tools |
| `v2/` | memory + healer + planner |
| `cache/` | JSON cache + learning.jsonl |
| `logs/` | system.log + errors.log |

---

## 🚀 Quick Start

```bash
# سؤال بسيط
python ai_team.py ask "اشرح OAuth2"

# سؤال مع debate
python ai_team.py ask "أفضل DB؟" --debate

# مهمة كبيرة (Task Tree)
python ai_agents.py --tree "build login automation"

# Dashboard
python dashboard.py  # http://localhost:5000

# Monitor
python monitor.py --watch

# Stats
python stats.py

# Scheduler
python scheduler.py
```

---

## 🔑 سجل المشاكل

| # | [TAG] | المشكلة | السبب | الحل | الحالة |
|---|---|---|---|---|---|
| 1 | [Cache] | Cache miss لمسافات | لم تُعمل normalize | strip+lower قبل MD5 | ✅ |
| 2 | [API] | Infinite loop في heal | لا MAX_RETRIES | MAX_RETRIES=3 | ✅ |
| 3 | [Backend] | Circular import | tools تكلم ai_team | ai_agents هو الوسيط | ✅ |
| 4 | [API] | Task explosion | لا MAX_DEPTH | MAX_DEPTH=3+Anti-Loop | ✅ |
| 5 | [API] | Provider لا يرجع | Disable دائم | Quarantine+Auto-Revive | ✅ |

---

## 📚 دروس مستفادة

| # | [TAG] | الدرس | السياق |
|---|---|---|---|
| 1 | [Cache] | normalize الـ input قبل hashing | cache normalization |
| 2 | [Backend] | ai_agents يكون الوسيط الوحيد | circular imports |
| 3 | [API] | Quarantine أفضل من Disable الدائم | monitor design |
| 4 | [Backend] | Jaccard similarity لمنع Task loops | Task Tree Anti-Loop |
| 5 | [Performance] | Cache data كل 5s لا عند كل request | dashboard I/O |

---

<!-- آخر رقم مشكلة مستخدم: 5 -->





# 🤖 Genspark CLI System

**الإصدار:** 4.0.0

---

## 📁 السكربتات

| السكربت | الغرض |
|---------|--------|
| `genspark_send.py` | يبعت رسالة + multi-turn context |
| `genspark_join.py` | يدخل محادثة عامة من حساب تاني |
| `genspark_auth.py` | يسجل حساب جديد + دخول |
| `genspark_picker.py` | بيختار أحسن حساب متاح |

---

## 💻 الأوامر

```bash
# ابدأ/تابع محادثة
python genspark_send.py --conv TEST --q "سؤالك"

# ابعت + اعمل رابط عام
python genspark_send.py --conv TEST --share --q "سؤالك"

# اعرض كل المحادثات
python genspark_send.py --list-convs

# دخل محادثة عامة من حساب تاني + رابط جديد
python genspark_join.py --url "https://genspark.ai/agents?id=XXX" --q "سؤالك" --share

# سجل حساب جديد
python genspark_auth.py

# دخول فقط
python genspark_auth.py --login --email x@y.com
```

---

## 📂 الملفات

| الملف | فيه إيه |
|-------|---------|
| `accounts_genspark.json` | الحسابات + cookies + balance |
| `conversations.json` | تاريخ المحادثات + project_id |

---

## 🔄 الفلو

```
genspark_send → Smart Picker → ask_proxy SSE → حفظ في conversations.json
genspark_join → viewer page SSR → inject history → ask_proxy جديد → share
```

---

## 🏆 سجل الإنجازات
- **Clarifai Parallel Pipeline**: تم بناء الإصدار الثالث (clarifai_parallel_v3.py) لتشغيل الإرسال بالتوازي (Multiprocessing) مع عزل كامل للبصمات (TLS/IP) عبر ProxyLeaseManager لحل مشاكل الـ Risk Engine.

| # | الإنجاز |
|---|---------|
| 1 | multi-turn context بـ conversations.json |
| 2 | SSE parsing (streaming + non-streaming + message_result) |
| 3 | CREDIT_EXHAUSTED detection + auto-retry |
| 4 | real-time balance update بعد كل رسالة |
| 5 | `--share` flag → project عام + رابط |
| 6 | `genspark_join.py` → دخول محادثة عامة من حساب تاني |
| 7 | SSR history injection (بدون login) |
| 8 | account locking لضمان context integrity |
| 9 | retry 3x في mail.tm |
| 10 | 8-step B2C Signup flow كامل (PKCE + CAPTCHA + OTP + SelfAsserted) |
| 11 | Groq Vision (Maverick + Scout) لحل الـ CAPTCHA تلقائياً |
| 12 | Session auto-refresh لما تنتهي بعد 5 CAPTCHA محاولات |
| 13 | emailnator integration كامل مع cookies + seen_ids لتجنب OTP قديم |
| 14 | OTP وصل بنجاح وتم إنشاء حساب جديد `i.mjam.es.liq.u.in@googlemail.com` |

---

## 🆕 الملفات الجديدة

| الملف | الغرض |
|-------|-------|
| `genspark_send.py` | Core sender |
| `genspark_join.py` | Public conv joiner |
| `genspark_auth.py` | Account registration |
| `genspark_picker.py` | Smart account picker |
| `accounts_genspark.json` | Account store |
| `conversations.json` | Conv history store |

---

## 🐛 سجل المشاكل

| # | [TAG] | المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|--------|
| 1 | [API] | حساب تاني + نفس project_id → رفض | HTTP 500 | ask_proxy مقيد بصاحب الـ project | genspark_join.py بيعمل project جديد بنفس الـ history | ✅ محلول |
| 2 | [API] | mail.tm response فاضي | `Expecting value: line 1 column 1` | mail.tm API rate limit أو downtime | retry 3x مع wait 3s + safe JSON parse | ✅ محلول |
| 3 | [API] | Project جديد private بالـ default | "You need permission" عند فتح الرابط | ask_proxy بيعمل is_private=True | أضفنا --share في genspark_join.py | ✅ محلول |
| 4 | [Chrome Extension] | مفيش viewer لو مش logged in | صفحة login بدل المحادثة | viewer يحتاج session | genspark_join يجيب SSR data بدون login | ✅ محلول |
| 5 | [Auth] | B2C_1A_SIGNUP_SIGNIN مش موجود | AADB2C90052 error | Genspark بيستخدم B2C_1_new_login مش B2C_1A | كتبنا 8-step flow صح مع PKCE + DisplayControlAction | ✅ محلول |
| 6 | [Auth] | CAPTCHA بيفشل دايماً | Pollinations 403 | Cloudflare بيحجب Pollinations من مصر | استخدمنا Groq Vision (Maverick + Scout) | ✅ محلول |
| 7 | [Auth] | Session تنتهي بعد 5 محاولات CAPTCHA | GetChallenge 400 | B2C session TTL قصير | OAuth auto-refresh ينشئ tx+csrf جديد | ✅ محلول |
| 8 | [Auth] | OTP مش بييجي على temp-mail.org | timeout 120s | Microsoft ترفض domains زي pazard/onbap/qvmao | حولنا لـ emailnator بـ googlemail.com | ✅ محلول |
| 9 | [Auth] | OTP قديم (718096) بيرجع دايماً | VerifyCode 400 cached | emailnator نفس inbox session بترجع messages قديمة | seen_ids snapshot قبل SendCode يفلتر القديم | ✅ محلول |
| 10 | [Auth] | VerifyCode يفشل رغم OTP صح | status 400 | tx اتغير بسبب session refresh والـ OTP بـ tx قديم | seen_ids fix تسرع إيجاد OTP الجديد قبل expire | ✅ محلول |

---

## 📚 دروس مستفادة

| # | [TAG] | الدرس | السياق |
|---|-------|-------|--------|
| 1 | [API] | ask_proxy مش بيسمح لحساب تاني يكمل project موجود | HTTP 500 عند محاولة cross-account |
| 2 | [API] | الـ NUXT_DATA في viewer page فيها كل الـ messages كـ indexed array | ممكن نجيب history بدون auth |
| 3 | [API] | mail.tm بيرجع empty response أحيانًا | محتاج retry + safe JSON parsing |
| 4 | [API] | project_id بيتعمل مع أول رسالة بس | مش موجود لو بدأت محادثة جديدة |
| 5 | [Auth] | Genspark B2C policy اسمه B2C_1_new_login مش B2C_1A | لازم تفحص الـ url في network لما تلاقي policy غلط |
| 6 | [Auth] | Pollinations AI محجوب من مصر | استخدم Groq Vision بدلها مع rotation على keys |
| 7 | [Auth] | emailnator بيرجع نفس الـ messages القديمة | خد snapshot من messageIDs قبل بعت OTP وافلتر المتجاهلين |
| 8 | [Auth] | Microsoft بتبعت OTP على googlemail بس مش على domains زي pazard | emailnator أفضل من temp-mail.org لـ Genspark |
| 9 | [Auth] | B2C CAPTCHA بيعمل rate limit بعد 5 محاولات غلط | لازم OAuth refresh كامل (session + tx + csrf) مش بس sleep |

---

## الحالة العامة

🟢 **شغال** — Registration كاملة + Login + Multi-turn + Share + Join

<!-- آخر رقم مشكلة مستخدم: 16 -->

---

## 🏆 سجل الإنجازات
- **Clarifai Parallel Pipeline**: تم بناء الإصدار الثالث (clarifai_parallel_v3.py) لتشغيل الإرسال بالتوازي (Multiprocessing) مع عزل كامل للبصمات (TLS/IP) عبر ProxyLeaseManager لحل مشاكل الـ Risk Engine. — Uncensored.ai Registration

| # | الإنجاز |
|---|--------|
| 1 | `uncensored_register.py v2` — Full Browser Registration (SeleniumBase + Emailnator) |
| 2 | Flow كامل: Create Account → Terms → Turnstile → OTP → JWT في **48 ثانية** |
| 3 | OTP استخراج من subject مباشرة (بدون HTML parsing) |
| 4 | `accounts_uncensored.json` — حفظ الحسابات |
| 5 | دليل شامل: walkthrough.md + implementation_plan.md للمنهجية العامة |

---

## 🆕 الملفات الجديدة — Uncensored

| الملف | الوظيفة |
|-------|---------|
| `Uuncensored/uncensored_register.py` | 🆕 Registration Script v2 (Full Browser) |
| `Uuncensored/accounts_uncensored.json` | 🆕 قاعدة بيانات الحسابات |
| `Uuncensored/debug_turnstile.py` | 🗑️ Debug script مؤقت (للحذف) |

---

## 🐛 سجل المشاكل — Uncensored.ai

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|------------|---------|-------|------|--------|
| 11 | [Auth] | captcha_missing_token عند sign_up | HTTP 400 من Clerk | Turnstile token غير مُرسَل | Full Browser (uc=True) بدل HTTP request | ✅ محلول |
| 12 | [Script] | React form مش بيتحدث مع JS value setter | Create Account button مش يشتغل | React state مش يتحدث من DOM mutation | ActionChains.send_keys() بـ keyboard events حقيقية | ✅ محلول |
| 13 | [Auth] | Terms of Service checkbox ما اتضغطش | HTTP request مش بيتبعت | Validation مخفية بـ checkbox | `button[class*='shrink-0']` + ActionChains click | ✅ محلول |
| 14 | [Auth] | XHR intercept فاشل (6 محاولات) | JS monkey-patch مش شغّال | Clerk SDK بيشتغل في service worker context | تركنا Turnstile يحل وحده في browser | ✅ محلول |
| 15 | [Script] | Emailnator session مش مُهيَّأة في register_browser | AttributeError أو empty XSRF | Emailnator object جديد بدون _init() | تمرير en المُهيَّأ من register_one | ✅ محلول |
| 16 | [Script] | UnicodeEncodeError في Banner على Windows | cp1252 مش بيدعم Arabic+Emoji | Terminal encoding | sys.stdout = io.TextIOWrapper(encoding='utf-8') | ✅ محلول |

---

## 📚 دروس مستفادة — Uncensored.ai

| # | [TAG] | الدرس | السياق |
|---|-------|-------|--------|
| 10 | [Script] | React form يحتاج ActionChains.send_keys() وليس JS value setter | React بيستمع لـ keyboard events مش DOM mutations |
| 11 | [Auth] | Turnstile بيتحل تلقائياً في uc=True — مفيش حاجة تعملها | محاولة استخراج token manually دايماً بتفشل |
| 12 | [Script] | دايماً افحص كل الـ buttons (حتى الصغيرة جداً) قبل Submit | Terms checkbox كانت السبب الجذري للفشل |
| 13 | [Script] | OTP في الـ subject مباشرة — أسرع من HTML parsing | `re.search(r'\b(\d{6})\b', subject)` |
| 14 | [Script] | XHR/fetch monkey-patch فاشل مع Clerk SDK (Service Worker) | الحل: Full Browser Registration بالكامل |
| 15 | [Backend] | "Full Browser First" — لو في CAPTCHA أو React Form معقد | SeleniumBase يعمل كل حاجة جوه البراوزر |

---

## 🏆 سجل الإنجازات
- **Clarifai Parallel Pipeline**: تم بناء الإصدار الثالث (clarifai_parallel_v3.py) لتشغيل الإرسال بالتوازي (Multiprocessing) مع عزل كامل للبصمات (TLS/IP) عبر ProxyLeaseManager لحل مشاكل الـ Risk Engine. — .agents System Sync

| # | الإنجاز |
|---|--------|
| 1 | `Sync P__poe & C__cursor` — مزامنة نظام الـ Multi-Agent (أكثر من 28 ملف SKILL و RULES) لدعم الذكاء الاصطناعي بين المشروعين بالكامل. |

---

## 🆕 الملفات الجديدة — .agents

| الملف | الوظيفة |
|-------|---------|
| `P__poe/.agents/skills/*` | 🆕 28+ Skills جديدة تم إضافتها لـ P__poe (System Architect, Planners, Checkers) |
| `P__poe/.agents/rules/01-user-context.md` | 🆕 سياق المستخدم الجديد |
| `C__cursor/.agents/skills/skills/23-debug-cursor.md` | 🆕 ملف تشخيص مشاكل Cursor |

---

## 🏆 سجل الإنجازات
- **Clarifai Parallel Pipeline**: تم بناء الإصدار الثالث (clarifai_parallel_v3.py) لتشغيل الإرسال بالتوازي (Multiprocessing) مع عزل كامل للبصمات (TLS/IP) عبر ProxyLeaseManager لحل مشاكل الـ Risk Engine. — Poe.com Registration

| # | الإنجاز |
|---|--------|
| 1 | `poe_register.py` — تسجيل دخول بأرقام الهواتف باستخدام `curl_cffi` (بدون متصفح) |
| 2 | تخطي Cloudflare وطلب الـ OTP بريكويست مباشر متدعم بواجهة المستخدم في الـ CLI |
| 3 | توثيق الـ Mobile bypass كبديل للـ `poe-formkey` WebAssembly |

---

## 🆕 الملفات الجديدة — Poe.com

| الملف | الوظيفة |
|-------|---------|
| `poe_register.py` | 🆕 سكريبت التسجيل برقم التليفون (CLI) |
| `accounts_poe.json` | 🆕 مستودع حفظ الحسابات |

---

## 🐛 سجل المشاكل — Poe.com

| # | [TAG] | المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|--------|
| 1 | [API] | `poe-formkey` مطلوب لنموذج الويب | 403 Forbidden | حماية GraphQL | محاولة التخطي باستخدام Mobile App Headers (400 Bad Request) أو استخدام PyMiniRacer للمستقبل | ⏳ |

---

## 📚 دروس مستفادة — Poe.com

| # | [TAG] | الدرس | السياق |
|---|-------|-------|--------|
| 1 | [API] | في تسجيلات Pure HTTP، لو توكن الويب متولد بـ WASM معقد، واجهة تطبيق الجوال (Mobile API) بتكون بديل جيد للتحايل على قيود المتصفح. | `poe-formkey` bypass |

---

## 🛡️ سجل إنجازات — WAF & Bot Diagnostic Framework

| # | الإنجاز |
|---|--------|
| 1 | بناء `WAF_BOT_DIAGNOSTIC_MASTER_PROMPT.md` — 7,700+ سطر SSOT كامل من تحليل 17,967 سطر خام |
| 2 | توثيق **169 Section** معمارية لتشخيص WAF/Bot بدون تكرار |
| 3 | فخ gRPC: HTTP 200 + grpc-status != 0 في الـ Trailers — WAF لا تكتشفه |
| 4 | **6 False Positive Patterns** (FP-01→FP-06) محددة ومنها: اسم O'Brien يُكشف كـ SQL Injection! |
| 5 | OTel Rule: الـ DENY المتعمد = `StatusCode.OK` لمنع false alert storms |
| 6 | دمج المرجع في كل ملفات الحوكمة: AGENTS.md، AGENT.md، GEMINI.md، 00-RULES.md، UNIVERSAL_PROVIDER_PROMPT |

---

## 🆕 الملفات الجديدة — WAF Diagnostic Framework

| الملف | الوظيفة |
|-------|---------|
| `O__oysho/test/WAF_BOT_DIAGNOSTIC_MASTER_PROMPT.md` | 🆕 المرجع الهندسي الكامل (7,700+ سطر) |
| `.agents/memory/WAF_BOT_DIAGNOSTIC_MASTER_PROMPT.md` | 🆕 نسخة الذاكرة للـ Agents (SSOT) |

---

## 📚 دروس مستفادة — WAF Diagnostic Framework

| # | [TAG] | الدرس | السياق |
|---|-------|-------|--------|
| 1 | [Security] | TTFB < 5ms مع 403 = Edge/CDN — مش Token مشكلة ← بيوفر ساعات debugging | Layer Attribution |
| 2 | [API] | gRPC بيرجع HTTP 200 مع error في الـ Trailers — CDN/WAF مش بتشوفه | gRPC Trap |
| 3 | [Security] | Health Check requests بتأكل من الـ Rate Limit Quota — استثنيها دايماً | FP-03 |
| 4 | [Security] | Async Worker Token Expiry = Silent DLQ Entry، مفيش 403 في اللوج | Layer 5 |
| 5 | [Security] | OTel StatusCode.DENY المتعمد = OK مش ERROR — يمنع false alert storms | OTel Rule |

---

## 🛡️ سجل إنجازات — Oysho Automation Pipeline

| # | الإنجاز |
|---|--------|
| 1 | تطوير `oysho_production_v2.py` — نظام الكوكيز v2.4 بقص فعلي (Actual Cut) |
| 2 | تطبيق Actual Cut عبر `threading.Lock` للحفظ الذري (Atomic Save) من الذاكرة لملف `cookie_store.json` ومنع استهلاك الكوكيز مرتين |
| 3 | توليد شخصيات واقعية (Human-like) عبر `Faker` لإنشاء إيميلات وباسووردات بدون عشوائية رديئة لمنع اكتشاف الحماية |
| 4 | تحسين جودة Planner Agent Output عن طريق وضع فواصل فارغة لتسهيل القراءة (Professional Layout) |

---

## 🆕 الملفات المحدثة — Oysho Automation

| الملف | الوظيفة |
|-------|---------|
| `O__oysho/oysho_production_v2.py` | سكربت الإنتاج المحدث لإرسال رسائل Oysho بشكل لائق ومستقر للعمل 24/7 |
| `O__oysho/cookie_store.json` | مستودع حفظ الجلسات وحذفها الفوري |

---

## 🐛 سجل المشاكل — Oysho Automation

| # | [TAG] | المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|--------|
| 117 | [Logic] | استهلاك نفس الـ Cookies مرتين | 403 / فشل في إرسال الـ SMS بعد عمل ريستارت | السكربت يقرأ الجلسة للذاكرة ولا يحذفها من الملف الأصلي (JSON) | تم تطبيق (Actual Cut) في `remove_slot()` لحذف الجلسة عبر `Lock` فورًا بعد القراءة | ✅ محلول |

---

## 📚 دروس مستفادة — Oysho Automation

| # | [TAG] | الدرس | السياق |
|---|-------|-------|--------|
| 1 | [Logic] | الاعتماد على التخزين المؤقت (RAM) فقط في الـ Loops اللانهائية يُسبب تسريب أو إعادة استخدام البيانات. يجب تحديث الملف الأصلي (Persistent Store) بشكل فوري. | منع الـ Duplicate Cookies |
| 2 | [Anti-Bot] | الاعتماد على توليد إيميلات نصية عشوائية `test123_abc` يُحفز أنظمة الـ Fraud Detection. أفضل استراتيجية هي مكتبة `Faker` بدومينات موثوقة (`hotmail, outlook, gmail`). | توليد شخصيات واقعية |

---

## 🏆 سجل الإنجازات
- **Clarifai Parallel Pipeline**: تم بناء الإصدار الثالث (clarifai_parallel_v3.py) لتشغيل الإرسال بالتوازي (Multiprocessing) مع عزل كامل للبصمات (TLS/IP) عبر ProxyLeaseManager لحل مشاكل الـ Risk Engine. — CLI Vibe UX Standardization

| # | الإنجاز |
|---|--------|
| 1 | فصل واجهة المستخدم (CLI Vibe UX) في ملف مستقل `cli_ux.py` وتطبيق التصميم الاحترافي على سكربت `send_mw4me_sms.py` |
| 2 | تحديث الـ Master Prompt `Z__..Numbers_Send.md` لاعتماد الـ Pattern كمعيار لأي سكريبت مستقبلي |

---

## 🆕 الملفات المحدثة — CLI Vibe UX

| الملف | الوظيفة |
|-------|---------|
| `M__moneyworks4me/cli_ux.py` | ملف الدعم الجديد لاحتواء دوال الواجهة والطباعة (Banner, Stats, Colors) بشكل نقي |
| `M__moneyworks4me/send_mw4me_sms.py` | السكريبت المُحذَّث بالأسلوب المعياري والـ `KeyboardInterrupt` Catcher |
| `Z__..Numbers_Send.md` | تحديث قواعد الأتمتة لاعتماد الـ Vibe UX في أي AI Agent قادم |

---

## 🐛 سجل المشاكل — CLI Vibe UX

| # | [TAG] | المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|--------|
| 118 | [UI] | تكرار أكواد الطباعة والألوان (DRY Violation) | ملفات طويلة وكود غير مقروء في كل مشاريع الأتمتة | دمج منطق الواجهة مع Business Logic | إنشاء `cli_ux.py` واستخراج كل دوال الـ UI كـ Helpers | ✅ محلول |

---

## 📚 دروس مستفادة — CLI Vibe UX

| # | [TAG] | الدرس | السياق |
|---|-------|-------|--------|
| 1 | [Architecture] | فصل الواجهة (UI/UX) عن الـ Business Logic في الـ CLI يسهل قراءة الكود ويوفر Templates جاهزة للذكاء الاصطناعي (Golden Code Reference) | توحيد قالب الـ CLI |

---

## 🏆 سجل الإنجازات
- **Clarifai Parallel Pipeline**: تم بناء الإصدار الثالث (clarifai_parallel_v3.py) لتشغيل الإرسال بالتوازي (Multiprocessing) مع عزل كامل للبصمات (TLS/IP) عبر ProxyLeaseManager لحل مشاكل الـ Risk Engine. — Multi-Model Orchestration & Parallel Engine

| # | الإنجاز | الملفات |
|---|---------|---------|
| 1 | `Genspark Chat` — تطبيق التزامن المتوازي `ask_all_parallel_interactive` لتوزيع الطلبات بشكل منظم لتفادي حدود الاستخدام Rate Limits عبر مستودع الحسابات `accounts_genspark.json`. | `Genspark_V2/genspark_chat.py` |
| 2 | دمج الـ `ThreadPoolExecutor` لدعم المعالجة بالتوازي لمجموعة من المتغيرات وتخصيص Thread لكل موديل مع عزل ملفات الـ Debugging كـ `debug_{mode}_error.txt`. | `Genspark_V2/genspark_chat.py` |
| 3 | المحافظة على التوافق الرجعي للصيغ القديمة عبر CLI Fallback، للسماح للمسكربت بالتبديل السلس بين التفاعل الفردي والتفويض الجماعي المتوازي. | `Genspark_V2/genspark_chat.py` |

---

## 🆕 الملفات المحدثة — Multi-Model Orchestration

| الملف | الوظيفة |
|-------|---------|
| `Genspark_V2/genspark_chat.py` | تعديل نقطة البداية (Main) وتطبيق Orchestrator Pattern مخصص. |

---

## 📚 دروس مستفادة — AI Orchestration

| # | [TAG] | الدرس | السياق |
|---|-------|-------|--------|
| 1 | [Performance] | يمكن تحقيق تجربة "Planner-Worker" مستقرة وقابلة للتوسع عبر مزامنة الطلبات بالـ ThreadPoolExecutor، بشرط فصل ملفات السجلات (Logs/Errors) لتجنب الـ Race Conditions وفساد البيانات من التزاحم. | التفويض الجماعي المتوازي |

| #503 | [API] | تسجيل حسابات Vear (Multi-Model AI) يتطلب Google reCAPTCHA. | توقف التسجيل برمجياً بدون متصفح لعدم وجود توكن صالح. | السيرفر لا يتحقق من الـ Token المرسل للإعتماد العمياء على الفرونت إند. | إرسال أي نص مزيف في مفتاح recaptcha ضمن Payload الـ POST يمر بنجاح. | تم الحل (Server Bypass) |
| #504 | [API] | دراسة وتسجيل حماية وتخطي نظام الـ Captcha في Flow تسجيل Vear.com | تم استغلال إهمال الخوادم وتخطي التسجيل بنجاح. |
| #505 | [API] | مطابقة شكل مخرجات Vear (JSON) مع الـ Providers الأخرى (DeepSeek, Genspark) لسهولة الدمج | توحيد هيكل JSON باستخدام keys مألوفة، مثل email و password و provider و cookies بشكل هرمي متفق عليه |

---

## 🏆 سجل الإنجازات — Synottip.cz Automations

| # | الإنجاز | الملفات |
|---|--------|--------|
| 1 | بناء خط تدفق تسجيل كامل (4 مراحل متتالية) بـ `requests` وتخطي حماية السيرفر | `M_muj.synottip.cz/TEST/synottip_step3_final.py` |
| 2 | تخطي الـ Captcha (السر التقني): اكتشاف Server-side validation flaw بحذف `g-recaptcha-token` | `M_muj.synottip.cz/TEST/synottip_step3_final.py` |
| 3 | اختبار إثبات القوة (Stress Test) لاختبار أرقام SMS ورفض الأكواد غير المدعومة | `M_muj.synottip.cz/TEST/synottip_sms_proof.py` |
| 4 | تفعيل Endpoint طلب الـ SMS (`GeneratePhoneVerCode`) بنجاح باستخدام Persistent Sessions | `M_muj.synottip.cz/TEST/synottip_sms_proof.py` |

### 📁 الملفات الجديدة/المعدلة

| الملف | الوظيفة | الحالة |
|-------|---------|-------|
| `M_muj.synottip.cz/TEST/synottip_step3_final.py` | سكريبت التسجيل بـ 4 مراحل (Pure Requests) بتخطي Captcha | ✅ مستقر |
| `M_muj.synottip.cz/TEST/synottip_sms_proof.py` | اختبار إرسال الـ SMS واستجابة كود الدول | ✅ مستقر |

### 🐛 سجل المشاكل

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|---------|---------|-------|------|-------|
| #506 | [Security] | استحالة التسجيل مع Captcha Token | 400 Bad Request / 403 | السيرفر يرفض التوكنات الوهمية | حذف الـ `g-recaptcha-token` بالكامل من الـ POST payload ليتجاوزه السيرفر (Validation Flaw) | ✅ محلولة |

### 📖 دروس مستفادة

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 109 | [Security] | أحياناً يكون الـ Validation Server-side مكتوب بطريقة سيئة (يرفض القيمة الخاطئة، لكن يقبل عدم وجودها تماماً). حذف الـ reCAPTCHA token كان هو مفتاح التخطي المباشر للتسجيل في مواقع الرهانات القوية. | Synottip Captcha Bypass |

### سجل الإنجازات
- إصلاح خطأ max_tokens الفادح في genspark_API_Key_chat.py الذي كان يتسبب في حظر الحسابات برمز 402 وهمي، واستعادة 72 حساب.
- إجراء اختبار أمني شامل (Fuzzing) للـ Backend الخاص بموقع teaserid.com باستخدام أكثر من 35 طريقة لاكتشاف ثغرات الـ reCAPTCHA.
- إثبات عملي بأن حل الـ reCAPTCHA مجاناً باستخدام Pure Requests لا يعمل مع (size=normal) لأنه يتطلب إرسال بيانات (Mouse Telemetry) والتي لا يمكن توليدها إلا عبر متصفح حقيقي.

### الملفات الجديدة
- FFfree______FFfree/teaserid/teaserid_fuzz_captcha.py (تم استبداله لاحقاً)
- FFfree______FFfree/teaserid/teaserid_bypass32.py (سكريبت الفازر الشامل بـ 35 طريقة)

### سجل المشاكل
| # | [API] | ظهور كود 402 باستمرار في حسابات شغالة | رفض من السيرفر | max_tokens بقيمة 10^18 في البايلود | تم تعديله لـ 10000 | تم الحل |
| #65 | [API] | فشل تخطي كابتشا teaserid عبر Requests | السيرفر يرفض الطلبات ويرد بـ Error 500 أو rresp=null | الكابتشا مرئية (size=normal) وتتطلب تفاعل المستخدم (Mouse Telemetry) | الحل الوحيد المجاني هو SeleniumBase أو المدفوع 2Captcha | محلولة بالاستقرار على 2Captcha حالياً |

### دروس مستفادة
| # | [API] | أرقام البايلود الخرافية (مثل 10^18) ترفضها السيرفرات كـ Credits Exhausted بدلاً من Bad Request | تصحيح Genspark Chat |
| #32 | [API] | الفرق بين كابتشا Invisible و Normal | الـ Pure Requests (anchor+reload) ممكن تنجح مع الـ Invisible لو الـ IP موثوق، لكنها تفشل بنسبة 100% مع المرئية لغياب بيانات حركة الماوس. |

| #5 | [Automation] | كتابة سكربت 04_request_sms_Next.py لدمج uiautomator2 مع Keyevents لإدخال رقم الهاتف والنقر على Next | زر Next لم يكن يتفعل بعد إدخال النص | الاعتماد على Delete + Retype Keyevents لتحفيز Form Validation | تم الحل بإنشاء مجلد commit4 والسكربت الجديد | ✅ |

| # | [WhatsApp] | تم الانتهاء من تجميع كود تخطي الحماية في core_bot.py معزول | تجاوز حظر اللمس | uia_swipe micro-swipe | تم بنجاح | مكتمل |

---

## 🏆 سجل الإنجازات — Genspark URL Aggregator (شغل فريق)
- **Genspark Chat Standalone Testing**: تم بنجاح تعطيل توليد ملفات الحفظ المؤقت `genspark_urls.json` و `conversations.json` افتراضياً عند كون `save_to_json = False` مع تأمين كافة استدعاءات الـ Load والـ Save للتحقق من خيارات الـ Config.

### 🆕 الملفات المحدثة
- `..............................................................................................................شغل فريق/genspark_chat_public_URLS.py` (تأمين وتحديث السكريبت ليدعم تمرير الـ Config وفحص `save_to_json`).

### 🐛 سجل المشاكل
| #700 | [Config] | كتابة ملفات جيسون مؤقتة (genspark_urls.json و conversations.json) دون رغبة المستخدم | تراكم ملفات كاش غير مرغوبة في المجلد | الدوال العامة load_urls و load_convs كانت تُستدعى بدون التحقق من save_to_json | تعديل السكريبت وإضافة cfg كمعامل وفحص getattr(cfg, "save_to_json", False) في كافة الاستدعاءات | ✅ تم الحل |

### 📚 دروس مستفادة
| #110 | [Config] | في بيئات الاختبار المستقلة (Standalone) يجب عزل وحظر كتابة أي ملفات كاش بشكل صارم عن طريق حواجز حماية مركزية (Guards) على مستوى الـ IO | تعطيل ملفات الحفظ المؤقت |

---

## 🏆 سجل الإنجازات — Genspark Cooldown & Stress Testing
- **Genspark Cooldown & Zero Balance Verification**: تم بنجاح تطوير وتشغيل نظام اختبارات قاسي Edge-Case Stress Testing (7/7 سيناريوهات) بنسبة نجاح 100% للتأكد من صمود نظام رصيد الصفر وفترات الانتظار (29 ساعة Cooldown)، وتفريقها ذرياً عن فترات الانتظار العادية للحسابات النشطة، مع الحفاظ التام على الحسابات `active = True` لدخول فترة Cooldown ديناميكياً بدلاً من تعطيلها للأبد.
- **Git Commits Multi-Feat**: إجراء الكوميت رقم `5191d82` لحل مشكلة الـ 524 و Cooldown الـ 29 ساعة للحسابات الصفرية، والكوميت رقم `416feeb` لتأمين الـ session refresh والـ warmup والـ zero-balance.

### 🆕 الملفات الجديدة والمحدثة
- `..............................................................................................................شغل فريق/test_zero_balance_cooldown.py` (سكريبت الاختبارات القاسية لنظام رصيد الصفر والـ 29 ساعة كول داون)
- `..............................................................................................................شغل فريق/genspark_chat_public_URLS.py` (إصلاح ثغرة كول داون الصفر والـ 524)
- `..............................................................................................................شغل فريق/genspark_API_Key_chat.py` (تحديث التعامل المعماري مع خطأ 524 وكول داون الصفر)

### 🐛 سجل المشاكل
| #701 | [Performance] | تعليق الحسابات الصفرية أو دخولها في كول داون دائم أو تعطيلها تماماً | توقف الحسابات الصفرية عن العمل نهائياً وفساد قاعدة البيانات | عدم التفرقة بين كول داون الصفر (29 ساعة) وكول داون الحسابات العادية | تصميم دالة ذكية للتحقق من انتهاء الـ Cooldown وتحديث حالة الحساب ذرياً ليبقى active=True | ✅ تم الحل |

### 📚 دروس مستفادة
| #111 | [Backend] | الحسابات الصفرية يجب أن تظل active=True وتدخل في كول داون مؤقت (29 ساعة) لأن رصيدها سيتجدد تلقائياً، بدلاً من وسمها بـ active=False وتعطيلها للأبد. | تدوير حسابات Genspark |

---

## 🏆 سجل الإنجازات — Genspark Ultra Mode & Session Warmup (شغل فريق)
- **Genspark Ultra Mode (Claude Opus / 4.7) Live Test**: تم بنجاح تفعيل واختبار مود الـ Ultra المتمثل في Claude Opus 4.7 حياً وتأكيد نجاح الإرسال وحصول المستخدم على رد تفصيلي عالي الذكاء والسياق في 15 ثانية فقط، مع توثيق آلية خصم النقاط الدقيقة (يخصم 11 نقطة بدلاً من نقطة واحدة في الموديل العادي) لضبط حسابات الكول داون الـ 29 ساعة.
- **Atomic Session Warmup Completion**: تنفيذ دورة Warmup كاملة لـ 10 حسابات منتهية متتالية بنجاح 100% وتحديث كروتها ذرياً قبل إطلاق المحادثة لضمان استقرار وتخطي حماية Azure B2C.

### 🆕 الملفات المحدثة
- `..............................................................................................................شغل فريق/genspark_chat_public_URLS.py` (تحديث وتأمين مود Ultra ومزامنة كروت ورصيد الحسابات ذرياً)

### 🐛 سجل المشاكل
| #702 | [Performance] | استهلاك رصيد الحسابات السريع في مود الـ Ultra | نفاد رصيد حسابات Genspark بمعدل 11x أسرع مقارنة بالموديل الافتراضي | تفعيل Claude Opus يخصم 11 نقطة من رصيد الحساب لكل رسالة بدلاً من نقطة واحدة | توثيق معدل الاستهلاك الدقيق للموديل وتحديث الـ cooldown تلقائياً لوضع الحساب في تبريد 29 ساعة عند نفاده | ✅ تم الحل |

### 📚 دروس مستفادة
| #112 | [Performance] | تفعيل مود الـ Ultra (Claude Opus) في Genspark يسرع عملية استهلاك رصيد الحسابات (خصم 11 نقطة) ودخولها كول داون الـ 29 ساعة أسرع بكثير، لذا يجب استخدامه بشكل مدروس للمهام المعقدة فقط. | تكلفة مود الـ Ultra |

---

## 🏆 سجل الإنجازات — Genspark API Key 5-Second Overall Timeout & Fail-Fast (شغل فريق)
- **Overall Timeout & Fail-Fast Integration**: تم بنجاح بناء وتشغيل سكريبت اختبار متكامل ومستقل `test_overall_timeout.py` للتحقق حياً من تفعيل مهلة قصوى إجمالية (overall_timeout) بمقدار 5 ثواني لقطع الخيوط المعلقة والهنج، وتبريد الحساب المتأثر بـ 524 لـ 29 ساعة كاملة وقطع المحاولات متفادياً محاولات الموديلات الأخرى بدون فائدة.
- **Git Commit Completion**: تسجيل الكوميت بنجاح لكافة التغييرات وسجلات التزامن وتثبيت الأداء وحالة الأيجنت.

### 🆕 الملفات المحدثة والجديدة
- `..............................................................................................................شغل فريق/test_overall_timeout.py` (سكريبت اختبار المهلة الإجمالية حياً)
- `..............................................................................................................شغل فريق/genspark_API_Key_chat.py` (تأمين قطع المهلة وتبريد الـ 524 بـ 29 ساعة)

### 🐛 سجل المشاكل
| #703 | [Performance] | تعليق السكربتات عند بطء الـ Upstream HTTP requests في خيوط التوازي | بقاء السكربت معلقاً للأبد أو لفترات طويلة جداً مما يضر بالـ performance | خيوط التوازي (Threads) تستخدم join() عادي بدون مهلات قصوى وتنتظر للأبد | تعيين daemon=True لجميع خيوط التوازي واستخدام join(timeout) المتناقص لقطع الخيوط المعلقة فوراً عند تجاوز المهلة الإجمالية | ✅ تم الحل |

### 📚 دروس مستفادة
| #113 | [Performance] | استخدام daemon=True مع join(timeout) ذكي يوفر فرامل طوارئ قوية وحقيقية لقطع خيوط التوازي المعلقة قسرياً عند بطء الريكويستات في بيئات التوازي الكثيف. | فرامل طوارئ خيوط التوازي |

---

## 🏆 سجل الإنجازات — Genspark Model Discovery & Probing (شغل فريق)
- **Genspark Model Discovery Script**: تم بنجاح بناء وتطوير وتشغيل سكريبت مستقل وجديد `discover_genspark_models.py` لفحص 28 موديل مرشح حياً لمعرفة المتاح وغير المدعوم عبر الـ API Key الخاص بجينسبارك.
- **Concurrency Rate Limit Bypass**: حل مشكلة الـ Concurrency Limit (429) الخاصة بـ Genspark (بحد أقصى 5 طلبات متزامنة لكل حساب) عبر تشغيل الفحص بـ ThreadPoolExecutor مقيد بـ `max_workers=3` مع تطبيق آلية تراجع أسي وعشوائي (Exponential Backoff) لإعادة المحاولة بأمان.
- **Live Probing Execution**: تشغيل الفحص حياً بنجاح تام وتحديد 11 موديل نشط وفعال بنسبة 100% و 17 موديل غير مدعوم أو مرفوض مع توثيق الأخطاء.

### 🆕 الملفات الجديدة
- `..............................................................................................................شغل فريق/discover_genspark_models.py` (سكريبت الفحص والاكتشاف الذكي للموديلات المتاحة حياً)

### 🐛 سجل المشاكل
| #704 | [Performance] | اصطدام فحص الموديلات بـ Rate Limit التزامن (HTTP 429) من سيرفر جينسبارك | فشل فحص أغلب الموديلات وعودتها برمز 429 | محاولة فحص 28 موديل دفعة واحدة بالتوازي متجاوزة الحد الأقصى المسموح (5 طلبات لكل حساب) | تقييد التوازي بـ 3 Threads كحد آمن، وحقن السكربت بـ random exponential backoff retry عند التقاط الـ 429 | ✅ تم الحل |

### 📚 دروس مستفادة
| #114 | [Performance] | عند التعامل مع حدود تزامن ضيقة جداً (مثل 5 طلبات متزامنة)، يجب خفض عدد خيوط التوازي لأقل من الليميت (max_workers=3) واستخدام sleep عشوائي متصاعد لضمان عبور كافة الريكويستات بأمان دون حظر. | تخطي Rate Limit التزامن |

---

## 🏆 سجل الإنجازات — Genspark Parallel Aggregator Live Verification (شغل فريق)
- **Genspark Parallel Aggregator Live Verification**: تم بنجاح تشغيل سكريبت الأوركسترا الرئيسي `genspark_chat_public_URLS.py` حياً للاستماع لـ `chat_send.txt` وحساب عملية `25*12` بالخطوات.
- **Ultra vs Normal Mode Performance comparison**: إثبات فاعلية التوازي بمقارنة استهلاك رصيد حسابات الخزان وسرعة الاستجابة (وضع الـ Ultra استجاب في 10 ثوانٍ والعادي في 12.8 ثانية).
- **Zero Balance Cooldown & Balances Audit**: التحقق الفعلي من التحديث الذري للأرصدة في `accounts_genspark.json` ودخول الحسابين تلقائياً في فترة Cooldown 29 ساعة بنجاح كامل.

### 🆕 الملفات المحدثة
- `..............................................................................................................شغل فريق/genspark_chat_public_URLS.py`
- `Root/ai_state.json`

### 📚 دروس مستفادة
| #115 | [Performance] | التوازي في Genspark يوفر نواتج منوعة ومختلفة في نفس الوقت وبسرعات فائقة (10s-13s) ويضمن الحصول على أفضل إجابة بديلة عند تعطل أو تراجع كفاءة أحد الموديلات. | توازي حسابات جينسبارك |

---

## 🏆 سجل الإنجازات — Genspark Concurrency locking & Aggregator v2.0.0 (شغل فريق)
- **Genspark Multi-Process Concurrency locking**: تم بنجاح تطبيق المزامنة الكلية ومنع تعارض العمليات (Lost Updates / Account Collisions) في الـ 13 سكريبت بالتوازي.
- **OS Kernel-Level File Locks**: دمج مكتبة `msvcrt` على الويندوز و `fcntl` على لينكس لمنع العمليات من تعديل ملف الحسابات المشترك `accounts_genspark_V5.5.json` في نفس الوقت.
- **Deadlock & Lost Update Prevention**: تحرير الأقفال تلقائياً بواسطة نظام التشغيل عند موت أو إنهاء العملية، مع إعادة قراءة وتحديث الحساب بالكامل داخل كتلة القفل.
- **Startup Jitter**: إدخال تأخير بدء تشغيل عشوائي لكل عملية لمنع تعليق طلبات القفل.
- **Syntax Verification**: اجتياز اختبار `py_compile` لجميع السكريبتات الـ 13 بنجاح كامل.

### 🆕 الملفات المحدثة
- `..............................................................................................................شغل فريق/Genspark_*.py` (تحديث الـ 13 سكريبت)
- `Root/ai_state.json`
- `Root/memory.md`
- `Root/walkthrough.md`

### 🐛 سجل المشاكل
| #705 | [Performance] | تعارض وتداخل الحسابات وفقدان التحديثات عند تشغيل سكريبتات Genspark الـ 13 بالتوازي | تداخل وتلف ملف الحسابات `accounts_genspark_V5.5.json` | قيام العمليات بالتعديل والكتابة في نفس ملف قاعدة البيانات في نفس الوقت دون قفل | دمج أقفال الملفات على مستوى نظام التشغيل (msvcrt/fcntl) والـ Startup Jitter | ✅ تم الحل |

### 📚 دروس مستفادة
| #116 | [Performance] | أقفال الملفات المؤقتة O_CREAT تسبب Deadlocks عند كراش السكريبت، ويجب استخدام أقفال النواة Kernel Locks التي يحررها نظام التشغيل تلقائياً فور موت العملية. | حماية توازي حسابات Genspark |

---

## 🏆 سجل الإنجازات — VIFE.ai
- **VIFE.ai Lifecycle & Generation Automation**: بناء نظام دورة حياة الحسابات والإحالات المطور بالكامل لتسجيل الحسابات وشحنها وتوليد الفيديوهات محلياً وبدون متصفح بالكامل.

| # | الإنجاز |
|---|--------|
| 1 | تسجيل الحسابات وتفعيلها آلياً عبر `01.05_proxy_register_vife.py` وربطها بالماستر. |
| 2 | شحن الإحالات للحسابات الماستر بالتوازي بـ `02.01_referral_boost_vife.py` وزيادة النقاط. |
| 3 | توليد الفيديوهات 5 ثوانٍ و 11 ثانية عبر WebSocket مباشر وتخطي كواشف البوتات بـ `05.05_video_generator_vife.py`. |
| 4 | إثبات فرضية تخطي فحص الرصيد (Credit Check Bypass) وحصول الحساب الجديد على أول فيديو مجاني بالكامل بـ 30 نقطة فقط. |

---

## 🆕 الملفات الجديدة — VIFE.ai

| الملف | الوظيفة |
|-------|---------|
| `vife.ai/01.05_proxy_register_vife.py` | 🆕 تسجيل حسابات ماستر وربط الإحالات تلقائياً |
| `vife.ai/02.01_referral_boost_vife.py` | 🆕 زيادة نقاط الحساب الماستر بالإحالات التابعة له |
| `vife.ai/05.05_video_generator_vife.py` | 🆕 توليد الفيديوهات وتنزيلها تلقائياً مع تحديد المدة `--duration` |
| `vife.ai/accounts_vife.json` | 🆕 قاعدة بيانات الحسابات وتدوير الحالات |

---

## 🐛 سجل المشاكل — VIFE.ai

| # | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|---|-------|------------|---------|-------|------|--------|
| #800 | [API] | فشل توليد الفيديو بسبب نقص الرصيد | ظهور خطأ `insufficient_credits` بالـ WebSocket | توليد فيديو 5 ثوانٍ يتطلب 810 نقاط والحساب المبتدئ يملك 30 نقطة فقط | شحن الحساب بالإحالات (كل إحالة تمنح +50 نقطة) أو استغلال ثغرة التخطي للمرة الأولى | ✅ محلول |
| #801 | [Script] | خطأ `INVALID_EVENT_DATA` عند الرد على خيارات الـ WebSocket | إيقاف وفشل جلسة التوليد فجأة | إرسال الرد بالحدث تحت `"type": "message"` بدلاً من `"type": "send_message"` | تعديل الحدث ليرسل كـ `"send_message"` مع ترقية عداد حزم الـ Socket.io (ACK) تصاعدياً | ✅ محلول |
| #802 | [Script] | تعليق الجلسة للأبد عند بطء خوادم VIFE.ai | السكريبت لا ينتهي ويظل معلقاً | عدم وجود مهلة قصوى لجلسة الـ WebSocket بالسكريبت | إدخال مهلة قصوى (overall timeout) قدرها 10 دقائق لجلسة الـ WebSocket لإنهاء الاتصال عند التشنج | ✅ محلول |

---

## 📚 دروس مستفادة — VIFE.ai

| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 117 | [API] | خوادم VIFE.ai تمنح كل حساب جديد محاولة توليد فيديو أولى مجانية بالكامل (تتخطى فحص الرصيد) كعرض ترويجي، مما يتيح للسكريبت توليد فيديو واحد فورياً لكل حساب بدون إحالات. | Free Video Bypass |
| 118 | [Script] | عند محاكاة أحداث Socket.io/WebSocket، يجب الحفاظ على ترقيم تصاعدي لحزم الـ ACK لتطابق بروتوكول الخادم وتفادي الرفض الصامت للطلبات. | WebSocket ACK IDs |

---

## 🏆 سجل الإنجازات — Active Team Backup & Zip (شغل فريق)
- **Active Team Scripts Backup**: تم بنجاح نسخ الـ 23 سكربت نشط ومشغل الفريق مع مجلدات الموديلات التابعة وملف حسابات جروك `accounts_Groq.json` (في الروت وفي مجلد `groq/` لضمان صحة المسارات النسبية للسكربتات) وتجهيزهم بملف ZIP واحد خفيف جداً.

### 🆕 الملفات الجديدة
| الملف | الوظيفة | الحالة |
|-------|---------|--------|
| `scratch/copy_and_zip.py` | سكريبت أتمتة نسخ السكربتات النشطة والمجلدات وحسابات جروك (لموقعين بالروت وبمجلد `groq/`) وضغطها | ✅ مستقر |
| `active_team_backup.zip` | الملف المضغوط النهائي لسكربتات ومجلدات وحسابات جروك | ✅ جاهز |

### 📚 دروس مستفادة
| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 119 | [Performance] | عند أخذ نسخ احتياطية للمشاريع، يجب الحفاظ على البنية الهيكلية للمجلدات الفرعية وملفات الحسابات بمساراتها النسبية المتوافقة مع الكود (مثل accounts_Groq.json بالروت ومجلد groq/) لتفادي الـ Runtime Errors. | نسخ وضغط السكربتات |

---

## 🏆 سجل الإنجازات — Genspark grok-4.5 Support & Payload Realignment (شغل فريق)
- **Genspark grok-4.5 Support**: تم بنجاح تعديل الموديل الافتراضي في `Genspark_grok-4.5.py` ليكون `grok-4.5` ومطابقة بايلود `ask_proxy` بنسبة 100% للطلبات الحية، مع معالجة وتحليل الـ payload ليعمل بوضع `ai_chat` الخاص بالـ client.
- **Syntax verification**: نجاح عملية التجميع والتحقق من سلامة البناء النحوي للسكريبت بنسبة 100% وخروجه برمز كود 0.

### 🆕 الملفات المحدثة
- `..............................................................................................................شغل فريق/Genspark_grok-4.5.py` (تحديث الموديل وقائمة التوجيه)

### 📚 دروس مستفادة
| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 120 | [Script] | إضافة موديلات الدردشة الحديثة مثل `grok-4.5` تتطلب إلحاقها بقائمة النماذج ذات البايلود المخصص للدردشة التفاعلية (`ai_chat`) لكي لا تفشل في طلبات الـ ask_proxy الخلفية. | تخصيص بايلود grok-4.5 |
| 121 | [Script] | عند نسخ سكريبتات أو عمل Fork لموديل جديد، يجب تحديث ACTIVE_MODELS الخاصة بوضع التوازي/التفاعل لتفادي استدعاء الموديل القديم من الذاكرة أو الكاش. | توازي حسابات Genspark |

---

## 🏆 سجل الإنجازات — Use.ai In-Memory V4 (شغل فريق)
- **Use.ai In-Memory Flow & Simplification**: تم بنجاح تبسيط معمارية سكريبتات Use.ai وإلغاء نظام الـ Pool وقفل الملفات المعقد بالكامل، والاعتماد على التسجيل الحي الفوري في الذاكرة (In-Memory Flow) عند كل تشغيل بنسبة 100%.
- **Resilience & Retry with Jitter**: دمج آلية إعادة محاولة ذكية (3 محاولات) مع Backoff متصاعد و Jitter عشوائي لمنع الـ Thundering Herd والـ Rate Limit (429) أثناء التشغيل المتوازي المتزامن.
- **Syntax & E2E Validation**: اجتياز اختبارات الـ compile والتشغيل الفردي والمتوازي بنجاح تام وحصول السكريبتات على الردود وروابط الشير دون تولد أي ملفات `.lock` على القرص.

### 🆕 الملفات المحدثة
- `..............................................................................................................شغل فريق/use_ai__claude-sonnet-5.py` (تبسيط المعمارية وتطبيق الـ In-Memory والـ Retry لـ Claude Sonnet 5)
- `..............................................................................................................شغل فريق/use_ai__claude-sonnet-4-6.py` (تحديث Claude Sonnet 4.6 ليعمل في الذاكرة بالكامل)
- `..............................................................................................................شغل فريق/use_ai__glm-5-2.py` (تحديث GLM 5.2 ليعمل في الذاكرة بالكامل)
- `..............................................................................................................شغل فريق/use_ai__grok-4-3.py` (تحديث Grok 4.3 ليعمل في الذاكرة بالكامل)
- `..............................................................................................................شغل فريق/use_ai__gpt-5-5.py` (تحديث الشات الموحد وتغيير الاسم إلى GPT-5-5 ليعمل في الذاكرة)
- `..............................................................................................................شغل فريق/0-team_runner.py` (تحديث خريطة الموديلات لتوجه للاسم الجديد)
- `..............................................................................................................شغل فريق/Root/ai_state.json` (تحديث سجل الحالة)
- `..............................................................................................................شغل فريق/Root/tasks.md` (مزامنة المهام المكتملة)



### 📚 دروس مستفادة
| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 122 | [Script] | في سكريبتات الأتمتة ذات الحسابات المؤقتة التي تُستخدم لمرة واحدة، الاعتماد على الذاكرة (In-Memory) لتوليد الجلسة مباشرة يلغي تعقيدات الأقفال والـ Race Conditions في البيئة الجماعية. | تبسيط أتمتة Use.ai |
| 123 | [Script] | إضافة Jitter عشوائي طفيف لآلية الـ Backoff للـ Retries تمنع اصطدام العمليات المتزامنة في إرسال طلبات التسجيل لنفس الـ API وتجاوز الـ Rate Limit 429. | حماية التسجيل المتوازي |

---

## 🏆 سجل الإنجازات — Use.ai & Genspark Scripts Zip Compression (شغل فريق)
- **Unified Scripts Compression**: تم بنجاح ضغط الملفات التسعة المحددة من سكريبتات `use_ai` و `Genspark` (ومنها موديلات GPT 5.6 و Grok 4.5 و Sonnet 4-6) في أرشيف مضغوط واحد باسم `شغل_فريق_ملفات.zip` لتسهيل نقلها وحفظ سورس كود الفريق.
- **Sub-repo Tracking & Commit**: تم إضافة وتأمين الملف المضغوط الجديد في مستودع الجيت الفرعي الخاص بمجلد `شغل فريق` لضمان إدراجه تحت رقابة النسخ.

### 🆕 الملفات الجديدة والمحدثة
- `..............................................................................................................شغل فريق/شغل_فريق_ملفات.zip` (الملف المضغوط النهائي لـ 9 سكريبتات نشطة)

### 🐛 سجل المشاكل
| #706 | [Script] | خطأ ترميز UnicodeEncodeError عند تشغيل سكريبت ضغط الملفات على نظام Windows | فشل ضغط الملفات وخروج سكريبت البايثون بخطأ 1 | محاولة طباعة اسم الملف المضغوط المحتوي على حروف عربية مباشرة على stdout الافتراضي للـ cmd/PowerShell | تعديل ترميز الـ stdout ليكون UTF-8 برمجياً عبر `sys.stdout.reconfigure(encoding='utf-8')` لتخطي قصر ترميز Windows | ✅ تم الحل |

### 📚 دروس مستفادة
| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 124 | [Script] | في بيئات نظام التشغيل Windows، يجب دائماً إعادة تكوين ترميز الـ standard output للـ Python إلى UTF-8 عند طباعة أي حروف عربية أو غير لاتينية لتجنب أخطاء الترميز الصامتة أو القاتلة. | ترميز الكونسول في ويندوز |

---

## 🏆 سجل الإنجازات — سكريبت التكرار والثريدات المتعددة لفيسبوك (04_resend_loop_threads.py)
- **Multi-threaded Resend Automation**: بناء وتشغيل سكريبت `04.02_resend_loop_threads.py` متكامل الأركان بنظام Lock آمن لمنع تكرار الحسابات أو الأرقام أو البروكسيات عبر الثريدات المتوازية.
- **English Terminal Logging Support**: إعادة صياغة رسائل الطباعة والتسجيل بالكامل للغة الإنجليزية بناءً على طلب العميل للتغلب على مشاكل الحروف العربية المقلوبة في كونسول ويندوز.
- **Dynamic CWD Paths Resolving**: دمج آلية توجيه ديناميكية ذكية للمسارات النسبية للملفات تكتشف مجلد `facebook__SMS` تلقائياً وتوجه المخرجات/المدخلات إليه عند تشغيل السكريبت من المجلد الرئيسي.

### 🆕 الملفات الجديدة والمحدثة
- `facebook__SMS/04_resend_loop_threads.py` (السكريبت الأصلي باللغة العربية)
- `facebook__SMS/04.02_resend_loop_threads.py` (النسخة المعربة بالكامل للغة الإنجليزية في المخرجات)

### 🐛 سجل المشاكل
| #707 | [Script] | خطأ عدم العثور على ملفات المدخلات (حسابات_كوكيز.txt) عند التشغيل من المجلد الرئيسي | توقف السكربت بخطأ 1 | محاولة قراءة الملفات من المجلد الحالي للعمل بينما هي موجودة داخل المجلد الفرعي facebook__SMS | إضافة كود ديناميكي في parse_args() يتحقق من وجود الملف في مجلد facebook__SMS تلقائياً إن لم يوجد بالرئيسي | ✅ تم الحل |
| #708 | [UI] | حروف الكونسول العربي مقلوبة ومقروءة بشكل خاطئ في Command Prompt نظام ويندوز | صعوبة تتبع حالة تشغيل الثريدات | عدم دعم التيرمينال الافتراضي لترميز الحروف العربية أحادية الاتجاه RTL | تحويل كافة رسائل كونسول السكريبت بالكامل للغة الإنجليزية في نسخة 04.02 بناءً على طلب العميل | ✅ تم الحل |

### 📚 دروس مستفادة
| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 125 | [Script] | في السكريبتات التي تعتمد على مدخلات ومخرجات نصية معقدة على ويندوز، يفضل توفير ترميز أو مخرجات إنجليزية لتلافي عيوب تيرمينال CMD/PowerShell في عرض اللغة العربية. | طباعة لغة عربية في ويندوز |
| 126 | [Config] | معالجة المسارات برمجياً بالتحقق من تواجد المجلدات الفرعية يوفر مرونة كاملة في طريقة استدعاء الأتمتة (سواء من مسارها أو من مسار الروت). | مرونة مسارات المدخلات |

---

## 🏆 سجل الإنجازات — فحص كوكيز فيسبوك المتوازي السريع (01.03_check_fb_cookies_fast.py)
- **Fast Parallel Cookies Checker**: إنشاء سكريبت فحص متوازي فائق السرعة `01.03_check_fb_cookies_fast.py` باستخدام ThreadPoolExecutor بـ 25 ثريد متزامن مع مكتبة `curl_cffi` لمحاكاة بصمة المتصفح الكاملة وتفادي WAF.
- **E2E Cookies Scan**: فحص كامل لـ 531 حساب كوكيز من ملف `حسابات_كوكيز.txt` في أقل من 40 ثانية.
- **Detailed Evidence Reporting**: تصنيف الحسابات بالكامل وتوليد تقرير كامل بالأدلة والـ URL النهائي وعناوين الصفحات وحجم الاستجابة في `تقرير_فحص_الكوكيز.md`.
- **Results Extraction**: تم استخراج الحسابات وتصنيفها بالكامل (0 شغال، 531 فاشل منتهي/حماية)، وحفظ الحسابات الشغالة والنشطة في `حسابات_كوكيز_شغال.txt` والحسابات الفاشلة في `حسابات_كوكيز_فاشل.txt`.

### 🆕 الملفات الجديدة والمحدثة
| الملف | الوظيفة | الحالة |
|-------|---------|--------|
| `facebook__SMS/01.03_check_fb_cookies_fast.py` | سكريبت الفحص المتوازي السريع لحسابات فيسبوك | ✅ مستقر وجاهز |
| `facebook__SMS/تقرير_فحص_الكوكيز.md` | تقرير الفحص المكتوب والمصنف كاملاً بالأدلة التفصيلية | ✅ تم إنشاؤه |
| `facebook__SMS/حسابات_كوكيز_شغال.txt` | الحسابات الشغالة والنشطة المفرزة | ✅ فارغ (0 حسابات شغالة) |
| `facebook__SMS/حسابات_كوكيز_فاشل.txt` | الحسابات الفاشلة (منتهية أو مقفلة بـ Checkpoint) | ✅ يحتوي على 531 حساب |

### 📚 دروس مستفادة
| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 127 | [Script] | استخدام `ThreadPoolExecutor` مع مكتبة `curl_cffi` يتيح تسريع فحص كوكيز الحسابات بمعدلات توازي عالية جداً بدون إحداث تعليق أو حظر للبصمة (JA3 Bypass). | فحص كوكيز فيسبوك |
| 128 | [Script] | كوكيز فيسبوك المنتهية منذ فترة طويلة (أكثر من سنة) يتم توجيهها تلقائياً لصفحة تسجيل الدخول أو الـ Checkpoint لحماية الحساب. | فحص كوكيز فيسبوك |

---

## 🏆 سجل الإنجازات — Use.ai Pure Requests 3-Script Flow & WebSocket Bypass (شغل فريق)
- **3-Script Architecture**: تقسيم تدفق الـ Use.ai إلى ثلاثة سكريبتات مستقلة تماماً: سكريبت إنشاء الحساب والبريد (`07_register_tempmail_use_ai.py`)، وسكريبت اللوجن والتفعيل وتخطي الروابط السحرية بالبريد المؤقت (`08_login_tempmail_use_ai.py`)، وسكريبت الشات المركزي والـ WebSocket الأوركسترا (`09_chat_use_ai.py`).
- **WebSocket Handshake 403 Bypass**: تخطي مشكلة الـ 403 Forbidden بجلب توكنات الـ WebSocket والـ App Attestation المطلوبة حديثاً للاتصال وتمريرها في الـ query string.
- **Account & Mailbox Auto-Destruction**: تدمير الحسابات والبريد المؤقت تلقائياً بمجرد انتهاء الشات لمنع تراكم الحسابات والحفاظ على الأمان.

### 🆕 الملفات الجديدة
| الملف | الوظيفة | الحالة |
|-------|---------|--------|
| `use.ai_AI/07_register_tempmail_use_ai.py` | سكريبت إنشاء البريد المؤقت والتسجيل التلقائي في Use.ai بدون متصفح وحفظ الحساب في الجيسون | ✅ مستقر |
| `use.ai_AI/08_login_tempmail_use_ai.py` | سكريبت إرسال كود اللوجن وقراءة البريد وتخطي الروابط السحرية ديناميكياً وتحديث الجلسة | ✅ مستقر |
| `use.ai_AI/09_chat_use_ai.py` | سكريبت المحادثة والأوركسترا المركزي لإدارة الحسابات وربط الـ WebSocket وتدمير الجلسات | ✅ مستقر |

### 🐛 سجل المشاكل
| #رقم | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|------|-------|-------------|---------|-------|------|--------|
| #709 | [Script] | فشل اتصال الـ WebSocket للـ Use.ai بـ 403 Forbidden | توقف الشات وصعوبة تدفق الرد | حظر الخادم للاتصال المباشر لعدم وجود توكنات الـ WS والـ App Attestation المتولدة بالطلب الخلفي | جلب التوكنات بطلبين get و post باستخدام كوكيز الجلسة وتمريرهم كـ query parameters | ✅ تم الحل |

### 📚 دروس مستفادة
| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 129 | [Script] | الاتصالات الحديثة عبر الـ WebSockets في منصات الـ AI تتطلب توقيع/Attestation إضافي يتم جلبه عبر API منفصل وتمريره برابط الاتصال لتخطي قيود الـ WAF والأمان. | تخطي 403 في WebSocket Use.ai |
| 130 | [Script] | فك تشفير روابط Customer.io المضمنة في إيميلات التفعيل ديناميكياً يتيح الحصول على الروابط السحرية الحقيقية بنقاء ودون الحاجة لتشغيل متصفح كامل. | قراءة وتفعيل الروابط السحرية |

## 🏆 سجل الإنجازات — اختبار وكيل مراجعة الكود والتحضير لـ gpt-sol workflow (شغل فريق)
- **Code Review Proxy Testing**: اختبار وتأكيد عمل سكريبت `Genspark_gpt-5.6-sol.py` كـ كوبري/وسيط كامل لنقل السياق البرمجي الكامل وكود ملف `upload_tar_to_github.py` والأسئلة الثلاثة والحصول على مراجعة دقيقة من الموديل Sol دون تدخل برمي مباشر.
- **Warmup & Refresh**: تشغيل وتأكيد نجاح عملية الـ Warmup وتجديد الجلسات التلقائي في الخلفية لـ 10 حسابات منتهية الصلاحية وجلب الأرصدة الحقيقية بنجاح.

### 🆕 الملفات المحدثة
| الملف | الوظيفة | الحالة |
|-------|---------|--------|
| `d:\SMS\.hRhRhRhRhRhR\..............................................................................................................شغل فريق\chat_send.txt` | ملف تخزين ونقل السياق والأسئلة المرسلة للموديل | ✅ مستقر |

### 🔑 سجل المشاكل
| #رقم | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|------|-------|-------------|---------|-------|------|--------|
| #710 | [Script] | فشل اختيار الحسابات لـ gpt-5.6-sol بسبب انتهاء الجلسات وتخطي الحد الأدنى للرصيد | رسالة خطأ بعدم وجود حسابات جاهزة لـ gpt-5.6-sol | تفعيل تصفية الحسابات بحد رصيد (min-balance = 90) مع انتهاء صلاحية جلسات الحسابات المتاحة | تشغيل الـ Warmup لتنشيط الجلسات تلقائياً وتمرير بارامتر `--min-balance 0` للسماح باستخدام الحسابات النشطة | ✅ تم الحل |

### 📚 دروس مستفادة
| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 131 | [Script] | تمرير حد رصيد منخفض أو صفر (min-balance 0) يضمن استمرارية تشغيل الاسكريبتات على الحسابات النشطة طالما تم تجديد جلساتها تلقائياً في الخلفية. | تجاوز مشكلة رصيد الحسابات المنتهي لسكريبت Genspark_gpt-5.6-sol.py |

---

## 🏆 سجل الإنجازات — تحليل وفحص فيديوهات بسطتهالك و VdoCipher DRM (_بطه/New folder)
- **1-Minute Video Detection**: تحليل فحص ملفات الـ HAR (`bassthalk..com.har` و `bassthalk.2.com.har`) وتحديد فيديو "مُقدمــة المحاضرة الثانية لرجالتنا أولى ثانوي🤍" ومدته 1 دقيقة واستخراج كافة الـ Requests الخاصة به.
- **DRM & Auth Diagnostics**: توثيق وبناء تقرير شامل يشرح خطأ `401 Unauthenticated` وهيدرات التوكن المطلوب، وطبيعة تشفير VdoCipher DRM وكيفية تداول المفاتيح.
- **Folder Documentation**: إنشاء وثيقة التقرير الشامل `README.md` بالمسار `_بطه/New folder/README.md`.

### 🆕 الملفات الجديدة والمحدثة
| الملف | الوظيفة | الحالة |
|-------|---------|--------|
---

## 🏆 سجل الإنجازات — تشغيل بيئة الأيجنتس السحابية والحلبة المتوازية لـ NoteGPT والـ Sandbox Exporter (.AAA_GGG_iii_VIBE_CODING)
- **Pure Agent Sandbox Engine**: بناء وتطوير محرك الأيجنتس السحابي الكامل `test_notegpt_agent_mode.py` لتشغيل بيئات الـ Linux Sandbox الحقيقية على NoteGPT بـ Pure Requests بدون متصفح.
- **Two-Phase History Persistence**: حل معضلة عدم ظهور المحادثات في قائمة Recents بالمتصفح عبر تطبيق بروتوكول المزامنة الثنائي (`POST /api/v2/ai-chat` عند البدء و `PUT /api/v2/ai-chat` عند الاكتمال مع مصفوفة الـ blocks والـ credit_usage).
- **Parallel Duel Benchmark**: بناء حلبة المبارزة المتوازية `test_deepseek_vs_minimax_agent_duel.py` واختبار موديل `DeepSeek V4 Flash` ضد `MiniMax M3` في مسائل معمارية معقدة (Distributed Locks و Asyncio Circuit Breaker).
- **Auto Sandbox Exporter**: بناء وتفعيل أداة الاستخراج والتنزيل التلقائي للملفات البرمجية التي ينشئها الأيجنت داخل الـ Sandbox وحفظها في مجلدات محلية منظمة.

### 🆕 الملفات الجديدة والمحدثة
| الملف | الوظيفة | الحالة |
|-------|---------|--------|
| `.AAA_GGG_iii_VIBE_CODING/test_notegpt_agent_mode.py` | محرك تشغيل الأيجنتس السحابي الحقيقي لـ NoteGPT مع المزامنة، التصدير التلقائي، تتبع الـ 3-Phase، والبطاقة الختامية الفخمة | ✅ مكتمل ومستقر |
| `.AAA_GGG_iii_VIBE_CODING/test_deepseek_vs_minimax_agent_duel.py` | حلبة المقارنة المتوازية الفورية 100% بين DeepSeek V4 و MiniMax M3 مع تصدير ملفات الـ Sandbox | ✅ مكتمل ومستقر |
| `.AAA_GGG_iii_VIBE_CODING/NOTEGPT_AGENT_SANDBOX_MASTER_DOCUMENTATION.md` | المرجع الهندسي والتشريحي الشامل لبروتوكول الأيجنتس، تشريح الـ HARs، وحلول التوقف والـ Quotas | ✅ موثق ومعتمد |
| `.AAA_GGG_iii_VIBE_CODING/agent_sandbox_output/deepseek_circuit_breaker/` | حزمة ملفات Circuit Breaker الكاملة المنشأة والمختبرة بواسطة DeepSeek V4 Flash | ✅ مستخرجة ومختبرة |

### 🔑 سجل المشاكل
| #رقم | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|------|-------|-------------|---------|-------|------|--------|
| #711 | [API] | عدم ظهور ردود الأيجنتس في قائمة Recents على موقع NoteGPT بعد انتهاء الستريم | ظهور المحادثة بعنوان None ومحتوى فارغ في واجهة الويب | فصل سيرفر الستريم عن قاعدة بيانات السجل واشتراط إرسال طلب PUT /api/v2/ai-chat مع مصفوفة الـ blocks | تطبيق المزامنة الثنائية وإرسال طلب PUT متضمن التفكير والنص والكريديت تلقائياً | ✅ تم الحل |
| #712 | [Script] | احتجاز الملفات البرمجية والمشاريع المنشأة بواسطة الأيجنت داخل بيئة الـ Linux Sandbox السحابية | ظهور رد نصي مختصر في الشات بينما الأكواد الكاملة موجودة بملفات الـ Sandbox | قيام الموديل بإنشاء ملفات عبر Tool Calls داخل مسار /home/daytona/ بدلاً من طباعتها كنص شات | بناء Auto Sandbox Exporter لاستخراج وتحميل كافة الملفات المنشأة تلقائياً إلى القرص المحلي | ✅ تم الحل |
| #713 | [API] | انقطاع بث الـ Stream وتوقف الأيجنت أثناء كتابة الملفات واختبارات Pytest الطويلة | توقف مؤشر الكتابة بعد 30 ثانية دون تسليم الملفات كاملة | قيود خوادم SSE/Cloudflare على أقصى مهلة للاتصال الواحد أثناء تشغيل التيرمينال الداخلي | اكتشاف واستخدام بروتوكول الاستئناف `POST /api/v2/chat/agent-stream/continue` الذي يعيد ربط الـ Session دون فقدان كود الساندبوكس | ✅ تم الحل |
| #714 | [Quotas] | قفل الجولة الأولى برمز `free_credits_insufficient` بعد استهلاك 11 كريديت | توقف الموديل المفاجئ قبل إتمام الـ 30 اختبار | تفعيل حد ناعم (Soft Quota Limit) في الجولة الأولى لحماية الخوادم من الاستهلاك المفرط | إعادة إرسال السؤال في نفس الـ `conversation_id` لاستئناف الساندبوكس واستهلاك 14 نقطة إضافية (إجمالي 25) لإنهاء الـ 30 test | ✅ تم الحل |
| #715 | [UI] | الخلط بين الرسالة التمهيدية الأولى واكتمال رد الأيجنت النهائي | ظهور حالة اكتمال المهمة مبكراً بينما الأيجنت ما زال يفكر ويكتب الملفات | قيام الأيجنت بإرسال نص تمهيدي سريع قبل الدخول في دورة الـ Agent Loop والـ Tool Calls | بناء معمارية الـ 3-Phase Live Lifecycle وتأطير الرد ببطاقة تقرير ختامي نيون مع تمييز الموديلات بالأيقونات | ✅ تم الحل |

### 📚 دروس مستفادة
| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 134 | [API] | معمارية منصات الأيجنتس الحديثة تفصل بين خادم بث الـ LLM وخادم قاعدة بيانات الـ UI، مما يستوجب إرسال طلب تأكيد ختامي لحفظ شجرة الرسائل. | مزامنة سجل NoteGPT Web UI |
| 135 | [Architecture] | نماذج التفكير العميق (Deep Reasoning) في وضع الأيجنتس تستغل وقت التفكير في إنشاء ملفات حقيقية داخل بيئة معزولة وتشغيل Unit Tests قبل إخراج الرد النهائي للمستخدم. | تحليل أداء DeepSeek V4 Flash في الـ Sandbox |
| 136 | [API] | مسار `agent-stream/continue` هو الآلية المعتمدة لاستئناف دورات الـ Agent Loop الطويلة في بيئات الساندبوكس السحابية عند حدوث Stream Timeouts. | فحص HAR #1 و HAR #2 |
| 137 | [Architecture] | الجلسات المفتوحة مسبقاً تسمح بـ Quota Overdraft لاستكمال بناء الملفات وتشغيل الاختبارات، وإعادة التوجيه لنفس الـ conversation_id يستأنف نفس بيئة اللينكس بدون تصفير. | تشريح استهلاك 25 كريديت لـ DeepSeek V4 |
| 138 | [UX] | بطاقات التقارير الختامية المؤطرة بـ Double-Line Neon Box توفر رؤية هندسية واضحة للوقت، الكريديت، وحالة ملفات الساندبوكس المنشأة. | تصميم لوحة التقرير التنفيذي في CLI |
---

## 🏆 سجل الإنجازات — ترقية حوكمة بولا v1.2 وتطهير الروت والنواة السداسية الموحدة (v2.6 Unified Core Edition)
- **Bolla Constitution v1.2 & Ironclad Citation**: ترقية وتثبيت دستور بولا الهندسي v1.2 والقوانين العشرة، وتفعيل الترسانة الفولاذية لقانون الإسناد المرجعي الصريح بالسطور (Law 8 Ironclad) لمنع التخمين وحظر الكلمات الاستنتاجية وفرض قالب الدليل المرجعي وقاعدة BEFORE/AFTER بالأرقام.
- **Unified Memory Core & FATAL RULE #SYNC**: اعتماد وتثبيت النواة السداسية الموحدة للاستمرارية حصراً داخل مجلد `Root/` (`ai_state.json`, `PROGRESS.md`, `tasks.md`, `memory.md`, `keys.txt`, `ANCHORS.md`, `HANDOFF.md`) مع فرض التحديث الإلزامي اللحظي.
- **Workflows Upgrades to v2.0**: ترقية وتوحيد مسارات العمل القياسية (`00-planning.md`, `00-sequential-requests.md`, `00-speckit.md`) لتدعم التدرج الثلاثي T0/T1/T2 والمراسي التشفيرية المشفرة بـ SHA-256 وتطهير مهارة التخطيط `02-planning-system`.
- **Forensic Debris Purge (108 Items Archived)**: إجراء فحص جنائي شامل وتطهير ركام الروت العام ونقل 108 عناصر عائمة (سكربتات، لوجات بمئات الكيلوبايتات، صور، ملفات مضغوطة، برومبتات مبعثرة) إلى أرشيف محمي ومنظم، وتصفية ملفات الروت العام من 80+ إلى 12 ملفاً فقط أساسياً.
- **Resolve __ROLE Duplication**: حسم ازدواجية السجلات بين `__ROLE/` و `Root/` بنقل تقارير وسكريبتات المراحل السابقة (P1 ➔ P3D) إلى الأرشيف وترك مؤشر دستوري نظيف، وتوحيد `AGENTS.md` و `PROGRESS.md` في الروت كمؤشرات قياسية للأصل.

### 🆕 الملفات الجديدة والمحدثة
| الملف | الوظيفة | الحالة |
|-------|---------|--------|
| `.agents/AGENTS.md` | المرجع الدستوري والتشغيلي الموحد v2.6 مع النواة السداسية وقوانين بولا | ✅ معتمد ونشط |
| `.agents/rules/00-bolla-constitution.md` | دستور بولا الهندسي v1.2 مع الترسانة الفولاذية لقانون الإسناد السطري | ✅ مشمع بـ SHA-256 |
| `.agents/workflows/00-planning.md` | نظام التخطيط الهندسي الشامل v2.0 (12 منهجية عالمية متكاملة مع بولا) | ✅ مشمع بـ SHA-256 |
| `.agents/workflows/00-sequential-requests.md` | نظام التطوير التتابعي v2.0 ومطابقة الـ HAR بالسطور | ✅ مشمع بـ SHA-256 |
| `.agents/workflows/00-speckit.md` | نظام التطوير المبني على المواصفات Spec-Kit v2.0 المتكامل مع القانون 9 | ✅ مشمع بـ SHA-256 |
| `.agents/skills/02-planning-system/SKILL.md` | مهارة التخطيط الرسمية النظيفة (القوالب الـ 5 وسجل الـ ADR Tracker) | ✅ مشمع بـ SHA-256 |
| `AGENTS.md` (في الروت العام) | مؤشر دستوري قياسي (SSOT Pointer) يوجه لـ `.agents/AGENTS.md` | ✅ نشط |
| `PROGRESS.md` (في الروت العام) | مؤشر وفهرس تنفيذي قياسي يوجه للأصل الحي في `Root/PROGRESS.md` | ✅ نشط |
| `Root/PROGRESS.md` | السجل التنفيذي العام الشامل للمشروع (المراحل من P0 إلى P11) | ✅ محدث وموثق |
| `Root/ANCHORS.md` | سجل المراسي التشفيرية المشفرة بـ SHA-256 لكافة ملفات القواعد والكود | ✅ محدث ومشمع |
| `Root/ai_state.json` | بوصلة الحالة والوضع اللحظي للنظام | ✅ محدث لحظياً |

### 🐛 سجل المشاكل
| #رقم | [TAG] | وصف المشكلة | الأعراض | السبب | الحل | الحالة |
|------|-------|-------------|---------|-------|------|--------|
| #716 | [Architecture] | تضخم وتكرار `ai_state.json` في 33 موضعاً بـ `AGENTS.md` مع وجود نصوص ملغاة | تشتت بوصلة الحالة وتضخم حجم الدستور لـ 565 سطراً | التراكم غير المنظم عبر جلسات عمل متعددة | إعادة هيكلة الدستور واختصاره لـ 236 سطراً وتثبيت النواة السداسية للاستمرارية حصراً داخل `Root/` | ✅ تم الحل |
| #717 | [Architecture] | وجود مراجع معطوبة لمجلدات مؤرشفة وأوامر ميتة لـ `crew.runner` في مسارات التخطيط والـ Spec-Kit | ارتباك الوكلاء بمحاولة استدعاء أدوات ملغاة | بقايا أنظمة سابقة ملغاة لم تُطهر | ترقية سير عمل التخطيط والـ Spec-Kit إلى v2.0 Bolla-compliant وتطهير مهارة التخطيط بالكامل | ✅ تم الحل |
| #718 | [Environment] | تراكم أكثر من 80 ملفاً عائماً بالروت العام مع صراع ازدواجية بين `__ROLE/` و `Root/` | تلوث الروت العام وانقسام مصدر الحقيقة لـ PROGRESS و HANDOFF | ترك مخلفات التجارب والمراحل السابقة بالروت دون عزل | أرشفة 108 عناصر عائمة وتثبيت `Root/` كمرجع أحادي وتحويل ملفات الروت لمؤشرات دستورية | ✅ تم الحل |

### 📚 دروس مستفادة
| #رقم | [TAG] | الدرس | السياق |
|------|-------|-------|-------|
| 139 | [Architecture] | تثبيت النواة السداسية للاستمرارية داخل مجلد مركزي واحد (`Root/`) يحمي الوكلاء من التشتت ويمنع تضارب الحالات اللحظية. | تطهير وتوحيد AGENTS.md v2.6 |
| 140 | [Governance] | قانون الإسناد المرجعي الصريح بالسطور (Bolla Law 8) وقالب الدليل المرجعي الإلزامي يمنعان الهلوسة والتخمين بنسبة 100%. | ترسانة الإثبات الفولاذية Law 8 Ironclad |
| 141 | [Architecture] | حظر وضع أي سكريبتات كود أو ملفات تجارب عائمة في الروت العام (القانون 10) يحمي مساحة العمل ويجعلها غرفة عمليات معقمة خالية من الهلوسة. | التطهير الجنائي الشامل وأرشفة 108 عناصر |
| 142 | [Architecture] | استخدام نمط المؤشرات الدستورية النظيفة (SSOT Pointers) في روت المشروع يوجه أدوات الـ AI للمصدر الحقيقي دون تكرار المحتوى (DRY). | توحيد AGENTS.md و PROGRESS.md في الروت |
