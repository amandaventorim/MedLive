from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio
import time
from datetime import datetime, timedelta

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.user_connections: Dict[str, WebSocket] = {}
        # Adicionar controle de salas de videoconferência
        self.video_rooms: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str, user_type: str):
        await websocket.accept()
        key = f"{user_type}_{user_id}"
        self.user_connections[key] = websocket
        print(f"Usuario {user_type} {user_id} conectado via WebSocket")

    async def join_video_room(self, websocket: WebSocket, room_id: str, user_id: str, user_type: str):
        """Conecta um usuário a uma sala de videoconferência"""
        print(f"[DEBUG] Tentando conectar {user_type} {user_id} na sala {room_id}")
        
        if room_id not in self.video_rooms:
            self.video_rooms[room_id] = {}
            print(f"[DEBUG] Sala {room_id} criada")
        
        user_key = f"{user_type}_{user_id}"
        self.video_rooms[room_id][user_key] = websocket
        
        print(f"[DEBUG] Usuários já na sala {room_id}: {list(self.video_rooms[room_id].keys())}")
        
        # Notificar outros usuários na sala
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user_id": user_id,
            "user_type": user_type,
            "room_id": room_id
        }, exclude_user=user_key)
        
        # Enviar lista de usuários já na sala para o novo usuário
        room_users = []
        for existing_user in self.video_rooms[room_id]:
            if existing_user != user_key:
                parts = existing_user.split("_", 1)
                if len(parts) == 2:
                    room_users.append({
                        "user_type": parts[0],
                        "user_id": parts[1]
                    })
        
        await websocket.send_text(json.dumps({
            "type": "room_users",
            "users": room_users,
            "room_id": room_id
        }))
        
        print(f"[DEBUG] Usuario {user_type} {user_id} entrou na sala {room_id}. Total na sala: {len(self.video_rooms[room_id])}")
        print(f"[DEBUG] Estado atual das salas: {dict((k, list(v.keys())) for k, v in self.video_rooms.items())}")

    async def join_video_room_already_connected(self, websocket: WebSocket, room_id: str, user_id: str, user_type: str):
        """Conecta um usuário a uma sala de videoconferência (WebSocket já aceito)"""
        print(f"[DEBUG] Tentando conectar {user_type} {user_id} na sala {room_id} (WebSocket já aceito)")
        
        if room_id not in self.video_rooms:
            self.video_rooms[room_id] = {}
            print(f"[DEBUG] Sala {room_id} criada")
        
        user_key = f"{user_type}_{user_id}"
        self.video_rooms[room_id][user_key] = websocket
        
        print(f"[DEBUG] Usuários já na sala {room_id}: {list(self.video_rooms[room_id].keys())}")
        
        # Notificar outros usuários na sala
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user_id": user_id,
            "user_type": user_type,
            "room_id": room_id
        }, exclude_user=user_key)
        
        # Enviar lista de usuários já na sala para o novo usuário
        room_users = []
        for existing_user in self.video_rooms[room_id]:
            if existing_user != user_key:
                parts = existing_user.split("_", 1)
                if len(parts) == 2:
                    room_users.append({
                        "user_type": parts[0],
                        "user_id": parts[1]
                    })
        
        await websocket.send_text(json.dumps({
            "type": "room_users",
            "users": room_users,
            "room_id": room_id
        }))
        
        print(f"[DEBUG] Usuario {user_type} {user_id} entrou na sala {room_id}. Total na sala: {len(self.video_rooms[room_id])}")
        print(f"[DEBUG] Estado atual das salas: {dict((k, list(v.keys())) for k, v in self.video_rooms.items())}")

    async def leave_video_room(self, room_id: str, user_id: str, user_type: str):
        """Remove um usuário de uma sala de videoconferência"""
        if room_id in self.video_rooms:
            user_key = f"{user_type}_{user_id}"
            if user_key in self.video_rooms[room_id]:
                del self.video_rooms[room_id][user_key]
                
                # Notificar outros usuários
                await self.broadcast_to_room(room_id, {
                    "type": "user_left",
                    "user_id": user_id,
                    "user_type": user_type,
                    "room_id": room_id
                })
                
                # Remover sala se vazia (verificar se ainda existe)
                if room_id in self.video_rooms and not self.video_rooms[room_id]:
                    del self.video_rooms[room_id]
                
                print(f"Usuario {user_type} {user_id} saiu da sala {room_id}")

    async def broadcast_to_room(self, room_id: str, message: dict, exclude_user: str = None):
        """Envia mensagem para todos os usuários em uma sala"""
        if room_id in self.video_rooms:
            # Coletar conexões inválidas para remover depois
            invalid_connections = []
            
            for user_key, websocket in self.video_rooms[room_id].items():
                if user_key != exclude_user:
                    try:
                        await websocket.send_text(json.dumps(message))
                    except Exception as e:
                        print(f"Erro ao enviar mensagem para {user_key}: {e}")
                        # Marcar conexão como inválida
                        invalid_connections.append(user_key)
            
            # Remover conexões inválidas após o loop
            for user_key in invalid_connections:
                if user_key in self.video_rooms[room_id]:
                    del self.video_rooms[room_id][user_key]
                    print(f"Conexão inválida removida: {user_key}")
            
            # Remover sala se ficou vazia
            if not self.video_rooms[room_id]:
                del self.video_rooms[room_id]
                print(f"Sala vazia removida: {room_id}")

    async def forward_webrtc_signal(self, room_id: str, sender_user: str, target_user: str, signal_data: dict):
        """Encaminha sinalizações WebRTC entre usuários da mesma sala"""
        if room_id in self.video_rooms and target_user in self.video_rooms[room_id]:
            try:
                message = {
                    "type": "webrtc_signal",
                    "from_user": sender_user,
                    "signal_data": signal_data
                }
                await self.video_rooms[room_id][target_user].send_text(json.dumps(message))
                return True
            except Exception as e:
                print(f"Erro ao encaminhar sinal WebRTC: {e}")
                return False
        return False

    def disconnect(self, user_id: str, user_type: str):
        key = f"{user_type}_{user_id}"
        if key in self.user_connections:
            del self.user_connections[key]
            print(f"Usuario {user_type} {user_id} desconectado")

    async def send_notification(self, user_id: str, user_type: str, message: dict):
        key = f"{user_type}_{user_id}"
        if key in self.user_connections:
            try:
                await self.user_connections[key].send_text(json.dumps(message))
                print(f"Notificação enviada para {user_type} {user_id}")
                return True
            except Exception as e:
                print(f"Erro ao enviar notificação: {e}")
                # Remove conexão inválida
                del self.user_connections[key]
                return False
        else:
            print(f"Usuario {user_type} {user_id} não está conectado")
            return False

    async def notify_patient_consultation_started(self, patient_id: str, consultation_id: str, doctor_name: str, room_id: str):
        """Notifica paciente que consulta foi iniciada - também salva no banco"""
        from data.model.notificacao_model import Notificacao
        from data.repo.notificacao_repo import inserir_notificacao
        import json
        
        message = {
            "type": "consultation_started",
            "consultation_id": consultation_id,
            "doctor_name": doctor_name,
            "room_id": room_id,
            "message": f"Dr(a). {doctor_name} iniciou sua consulta. Clique para entrar na sala.",
            "timestamp": datetime.now().isoformat(),
            "persistent": True  # Indica que deve ser salva no banco
        }
        
        # Salvar no banco de dados
        try:
            notificacao = Notificacao(
                idNotificacao=None,
                idUsuario=int(patient_id),
                tipoUsuario="paciente",
                tipo="consulta_iniciada",
                titulo="Consulta Iniciada",
                mensagem=message["message"],
                lida=False,
                dadosAdicionais=json.dumps({
                    "consultation_id": consultation_id,
                    "doctor_name": doctor_name,
                    "room_id": room_id
                }),
                acaoRequerida=False
            )
            inserir_notificacao(notificacao)
        except Exception as e:
            print(f"Erro ao salvar notificação de consulta iniciada: {e}")
        
        return await self.send_notification(patient_id, "paciente", message)

    async def notify_patient_consultation_ended(self, patient_id: str, consultation_id: str, doctor_name: str):
        """Notifica paciente que consulta foi finalizada"""
        message = {
            "type": "consultation_ended",
            "consultation_id": consultation_id,
            "doctor_name": doctor_name,
            "message": f"Sua consulta com Dr(a). {doctor_name} foi finalizada.",
            "timestamp": datetime.now().isoformat(),
            "persistent": False  # Não precisa salvar no banco
        }
        return await self.send_notification(patient_id, "paciente", message)

    async def notify_doctor_patient_joined(self, doctor_id: str, patient_name: str, room_id: str):
        """Notifica médico que paciente entrou na sala"""
        message = {
            "type": "patient_joined",
            "patient_name": patient_name,
            "room_id": room_id,
            "message": f"Paciente {patient_name} entrou na sala de consulta.",
            "timestamp": datetime.now().isoformat(),
            "persistent": False  # Não precisa salvar no banco
        }
        return await self.send_notification(doctor_id, "medico", message)

    async def notify_new_appointment(self, doctor_id: str, patient_name: str, appointment_date: str, appointment_time: str, appointment_id: int):
        """Notifica médico sobre novo agendamento - salva no banco"""
        from data.repo.notificacao_repo import criar_notificacao_agendamento
        
        try:
            # Salvar no banco de dados
            notification_id = criar_notificacao_agendamento(
                id_medico=int(doctor_id),
                nome_paciente=patient_name,
                data_consulta=appointment_date,
                horario=appointment_time,
                agendamento_id=appointment_id
            )
            
            # Enviar notificação em tempo real
            message = {
                "type": "novo_agendamento",
                "titulo": "Nova Consulta Agendada",
                "mensagem": f"{patient_name} agendou uma consulta para {appointment_date} às {appointment_time}",
                "patient_name": patient_name,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
                "appointment_id": appointment_id,
                "notification_id": notification_id,
                "timestamp": datetime.now().isoformat(),
                "persistent": True
            }
            
            await self.send_notification(doctor_id, "medico", message)
            return notification_id
            
        except Exception as e:
            print(f"Erro ao notificar novo agendamento: {e}")
            return None

    async def notify_appointment_reminder(self, patient_id: str, doctor_name: str, appointment_date: str, appointment_time: str, appointment_id: int):
        """Notifica paciente 24h antes da consulta para confirmação - salva no banco"""
        from data.repo.notificacao_repo import criar_notificacao_confirmacao_consulta
        
        try:
            # Salvar no banco de dados
            notification_id = criar_notificacao_confirmacao_consulta(
                id_paciente=int(patient_id),
                nome_medico=doctor_name,
                data_consulta=appointment_date,
                horario=appointment_time,
                agendamento_id=appointment_id
            )
            
            # Enviar notificação em tempo real
            message = {
                "type": "confirmacao_consulta",
                "titulo": "Confirme sua Presença",
                "mensagem": f"Sua consulta com Dr(a). {doctor_name} está marcada para amanhã ({appointment_time}). Você confirmará presença?",
                "doctor_name": doctor_name,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
                "appointment_id": appointment_id,
                "notification_id": notification_id,
                "timestamp": datetime.now().isoformat(),
                "persistent": True,
                "acaoRequerida": True
            }
            
            await self.send_notification(patient_id, "paciente", message)
            return notification_id
            
        except Exception as e:
            print(f"Erro ao notificar lembrete de consulta: {e}")
            return None

    async def send_persistent_notification(self, user_id: str, user_type: str, notification_data: dict):
        """Envia notificação que será salva no banco e enviada em tempo real"""
        from data.model.notificacao_model import Notificacao
        from data.repo.notificacao_repo import inserir_notificacao
        import json
        
        try:
            # Salvar no banco
            notificacao = Notificacao(
                idNotificacao=None,
                idUsuario=int(user_id),
                tipoUsuario=user_type,
                tipo=notification_data.get("type", "geral"),
                titulo=notification_data.get("titulo", "Notificação"),
                mensagem=notification_data.get("mensagem", ""),
                lida=False,
                dadosAdicionais=json.dumps(notification_data.get("dados_extras", {})),
                acaoRequerida=notification_data.get("acao_requerida", False)
            )
            
            notification_id = inserir_notificacao(notificacao)
            
            # Adicionar ID da notificação aos dados
            notification_data["notification_id"] = notification_id
            notification_data["persistent"] = True
            notification_data["timestamp"] = datetime.now().isoformat()
            
            # Enviar em tempo real
            await self.send_notification(user_id, user_type, notification_data)
            
            return notification_id
            
        except Exception as e:
            print(f"Erro ao enviar notificação persistente: {e}")
            return None

    def get_connected_users(self):
        """Retorna lista de usuários conectados"""
        return list(self.user_connections.keys())

    async def notify_appointment_confirmation_needed(self, patient_id: str, agendamento_id: int, data_consulta: str, horario_consulta: str):
        """Notifica paciente que precisa confirmar consulta"""
        # Calcular se é para amanhã ou hoje
        data_consulta_obj = datetime.strptime(data_consulta, "%Y-%m-%d")
        hoje = datetime.now().date()
        amanha = hoje + timedelta(days=1)
        
        if data_consulta_obj.date() == amanha:
            periodo = "amanhã"
        elif data_consulta_obj.date() == hoje:
            periodo = "hoje"
        else:
            periodo = f"em {data_consulta}"
        
        message = {
            "type": "appointment_confirmation_needed",
            "agendamento_id": agendamento_id,
            "data_consulta": data_consulta,
            "horario_consulta": horario_consulta,
            "titulo": "Confirmar Consulta",
            "message": f"Você tem uma consulta {periodo} às {horario_consulta}. Confirme sua presença.",
            "timestamp": datetime.now().isoformat(),
            "persistent": True,  # Salvar no banco
            "acao_requerida": True,
            "acoes": [
                {"tipo": "confirmar", "texto": "Confirmar", "classe": "btn-success"},
                {"tipo": "cancelar", "texto": "Cancelar", "classe": "btn-danger"}
            ]
        }
        
        # Enviar notificação persistente
        return await self.send_persistent_notification(
            user_id=patient_id,
            user_type="paciente",
            notification_data=message
        )

# Instância global do gerenciador
manager = ConnectionManager()