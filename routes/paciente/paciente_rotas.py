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