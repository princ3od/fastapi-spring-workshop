from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI()

# Mock database
database = [
    {"todo_id": 1, "title": "買い物", "description": "牛乳、卵、パン", "done": False},
    {"todo_id": 2, "title": "本を読む", "description": "Python の本を終わらせる", "done": True}
]

# Hello World endpoint
@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

# Get Todo by ID endpoint
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in database:
        if todo["todo_id"] == todo_id:
            return todo
    # Use HTTPException for error handling
    raise HTTPException(status_code=404, detail="Todo アイテムが見つかりません")

# Path parameter example (user todo)
@app.get("/users/{user_id}/todos/{todo_id}")
def get_user_todo(user_id: int, todo_id: int):
    return {"user_id": user_id, "todo_id": todo_id}

# Query parameter example (filter todos)
@app.get("/todos")
def get_all_todos(size: Optional[int] = None, done: Optional[bool] = None):
    result = database
    if done is not None:
        result = [todo for todo in result if todo["done"] == done]
    return result[:size] if size else result

# Pydantic model for creating a Todo item
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Todo アイテムのタイトル")
    description: str = Field("", max_length=300, description="タスクの簡単な説明")
    done: bool = Field(False, description="タスクが完了しているかどうか")

class Todo(TodoCreate):
    todo_id: int = Field(..., description="Todo アイテムのID")

# POST endpoint to create a new Todo item
@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo["todo_id"] for todo in database) + 1
    todo_item = {"todo_id": new_todo_id, **todo.dict()}
    database.append(todo_item)
    return todo_item

# Pydantic model for updating a Todo item
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100, description="Todo アイテムのタイトル")
    description: Optional[str] = Field(None, max_length=300, description="タスクの簡単な説明")
    done: Optional[bool] = Field(None, description="タスクが完了しているかどうか")

# PUT endpoint to update a Todo item
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in database:
        if todo["todo_id"] == todo_id:
            update_data = updated_todo.dict(exclude_unset=True)
            todo.update(update_data)
            return todo
    # Use HTTPException for error handling
    raise HTTPException(status_code=404, detail="Todo アイテムが見つかりません")

# DELETE endpoint to delete a Todo item
@app.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(database):
        if todo["todo_id"] == todo_id:
            return database.pop(index)
    # Use HTTPException for error handling
    raise HTTPException(status_code=404, detail="Todo アイテムが見つかりません")
