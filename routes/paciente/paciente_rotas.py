from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard_paciente")
@requer_autenticacao(["paciente"])
async def get_dashboard_paciente(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/dashboard_paciente.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/cadastro_paciente")
async def get_cadastro_paciente(request: Request):
    # Rota de cadastro deve ser pública
    return templates.TemplateResponse("/paciente/cadastro_paciente.html", {
        "request": request
    })

@router.get("/perfil_paciente")
@requer_autenticacao(["paciente"])
async def get_perfil_paciente(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/perfil_paciente.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/minhas_consultas")
@requer_autenticacao(["paciente"])
async def get_minhas_consultas(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/minhas_consultas.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/buscar_medicos")
@requer_autenticacao(["paciente"])
async def get_buscar_medicos(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/buscar_medicos.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/agendar_consulta")
@requer_autenticacao(["paciente"])
async def get_agendar_consulta(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/agendar_consulta.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/pagamento")
@requer_autenticacao(["paciente"])
async def get_pagamento(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/pagamento.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/prontuario")
@requer_autenticacao(["paciente"])
async def get_prontuario(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/prontuario.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/sala_espera")
@requer_autenticacao(["paciente"])
async def get_sala_espera(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/sala_espera.html", {
        "request": request,
        "usuario": usuario_logado
    })