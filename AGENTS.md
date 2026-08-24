# AGENTS.md

Engine-independent project core for **"AI 에이전트 엔지니어링"** (Building Applications with AI Agents, 한빛미디어) — the Korean edition example code.

This file is the **canonical home** for the facts every coding agent needs (project context, build/test commands, architecture, gotchas). Claude Code reads it via the `AGENTS.md` import in `CLAUDE.md`; Codex (project `AGENTS.md` / `~/.codex/AGENTS.md`) and other agents (e.g. amp) read it directly. **Claude/OMC-specific runtime instructions** (skill routing, hooks, the recall gate, delegation policy) live in `CLAUDE.md`'s "## Claude Code" overlay, **not here** — keep that boundary clean.

## Project Context

Korean translation of the example code for **"AI 에이전트 엔지니어링"** (Building Applications with AI Agents, 한빛미디어). The Korean edition has been reorganized by book chapter (`ch02/`–`ch12/`) and updated for **Python 3.12 + LangChain 1.0**, while the original English framework-style source remains under `src/`. Both layouts coexist; some examples have parallel implementations in both (e.g., MCP servers, customer support agent).

## Common Commands

The project uses **uv** (Astral) exclusively. Do not invoke `pip`, `poetry`, or `pipenv`.

```bash
# Install / sync dependencies (creates .venv, reads uv.lock)
uv sync

# Run any script — uv handles venv activation
uv run python ch02/simple_customer_support_agent.py

# Run the full test suite (the tests/ path is required from the repo root — see Project-Specific Gotchas).
# Expect 2 skips: the optional fine-tuning extra is absent, and one agent test is gated on the LangChain 1.0 migration.
uv run pytest tests/ -q

# Optional: install fine-tuning extras (heavy: torch, transformers, peft, trl, bitsandbytes, datasets)
uv sync --extra fine-tuning

# Run batch evaluation (entry point referenced from project.md)
# NOTE: currently fails at import until the LangChain 1.0 migration lands (see Project-Specific Gotchas)
# (scenario filenames vary by domain — list them with `ls src/common/evaluation/scenarios/`)
uv run python -m src.common.evaluation.batch_evaluation \
  --dataset src/common/evaluation/scenarios/<scenario>.jsonl \
  --graph_py src/frameworks/langgraph_agents/<domain>/<agent>.py

# Start the local observability stack (Loki + Tempo + Promtail)
cd src/common/observability && docker-compose up -d
```

### Environment

- Python is **pinned to 3.12** (`>=3.12,<3.13` in `pyproject.toml`; venv runs CPython 3.12.11). Do not assume 3.13+ syntax/stdlib.
- `.env` is required at the repo root with `OPENAI_API_KEY` (template: `.env.example`). Some examples additionally need `WOLFRAM_ALPHA_APP_ID`, `YOUR_SLACK_BOT_TOKEN`, or `TRACELOOP_API_KEY`. The `LANGCHAIN_*` block in `.env.example` is optional LangSmith tracing, off by default (`LANGCHAIN_TRACING_V2=false`) and read by no example — `langsmith` is only a transitive dependency.
- WSL is recommended on Windows because some dependencies don't work on native Win32.

## Architecture — Big Picture

### Two parallel code layouts

```
ch02/ … ch12/   ← Korean edition: standalone, chapter-by-chapter scripts
                  Run directly: `python chXX/file.py`
                  Self-contained per chapter (chapters do NOT import from each other)

src/            ← Original English framework: package-style, cross-cutting modules
                  Entry points expect `src.` prefix (see "Test import gotcha" below)
```

The two layouts overlap intentionally for pedagogical reasons. When asked to modify "the customer support agent", clarify which copy: `ch02/simple_customer_support_agent.py` (Korean book), `ch09/agents/customer_support_agent.py` (evaluation harness), or `src/frameworks/langgraph_agents/ecommerce_customer_support/customer_support_agent.py` (original framework).

### `src/` module structure (cross-cutting concerns)

- `src/frameworks/langgraph_agents/<domain>/` — **7 production-style domain agents** (ecommerce, financial_services, healthcare, it_helpdesk, legal, soc, supply_chain). Each domain pairs an agent file with a JSONL evaluation set under `src/common/evaluation/scenarios/`.
- `src/fine_tuning/` — SFT, DPO, RLVR scripts. Training data in `training_data/*.jsonl`. Output checkpoints land under `ch07/fine_tuned_model/` (gitignored).

