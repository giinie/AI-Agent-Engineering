---
paths:
  - "ch04/mcp_servers/**"
  - "src/common/mcp/**"
---

# Two MCP server copies

`ch04/mcp_servers/{MCP_math_server,MCP_weather_server}.py` and `src/common/mcp/MCP_{math,weather}_server.py` are separate files. Edits in one are not reflected in the other. Confirm which copy a fix should target before editing.
