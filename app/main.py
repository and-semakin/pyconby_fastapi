from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserCreate(BaseModel):
    email: str
    password: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"id": user_id, "email": "johndoe@example.com"}


@app.post("/users")
def create_user(user: UserCreate):
    return user
