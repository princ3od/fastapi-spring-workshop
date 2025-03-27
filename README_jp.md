# FastAPI Todo API - Spring Workshop - AIS Lab

## インストール

1. FastAPI と必要な依存関係をインストールします:

    ```bash
    pip install fastapi[standard] uvicorn
    ```

## Hello World の例

1. 新しいフォルダを作成します。
2. フォルダ内に `main.py` ファイルを作成します。
3. 次のコードを追加して、FastAPI アプリを初期化します:

    ```python
    from fastapi import FastAPI
    
    app = FastAPI()
    
    @app.get("/")
    def hello_world():
        return {"message": "Hello, World!"}
    ```

4. FastAPI サーバーを実行します:

    ```bash
    uvicorn main:app --port 8080

    # または

    fastapi dev main.py
    ```

5. ブラウザで `http://127.0.0.1:8080` を開いて、最初の API レスポンスを確認します。

## パスパラメータ

1. todo アイテムのリストをモックデータベースとして作成します:

    ```python
    database = [
        {"todo_id": 1, "title": "買い物", "description": "牛乳、卵、パン", "done": False},
        {"todo_id": 2, "title": "本を読む", "description": "Python の本を終わらせる", "done": True}
    ]
    ```

2. ID で todo アイテムを取得する API エンドポイントを追加します:

    ```python
    @app.get("/todos/{todo_id}")
    def get_todo(todo_id: int):
        for todo in database:
            if todo["todo_id"] == todo_id:
                return todo
        return {"error": "Todo アイテムが見つかりません"}
    ```

3. パスパラメータの使用例:

    ```python
    @app.get("/users/{user_id}/todos/{todo_id}")
    def get_user_todo(user_id: int, todo_id: int):
        return {"user_id": user_id, "todo_id": todo_id}
    ```

## クエリパラメータ

1. todo アイテムをフィルタリングする API エンドポイントを作成します:

    ```python
    from typing import Optional
    
    @app.get("/todos")
    def get_all_todos(size: Optional[int] = None, done: Optional[bool] = None):
        result = database
        if done is not None:
            result = [todo for todo in result if todo["done"] == done]
        return result[:size] if size else result
    ```

## POST エンドポイント (Todo アイテムの追加)

1. 新しい todo アイテムを作成するエンドポイントを追加します:

    ```python
    from pydantic import BaseModel, Field
    
    class Todo(BaseModel):
        title: str = Field(..., min_length=1, max_length=100, description="Todo アイテムのタイトル")
        description: str = Field("", max_length=300, description="タスクの簡単な説明")
        done: bool = Field(False, description="タスクが完了しているかどうか")
    
    @app.post("/todos")
    def create_todo(todo: Todo):
        new_todo_id = max(todo["todo_id"] for todo in database) + 1
        todo_item = {"todo_id": new_todo_id, **todo.dict()}
        database.append(todo_item)
        return todo_item
    ```

## PUT エンドポイント (Todo アイテムの更新)

1. `Todo` モデルを変更して、オプションのフィールドを追加します:

    ```python
    from typing import Optional
    
    class TodoUpdate(BaseModel):
        title: Optional[str] = Field(None, max_length=100, description="Todo アイテムのタイトル")
        description: Optional[str] = Field(None, max_length=300, description="タスクの簡単な説明")
        done: Optional[bool] = Field(None, description="タスクが完了しているかどうか")
    ```

2. Todo アイテムのエンドポイントを更新して部分的な更新をサポートします:

    ```python
    @app.put("/todos/{todo_id}")
    def update_todo(todo_id: int, updated_todo: TodoUpdate):
        for todo in database:
            if todo["todo_id"] == todo_id:
                update_data = updated_todo.dict(exclude_unset=True)
                todo.update(update_data)
                return todo
        return {"error": "Todo アイテムが見つかりません"}
    ```

## DELETE エンドポイント (Todo アイテムの削除)

1. Todo アイテムを削除するエンドポイントを追加します:

    ```python
    @app.delete("/todos/{todo_id}")
    def delete_todo(todo_id: int):
        for index, todo in enumerate(database):
            if todo["todo_id"] == todo_id:
                return database.pop(index)
        return {"error": "Todo アイテムが見つかりません"}
    ```

## 型検証とエラーハンドリング

1. より堅牢な `Todo` モデルを定義して検証を行います:

    ```python
    class Todo(BaseModel):
        title: str = Field(..., min_length=1, max_length=100, description="Todo アイテムのタイトル")
        description: str = Field("", max_length=300, description="簡単な説明")
        done: bool = Field(False, description="タスクが完了しているかどうか")
    ```

2. FastAPI の組み込み `HTTPException` を使用してエラーを処理します:

    ```python
    @app.get("/todos/{todo_id}")
    def get_todo(todo_id: int):
        for todo in database:
            if todo["todo_id"] == todo_id:
                return todo
        return {"error": "Todo アイテムが見つかりません"}
    ```

## 自動 API ドキュメンテーション

FastAPI は Swagger UI と Redoc で自動的に API ドキュメンテーションを提供します:

- インタラクティブな Swagger UI にアクセスするには `http://127.0.0.1:8080/docs` を訪問します。
- 代替の Redoc UI にアクセスするには `http://127.0.0.1:8080/redoc` を訪問します。

---

おめでとうございます！FastAPI を使ってシンプルな Todo API を作成しました。これから認証、データベース統合、さらにはストリーミングレスポンスなど、さらに多くの機能を追加することができます。楽しいコーディングを！ 🚀
