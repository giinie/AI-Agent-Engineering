---
paths:
  - "pyproject.toml"
  - "pytest.ini"
  - ".mcp.json"
  - "conftest.py"
  - "src/__init__.py"
  - "src/common/evaluation/ai_judge.py"
  - "tests/evaluation/test_ai_judge.py"
  - "ch07/**"
  - "src/fine_tuning/**"
  - "ch04/mcp_servers/**"
  - "src/common/mcp/**"
  - "src/common/observability/**"
  - "src/frameworks/langgraph_agents/**"
  - "src/common/evaluation/scenarios/**"
  - "notebook/**"
  - "AGENTS.md"
  - "CLAUDE.md"
  - "WORKFLOW_ORCHESTRATION.md"
---

# Doc-sync audit triggers

The directory-membership trigger lives in `CLAUDE.md` instead, because creating a file in a new directory reads nothing that would load this rule.

- Audit `AGENTS.md`'s **Project-Specific Gotchas** after edits to `pyproject.toml`, `pytest.ini`, `.mcp.json`, `conftest.py`, `src/__init__.py`, `src/common/evaluation/ai_judge.py`, or `tests/evaluation/test_ai_judge.py` — those files contain the current-state facts the Gotchas section quotes, and silent drift between them caused commit `060ccd0`'s gotcha staleness. The last two carry the `OPENAI_API_KEY` Gotcha's facts (`AIJudge.__init__` constructing a real `ChatOpenAI`; two cases calling `AIJudge()` without a `DummyLLM`), so injecting a stub there or adding `load_dotenv()` to the module silently falsifies it.
- Audit the path-scoped rules in `.claude/rules/` (fine-tuning, mcp-server-copies, observability) after edits under `ch07/`, `src/fine_tuning/`, `ch04/mcp_servers/`, `src/common/mcp/`, or `src/common/observability/`.
- Audit `AGENTS.md`'s **Architecture** section after any addition under `src/frameworks/langgraph_agents/`, `src/common/evaluation/scenarios/`, `notebook/`, or a new top-level `chNN/` — that section enumerates those directories' membership (7 domain agents, `ch02/`–`ch12/`, `notebook/chNN_*.ipynb`), so a new member silently falsifies it while every file named above stays byte-identical. Name the directories, not the files inside them: a file-only trigger list repeats the enumeration weakness it exists to catch.
- Audit `CLAUDE.md` for the Claude-specific overlay (Skill Policy, Mandatory Reading) and the `AGENTS.md` import link.

## Instruction file boundary (`AGENTS.md` ↔ `CLAUDE.md`)

The split exists so other coding agents (Codex, amp) can read the project core directly. Keep the boundary clean — it is itself an audit surface:

- **Engine-independent facts** (project context, build/test commands, architecture, gotchas, the code-quality priority) → `AGENTS.md` **only**.
- **Claude-specific runtime instructions** (skill routing, hooks, the recall-before-proposing gate, subagent gating, delegation policy) → the `CLAUDE.md` overlay (or `WORKFLOW_ORCHESTRATION.md`) **only**.
- `WORKFLOW_ORCHESTRATION.md` is **shared workflow policy**, not a Claude-only bucket. It holds how-we-work rules (planning, verification, subagent gating, the recall gate, code quality) rather than project facts, and it is written to be readable by whatever agent is running — some passages may name a specific engine or model, and that is a detail of the rule, not a change of ownership. `AGENTS.md` may reference it — that is not a boundary violation.
- When auditing instruction docs, check all four surfaces: (1) `AGENTS.md` content, (2) the `CLAUDE.md` overlay's content, (3) the `AGENTS.md` import link is live, (4) no engine-independent fact has leaked into the overlay and no Claude-specific instruction has leaked into `AGENTS.md`.
