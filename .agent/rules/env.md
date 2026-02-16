---
trigger: always_on
---

# Environment Policy
- All new libraries MUST be installed into a local `.venv`.
- Never install packages to the global Python path.
- If the agent detects a missing dependency, it must first initialize the venv if not present.