# Todo

## ai-* 패밀리에서 Gemini CLI 제거 (2026-05-27)

**배경**: Google이 2026-06-18에 Gemini CLI를 free/AI Pro/AI Ultra에서 서비스 중단. 대체재 Antigravity CLI는 headless 모드가 부족하여 ai-* 스킬 사용에 부적합. 사용자 결정에 따라 즉시 완전 제거.

**정책 (사용자 확정)**:
- 옵션 A: 즉시 완전 제거 (3주 잔여 capability 포기)
- 옵션 A1: ai-research default를 codex로 승격 (`codex --search` 플래그로 web search 활성)
- ai-parallel / ai-review: default를 codex 단일로, amp는 explicit 요청 시 codex+amp 2/3-way
- `CLI Exclusivity Rule` 유지 (MCP search tool 대체 금지 그대로)
- `security.md`의 `GEMINI_API_KEY` redaction 패턴은 보존 (기존 키 누출 위험 무관)

### Checklist

- [x] `~/.claude/skills/ai-delegate/SKILL.md` — provider/fallback/Examples 정리, Execution Context의 CLI 목록 codex/amp만 유지
- [x] `~/.claude/skills/ai-deep/SKILL.md` — Level 2를 codex 단일로, Provider Selection Guide·routing heuristics·fallback chain 정리
- [x] `~/.claude/skills/ai-parallel/SKILL.md` — codex 단일 default + amp explicit 시 2-way 분기로 Step 4·File Count·Provider Strategy·Partial Failure 재구성, Report 테이블도 갱신
- [x] `~/.claude/skills/ai-review/SKILL.md` — Claude+codex 2-perspective default + amp explicit 시 3-way 분기, Comparative Report 2-col/3-col 분기 명시
- [x] `~/.claude/skills/ai-research/SKILL.md` (영향 최대) — default provider codex (`--search` 활성), Search Type Routing·Step 4 본문에 plugin 경로/raw CLI 경로(`codex --search`) 명시
- [x] `~/.claude/skills/ai-delegate/references/conventions.md` — fallback chain 예시 및 default provider 주석 갱신, CLI Exclusivity Rule 단락의 provider 목록 codex/amp로 축소
- [x] `~/.claude/skills/ai-delegate/references/security.md` (no-op) — `GEMINI_API_KEY=` redaction 패턴 보존 (deprecation과 누출 위험 무관)

### Verification

- [x] `grep -rn -i "gemini" ~/.claude/skills/ai-*` → security.md line 30의 `GEMINI_API_KEY` 패턴 1줄만 남음 확인 ✅
- [x] `codex --help | grep -A1 "\-\-search"` → "Enable live web search. When enabled, the native Responses `web_search` tool is available" 확인 ✅
- [x] WORKFLOW_ORCHESTRATION.md "3-question self-check"
  - Tests: N/A (스킬 문서 변경, 실행 가능 코드 변경 없음)
  - WHY 명시: ai-research SKILL.md에 "This default was chosen after `codex --help` Phase 1 verified the `--search` flag exposes the Responses `web_search` tool" 주석 추가 ✅
  - Critical Rules: Surgical Changes 준수, CLI Exclusivity Rule 위반 없음 ✅
- [x] `git diff --stat`: 6개 파일, 168 insertions / 135 deletions — surgical 적용 규모 일치 ✅

### Lessons

- 추가됨: `tasks/lessons.md`에 [2026-05-27] 항목 — "외부 CLI deprecation 시 대체 CLI의 동등 capability를 `--help` Phase 1으로 사전 확인 + 2-way 분할 스킬은 explicit alternate provider 분기 보존"

### Review

**변경 요약**: Google Gemini CLI deprecation (2026-06-18 서비스 중단) 대응으로 사용자 결정에 따라 ai-* 패밀리 5개 스킬과 conventions.md에서 gemini 의존성 완전 제거. ai-research default를 codex(`--search` 활성)로 승격하고, ai-parallel/ai-review는 codex 단일 default + amp explicit 시 2-way/3-way 분기 구조로 재설계.

**보존 항목**: (1) security.md의 `GEMINI_API_KEY` redaction 패턴 — 기존 키 누출 위험은 deprecation과 무관. (2) CLI Exclusivity Rule — MCP search tool 대체 금지 정책 유지.

**Out of Scope (별도 후속 작업)**: SKILL_ROUTING.md/MCP_ROUTING.md/CLAUDE.md 등 사용자-/프로젝트-범위 라우팅 문서의 cross-reference audit (`audit-instruction-docs` 스킬 사용 권장), Antigravity CLI 통합 실험 (현재 headless 모드 부족), amp 사용량 모니터링 정책.

**Follow-up 권장**: (1) 다음 세션에서 `/audit-instruction-docs` 실행해서 user-scope 라우팅 문서들이 새 ai-* description과 일치하는지 점검. (2) 2026-06-18 이후 Antigravity CLI headless 모드 개선이 확인되면 ai-* 패밀리에 alternate provider로 재합류 검토 가능.
