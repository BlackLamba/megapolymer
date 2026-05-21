from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.generation import router as generation_router

from app.db.base import Base
from app.db.session import engine

from app.models.user import User
from app.models.experiment import Experiment
from app.models.molecule import Molecule
from app.api.experiments import router as experiments_router
from app.api.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Polymer Platform API")

# CORS (чтобы React мог обращаться)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(generation_router)
app.include_router(experiments_router)


@app.get("/")
def root():
    return {"status": "ok"}