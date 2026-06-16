# Todo

## AGENTS.md 분리 — 크로스엔진 구현 핸드오프 기반 (2026-06-16)

**배경**: gi-forge story 산출물을 Codex/amp에 구현 핸드오프하고 Claude로 검증/배포하는 워크플로우를 위해, 구현 엔진이 못 읽는 프로젝트 핵심 컨텍스트(commands/gotchas/architecture)를 엔진 독립 `AGENTS.md`로 분리. 공식 문서(code.claude.com/docs/en/memory § AGENTS.md) 확인: **Claude Code는 AGENTS.md를 네이티브로 안 읽음 → `@AGENTS.md` import가 정답**(이중 로드 없음). Windows는 symlink 대신 import 사용(문서 명시).

**구조 (사용자 확정)**: AGENTS.md = 엔진 독립 정본 코어 / CLAUDE.md = `@AGENTS.md` + Claude·OMC 오버레이. 복사 ❌ import ⭕ (repo 내 중복 0).

### Checklist

- [x] `AGENTS.md` 신규 생성 — Project Context / Common Commands / Environment / Architecture / Project-Specific Gotchas / Code Quality(짧은 echo) / References 이동 (133줄)
- [x] `CLAUDE.md` 재작성 — `@AGENTS.md` import + "## Claude Code" 오버레이(Rules/Precedence/Skill Policy/Mandatory Reading)만 잔류 (41줄)
- [x] doc-sync/감사 타깃 **확장**(재지정 아님): Architecture·Gotchas 콘텐츠 규칙 → AGENTS.md, 오버레이 → CLAUDE.md, **둘 다 감사 집합 유지** (Skill Policy Doc sync 불릿 재작성)
- [x] 신설 감사 차원: `### Instruction File Boundary` 섹션 추가 — import 링크 생존 + 분할 경계 정합 4표면 명문화

### 감사 4표면 (분할이 만든 것)
1. AGENTS.md 콘텐츠  2. CLAUDE.md 오버레이 콘텐츠  3. `@AGENTS.md` import 배선  4. 분할 경계 정합

### Verification

- [x] 3-question self-check (tests N/A — 문서 변경, 실행 코드 무변경; WHY는 AGENTS.md 헤더+Boundary 섹션에 명시; Surgical — 콘텐츠 verbatim 이동, 신규 추가는 Code Quality echo 4줄 + Boundary 섹션뿐)
- [x] CLAUDE.md에 엔진 독립 콘텐츠 잔류 0 확인 (grep: uv sync/Chapter map/Python 3.12 등 본문 매치 없음, line 27 매치는 감사 *규칙*의 트리거 언급)
- [x] `@` import 토큰 = 의도된 3줄만(7 `@AGENTS.md`, 13 `@WORKFLOW_ORCHESTRATION.md`, 22 user-scope ×2). prose 내 `@AGENTS.md`·`@WORKFLOW_ORCHESTRATION.md` 3건은 `@` 제거(재import 방지 — 신설 감사차원 ③이 첫 적용에서 자체 검출)
- [x] 각 파일 200줄 soft target 준수 (41 / 133)

### Review

**변경 요약**: gi-forge story → Codex/amp 구현 핸드오프 → Claude 검증 워크플로우의 기반으로, 프로젝트 핵심 컨텍스트를 엔진 독립 `AGENTS.md`로 분리. `CLAUDE.md`는 `@AGENTS.md` import + Claude/OMC 오버레이로 축소(148→41줄). 공식 문서가 권장하는 정확한 패턴(Claude는 AGENTS.md 미독 → `@import`).

**drift 방지**: repo 내 공유 코어 단일본(중복 0). doc-sync/감사 규칙을 **확장**(AGENTS.md 추가 + CLAUDE.md 유지, 둘 다)하고, 분할이 만든 새 감사 차원(import 링크·경계 정합) 4표면을 `### Instruction File Boundary`에 명문화.

**미커밋**: 사용자 명시 승인 시 커밋 (CLAUDE.md commit protocol). 커밋 분리 권장: `docs(claude)` 1건(CLAUDE.md+AGENTS.md+todo).

**후속(미적용, 사용자 선택)**: (1) gi-forge `templates/story.md`에 "외부 구현 엔진 핸드오프" 섹션(uv 실행/테스트 명령 + bounce 계약), (2) 워크플로우 절차 문서화, (3) user-scope `audit-instruction-docs` 스킬 감사 집합에 AGENTS.md 인지 추가.

---

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

---

## 메모리 recall 재발 방지 — 워크플로 게이트 + 인덱스 밀도 (2026-06-16)

**배경**: 감사/제안 작업에서 이미 걸러진 결정(statusLine 오탐 ×2, env-deny 확대)을 반복 재제기. 측정 결과 메모리 구성 자체는 양호(3계층 ~7KB, 글자 중복 ≈0); 실패 원인은 메커니즘에 있음 — (A) 세션 시작에 MEMORY.md *인덱스 한 줄*만 주입되고 토픽 파일 본문은 미로드, (B) 메모리는 advisory context라 강제력 없음. 공식 문서 처방: 강제는 훅, 하지만 비용 대비 효과로 워크플로 게이트(2) + 인덱스 밀도(3) 채택(사용자 확정).

### Checklist

- [x] **#2 WORKFLOW_ORCHESTRATION.md** — `## Recall Before Proposing (Audit / Review Gate)` 신규 섹션 추가 (Planning 직후, line 17). "recall first, scan second" + "drop, don't re-raise" + 재검증 규칙
- [x] **#3 MEMORY.md** — `**[STANDING NO]**` 마커 컨벤션 도입: (a) 상단 legend 1줄(탈출구 포함 + 게이트 cross-ref), (b) 재제기된 3개 항목에 마커 prepend — routing slim floor / statusLine / .env deny glob overbroad
- [x] **드리프트 정합** — `feedback_audit_recall_before_proposing.md` 본문 + MEMORY.md 인덱스 줄에 "WORKFLOW § Recall Before Proposing로 승격(2026-06-16)" 양방향 cross-ref 추가 (user CLAUDE.md 정합 규칙: level 2 갱신 시 level 5 메모리 reconcile)

### Verification

- [x] 3-question self-check (tests N/A — doc 변경; WHY는 섹션 인용문에 명시; Surgical Changes 준수)
- [x] MEMORY.md 줄 수 = 17 (≤ 200 예산) ✅
- [x] `[STANDING NO]` 4건 확인(legend 1 + 마커 3), WORKFLOW 섹션 line 17 존재 ✅
- [x] git diff: 프로젝트 레포 2파일(WORKFLOW +20, todo). 메모리 2파일은 auto-memory(미추적)라 git 대상 아님 — 의도된 동작 ✅

### Scope 결정사항

- 게이트는 **프로젝트 스코프**(WORKFLOW_ORCHESTRATION.md) — 사용자가 옵션 2에서 명시 선택
- 마커 대상은 **실제 재제기된 settled-decision 메모리 3개로 한정** (over-engineering 회피); 프로세스 규칙인 audit-recall 메모리는 마커 대상 아님(cross-ref만)
- 커밋: `docs(workflow)` + `docs(memory)` 분리 가능, push는 명시 승인 후
