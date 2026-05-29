---
paths:
  - "src/common/observability/**"
---

# Observability is opt-in

`loki_logger.py` and `instrument_tempo.py` no-op gracefully if `LOKI_ENDPOINT` / `TEMPO_ENDPOINT` are unreachable, but errors may surface in logs. Either start the local stack (`cd src/common/observability && docker-compose up -d`) or stub these calls when running examples standalone.
