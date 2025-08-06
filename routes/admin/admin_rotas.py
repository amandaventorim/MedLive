from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# tem que fazer essa pagina ainda
@router.get("/dashboard_admin")
async def get_dashboard_medico():
    response = templates.TemplateResponse("/admin/dashboard_admin.html", {"request": {}})
    return response

@router.get("/cadastro_admin")
async def get_cadastro_medico():
    response = templates.TemplateResponse("/admin/cadastro_admin.html", {"request": {}})
    return response
