from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime
from fastapi.responses import HTMLResponse
router = APIRouter()
template = Jinja2Templates(directory="templates")

# added time just for development purpose
# "time" : datetime.utcnow().timestamp()

# User Auth Page
@router.get("/", response_class=HTMLResponse)
async def auth(req: Request):
    return template.TemplateResponse(name="auth.html", context={
                                        "request": req,
                                         "time" : datetime.utcnow().timestamp()})

# Home Page
@router.get("/home", response_class=HTMLResponse)
async def home(req: Request):
    return template.TemplateResponse(name="home.html", 
                                     context={
                                         "request": req,
                                         "time" : datetime.utcnow().timestamp()})

#Editor Page
@router.get("/editor", response_class=HTMLResponse)
async def result(req: Request):
    return template.TemplateResponse(name="editor.html", context={
                                        "request": req,
                                        "time" : datetime.utcnow().timestamp()})