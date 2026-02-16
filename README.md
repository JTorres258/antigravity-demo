# Tao Todo App

A simple, functional, and aesthetically pleasing Todo List web application built with Python (FastAPI) and vanilla HTML/CSS/JS.

## Features
- **FastAPI Backend**: Efficient and modern Python web framework.
- **SQLite Database**: Lightweight and serverless persistent storage.
- **Premium UI**: Dark mode design with glassmorphism and smooth animations.
- **Interactive**: Real-time updates without page reloads.

## Structure
- `app.py`: Main entry point and API definitions.
- `templates/index.html`: The HTML structure of the application.
- `static/style.css`: The styling and animations.
- `static/script.js`: The frontend logic for interacting with the API.

## How to Run

1.  **Navigate to the project root** (parent directory of `todo_app`).
2.  **Activate your virtual environment**:
    ```bash
    .venv/Scripts/activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application**:
    ```bash
    uvicorn todo_app.app:app --reload
    ```
5.  **Open in Browser**:
    Visit [http://127.0.0.1:8001](http://127.0.0.1:8001).

## Running as Executable

The application can also be run as a standalone executable.

1.  **Navigate to the `dist` folder**:
    ```powershell
    cd dist
    ```
2.  **Run the executable**:
    ```powershell
    ./TaoTodo.exe
    ```
3.  **Open in Browser**:
    Visit [http://127.0.0.1:8001](http://127.0.0.1:8001).

> **Note**: The database `todos.db` will be created in the same folder as the executable to ensure data persistence.


## Agent Rules

This project adheres to specific rules defined in the `.agent/rules` directory.

### Environment Policy (`.agent/rules/env.md`)
- All new libraries MUST be installed into a local `.venv`.
- Never install packages to the global Python path.
- If the agent detects a missing dependency, it must first initialize the venv if not present.

### Startup Dashboard Rule (`.agent/rules/startup.md`)
**Trigger:** On workspace initialization or Agent restart.
**Instruction:**
1. The Agent must automatically launch the **Browser Tool**.
2. Navigate immediately to `http://127.0.0.1:8001/`.
3. Dock the browser window to the side of the editor so the TODO list is visible.
4. If the page requires a local server, check if port 8001 (or your specific port) is active; if not, run `uvicorn todo_app.app:app --reload` first.
