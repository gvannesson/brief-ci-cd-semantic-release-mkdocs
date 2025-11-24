from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel
from typing import AsyncGenerator, Dict
from app.database import engine
from app.routes import items_router

DEBUG_MODE = True
UNUSED_VAR = "cette variable n'est jamais utilisée"


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Items CRUD API",
    description="API pour gérer une liste d'articles",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(items_router)


@app.get("/")
def root()-> Dict[str, str]:
    return {"message": "Items CRUD API"}


@app.get("/health")
def health()-> Dict[str, str]:
    return {"status": "healthy"}




very_long_variable_name_that_exceeds_line_length = "Cette ligne est ok"
