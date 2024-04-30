from fastapi import FastAPI

from src.presentation.cinema_routers import cinema_router

app = FastAPI()

app.include_router(cinema_router)
