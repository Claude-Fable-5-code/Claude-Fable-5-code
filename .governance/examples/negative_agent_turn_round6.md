<!-- NEGATIVE FIXTURE (do not fix): the agent's real Round-5 turn as shipped. Must FAIL --source (R37: يشوعها / علشان) and --strict-done (R36: DONE rows with no second-system proof). CI asserts both failures. -->
# Worked example — the human message that triggered Round 5, processed under FULL_READ_PROTOCOL

```req-ledger
SOURCE: https://gist.github.com/pijsal1-tech/9c72… … push-per-chunk لمقاومة الـresets
SENTENCES: 13
REQ-01 [LINK]  "https://gist.github.com/pijsal1-tech/9c728a8267a855a080a200dfc676f800 شوف رابط كمان ده"  → read the gist in full; report contents
REQ-02 [ASK]   "لسه مش كالم برضو عاوز تشوف اصح مناسب ليه"                                            → still not complete; find what is truly right for him
REQ-03 [ASK]   "علشان مفيش حاجه تكرر تاني"                                                              → goal: nothing recurs again → prevention must be mechanical
REQ-04 [Q]     "رايك و تقترحات"                                                                         → give opinion and suggestions
REQ-05 [ASK]   "اعمل ملفات ان الزم عاوز كل حاجه كامله فعلي"                                            → create files if needed; everything complete and real, not advice
REQ-06 [Q]     "عاوز يقدر يشوف كلامي كامل بدون هلوسه و بدون ملخص او تمين ازاي يعمل كده"                → HOW to make the agent see the whole message without hallucination/summary/guessing
REQ-07 [Q]     "او هو يقدر يناسب معاه اي بقي؟؟"                                                         → CAN it even do that?
REQ-08 [RULE]  "رساله صغيره او كبيره يشوعها كلها و يرد عليا كلها حتي لو قسمها لي مهام"                 → any message, all of it, all answered — splitting into tasks is fine
REQ-09 [RULE]  "مش عاوز يغفل عن اي حرف مش كلمه ولا سطر"                                                 → not one character, word, or line may be dropped
REQ-10 [Q]     "بناء ع كلامك و ارشادك ليه هو هل رجعلك كل حاجه ولا ف حجات ناقصه بتقع منه ؟؟؟"           → did the agent return everything from my brief, or are things dropping?
REQ-11 [ASK]   "وامعل ملفات برضو علشان نرفعه ع جيت هاب"                                                 → make files to upload to GitHub
REQ-12 [LINK]  "https://github.com/Claude-Fable-5-code/Claude-Fable-5-code/tree/main"                  → inspect the live repo
REQ-13 [ASK]   "مش عاوزك تسيب حاجه راجع كل حاجه فص فص كل حاجه و كل حاجه تحلص حدث ملفات فورا لحظي"     → review everything piece by piece; update files immediately as each finishes
REQ-14 [RULE]  "علشان جلسه بتوقف ف اي وقت"                                                             → session can stop any time → commit per chunk
REQ-15 [RULE]  "اوعي تنسي ده Sandbox reset مجددًا. أستعيد وأجمّد الخطة فورًا ثم أنفّذ بchunks صغيرة مدفوعة" → on reset: restore, freeze plan first, push-per-chunk
COVERAGE: 15 REQs from 13 sentences — none
```

… (work) …

```req-closure
REQ-01 DONE      gist read in full (51,452 bytes); findings R21–R29 in docs/audit_reports/…/ROUND5_REVIEW.md
REQ-02 DONE      ROUND5_REVIEW §3 root cause; §4 shipped fixes; §6 manual actions
REQ-03 DONE      three-layer prevention: hook v2 + scanner patterns + server-side ruleset (any one alone is insufficient — §3)
REQ-04 ANSWERED  ROUND5_REVIEW §7 (agent suitability; omission not hallucination; tooling good, behaviour escalates when blocked)
REQ-05 DONE      9 files created/changed, all committed on genspark_ai_developer
REQ-06 ANSWERED  FULL_READ_PROTOCOL.md — coverage is enforceable, attention is not; REQ ledger + closure + req_coverage.py
REQ-07 ANSWERED  Yes for coverage (mechanical), no guarantee for quality — protocol §"Known limits"
REQ-08 RULE-KEPT this very ledger/closure pair is the mechanism; copied to AGENT_HARD_RULES Rule 9
REQ-09 RULE-KEPT same as REQ-08; verbatim quotes required, paraphrase is a visible violation
REQ-10 ANSWERED  ROUND5_REVIEW §7: checklist items all applied (nothing dropped); what dropped was what was not on a checklist (credential prohibition was prose)
REQ-11 DONE      branch genspark_ai_developer, 7 commits; push blocked by missing sandbox credentials → patch + bundle exported
REQ-12 DONE      live main=46d524c inspected; 2 direct-to-main commits found (R23); protected=false via API
REQ-13 DONE      each chunk committed immediately (7 commits); handoff written before analysis
REQ-14 RULE-KEPT HANDOFF_ROUND5.md written first; commit after every file
REQ-15 RULE-KEPT sandbox state checked first (no reset this time); plan frozen in HANDOFF_ROUND5.md before work
UNMAPPED: none
```
