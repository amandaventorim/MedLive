from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/contato")
async def get_contato(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})

@router.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/esqueceu_senha")
async def get_esqueceu_senha(request: Request):
    return templates.TemplateResponse("esqueceu_senha.html", {"request": request})

@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse("cadastro_anterior.html", {"request": request})

@router.get("/test_verificacao")
async def get_test_verificacao(request: Request):
    return templates.TemplateResponse("test_verificacao.html", {"request": request})

