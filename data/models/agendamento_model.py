from dataclasses import dataclass


@dataclass
class Agendamento:
    idAgendamento: int
    status: str
    dataAgendamento: str
    idPaciente: int