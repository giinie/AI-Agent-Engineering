# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

The engine-independent project core — Project Context, Common Commands, Environment, Architecture, Project-Specific Gotchas — lives in `AGENTS.md` (imported below) and is shared with other coding agents (Codex, amp). The sections under "## Claude Code" are the Claude/OMC-specific overlay; everything engine-independent belongs in `AGENTS.md`, not here.

@AGENTS.md

## Claude Code

### Rules

Workflow orchestration: @WORKFLOW_ORCHESTRATION.md

### Precedence

Rules in `AGENTS.md`, this file, and `WORKFLOW_ORCHESTRATION.md` override user-scope
delegation defaults (including OMC delegation_rules).

### Skill Policy

Inherits skill routing from `~/.claude/SKILL_ROUTING.md` and MCP catalog from `~/.claude/MCP_ROUTING.md`. Project-specific additions:

- **Security-related changes** (auth / JWT / refresh token rotation / CORS / rate-limit): Review is MANDATORY. Use `security-review` (built-in) for the change scan, or delegate to the `oh-my-claudecode:security-reviewer` agent. For systematic root-cause investigation of a security regression, use `oh-my-claudecode:debug` (per `~/.claude/SKILL_ROUTING_DETAIL.md` § Security).
- **New business logic**: The existing integration/unit test suite is solid — write tests first manually, optionally delegating scaffolding to the `oh-my-claudecode:executor` agent. No TDD-specific skill is installed at user scope (see `~/.claude/SKILL_ROUTING_DETAIL.md` § Deprecated / Uninstalled — the `superpowers:test-driven-development` row documents the no-replacement fallback).
- **Code review**: Use `ai-review` (multi-model). For delegated review tasks, prefer the `oh-my-claudecode:code-reviewer` agent.
- **Doc sync**: The engine-independent core now lives in `AGENTS.md`. When code changes affect API endpoints, environment variables, the Architecture section, or any "WHY" annotation, run `sync-docs:sync-docs` to update **`AGENTS.md`** (not this file). Audit `AGENTS.md`'s **Project-Specific Gotchas** after edits to `pyproject.toml`, `pytest.ini`, `.mcp.json`, `conftest.py`, or `src/__init__.py` — those files contain the current-state facts the Gotchas section quotes, and silent drift between them caused commit `060ccd0`'s gotcha staleness. Audit **this `CLAUDE.md`** for the Claude/OMC overlay (Skill Policy, Mandatory Reading) and the `AGENTS.md` import link. Also audit the path-scoped rules in `.claude/rules/` (fine-tuning, mcp-server-copies, observability) after edits under `ch07/`, `src/fine_tuning/`, `ch04/mcp_servers/`, `src/common/mcp/`, or `src/common/observability/`.

### Instruction File Boundary (`AGENTS.md` ↔ `CLAUDE.md`)

The split exists so other coding agents (Codex, amp) can read the project core directly. Keep the boundary clean — it is itself an audit surface:

- **Engine-independent facts** (project context, build/test commands, architecture, gotchas, the code-quality priority) → `AGENTS.md` **only**.
- **Claude/OMC runtime instructions** (skill routing, hooks, the recall-before-proposing gate, subagent gating, delegation policy) → this `CLAUDE.md` overlay (or `WORKFLOW_ORCHESTRATION.md`) **only**.
- When auditing instruction docs, check all four surfaces: (1) `AGENTS.md` content, (2) this overlay's content, (3) the `AGENTS.md` import link is live, (4) no engine-independent fact has leaked into the overlay and no Claude/OMC instruction has leaked into `AGENTS.md`.

### Mandatory Reading

- `WORKFLOW_ORCHESTRATION.md` — auto-loaded via the `### Rules` import. Key items the agent must honor: subagent gating (spawn only for context isolation), the recall-before-proposing gate for audit/review tasks (open the area's `feedback_*`/`reference_*` auto-memory body before building findings), verification before completion, and the project-scope code-quality priority (see `AGENTS.md` § Code Quality).
- `tasks/lessons.md` — read at session start; apply non-obvious project patterns recorded there.
- `tasks/todo.md` — append checkable plan items here for cross-file or architectural changes before implementing.
