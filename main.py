from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

# 1. Initialize the FastAPI app
app = FastAPI(
    title="My To-Do List API",
    description="A simple API for learning FastAPI and Render deployment.",
    version="1.0.0",
)

# 2. Pydantic Models for our To-Do items
# This defines the "shape" of our data and validates it.
class Todo(BaseModel):
    id: int
    title: str
    completed: bool

# This model is for creating a new Todo, where the ID is not needed
class TodoCreate(BaseModel):
    title: str
    completed: bool = False # Give a default value

# 3. A simple in-memory "database"
# We'll use a Python dictionary to store our to-dos.
# The key will be the todo's ID.
db: Dict[int, Todo] = {
    1: Todo(id=1, title="Learn FastAPI", completed=True),
    2: Todo(id=2, title="Deploy on Render", completed=False),
    3: Todo(id=3, title="Connect Flutter App", completed=False),
}
next_id = 4 # To auto-increment our IDs

# 4. API Endpoints (Our "Routes")

@app.get("/")
def read_root():
    """A welcome message for the root URL."""
    return {"message": "Welcome to the To-Do List API! Go to /docs to see the API documentation."}

@app.get("/todos", response_model=List[Todo])
def get_all_todos():
    """Retrieve all to-do items."""
    return list(db.values())

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo_in: TodoCreate):
    """Create a new to-do item."""
    global next_id
    # Create a full Todo object from the TodoCreate model
    new_todo = Todo(id=next_id, title=todo_in.title, completed=todo_in.completed)
    db[next_id] = new_todo
    next_id += 1
    return new_todo

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int):
    """Retrieve a single to-do item by its ID."""
    if todo_id not in db:
        raise HTTPException(status_code=404, detail="To-Do item not found")
    return db[todo_id]

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_in: TodoCreate):
    """Update an existing to-do item."""
    if todo_id not in db:
        raise HTTPException(status_code=404, detail="To-Do item not found")
    
    # Update the fields of the existing todo
    existing_todo = db[todo_id]
    existing_todo.title = todo_in.title
    existing_todo.completed = todo_in.completed
    
    db[todo_id] = existing_todo
    return existing_todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    """Delete a to-do item."""
    if todo_id not in db:
        raise HTTPException(status_code=404, detail="To-Do item not found")
    del db[todo_id]
    # A 204 No Content response doesn't return a body, so we return nothing
    return