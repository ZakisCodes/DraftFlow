from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime
router = APIRouter()
template = Jinja2Templates(directory="templates")


# added time just for development purpose
# "time" : datetime.utcnow().timestamp()

@router.get("/home")
async def home(req: Request):
    return template.TemplateResponse(name="home.html", 
                                     context={
                                         "request": req,
                                         "time" : datetime.utcnow().timestamp()})

@router.get("/editor")
async def result(req: Request):
    return template.TemplateResponse(name="editor.html", context={
                                        "request": req,
                                        "time" : datetime.utcnow().timestamp()})

@router.get("/")
async def auth(req: Request):
    return template.TemplateResponse(name="auth.html", context={
                                        "request": req,
                                         "time" : datetime.utcnow().timestamp()})

