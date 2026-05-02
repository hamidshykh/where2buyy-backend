from fastapi import FastAPI
from .routers import products, home
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
import os

app = FastAPI(title="FastAPI MySQL Example")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing only (use specific domain in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(products.router)
app.include_router(home.router)



@app.on_event("startup")
def startup():
    # Create tables if they don't exist (for quick demo). Use Alembic in prod.
    Base.metadata.create_all(bind=engine)
