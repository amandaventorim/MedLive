from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from util.auth_decorator import get_current_user
from data.repo.notificacao_repo import (
    obter_notificacoes_por_usuario,
    obter_notificacoes_nao_lidas,
    contar_notificacoes_nao_lidas,
    marcar_notificacao_como_lida,
    marcar_todas_notificacoes_como_lidas,
    deletar_notificacao,
    obter_notificacao_por_id,
    criar_notificacao_resposta_confirmacao
)
from data.repo.agendamento_repo import obter_agendamento_por_id
from data.repo.medico_repo import obter_medico_por_id
from data.repo.paciente_repo import obter_paciente_por_id
from util.websocket_manager import manager
import json
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()


class ConfirmPresenceRequest(BaseModel):
    notification_id: int
    confirmed: bool


class MarkAsReadRequest(BaseModel):
    user_id: int
    user_type: str


@router.get("/api/notifications/{user_type}/{user_id}")
async def get_notifications(
    user_type: str, 
    user_id: int, 
    request: Request,
    current_user=Depends(get_current_user)
):
    """Obtém todas as notificações de um usuário"""
    try:
        # Verificar se o usuário pode acessar essas notificações
        if str(current_user.get("idUsuario")) != str(user_id):
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        if user_type not in ["medico", "paciente"]:
            raise HTTPException(status_code=400, detail="Tipo de usuário inválido")
        
        # Buscar notificações
        notifications = obter_notificacoes_por_usuario(user_id, user_type, limite=20)
        unread_count = contar_notificacoes_nao_lidas(user_id, user_type)
        
        # Converter para formato JSON
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                "idNotificacao": notification.idNotificacao,
                "idUsuario": notification.idUsuario,
                "tipoUsuario": notification.tipoUsuario,
                "tipo": notification.tipo,
                "titulo": notification.titulo,
                "mensagem": notification.mensagem,
                "lida": notification.lida,
                "dataInclusao": notification.dataInclusao,
                "dadosAdicionais": notification.dadosAdicionais,
                "acaoRequerida": notification.acaoRequerida,
                "expiresAt": notification.expiresAt
            })
        
        return JSONResponse({
            "notifications": notifications_data,
            "unread_count": unread_count
        })
        
    except Exception as e:
        print(f"Erro ao buscar notificações: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.post("/api/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    request_data: MarkAsReadRequest,
    current_user=Depends(get_current_user)
):
    """Marca uma notificação específica como lida"""
    try:
        # Verificar se o usuário pode marcar esta notificação
        if str(current_user.get("idUsuario")) != str(request_data.user_id):
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Marcar como lida
        success = marcar_notificacao_como_lida(
            notification_id, 
            request_data.user_id, 
            request_data.user_type
        )
        
        if success:
            return JSONResponse({"message": "Notificação marcada como lida"})
        else:
            raise HTTPException(status_code=404, detail="Notificação não encontrada")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao marcar notificação como lida: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.post("/api/notifications/{user_type}/{user_id}/mark-all-read")
async def mark_all_notifications_read(
    user_type: str,
    user_id: int,
    current_user=Depends(get_current_user)
):
    """Marca todas as notificações de um usuário como lidas"""
    try:
        # Verificar se o usuário pode marcar estas notificações
        if str(current_user.get("idUsuario")) != str(user_id):
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        if user_type not in ["medico", "paciente"]:
            raise HTTPException(status_code=400, detail="Tipo de usuário inválido")
        
        # Marcar todas como lidas
        success = marcar_todas_notificacoes_como_lidas(user_id, user_type)
        
        if success:
            return JSONResponse({"message": "Todas as notificações foram marcadas como lidas"})
        else:
            raise HTTPException(status_code=500, detail="Erro ao marcar notificações")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao marcar todas as notificações como lidas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.delete("/api/notifications/{notification_id}")
async def delete_notification(
    notification_id: int,
    user_id: int,
    user_type: str,
    current_user=Depends(get_current_user)
):
    """Deleta uma notificação específica"""
    try:
        # Verificar se o usuário pode deletar esta notificação
        if str(current_user.get("idUsuario")) != str(user_id):
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        # Deletar notificação
        success = deletar_notificacao(notification_id, user_id, user_type)
        
        if success:
            return JSONResponse({"message": "Notificação removida"})
        else:
            raise HTTPException(status_code=404, detail="Notificação não encontrada")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao deletar notificação: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.post("/api/confirm-presence")
async def confirm_presence(
    request_data: ConfirmPresenceRequest,
    current_user=Depends(get_current_user)
):
    """Confirma presença do paciente e notifica o médico"""
    try:
        # Buscar a notificação
        notification = obter_notificacao_por_id(
            request_data.notification_id,
            current_user.get("idUsuario"),
            "paciente"
        )
        
        if not notification or notification.tipo != "confirmacao_consulta":
            raise HTTPException(status_code=404, detail="Notificação não encontrada")
        
        # Extrair dados da notificação
        dados_adicionais = json.loads(notification.dadosAdicionais or '{}')
        agendamento_id = dados_adicionais.get("agendamento_id")
        nome_medico = dados_adicionais.get("nome_medico")
        data_consulta = dados_adicionais.get("data_consulta")
        horario = dados_adicionais.get("horario")
        
        if not agendamento_id:
            raise HTTPException(status_code=400, detail="Dados da consulta não encontrados")
        
        # Buscar informações do agendamento
        agendamento = obter_agendamento_por_id(agendamento_id)
        if not agendamento:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado")
        
        # Buscar informações do paciente
        paciente = obter_paciente_por_id(current_user.get("idUsuario"))
        if not paciente:
            raise HTTPException(status_code=404, detail="Paciente não encontrado")
        
        # Criar notificação para o médico
        criar_notificacao_resposta_confirmacao(
            id_medico=agendamento.idMedico,
            nome_paciente=paciente.nome,
            confirmou=request_data.confirmed,
            data_consulta=data_consulta,
            horario=horario,
            agendamento_id=agendamento_id
        )
        
        # Enviar notificação em tempo real para o médico
        notification_message = {
            "type": "resposta_confirmacao",
            "titulo": f"Paciente {'CONFIRMOU' if request_data.confirmed else 'NÃO CONFIRMOU'} Presença",
            "mensagem": f"{paciente.nome} {'confirmou' if request_data.confirmed else 'não confirmou'} presença para consulta de {data_consulta} às {horario}",
            "paciente": paciente.nome,
            "confirmou": request_data.confirmed,
            "data_consulta": data_consulta,
            "horario": horario,
            "timestamp": datetime.now().isoformat(),
            "persistent": True
        }
        
        await manager.send_notification(
            str(agendamento.idMedico), 
            "medico", 
            notification_message
        )
        
        # Marcar a notificação de confirmação como lida
        marcar_notificacao_como_lida(
            request_data.notification_id,
            current_user.get("idUsuario"),
            "paciente"
        )
        
        return JSONResponse({
            "message": "Confirmação enviada com sucesso",
            "confirmed": request_data.confirmed
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao confirmar presença: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")