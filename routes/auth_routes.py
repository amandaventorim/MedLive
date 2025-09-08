from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from data.repo.usuario_repo import obter_usuario_por_email
from util.security import verificar_senha
from util.auth_decorator import criar_sessao


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    redirect: str = Form(None)
):
    usuario = obter_usuario_por_email(email)
    print(f"Usuário obtido: {usuario}")  # Debug: Verificar o usuário obtido

    if not usuario or not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "erro": "Email ou senha inválidos"}
        )

    usuario_dict = {
        "idUsuario": usuario.idUsuario,
        "nome": usuario.nome,
        "cpf": usuario.cpf,
        "email": usuario.email,
        "perfil": usuario.perfil,
        "foto": usuario.foto,
        "token_redefinicao": usuario.token_redefinicao,
        "data_token": usuario.data_token,
        "data_cadastro": usuario.data_cadastro
    }
    criar_sessao(request, usuario_dict)

    print("Redirecionando para /dashboard_paciente")
    # Redirecionar conforme perfil do usuário cadastrado
    if usuario.perfil == "admin":
        return RedirectResponse("/dashboard_admin", status_code=303)
    elif usuario.perfil == "medico":
        return RedirectResponse("/dashboard_medico", status_code=303)
    elif usuario.perfil == "paciente":
        return RedirectResponse("/dashboard_paciente", status_code=303)
    else:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "erro": "Perfil do usuário não reconhecido."}
        )
    

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)



