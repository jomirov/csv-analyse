from fastapi import FastAPI
from .routers.csv_analyse import router

app = FastAPI()

app.include_router(router)