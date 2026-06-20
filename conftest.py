import sys
from pathlib import Path

# Tests import the cross-cutting modules with the bare ``common.*`` style
# (e.g. ``from common.evaluation.ai_judge import AIJudge``). Those packages live
# under ``src/``, which is not a source root for headless ``uv run pytest`` (no
# IDE sys.path injection). Put ``src/`` on sys.path so the bare imports resolve.
sys.path.insert(0, str(Path(__file__).parent / "src"))
