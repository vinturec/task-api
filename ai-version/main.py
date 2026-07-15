from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task API")

tasks: list[dict] = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Walk the dog", "done": True},
    {"id": 3, "title": "Write report", "done": False},
]


class TaskCreate(BaseModel):
    title: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


def _find_task(task_id: int) -> Optional[dict]:
    return next((task for task in tasks if task["id"] == task_id), None)


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = _find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate):
    if body.title is None or not body.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")

    new_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {"id": new_id, "title": body.title, "done": False}
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate):
    task = _find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if body.title is not None:
        if not body.title.strip():
            raise HTTPException(status_code=400, detail="title cannot be empty")
        task["title"] = body.title

    if body.done is not None:
        task["done"] = body.done

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    task = _find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    tasks.remove(task)
