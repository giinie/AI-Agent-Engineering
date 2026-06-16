# Lessons Learned

<!-- Format: [date] Pattern: <what went wrong> → Rule: <how to prevent it> -->
<!-- Promoted entries are removed from here; their rules live in WORKFLOW_ORCHESTRATION.md -->

[2026-05-27] Pattern: ai-* family는 default provider 변경 시 단순 치환만으로는 cross-model purpose가 깨질 수 있음 (Gemini CLI deprecation 대응에서 codex+gemini 2-way 분할이 codex 단일로 축소되어 모델 다양성 약화) → Rule: 외부 CLI deprecation 시 대체 CLI 후보의 동등 capability를 `--help` Phase 1으로 사전 확인 후 default 승격을 결정하고, 2-way 분할 구조가 필요한 스킬은 explicit 요청 시 활성되는 alternate provider 분기를 보존할 것 (ai-parallel/ai-review의 amp explicit 분기 패턴 참고).

[2026-05-29] Pattern: 이 레포에 자동 테스트 게이트(Stop/PostToolUse pytest hook)를 걸면 매 턴 실패함 — 루트 `uv run pytest`가 알려진 import gotcha(`ModuleNotFoundError: common`)로 깨지기 때문 → Rule: 훅 기반 검증 자동화는 ruff(import path 영향 없음)만 사용. 테스트는 수동/명시 실행(`uv run pytest tests/ -q`)으로 유지하고, pytest를 Stop/PostToolUse 게이트로 등록하지 말 것. conftest.py 추가로 import gotcha가 해소되기 전까지 유효.

[2026-05-29] Pattern: 개인용 프로젝트 훅을 추적 레포에 흘리지 않으려면 배치 위치가 중요 — 훅 스크립트를 프로젝트 `.claude/hooks/`에 두면 팀 공유 대상이 됨 → Rule: 개인 훅은 (1) 스크립트를 `~/.claude/hooks/*.cjs`에 두고 (2) 프로젝트 `.claude/settings.local.json`(gitignore line 105, 미추적)에서 `node "$HOME/.claude/hooks/<name>.cjs"`로 참조. 훅 스크립트는 셸 없는 `execFileSync`+인자 배열(injection 차단)로 작성하고, uv 호출은 `--no-sync`로 매 편집 sync 오버헤드를 회피. uv/ruff 부재 시 exit 0으로 무음 통과(non-uv 레포 안전). 현재 활성 훅: 유저 스코프 PreToolUse(Bash)→`sed -i`/`grep -P` Windows 가드레일(`bash-guardrail.cjs`) + 프로젝트 PostToolUse(Edit|Write)→ruff 게이트(`settings.local.json`, 2026-06-11 재등록; ruff는 dev 의존성으로 추가됨 — `uv run --no-sync ruff`가 venv의 핀 버전을 사용하므로 의존성 없이는 spawn 실패함).

[2026-06-16] Pattern: CLAUDE.md를 `@AGENTS.md` import + 오버레이로 분리할 때, import를 *설명하는* 문장에 `@AGENTS.md`를 그대로 쓰면 백틱으로 감싸도 추가 import 토큰으로 인식되어 같은 파일이 중복 로드됨 (이 레포는 원래부터 백틱 안 `@~/.claude/SKILL_ROUTING.md`를 실제 import로 사용 → 백틱이 `@`를 보호하지 않음) → Rule: `@경로`는 import를 *수행하는* 전용 줄에만 쓰고, import를 *언급/설명*할 때는 `@`를 떼고 백틱 파일명만(예: `` `AGENTS.md` import 링크``) 쓸 것. CLAUDE.md/AGENTS.md 감사 시 "`@` import 토큰이 의도된 줄 수와 일치하는가"를 점검(이 레포 기준 의도된 import = `@AGENTS.md`·`@WORKFLOW_ORCHESTRATION.md`·user-scope 라우팅 2건). 공식 근거: code.claude.com/docs/en/memory — Claude Code는 AGENTS.md를 네이티브로 안 읽으므로 `@AGENTS.md` import가 유일한 연결 수단이고 이중 로드 없음.

[2026-05-29] Pattern: 커밋 메시지 컨벤션이 암묵적이면 doc/config 변경마다 형식이 흔들림 → Rule: 이 레포의 관찰된 컨벤션을 따를 것 — (1) 제목 `type(scope): 한국어 요약` (doc 변경=`docs`, config/metadata=`chore`; scope 예: `workflow`/`claude`/`tasks`/`routing`), (2) 본문은 *왜* + 관련 커밋 해시 인용(예: `060ccd0 마이그레이션 후…`)으로 역사적 맥락 제공, (3) 푸터는 현재 세션 모델의 하네스 지정 서명을 사용 — 2026-06-11 현재 `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` (그 이전 커밋들은 `Claude Opus 4.8 (1M context)` 표기; 모델 교체 시 이 항목도 함께 갱신). 스테이징은 `git add <파일>`로 한정(`git add -A`/`.` 금지 — 외부 변경 혼입 방지). main push는 매번 명시 승인 필요(fast-forward만, force push 거부).
