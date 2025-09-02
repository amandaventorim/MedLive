from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from data.repo.paciente_repo import inserir_paciente
from data.model.paciente_model import Paciente  # Adicione este import

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cadastro_paciente")
async def get_cadastro_paciente(request: Request):
    response = templates.TemplateResponse("/paciente/cadastro_paciente.html", {"request": request})
    return response

@router.post("/cadastro_paciente")
async def cadastrar_paciente(
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    genero: str = Form(...),
    dataNascimento: str = Form(...),
    endereco: str = Form(...),
    convenio: str = Form(...)
):
    try:
        paciente = Paciente(
            idUsuario=None,
            idPaciente=None,
            nome=nome,
            cpf=cpf,
            email=email,
            senha=senha,
            genero=genero,
            dataNascimento=dataNascimento,
            endereco=endereco,
            convenio=convenio
        )
        inserir_paciente(paciente)
        return RedirectResponse("/login", status_code=303)
    except Exception as e:
        print("Erro ao cadastrar paciente:", e)
        return {"detail": str(e)}