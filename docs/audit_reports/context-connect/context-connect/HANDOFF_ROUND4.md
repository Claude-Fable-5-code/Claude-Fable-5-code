# HANDOFF — Round 4 (consultant → agent)

**Branch:** `genspark_ai_developer` (3 commits on top of `f9d7d02`)
**Backup:** git bundle on AI Drive `fable_round4_genspark_ai_developer_2026-09-05.bundle`
**Sandbox note:** consultant sandbox has no GitHub credentials — push/PR requires human or agent action (see §Resume).

## Last confirmed state
- `f9d7d02` independently verified: R03 ✅ R09 ✅ R14 ✅ ; R18 ❌ (verify_sync hard-coded paths) ; R16 ❌ (2 new tokens in public gist).
- `.governance/` toolkit written and self-tested: probe 9/9, secret_scan clean, path_scan clean, parity 1/1, pre-commit hook blocked a fake token in negative test.

## Resume (whoever picks this up)
1. `git fetch origin && git checkout genspark_ai_developer` (or `git bundle unbundle` from AI Drive if the branch never reached GitHub).
2. `bash .governance/install_hooks.sh`
3. Push **without touching credentials** — `git push -u origin genspark_ai_developer`. If 401/403 → stop, ask the human to run `gh auth login`.
4. Open PR → main. Wait for `governance-gate` to go green. Only then flip P15 in `proposed_files/PROGRESS.md` to DONE.
5. Copy `.governance/` into the master workspace and add it to `verify_sync` MAPPING.

## Human actions (not automatable)
- Revoke `ghp_7XO63LUK…` and `ghp_Llu676dV…`. Delete/privatise gists.
- Settings → Code security → enable Secret scanning + Push protection.
