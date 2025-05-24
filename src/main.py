from fastapi import FastAPI
from .routers import router as api_router
from fastapi.staticfiles import StaticFiles
app = FastAPI(
    title="DraftFlow",
    version="1.0.0"
    )

app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
