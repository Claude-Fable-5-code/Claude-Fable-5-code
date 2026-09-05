# Verification — الأدلة وطريقة إعادة الإنتاج

## نتائج الجلسة

النسخة: `a70caf9fcdbdb1bb62a8dc7c1d83af6f7110ddaa`، التاريخ: 2026-09-05.

| الفحص | النتيجة الفعلية | تفسيرها |
|---|---|---|
| Python compile in memory | PASS | صياغة السكربت صحيحة؛ لا يثبت صحة السلوك |
| جرد Git | 20 ملفًا: 19 Markdown + Python واحد | قبل إضافة context-connect |
| active hashes المحلية القابلة للمقارنة | 8/8 MATCH | CRLF→LF ثم SHA-256؛ لا يشمل ملفات الإنتاج الغائبة |
| parent traversal | REPRODUCED | كتب خارج workspace المختار، داخل المختبر المؤقت فقط |
| إعادة التهيئة بتأكيد y | REPRODUCED | استبدلت حالة marker السابقة |
| عقد JSON مقابل AGENTS | MISMATCH | غياب mode, turn_count, git_commit, next_action |
| توليد HANDOFF | NOT CREATED | الأداة لا تنشئ كوبري التسليم |
| مجلدات بدل ملفات | FALSE POSITIVE | validate_root أعادت True |
| CLI لمشروع غير موجود | FALSE SUCCESS EXIT | رسالة نقص، لكن exit code 0 |

هذه **اختبارات توصيف للعيوب الموجودة**: نجاح إعادة إنتاج العيب لا يعني أن السكربت صالح للإنتاج. لم يتم إصلاحه في هذه المهمة.

## إعادة إنتاج السلوك بأمان

شغّل من جذر نسخة المستودع باستخدام Python 3. الاختبار ينشئ بيانات صناعية داخل مجلد مؤقت تحت الجذر ويحذف هذا المجلد فقط عند الخروج. يستخرج الدالتين من AST ويتجاوز initialization الخاص بالـstdout والـWORKSPACE؛ اختبار CLI المنفصل يشغّل `--validate` فقط على fixture غير موجودة. لا يثبت ذلك سلوك كل المنصات أو سلامة كل سيناريو.

```python
import ast
import json
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

base = Path.cwd()
script = base / "proposed_files/init_root.py"
source = script.read_text(encoding="utf-8")
compile(source, str(script), "exec")
functions = ast.Module(
    body=[n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)],
    type_ignores=[],
)
with tempfile.TemporaryDirectory(prefix=".review-probe-", dir=base) as tmp:
    lab = Path(tmp)
    workspace = lab / "workspace"
    workspace.mkdir()
    namespace = {
        "Path": Path, "WORKSPACE": workspace, "json": json,
        "datetime": datetime, "print": lambda *a, **kw: None,
        "input": lambda _: "y",
    }
    exec(compile(functions, "isolated_functions", "exec"), namespace)
    outside = lab / "outside"
    outside.mkdir()
    assert namespace["create_root"]("../outside", "synthetic test")
    state = outside / "Root/ai_state.json"
    assert state.is_file()
    state.write_text('{"marker":"KEEP"}', encoding="utf-8")
    assert namespace["create_root"]("../outside", "overwrite test")
    assert "marker" not in json.loads(state.read_text(encoding="utf-8"))

    project = workspace / "valid"
    project.mkdir()
    assert namespace["create_root"]("valid", "schema test")
    root = project / "Root"
    data = json.loads((root / "ai_state.json").read_text(encoding="utf-8"))
    expected = {"mode", "current_tag", "turn_count", "git_commit",
                "last_action", "next_action", "last_message_summary", "last_updated"}
    assert expected - data.keys() == {"mode", "turn_count", "git_commit", "next_action"}
    assert not (root / "HANDOFF.md").exists()
    assert not (project / "HANDOFF.md").exists()
    for file in root.iterdir():
        file.unlink()
        file.mkdir()
    assert namespace["validate_root"]("valid") is True
    result = subprocess.run(
        [sys.executable, str(script), "--project", str(lab / "missing"), "--validate"],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )
    assert result.returncode == 0 and "ناقصة" in result.stdout
print("REPRODUCED: traversal, overwrite, schema mismatch, missing handoff, false validation, exit 0")
```

بعد إصلاح السكربت يجب أن تتغير هذه assertions لتثبت **رفض** الحالات الخاطئة؛ هذه ليست regression suite جاهزة للإصلاح المستقبلي.

## إعادة حساب المراسي

المقارنة تربط مسارات البيئة الأصلية بنسخ `proposed_files` صراحة، ولا تفترض أن أي ملف متشابه الاسم يطابق أصلًا إنتاجيًا.

```python
import hashlib
from pathlib import Path

base = Path.cwd() / "proposed_files"
mapping = {
    "bolla_constitution_v1_2_ironclad": "00-bolla-constitution.md",
    "gemini_v1_2": "GEMINI.md",
    "workflow_sequential_v2": "00-sequential-requests.md",
    "agents_v2_6_planning_v2": "AGENTS.md",
    "workflow_planning_v2": "00-planning.md",
    "skill_planning_system_clean": "planning_skill.md",
    "workflow_speckit_v2": "00-speckit.md",
    "agent_md_unified_v2": "AGENT.md",
}
seen = set()
for row in (base / "Root_ANCHORS.md").read_text(encoding="utf-8").splitlines():
    if "**Active Sealed**" not in row:
        continue
    cells = [value.strip().strip("`") for value in row.strip("|").split("|")]
    if cells[0] not in mapping:
        continue
    raw = (base / mapping[cells[0]]).read_bytes().replace(b"\r\n", b"\n")
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == cells[4], (cells[0], digest, cells[4])
    print(cells[0], "MATCH", "actual lines", len(raw.splitlines()), "recorded", cells[3])
    seen.add(cells[0])
assert seen == set(mapping)
```

أعداد السطور المختلفة: GEMINI `113/114`، AGENTS `305/307`، planning `146/185` (فعلي/مسجل). Hashes متطابقة للثمانية، وهذه ملاحظة metadata فقط.

## بوابة الحزمة الجديدة

- فحص Markdown النسبي وUTF-8 وcode fences، و`git diff --check`.
- تشغيل كتل Python أعلاه من المستند نفسه للتأكد من صلاحية إعادة الإنتاج.
- مقارنة baseline: التغييرات يجب أن تكون إضافات داخل `context-connect/` فقط؛ لا تعديل للملفات الأصلية.
- فحص remote push وPR منفصل عن نجاح الفحوص المحلية. وضع النشر مسجل في HANDOFF، ولا تعتبر اختبارًا ناجحًا دليلًا على الرفع.

لا توجد هنا نتائج تشغيل لتطبيق FastAPI/Telegram أو IDE. لم يتم تنفيذ اختبار crash حقيقي ولا full secret scan.
