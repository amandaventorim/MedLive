from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root():
    response = templates.TemplateResponse("index.html", {"request": {}})
    return response

@router.get("/contato")
async def get_contato():
    response = templates.TemplateResponse("contato.html", {"request": {}})
    return response

@router.get("/login")
async def get_login():
    response = templates.TemplateResponse("login.html", {"request": {}})
    return response

@router.get("/cadastro")
async def get_cadastro():
    response = templates.TemplateResponse("cadastro_anterior.html", {"request": {}})
    return response

