from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard_medico")
@requer_autenticacao(["medico"])
async def get_dashboard_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/dashboard_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/agenda_medico")
@requer_autenticacao(["medico"])
async def get_agenda_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/agenda_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/consultas_medico")
@requer_autenticacao(["medico"])
async def get_consultas_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/consultas_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/pacientes_medico")
@requer_autenticacao(["medico"])
async def get_pacientes_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/pacientes_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/perfil_medico")
@requer_autenticacao(["medico"])
async def get_perfil_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/perfil_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/planos_medico")
@requer_autenticacao(["medico"])
async def get_planos_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/planos_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/cadastro_medico")
async def get_cadastro_medico(request: Request):
    # Rota de cadastro deve ser pública
    return templates.TemplateResponse("/medico/cadastro_medico.html", {
        "request": request
    })

@router.get("/pagamento_plano")
async def get_pagamento_plano(request: Request):
    # Rota de pagamento pode ser pública para permitir cadastro
    return templates.TemplateResponse("/medico/pagamento_plano.html", {
        "request": request
    })

@router.get("/sala_consulta")
@requer_autenticacao(["medico", "paciente"])
async def get_sala_consulta(request: Request, usuario_logado: dict = None):
    # Sala de consulta acessível para médicos e pacientes
    return templates.TemplateResponse("/sala_consulta.html", {
        "request": request,
        "usuario": usuario_logado
    })
