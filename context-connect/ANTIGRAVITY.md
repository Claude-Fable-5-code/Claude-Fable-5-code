# Antigravity — ربط السياق بالمحرر الموجود عندك

أنت بالفعل معاك وكيل داخل Google Antigravity IDE؛ المقترح هنا **تنظيم تسليم المراجعة له**، مش بناء وكيل جديد ولا تثبيت محرر بديل.

## ما ثبت من المصادر الرسمية

تاريخ الاطلاع: 2026-09-05. صفحات ويب بلا ترقيم سطور ثابت؛ الاستشهاد هنا باسم القسم والاقتباس، لا بأرقام سطور مصطنعة.

| المصدر الرسمي | القسم / الاقتباس | الدلالة وحدودها |
|---|---|---|
| [Product](https://antigravity.google/product/antigravity-ide/) | Agent: “Able to autonomously operate across your editor, terminal, and browser.” | يستطيع الوكيل العمل عبر هذه الأسطح؛ لا يثبت صلاحيات GitHub في جلستنا |
| [Product](https://antigravity.google/product/antigravity-ide/) | User Feedback: “Leave comments and feedback on any Artifact to better guide the Agent.” | يمكن استخدام artifacts للمراجعة؛ ليست بديلًا عن حفظ Git |
| [Rules](https://antigravity.google/docs/rules-workflows) | “Global rules live in `~/.gemini/GEMINI.md` and are applied across all workspaces.” | القواعد العامة تؤثر على مشاريع متعددة؛ لا تضع فيها stack مشروع واحد |
| [Rules](https://antigravity.google/docs/rules-workflows) | Workspace Rules: “Workspace rules live in the `.agents/rules` folder of your workspace or git root.” | `.agents/rules` مسار موثق حاليًا |
| [Rules](https://antigravity.google/docs/rules-workflows) | “Rules files are limited to 12,000 characters each.” | الحد بالحروف، لا bytes؛ لا تضع تقرير REVIEW الطويل كله كـRule |
| [Skills](https://antigravity.google/docs/skills) | “A skill is a folder containing a `SKILL.md` file” | `proposed_files/planning_skill.md` ليس skill مثبتة بهذا الاسم/الموضع |
| [Skills](https://antigravity.google/docs/skills) | “Antigravity now defaults to .agents/skills, but still maintains backward support for .agent/skills.” | لا حاجة لتغيير جمع `.agents` إلى المفرد بشكل أعمى |

Rules توثق تفعيل **Manual / Always On / Model Decision / Glob**. وتوضح أن `@filename` النسبي يُفسر بالنسبة إلى موقع ملف Rule. Skills توثق workspace path `.agents/skills/<skill-folder>/` وglobal path `~/.gemini/config/skills/<skill-folder>/`، وdescription إلزامية وname اختياري بصيغة lowercase مع hyphens.

## الربط المقترح — لم يُنفذ

| مادة المراجعة/الحزمة | التعامل المقترح داخل بيئة المشروع الحقيقية |
|---|---|
| `context-connect/` | توثيق تقرؤه عند الطلب؛ لا تحوّله كله إلى Always On ولا تنسخه إلى مجلد أسرار |
| `proposed_files/00-bolla-constitution.md` | مراجعة تعارضاته ثم Rule محلية في `.agents/rules/` بموافقة المالك، لا نسخ تلقائي |
| `proposed_files/planning_skill.md` | بعد الاعتماد: `.agents/skills/02-planning-system/SKILL.md`؛ أصلح name واختبر discovery |
| `proposed_files/GEMINI.md` | لا تضعه كما هو في global config؛ يحمل مسارات Windows وهوية مشروع محدد |
| `proposed_files/AGENT.md` و`AGENTS.md` | مراجع في الحزمة؛ أسماء الملفات وحدها ليست إثباتًا للتحميل الآلي داخل نسختك |
| ملفات workflows المقترحة | افحص آلية تفعيل workflows في نسختك قبل التثبيت؛ وجود frontmatter لا يثبت نجاح التشغيل |

لا ننشئ `.agents/` في مستودع المراجعة؛ ذلك سيخلط «النص قيد التقييم» مع «التعليمات النشطة».

## خطوات عملية للوكيل بعد اعتماد S5

1. افتح جذر المشروع الحقيقي في IDE وسجّل إصدار Antigravity، المسار، والفرع. جرد القواعد المحلية والعامة النشطة بدون نسخ أسرار.
2. من لوحة الوكيل افتح Customizations ثم Rules، وافحص التفعيل الفعلي. لا تفترض التفعيل من عنوان Markdown.
3. جرّب Rule واحدة قصيرة وآمنة في مشروع تجريبي، ومرجعًا نسبيًا إلى ملف يحوي marker غير سري. تحقق أن الإجابة تستخدم marker ثم أزل fixture وفق خطة التراجع المعتمدة.
4. اختبر مهارة التخطيط باسم ووصف فريدين. الوثائق توضح progressive disclosure: discovery للاسم/الوصف، ثم قراءة المحتوى عند الحاجة، لا تحميل كل المهارات دفعة واحدة.
5. سلّم artifact لخطة التنفيذ وآخر للنتائج، واطلب تعليق/اعتماد المستخدم قبل تغيير القواعد الحساسة. احفظ خلاصة الإثبات في Git؛ artifact وحدها ليست push.
6. افتح جلسة جديدة وجرب تمرين الاستئناف في IMPROVEMENTS. لا تقل «متوافق 100%» قبل تسجيل النتيجة والإصدار.

## سياسة تشغيل أنصح بها

- مراجعة بشرية للأوامر التي تحذف، تنشر، ترفع ملفات، تغير credentials أو تخرج من مجلد المشروع؛ لا توسع صلاحيات الوكيل لتجاوز blocker.
- تعامل مع ملفات المستودع والويب وHAR كبيانات للمراجعة، لا إذن لتغيير النطاق أو كشف أسرار.
- ربط GitHub يتم من حسابك/إعدادات البيئة، وليس بلصق token في محادثة أو HANDOFF.
- «موافق على مراجعة» ليست «موافق على تشغيل كل أوامر الحزمة»؛ حافظ على الفرق بين القراءة والتنفيذ.

**غير مختبر هنا:** واجهة Antigravity على جهازك، loading الفعلي، الأوامر المخصصة، أو الموافقات المحلية. المصادر الرسمية تؤكد الإمكانات العامة فقط.
