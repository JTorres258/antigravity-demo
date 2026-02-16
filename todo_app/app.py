from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
import os

app = FastAPI(title="Tao Todo API", description="A simple API for managing todo items.")

# Mount static files
app.mount("/static", StaticFiles(directory="todo_app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="todo_app/templates")

# Database setup
DB_FILE = "todo_app/todos.db"

def init_db():
    """Initializes the SQLite database and creates the todos table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Models
class TodoCreate(BaseModel):
    """Schema for creating a new todo item."""
    title: str

class TodoUpdate(BaseModel):
    """Schema for updating an existing todo item."""
    title: Optional[str] = None
    completed: Optional[bool] = None

class TodoItem(BaseModel):
    """Schema for a todo item response."""
    id: int
    title: str
    completed: bool

# Helpers
def get_db_connection():
    """Establishes/returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.get("/")
async def home(request: Request):
    """Serves the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/todos", response_model=List[TodoItem])
async def get_todos():
    """Retrieves all todo items from the database."""
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return [dict(todo) for todo in todos]

@app.post("/api/todos", response_model=TodoItem)
async def create_todo(todo: TodoCreate):
    """Creates a new todo item."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todos (title, completed) VALUES (?, ?)', (todo.title, False))
    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": todo_id, "title": todo.title, "completed": False}

@app.put("/api/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo: TodoUpdate):
    """Updates an existing todo item's title or completion status."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if exists
    existing = cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    
    current_title = existing['title']
    current_completed = existing['completed']
    
    new_title = todo.title if todo.title is not None else current_title
    new_completed = todo.completed if todo.completed is not None else current_completed
    
    cursor.execute('UPDATE todos SET title = ?, completed = ? WHERE id = ?', (new_title, new_completed, todo_id))
    conn.commit()
    conn.close()
    
    return {"id": todo_id, "title": new_title, "completed": new_completed}

@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """Deletes a todo item by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return {"message": "Todo deleted"}
