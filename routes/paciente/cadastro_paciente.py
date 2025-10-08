from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from data.repo import usuario_repo
from data.repo.paciente_repo import inserir_paciente
from data.model.paciente_model import Paciente
from util.security import criar_hash_senha
from dto import CriarPacienteDTO

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cadastro_paciente")
async def get_cadastro_paciente(request: Request):
    response = templates.TemplateResponse("/paciente/cadastro_paciente.html", {"request": request})
    return response

@router.post("/cadastro_paciente")
async def cadastrar_paciente(
    request: Request,
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    genero: str = Form(...),
    dataNascimento: str = Form(...),
    endereco: str = Form(...),
    convenio: str = Form(...)
):
    # Guardar os dados originais do formulário para preservar em caso de erro
    dados_formulario = {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "genero": genero,
        "dataNascimento": dataNascimento,
        "endereco": endereco,
        "convenio": convenio
    }
    
    try:
        print(f"DEBUG: Tentando validar dados - Nome: {nome}, CPF: {cpf}, Email: {email}")
        
        # Validar dados com DTO
        paciente_dto = CriarPacienteDTO(
            nome=nome,
            cpf=cpf,
            email=email,
            senha=senha,
            genero=genero,
            dataNascimento=dataNascimento,
            endereco=endereco,
            convenio=convenio
        )
        
        print(f"DEBUG: DTO criado com sucesso - Nome validado: {paciente_dto.nome}")
        
        # Verificar se email já existe
        if usuario_repo.obter_usuario_por_email(paciente_dto.email):
            print(f"DEBUG: Email já existe no banco: {paciente_dto.email}")
            return templates.TemplateResponse(
                "/paciente/cadastro_paciente.html",
                {
                    "request": request, 
                    "erro": "Email já cadastrado",
                    "dados": dados_formulario
                }
            )
        
        # Criar hash da senha
        senha_hash = criar_hash_senha(paciente_dto.senha)

        # Criar objeto Paciente usando dados validados do DTO
        paciente = Paciente(
            idUsuario=None,
            idPaciente=None,
            nome=paciente_dto.nome,
            cpf=paciente_dto.cpf,
            email=paciente_dto.email,
            senha=senha_hash,
            genero=paciente_dto.genero,
            dataNascimento=paciente_dto.dataNascimento,
            perfil="paciente",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            endereco=paciente_dto.endereco,
            convenio=paciente_dto.convenio
        )
        
        # Processar cadastro
        print(f"DEBUG: Inserindo paciente no banco de dados")
        inserir_paciente(paciente)
        print(f"DEBUG: Paciente inserido com sucesso!")
        
        # Sucesso - Redirecionar
        return RedirectResponse("/login", status_code=303)
        
    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = dict()
        for erro in e.errors():
            # Pegar apenas a mensagem customizada, removendo prefixos do Pydantic
            campo = erro['loc'][0] if erro['loc'] else 'campo'
            mensagem = erro['msg']
            erros[campo.upper()] = mensagem.replace('Value error, ', '')
            # Se a mensagem começa com "Value error, ", remove esse prefixo
        #     if mensagem.startswith("Value error, "):
        #         mensagem = mensagem.replace("Value error, ", "")
        #     erros.append(mensagem)
        # erro_msg = " | ".join(erros)
        
        # Retornar template com dados preservados e erro
        return templates.TemplateResponse("/medico/cadastro_medico.html", {
            "request": request,
            "erros": erros,
            "dados": dados_formulario  # Preservar dados digitados
        })
        
    except Exception as e:
        # Erro geral
        print("Erro ao cadastrar paciente:", e)
        return templates.TemplateResponse("/paciente/cadastro_paciente.html", {
            "request": request,
            "erros": "Erro ao processar cadastro. Tente novamente.",
            "dados": dados_formulario
        })