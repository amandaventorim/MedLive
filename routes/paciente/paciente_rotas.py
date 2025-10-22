from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from fastapi.responses import JSONResponse
from data.repo.medico_repo import obter_todos_medicos
from data.repo.agendamento_repo import obter_agendamentos_por_paciente
from data.repo.usuario_repo import atualizar_senha_usuario, obter_usuario_por_id
from util.security import verificar_senha, criar_hash_senha

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard_paciente")
@requer_autenticacao(["paciente"])
async def get_dashboard_paciente(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/dashboard_paciente.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/cadastro_paciente")
async def get_cadastro_paciente(request: Request):
    # Rota de cadastro deve ser pública
    return templates.TemplateResponse("/paciente/cadastro_paciente.html", {
        "request": request
    })

@router.get("/perfil_paciente")
@requer_autenticacao(["paciente"])
async def get_perfil_paciente(request: Request, usuario_logado: dict = None):
    from data.repo.paciente_repo import obter_paciente_por_id
    
    # Buscar informações completas do paciente
    paciente = obter_paciente_por_id(usuario_logado["idUsuario"])
    
    return templates.TemplateResponse("/paciente/perfil_paciente.html", {
        "request": request,
        "usuario": usuario_logado,
        "paciente": paciente
    })

@router.get("/minhas_consultas")
@requer_autenticacao(["paciente"])
async def get_minhas_consultas(request: Request, sucesso: str = None, usuario_logado: dict = None):
    # Preparar mensagem de sucesso se houver
    mensagem_sucesso = None
    if sucesso == "agendamento":
        mensagem_sucesso = "Consulta agendada com sucesso! Você receberá uma confirmação em breve."
    
    # Debug: Verificar qual usuário está logado
    print(f"🔍 DEBUG - Usuário logado: ID={usuario_logado.get('idUsuario')}, Nome={usuario_logado.get('nome')}, Email={usuario_logado.get('email')}")
    
    # Buscar agendamentos do paciente logado
    consultas = []
    try:
        consultas = obter_agendamentos_por_paciente(usuario_logado["idUsuario"])
        print(f"🔍 DEBUG - Encontrados {len(consultas)} agendamentos para o paciente ID {usuario_logado['idUsuario']}")
        
        # Debug: Mostrar detalhes dos agendamentos encontrados
        for i, consulta in enumerate(consultas):
            print(f"  {i+1}. Médico: {consulta.get('nomeMedico')} | Data: {consulta.get('dataAgendamento')} | Horário: {consulta.get('horario')}")
            
    except Exception as e:
        print(f"❌ Erro ao buscar consultas do paciente {usuario_logado['idUsuario']}: {e}")
    
    return templates.TemplateResponse("/paciente/minhas_consultas.html", {
        "request": request,
        "usuario": usuario_logado,
        "mensagem_sucesso": mensagem_sucesso,
        "consultas": consultas
    })

@router.get("/buscar_medicos")
@requer_autenticacao(["paciente"])
async def get_buscar_medicos(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/buscar_medicos.html", {
        "request": request,
        "usuario": usuario_logado
    })

# Rota de agendar_consulta movida para consulta_rotas.py para evitar duplicação

@router.get("/pagamento")
@requer_autenticacao(["paciente"])
async def get_pagamento(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/pagamento.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/prontuario")
@requer_autenticacao(["paciente"])
async def get_prontuario(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/prontuario.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/sala_espera")
@requer_autenticacao(["paciente"])
async def get_sala_espera(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/paciente/sala_espera.html", {
        "request": request,
        "usuario": usuario_logado
    })

# Rota API para retornar médicos cadastrados
@router.get("/api/medicos")
async def api_medicos():
    from data.repo.medico_especialidade_repo import obter_especialidade_por_medico
    from data.repo.especialidade_repo import obter_especialidade_por_id
    
    medicos = obter_todos_medicos()
    # Retorna apenas os campos relevantes para o frontend
    medicos_dict = []
    
    for m in medicos:
        # Buscar especialidade do médico
        medico_esp = obter_especialidade_por_medico(m.idMedico)
        especialidade_nome = ""
        
        if medico_esp:
            especialidade = obter_especialidade_por_id(medico_esp.idEspecialidade)
            if especialidade:
                especialidade_nome = especialidade.nome
        
        medicos_dict.append({
            "id": m.idMedico,
            "name": m.nome,
            "specialty": especialidade_nome or "Não especificada",
            "crm": m.crm,
            "experience": getattr(m, "statusProfissional", ""),
            "email": m.email,
            "rating": 4.5,  # Valor padrão
            "reviews": 0,  # Valor padrão
            "price": "R$ 150,00",  # Valor padrão
            "availability": "Disponível"  # Valor padrão
        })
    
    return JSONResponse(content=medicos_dict)

@router.post("/alterar_senha")
@requer_autenticacao(["paciente"])
async def alterar_senha_paciente(
    request: Request,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    confirmar_senha: str = Form(...),
    usuario_logado: dict = None
):
    """
    Altera a senha do paciente logado
    """
    try:
        # Validações básicas
        if not senha_atual or not nova_senha or not confirmar_senha:
            return JSONResponse(
                status_code=400,
                content={"sucesso": False, "erro": "Todos os campos são obrigatórios"}
            )
        
        if nova_senha != confirmar_senha:
            return JSONResponse(
                status_code=400,
                content={"sucesso": False, "erro": "Nova senha e confirmação não coincidem"}
            )
        
        if len(nova_senha) < 6:
            return JSONResponse(
                status_code=400,
                content={"sucesso": False, "erro": "Nova senha deve ter pelo menos 6 caracteres"}
            )
        
        # Buscar usuário atual no banco
        usuario_db = obter_usuario_por_id(usuario_logado["idUsuario"])
        if not usuario_db:
            return JSONResponse(
                status_code=404,
                content={"sucesso": False, "erro": "Usuário não encontrado"}
            )
        
        # Verificar se a senha atual está correta
        if not verificar_senha(senha_atual, usuario_db.senha):
            return JSONResponse(
                status_code=400,
                content={"sucesso": False, "erro": "Senha atual incorreta"}
            )
        
        # Criar hash da nova senha
        nova_senha_hash = criar_hash_senha(nova_senha)
        
        # Atualizar senha no banco
        sucesso = atualizar_senha_usuario(usuario_logado["idUsuario"], nova_senha_hash)
        
        if sucesso:
            return JSONResponse(
                status_code=200,
                content={"sucesso": True, "mensagem": "Senha alterada com sucesso!"}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"sucesso": False, "erro": "Erro interno ao alterar senha"}
            )
            
    except Exception as e:
        print(f"❌ Erro ao alterar senha: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"sucesso": False, "erro": "Erro interno do servidor"}
        )