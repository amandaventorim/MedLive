from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard_admin")
async def get_dashboard_admin():
    response = templates.TemplateResponse("/admin/dashboard_admin.html", {"request": {}})
    return response

@router.get("/cadastro_admin")
async def get_cadastro_admin():
    response = templates.TemplateResponse("/admin/cadastro_admin.html", {"request": {}})
    return response
    
