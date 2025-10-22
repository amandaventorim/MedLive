from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from util.auth_decorator import requer_autenticacao
from data.repo.especialidade_repo import (
    obter_todas_especialidades, 
    inserir_especialidade,
    obter_especialidade_por_id,
    excluir_especialidade
)
from data.repo.medico_repo import obter_todos_medicos
from data.repo.paciente_repo import obter_todos_pacientes
from data.repo.administrador_repo import obter_todos_administradores
from data.model.especialidade_model import Especialidade

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard_admin")
@requer_autenticacao(["admin"])
async def get_dashboard_admin(request: Request, usuario_logado: dict = None):
    # Buscar dados reais do banco
    especialidades = obter_todas_especialidades()
    medicos = obter_todos_medicos()
    pacientes = obter_todos_pacientes()
    administradores = obter_todos_administradores()
    
    return templates.TemplateResponse("/admin/dashboard_admin.html", {
        "request": request, 
        "usuario": usuario_logado,
        "especialidades": especialidades,
        "medicos": medicos,
        "pacientes": pacientes,
        "administradores": administradores
    })

@router.get("/cadastro_admin")
@requer_autenticacao(["admin"])
async def get_cadastro_admin(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/admin/cadastro_admin.html", {
        "request": request, 
        "usuario": usuario_logado
    })

@router.get("/perfil_admin")
@requer_autenticacao(["admin"])
async def get_perfil_admin(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/admin/perfil_admin.html", {
        "request": request, 
        "usuario": usuario_logado
    })

@router.get("/gerenciar_especialidades")
@requer_autenticacao(["admin"])
async def get_gerenciar_especialidades(request: Request, usuario_logado: dict = None):
    """Página para gerenciar especialidades médicas"""
    try:
        especialidades = obter_todas_especialidades()
        return templates.TemplateResponse("/admin/especialidades.html", {
            "request": request,
            "usuario": usuario_logado,
            "especialidades": especialidades
        })
    except Exception as e:
        print(f"Erro ao obter especialidades: {e}")
        return templates.TemplateResponse("/admin/especialidades.html", {
            "request": request,
            "usuario": usuario_logado,
            "especialidades": [],
            "erro": "Erro ao carregar especialidades"
        })

@router.post("/cadastrar_especialidade")
@requer_autenticacao(["admin"])
async def cadastrar_especialidade(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    usuario_logado: dict = None
):
    """Cadastra uma nova especialidade"""
    try:
        especialidade = Especialidade(
            idEspecialidade=None,
            nome=nome.strip(),
            descricao=descricao.strip()
        )
        
        id_inserido = inserir_especialidade(especialidade)
        
        if id_inserido:
            return RedirectResponse("/gerenciar_especialidades?success=1", status_code=303)
        else:
            return RedirectResponse("/gerenciar_especialidades?erro=1", status_code=303)
            
    except Exception as e:
        print(f"Erro ao cadastrar especialidade: {e}")
        return RedirectResponse("/gerenciar_especialidades?erro=1", status_code=303)

@router.post("/excluir_especialidade/{id_especialidade}")
@requer_autenticacao(["admin"])
async def excluir_especialidade_route(
    id_especialidade: int,
    request: Request,
    usuario_logado: dict = None
):
    """Exclui uma especialidade"""
    try:
        sucesso = excluir_especialidade(id_especialidade)
        
        if sucesso:
            return JSONResponse({"success": True, "message": "Especialidade excluída com sucesso"})
        else:
            return JSONResponse({"success": False, "message": "Erro ao excluir especialidade"}, status_code=400)
            
    except Exception as e:
        print(f"Erro ao excluir especialidade: {e}")
        return JSONResponse({"success": False, "message": str(e)}, status_code=500)
    
