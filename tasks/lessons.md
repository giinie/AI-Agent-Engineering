# Lessons Learned

<!-- Format: [date] Pattern: <what went wrong> → Rule: <how to prevent it> -->
<!-- Promoted entries are removed from here; their rules live in WORKFLOW_ORCHESTRATION.md -->

[2026-05-27] Pattern: ai-* family는 default provider 변경 시 단순 치환만으로는 cross-model purpose가 깨질 수 있음 (Gemini CLI deprecation 대응에서 codex+gemini 2-way 분할이 codex 단일로 축소되어 모델 다양성 약화) → Rule: 외부 CLI deprecation 시 대체 CLI 후보의 동등 capability를 `--help` Phase 1으로 사전 확인 후 default 승격을 결정하고, 2-way 분할 구조가 필요한 스킬은 explicit 요청 시 활성되는 alternate provider 분기를 보존할 것 (ai-parallel/ai-review의 amp explicit 분기 패턴 참고).
