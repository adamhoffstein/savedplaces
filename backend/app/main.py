from fastapi import FastAPI
from app.routes import (
    nearby,
)
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nearby.router, prefix="/nearby", tags=["nearby"])
