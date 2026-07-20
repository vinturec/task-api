import os
import sqlite3
from typing import Optional

DB_PATH = os.environ.get("SQLITE_DB_PATH", "tasks.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done  BOOLEAN NOT NULL DEFAULT 0
            );
        """)
        count = conn.execute("SELECT COUNT(*) FROM tasks;").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?);",
                [("Buy milk", 0), ("Walk the dog", 1), ("Write report", 0)],
            )
        conn.commit()


def _row_to_dict(row):
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


def get_all():
    with _get_conn() as conn:
        rows = conn.execute("SELECT id, title, done FROM tasks ORDER BY id;").fetchall()
        return [_row_to_dict(r) for r in rows]


def get_by_id(task_id):
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?;", (task_id,)
        ).fetchone()
        return _row_to_dict(row) if row else None


def create(title):
    with _get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (title, done) VALUES (?, 0);", (title,)
        )
        conn.commit()
        new_id = cur.lastrowid
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?;", (new_id,)
        ).fetchone()
        return _row_to_dict(row)


def update(task_id, title: Optional[str], done: Optional[bool]):
    existing = get_by_id(task_id)
    if existing is None:
        return None
    new_title = title if title is not None else existing["title"]
    new_done = done if done is not None else existing["done"]
    with _get_conn() as conn:
        conn.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?;",
            (new_title, int(new_done), task_id),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?;", (task_id,)
        ).fetchone()
        return _row_to_dict(row)


def delete(task_id):
    with _get_conn() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
        conn.commit()
        return cur.rowcount > 0


init_db()
