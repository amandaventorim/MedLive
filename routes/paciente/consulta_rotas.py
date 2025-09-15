from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo.agendamento_repo import inserir_agendamento
from data.model.agendamento_model import Agendamento
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/agendar_consulta")
@requer_autenticacao(["paciente"])
async def agendar_consulta_form(request: Request, usuario_logado: dict = None):
    # Renderiza o formulário de agendamento
    return templates.TemplateResponse("/paciente/agendar_consulta.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.post("/agendar_consulta")
@requer_autenticacao(["paciente"])
async def agendar_consulta(
    request: Request,
    dataAgendamento: str = Form(...),
    usuario_logado: dict = None
):
    # Cria e insere o agendamento
    agendamento = Agendamento(
        idAgendamento=None,
        idPaciente=usuario_logado["idPaciente"],
        status="pendente",
        dataAgendamento=dataAgendamento
    )
    agendamento_id = inserir_agendamento(agendamento)
    if agendamento_id:
        return RedirectResponse("/paciente/minhas_consultas", status_code=303)
    return templates.TemplateResponse("/paciente/agendar_consulta.html", {
        "request": request,
        "usuario": usuario_logado,
        "erro": "Erro ao agendar consulta. Tente novamente."
    })
