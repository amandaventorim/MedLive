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

    async def connect(self, websocket: WebSocket, user_id: str, user_type: str):
        await websocket.accept()
        key = f"{user_type}_{user_id}"
        self.user_connections[key] = websocket
        print(f"Usuario {user_type} {user_id} conectado via WebSocket")

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