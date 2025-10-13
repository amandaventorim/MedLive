from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import ValidationError

from data.repo.usuario_repo import obter_usuario_por_email
from data.repo.paciente_repo import obter_id_paciente_por_usuario
from data.repo.medico_repo import obter_id_medico_por_usuario
from util.security import verificar_senha
from util.auth_decorator import criar_sessao
from dto import LoginUsuarioDTO


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(),
    senha: str = Form(),
    redirect: str = Form(None)
):
    # Guardar dados do formulário para preservar em caso de erro
    dados_formulario = {
        "email": email
    }
    
    try:
        # Validar dados com DTO
        login_dto = LoginUsuarioDTO(
            email=email,
            senha=senha
        )
        
        # Buscar usuário pelo email validado
        usuario = obter_usuario_por_email(login_dto.email)
        print(f"Usuário obtido: {usuario}")  # Debug
        
        if not usuario or not verificar_senha(login_dto.senha, usuario.senha):
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request, 
                    "erros": {"GERAL": "Credenciais inválidas!"},
                    "dados": dados_formulario
                }
            )

        usuario_dict = {
            "idUsuario": usuario.idUsuario,
            "nome": usuario.nome,
            "cpf": usuario.cpf,
            "email": usuario.email,
            "perfil": usuario.perfil,
            "tipo": usuario.perfil,  # Adicionar campo tipo para compatibilidade
            "foto": usuario.foto,
            "token_redefinicao": usuario.token_redefinicao,
            "data_token": usuario.data_token,
            "data_cadastro": usuario.data_cadastro
        }
        
        # Adicionar IDs específicos baseados no perfil
        if usuario.perfil == "paciente":
            id_paciente = obter_id_paciente_por_usuario(usuario.idUsuario)
            if id_paciente:
                usuario_dict["idPaciente"] = id_paciente
        elif usuario.perfil == "medico":
            id_medico = obter_id_medico_por_usuario(usuario.idUsuario)
            if id_medico:
                usuario_dict["idMedico"] = id_medico
        
        criar_sessao(request, usuario_dict)

        print("Redirecionando para dashboard")
        # Redirecionar conforme perfil do usuário
        if usuario.perfil == "admin":
            return RedirectResponse("/dashboard_admin", status_code=303)
        elif usuario.perfil == "medico":
            return RedirectResponse("/dashboard_medico", status_code=303)
        elif usuario.perfil == "paciente":
            return RedirectResponse("/dashboard_paciente", status_code=303)
        else:
            return RedirectResponse("/", status_code=303)
            
    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = dict()
        for erro in e.errors():
            campo = erro['loc'][0] if erro['loc'] else 'campo'
            mensagem = erro['msg']
            erros[campo.upper()] = mensagem.replace('Value error, ', '')

        # erro_msg = " | ".join(erros)
        # logger.warning(f"Erro de validação no cadastro: {erro_msg}")

        # Retornar template com dados preservados e erro
        return templates.TemplateResponse("login.html", {
            "request": request,
            "erros": erros,
            "dados": dados_formulario  # Preservar dados digitados
        })

    except Exception as e:
        # logger.error(f"Erro ao processar cadastro: {e}")

        return templates.TemplateResponse("login.html", {
            "request": request,
            "erros": {"GERAL": "Ocorreu um erro ao processar o login. Tente novamente mais tarde."},
            "dados": dados_formulario
        })

    

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)




