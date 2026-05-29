# Lessons Learned

<!-- Format: [date] Pattern: <what went wrong> → Rule: <how to prevent it> -->
<!-- Promoted entries are removed from here; their rules live in WORKFLOW_ORCHESTRATION.md -->

[2026-05-27] Pattern: ai-* family는 default provider 변경 시 단순 치환만으로는 cross-model purpose가 깨질 수 있음 (Gemini CLI deprecation 대응에서 codex+gemini 2-way 분할이 codex 단일로 축소되어 모델 다양성 약화) → Rule: 외부 CLI deprecation 시 대체 CLI 후보의 동등 capability를 `--help` Phase 1으로 사전 확인 후 default 승격을 결정하고, 2-way 분할 구조가 필요한 스킬은 explicit 요청 시 활성되는 alternate provider 분기를 보존할 것 (ai-parallel/ai-review의 amp explicit 분기 패턴 참고).

[2026-05-29] Pattern: 이 레포에 자동 테스트 게이트(Stop/PostToolUse pytest hook)를 걸면 매 턴 실패함 — 루트 `uv run pytest`가 알려진 import gotcha(`ModuleNotFoundError: common`)로 깨지기 때문 → Rule: 훅 기반 검증 자동화는 ruff(import path 영향 없음)만 사용. 테스트는 수동/명시 실행(`uv run pytest tests/ -q`)으로 유지하고, pytest를 Stop/PostToolUse 게이트로 등록하지 말 것. conftest.py 추가로 import gotcha가 해소되기 전까지 유효.

[2026-05-29] Pattern: 개인용 프로젝트 훅을 추적 레포에 흘리지 않으려면 배치 위치가 중요 — 훅 스크립트를 프로젝트 `.claude/hooks/`에 두면 팀 공유 대상이 됨 → Rule: 개인 훅은 (1) 스크립트를 `~/.claude/hooks/*.cjs`에 두고 (2) 프로젝트 `.claude/settings.local.json`(gitignore line 105, 미추적)에서 `node "$HOME/.claude/hooks/<name>.cjs"`로 참조. 훅 스크립트는 셸 없는 `execFileSync`+인자 배열(injection 차단)로 작성하고, uv 호출은 `--no-sync`로 매 편집 sync 오버헤드를 회피. uv/ruff 부재 시 exit 0으로 무음 통과(non-uv 레포 안전). 현재 활성 훅: PostToolUse(Edit|Write)→ruff 게이트(settings.local.json), 유저 스코프 PreToolUse(Bash)→`sed -i`/`grep -P` Windows 가드레일.
