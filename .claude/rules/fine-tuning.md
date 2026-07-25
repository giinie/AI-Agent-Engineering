---
paths:
  - "ch07/**"
  - "src/fine_tuning/**"
---

# Fine-tuning scripts are GPU-heavy

`src/fine_tuning/*.py` and `ch07/test_*_model.py` require the `fine-tuning` optional extras (`uv sync --extra fine-tuning` — torch, transformers, peft, trl, bitsandbytes, datasets) and substantial VRAM. Don't run them by default during refactors; only when explicitly asked. Without the extras, headless `uv run pytest` collecting `ch07/test_{dpo,sft}_model.py` fails with `ModuleNotFoundError: No module named 'peft'` (`test_rlvr_model.py` imports only torch/transformers, present as transitive deps, so it collects fine).
