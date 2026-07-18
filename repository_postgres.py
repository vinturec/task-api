"""
Postgres task repository — same interface as repository_memory.py:
get_all(), get_by_id(id), create(title), update(id, title, done), delete(id).

main.py doesn't know or care which one it's talking to. That's the point
of this assignment: swap this import in, and nothing else changes.
"""
import os
import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ["DATABASE_URL"]


def _get_conn():
    return psycopg2.connect(DATABASE_URL)


def get_all():
    with _get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT id, title, done FROM tasks ORDER BY id;")
        return cur.fetchall()


def get_by_id(task_id: int):
    with _get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
        return cur.fetchone()


def create(title: str):
    with _get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "INSERT INTO tasks (title, done) VALUES (%s, FALSE) RETURNING id, title, done;",
            (title,),
        )
        row = cur.fetchone()
        conn.commit()
        return row


def update(task_id: int, title: str | None, done: bool | None):
    existing = get_by_id(task_id)
    if existing is None:
        return None
    new_title = title if title is not None else existing["title"]
    new_done = done if done is not None else existing["done"]
    with _get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;",
            (new_title, new_done, task_id),
        )
        row = cur.fetchone()
        conn.commit()
        return row


def delete(task_id: int) -> bool:
    with _get_conn() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        return deleted
