# Workflow Orchestration

> Planning, execution, and verification rules for AI-assisted development workflows. Subagent usage, task tracking, bug fixing, and code quality standards.

**Session Start**: If `tasks/lessons.md` exists, read it and apply relevant rules before proceeding.

## Planning
- Enter plan mode for **cross-file changes or architectural decisions** — not every multi-step task
- Write the plan to `tasks/todo.md` with checkable items before implementing
- **Always check official documentation limitations before designing with platform features (Team, Agent, MCP, etc.)** — especially critical for experimental features. Use `context7` MCP for SDK/framework docs (per `~/.claude/MCP_ROUTING.md` §3 Tie-Breaking).
- Check in with the user before starting implementation on non-trivial plans
- If execution goes sideways, STOP and re-plan — do not keep pushing forward
- When the session is in "work without stopping for clarifying questions" mode (set via system reminder or explicit user instruction):
  - Record the assumption inline in the response, then proceed
  - **Irreversible actions still require explicit confirmation**: DB schema migrations, network calls with external side effects, destructive shell commands (`rm -rf`, `git reset --hard`, `git push --force`), production deploys, secret/credential changes

## Recall Before Proposing (Audit / Review Gate)

> Promoted 2026-06-16 after repeated re-raises of already-settled decisions
> (statusLine false-positive ×2, env-deny widening). Auto-memory is advisory
> context, not enforcement — and session start injects only the `MEMORY.md`
> index line, NOT topic-file bodies. The body must be opened deliberately.

For any audit, review, drift-check, or improvement-proposal task on harness /
config / instruction docs:
- **Recall first, scan second.** Before assembling any findings or proposal
  list, open the relevant `feedback_*.md` / `reference_*.md` auto-memory topic
  file(s) for the area under review — not just the `MEMORY.md` index line.
  Then scan disk. Then build proposals.
- **Drop, don't re-raise.** A finding that contradicts a recalled "standing NO"
  / "already at correct shape" decision is dropped — unless new evidence
  overrides the prior call, in which case cite that evidence and state
  explicitly that you are reopening a settled decision.
- Recalled memory reflects what was true when written; if it names a file /
  flag / path, re-verify before acting.

## Subagent Usage

> Overrides user-scope OMC `<delegation_rules>` (aggressive delegation). The mechanism is the user-scope `CLAUDE.md` § Instruction Precedence (Unified), which places project-scope rules at level 2 and OMC defaults at level 4 — so this file wins for delegation policy when active.

- Spawn subagents **only when context isolation is explicitly needed**:
  - Parallel independent analysis (e.g., reviewing multiple modules simultaneously)
  - Research/exploration that would pollute the main context window
  - Adversarial review: one subagent implements, a separate reviewer subagent critiques
- One focused task per subagent — never multiplex unrelated concerns in a single subagent
- Do NOT spawn subagents for simple sequential tasks; keep the main context clean instead
- Prefer 2–3 targeted subagents over large swarms — you cannot effectively observe 10+ agents
- **Targeted search → direct tools first**: For known file paths, specific patterns, or directory exploration, use Glob/Grep/Read directly. Explore subagents are for broad, open-ended codebase questions only.
- **Subagent gate failure**: Explore agents may return empty results due to plugin skill gate conflicts (e.g., a hook printing `SUBAGENT-STOP` or `EXTREMELY-IMPORTANT` markers in place of search results). If an agent returns gate-check output instead of actual results, switch to direct tools immediately — do not retry the same agent. (The original `superpowers` plugin that produced this exact pattern is no longer installed at user scope, but the same anti-pattern can recur with any future gate plugin.)
- **Esc+Esc interrupt vs permission denial**: When a user interrupts a running Agent with Esc double-tap, Claude Code reports `"The user doesn't want to proceed"` — identical to a permission denial. Do not assume a hook or permission system blocked the call. Agent tool calls are auto-approved and do not show approval prompts.

## External-Engine Implementation Handoff

> Validated 2026-06-17 via E2E (gi-forge story → codex implementation → Claude
> verify → done). Mechanics + version facts in auto-memory
> `gi-forge-external-engine-handoff` and `codex-plugin-skill-drift-and-tty-search`.
> codex/amp versions drift fast — re-verify the CLI interface (`{cli} --help`,
> `/codex:setup`) before relying on exact flags.

A gi-forge story file is an **engine-neutral handoff contract**: its embedded
구현 계약 header lets *any* engine (Claude, codex, amp) implement the story from
the file alone. The implementation step is therefore **routable per story** —
Claude decides the route; **verification and deploy always stay in Claude**.

**Routing (Claude decides, per story):**
- **Claude direct** — ambiguity remains, interactive iteration likely, HALT
  conditions likely to fire, or security-sensitive (auth/JWT/refresh/CORS/
  rate-limit → review is MANDATORY per project Skill Policy; do not delegate
  blindly).
- **codex** (`ai-delegate`, or raw `codex exec`) — well-specified mechanical
  story, sandbox safety, cross-model diversity, cost offload.
- **codex parallel** (`ai-parallel`) — one story touches 5+ files with identical
  transforms.
