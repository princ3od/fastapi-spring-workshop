# FastAPI Todo API - Spring Workshop - AIS Lab

## Installation

1. Install FastAPI and required dependencies:

    ```bash
    pip install fastapi[standard] uvicorn
    ```

## Hello World Example

1. Create a new folder.
2. Inside the folder, create a `main.py` file.
3. Add the following code to initialize a FastAPI app:

    ```python
    from fastapi import FastAPI
    
    app = FastAPI()
    
    @app.get("/")
    def hello_world():
        return {"message": "Hello, World!"}
    ```

4. Run the FastAPI server:

    ```bash
    uvicorn main:app --port 8080

    # or

    fastapi dev main.py
    ```

5. Open `http://127.0.0.1:8080` in your browser to see your first API response.

## Path Parameters

1. Create a list of todo items as a mock database:

    ```python
    database = [
        {"todo_id": 1, "title": "Buy groceries", "description": "Milk, Eggs, Bread", "done": False},
        {"todo_id": 2, "title": "Read a book", "description": "Finish Python book", "done": True}
    ]
    ```

2. Add an API endpoint to get a todo item by its ID:

    ```python
    @app.get("/todos/{todo_id}")
    def get_todo(todo_id: int):
        for todo in database:
            if todo["todo_id"] == todo_id:
                return todo
        return {"error": "Todo item not found"}
    ```

3. Example usage of path parameters:

    ```python
    @app.get("/users/{user_id}/todos/{todo_id}")
    def get_user_todo(user_id: int, todo_id: int):
        return {"user_id": user_id, "todo_id": todo_id}
    ```

## Query Parameters

1. Create an API endpoint to filter todos:

    ```python
    from typing import Optional
    
    @app.get("/todos")
    def get_all_todos(size: Optional[int] = None, done: Optional[bool] = None):
        result = database
        if done is not None:
            result = [todo for todo in result if todo["done"] == done]
        return result[:size] if size else result
    ```

## POST Endpoint (Add a Todo Item)

1. Add an endpoint to create a new todo item:

    ```python
    from pydantic import BaseModel, Field
    
    class Todo(BaseModel):
        title: str = Field(..., min_length=1, max_length=100, description="The title of the todo item")
        description: str = Field("", max_length=300, description="A short description of the task")
        done: bool = Field(False, description="Indicates whether the task is completed")
    
    @app.post("/todos")
    def create_todo(todo: Todo):
        new_todo_id = max(todo["todo_id"] for todo in database) + 1
        todo_item = {"todo_id": new_todo_id, **todo.dict()}
        database.append(todo_item)
        return todo_item
    ```

## PUT Endpoint (Update a Todo Item)

1. Modify the `Todo` model to allow optional fields:

    ```python
    from typing import Optional
    
    class TodoUpdate(BaseModel):
        title: Optional[str] = Field(None, max_length=100, description="The title of the todo item")
        description: Optional[str] = Field(None, max_length=300, description="A short description of the task")
        done: Optional[bool] = Field(None, description="Indicates whether the task is completed")
    ```

2. Update the todo item endpoint to support partial updates:

    ```python
    @app.put("/todos/{todo_id}")
    def update_todo(todo_id: int, updated_todo: TodoUpdate):
        for todo in database:
            if todo["todo_id"] == todo_id:
                update_data = updated_todo.dict(exclude_unset=True)
                todo.update(update_data)
                return todo
        return {"error": "Todo item not found"}
    ```

## DELETE Endpoint (Remove a Todo Item)

1. Add an endpoint to delete a todo item:

    ```python
    @app.delete("/todos/{todo_id}")
    def delete_todo(todo_id: int):
        for index, todo in enumerate(database):
            if todo["todo_id"] == todo_id:
                return database.pop(index)
        return {"error": "Todo item not found"}
    ```

## Type Validation & Error Handling

1. Define a more robust `Todo` model with validation:

    ```python
    class Todo(BaseModel):
        title: str = Field(..., min_length=1, max_length=100, description="Title of the todo item")
        description: str = Field("", max_length=300, description="Short description")
        done: bool = Field(False, description="Indicates whether the task is completed")
    ```

2. Use FastAPI’s built-in HTTPException for handling errors:

    ```python
    @app.get("/todos/{todo_id}")
    def get_todo(todo_id: int):
        for todo in database:
            if todo["todo_id"] == todo_id:
                return todo
        return {"error": "Todo item not found"}
    ```

## Automatic API Documentation

FastAPI provides automatic API documentation with Swagger UI and Redoc:

- Visit `http://127.0.0.1:8080/docs` for an interactive Swagger UI.
- Visit `http://127.0.0.1:8080/redoc` for an alternative Redoc UI.

---

Congratulations! You have built a simple Todo API using FastAPI. You can now extend this API with more features, such as authentication, database integration, and even streaming responses. Happy coding! 🚀
