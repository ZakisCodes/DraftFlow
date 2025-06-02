from fastapi import FastAPI, Request
from .routers import router as api_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
app = FastAPI(
    title="DraftFlow",
    version="1.0.0"
    )

# middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Custom Middleware to Add Headers
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
#    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Resource-Policy"] = "cross-origin"
    return response

# loading the endpoints
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