`notebook/chNN_*.ipynb` (ch02–ch12) — Colab-friendly versions (Traceloop/Loki removed; ch03 won't run in Colab; ch08 distributed variants need extra infra).

## Project-Specific Gotchas

> Path-scoped gotchas (fine-tuning, MCP server copies, observability) live in `.claude/rules/`. Claude Code auto-loads them when reading files under their target paths (`ch07/**`, `src/fine_tuning/**`, `ch04/mcp_servers/**`, `src/common/mcp/**`, `src/common/observability/**`); other engines should read those rule files manually when working under those paths. The entries below are command/build-level (triggered by intent, not file reads) and stay eager here.

### Test import path: bare `common.*` imports resolved via root `conftest.py`
Tests import the cross-cutting modules with the bare `from common.evaluation.ai_judge import AIJudge` style, but those packages live under `src/`, which hatchling installs as `src.common.*` (`packages = ["src"]`) — so `common` is not importable from a headless `uv run pytest`. The repo-root `conftest.py` does `sys.path.insert(0, str(Path(__file__).parent / "src"))` so the bare imports resolve.
- Before this `conftest.py` existed, `uv run pytest` failed with `ModuleNotFoundError: No module named 'common'`; the import style only worked via IDE source-root injection (`.idea/` config + JetBrains MCP bridge in `.mcp.json`).
- Keep the bare `from common...` imports as-is — the root `conftest.py` is the chosen fix; do **not** rewrite them to `from src.common...`.

### `pytest.ini` overrides `pyproject.toml` test config
The repo has BOTH `pytest.ini` (only `filterwarnings`) and `[tool.pytest.ini_options]` in `pyproject.toml` (with `testpaths = ["tests"]`, etc.). When `pytest.ini` exists, pytest **ignores** the pyproject.toml block entirely. Consequence: `uv run pytest` collects every `test_*.py` in the repo, including `ch07/test_dpo_model.py` / `ch07/test_sft_model.py` (which import `peft` from the optional `fine-tuning` extras and fail with `ModuleNotFoundError: No module named 'peft'` by default; `ch07/test_rlvr_model.py` imports only torch/transformers, present as transitive deps, so it collects fine).
- Workaround for normal runs: `uv run pytest tests/ -q` (explicit path) or merge the pyproject `[tool.pytest.ini_options]` keys into `pytest.ini`.
- Don't "fix" by deleting `pytest.ini` — its `filterwarnings` setting is intentional.

### Duplicate dev dependency declarations
`pyproject.toml` declares dev dependencies in **both** `[project.optional-dependencies] dev` (PEP 631, for `pip install -e .[dev]` callers) and `[dependency-groups] dev` (PEP 735, uv-canonical). Content is identical and must be kept in sync manually when adding/removing dev tools — `uv add --dev <pkg>` only updates the `[dependency-groups]` block. Migration from the legacy `[tool.uv].dev-dependencies` form was completed in commit `060ccd0`; don't reintroduce that section.

### `src/__init__.py` exists
`src/` is a Python package, not a source root. The bare-`common` import style works headlessly because the repo-root `conftest.py` puts `src/` on `sys.path` (see "Test import path" above); IDEs additionally inject it via `.idea/` source roots.

### `.mcp.json` registers a JetBrains SSE bridge
The local `.mcp.json` points at the JetBrains IDE plugin's local SSE endpoint (`http://127.0.0.1:<dynamic-port>/sse`). The port is assigned by the JetBrains plugin at IDE startup and changes between sessions — do **not** treat the exact port as a current-state fact. Verify with `cat .mcp.json` if the value matters. The file is gitignored (`.mcp.json` in `.gitignore`) and **not tracked** — `git ls-files .mcp.json` returns nothing; the JetBrains plugin recreates it on demand. Don't add secrets here; use `.mcp.json.example` for templates.

### LangChain 1.0 migration is incomplete (`langchain.schema` removed)
13 source files under `src/frameworks/langgraph_agents/` (plus `src/common/evaluation/batch_evaluation.py` — 14 total) still `from langchain.schema import ...`, a module **removed in LangChain 1.0**. With langchain pinned `>=1.1.0` (`pyproject.toml`), those modules fail to import (`ModuleNotFoundError: No module named 'langchain.schema'`) — the affected agents are currently non-importable. The replacement is `from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage` (verified present in the installed `langchain_core`).
- Enumerate every site: `grep -rn "langchain.schema" --include="*.py" src/`.
- `tests/frameworks/langgraph_agents/test_langgraph_customer_support_agent.py` is `pytest.skip(allow_module_level=True)`-guarded pending this migration; drop the skip once `customer_support_agent.py` is migrated.
- The edit is mechanical, but each file also carries pre-existing lint debt (in 12 of the 14, a misplaced `from __future__ import annotations` above the module docstring → an E402 cascade) that the project's ruff lint gate (a Claude Code PostToolUse hook; other engines run `ruff` manually) surfaces the moment you touch the file — budget for that cleanup per file.

## Code Quality

**Priority** (engine-independent; full rules in `WORKFLOW_ORCHESTRATION.md` § Code Quality): `Correctness > Simplicity > Elegance > Speed`.

- Fix root causes, not temporary patches.
- Write the simplest change that solves the problem; match existing style; touch only what you must.

## References

- `project.md` — file-by-file map (Korean), covering `src/` and `tests/` only — the Korean-edition chapter layout `ch02/`–`ch12/` is not included. Use as a lookup table when locating functionality under `src/`.
- `src/common/evaluation/README_Evaluations.md` — evaluation framework usage.
- Korean repo: https://github.com/TeeDDub/AI-Agent-Engineering
- Original (English): https://github.com/michaelalbada/BuildingApplicationsWithAIAgents
