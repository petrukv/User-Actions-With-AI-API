from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import models
from app.db.postgres_connection import engine
from app.routes import user_routes
from app.auth import authentication


app = FastAPI()
app.include_router(user_routes.router)
app.include_router(authentication.router)



origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(engine)