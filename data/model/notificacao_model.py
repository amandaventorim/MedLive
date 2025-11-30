from dataclasses import dataclass
from typing import Optional


@dataclass
class Notificacao:
    idNotificacao: Optional[int]
    idUsuario: int  # ID do usuário que vai receber a notificação
    tipoUsuario: str  # 'medico' ou 'paciente'
    tipo: str  # Tipo da notificação: 'agendamento', 'consulta_iniciada', 'confirmacao_consulta', 'resposta_confirmacao', etc.
    titulo: str  # Título da notificação
    mensagem: str  # Mensagem da notificação
    lida: bool = False  # Se a notificação foi lida
    dataInclusao: Optional[str] = None  # Data de criação
    dadosAdicionais: Optional[str] = None  # JSON com dados extras (agendamento_id, etc.)
    acaoRequerida: bool = False  # Se requer ação do usuário (confirmar consulta, etc.)
    expiresAt: Optional[str] = None  # Data de expiração da notificação