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
3.  **Run the application**:
    ```bash
    uvicorn todo_app.app:app --reload
    ```
4.  **Open in Browser**:
    Visit [http://127.0.0.1:8000](http://127.0.0.1:8000).
