from fastapi import FastAPI
from .routers.preview import router

app = FastAPI()

app.include_router(router)