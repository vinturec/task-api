from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()  # only matters when running outside Docker; compose passes env vars directly

import repository_postgres as repo  # swap this for repository_memory to go back to A2

app = FastAPI()


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# ---- Stage 1 ----
@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
    return {"status": "ok"}


# ---- Stage 2 ----
@app.get("/tasks")
def get_tasks():
    return repo.get_all()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = repo.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


# ---- Stage 3 ----
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")
    return repo.create(task.title)


# ---- Stage 4 ----
@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    if update.title is not None and not update.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")
    task = repo.update(task_id, update.title, update.done)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return
