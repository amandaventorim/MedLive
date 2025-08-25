from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard_paciente")
async def get_dashboard_paciente():
    response = templates.TemplateResponse("/paciente/dashboard_paciente.html", {"request": {}})
    return response

@router.get("/cadastro_paciente")
async def get_cadastro_paciente():
    response = templates.TemplateResponse("/paciente/cadastro_paciente.html", {"request": {}})
    return response

@router.get("/perfil_paciente")
async def get_perfil_paciente():
    response = templates.TemplateResponse("/paciente/perfil_paciente.html", {"request": {}})
    return response

@router.get("/minhas_consultas")
async def get_minhas_consultas():
    response = templates.TemplateResponse("/paciente/minhas_consultas.html", {"request": {}})
    return response

@router.get("/buscar_medicos")
async def get_buscar_medicos():
    response = templates.TemplateResponse("/paciente/buscar_medicos.html", {"request": {}})
    return response

@router.get("/agendar_consulta")
async def get_agendar_consulta():
    response = templates.TemplateResponse("/paciente/agendar_consulta.html", {"request": {}})
    return response

@router.get("/pagamento")
async def get_pagamento():
    response = templates.TemplateResponse("/paciente/pagamento.html", {"request": {}})
    return response

@router.get("/prontuario")
async def get_prontuario():
    response = templates.TemplateResponse("/paciente/prontuario.html", {"request": {}})
    return response

@router.get("/sala_espera")
async def get_sala_espera():
    response = templates.TemplateResponse("/paciente/sala_espera.html", {"request": {}})
    return response