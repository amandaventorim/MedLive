from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from data.repo.usuario_repo import obter_usuario_por_email

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def post_login(request: Request, response: Response, email: str = Form(...), senha: str = Form(...)):
    usuario = obter_usuario_por_email(email)

    if usuario and usuario.senha == senha:
        request.session["usuario_id"] = usuario.idUsuario
        request.session["tipo_usuario"] = "paciente" # Assumindo que é paciente por enquanto
        return RedirectResponse(url="/dashboard_paciente", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "erro": "Email ou senha inválidos."})
