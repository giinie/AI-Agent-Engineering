# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

The engine-independent project core — Project Context, Common Commands, Environment, Architecture, Project-Specific Gotchas — lives in `AGENTS.md` (imported below) and is shared with other coding agents (Codex, amp). The sections under "## Claude Code" are the Claude-specific overlay; everything engine-independent belongs in `AGENTS.md`, not here.

@AGENTS.md

## Claude Code

### Rules

Workflow orchestration: @WORKFLOW_ORCHESTRATION.md

### Precedence

Rules in `AGENTS.md`, this file, and `WORKFLOW_ORCHESTRATION.md` override user-scope
delegation defaults.

### Skill Policy

Inherits skill routing from `~/.claude/SKILL_ROUTING.md` and MCP catalog from `~/.claude/MCP_ROUTING.md`. Project-specific additions:

- **Security-related changes** (auth / JWT / refresh token rotation / CORS / rate-limit): Review is MANDATORY. Use `security-review` (built-in) for the change scan, or delegate it to a subagent carrying that skill's checklist. For systematic root-cause investigation of a security regression, use `ai-deep` (per `~/.claude/SKILL_ROUTING_DETAIL.md` § Security).
- **New business logic**: The existing integration/unit test suite is solid — write tests first manually; delegate scaffolding only when it is a genuinely independent track. No TDD-specific skill is installed at user scope (see `~/.claude/SKILL_ROUTING_DETAIL.md` § Deprecated / Uninstalled — the `superpowers:test-driven-development` row documents the no-replacement fallback).
- **Code review**: Use `ai-review` (multi-model), or the built-in `/code-review` for a single-pass review of the working diff.
- **Doc sync**: The engine-independent core lives in `AGENTS.md`. When code changes affect build commands, environment variables, the Architecture section, or any Gotcha-quoted fact, run `sync-docs:sync-docs` to update **`AGENTS.md`** (not this file). Adding a member under `src/frameworks/langgraph_agents/`, `src/common/evaluation/scenarios/`, `notebook/`, or a new top-level `chNN/` falsifies `AGENTS.md`'s Architecture enumeration — audit it. The per-file audit triggers and the `AGENTS.md` ↔ `CLAUDE.md` boundary rules load from `.claude/rules/doc-sync.md` when a matching file is read.

### Mandatory Reading

- `WORKFLOW_ORCHESTRATION.md` — auto-loaded via the `### Rules` import.
- `tasks/lessons.md` — read at session start; apply non-obvious project patterns recorded there.
- `tasks/todo.md` — append checkable plan items here for cross-file or architectural changes before implementing.
