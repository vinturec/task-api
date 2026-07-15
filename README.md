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

I hand-wrote main.py through Stages 0-6, then prompted an AI to build the same 
API from a fresh description (see prompt below) and compared the two.

**Prompt used:**
"hey can you build me a simple crud api in python using fastapi. it's for managing 
a to-do list of tasks. each task should just have an id, a title, and a done 
true/false field. don't use a database, just keep everything in memory in a list. 
i need these routes: GET /tasks, GET /tasks/{id}, POST /tasks, PUT /tasks/{id}, 
DELETE /tasks/{id}. if someone tries to get/update/delete a task id that doesn't 
exist, send back a 404 with an error message. if someone tries to create a task 
with an empty or missing title, send back a 400. also make sure it uses the right 
status codes — 200 for normal get requests, 201 when something's created, 204 
when something's deleted."

**What the AI did better:** It added a title to the FastAPI app 
(`FastAPI(title="Task API")`) and used explicit type hints like `list[dict]` for 
the tasks list, which is slightly more polished Python style than my version.

**What it got wrong or ignored:** [fill in once you see the rest of the diff — 
e.g. did it handle the title-validation the same way, same status codes, etc.]

**What my prompt didn't specify:** I never told it how to generate new task ids, 
what Python version to target, or exactly how to word error messages — the AI 
made its own reasonable choices on all of these, and they ended up close to mine 
but not identical
