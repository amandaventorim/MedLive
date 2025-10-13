from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
import secrets
import time
from util.websocket_manager import manager
from util.auth_decorator import get_current_user, obter_usuario_logado
from data.repo.agendamento_repo import obter_agendamento_por_id, atualizar_status_agendamento


app = FastAPI()

# Gerar chave secreta (em produção, use variável de ambiente!)
SECRET_KEY = secrets.token_urlsafe(32)

# Adicionar middleware de sessão
app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=28800,  # Sessão expira em 8 horas
    same_site="lax",
    https_only=False  # Em produção, mude para True com HTTPS
)


router = APIRouter()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)

from routes import public
app.include_router(public.router)

from routes import auth_routes
app.include_router(auth_routes.router)

from routes import perfil_routes
app.include_router(perfil_routes.router)

from routes.paciente import paciente_rotas, cadastro_paciente, consulta_rotas
app.include_router(paciente_rotas.router)
app.include_router(cadastro_paciente.router)
app.include_router(consulta_rotas.router)
from routes.medico import medico_rotas, cadastro_medico
app.include_router(medico_rotas.router)
app.include_router(cadastro_medico.router)

from routes.admin import admin_rotas
app.include_router(admin_rotas.router)

# WebSocket endpoints
@app.websocket("/ws/{user_type}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_type: str, user_id: str):
    await manager.connect(websocket, user_id, user_type)
    try:
        while True:
            data = await websocket.receive_text()
            # Aqui você pode processar mensagens do cliente se necessário
            print(f"Mensagem recebida de {user_type} {user_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id, user_type)

# Endpoint para iniciar consulta
@app.post("/consulta/{agendamento_id}/iniciar")
async def iniciar_consulta(request: Request, agendamento_id: str):
    try:
        # Obter usuário atual da sessão
        current_user = obter_usuario_logado(request)
        if not current_user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Verificar se é médico
        user_type = current_user.get("tipo") or current_user.get("perfil")
        if user_type != "medico":
            raise HTTPException(status_code=403, detail="Apenas médicos podem iniciar consultas")
        
        # Buscar dados do agendamento
        agendamento = obter_agendamento_por_id(int(agendamento_id))
        if not agendamento:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        # Verificar se o médico é o responsável pela consulta
        if agendamento.idMedico != current_user.get("idUsuario"):
            raise HTTPException(status_code=403, detail="Você não tem permissão para iniciar esta consulta")
        
        # Gerar room_id único para a videoconferência
        room_id = f"consulta_{agendamento_id}_{int(time.time())}"
        
        # Atualizar status do agendamento
        atualizar_status_agendamento(int(agendamento_id), "em_andamento", room_id)
        
        # Notificar o paciente
        notification_sent = await manager.notify_patient_consultation_started(
            patient_id=str(agendamento.idPaciente),
            consultation_id=agendamento_id,
            doctor_name=current_user.get("nome"),
            room_id=room_id
        )
        
        return {
            "message": "Consulta iniciada",
            "room_id": room_id,
            "patient_notified": notification_sent,
            "agendamento_id": agendamento_id
        }
    except Exception as e:
        print(f"Erro ao iniciar consulta: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# Endpoint para entrar na sala de videoconferência (usando sala_consulta.html existente)
@app.get("/videoconferencia/{room_id}")
async def entrar_videoconferencia(request: Request, room_id: str):
    try:
        # Obter usuário atual da sessão
        current_user = obter_usuario_logado(request)
        if not current_user:
            # Redirecionar para login se não autenticado
            return RedirectResponse(url="/login", status_code=302)
        
        # Verificar se o usuário tem permissão para entrar nesta sala
        # Extrair consultation_id do room_id
        parts = room_id.split("_")
        if len(parts) >= 2 and parts[0] == "consulta":
            agendamento_id = parts[1]
            agendamento = obter_agendamento_por_id(int(agendamento_id))
            
            if agendamento:
                user_id = current_user.get("idUsuario")
                user_type = current_user.get("tipo") or current_user.get("perfil")
                
                # Verificar se é o médico ou paciente da consulta
                if (user_type == "medico" and agendamento.idMedico == user_id) or \
                   (user_type == "paciente" and agendamento.idPaciente == user_id):
                    
                    # Se for paciente entrando, notificar o médico
                    if user_type == "paciente":
                        await manager.notify_doctor_patient_joined(
                            doctor_id=str(agendamento.idMedico),
                            patient_name=current_user.get("nome"),
                            room_id=room_id
                        )
                    
                    # Buscar dados do médico e paciente para exibir na sala
                    from data.repo.medico_repo import obter_medico_por_id
                    from data.repo.paciente_repo import obter_paciente_por_id
                    
                    medico_info = obter_medico_por_id(agendamento.idMedico)
                    paciente_info = obter_paciente_por_id(agendamento.idPaciente)
                    
                    # Retornar página de videoconferência existente
                    return templates.TemplateResponse("sala_consulta.html", {
                        "request": request,
                        "room_id": room_id,
                        "user_name": current_user.get("nome"),
                        "user_type": user_type,
                        "agendamento_id": agendamento_id,
                        "agendamento": agendamento,
                        "medico": medico_info,
                        "paciente": paciente_info,
                        "usuario": current_user
                    })
        
        raise HTTPException(status_code=403, detail="Você não tem permissão para entrar nesta sala")
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de sala inválido")
    except Exception as e:
        print(f"Erro ao entrar na videoconferência: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# Endpoint API para verificar permissão na sala (usado pelo JavaScript)
@app.get("/api/videoconferencia/{room_id}")
async def verificar_sala_videoconferencia(request: Request, room_id: str):
    try:
        # Obter usuário atual da sessão
        current_user = obter_usuario_logado(request)
        if not current_user:
            raise HTTPException(status_code=401, detail="Usuário não autenticado")
        
        # Verificar se o usuário tem permissão para entrar nesta sala
        # Extrair consultation_id do room_id
        parts = room_id.split("_")
        if len(parts) >= 2 and parts[0] == "consulta":
            agendamento_id = parts[1]
            agendamento = obter_agendamento_por_id(int(agendamento_id))
            
            if agendamento:
                user_id = current_user.get("idUsuario")
                user_type = current_user.get("tipo") or current_user.get("perfil")
                
                # Verificar se é o médico ou paciente da consulta
                if (user_type == "medico" and agendamento.idMedico == user_id) or \
                   (user_type == "paciente" and agendamento.idPaciente == user_id):
                    
                    return {
                        "room_id": room_id,
                        "user_name": current_user.get("nome"),
                        "user_type": user_type,
                        "agendamento_id": agendamento_id,
                        "has_permission": True
                    }
        
        return {"has_permission": False, "message": "Você não tem permissão para entrar nesta sala"}
    except Exception as e:
        print(f"Erro ao verificar sala: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