- **amp** (`ai-delegate`, generic `amp -x`) — hard-reasoning story, or after
  codex fails.

**Delegation mechanics (only when routing to an external engine):**
- The delegation prompt MUST scope the constraint to command *execution*, not
  file I/O: *"follow the story's 구현 계약; you MAY read and write project files
  (that is how you implement), but do NOT EXECUTE tests / build-or-sync
  (`uv`/`pip`/`python -m`) / `git` / network — verification is a separate step."*
  A blanket *"do NOT run shell / code edits only"* **mis-fires on codex**: codex
  reads files through its shell tool, so "no shell" blocks it from even reading
  the story file and it returns 0 files (observed v5, 2026-06-18 — the corrected
  wording then worked first try). `--sandbox workspace-write` blocks network, so
  an actually-executed `uv`/`pytest` run **hangs** the engine (~5 min) — that is
  why *execution* is forbidden while reads/writes are explicitly permitted.
- Hand the engine the **story file path**, not a paraphrase — the contract
  travels with the file.
- Raw path (isolated dir / fixture): `codex exec --cd <repo> --sandbox
  workspace-write - < <prompt-file>` (stdin redirect avoids quoting; capture
  stdout with `> <log>`). This sidesteps the `/codex:review` silent-route and
  `codex --search` TTY traps (different subcommand). **Use this — NOT
  `/codex:rescue` — whenever the target is an isolated dir**: `ai-delegate`'s
  Tier-1 codex path (`/codex:rescue`) runs in the **session cwd** and has no
  `--cd` routing, so it cannot aim at a separate dir and would mutate the wrong
  repo (confirmed v5, 2026-06-18).
- Production path (target = session cwd): `Skill("/codex:rescue --wait --fresh
  --write {story path + follow 구현 계약}")`. Never `/codex:review` (unregistered
  → silent route to `code-review:code-review`) or `amp review` (experimental,
  forces `--dangerously-allow-all`).

**Claude owns (regardless of route):**
- Before delegating: capture `baseline_commit` — the sandboxed engine cannot run
  git.
- After the engine returns: run the project test gates; optional cross-model
  review via `ai-review`; flip the story `review → done` and mirror
  `sprint-status.yaml`; commit. **Push requires explicit approval every time**
  (auto-memory `feedback-project-repo-main-push`).
- codex 0.140.0 reliably did the in-file bookkeeping (status transition, sprint
  mirror, Dev Agent Record incl. honest deviation notes) when the prompt named
  the contract — so Claude's role here is **verify-and-close, not redo**.

## Task Execution
- Track progress by marking items complete in `tasks/todo.md` as you go
- Provide a high-level summary of changes at each major step
- Add a review section to `tasks/todo.md` when the task is complete

## Verification
- Never mark a task complete without proving it works
- Run tests, check logs, and demonstrate correctness before reporting done
- When relevant, diff behavior between main branch and your changes
- Before presenting results, run a 3-question self-check:
  1. Tests pass?
  2. Is the WHY of new code clear (annotation in Key Patterns if applicable)?
  3. No Critical Rules violated?

## Bug Fixing
- When given a bug report: just fix it — no hand-holding required for localized fixes.
- If the fix requires cross-file changes or architectural decisions, escalate to Planning first.
- Point at logs, errors, and failing tests, then resolve them autonomously
- Fix failing CI tests without waiting to be told how
- Zero context switching required from the user

## Lessons & Self-Improvement

> **Where to record**: project-specific patterns (this codebase's file paths, repo conventions, gotchas) → `tasks/lessons.md`. Cross-project user/tool feedback (toolchain quirks, OMC behavior, environment) → user-scope auto-memory at `~/.claude/projects/<slug>/memory/`. If a pattern applies beyond this project, prefer auto-memory.

- After a user correction that reveals a **non-obvious or recurring pattern**, append it to `tasks/lessons.md` (project-scope) or save it as a feedback memory (cross-project).
- Format for `tasks/lessons.md`: `[date] Pattern: <what went wrong> → Rule: <how to prevent it>`
- Keep `tasks/lessons.md` concise — prune entries that no longer apply
- Promote rules to this file (WORKFLOW_ORCHESTRATION.md) when violated 3+ times across sessions, OR when a single violation has high blast radius (e.g., security, data loss, irreversible state changes)

## Code Quality

> Inherits `~/.claude/CODE_QUALITY.md` (Simplicity First + Surgical Changes).
> This section adds project-specific deltas only — do not restate user-scope rules.

**Priority** (matches user-scope `~/.claude/CODE_QUALITY.md`, restated for visibility since this drives every project decision): `Correctness > Simplicity > Elegance > Speed`.

- No temporary fixes — find and address root causes
- After a non-trivial change, ask once about **code just written in this session**:
  "Is there a more elegant solution?" — If yes and low-risk, refactor. Else ship.
- Elegance checks do NOT apply to:
  - Simple, obvious fixes (no over-engineering)
  - Pre-existing code (follows the user-scope Surgical Changes rule)
- See also: Bug Fixing
