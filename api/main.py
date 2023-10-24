from fastapi import FastAPI

from db.connection import connect_to_database
from routers.auth import router as auth_router
from routers.model import router as model_router

connect_to_database()

app = FastAPI()

app.include_router(auth_router, prefix="/api")
app.include_router(model_router, prefix="/api/model")


@app.get("/")
def read_root():
    return {"message": "Welcome to GenL API"}
