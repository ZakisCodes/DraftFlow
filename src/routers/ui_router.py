from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
template = Jinja2Templates(directory="templates")

@router.get("/")
async def home(req: Request):
    return template.TemplateResponse(name="home.html", context={"request": req})

@router.get("/editor")
async def result(req: Request):
    return template.TemplateResponse(name="editor.html", context={"request": req})

@router.get("/auth")
async def auth(req: Request):
    return template.TemplateResponse(name="auth.html", context={"request": req})