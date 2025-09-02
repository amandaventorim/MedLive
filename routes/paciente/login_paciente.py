from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI

from data.repo.paciente_repo import obter_todos_pacientes
from data.repo.paciente_repo import obter_todos_pacientes

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Adicione SessionMiddleware à aplicação principal no main.py
# app.add_middleware(SessionMiddleware, secret_key="sua_chave_secreta")

@router.get("/login_paciente")
async def get_login_paciente(request: Request):
    return templates.TemplateResponse("/paciente/login_paciente.html", {"request": request})

@router.post("/login_paciente")
async def login_paciente(request: Request, email: str = Form(...), senha: str = Form(...)):
    pacientes = obter_todos_pacientes()
    paciente_encontrado = next((p for p in pacientes if p.email == email), None)
    if paciente_encontrado and paciente_encontrado.senha == senha:
        request.session["usuario_id"] = paciente_encontrado.idUsuario
        request.session["tipo_usuario"] = "paciente"
        return RedirectResponse("/paciente", status_code=303)
    return templates.TemplateResponse("/paciente/login_paciente.html", {"request": request, "erro": "Email ou senha inválidos ou usuário não cadastrado."})
