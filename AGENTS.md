# AGENTS.md

Engine-independent project core for **"AI 에이전트 엔지니어링"** (Building Applications with AI Agents, 한빛미디어) — the Korean edition example code.

This file is the **canonical home** for the facts every coding agent needs (project context, build/test commands, architecture, gotchas). Claude Code reads it via the `@AGENTS.md` import in `CLAUDE.md`; Codex (project `AGENTS.md` / `~/.codex/AGENTS.md`) and other agents (e.g. amp) read it directly. **Claude/OMC-specific runtime instructions** (skill routing, hooks, the recall gate, delegation policy) live in `CLAUDE.md`'s "## Claude Code" overlay, **not here** — keep that boundary clean.

## Project Context

Korean translation of the example code for **"AI 에이전트 엔지니어링"** (Building Applications with AI Agents, 한빛미디어). The Korean edition has been reorganized by book chapter (`ch02/`–`ch12/`) and updated for **Python 3.12 + LangChain 1.0**, while the original English framework-style source remains under `src/`. Both layouts coexist; some examples have parallel implementations in both (e.g., MCP servers, customer support agent).

## Common Commands

The project uses **uv** (Astral) exclusively. Do not invoke `pip`, `poetry`, or `pipenv`.

```bash
# Install / sync dependencies (creates .venv, reads uv.lock)
uv sync

# Run any script — uv handles venv activation
uv run python ch02/simple_customer_support_agent.py

# Run the full test suite
uv run pytest -q

# Run a single test file
uv run pytest tests/evaluation/test_ai_judge.py -v

# Run a single test by name
uv run pytest tests/evaluation/test_ai_judge.py::TestAIJudge::test_specific_method -v

# Add a new dependency (auto-updates pyproject.toml + uv.lock)
uv add <package>
uv add --dev <package>

# Optional: install fine-tuning extras (heavy: torch, transformers, peft, trl, bitsandbytes)
uv sync --extra fine-tuning

# Run batch evaluation (entry point referenced from project.md)
uv run python -m src.common.evaluation.batch_evaluation \
  --dataset src/common/evaluation/scenarios/<domain>_evaluation_set.jsonl \
  --graph_py src/frameworks/langgraph_agents/<domain>/<agent>.py

# Start the local observability stack (Loki + Tempo + Promtail)
cd src/common/observability && docker-compose up -d
```

### Environment

- Python is **pinned to 3.12** (`>=3.12,<3.13` in `pyproject.toml`; venv runs CPython 3.12.11). Do not assume 3.13+ syntax/stdlib.
- `.env` is required at the repo root with `OPENAI_API_KEY` (template: `.env.example`). Some examples additionally need `WOLFRAM_ALPHA_APP_ID`, `YOUR_SLACK_BOT_TOKEN`, `TRACELOOP_API_KEY`, `LANGCHAIN_API_KEY`.
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

- `src/common/` — framework-agnostic infrastructure
  - `evaluation/` — `metrics.py` (Tool Recall/Precision, Phrase Recall, Task Success), `ai_judge.py` (LLM-as-judge), `batch_evaluation.py` (the JSONL → metrics pipeline), `memory_evaluation.py`, `distribution_shifts.py`. Domain scenarios live in `evaluation/scenarios/*.jsonl`.
  - `observability/` — `loki_logger.py` (HTTP push to `LOKI_ENDPOINT`), `instrument_tempo.py` (OTLP spans → `TEMPO_ENDPOINT`), plus `docker-compose.yaml` to run the stack locally.
  - `a2a/` — Agent-to-Agent JSON-RPC 2.0 protocol (`agent_server.py` exposes `/.well-known/agent.json`, `agent_client.py` discovers and calls).
  - `mcp/` — Model Context Protocol servers (math, weather) over stdio.
  - `graph_rag.py` — single-file Graph RAG implementation (chunking → entity extraction → Leiden community detection → hierarchical summarization).
- `src/frameworks/<framework>_agents/` — agent implementations grouped by SDK (`langchain/`, `langgraph_agents/`, `autogen_agents/`, `open_ai/`).
- `src/frameworks/langgraph_agents/<domain>/` — **7 production-style domain agents** (ecommerce, financial_services, healthcare, it_helpdesk, legal, soc, supply_chain). Each domain pairs an agent file with a JSONL evaluation set under `src/common/evaluation/scenarios/`.
- `src/fine_tuning/` — SFT, DPO, RLVR scripts. Training data in `training_data/*.jsonl`. Output checkpoints land under `ch07/fine_tuned_model/` (gitignored).

### Chapter map (ch02–ch12)

