from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

_users: dict[int, dict] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob",   "email": "bob@example.com"},
}
_next_id = 3


class UserCreate(BaseModel):
    name: str
    email: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


@router.get("/")
def list_users():
    return list(_users.values())


@router.get("/{user_id}")
def get_user(user_id: int):
    user = _users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", status_code=201)
def create_user(body: UserCreate):
    global _next_id
    user = {"id": _next_id, "name": body.name, "email": body.email}
    _users[_next_id] = user
    _next_id += 1
    return user


@router.put("/{user_id}")
def update_user(user_id: int, body: UserUpdate):
    user = _users.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if body.name is not None:
        user["name"] = body.name
    if body.email is not None:
        user["email"] = body.email
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in _users:
        raise HTTPException(status_code=404, detail="User not found")
    del _users[user_id]
