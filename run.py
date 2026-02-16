import os
import sys
import multiprocessing
import uvicorn
from todo_app import app

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    # Fix for multiprocessing (needed for uvicorn workers on Windows)
    multiprocessing.freeze_support()
    
    # Check if frozen
    if getattr(sys, 'frozen', False):
        # We are running in a bundle
        bundle_dir = sys._MEIPASS
        
        # IMPORTANT: Maintain persistence by keeping DB file outside the temp folder
        # We want the DB to be in the same folder as the .exe
        exe_dir = os.path.dirname(sys.executable)
        db_path = os.path.join(exe_dir, "todos.db")
        
        # Monkeypatch the DB path in the app module
        # Note: We must ensure app.py uses this variable or we patch it before app logic runs fully
        # In todo_app/app.py: DB_FILE = "todo_app/todos.db"
        # Since we imported app above, the module level code has ALREADY executed with the old path.
        # We need to update it.
        app.DB_FILE = db_path
        
        # However, init_db() was already called at import time with the OLD path.
        # We need to re-initialize the DB with the NEW path.
        # Let's inspect app.py structure again. 
        # It calls init_db() at module level.
        # We should probably modify app.py to execution-defer this or handle it here.
        # Since I cannot easily change app.py structure without risking regression, 
        # I will re-run init_db() here with the new path.
        
        # Updates the variable used in functions
        app.DB_FILE = db_path
        
        # Re-run init to ensure table exists in the REAL db file
        app.init_db()
        
        # Now about static files and templates. 
        # They are mounted as "todo_app/static".
        # If we are frozen, we need to make sure Uvicorn/FastAPI finds them.
        # One way is to change CWD to _MEIPASS, but that breaks the DB path logic if not careful.
        # Actually, FastAPI StaticFiles uses relative paths.
        # If we change CWD to `bundle_dir`, "todo_app/static" must exist there.
        # So we will instruct PyInstaller to copy `todo_app` folder content to `todo_app` in `_MEIPASS`.
        os.chdir(bundle_dir)
        
    # Start Uvicorn
    # host="0.0.0.0" allows access from network, "127.0.0.1" is local only. Use 127.0.0.1 for safety unless specified.
    # port=8001 as requested.
    uvicorn.run(app.app, host="127.0.0.1", port=8001, log_level="info")
