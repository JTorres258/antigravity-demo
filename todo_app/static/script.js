const todoInput = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');
const todoList = document.getElementById('todo-list');

// API Base URL
const API_URL = '/api/todos';

// Fetch Todos on Load
document.addEventListener('DOMContentLoaded', fetchTodos);

// Event Listeners
addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTodo();
});

/**
 * Fetches all todos from the API and renders them.
 */
async function fetchTodos() {
    try {
        const response = await fetch(API_URL);
        const todos = await response.json();
        renderTodos(todos);
    } catch (error) {
        console.error('Error fetching todos:', error);
    }
}

/**
 * Sends a POST request to create a new todo item.
 */
async function addTodo() {
    const text = todoInput.value.trim();
    if (!text) return;

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: text })
        });

        if (response.ok) {
            todoInput.value = '';
            fetchTodos();
        }
    } catch (error) {
        console.error('Error adding todo:', error);
    }
}

/**
 * Toggles a todo's completion status via PUT request.
 * @param {number} id - The ID of the todo.
 * @param {boolean} currentStatus - The current completion status.
 */
async function toggleTodo(id, currentStatus) {
    try {
        await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ completed: !currentStatus })
        });
        fetchTodos();
    } catch (error) {
        console.error('Error toggling todo:', error);
    }
}

/**
 * Deletes a todo item via DELETE request.
 * @param {number} id - The ID of the todo to delete.
 */
async function deleteTodo(id) {
    try {
        await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        fetchTodos(); // Refresh list
    } catch (error) {
        console.error('Error deleting todo:', error);
    }
}

/**
 * Renders the list of todos into the DOM.
 * @param {Array} todos - The list of todo objects.
 */
function renderTodos(todos) {
    todoList.innerHTML = '';
    todos.forEach(todo => {
        const li = document.createElement('li');
        li.className = `todo-item ${todo.completed ? 'completed' : ''}`;

        li.innerHTML = `
            <div class="todo-content" onclick="toggleTodo(${todo.id}, ${todo.completed})">
                <div class="check-circle"></div>
                <span class="todo-text">${escapeHtml(todo.title)}</span>
            </div>
            <button class="delete-btn" onclick="deleteTodo(${todo.id})">
                <i class="fas fa-trash"></i>
            </button>
        `;

        todoList.appendChild(li);
    });
}

/**
 * Escapes HTML characters to prevent XSS.
 * @param {string} text - The input text.
 * @returns {string} - Escaped text.
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
