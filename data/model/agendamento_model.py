from dataclasses import dataclass
from typing import Optional


@dataclass
class Agendamento:
    idAgendamento: int
    idPaciente: int
    idMedico: int
    dataAgendamento: str
    horario: str
    status: str = "agendado"
    queixa: str = ""
    preco: float = 0.0
    dataInclusao: Optional[str] = None
    