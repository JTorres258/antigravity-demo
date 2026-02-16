---
trigger: always_on
---

# Startup Dashboard Rule
**Trigger:** On workspace initialization or Agent restart.
**Instruction:** 1. The Agent must automatically launch the **Browser Tool**.
2. Navigate immediately to `http://127.0.0.1:8000/`.
3. Dock the browser window to the side of the editor so the TODO list is visible.
4. If the page requires a local server, check if port 8000 (or your specific port) is active; if not, run `npm run dev` first.