# Hard Implementation — شرح بالمصري

دي الـskill الكاملة لتنفيذ مهام Spec Kit على **Codex وOpenCode**.
بتوجّه الـagent إنه يقرأ المطلوب، يرتّب المهام حسب اعتمادياتها، ينفّذ، يختبر،
يراجع، ويكمّل الشغل المتاح بدل ما يقف لمجرد إنه خلّص مجموعة مهام.

**النص الأصلي كامل: ٢٣٩٧ سطر، بكل أقسامه الـ٤٦، من غير حذف أو اختصار.**
موجود في [ملف الـworkflow](skills/hard-implementation/references/workflow.md).
فيه اختبار ببصمة الملف بيتأكد إنه فضل زي الأصل بالضبط.

## قبل الاستخدام

جهّز الـfeature في Spec Kit بحيث يكون عندك:

- `spec.md`: المطلوب.
- `plan.md`: خطة التنفيذ.
- `tasks.md`: قائمة المهام.

واستخدم Codex أو OpenCode بحسابك وإعداداتك المعتادة.
الـskill مش بتوفّر اشتراك أو موديل، ومش بتغيّر الموديل اللي أنت مختاره.

## التنزيل

افتح الـTerminal جوه فولدر مشروعك. لو عندك [uv](https://docs.astral.sh/uv/getting-started/installation/)، اكتب:

```bash
uv run --no-project https://raw.githubusercontent.com/Mohammed-AliDev/hard-implementation/v1.0.1/install.py
```

الأمر ده بيثبّت دعم الأداتين. لو عايز واحدة بس، زوّد `--agent codex` أو
`--agent opencode` في آخره. التثبيت خاص بالمشروع اللي أنت واقف جواه.

لو معندكش uv وعندك Python 3.10 أو أحدث، نزّل المستودع وشغّل المثبّت:

```bash
git clone --branch v1.0.1 --depth 1 https://github.com/Mohammed-AliDev/hard-implementation.git
python3 hard-implementation/install.py --project /path/to/your/project
```

بدّل `/path/to/your/project` بمسار مشروعك الحقيقي. على Windows ممكن تستخدم
`py -3` بدل `python3`. تقدر تضيف `--dry-run` علشان تشوف اللي هيتثبت قبل الكتابة.

## التشغيل

افتح أداة البرمجة من مشروعك. **الأمر الجاي بيتكتب في شات الأداة، مش الـTerminal.**

في **Codex**:

```text
$hard-implementation specs/001-your-feature
```

في **OpenCode**:

```text
/hard.implement specs/001-your-feature
```

بدّل `specs/001-your-feature` بمسار الـfeature عندك.
لو الأمر أو المهارة مش ظاهرين بعد التثبيت، افتح جلسة جديدة من الأداة.

## لو الشغل اتقطع

اكتب نفس أمر التشغيل ونفس مسار الـfeature تاني. المهارة بتوجّه الـagent إنه
يقرأ آخر تقدم محفوظ، ويطابقه مع الكود والمهام والاختبارات الحالية، وبعدها يكمل.

التقدم بيتسجّل عادة في:

```text
specs/001-your-feature/evidence/implementation-state.md
```

`tasks.md` بيظل قائمة الشغل الأساسية. تسجيل إن مهمة خلصت مش بديل عن التحقق منها.

الـskill بتساعد الـagent يكمّل وهو شغّال، لكن مش بتفتح برنامج اتقفل لوحدها،
ومش بتتجاوز حد الاستخدام أو الصلاحيات. لو فيه عائق حقيقي، المفروض توضّحه
وتسجّل اللي لسه ناقص. الشغل بيكون محلي، والـpush محتاج طلب صريح منك.

## الحفاظ على ملفاتك

المثبّت بيرفض يستبدل ملف مختلف موجود عندك، أو ملف تابع له عدّلته بنفسك.
مش بيغيّر إعدادات Codex أو OpenCode أو ملف `AGENTS.md`.
إعادة نفس أمر التثبيت آمنة في الحالة المعتادة، وبتصلّح الملفات التابعة له لو ناقصة.

لإزالة التثبيت، اكتب أمر التثبيت ومعاه `--uninstall`:

```bash
uv run --no-project https://raw.githubusercontent.com/Mohammed-AliDev/hard-implementation/v1.0.1/install.py --uninstall
```

بيحذف الملفات اللي ثبّتها ولسه متعدّلتش فقط. ملفات المشروع والتقدم المسجّل تفضل موجودة.

## إيه اللي اتضاف للنص الأصلي؟

- تعريف يخلي الأدوات تكتشف الـskill وتحمل النص الكامل.
- أمر `/hard.implement` لـOpenCode.
- تعليمات إضافية لحفظ التقدم والاستئناف.
- أداة تعدّ المهام المفتوحة والمعلّمة كمكتملة؛ العدد وحده مش إثبات نجاح التنفيذ.
- مثبّت واختبارات ودليل استخدام.

راجع [إثبات الحفاظ على النص](docs/PRESERVATION.md) و[نتائج الاختبارات](docs/VALIDATION.md).
للتفاصيل الفنية، فيه [README بالإنجليزي](README.md).
