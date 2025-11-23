from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import ValidationError
import random
from datetime import datetime, timedelta

from data.repo import usuario_repo
from data.repo.paciente_repo import inserir_paciente
from data.model.paciente_model import Paciente
from util.security import criar_hash_senha
from util.validacoes_dto import ValidacaoError
from util.email_service import email_service
from dto import CriarPacienteDTO

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Armazenamento temporário de códigos de verificação (em produção, use Redis ou banco)
verification_codes = {}

@router.get("/cadastro_paciente")
async def get_cadastro_paciente(request: Request):
    response = templates.TemplateResponse("/paciente/cadastro_paciente.html", {"request": request})
    return response

@router.post("/gerar_codigo_verificacao")
async def gerar_codigo_verificacao(request: Request):
    """Gera um código de verificação de 6 dígitos e envia por email"""
    try:
        data = await request.json()
        email = data.get("email")
        nome = data.get("nome", "Usuário")
        
        if not email:
            return JSONResponse({"success": False, "message": "Email não fornecido"}, status_code=400)
        
        # Gerar código de 6 dígitos
        codigo = str(random.randint(100000, 999999))
        
        # Armazenar código com timestamp (expira em 5 minutos)
        expiracao = datetime.now() + timedelta(minutes=5)
        verification_codes[email] = {
            "codigo": codigo,
            "expiracao": expiracao,
            "tentativas": 0
        }
        
        print(f"[VERIFICAÇÃO] Código gerado para {email}: {codigo}")
        
        # Enviar email com o código
        try:
            email_enviado = email_service.enviar_codigo_verificacao(
                para_email=email,
                para_nome=nome,
                codigo=codigo
            )
            
            if email_enviado:
                return JSONResponse({
                    "success": True,
                    "message": "Código de verificação enviado para seu email"
                })
            else:
                # Se falhar no envio, remover código gerado
                del verification_codes[email]
                return JSONResponse({
                    "success": False,
                    "message": "Erro ao enviar email. Verifique seu endereço de email e tente novamente."
                }, status_code=500)
                
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            # Se falhar no envio, remover código gerado
            if email in verification_codes:
                del verification_codes[email]
            return JSONResponse({
                "success": False,
                "message": "Erro ao enviar email de verificação. Tente novamente."
            }, status_code=500)
        
    except Exception as e:
        print(f"Erro ao gerar código: {e}")
        return JSONResponse({"success": False, "message": "Erro ao gerar código"}, status_code=500)

@router.post("/verificar_codigo")
async def verificar_codigo(request: Request):
    """Verifica se o código de verificação está correto"""
    try:
        data = await request.json()
        email = data.get("email")
        codigo = data.get("codigo")
        
        if not email or not codigo:
            return JSONResponse({"success": False, "message": "Email ou código não fornecido"}, status_code=400)
        
        # Verificar se existe código para este email
        if email not in verification_codes:
            return JSONResponse({"success": False, "message": "Código não encontrado ou expirado"}, status_code=400)
        
        dados_verificacao = verification_codes[email]
        
        # Verificar se o código expirou
        if datetime.now() > dados_verificacao["expiracao"]:
            del verification_codes[email]
            return JSONResponse({"success": False, "message": "Código expirado. Solicite um novo código"}, status_code=400)
        
        # Verificar número de tentativas (máximo 5)
        if dados_verificacao["tentativas"] >= 5:
            del verification_codes[email]
            return JSONResponse({"success": False, "message": "Número máximo de tentativas excedido"}, status_code=400)
        
        # Verificar se o código está correto
        if dados_verificacao["codigo"] == codigo:
            # Código correto - limpar da memória
            del verification_codes[email]
            return JSONResponse({"success": True, "message": "Email verificado com sucesso!"})
        else:
            # Código incorreto - incrementar tentativas
            verification_codes[email]["tentativas"] += 1
            tentativas_restantes = 5 - verification_codes[email]["tentativas"]
            return JSONResponse({
                "success": False,
                "message": f"Código incorreto. Você tem {tentativas_restantes} tentativa(s) restante(s)"
            }, status_code=400)
        
    except Exception as e:
        print(f"Erro ao verificar código: {e}")
        return JSONResponse({"success": False, "message": "Erro ao verificar código"}, status_code=500)

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
        
        # Validar se email e CPF já existem usando funções de validação
        from util.validacoes_dto import validar_duplicatas_usuario
        validar_duplicatas_usuario(str(paciente_dto.email), paciente_dto.cpf)
        
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
            campo_upper = campo.upper()
            mensagem_limpa = mensagem.replace('Value error, ', '')
            erros[campo_upper] = mensagem_limpa
            print(f"DEBUG: Erro - Campo: '{campo}' -> '{campo_upper}', Mensagem: '{mensagem_limpa}'")
        
        print(f"DEBUG: Dicionário de erros final: {erros}")
        
        # Retornar template com dados preservados e erro
        return templates.TemplateResponse("/paciente/cadastro_paciente.html", {
            "request": request,
            "erros": erros,
            "dados": dados_formulario  # Preservar dados digitados
        })
        
    except (ValueError, ValidacaoError) as e:
        # Erro de validação de duplicatas (email ou CPF já cadastrados)
        print(f"DEBUG: Erro de duplicata: {str(e)}")
        return templates.TemplateResponse("/paciente/cadastro_paciente.html", {
            "request": request,
            "erros": {"GERAL": str(e)},
            "dados": dados_formulario
        })
        
    except Exception as e:
        # Erro geral
        print("Erro ao cadastrar paciente:", e)
        return templates.TemplateResponse("/paciente/cadastro_paciente.html", {
            "request": request,
            "erros": {"GERAL": "Erro ao processar cadastro. Tente novamente."},
            "dados": dados_formulario
        })