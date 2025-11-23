from fastapi import WebSocket
from typing import Dict, List
import json
import asyncio
import time
from datetime import datetime

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
        message = {
            "type": "consultation_started",
            "consultation_id": consultation_id,
            "doctor_name": doctor_name,
            "room_id": room_id,
            "message": f"Dr(a). {doctor_name} iniciou sua consulta. Clique para entrar na sala.",
            "timestamp": datetime.now().isoformat()
        }
        return await self.send_notification(patient_id, "paciente", message)

    async def notify_patient_consultation_ended(self, patient_id: str, consultation_id: str, doctor_name: str):
        message = {
            "type": "consultation_ended",
            "consultation_id": consultation_id,
            "doctor_name": doctor_name,
            "message": f"Sua consulta com Dr(a). {doctor_name} foi finalizada.",
            "timestamp": datetime.now().isoformat()
        }
        return await self.send_notification(patient_id, "paciente", message)

    async def notify_doctor_patient_joined(self, doctor_id: str, patient_name: str, room_id: str):
        message = {
            "type": "patient_joined",
            "patient_name": patient_name,
            "room_id": room_id,
            "message": f"Paciente {patient_name} entrou na sala de consulta.",
            "timestamp": datetime.now().isoformat()
        }
        return await self.send_notification(doctor_id, "medico", message)

    def get_connected_users(self):
        """Retorna lista de usuários conectados"""
        return list(self.user_connections.keys())

# Instância global do gerenciador
manager = ConnectionManager()