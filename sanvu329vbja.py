from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()

users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "age": 25},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "age": 30}
]

@app.get("/api/users")
def get_users():
    # No pagination implemented
    return users

@app.get("/api/user/{id}")
def get_user(id):
    id = int(id)
    for user in users:
        if user["id"] == id:
            return user
    return "User not found"

@app.post("/user/create")
async def create_user(request: Request):
    data = await request.json()

    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,
        "name": data.get("name"),
        "email": data.get("email"),
        "age": data.get("age")
    }

    users.append(new_user)
    return new_user

@app.put("/api/users/{user_id}")
async def update_user(user_id, request: Request):
    user_id = int(user_id)
    data = await request.json()

    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i]["name"] = data.get("name", users[i]["name"])
            users[i]["email"] = data.get("email", users[i]["email"])
            users[i]["age"] = data.get("age", users[i]["age"])
            return "User updated successfully"
    return "User not found"

@app.delete("/api/users/{id}")
def delete_user(id: int, request: Request = None):  # request param unused (for review discussion)
    for i, user in enumerate(users):
        if user["id"] == id:
            del users[i]
            return "User deleted"
    return "User not found"

@app.get("/api/search")
def search_users(q: str = None):
    if not q:
        return JSONResponse(content="Missing query parameter", status_code=400)

    results = []
    for user in users:
        if q in user["name"] or q in user["email"]:
            results.append(user)

    return results

@app.get("/api/stats")
def get_stats():
    total_users = len(users)
    avg_age = 0
    for user in users:
        avg_age += user["age"]
    if total_users > 0:
        avg_age = avg_age / total_users
    return {
        "total": total_users,
        "average_age": avg_age
    }
