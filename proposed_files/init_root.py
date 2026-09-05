#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
"""
init_root.py — إنشاء وفحص مجلد Root/ لأي مشروع وفق دستور بولا v1.2 والنواة الموحدة
الاستخدام:
    python .agents/tools/init_root.py --project "اسم المشروع" --desc "وصف المشروع"
    python .agents/tools/init_root.py --project nexus --desc "Nexus AI Orchestrator"
    python .agents/tools/init_root.py --project nexus --validate
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent


def create_root(project_name: str, description: str, tech_stack: str = "Python"):
    project_path = (WORKSPACE / project_name).resolve()

    # R02: حظر Path Traversal خارج مساحة العمل
    try:
        project_path.relative_to(WORKSPACE)
    except ValueError:
        print(f"❌ خطأ أمني: المسار {project_path} يقع خارج مساحة العمل المعتمدة!")
        sys.exit(1)

    root_path = project_path / "Root"

    if not project_path.exists():
        print(f"❌ المجلد {project_path} مش موجود!")
        sys.exit(1)

    existing_state = {}
    if root_path.exists():
        print(f"⚠️ Root/ موجود بالفعل في {project_name}")
        # R03: الحفاظ على الحالة الحالية إن وجدت
        state_file = root_path / "ai_state.json"
        if state_file.is_file():
            try:
                existing_state = json.loads(state_file.read_text(encoding="utf-8"))
            except Exception:
                existing_state = {}
        answer = input("   هل تريد إعادة التهيئة والحفاظ على الحالة السابقة؟ (y/n): ").strip().lower()
        if answer != "y":
            print("   تم الإلغاء.")
            return False

    root_path.mkdir(parents=True, exist_ok=True)
    now = datetime.now().isoformat(timespec="seconds")

    # ── ai_state.json (مطابقة لعقد AGENTS.md: 8 مفاتيح قياسية في الإنشاء الجديد، والحفاظ الكامل على الحالة عند إعادة التهيئة) ──
    ai_state = {
        "mode": existing_state.get("mode", "[READING]"),
        "current_tag": existing_state.get("current_tag", "[READING]"),
        "turn_count": existing_state.get("turn_count", 0),
        "git_commit": existing_state.get("git_commit", "initial"),
        "last_action": existing_state.get("last_action", f"تم إنشاء وتدشين Root/ لمشروع: {project_name}"),
        "next_action": existing_state.get("next_action", "اقرأ README.md وباشر فحص المتطلبات"),
        "last_message_summary": existing_state.get("last_message_summary", f"تهيئة النواة الموحدة ({tech_stack})"),
        "last_updated": now
    }
    if existing_state:
        for k, v in existing_state.items():
            ai_state[k] = v
        ai_state["last_updated"] = now

    (root_path / "ai_state.json").write_text(
        json.dumps(ai_state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # ── tasks.md ────────────────────────────────────────────────
    if not (root_path / "tasks.md").exists():
        (root_path / "tasks.md").write_text(f"""# 📋 المهام — {project_name}

## ✅ المهام المنجزة
- [x] إنشاء مجلد Root/ وتدشين النواة الموحدة للاستمرارية

## 🔄 المهام الجارية
- [ ] قراءة README.md وفهم المشروع

## 📋 المهام القادمة
<!-- أضف المهام هنا -->
""", encoding="utf-8")

    # ── memory.md ───────────────────────────────────────────────
    if not (root_path / "memory.md").exists():
        (root_path / "memory.md").write_text(f"""# 🧠 الذاكرة الحية — {project_name}

## 📌 الحقائق الأساسية
- **الهدف:** {description}
- **التكنولوجيا:** {tech_stack}

---

## 🔓 اكتشافات مهمة
<!-- أضف هنا الاكتشافات المؤكدة بدليل -->

---

## ❌ محاولات فاشلة (لا تكررها!)
<!-- أضف هنا اللي جربته وفشل -->

---

## 💡 دروس مستفادة
<!-- أضف هنا الدروس المستفادة -->
""", encoding="utf-8")

    # ── PROGRESS.md ─────────────────────────────────────────────
    if not (root_path / "PROGRESS.md").exists():
        (root_path / "PROGRESS.md").write_text(f"""# 📊 سجل التقدم الخطي والمربعات التفاعلية — {project_name}

> **تاريخ الإنشاء:** {now[:10]}  
> **حالة المشروع:** مرحلة التهيئة

## ✅ المنجزات
- [x] إنشاء وتدشين مجلد Root/ والنواة الموحدة للاستمرارية

## ⏳ المهام الحالية
- [ ] فحص المتطلبات وبدء التنفيذ خطوة بخطوة
""", encoding="utf-8")

    # ── keys.txt (خزان أسماء ومراجع المتغيرات فقط — خالي من الأسرار) ──
    if not (root_path / "keys.txt").exists():
        (root_path / "keys.txt").write_text(f"""# 🔑 خزان أسماء ومراجع المتغيرات والمفاتيح البيئية — {project_name}
