from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from data.repo.medico_repo import inserir_medico
from data.repo import usuario_repo
from data.model.medico_model import Medico
from util.security import criar_hash_senha
from util.validacoes_dto import ValidacaoError
from dto import CriarMedicoDTO

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
    # Guardar os dados originais do formulário para preservar em caso de erro
    dados_formulario = {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "genero": genero,
        "dataNascimento": dataNascimento,
        "crm": crm,
        "statusProfissional": statusProfissional
    }
    
    print("Recebendo dados do formulário de cadastro de médico...")
    print(f"Nome: {nome}, CPF: {cpf}, Email: {email}, CRM: {crm}")
    
    try:
        # Validar dados com DTO
        medico_dto = CriarMedicoDTO(
            nome=nome,
            cpf=cpf,
            email=email,
            senha=senha,
            genero=genero,
            dataNascimento=dataNascimento,
            crm=crm,
            statusProfissional=statusProfissional
        )
        
        print(f"DEBUG: DTO criado com sucesso - Nome validado: {medico_dto.nome}")
        
        # Validar se email e CPF já existem usando funções de validação
        from util.validacoes_dto import validar_duplicatas_usuario
        validar_duplicatas_usuario(str(medico_dto.email), medico_dto.cpf)
        
        # Criar hash da senha
        senha_hash = criar_hash_senha(medico_dto.senha)
        print(f"Senha (hash): {senha_hash}")
        
        # Criar objeto Medico usando dados validados do DTO
        medico = Medico(
            idUsuario=None,
            idMedico=None,
            nome=medico_dto.nome,
            cpf=medico_dto.cpf,
            email=medico_dto.email,
            senha=senha_hash,
            genero=medico_dto.genero,
            dataNascimento=medico_dto.dataNascimento,
            perfil="medico",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
            crm=medico_dto.crm,
            statusProfissional=medico_dto.statusProfissional
        )
        
        # Processar cadastro
        print(f"Objeto Medico criado: {medico}")
        inserir_medico(medico)
        print("Médico inserido com sucesso no banco de dados.")
        
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
        
    except (ValueError, ValidacaoError) as e:
        # Erro de validação de duplicatas (email ou CPF já cadastrados)
        print(f"DEBUG: Erro de duplicata: {str(e)}")
        return templates.TemplateResponse("/medico/cadastro_medico.html", {
            "request": request,
            "erros": {"GERAL": str(e)},
            "dados": dados_formulario
        })
        
    except Exception as e:
        # Erro geral
        print("Erro ao cadastrar medico:", e)
        return templates.TemplateResponse("/medico/cadastro_medico.html", {
            "request": request,
            "erros": "Erro ao cadastrar médico: " + str(e),
            "dados": dados_formulario
        })
