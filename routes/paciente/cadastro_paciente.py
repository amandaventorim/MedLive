from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from httpx import request

from data.repo import usuario_repo
from data.repo.paciente_repo import inserir_paciente
from data.model.paciente_model import Paciente
from util.security import criar_hash_senha  # Adicione este import

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
    perfil="paciente",
    foto=None,
    token_redefinicao=None,
    data_token=None,
    data_cadastro=None,
    endereco: str = Form(...),
    convenio: str = Form(...)
):
    
     # Verificar se email já existe
    if usuario_repo.obter_usuario_por_email(email):
        return templates.TemplateResponse(
            "cadastro.html",
            {"request": request, "erro": "Email já cadastrado"}
        )
    
    # Criar hash da senha
    senha_hash = criar_hash_senha(senha)

    try:
        paciente = Paciente(
            idUsuario=None,
            idPaciente=None,
            nome=nome,
            cpf=cpf,
            email=email,
            senha=senha_hash,
            genero=genero,
            dataNascimento=dataNascimento,
            perfil="paciente",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            endereco=endereco,
            convenio=convenio
        )
        inserir_paciente(paciente)
        return RedirectResponse("/login", status_code=303)
    except Exception as e:
        print("Erro ao cadastrar paciente:", e)
        return {"detail": str(e)}