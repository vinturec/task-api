"""
In-memory task repository.

This is your ORIGINAL Stage 0-6 storage, just moved into its own module
so it has the exact same shape (function names + return values) as
repository_postgres.py. main.py talks to whichever one is imported —
it never touches a list or a database directly.
"""

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Walk the dog", "done": True},
    {"id": 3, "title": "Write report", "done": False},
]


def get_all():
    return tasks


def get_by_id(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def create(title: str):
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": title, "done": False}
    tasks.append(new_task)
    return new_task


def update(task_id: int, title: str | None, done: bool | None):
    task = get_by_id(task_id)
    if task is None:
        return None
    if title is not None:
        task["title"] = title
    if done is not None:
        task["done"] = done
    return task


def delete(task_id: int) -> bool:
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return True
    return False
