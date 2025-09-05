from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard_medico")
async def get_dashboard_medico():
    response = templates.TemplateResponse("/medico/dashboard_medico.html", {"request": {}})
    return response

@router.get("/agenda_medico")
async def get_agenda_medico():
    response = templates.TemplateResponse("/medico/agenda_medico.html", {"request": {}})
    return response

@router.get("/consultas_medico")
async def get_consultas_medico():
    response = templates.TemplateResponse("/medico/consultas_medico.html", {"request": {}})
    return response

@router.get("/pacientes_medico")
async def get_pacientes_medico():
    response = templates.TemplateResponse("/medico/pacientes_medico.html", {"request": {}})
    return response

@router.get("/perfil_medico")
async def get_perfil_medico():
    response = templates.TemplateResponse("/medico/perfil_medico.html", {"request": {}})
    return response

@router.get("/planos_medico")
async def get_planos_medico():
    response = templates.TemplateResponse("/medico/planos_medico.html", {"request": {}})
    return response

@router.get("/cadastro_medico")
async def get_cadastro_medico():
    response = templates.TemplateResponse("/medico/cadastro_medico.html", {"request": {}})
    return response

@router.get("/pagamento_plano")
async def get_pagamento_plano():
    response = templates.TemplateResponse("/medico/pagamento_plano.html", {"request": {}})
    return response

@router.get("/sala_consulta")
async def get_sala_consulta():
    response = templates.TemplateResponse("/sala_consulta.html", {"request": {}})
    return response
