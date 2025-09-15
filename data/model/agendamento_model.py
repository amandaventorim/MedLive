from dataclasses import dataclass


@dataclass
class Agendamento:
    idAgendamento: int
    idPaciente: int
    status: str
    dataAgendamento: str
    queixa: str = ""
    idMedico: str = ""
    