# (محمي بـ .gitignore وممنوع رفعه للـ Git — تُسجل هنا أسماء ومراجع المتغيرات فقط، وممنوع تخزين أسرار خام)
""", encoding="utf-8")

    # ── ANCHORS.md ──────────────────────────────────────────────
    if not (root_path / "ANCHORS.md").exists():
        (root_path / "ANCHORS.md").write_text(f"""# ⚓ سجل المراسي التشفيرية المحلي — {project_name}

| Anchor ID | Parent | File | Lines | LF SHA-256 | Date | Phase Doc | Status |
|---|---|---|---|---|---|---|---|
""", encoding="utf-8")

    # ── HANDOFF.md ──────────────────────────────────────────────
    if not (root_path / "HANDOFF.md").exists():
        (root_path / "HANDOFF.md").write_text(f"""# 🤝 كوبري التسليم والاستئناف — {project_name}

## 📌 الحالة الراهنة
- **المرحلة:** التهيئة الأولية
- **آخر خطوة:** تدشين مجلد Root/
- **الخطوة القادمة:** فحص متطلبات المشروع وبدء التنفيذ
""", encoding="utf-8")

    # ── AGENTS.md (pointer) ─────────────────────────────────────
    if not (root_path / "AGENTS.md").exists():
        (root_path / "AGENTS.md").write_text(f"""> ⭐ **القواعد الكاملة في:** `.agents/AGENTS.md` — المرجع الموحد
> **اقرأه أول كل session**

---

## 📁 ملفات هذا المشروع (Root/)

| الملف | الوظيفة |
|-------|---------|
| `ai_state.json` | ⭐ البوصلة اللحظية للحالة — بعد كل رسالة (§FATAL RULE #SYNC) |
| `PROGRESS.md` | سجل التقدم الخطي والمربعات التفاعلية [x] عند الـ Milestones |
| `tasks.md` | المهام الحية الخطي والتفاصيل التراكمية عند إغلاق المهام |
| `memory.md` | الذاكرة الفنية — اكتشافات وحلول ودروس مستفادة |
| `keys.txt` | خزان أسماء ومراجع المفاتيح (محمي بـ .gitignore وممنوع رفعه للـ Git) |
| `ANCHORS.md` | سجل المراسي التشفيرية المشفرة بـ SHA-256 |
| `HANDOFF.md` | كوبري التسليم والاستئناف الهندسي عند إغلاق المرحلة |

---

## 📌 معلومات المشروع
- **الاسم:** {project_name}
- **الهدف:** {description}
- **التقنية:** {tech_stack}
""", encoding="utf-8")

    print(f"\n✅ تم إنشاء Root/ لمشروع: {project_name}")
    print(f"   المسار: {root_path}")
    print(f"   الملفات: ai_state.json, PROGRESS.md, tasks.md, memory.md, keys.txt, ANCHORS.md, HANDOFF.md, AGENTS.md")
    return True


def validate_root(project_name: str):
    """تحقق إن Root/ فيه الملفات الأساسية كملفات حقيقية (is_file)"""
    project_path = (WORKSPACE / project_name).resolve()
    try:
        project_path.relative_to(WORKSPACE)
    except ValueError:
        print(f"❌ خطأ أمني: المسار {project_path} يقع خارج مساحة العمل المعتمدة!")
        return False

    root_path = project_path / "Root"
    required = ["ai_state.json", "PROGRESS.md", "tasks.md", "memory.md", "keys.txt", "ANCHORS.md", "HANDOFF.md", "AGENTS.md"]
    
    print(f"\n🔍 فحص Root/ في: {project_name}")
    all_ok = True
    for f in required:
        target = root_path / f
        # R04: التحقق من كون العنصر ملفاً حقيقياً وليس مجلداً
        is_f = target.is_file()
        status = "✅" if is_f else "❌"
        print(f"   {status} {f}")
        if not is_f:
            all_ok = False
    
    if all_ok:
        print("   ✅ كل الملفات الأساسية موجودة وسليمة!")
    else:
        print("   ❌ فيه ملفات ناقصة أو غير صحيحة — شغّل init_root لإنشائها")
    return all_ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="إنشاء Root/ لمشروع جديد وفق دستور بولا v1.2")
    parser.add_argument("--project", required=True, help="اسم مجلد المشروع")
    parser.add_argument("--desc", default="مشروع جديد", help="وصف المشروع")
    parser.add_argument("--tech", default="Python", help="التكنولوجيا المستخدمة")
    parser.add_argument("--validate", action="store_true", help="فحص Root/ فقط بدون إنشاء")
    args = parser.parse_args()

    if args.validate:
        ok = validate_root(args.project)
        if not ok:
            sys.exit(1)
    else:
        success = create_root(args.project, args.desc, args.tech)
        if not success:
            sys.exit(1)
