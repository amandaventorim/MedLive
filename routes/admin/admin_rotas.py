from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard_admin")
@requer_autenticacao(["admin"])
async def get_dashboard_admin(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/admin/dashboard_admin.html", {
        "request": request, 
        "usuario": usuario_logado
    })

@router.get("/cadastro_admin")
@requer_autenticacao(["admin"])
async def get_cadastro_admin(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/admin/cadastro_admin.html", {
        "request": request, 
        "usuario": usuario_logado
    })

@router.get("/perfil_admin")
@requer_autenticacao(["admin"])
async def get_perfil_admin(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/admin/perfil_admin.html", {
        "request": request, 
        "usuario": usuario_logado
    })
    
