from fastapi import FastAPI
from app.routes import nearby, users, auth, places, placelists
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

app.include_router(
    placelists.router, prefix="/placelists", tags=["placelists"]
)
app.include_router(nearby.router, prefix="/nearby", tags=["nearby"])
app.include_router(places.router, prefix="/places", tags=["places"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
