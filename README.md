# Task API

A simple in-memory CRUD API for managing tasks, built with FastAPI.

## How to run it

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi "uvicorn[standard]"
uvicorn main:app --reload --port 8000
```

Then visit http://127.0.0.1:8000/docs for interactive Swagger docs.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | /tasks | List all tasks |
| GET | /tasks/{id} | Get one task |
| POST | /tasks | Create a task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |

## Example request

```
curl -i http://127.0.0.1:8000/tasks
```

Response:

```
PASTE_YOUR_CURL_OUTPHTTP/1.1 200 OK
date: Wed, 15 Jul 2026 11:28:57 GMT
server: uvicorn
content-length: 131
content-type: application/json

[{"id":1,"title":"Buy milk","done":false},{"id":2,"title":"Walk the dog","done":true},{"id":3,"title":"Write report","done":false}]%  UT_HERE
```

## Swagger screenshot

Screenshot 2026-07-15 at 2.31.12 PM.png

## AI vs me

Coming after Stage 7.## BE-04: Containerized stack (app + Postgres)

### How to run it

```
cp .env.example .env      # then edit values if you want
docker compose up --build
```

Visit http://localhost:8000/docs for Swagger, or http://localhost:8000/tasks.

### What changed from A2

`main.py`'s routes are **unchanged** — same paths, same status codes, same
validation. What changed is a single import:

```python
import repository_postgres as repo   # was: manipulating a list directly
```

`repository_postgres.py` exposes the exact same functions as the original
in-memory version (`get_all`, `get_by_id`, `create`, `update`, `delete`),
so the routes never needed to know storage changed underneath them. The
in-memory version still lives in `repository_memory.py` if you want to
diff the two side by side.

### Persistence proof

1. `docker compose up -d`
2. `curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"survive a restart"}'`
3. `docker compose down` (stops + removes containers, but the named volume `pgdata` is kept)
4. `docker compose up -d`
5. `curl http://localhost:8000/tasks` → the new task is still there.

(If you instead run `docker compose down -v`, the volume is deleted and
you'll go back to just the 3 seed rows — that's expected, it's the
same "gone on reset" lesson from A2, except now the reset button is a
flag you have to explicitly pass instead of just restarting the process.)

### Env vars

`.env` is gitignored; `.env.example` is committed as the template. The
app reads `DATABASE_URL` (via `docker-compose.yml`'s `environment:` block,
which pulls from `.env` at the project root).
