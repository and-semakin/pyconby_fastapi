from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal, engine

app = FastAPI()


class UserCreate(BaseModel):
    email: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).first()


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = f"insecurefakehashed-{user.password}"
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
