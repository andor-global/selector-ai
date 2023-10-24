from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.connection import connect_to_database
from .routers.auth import router as auth_router
from .routers.model import router as model_router

connect_to_database()

app = FastAPI()

app.include_router(auth_router, prefix="/api")
app.include_router(model_router, prefix="/api/model")


origins = [
    "https://genl.render.com",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to GenL API"}
