---
paths:
  - "src/common/observability/**"
---

# Observability is opt-in

`loki_logger.py` and `instrument_tempo.py` hardcode `http://localhost:3100` / `http://localhost:3200`; the endpoints are **not** configurable by environment variable, so point them elsewhere by editing the modules. `log_to_loki()` posts with no try/except and no timeout, so it raises `ConnectionError` when the stack is down; it does **not** degrade quietly. Either start the local stack (`cd src/common/observability && docker-compose up -d`) or stub these calls when running examples standalone.
