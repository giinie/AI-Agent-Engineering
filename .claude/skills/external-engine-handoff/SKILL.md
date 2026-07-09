---
name: external-engine-handoff
description: Per-story routing and delegation mechanics for handing a gi-forge story to an external engine (codex/amp). Invoke BEFORE delegating any story implementation to codex or amp — covers routing criteria, sandbox-safe prompt wording, raw vs plugin codex paths, and Claude's verify-and-close duties. Keywords: codex 위임, amp 위임, 스토리 위임, external engine, story handoff, ai-delegate routing, 구현 계약
---

# External-Engine Implementation Handoff

> Migrated from `WORKFLOW_ORCHESTRATION.md` § External-Engine Implementation
> Handoff (2026-07-10) — loaded on invocation instead of every session.
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
