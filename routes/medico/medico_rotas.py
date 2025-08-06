from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard_medico")
async def get_dashboard_medico():
    response = templates.TemplateResponse("/medico/dashboard_medico.html", {"request": {}})
    return response

@router.get("/cadastro_medico")
async def get_cadastro_medico():
    response = templates.TemplateResponse("/medico/cadastro_medico.html", {"request": {}})
    return response