| Ch | Topic | Key files |
|----|-------|-----------|
| 02 | Simple agent + evaluation | `simple_customer_support_agent.py`, `customer_support_agent_evaluation.py` |
| 03 | Realtime voice agent | FastAPI + WebSockets backend (`realtime_voice_agent.py`) + browser client (`index.html`) |
| 04 | Tool use + MCP | Calculator/Wikipedia/Stock tools; `mcp_servers/` (math, weather) — note: duplicates `src/common/mcp/` |
| 05 | Skill selection | basic / semantic (embedding) / hierarchical |
| 06 | Memory | `short_term_memory.py` (LangGraph `MemorySaver`), `basic_bm25.py` (long-term retrieval primitives), `graphrag_test.sh` |
| 07 | Learning + fine-tuning | Reflexion, experiential learning, SFT, DPO, RLVR + `test_*_model.py` runners |
| 08 | Multi-agent supply chain | LangGraph baseline + Ray / Redis Streams / Temporal variants + `adas/` (Automated Design of Agentic Systems) + `a2a/` |
| 09 | Evaluation | `metrics.py`, `memory_evaluation.py`, `batch_evaluation.py`, `agents/`, `scenarios/` (mirrors `src/common/evaluation/`) |
| 10 | Distribution shifts | KS test / KL divergence / PSI / embedding-based drift |
| 11 | SOC analyst | `soc_analyst_agent.py` + DSPy-based optimizers |
| 12 | Prompt injection defense | `llm-guard` based blocklist + PII anonymization |

`notebook/ch0X_*.ipynb` — Colab-friendly versions (Traceloop/Loki removed; ch03 won't run in Colab; ch08 distributed variants need extra infra).

## Project-Specific Gotchas

> Path-scoped gotchas (fine-tuning, MCP server copies, observability) live in `.claude/rules/`. Claude Code auto-loads them when reading files under their target paths (`ch07/**`, `src/fine_tuning/**`, `ch04/mcp_servers/**`, `src/common/mcp/**`, `src/common/observability/**`); other engines should read those rule files manually when working under those paths. The entries below are command/build-level (triggered by intent, not file reads) and stay eager here.

### Test import path is broken at the repo root (verified)
Tests use bare `from common.evaluation.ai_judge import AIJudge` style, but `uv run pytest` from the repo root fails with `ModuleNotFoundError: No module named 'common'`. There is **no `conftest.py` at the repo root** to add `src/` to `sys.path`, and `pyproject.toml` configures hatchling with `packages = ["src"]` (which would install as `src.common.*`, not `common.*`).
- The tests presumably worked when invoked from inside `src/` or via an IDE that injects sources roots (the `.idea/` config + JetBrains MCP bridge in `.mcp.json` suggests this).
- For headless `uv run pytest`: either add a root `conftest.py` doing `sys.path.insert(0, str(Path(__file__).parent / "src"))`, or ask the user before rewriting all `from common...` to `from src.common...`. Don't silently change either without confirmation.

### `pytest.ini` overrides `pyproject.toml` test config
The repo has BOTH `pytest.ini` (only `filterwarnings`) and `[tool.pytest.ini_options]` in `pyproject.toml` (with `testpaths = ["tests"]`, etc.). When `pytest.ini` exists, pytest **ignores** the pyproject.toml block entirely. Consequence: `uv run pytest` collects every `test_*.py` in the repo, including `ch07/test_dpo_model.py` / `ch07/test_sft_model.py` / `ch07/test_rlvr_model.py` (which require the optional `fine-tuning` extras and fail with `ModuleNotFoundError: No module named 'peft'` by default).
- Workaround for normal runs: `uv run pytest tests/ -q` (explicit path) or merge the pyproject `[tool.pytest.ini_options]` keys into `pytest.ini`.
- Don't "fix" by deleting `pytest.ini` — its `filterwarnings` setting is intentional.

### Duplicate dev dependency declarations
`pyproject.toml` declares dev dependencies in **both** `[project.optional-dependencies] dev` (PEP 631, for `pip install -e .[dev]` callers) and `[dependency-groups] dev` (PEP 735, uv-canonical). Content is identical and must be kept in sync manually when adding/removing dev tools — `uv add --dev <pkg>` only updates the `[dependency-groups]` block. Migration from the legacy `[tool.uv].dev-dependencies` form was completed in commit `060ccd0`; don't reintroduce that section.

### `src/__init__.py` exists
`src/` is a Python package, not a source root. Tests that already work via the bare-`common` style imply some sys.path manipulation is happening (likely IDE-level via `.idea/` for JetBrains, see `.mcp.json`). Headless `uv run pytest` may not replicate this.

### `.mcp.json` registers a JetBrains SSE bridge
The local `.mcp.json` points at the JetBrains IDE plugin's local SSE endpoint (`http://127.0.0.1:<dynamic-port>/sse`). The port is assigned by the JetBrains plugin at IDE startup and changes between sessions — do **not** treat the exact port as a current-state fact. Verify with `cat .mcp.json` if the value matters. The file is gitignored (`.mcp.json` in `.gitignore`) and **not tracked** — `git ls-files .mcp.json` returns nothing; the JetBrains plugin recreates it on demand. Don't add secrets here; use `.mcp.json.example` for templates.

## Code Quality

**Priority** (engine-independent; full rules in `WORKFLOW_ORCHESTRATION.md` § Code Quality and user-scope `~/.claude/CODE_QUALITY.md`): `Correctness > Simplicity > Elegance > Speed`.

- Fix root causes, not temporary patches.
- Write the simplest change that solves the problem; match existing style; touch only what you must.

## References

- `project.md` — exhaustive file-by-file map (Korean). Use as a lookup table when locating functionality.
- `src/common/evaluation/README_Evaluations.md` — evaluation framework usage.
- Korean repo: https://github.com/TeeDDub/AI-Agent-Engineering
- Original (English): https://github.com/michaelalbada/BuildingApplicationsWithAIAgents
