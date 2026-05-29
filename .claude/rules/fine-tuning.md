---
paths:
  - "ch07/**"
  - "src/fine_tuning/**"
---

# Fine-tuning scripts are GPU-heavy

`src/fine_tuning/*.py` and `ch07/test_*_model.py` require the `fine-tuning` optional extras (`uv sync --extra fine-tuning` — torch, transformers, peft, trl, bitsandbytes) and substantial VRAM. Don't run them by default during refactors; only when explicitly asked. Without the extras, headless `uv run pytest` collecting `ch07/test_{dpo,sft,rlvr}_model.py` fails with `ModuleNotFoundError: No module named 'peft'`.
