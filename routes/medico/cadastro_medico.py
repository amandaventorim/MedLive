from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from data.repo.medico_repo import inserir_medico
from data.model.medico_model import Medico

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cadastro_medico")
async def get_cadastro_medico(request: Request):
    response = templates.TemplateResponse("/medico/cadastro_medico.html", {"request": request})
    return response

@router.post("/cadastro_medico")
async def cadastrar_medico(
    request: Request,
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    genero: str = Form(...),
    dataNascimento: str = Form(...),
    crm: str = Form(...),
    statusProfissional: str = Form(...)
):
    print("Recebendo dados do formulário de cadastro de médico...")
    print(f"Nome: {nome}, CPF: {cpf}, Email: {email}, Gênero: {genero}, DataNascimento: {dataNascimento}, CRM: {crm}, Status: {statusProfissional}")
    from util.security import criar_hash_senha
    senha_hash = criar_hash_senha(senha)
    print(f"Senha (hash): {senha_hash}")
    try:
        medico = Medico(
            idUsuario=None,
            idMedico=None,
            nome=nome,
            cpf=cpf,
            email=email,
            senha=senha_hash,
            genero=genero,
            dataNascimento=dataNascimento,
            perfil="medico",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crm=crm,
            statusProfissional=statusProfissional
        )
        print(f"Objeto Medico criado: {medico}")
        inserir_medico(medico)
        print("Médico inserido com sucesso no banco de dados.")
        return RedirectResponse("/login", status_code=303)
    except Exception as e:
        print("Erro ao cadastrar medico:", e)
        return templates.TemplateResponse("/medico/cadastro_medico.html", {"request": request, "erro": "Erro ao cadastrar médico: " + str(e)})
