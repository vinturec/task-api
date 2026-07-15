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

hey can you build me a simple crud api in python using fastapi. it's for managing a to-do list of tasks. each task should just have an id, a title, and a done true/false field. don't use a database, just keep everything in memory in a list.
i need these routes:

GET /tasks - gives back all the tasks
GET /tasks/{id} - gives back one task
POST /tasks - creates a new task
PUT /tasks/{id} - updates a task
DELETE /tasks/{id} - deletes a task

if someone tries to get/update/delete a task id that doesn't exist, send back a 404 with an error message. if someone tries to create a task with an empty or missing title, send back a 400.
also make sure it uses the right status codes — 200 for normal get requests, 201 when something's created, 204 when something's deleted